"""Behaviour of tools/judge/judge.py: verdicts and scoring.  python -m unittest discover -s tools/tests"""
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(REPO / "tools" / "judge"), str(REPO / "tools" / "verify")]

import judge  # noqa: E402

# M1Q1 (Festival Pairs): count pairs whose sum is divisible by K.
CORRECT_QUADRATIC = """
import sys
d = sys.stdin.read().split()
n, k = int(d[0]), int(d[1])
a = list(map(int, d[2:2 + n]))
print(sum(1 for i in range(n) for j in range(i + 1, n) if (a[i] + a[j]) % k == 0))
"""
ALWAYS_ZERO = "print(0)\n"
CRASHES = "raise ValueError('boom')\n"
CRASHES_ON_BIG_INPUT = """
import sys
d = sys.stdin.read().split()
if len(d) > 1000:
    raise RecursionError("maximum recursion depth exceeded")
print(0)
"""
SLOW_ON_BIG_INPUT = """
import sys, time
d = sys.stdin.read().split()
if len(d) > 1000:
    time.sleep(30)
print(0)
"""


class JudgeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def program(self, code):
        path = Path(self.tmp.name) / "solution.py"
        path.write_text(code, encoding="utf-8")
        return path

    def groups(self, code, **kwargs):
        _, groups = judge.judge("M1Q1", self.program(code), seed=1, **kwargs)
        return {g.name: g for g in groups}

    def failure(self, group):
        self.assertIsNotNone(group.first_failure, f"{group.name}: expected a failure")
        return group.first_failure or ""

    def test_reference_scores_full_marks(self):
        ref = judge.reference_code(judge.problem("M1Q1"))
        groups = self.groups(ref, tests=5)
        self.assertEqual(judge.score(list(groups.values())), 100)

    def test_wrong_answer_is_reported_with_the_failing_input(self):
        groups = self.groups(ALWAYS_ZERO, tests=20, large=False)
        self.assertLess(groups["random"].passed, 20)
        self.assertTrue(self.failure(groups["samples"]).startswith("WA on input"))

    def test_crash_is_a_runtime_error(self):
        groups = self.groups(CRASHES, tests=2, large=False)
        self.assertEqual(groups["random"].passed, 0)
        self.assertIn("RE", self.failure(groups["random"]))
        self.assertIn("ValueError", self.failure(groups["random"]))

    def test_slow_program_gets_time_limit_exceeded_on_large_tests(self):
        groups = self.groups(SLOW_ON_BIG_INPUT, tests=0, min_time_limit=0.5)
        self.assertEqual(groups["large"].passed, 0)
        self.assertTrue(self.failure(groups["large"]).startswith("TLE on large test"))

    def test_crash_on_a_large_test_shows_the_error(self):
        groups = self.groups(CRASHES_ON_BIG_INPUT, tests=0)
        self.assertIn("RecursionError", self.failure(groups["large"]))

    def test_correct_brute_force_earns_half_marks(self):
        groups = self.groups(CORRECT_QUADRATIC, tests=10, min_time_limit=0.5)
        self.assertEqual(judge.score(list(groups.values())), judge.SMALL_POINTS)


class ScoreTest(unittest.TestCase):
    def test_score_weights_small_and_large_tests(self):
        groups = [judge.Group("samples", 1, 1), judge.Group("random", 25, 50), judge.Group("large", 1, 2)]
        # small: 26/51 of 50 points, large: 1/2 of 50 points
        self.assertEqual(judge.score(groups), round(50 * 26 / 51 + 25))

    def test_without_large_tests_small_tests_carry_all_points(self):
        groups = [judge.Group("samples", 1, 1), judge.Group("random", 9, 9), judge.Group("large")]
        self.assertEqual(judge.score(groups), 100)

    def test_every_mock_problem_has_a_generator(self):
        self.assertEqual(sorted(judge.all_keys()), sorted(judge.SPECS))


if __name__ == "__main__":
    unittest.main()
