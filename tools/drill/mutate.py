"""`review.py debug N`: plant one realistic bug in a verified solution for you to find.

One token of the optimized solution is changed (`<` ↔ `<=`, `+ 1` ↔ `- 1`, `min` ↔ `max`, `and` ↔ `or`,
`0` ↔ `1`, …) and the mutant is kept only if the note's checks catch it, so there is always a real bug.
Interviews increasingly include reading and debugging rounds; this trains exactly that.
"""
import io
import json
import random
import tokenize
from pathlib import Path

from drill.attempt import check

SWAPS = {"<": "<=", "<=": "<", ">": ">=", ">=": ">", "==": "!=", "!=": "==",
         "min": "max", "max": "min", "and": "or", "or": "and", "True": "False", "False": "True",
         "0": "1", "1": "0"}
SIGN_SWAPS = {"+": "-", "-": "+"}  # only directly before a number: the classic off-by-one
SKIP_LINE_STARTS = ("def ", "class ", "import ", "from ", "@")
MAX_TRIES = 40


def candidates(code):
    """[(row, col, old, new)] for every token worth mutating (1-based rows, like tokenize)."""
    tokens = list(tokenize.generate_tokens(io.StringIO(code).readline))
    lines = code.splitlines()
    found = []
    for i, tok in enumerate(tokens):
        row, col = tok.start
        if row > len(lines) or lines[row - 1].lstrip().startswith(SKIP_LINE_STARTS):
            continue
        if tok.type in (tokenize.OP, tokenize.NAME, tokenize.NUMBER) and tok.string in SWAPS:
            found.append((row, col, tok.string, SWAPS[tok.string]))
        elif tok.type == tokenize.OP and tok.string in SIGN_SWAPS and i + 1 < len(tokens) \
                and tokens[i + 1].type == tokenize.NUMBER and tokens[i - 1].type in (tokenize.NAME, tokenize.NUMBER,
                                                                                    tokenize.OP):
            found.append((row, col, tok.string, SIGN_SWAPS[tok.string]))
    return found


def apply(code, row, col, old, new):
    lines = code.splitlines(keepends=True)
    line = lines[row - 1]
    assert line[col:col + len(old)] == old, (line, col, old)
    lines[row - 1] = line[:col] + new + line[col + len(old):]
    return "".join(lines)


def plant(number, code, rng, judge=check, max_tries=MAX_TRIES):
    """Return (mutant code, row, original line, mutated line) for a mutant the checks catch, or None."""
    options = candidates(code)
    rng.shuffle(options)
    for row, col, old, new in options[:max_tries]:
        mutant = apply(code, row, col, old, new)
        try:
            compile(mutant, "<mutant>", "exec")
        except SyntaxError:
            continue
        if not judge(number, mutant, timing=False).passed:
            return mutant, row, code.splitlines()[row - 1], mutant.splitlines()[row - 1]
    return None


def write_drill(practice_dir, number, title, result):
    mutant, row, original, mutated = result
    practice_dir.mkdir(exist_ok=True)
    target = practice_dir / f"debug_{number}.py"
    header = (f"# Debug drill — LeetCode {number}. {title}\n"
              "# One token of this verified solution was changed and the checks now fail.\n"
              "# Find the bug by READING it first, as in an interview; then fix it and run\n"
              f"#     python tools/review.py check {number} {practice_dir.name}/{target.name}\n"
              f"# Stuck?  python tools/review.py debug {number} --reveal\n\n")
    target.write_text(header + mutant, encoding="utf-8", newline="\n")
    answer = {"row": row + header.count("\n"), "original": original.strip(), "mutated": mutated.strip()}
    (practice_dir / f".debug_{number}.json").write_text(json.dumps(answer), encoding="utf-8")
    return target


def reveal(practice_dir, number):
    path = Path(practice_dir) / f".debug_{number}.json"
    if not path.exists():
        raise SystemExit(f"no debug drill for #{number}: run `python tools/review.py debug {number}` first")
    answer = json.loads(path.read_text(encoding="utf-8"))
    return f"line {answer['row']}: `{answer['mutated']}` should be `{answer['original']}`"


def new_rng(seed=None):
    return random.Random(seed)
