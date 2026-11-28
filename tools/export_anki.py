"""Export the notes as an Anki deck you can review on your phone.

    python tools/export_anki.py                      # every note → exports/leetcode-dump-anki.tsv
    python tools/export_anki.py --status review      # only the 🔄 notes
    python tools/export_anki.py --out deck.tsv

In Anki: File → Import → choose the .tsv. The file's header lines set the note type (Basic), the deck
(LeetCode-Dump), HTML and tags, and give every card a stable id, so importing a newer export UPDATES your
cards instead of duplicating them. No add-on or extra package is needed.

Front: the problem statement (title hidden — recognising the pattern is the point).
Back:  title + link, pattern, recognition signal, approach, complexity.
"""
import argparse
import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from build_index import REPO, checked_notes  # noqa: E402
from drill.picks import folder_of  # noqa: E402
from drill.sections import approach, complexity, link, signal, statement  # noqa: E402

DEFAULT_OUT = REPO / "exports" / "leetcode-dump-anki.tsv"
HEADER = ["#separator:tab", "#html:true", "#notetype:Basic", "#deck:LeetCode-Dump", "#guid column:1",
          "#tags column:4"]


def to_html(markdown):
    """The little Markdown the notes use (`code`, **bold**, bullets, line breaks) as Anki-safe HTML."""
    out = []
    for line in markdown.replace("\t", "    ").splitlines():
        text = html.escape(line.strip())
        text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
        text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
        text = re.sub(r"^[*-] ", "• ", text)
        out.append(text)
    return re.sub(r"^(<br>)+|(<br>)+$", "", "<br>".join(out))


def card(note):
    text = note.path.read_text(encoding="utf-8")
    front = "<b>Which pattern solves this?</b><br><br>" + to_html(statement(text) or note.title)
    url = link(text)
    back = [f"<b>{note.number}. {html.escape(note.title)}</b> ({note.difficulty})"
            + (f' · <a href="{url}">LeetCode</a>' if url else "")]
    pattern = folder_of(note).replace("_", " ") + (f" ({', '.join(note.tags)})" if note.tags else "")
    for label, value in (("Pattern", pattern), ("Signal", signal(text)),
                         ("Approach", approach(text)), ("Complexity", complexity(text))):
        if value:
            back.append(f"<b>{label}:</b> {to_html(value)}")
    tags = " ".join([f"leetcode-dump pattern::{folder_of(note)} difficulty::{note.difficulty}",
                     f"status::{'solved' if note.status == '✅' else 'review'}"] + [f"tag::{t}" for t in note.tags])
    return [f"leetcode-dump-{note.number}", front, "<br>".join(back), tags]


def export(notes, out):
    rows = ["\t".join(card(n)) for n in sorted(notes, key=lambda n: n.number)]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(HEADER + rows) + "\n", encoding="utf-8", newline="\n")
    return len(rows)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--status", choices=("all", "review", "solved"), default="all")
    p.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = p.parse_args(argv)
    notes = checked_notes()
    if args.status != "all":
        notes = [n for n in notes if (n.status == "🔄") == (args.status == "review")]
    count = export(notes, args.out)
    print(f"wrote {count} cards to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
