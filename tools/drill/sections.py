"""Read the parts of a note the drill shows: the statement, the recognition signal, the approach."""
import re

H2_RE = re.compile(r"^## (.+)$", re.M)
LINK_RE = re.compile(r"https://leetcode\.com/problems/[\w-]+/?")


def clean_heading(heading):
    return re.sub(r"[*🔹]", "", heading).strip()


def sections(text):
    """{heading: body} for every `## heading`, in order (headings cleaned of ** and 🔹)."""
    text = text.replace("\r\n", "\n")
    marks = list(H2_RE.finditer(text))
    out = {}
    for i, mark in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        out[clean_heading(mark.group(1))] = text[mark.end():end].strip("\n")
    return out


def section(text, *names):
    """Body of the first section whose heading starts with one of `names` (case-insensitive), or ''."""
    wanted = tuple(n.lower() for n in names)
    for heading, body in sections(text).items():
        if heading.lower().startswith(wanted):
            return body.strip()
    return ""


def bullet(text, label):
    """Value of a `* **label** value` bullet anywhere in the note, or ''."""
    label = re.escape(label.rstrip(":"))
    match = re.search(rf"^\s*[*-] \*\*{label}:?\*\*:?\s*(.+)$", text, re.M)
    return match.group(1).strip() if match else ""


def statement(text):
    # One hand-written note (199) uses an older step-by-step layout: its Step 1 restates the problem.
    return section(text, "Problem Statement") or section(text, "Step 1")


def signal(text):
    """The note's 'how do I recognise this?' line (format v2 section, or the v1 Quick Breakdown bullet)."""
    return section(text, "Recognition Signal") or bullet(text, "When to Use This Pattern?")


def approach(text):
    return (section(text, "Approach Ladder") or bullet(text, "Main Approach")
            or bullet(text, "Optimal Approach"))


def complexity(text):
    time_c, space_c = bullet(text, "Time Complexity"), bullet(text, "Space Complexity")
    return " · ".join(p for p in (f"time {time_c}" if time_c else "", f"space {space_c}" if space_c else "") if p)


def link(text):
    match = LINK_RE.search(text)
    return match.group(0) if match else ""
