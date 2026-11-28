"""Parse a note and enforce the note format.

Every LeetCode note starts with front matter, then its title, link and status:

    ---
    difficulty: Medium
    tags: [dp-1d, trie]
    ---

    # 139. Word Break

    **🔗 Link:** [LeetCode 139](https://leetcode.com/problems/word-break/)
    **🟢 Status:** 🔄 Need Review

* `difficulty` is Easy, Medium or Hard; `tags` are 1-4 slugs from tools/taxonomy.json, and at least one must be
  in the note's folder's `tags_any` list.
* The status is exactly `✅ Solved` or `🔄 Need Review`.
* The note has the two personal sections, `## 🔹 Say It Out Loud` and `## 🔹 My Attempts`.
* Related problems that have a note here are links, not "(in this repo)" text.
"""
import json
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TAXONOMY_FILE = REPO / "tools" / "taxonomy.json"
SKIP_DIRS = {"LeetcodeTemplates", "Infosys_SP_DSE", "Interview_Prep", "tools", ".github", ".githooks",
             "practice", "exports", "site", "site_src", "docs_src"}
FRONT_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)
FIELD_RE = re.compile(r"^([a-z_]+): (.+)$")
HEADER_RE = re.compile(r"^# (\d+)\. (.+)$", re.M)
STATUS_RE = re.compile(r"^\*\*🟢 Status:\*\* (.*)$", re.M)
LINK_RE = re.compile(r"^\*\*🔗 Link:\*\* .*https://leetcode\.com/problems/([\w-]+)", re.M)
STATUSES = {"✅ Solved": "✅", "🔄 Need Review": "🔄"}
DIFFICULTIES = ("Easy", "Medium", "Hard")
PERSONAL_SECTIONS = ("Say It Out Loud", "My Attempts")
MAX_TAGS = 4


@dataclass(frozen=True)
class Note:
    path: Path
    number: int
    title: str
    difficulty: str
    status: str  # "✅" or "🔄"
    tags: tuple = ()
    slug: str = ""

    @property
    def folder(self):
        return self.path.relative_to(REPO).parts[0]


@lru_cache(maxsize=None)
def taxonomy():
    return json.loads(TAXONOMY_FILE.read_text(encoding="utf-8"))


def note_paths(repo=REPO):
    return sorted(p for p in repo.rglob("*.md")
                  if p.parent != repo and p.relative_to(repo).parts[0] not in SKIP_DIRS
                  and ".git" not in p.parts and re.match(r"\d+\.", p.name))


def front_matter(text):
    """({field: value}, rest of the text). `tags: [a, b]` becomes a list. Raises ValueError if malformed."""
    match = FRONT_RE.match(text)
    if not match:
        raise ValueError("must start with front matter (--- / difficulty: … / tags: […] / ---)")
    fields = {}
    for line in match.group(1).split("\n"):
        field = FIELD_RE.match(line)
        if not field:
            raise ValueError(f"bad front matter line {line!r}")
        key, value = field.groups()
        if value.startswith("[") and value.endswith("]"):
            fields[key] = [v.strip() for v in value[1:-1].split(",") if v.strip()]
        else:
            fields[key] = value.strip()
    return fields, text[match.end():]


def render_front_matter(difficulty, tags):
    return f"---\ndifficulty: {difficulty}\ntags: [{', '.join(tags)}]\n---\n"


def check_tags(tags, folder):
    """Format errors for a note's tags in `folder` (empty list when fine)."""
    tax = taxonomy()
    errors = []
    if not isinstance(tags, list) or not 1 <= len(tags) <= MAX_TAGS:
        return [f"needs 1-{MAX_TAGS} tags, got {tags!r}"]
    unknown = [t for t in tags if t not in tax["tags"]]
    if unknown:
        errors.append(f"unknown tags {unknown} (vocabulary: tools/taxonomy.json)")
    if len(set(tags)) != len(tags):
        errors.append(f"duplicate tags {tags}")
    spec = tax["folders"].get(folder)
    if spec is None:
        errors.append(f"folder {folder!r} is not in tools/taxonomy.json")
    elif not set(tags) & set(spec["tags_any"]):
        errors.append(f"tags {tags} need one of {spec['tags_any']} for folder {folder}")
    return errors


def parse(path):
    """Return (Note, []) for a well-formed note, or (None, [errors])."""
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    rel = path.relative_to(REPO).as_posix()
    try:
        fields, body = front_matter(text)
    except ValueError as err:
        return None, [f"{rel}: {err}"]
    errors = []
    difficulty, tags = fields.get("difficulty"), fields.get("tags")
    if difficulty not in DIFFICULTIES:
        errors.append(f"difficulty must be one of {DIFFICULTIES}, got {difficulty!r}")
    errors += check_tags(tags, path.relative_to(REPO).parts[0])
    extra = set(fields) - {"difficulty", "tags"}
    if extra:
        errors.append(f"unknown front matter fields {sorted(extra)}")
    first = body.lstrip("\n").split("\n", 1)[0]
    header = HEADER_RE.match(first)
    file_number = int(path.name.split(".", 1)[0])
    if not header:
        errors.append(f"first line after the front matter must be '# N. Title', got {first!r}")
    elif int(header.group(1)) != file_number:
        errors.append(f"header number {header.group(1)} != file number {file_number}")
    statuses = STATUS_RE.findall(body)
    if len(statuses) != 1 or statuses[0].strip() not in STATUSES:
        errors.append(f"need exactly one status line, one of {list(STATUSES)}; found {statuses}")
    link = LINK_RE.search(body)
    if not link:
        errors.append("missing '**🔗 Link:**' line with a leetcode.com/problems/ URL")
    for name in PERSONAL_SECTIONS:
        if not re.search(rf"^## 🔹 {name}$", body, re.M):
            errors.append(f"missing the personal section '## 🔹 {name}'")
    if "(in this repo)" in body:
        errors.append("'(in this repo)' mention: run `python tools/build_index.py` to turn it into a link")
    if errors or header is None or link is None:
        return None, [f"{rel}: {e}" for e in errors]
    assert isinstance(tags, list) and isinstance(difficulty, str)
    note = Note(path, file_number, header.group(2).strip(), difficulty, STATUSES[statuses[0].strip()],
                tuple(tags), link.group(1))
    return note, []


def load_notes():
    notes, errors = [], []
    for path in note_paths():
        note, problems = parse(path)
        errors += problems
        if note:
            notes.append(note)
    return notes, errors
