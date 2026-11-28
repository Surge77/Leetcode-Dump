"""Apply the interview-ready prose (agent JSON) to notes: the phase 2 of note format v2.

    python tools/backfill/apply_prose_v2.py tools/backfill/out/batch_*.json [--dry-run]

For each note in the JSON it rebuilds the prose in the v2 order of LeetcodeTemplates/ActiveTemplate.md and keeps,
byte for byte: the front matter's difficulty, the title/link/status lines, the Problem Statement, every section
containing code (in its original order), any non-standard section, and the personal sections (Say It Out Loud,
My Attempts). It replaces the v1 prose sections (Quick Breakdown … Complexity Analysis). Tags from the JSON are
used when they are valid for the note's folder. Run build_index.py and verify.py afterwards.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from notebook.links import note_index, rel_link  # noqa: E402
from notebook.model import REPO, check_tags, front_matter, render_front_matter  # noqa: E402

V1_PROSE = ("Quick Breakdown", "Optimization Path", "Solution Breakdown", "Pattern Recognition",
            "Tricks & Patterns Used", "Alternative Data Structures", "Complexity Analysis")
V2_PROSE = ("Recognition Signal", "Clarifying Questions", "Approach Ladder", "Why It Works", "Dry Run", "Test Cases",
            "Bugs to Watch", "Follow-ups & Variations", "Related")
REPLACED = V1_PROSE + V2_PROSE  # rebuilt from the JSON on every run, so re-applying is idempotent
PERSONAL = ("Say It Out Loud", "My Attempts")
CODE_LANGS = {"python", "java", "cpp", "c", "javascript", "typescript", "sql"}
FIELDS = ("tags", "signal", "clarify", "ladder", "why", "dry_run", "tests", "bugs", "followups", "related")


def split_sections(body):
    """(preamble, [(heading, full section text)]) where heading is cleaned of ** and 🔹."""
    parts = re.split(r"(?m)^(?=## )", body)
    pre, out = parts[0], []
    for part in parts[1:]:
        heading = re.sub(r"[*🔹]", "", part.split("\n", 1)[0][3:]).strip()
        out.append((heading, part.rstrip("\n") + "\n"))
    return pre, out


def bullets(items):
    return "\n".join(f"* {item}" for item in items)


def section(title, content):
    return f"## 🔹 {title}\n\n{content.strip()}\n"


def ladder_table(steps):
    rows = ["| Step | Idea | Time | Space |", "|---|---|---|---|"]
    rows += [f"| {s['step']} | {s['idea'].replace('|', '/')} | {s['time']} | {s['space']} |" for s in steps]
    return "\n".join(rows)


def related(items, note_dir, index):
    lines = []
    for item in items:
        number, title, why = int(item["number"]), item["title"].strip(), item.get("why", "").strip()
        if number in index:
            text = f"[{number}. {title}]({rel_link(index[number][0], note_dir)})"
        else:
            text = f"{number}. {title}"
        lines.append(f"* {text}{': ' + why if why else ''}")
    return "\n".join(lines)


def validate(entry, number):
    missing = [f for f in FIELDS if f not in entry]
    if missing:
        raise ValueError(f"#{number}: missing fields {missing}")
    steps = [s["step"] for s in entry["ladder"]]
    if not steps or steps[0] != "Brute force" or steps[-1] != "Optimal":
        raise ValueError(f"#{number}: ladder must run Brute force … Optimal, got {steps}")


def rebuild(text, entry, path, index):
    number = int(path.name.split(".", 1)[0])
    validate(entry, number)
    fields, body = front_matter(text.replace("\r\n", "\n"))
    folder = path.relative_to(REPO).parts[0]
    tags = entry["tags"] if not check_tags(entry["tags"], folder) else fields["tags"]
    pre, sections = split_sections(body)
    by_name = dict(sections)
    statement = next((s for h, s in sections if h.startswith("Problem Statement")), None)
    if statement is None and entry.get("statement"):
        statement = section("Problem Statement", entry["statement"])
    kept = [(h, s) for h, s in sections if not h.startswith(REPLACED + PERSONAL + ("Problem Statement",))]
    code = [s for _, s in kept if "```" in s]
    extras = [s for _, s in kept if "```" not in s]
    say = by_name.get("Say It Out Loud") or section("Say It Out Loud", "*Yours to write.*")
    attempts = by_name.get("My Attempts") or section("My Attempts", "*Yours to write.*")
    out = [render_front_matter(fields["difficulty"], tags), pre.strip("\n") + "\n"]
    out += [statement] if statement else []
    out += [section("Recognition Signal", entry["signal"]),
            section("Clarifying Questions", bullets(entry["clarify"])),
            section("Approach Ladder", ladder_table(entry["ladder"])),
            section("Why It Works", entry["why"]),
            say,
            section("Dry Run", entry["dry_run"]),
            section("Test Cases", bullets(entry["tests"])),
            section("Bugs to Watch", bullets(entry["bugs"])),
            section("Follow-ups & Variations", bullets(entry["followups"])),
            section("Related", related(entry["related"], path.parent, index))]
    out += extras + code + [attempts]
    return "\n".join(part.rstrip("\n") + "\n" for part in out)


def fences(text):
    """Every code block (by language) in order: the applier must never change one."""
    return [b for b in _all_fences(text) if b[1].lower() in CODE_LANGS]


def _all_fences(text):
    return re.findall(r"^([ \t]*)```(\w*)[ \t]*\n(.*?)^\1```", text, re.S | re.M)


def main(argv):
    dry = "--dry-run" in argv
    entries = {}
    for name in (a for a in argv if not a.startswith("--")):
        entries.update(json.loads(Path(name).read_text(encoding="utf-8")))
    index = note_index()
    changed = 0
    for key, entry in sorted(entries.items(), key=lambda kv: int(kv[0])):
        path = index[int(key)][0]
        text = path.read_text(encoding="utf-8")
        new = rebuild(text, entry, path, index)
        if fences(new) != fences(text.replace("\r\n", "\n")):
            raise SystemExit(f"#{key}: code blocks would change; aborting before writing anything else")
        if not dry:
            path.write_text(new, encoding="utf-8", newline="\n")
        changed += 1
    print(f"{'would rebuild' if dry else 'rebuilt'} {changed} notes; now run build_index.py and verify.py")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
