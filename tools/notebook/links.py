"""Keep links between notes correct.

* A relative link to a note (`../DP/139.Word_Break.md`) is rewritten to the note's current path, so moving a
  note between folders never breaks a link.
* A related-problem bullet `* 132. Palindrome Partitioning II (minimum cuts) (in this repo)` becomes
  `* [132. Palindrome Partitioning II](../DP/132.Palindrome_Partitioning_II.md) (minimum cuts)`.
"""
import os
import re
from pathlib import Path
from urllib.parse import quote, unquote

from notebook.model import REPO, note_paths

NOTE_LINK_RE = re.compile(r"\]\((?!https?://|#)([^()\s]*?(?:\([^()\s]*\)[^()\s]*?)*\.md)(#[^)\s]*)?\)")
MENTION_RE = re.compile(r"^(\s*[*-] )(\d+)\. (.+?) \(in this repo\)(.*)$", re.M)
GENERATED = {"INDEX.md", "SHEETS.md", "TAGS.md", "COMPANIES.md"}


def note_index(repo=REPO):
    """{number: (path, title from the file name)} for every note file."""
    out = {}
    for path in note_paths(repo):
        number, rest = path.name.split(".", 1)
        out[int(number)] = (path, rest[:-3].replace("_", " "))
    return out


def rel_link(target, from_dir):
    return quote(Path(os.path.relpath(target, from_dir)).as_posix(), safe="/._-")


def number_of(link_target):
    match = re.match(r"(\d+)\.", unquote(link_target).rsplit("/", 1)[-1])
    return int(match.group(1)) if match else None


def fix_note_links(text, from_dir, index):
    def repl(m):
        number = number_of(m.group(1))
        if number is None or number not in index:
            return m.group(0)
        return f"]({rel_link(index[number][0], from_dir)}{m.group(2) or ''})"

    return NOTE_LINK_RE.sub(repl, text)


def link_mentions(text, from_dir, index, titles):
    """Turn '(in this repo)' bullets into links; `titles` maps number -> the note's real title."""
    def repl(m):
        indent, number, rest, tail = m.group(1), int(m.group(2)), m.group(3), m.group(4)
        if number not in index:
            return m.group(0)
        title = titles.get(number) or index[number][1]
        remark = rest[len(title):].strip() if rest.startswith(title) else ""
        label = title if rest.startswith(title) else rest
        link = f"[{number}. {label}]({rel_link(index[number][0], from_dir)})"
        return f"{indent}{link}{' ' + remark if remark else ''}{tail}"

    return MENTION_RE.sub(repl, text)


def markdown_files(repo=REPO):
    """Every hand-written Markdown file whose links we maintain."""
    skip = {"tools", ".github", ".githooks", "practice", "exports", "site", "site_src", "docs_src"}
    return sorted(p for p in repo.rglob("*.md")
                  if ".git" not in p.parts and p.relative_to(repo).parts[0] not in skip
                  and not (p.parent == repo and p.name in GENERATED))


def updated_files(titles=None, repo=REPO):
    """{path: new text} for every Markdown file whose note links are stale."""
    index = note_index(repo)
    titles = titles or {}
    out = {}
    for path in markdown_files(repo):
        text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        new = fix_note_links(link_mentions(text, path.parent, index, titles), path.parent, index)
        if new != text:
            out[path] = new
    return out

