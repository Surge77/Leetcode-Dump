"""Spaced-repetition drill over the 🔄 Need Review notes.

    python tools/review.py                 # today's problems (same picks all day)
    python tools/review.py today -n 5      # ask for more
    python tools/review.py log 322 pass    # solved it unaided, cleanly
    python tools/review.py log 322 fail    # needed the note, or got it wrong
    python tools/review.py show 322        # reveal the note (and its pattern folder)
    python tools/review.py stats

Today's list shows only the title, difficulty and LeetCode link, never the folder:
naming the pattern is half the problem. A pass schedules the next review further
out (1, 3, 7, 16, 35 days); a fail resets to tomorrow. Two passes in a row flip the
note to ✅ Solved, a fail flips it back to 🔄, and INDEX.md is rebuilt either way.
Progress lives in tools/review_state.json — commit it to keep it across machines.
"""
import argparse
import json
import random
import re
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from build_index import REPO, checked_notes, write_index  # noqa: E402

STATE_FILE = HERE / "review_state.json"
INTERVALS = (1, 3, 7, 16, 35)  # days until the next review after the 1st, 2nd, ... consecutive pass
MASTERED_STREAK = 2
DEFAULT_PICKS = 3
EXAM_WEIGHT = 3  # new problems from exam-heavy topics are drawn this many times as often
EXAM_FOLDERS = ("DP", "Graph", "Math_Number_Theory", "Segment_Tree", "Fenwick_Tree", "Union_Find",
                "Prefix_Sum", "Modified_Binary_search", "Greedy", "Tree_Binary_Lifting", "Meet_in_the_Middle",
                "String_Matching", "Game_Theory", "Intervals_Problems")
STATUS_LINE_RE = re.compile(r"^(\*\*🟢 Status:\*\* ).*$", re.M)
LINK_RE = re.compile(r"https://leetcode\.com/problems/[\w-]+/?")


def load_state(path=STATE_FILE):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(state, path=STATE_FILE):
    ordered = dict(sorted(state.items(), key=lambda kv: int(kv[0])))
    path.write_text(json.dumps(ordered, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def schedule(entry, passed, today):
    """Return a NEW state entry after a review on `today` (entry may be None for a first review)."""
    entry = entry or {"streak": 0, "history": []}
    streak = entry["streak"] + 1 if passed else 0
    wait = INTERVALS[min(entry["streak"], len(INTERVALS) - 1)] if passed else 1
    return {
        "streak": streak,
        "due": (today + timedelta(days=wait)).isoformat(),
        "history": entry["history"] + [f"{today.isoformat()}:{'pass' if passed else 'fail'}"],
    }


def logged_on(entry, day):
    return bool(entry) and any(h.startswith(day.isoformat()) for h in entry["history"])


def weight(note):
    folder = note.path.relative_to(REPO).parts[0]
    return EXAM_WEIGHT if folder.startswith(EXAM_FOLDERS) else 1


def pick(notes, state, today, count, rng):
    """Due reviews first (most overdue first), then new 🔄 notes drawn by topic weight."""
    due = sorted((n for n in notes if str(n.number) in state and state[str(n.number)]["due"] <= today.isoformat()),
                 key=lambda n: (state[str(n.number)]["due"], n.number))
    picks = due[:count]
    fresh = [n for n in notes if n.status == "🔄" and str(n.number) not in state]
    while len(picks) < count and fresh:
        chosen = rng.choices(fresh, weights=[weight(n) for n in fresh])[0]
        fresh.remove(chosen)
        picks.append(chosen)
    return picks


def set_status(path, status):
    """Rewrite the note's status line to `status` ("✅ Solved" or "🔄 Need Review")."""
    text = path.read_text(encoding="utf-8")
    new = STATUS_LINE_RE.sub(lambda m: m.group(1) + status, text, count=1)
    if new != text:
        path.write_text(new, encoding="utf-8", newline="\n")
    return new != text


def link_of(note):
    match = LINK_RE.search(note.path.read_text(encoding="utf-8"))
    return match.group(0) if match else "(no link)"


def find(notes, number):
    for note in notes:
        if note.number == number:
            return note
    raise SystemExit(f"no note #{number}")


def cmd_today(notes, state, today, count):
    rng = random.Random(today.toordinal())  # the same picks all day
    picks = pick(notes, state, today, count, rng)
    if not picks:
        print("Nothing due and no 🔄 notes left. 🎉")
        return
    print(f"Review for {today} — solve each unaided, then `python tools/review.py log <#> pass|fail`\n")
    for note in picks:
        tag = "review" if str(note.number) in state else "new"
        print(f"  {note.number:>5}  {note.title:<55} {note.difficulty:<6} {tag:<6} {link_of(note)}")


def cmd_log(notes, state, today, number, passed):
    note = find(notes, number)
    if logged_on(state.get(str(number)), today):
        raise SystemExit(f"#{number} was already logged today; one review per day "
                         "(two same-day passes would mark it solved without spacing)")
    entry = schedule(state.get(str(number)), passed, today)
    state = {**state, str(number): entry}
    save_state(state)
    new_status = new_status_after(passed, entry["streak"])
    changed = new_status is not None and set_status(note.path, new_status)
    if changed:
        write_index()
    message = f"#{number}: {'pass' if passed else 'fail'} → streak {entry['streak']}, next review {entry['due']}"
    print(message + (f"; status → {new_status}" if changed else ""))


def new_status_after(passed, streak):
    """✅ after MASTERED_STREAK passes in a row, 🔄 after any fail, otherwise unchanged (None)."""
    if not passed:
        return "🔄 Need Review"
    return "✅ Solved" if streak >= MASTERED_STREAK else None


def cmd_stats(notes, state, today):
    reviewed = [n for n in notes if str(n.number) in state]
    due = [n for n in reviewed if state[str(n.number)]["due"] <= today.isoformat()]
    todo = [n for n in notes if n.status == "🔄"]
    print(f"{len(notes)} notes · ✅ {len(notes) - len(todo)} · 🔄 {len(todo)} · "
          f"reviewed at least once {len(reviewed)} · due today {len(due)}")
    by_folder = {}
    for note in todo:
        folder = note.path.relative_to(REPO).parts[0]
        by_folder[folder] = by_folder.get(folder, 0) + 1
    print("🔄 left by topic: " + ", ".join(f"{f} {c}" for f, c in sorted(by_folder.items(), key=lambda kv: -kv[1])))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd")
    today_cmd = sub.add_parser("today", help="today's problems")
    today_cmd.add_argument("-n", type=int, default=DEFAULT_PICKS, help=f"how many (default {DEFAULT_PICKS})")
    log_cmd = sub.add_parser("log", help="record a review")
    log_cmd.add_argument("number", type=int)
    log_cmd.add_argument("outcome", choices=("pass", "fail"))
    show_cmd = sub.add_parser("show", help="reveal a note's path")
    show_cmd.add_argument("number", type=int)
    sub.add_parser("stats", help="progress summary")
    args = parser.parse_args(argv)

    notes, state, today = checked_notes(), load_state(), date.today()
    if args.cmd in (None, "today"):
        cmd_today(notes, state, today, getattr(args, "n", DEFAULT_PICKS))
    elif args.cmd == "log":
        cmd_log(notes, state, today, args.number, args.outcome == "pass")
    elif args.cmd == "show":
        print(find(notes, args.number).path.relative_to(REPO).as_posix())
    else:
        cmd_stats(notes, state, today)
    return 0


if __name__ == "__main__":
    sys.exit(main())
