"""`review.py check N my.py`: judge YOUR solution with the note's own checks.

Your code replaces the note's optimized block (its last python block) and must pass everything the
reference passes: LeetCode's official examples, the random comparison against the brute force, and the
max-size run, whose time limit IS enforced here (a correct but slow answer is a fail, as on LeetCode).

* The checks run in a separate process with a deadline, so an infinite loop is reported as a time-limit
  failure instead of hanging the drill.
* Your file must define the same top-level classes as the reference (usually `Solution`). Some checks also
  exercise extra helper methods of the reference (e.g. a bitset variant); those are lent to your class, but
  the problem's public method never is.
"""
import contextlib
import importlib
import io
import json
import multiprocessing
import os
import sys
import traceback
from dataclasses import dataclass
from pathlib import Path
from queue import Empty

VERIFY_DIR = Path(__file__).resolve().parents[1] / "verify"
DEFAULT_DEADLINE = 60  # seconds for all of a note's checks together
INJECTED = {"TreeNode", "ListNode"}  # the harness provides these to every block


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


def public_method(number):
    """The method LeetCode calls for this problem (None for design problems)."""
    data = json.loads((VERIFY_DIR / "official_examples.json").read_text(encoding="utf-8"))
    entry = data.get(str(number), {})
    return entry.get("method") if entry.get("kind") == "function" else None


def classes_in(harness, code):
    ns = harness.ns_from(code)
    return {k: v for k, v in ns.items() if isinstance(v, type) and k not in INJECTED and v.__module__ == "lc"}


def prepare(harness, number, code):
    """(code to judge, error message or None): require the reference's classes, lend its helper methods."""
    reference = harness.blocks_of(harness.lc_path(number))[-1]
    ref_classes = classes_in(harness, reference)
    try:
        mine = classes_in(harness, code)
    except Exception as exc:  # the attempt does not even run at import time
        return code, f"your file failed to load: {type(exc).__name__}: {exc}"
    missing = sorted(set(ref_classes) - set(mine))
    if missing:
        return code, f"your file must define {', '.join('class ' + m for m in missing)} (as on LeetCode)"
    public = public_method(number)
    lend = {name: sorted(k for k in vars(cls) if not k.startswith("__") and k != public and not hasattr(mine[name], k))
            for name, cls in ref_classes.items()}
    lend = {name: methods for name, methods in lend.items() if methods}
    if not lend:
        return code, None
    shim = ("\n\n# --- added by the judge: reference-only helpers that the checks also call ---\n"
            f"_reference = {{'__name__': 'lc', 'TreeNode': TreeNode, 'ListNode': ListNode}}\n"
            f"exec({reference!r}, _reference)\n"
            f"for _cls, _methods in {lend!r}.items():\n"
            "    for _m in _methods:\n"
            "        setattr(globals()[_cls], _m, vars(_reference[_cls])[_m])\n")
    return code + shim, None


def check_here(number, code, timing=True, quiet=True):
    """Run note `number`'s checks with `code` as the solution under test, in this process."""
    harness = load_harness()
    keys = keys_for(harness, number)
    if not keys:
        raise SystemExit(f"note #{number} has no checks in tools/verify")
    code, problem = prepare(harness, number, code)
    if problem:
        return Verdict(False, False, len(keys), f"FAIL: {problem}")
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


def _worker(number, code, timing, queue):
    try:
        verdict = check_here(number, code, timing)
        queue.put((verdict.passed, verdict.tle, verdict.checks, verdict.report))
    except SystemExit as exc:
        queue.put(("exit", str(exc)))


def check(number, code, timing=True, deadline=DEFAULT_DEADLINE):
    """Run the checks in a child process; a run that exceeds `deadline` seconds is a time-limit failure."""
    ctx = multiprocessing.get_context("spawn")
    queue = ctx.Queue()
    proc = ctx.Process(target=_worker, args=(number, code, timing, queue), daemon=True)
    proc.start()
    proc.join(deadline)
    if proc.is_alive():
        proc.terminate()
        proc.join()
        return Verdict(False, True, 0, f"FAIL: TIME LIMIT: no verdict after {deadline} s (an infinite loop?)")
    try:
        result = queue.get(timeout=5)
    except Empty:
        return Verdict(False, False, 0, f"FAIL: the checker crashed (exit code {proc.exitcode})")
    if result[0] == "exit":
        raise SystemExit(result[1])
    return Verdict(*result)


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
