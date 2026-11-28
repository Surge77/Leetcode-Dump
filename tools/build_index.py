"""Enforce the note format and regenerate every generated file.

    python tools/build_index.py           # fix note links, check the format, rewrite the generated files
    python tools/build_index.py --check   # exit 1 on a format error, a stale link or a stale file (CI, pre-commit)

Generated: INDEX.md, SHEETS.md, TAGS.md, COMPANIES.md, each folder's README.md ladder block, and the README
numbers block. The note format itself is documented in tools/notebook/model.py.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from notebook import links, pages, render  # noqa: E402
from notebook.model import (DIFFICULTIES, HEADER_RE, REPO, STATUSES, Note, load_notes,  # noqa: E402,F401
                            note_paths, parse, taxonomy)
from notebook.render import STATS_END, STATS_START, render_stats  # noqa: E402,F401

README = REPO / "README.md"


def with_stats(readme, notes):
    return render.with_block(readme, STATS_START, STATS_END, render_stats(notes), "README.md")


def checked_notes():
    """All notes, or SystemExit listing every format error."""
    notes, errors = load_notes()
    if errors:
        sys.exit("Note format errors:\n  " + "\n  ".join(errors))
    return notes


def note_titles():
    """{number: title} read straight from each note's '# N. Title' line (works before the full lint passes)."""
    titles = {}
    for path in note_paths():
        match = HEADER_RE.search(path.read_text(encoding="utf-8"))
        if match:
            titles[int(match.group(1))] = match.group(2).strip()
    return titles


def generated(notes):
    """{output file: expected content} for every generated document."""
    readme = README.read_text(encoding="utf-8").replace("\r\n", "\n")
    out = {REPO / "INDEX.md": render.render_index(notes), REPO / "SHEETS.md": render.render_sheets(notes),
           REPO / "TAGS.md": render.render_tags(notes), README: with_stats(readme, notes)}
    companies = pages.render_companies(notes)
    if companies is not None:
        out[REPO / "COMPANIES.md"] = companies
    out.update(pages.pattern_pages(notes))
    return out


def write(path, content):
    path.write_text(content, encoding="utf-8", newline="\n")


def write_index():
    """Fix links, then rewrite every generated file; return the number of notes."""
    for path, text in links.updated_files(note_titles()).items():
        write(path, text)
    notes = checked_notes()
    for target, content in generated(notes).items():
        write(target, content)
    return len(notes)


def main():
    if "--check" not in sys.argv:
        print(f"{write_index()} notes well-formed; links fixed; generated files rewritten")
        return
    stale_links = links.updated_files(note_titles())
    if stale_links:
        names = ", ".join(p.relative_to(REPO).as_posix() for p in list(stale_links)[:5])
        sys.exit(f"stale note links in {len(stale_links)} file(s) ({names}…): run `python tools/build_index.py`")
    notes = checked_notes()
    for target, content in generated(notes).items():
        current = target.read_text(encoding="utf-8") if target.exists() else ""
        if current.replace("\r\n", "\n") != content:
            sys.exit(f"{target.relative_to(REPO).as_posix()} is stale: run `python tools/build_index.py`")
    print(f"{len(notes)} notes well-formed; links and generated files are up to date")


if __name__ == "__main__":
    main()
