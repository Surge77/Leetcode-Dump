"""Spaced-repetition scheduling.

A review is graded fail / hard / ok / easy ("pass" means ok). Each note sits on a step of INTERVALS:

* ok   waits INTERVALS[step] days, then moves one step up
* easy waits the NEXT step's interval and moves two steps up
* hard waits INTERVALS[step] days and stays on its step
* fail resets to step 0 and comes back tomorrow

The gaps keep growing (up to 300 days), so a mastered repo costs about 2 reviews a day, not 13.
Two non-fail reviews in a row mark a note ✅; a fail marks it 🔄 again.
"""
from datetime import timedelta

INTERVALS = (1, 3, 7, 16, 35, 75, 150, 300)
MASTERED_STREAK = 2
# A note that was already ✅ before its first drill review starts here, as if it had two passes.
SEEDED_STEP = 2
GRADES = ("fail", "hard", "ok", "easy")
ALIASES = {"pass": "ok"}
REASONS = ("pattern", "approach", "edge", "bug", "tle", "forgot", "other")
REASON_HELP = {
    "pattern": "did not recognise the pattern",
    "approach": "knew the pattern, could not build the solution",
    "edge": "missed an edge case",
    "bug": "implementation bug",
    "tle": "correct but too slow",
    "forgot": "forgot the key trick",
    "other": "anything else",
}
TARGET_MINUTES = {"Easy": 15, "Medium": 25, "Hard": 40}


def normalize_grade(grade):
    grade = ALIASES.get(grade, grade)
    if grade not in GRADES:
        raise ValueError(f"grade must be one of {GRADES + tuple(ALIASES)}, got {grade!r}")
    return grade


def schedule(entry, grade, today, solved_before=False, mins=None, why=None):
    """Return a NEW entry after a review on `today`. `entry` is None for a note's first review."""
    grade = normalize_grade(grade)
    if entry is None:
        seeded = solved_before
        entry = {"step": SEEDED_STEP if seeded else 0, "streak": MASTERED_STREAK if seeded else 0, "history": []}
    last = len(INTERVALS) - 1
    step = entry["step"]
    if grade == "fail":
        new_step, streak, wait = 0, 0, 1
    else:
        streak = entry["streak"] + 1
        wait = INTERVALS[min(step + (1 if grade == "easy" else 0), last)]
        new_step = min(step + {"hard": 0, "ok": 1, "easy": 2}[grade], last)
    record = {"date": today.isoformat(), "grade": grade}
    if mins is not None:
        record["mins"] = int(mins)
    if why:
        record["why"] = why
    return {"step": new_step, "streak": streak, "due": (today + timedelta(days=wait)).isoformat(),
            "history": entry["history"] + [record]}


def logged_on(entry, day):
    return bool(entry) and any(h["date"] == day.isoformat() for h in entry["history"])


def new_status_after(grade, streak):
    """✅ after MASTERED_STREAK non-fail reviews in a row, 🔄 after any fail, otherwise unchanged (None)."""
    if normalize_grade(grade) == "fail":
        return "🔄 Need Review"
    return "✅ Solved" if streak >= MASTERED_STREAK else None
