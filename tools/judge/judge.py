"""Offline judge for the Infosys mock problems — scores YOUR stdin/stdout program per test case.

    python tools/judge/judge.py M1Q2 my_solution.py           # judge one solution
    python tools/judge/judge.py M1Q2 my_solution.py --seed 7  # reproduce a run
    python tools/judge/judge.py --list                        # every problem key
    python tools/judge/judge.py --self-test [M1Q2 ...]        # reference must score 100% (CI)

Tests: the statement's samples, random small inputs checked against the reference
solution, and max-constraint inputs with a time limit of max(MIN_TIME_LIMIT,
TIME_FACTOR x the reference's own time on this machine), so the limit adapts to
how fast your computer is.
"""
import argparse
import random
import re
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path[:0] = [str(HERE), str(REPO / "tools" / "verify")]

from harness import blocks_of, run_program  # noqa: E402
from specs import SPECS  # noqa: E402

MOCKS = REPO / "Infosys_SP_DSE"
KEY_RE = re.compile(r"^M(\d+)Q([1-3])$")
SAMPLE_IN_RE = re.compile(r"\*\*Sample Input[^*]*\*\*\s*```text\n(.*?)```", re.S)
SAMPLE_OUT_RE = re.compile(r"\*\*Sample Output[^*]*\*\*\s*```text\n(.*?)```", re.S)
MIN_TIME_LIMIT = 2.0  # seconds
TIME_FACTOR = 3.0
SMALL_TIME_LIMIT = 5.0  # generous: small inputs only catch infinite loops
REFERENCE_TIME_LIMIT = 120.0  # the reference itself must finish; anything longer is a broken spec
SHOW = 300  # characters of input/output shown for a failing test
SMALL_POINTS = 50  # of 100: samples + random small tests; large tests carry the rest
NL = "\n"


@dataclass
class Problem:
    key: str
    title: str
    statement: Path
    solution: Path


@dataclass
class Group:
    name: str
    passed: int = 0
    total: int = 0
    first_failure: Optional[str] = None
    notes: List[str] = field(default_factory=list)


def problem(key):
    match = KEY_RE.match(key.upper())
    if not match:
        raise SystemExit(f"bad key {key!r}: expected e.g. M1Q2")
    folder = MOCKS / f"Mock_Test_{match.group(1)}"
    found = sorted(folder.glob(f"Q{match.group(2)}_*.md"))
    if not found:
        raise SystemExit(f"no problem {key.upper()} under {folder.relative_to(REPO)}")
    statement = found[0]
    title = statement.read_text(encoding="utf-8").split("\n", 1)[0].split(": ", 1)[-1]
    return Problem(key.upper(), title, statement, folder / "solutions" / statement.name)


def all_keys():
    keys = []
    for folder in MOCKS.glob("Mock_Test_*"):
        for statement in folder.glob("Q[1-3]_*.md"):
            keys.append(f"M{folder.name.rsplit('_', 1)[1]}Q{statement.name[1]}")
    return sorted(keys, key=key_order)


def key_order(key):
    match = KEY_RE.match(key)
    return (int(match.group(1)), int(match.group(2))) if match else (0, 0)


def samples(prob):
    text = prob.statement.read_text(encoding="utf-8")
    ins, outs = SAMPLE_IN_RE.findall(text), SAMPLE_OUT_RE.findall(text)
    if not ins or len(ins) != len(outs):
        raise SystemExit(f"{prob.key}: could not read the sample input/output pairs")
    return list(zip(ins, outs))


def reference_code(prob):
    """The optimized solution: the last python block of the solution file."""
    return blocks_of(prob.solution)[-1]


def run(program, stdin_text, limit):
    """Run a Python file; return (verdict, stdout, seconds). Verdict: OK, RE or TLE."""
    start = time.perf_counter()
    try:
        proc = subprocess.run([sys.executable, str(program)], input=stdin_text, capture_output=True,
                              text=True, encoding="utf-8", timeout=limit)
    except subprocess.TimeoutExpired:
        return "TLE", "", time.perf_counter() - start
    elapsed = time.perf_counter() - start
    if proc.returncode != 0:
        tail = proc.stderr.strip().splitlines()[-1:] or [f"exit code {proc.returncode}"]
        return "RE", tail[0], elapsed
    return "OK", proc.stdout, elapsed


def same(got, want):
    return got.split() == want.split()


def clip(text):
    text = text.strip()
    return text if len(text) <= SHOW else text[:SHOW] + f" … ({len(text)} chars)"


def check(group, verdict, got, want, stdin_text):
    group.total += 1
    if verdict == "OK" and same(got, want):
        group.passed += 1
        return
    if group.first_failure is not None:
        return
    name = verdict if verdict != "OK" else "WA"
    if group.name == "large":  # a megabyte of input helps nobody: show its first line only
        error = f": {got}" if verdict == "RE" else ""  # e.g. RecursionError on a path-shaped tree
        group.first_failure = f"{name} on large test {group.total} (first line: {stdin_text.split(NL, 1)[0]}){error}"
        return
    detail = got if verdict == "RE" else "(killed at the time limit)" if verdict == "TLE" else clip(got)
    group.first_failure = f"{name} on input:\n{clip(stdin_text)}\n  expected: {clip(want)}\n  got:      {detail}"


def judge(key, program, tests=50, seed=None, min_time_limit=MIN_TIME_LIMIT, large=True):
    """Judge `program` (a .py path) on problem `key`; return (problem, [Group, ...])."""
    prob = problem(key)
    spec = SPECS.get(prob.key)
    if spec is None:
        raise SystemExit(f"{prob.key}: no input generator in tools/judge/specs*.py")
    rng = random.Random(seed)
    ref = reference_code(prob)
    groups = [Group("samples"), Group("random"), Group("large")]

    for stdin_text, want in samples(prob):
        verdict, got, _ = run(program, stdin_text, SMALL_TIME_LIMIT)
        check(groups[0], verdict, got, want, stdin_text)

    for _ in range(tests):
        stdin_text = spec.small(rng)
        verdict, got, _ = run(program, stdin_text, SMALL_TIME_LIMIT)
        check(groups[1], verdict, got, run_program(ref, stdin_text), stdin_text)

    if large:
        with tempfile.TemporaryDirectory() as tmp:
            ref_file = Path(tmp) / "reference.py"
            ref_file.write_text(ref, encoding="utf-8")
            for stdin_text in spec.large(rng):
                ref_verdict, want, ref_time = run(ref_file, stdin_text, REFERENCE_TIME_LIMIT)
                if ref_verdict != "OK":  # never grade against a crashed or hung reference
                    raise SystemExit(f"{prob.key}: reference solution {ref_verdict} on a large test: {want}")
                limit = max(min_time_limit, TIME_FACTOR * ref_time)
                verdict, got, took = run(program, stdin_text, limit)
                check(groups[2], verdict, got, want, stdin_text)
                groups[2].notes.append(f"{took:.2f}s (reference {ref_time:.2f}s, limit {limit:.2f}s)")
    return prob, groups


def report(prob, groups, seed):
    print(f"{prob.key} — {prob.title}  (seed {seed})")
    for g in groups:
        if g.total == 0:
            continue
        mark = "✓" if g.passed == g.total else "✗"
        extra = f"  [{'; '.join(g.notes)}]" if g.notes else ""
        print(f"  {g.name:<8} {g.passed:>3}/{g.total:<3} {mark}{extra}")
        if g.first_failure:
            print("    " + g.first_failure.replace("\n", "\n    "))
    points = score(groups)
    print(f"  score    {points}/100" + ("" if points == 100 else f"  — {verdict_hint(groups)}"))
    return points == 100


def score(groups):
    """Small tests (samples + random) are worth SMALL_POINTS, large tests the rest —
    so a correct brute force lands near half marks, as on the real exam."""
    small = [g for g in groups if g.name != "large"]
    large = [g for g in groups if g.name == "large" and g.total]
    small_total = sum(g.total for g in small)
    small_share = sum(g.passed for g in small) / small_total if small_total else 0
    if not large:  # --no-large: small tests are all there is
        return round(100 * small_share)
    large_share = large[0].passed / large[0].total
    return round(SMALL_POINTS * small_share + (100 - SMALL_POINTS) * large_share)


def verdict_hint(groups):
    small_ok = all(g.passed == g.total for g in groups if g.name != "large")
    if small_ok:
        return "correct but too slow or failing at max constraints: optimise"
    return "wrong answers on small inputs: fix correctness first"


def self_test(keys, tests):
    """Judge every reference solution against itself: all must score 100%."""
    failed = []
    with tempfile.TemporaryDirectory() as tmp:
        for key in keys or all_keys():
            ref_file = Path(tmp) / f"{key}.py"
            ref_file.write_text(reference_code(problem(key)), encoding="utf-8")
            prob, groups = judge(key, ref_file, tests=tests, seed=0, min_time_limit=60)
            if not report(prob, groups, 0):
                failed.append(key)
    print(f"\nself-test: {len(failed)} failing {failed}" if failed else "\nself-test: every reference scores 100%")
    return not failed


def utf8_stdout():
    """Print ✓ ✅ → etc. even when stdout is a pipe on Windows (default cp1252 cannot encode them)."""
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if callable(reconfigure):
        reconfigure(encoding="utf-8", errors="replace")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("key", nargs="?", help="problem key, e.g. M1Q2")
    parser.add_argument("program", nargs="?", help="your solution, a .py file reading stdin")
    parser.add_argument("--tests", type=int, default=50, help="random small tests (default 50)")
    parser.add_argument("--seed", type=int, help="random seed (printed on every run)")
    parser.add_argument("--no-large", action="store_true", help="skip the max-constraint tests")
    parser.add_argument("--list", action="store_true", help="list problem keys")
    parser.add_argument("--self-test", nargs="*", metavar="KEY", help="judge the reference solutions (CI)")
    args = parser.parse_args(argv)
    utf8_stdout()

    if args.list:
        for key in all_keys():
            prob = problem(key)
            print(f"{key:<6} {prob.title:<28} {prob.statement.relative_to(REPO).as_posix()}")
        return 0
    if args.self_test is not None:
        return 0 if self_test(args.self_test, min(args.tests, 20)) else 1
    if not (args.key and args.program):
        parser.error("give a problem key and your program, e.g. `judge.py M1Q2 my_q2.py`")
    program = Path(args.program)
    if not program.is_file():
        parser.error(f"{program} is not a file")
    seed = args.seed if args.seed is not None else random.randrange(10**6)
    prob, groups = judge(args.key, program, tests=args.tests, seed=seed, large=not args.no_large)
    return 0 if report(prob, groups, seed) else 1


if __name__ == "__main__":
    sys.exit(main())
