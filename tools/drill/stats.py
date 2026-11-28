"""`review.py stats`: progress, weakest topics, why you fail, how long you take, quiz and cold-solve record."""
from collections import Counter
from datetime import timedelta
from statistics import median

from drill.picks import folder_of
from drill.schedule import TARGET_MINUTES

WINDOW_DAYS = 30


def records(notes, entries):
    """(note, history record) for every review ever logged."""
    by_number = {str(n.number): n for n in notes}
    return [(by_number[k], h) for k, e in entries.items() if k in by_number for h in e["history"]]


def weakest_topics(reviews, top=5, min_reviews=2):
    totals, fails = Counter(), Counter()
    for note, rec in reviews:
        totals[folder_of(note)] += 1
        fails[folder_of(note)] += rec["grade"] == "fail"
    rated = [(fails[f] / totals[f], f) for f in totals if totals[f] >= min_reviews and fails[f]]
    return [(f, fails[f], totals[f]) for _, f in sorted(rated, key=lambda rf: (-rf[0], rf[1]))[:top]]


def minutes_by_difficulty(reviews):
    """{difficulty: (median minutes, reviews timed, target)} for reviews logged with --mins."""
    timed = {}
    for note, rec in reviews:
        if "mins" in rec and rec["grade"] != "fail":
            timed.setdefault(note.difficulty, []).append(rec["mins"])
    return {d: (median(m), len(m), TARGET_MINUTES[d]) for d, m in timed.items()}


def recent(rows, today, days=WINDOW_DAYS):
    since = (today - timedelta(days=days)).isoformat()
    return [r for r in rows if r["date"] >= since]


def summary(notes, state, today):
    entries = state["notes"]
    reviews = records(notes, entries)
    todo = [n for n in notes if n.status == "🔄"]
    never_checked = [n for n in notes if n.status == "✅" and str(n.number) not in entries]
    due = [k for k, e in entries.items() if e["due"] <= today.isoformat()]
    lines = [f"{len(notes)} notes · ✅ {len(notes) - len(todo)} · 🔄 {len(todo)} · reviewed at least once "
             f"{len(entries)} · due today {len(due)} · ✅ never re-checked {len(never_checked)}"]
    by_folder = Counter(folder_of(n) for n in todo)
    if by_folder:
        lines.append("🔄 left by topic: " + ", ".join(f"{f} {c}" for f, c in by_folder.most_common()))
    weak = weakest_topics(reviews)
    if weak:
        lines.append("Weakest topics (fails / reviews): " + ", ".join(f"{f} {x}/{t}" for f, x, t in weak))
    reasons = Counter(rec["why"] for _, rec in reviews if rec.get("why"))
    if reasons:
        lines.append("Why reviews went wrong: " + ", ".join(f"{r} {c}" for r, c in reasons.most_common()))
    for difficulty, (med, count, target) in sorted(minutes_by_difficulty(reviews).items(),
                                                   key=lambda kv: list(TARGET_MINUTES).index(kv[0])):
        flag = "on target" if med <= target else f"{med - target:g} min over"
        lines.append(f"Time, {difficulty}: median {med:g} min over {count} timed solves (target {target}) — {flag}")
    quiz = recent(state["quiz"], today)
    if quiz:
        right = sum(1 for q in quiz if q["ok"])
        lines.append(f"Pattern quiz, last {WINDOW_DAYS} days: {right}/{len(quiz)} named correctly")
    cold = recent(state["cold"], today)
    if cold:
        passed = sum(1 for c in cold if c["result"] == "pass")
        lines.append(f"Cold solves (unseen problems), last {WINDOW_DAYS} days: {passed}/{len(cold)} solved")
    return "\n".join(lines)
