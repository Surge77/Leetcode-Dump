"""Which notes to practise today, and narrowing the pool to a sheet or a topic."""
import json
from pathlib import Path

from drill.schedule import logged_on

REPO = Path(__file__).resolve().parents[2]
SHEETS_FILE = REPO / "tools" / "sheets.json"
EXAM_WEIGHT = 3  # new problems from exam-heavy topics are drawn this many times as often
EXAM_FOLDERS = ("DP", "Graph", "Math_Number_Theory", "Segment_Tree", "Fenwick_Tree", "Union_Find",
                "Prefix_Sum", "Modified_Binary_search", "Greedy", "Tree_Binary_Lifting", "Meet_in_the_Middle",
                "String_Matching", "Game_Theory", "Intervals_Problems")


def folder_of(note):
    return note.path.relative_to(REPO).parts[0]


def weight(note):
    return EXAM_WEIGHT if folder_of(note).startswith(EXAM_FOLDERS) else 1


def sheet_numbers(name, sheets_file=SHEETS_FILE):
    """Problem numbers of the sheet whose name contains `name` (case-insensitive)."""
    sheets = json.loads(Path(sheets_file).read_text(encoding="utf-8"))
    hits = [s for s in sheets if name.lower() in s.lower()]
    if len(hits) != 1:
        raise SystemExit(f"--sheet {name!r} matches {hits or 'no sheet'}; sheets: {', '.join(sheets)}")
    return {num for topic in sheets[hits[0]]["topics"] for num in topic["problems"]}


def scope(notes, sheet=None, topic=None, sheets_file=SHEETS_FILE):
    """Notes in the chosen sheet and/or whose folder contains `topic` (case-insensitive)."""
    if sheet:
        wanted = sheet_numbers(sheet, sheets_file)
        notes = [n for n in notes if n.number in wanted]
    if topic:
        notes = [n for n in notes if topic.lower() in folder_of(n).lower()]
        if not notes:
            raise SystemExit(f"--topic {topic!r} matches no folder")
    return notes


def pick(notes, entries, today, count, rng):
    """Due reviews first, then never-reviewed notes drawn by topic weight.

    Never-reviewed ✅ notes are drawn too: they were marked solved before the drill existed, so they
    have never been checked. Both pools are rebuilt as they stood at the START of `today`, so logging
    a review does not reshuffle the rest of the day's list.
    """
    iso = today.isoformat()

    def entry(n):
        return entries.get(str(n.number))

    def first_logged_today(e):
        return bool(e) and bool(e["history"]) and e["history"][0]["date"] == iso

    def due_this_morning(e):
        return bool(e) and not first_logged_today(e) and (e["due"] <= iso or logged_on(e, today))

    picks = [n for n in notes if due_this_morning(entry(n))][:count]
    fresh = [n for n in notes if entry(n) is None or first_logged_today(entry(n))]
    while len(picks) < count and fresh:
        chosen = rng.choices(fresh, weights=[weight(n) for n in fresh])[0]
        fresh.remove(chosen)
        picks.append(chosen)
    return picks
