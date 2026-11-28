"""Create a new note from the template, plus a failing check stub you must fill in.

    python tools/new_note.py 2999 "Count Powerful Integers" --difficulty Hard --folder DP_Advanced --tags dp-digit
    python tools/new_note.py 1 "Two Sum" --difficulty Easy --folder Arrays_and_Hashing --tags hashing --slug two-sum

It writes <Folder>/<N>.<Title>.md from LeetcodeTemplates/ActiveTemplate.md and appends a @case(N) stub to
tools/verify/tests_<folder>.py that raises until you replace it with real checks, so a note can never land
without tests. Then: write the note and both solutions, write the checks, run
`python tools/verify/verify.py N` and `python tools/build_index.py`.
"""
import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from notebook.model import DIFFICULTIES, REPO, check_tags, note_paths, taxonomy  # noqa: E402

TEMPLATE = REPO / "LeetcodeTemplates" / "ActiveTemplate.md"
VERIFY = REPO / "tools" / "verify"
STUB = '''

@case({number})
def _(h):
    brute, opt = h.lc_all({number}, "Solution")
    b, o = brute["Solution"](), opt["Solution"]()
    # 1. LeetCode's examples:   assert o.method(example_input) == expected
    # 2. Random inputs:         for _ in range(300): assert b.method(x) == o.method(x), x
    # 3. One max-size run:      timed_call(lambda: o.method(big_input), 2)  (from tests_b10)
    raise NotImplementedError("write the checks for #{number}, then delete this line")
'''


def file_name(number, title):
    cleaned = re.sub(r"[^\w()'.-]+", "_", title.strip()).strip("_")
    return f"{number}.{cleaned}.md"


def slug_of(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def tests_file(folder, verify_dir=VERIFY):
    return verify_dir / f"tests_{folder.lower()}.py"


def scaffold(number, title, difficulty, folder, tags, slug=None, repo=REPO, verify_dir=VERIFY):
    """Create the note and the check stub; return (note path, tests path). SystemExit on bad input."""
    if difficulty not in DIFFICULTIES:
        raise SystemExit(f"--difficulty must be one of {DIFFICULTIES}")
    errors = check_tags(tags, folder)
    if errors:
        raise SystemExit("; ".join(errors))
    existing = [p for p in note_paths(repo) if p.name.split(".", 1)[0] == str(number)]
    if existing:
        raise SystemExit(f"#{number} already has a note: {existing[0].relative_to(repo).as_posix()}")
    note = repo / folder / file_name(number, title)
    text = TEMPLATE.read_text(encoding="utf-8")
    for key, value in {"number": str(number), "title": title, "slug": slug or slug_of(title),
                       "difficulty": difficulty, "tags": ", ".join(tags)}.items():
        text = text.replace("{{" + key + "}}", value)
    note.parent.mkdir(parents=True, exist_ok=True)
    note.write_text(text, encoding="utf-8", newline="\n")
    tests = tests_file(folder, verify_dir)
    if not tests.exists():
        tests.write_text(f'"""Checks for the notes in {folder}/ added with tools/new_note.py."""\n'
                         "from harness import case  # noqa: F401\n", encoding="utf-8", newline="\n")
    with tests.open("a", encoding="utf-8", newline="\n") as f:
        f.write(STUB.format(number=number))
    return note, tests


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("number", type=int)
    p.add_argument("title")
    p.add_argument("--difficulty", required=True, choices=DIFFICULTIES)
    p.add_argument("--folder", required=True, choices=list(taxonomy()["folders"]))
    p.add_argument("--tags", required=True, help="comma-separated slugs from tools/taxonomy.json")
    p.add_argument("--slug", help="LeetCode URL slug (default: from the title)")
    args = p.parse_args(argv)
    tags = [t.strip() for t in args.tags.split(",") if t.strip()]
    note, tests = scaffold(args.number, args.title, args.difficulty, args.folder, tags, args.slug)
    print(f"created {note.relative_to(REPO).as_posix()} and a check stub in {tests.relative_to(REPO).as_posix()}\n"
          f"next: fill in the note, replace the stub, then `python tools/verify/verify.py {args.number}` "
          "and `python tools/build_index.py`")
    return 0


if __name__ == "__main__":
    sys.exit(main())
