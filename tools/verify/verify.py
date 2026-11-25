"""Check every solution in the repo.

    python tools/verify/verify.py            # all checks
    python tools/verify/verify.py 322 M1Q3   # selected checks

Set VERIFY_TIMING=1 to also enforce the max-constraint timing limits of the
mock tests (off by default: CI machines vary in speed).
"""
import importlib
import sys
import traceback
from pathlib import Path

sys.setrecursionlimit(10_000)
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import harness  # noqa: E402

for f in sorted(HERE.glob("tests_*.py")):
    importlib.import_module(f.stem)

keys = [int(k) if k.isdigit() else k for k in sys.argv[1:]] or list(harness.CASES)
failed = []
for key in keys:
    try:
        harness.CASES[key](harness)
        print(f"PASS {key}")
    except Exception:
        failed.append(key)
        print(f"FAIL {key}")
        traceback.print_exc(limit=3)
print(f"\n{len(keys) - len(failed)}/{len(keys)} passed; failed: {failed}")
sys.exit(1 if failed else 0)
