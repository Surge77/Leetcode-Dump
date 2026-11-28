"""`review.py check N my.py`: judge YOUR solution with the note's own checks.

Your code replaces the note's optimized block (its last python block) and must pass everything the
reference passes: LeetCode's official examples, the random comparison against the brute force, and the
max-size run, whose time limit IS enforced here (a correct but slow answer is a fail, as on LeetCode).
"""
import contextlib
import importlib
import io
import os
import sys
import traceback
from dataclasses import dataclass
from pathlib import Path

VERIFY_DIR = Path(__file__).resolve().parents[1] / "verify"


@dataclass
class Verdict:
    passed: bool
    tle: bool
    checks: int
    report: str


def load_harness():
    """The verify harness with every tests_*.py registered (imported once per process)."""
    if str(VERIFY_DIR) not in sys.path:
        sys.path.insert(0, str(VERIFY_DIR))
    sys.setrecursionlimit(max(sys.getrecursionlimit(), 10_000))
    harness = importlib.import_module("harness")
    for f in sorted(VERIFY_DIR.glob("tests_*.py")):
        importlib.import_module(f.stem)
    return harness


def keys_for(harness, number):
    return [k for k in (number, f"{number}-official") if k in harness.CASES]


def is_timeout(exc):
    """True when the failing assert is the max-size time limit in timed()/timed_call()."""
    frames = traceback.extract_tb(exc.__traceback__)
    return isinstance(exc, AssertionError) and any(f.name in ("timed_call", "timed") for f in frames)


def check(number, code, timing=True, quiet=True):
    """Run note `number`'s checks with `code` as the solution under test."""
    harness = load_harness()
    keys = keys_for(harness, number)
    if not keys:
        raise SystemExit(f"note #{number} has no checks in tools/verify")
    old_env = os.environ.get("VERIFY_TIMING")
    if timing:
        os.environ["VERIFY_TIMING"] = "1"
    harness.OVERRIDES[number] = code
    lines, tle, failed = [], False, False
    try:
        for key in keys:
            out = io.StringIO()
            try:
                with contextlib.redirect_stdout(out) if quiet else contextlib.nullcontext():
                    harness.CASES[key](harness)
                lines.append(f"PASS {key}")
            except Exception as exc:  # any failure of the user's code is a verdict, not a crash
                failed = True
                tle = tle or is_timeout(exc)
                kind = "TIME LIMIT" if is_timeout(exc) else type(exc).__name__
                detail = str(exc).strip()[:400]
                lines.append(f"FAIL {key}: {kind}{': ' + detail if detail else ''}")
            timing_lines = [ln.strip() for ln in out.getvalue().splitlines() if "max-constraint" in ln]
            lines += [f"     {ln}" for ln in timing_lines]
    finally:
        harness.OVERRIDES.pop(number, None)
        if old_env is None:
            os.environ.pop("VERIFY_TIMING", None)
        else:
            os.environ["VERIFY_TIMING"] = old_env
    return Verdict(not failed, tle, len(keys), "\n".join(lines))


def read_solution(path):
    path = Path(path)
    if not path.is_file():
        raise SystemExit(f"{path}: no such file")
    code = path.read_text(encoding="utf-8")
    try:
        compile(code, str(path), "exec")
    except SyntaxError as err:
        raise SystemExit(f"{path}: syntax error on line {err.lineno}: {err.msg}")
    return code
