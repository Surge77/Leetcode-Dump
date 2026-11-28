"""Practice drill over the notes: spaced repetition, an attempt judge, a pattern quiz and a debug drill.

    python tools/review.py                        # today's problems (same picks all day)
    python tools/review.py today -n 5 --sheet neetcode   # more picks, only from one sheet
    python tools/review.py log 322 ok --mins 24   # graded fail | hard | ok | easy ("pass" = ok)
    python tools/review.py log 322 fail --why edge --mins 31 --note "forgot the empty-amount base case"
    python tools/review.py today --company google      # only problems asked at a company (COMPANIES.md)
    python tools/review.py check 322 my_322.py --log --mins 24   # judge your file, then log the result
    python tools/review.py show 322               # reveal the note
    python tools/review.py quiz -n 10             # statement only: name the pattern
    python tools/review.py debug 322              # find the planted bug in a verified solution
    python tools/review.py cold two-sum pass --mins 12 --difficulty Easy --source contest
    python tools/review.py plan --by 2027-01-15 --sheet neetcode
    python tools/review.py stats

Today's list shows only the title, difficulty and link, never the folder: naming the pattern is half
the problem. Reviews are spaced 1 → 3 → 7 → 16 → 35 → 75 → 150 → 300 days (see drill/schedule.py).
Two non-fail reviews in a row flip a note to ✅ Solved, a fail flips it back to 🔄, and INDEX.md is
rebuilt either way. Never-reviewed ✅ notes are drawn too, so old "solved" marks get re-checked.
Progress lives in tools/review_state.json — commit it to keep it across machines.
"""
import argparse
import random
import re
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from build_index import REPO, checked_notes, write_index  # noqa: E402
from drill import attempt, mutate, plan, quiz, stats  # noqa: E402
from drill.picks import pick, scope  # noqa: E402
from drill.schedule import GRADES, REASON_HELP, REASONS, logged_on, new_status_after, schedule  # noqa: E402
from drill.sections import link  # noqa: E402
from drill.state import load_state, save_state  # noqa: E402

DEFAULT_PICKS = 3
PRACTICE_DIR = REPO / "practice"  # gitignored scratch space for attempts and debug drills
STATUS_LINE_RE = re.compile(r"^(\*\*🟢 Status:\*\* ).*$", re.M)
ATTEMPTS_RE = re.compile(r"(^## 🔹 My Attempts\n)(.*?)(?=^## |\Z)", re.M | re.S)


def set_status(path, status):
    """Rewrite the note's status line to `status` ("✅ Solved" or "🔄 Need Review")."""
    text = path.read_text(encoding="utf-8")
    new = STATUS_LINE_RE.sub(lambda m: m.group(1) + status, text, count=1)
    if new != text:
        path.write_text(new, encoding="utf-8", newline="\n")
    return new != text


def add_attempt(path, line):
    """Append one line to the note's '## 🔹 My Attempts' section (dropping the italic placeholder)."""
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    match = ATTEMPTS_RE.search(text)
    if not match:
        return False
    kept = [ln for ln in match.group(2).strip("\n").split("\n") if ln.strip() and not ln.startswith("*One line per attempt")]
    body = "\n".join(kept + [f"- {line}"]) + "\n"
    rest = text[match.end():]
    new = text[:match.start(2)] + "\n" + body + ("\n" + rest if rest else "")
    path.write_text(new, encoding="utf-8", newline="\n")
    return True


def attempt_line(today, grade, mins=None, why=None, note=None):
    parts = [today.isoformat()] + ([f"{mins} min"] if mins is not None else []) + [grade]
    detail = ": ".join(p for p in (why, note) if p)
    return " · ".join(parts + ([detail] if detail else []))


def find(notes, number):
    for note in notes:
        if note.number == number:
            return note
    raise SystemExit(f"no note #{number}")


def link_of(note):
    return link(note.path.read_text(encoding="utf-8")) or "(no link)"


def cmd_today(notes, state, today, count):
    rng = random.Random(today.toordinal())  # the same picks all day
    picks = pick(notes, state["notes"], today, count, rng)
    if not picks:
        print("Nothing due and nothing new in this scope. 🎉")
        return
    print(f"Review for {today} — solve each unaided, then `python tools/review.py check <#> <file>` "
          "or `log <#> <grade>`\n")
    for note in picks:
        e = state["notes"].get(str(note.number))
        tag = "done" if logged_on(e, today) else "review" if e else "re-check" if note.status == "✅" else "new"
        print(f"  {note.number:>5}  {note.title:<55} {note.difficulty:<6} {tag:<8} {link_of(note)}")


def log_review(notes, state, today, number, grade, mins=None, why=None, note_text=None):
    note = find(notes, number)
    entries = state["notes"]
    if logged_on(entries.get(str(number)), today):
        raise SystemExit(f"#{number} was already logged today; one review per day "
                         "(two same-day passes would mark it solved without spacing)")
    entry = schedule(entries.get(str(number)), grade, today, solved_before=note.status == "✅", mins=mins, why=why)
    entries[str(number)] = entry
    save_state(state)
    new_status = new_status_after(grade, entry["streak"])
    changed = new_status is not None and set_status(note.path, new_status)
    add_attempt(note.path, attempt_line(today, grade, mins, why, note_text))
    if changed:
        write_index()
    message = f"#{number}: {grade} → streak {entry['streak']}, next review {entry['due']}"
    print(message + (f"; status → {new_status}" if changed else ""))


def cmd_check(notes, state, today, args):
    note = find(notes, args.number)
    verdict = attempt.check(args.number, attempt.read_solution(args.file), timing=not args.no_timing)
    print(verdict.report)
    print(f"\n#{note.number} {note.title}: {'ACCEPTED' if verdict.passed else 'REJECTED'}")
    if args.log:
        grade = args.grade if verdict.passed else "fail"
        why = None if verdict.passed else ("tle" if verdict.tle else args.why or "bug")
        log_review(notes, state, today, args.number, grade, args.mins, why, args.note)
    return 0 if verdict.passed else 1


def cmd_debug(notes, args):
    if args.reveal:
        print(mutate.reveal(PRACTICE_DIR, args.number))
        return 0
    note = find(notes, args.number)
    code = attempt.load_harness().blocks_of(note.path)[-1]
    result = mutate.plant(args.number, code, mutate.new_rng(args.seed))
    if result is None:
        raise SystemExit(f"#{args.number}: no single-token bug was caught by its checks; try another note")
    target = mutate.write_drill(PRACTICE_DIR, args.number, note.title, result)
    print(f"Planted one bug in {target.relative_to(REPO).as_posix()} — find it, fix it, then\n"
          f"    python tools/review.py check {args.number} {target.relative_to(REPO).as_posix()}")
    return 0


def cmd_quiz(notes, state, today, args):
    rng = random.Random(args.seed)
    cards = quiz.draw(quiz.candidates(notes), args.n, rng)
    results = quiz.run(cards, today, interactive=not args.no_input)
    if results:
        state["quiz"] += results
        save_state(state)
        print(f"\n{sum(r['ok'] for r in results)}/{len(results)} named correctly")


def cmd_cold(state, today, args):
    record = {"date": today.isoformat(), "problem": args.problem, "result": args.result}
    for key in ("mins", "difficulty", "source"):
        if getattr(args, key) is not None:
            record[key] = getattr(args, key)
    state["cold"].append(record)
    save_state(state)
    print(f"cold solve logged: {args.problem} {args.result}")


def parser():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd")

    def scoped(cmd, help_text):
        s = sub.add_parser(cmd, help=help_text)
        s.add_argument("--sheet", help="only problems of this sheet (e.g. neetcode, grind, 'top interview')")
        s.add_argument("--topic", help="only folders or tags containing this text (e.g. dp, graph, monotonic)")
        s.add_argument("--company", help="only problems asked at this company (see COMPANIES.md)")
        return s

    scoped("today", "today's problems").add_argument("-n", type=int, default=DEFAULT_PICKS)
    log = sub.add_parser("log", help="record a review")
    log.add_argument("number", type=int)
    log.add_argument("grade", choices=GRADES + ("pass",))
    log.add_argument("--mins", type=int, help="minutes it took")
    log.add_argument("--why", choices=REASONS, help="; ".join(f"{k}: {v}" for k, v in REASON_HELP.items()))
    log.add_argument("--note", help="what tripped you up; added to the note's My Attempts section")
    sub.add_parser("show", help="reveal a note's path").add_argument("number", type=int)
    sub.add_parser("stats", help="progress, weak topics, timing")
    pl = scoped("plan", "daily load needed to finish by a date")
    pl.add_argument("--by", required=True, type=date.fromisoformat, help="deadline, YYYY-MM-DD")
    qz = scoped("quiz", "name the pattern from the statement alone")
    qz.add_argument("-n", type=int, default=5)
    qz.add_argument("--seed", type=int)
    qz.add_argument("--no-input", action="store_true", help="print the cards, answers at the end")
    ck = sub.add_parser("check", help="judge your solution file with the note's checks")
    ck.add_argument("number", type=int)
    ck.add_argument("file")
    ck.add_argument("--log", action="store_true", help="log the verdict as today's review")
    ck.add_argument("--grade", choices=("hard", "ok", "easy"), default="ok", help="grade logged if accepted")
    ck.add_argument("--mins", type=int)
    ck.add_argument("--why", choices=REASONS, help="reason logged if rejected (default: bug, or tle)")
    ck.add_argument("--no-timing", action="store_true", help="do not enforce the max-size time limit")
    ck.add_argument("--note", help="what tripped you up; added to the note's My Attempts section")
    db = sub.add_parser("debug", help="find a planted bug in a verified solution")
    db.add_argument("number", type=int)
    db.add_argument("--reveal", action="store_true")
    db.add_argument("--seed", type=int)
    cd = sub.add_parser("cold", help="log an attempt at a problem NOT in this repo")
    cd.add_argument("problem", help="slug or URL")
    cd.add_argument("result", choices=("pass", "fail"))
    cd.add_argument("--mins", type=int)
    cd.add_argument("--difficulty", choices=("Easy", "Medium", "Hard"))
    cd.add_argument("--source", choices=("contest", "oa", "interview", "other"))
    return p


def utf8_stdout():
    """Print ✓ ✅ → etc. even when stdout is a pipe on Windows (default cp1252 cannot encode them)."""
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if callable(reconfigure):
        reconfigure(encoding="utf-8", errors="replace")


def main(argv=None):
    args = parser().parse_args(argv)
    utf8_stdout()
    notes, state, today = checked_notes(), load_state(), date.today()
    cmd = args.cmd or "today"
    if cmd in ("today", "plan", "quiz"):
        notes = scope(notes, args.sheet, args.topic, company=args.company)
    if cmd == "today":
        cmd_today(notes, state, today, getattr(args, "n", DEFAULT_PICKS))
    elif cmd == "log":
        log_review(notes, state, today, args.number, args.grade, args.mins, args.why, args.note)
    elif cmd == "show":
        print(find(notes, args.number).path.relative_to(REPO).as_posix())
    elif cmd == "stats":
        print(stats.summary(notes, state, today))
    elif cmd == "plan":
        print(plan.render(plan.plan(notes, state["notes"], today, args.by), args.by))
    elif cmd == "quiz":
        cmd_quiz(notes, state, today, args)
    elif cmd == "check":
        return cmd_check(notes, state, today, args)
    elif cmd == "debug":
        return cmd_debug(notes, args)
    elif cmd == "cold":
        cmd_cold(state, today, args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
