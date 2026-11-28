"""Stage the repo's Markdown into site_src/ for the Zensical site (it cannot build from the repo root).

    python tools/site/build_site.py      # writes site_src/ (gitignored)
    zensical build --clean               # writes site/ (gitignored); config: zensical.toml

What staging changes, so the same Markdown reads well on GitHub and on the site:
* README.md becomes index.md (the home page); folder READMEs stay README.md (section index pages).
* A note's difficulty is added to its tags, so the site's tag list can filter by difficulty too.
* Links to files the site does not contain (code, JSON, LICENSE, folders) point at GitHub instead.
"""
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import unquote

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "site_src"
GITHUB = "https://github.com/Surge77/Leetcode-Dump"
SKIP_TOP = {"tools", "LeetcodeTemplates", ".github", ".githooks", ".git", ".idea", ".claude", ".vscode", "practice", "exports", "site",
            "site_src"}
SKIP_NAMES = {"CLAUDE.md", "CLAUDE.local.md"}
LINK_RE = re.compile(r"(\]\()(?!https?://|#|mailto:)([^()\s]*?(?:\([^()\s]*\)[^()\s]*?)*)(#[^)\s]*)?(\))")
TAGS_RE = re.compile(r"\A(---\ndifficulty: (\w+)\ntags: \[)([^\]]*)(\]\n---\n)")


def sources(repo=REPO):
    return sorted(p for p in repo.rglob("*.md")
                  if p.relative_to(repo).parts[0] not in SKIP_TOP and p.name not in SKIP_NAMES
                  and "archive" not in p.relative_to(repo).parts)


def staged_name(rel):
    return Path("index.md") if rel == Path("README.md") else rel


def rewrite_links(text, rel, staged, repo=REPO):
    """Keep links between staged pages relative; send everything else to GitHub."""
    def repl(m):
        target = m.group(2)
        if not target:
            return m.group(0)
        resolved = (repo / rel.parent / unquote(target)).resolve()
        try:
            in_repo = resolved.relative_to(repo)
        except ValueError:
            return m.group(0)
        if in_repo in staged:
            # GitHub turns "## 🔹 Title" into "#-title"; the site's slug drops the emoji's dash.
            anchor = "#" + m.group(3)[2:] if (m.group(3) or "").startswith("#-") else m.group(3) or ""
            new = target
            if in_repo == Path("README.md"):
                new = Path(*[".."] * len(rel.parent.parts), "index.md").as_posix() if rel.parent.parts else "index.md"
            return f"{m.group(1)}{new}{anchor}{m.group(4)}"
        kind = "tree" if resolved.is_dir() else "blob"
        return f"{m.group(1)}{GITHUB}/{kind}/master/{in_repo.as_posix()}{m.group(3) or ''}{m.group(4)}"

    return LINK_RE.sub(repl, text)


def add_difficulty_tag(text):
    def repl(m):
        tags = [t.strip() for t in m.group(3).split(",") if t.strip()]
        return f"{m.group(1)}{', '.join(tags + [m.group(2).lower()])}{m.group(4)}"

    return TAGS_RE.sub(repl, text, count=1)


def stage(repo=REPO, out=OUT):
    if out.exists():
        shutil.rmtree(out)
    files = sources(repo)
    staged = {p.relative_to(repo) for p in files}
    for path in files:
        rel = path.relative_to(repo)
        text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        text = add_difficulty_tag(rewrite_links(text, rel, staged, repo))
        dest = out / staged_name(rel)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8", newline="\n")
    return len(files)


def main():
    count = stage()
    print(f"staged {count} pages into {OUT.relative_to(REPO)}/; now run `zensical build --clean`")
    return 0


if __name__ == "__main__":
    sys.exit(main())
