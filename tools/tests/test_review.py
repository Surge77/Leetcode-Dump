"""Behaviour of tools/review.py: scheduling, picking and status flips.  python -m unittest discover -s tools/tests"""
import random
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools"))

import review  # noqa: E402
from build_index import Note  # noqa: E402

TODAY = date(2026, 11, 26)


def note(number, status="🔄", folder="Arrays"):
    return Note(REPO / folder / f"{number}.X.md", number, f"P{number}", "Medium", status)


class ScheduleTest(unittest.TestCase):
    def test_first_pass_is_due_tomorrow(self):
        entry = review.schedule(None, True, TODAY)
        self.assertEqual((entry["streak"], entry["due"]), (1, "2026-11-27"))

    def test_consecutive_passes_space_out(self):
        entry = None
        dues = []
        for _ in range(4):
            entry = review.schedule(entry, True, TODAY)
            dues.append(entry["due"])
        self.assertEqual(dues, ["2026-11-27", "2026-11-29", "2026-12-03", "2026-12-12"])

    def test_fail_resets_streak_and_keeps_history(self):
        passed = review.schedule(None, True, TODAY)
        failed = review.schedule(passed, False, TODAY)
        self.assertEqual((failed["streak"], failed["due"]), (0, "2026-11-27"))
        self.assertEqual(failed["history"], ["2026-11-26:pass", "2026-11-26:fail"])
        self.assertEqual(passed["streak"], 1, "schedule must not mutate its input")

    def test_detects_a_review_already_logged_today(self):
        entry = review.schedule(None, True, TODAY)
        self.assertTrue(review.logged_on(entry, TODAY))
        self.assertFalse(review.logged_on(entry, date(2026, 11, 27)))
        self.assertFalse(review.logged_on(None, TODAY))

    def test_status_flips(self):
        self.assertIsNone(review.new_status_after(True, 1))
        self.assertEqual(review.new_status_after(True, review.MASTERED_STREAK), "✅ Solved")
        self.assertEqual(review.new_status_after(False, 0), "🔄 Need Review")


class PickTest(unittest.TestCase):
    def test_overdue_reviews_come_before_new_problems(self):
        notes = [note(1), note(2), note(3, status="✅")]
        state = {"3": {"streak": 1, "due": "2026-11-20", "history": []}}
        picks = review.pick(notes, state, TODAY, 2, random.Random(0))
        self.assertEqual(picks[0].number, 3)
        self.assertIn(picks[1].number, (1, 2))

    def test_reviews_not_yet_due_and_solved_new_notes_are_skipped(self):
        notes = [note(1), note(2, status="✅")]
        state = {"1": {"streak": 2, "due": "2026-12-30", "history": []}}
        self.assertEqual(review.pick(notes, state, TODAY, 3, random.Random(0)), [])

    def test_exam_topics_are_drawn_more_often(self):
        notes = [note(1, folder="DP_Knapsack"), note(2, folder="Arrays")]
        firsts = [review.pick(notes, {}, TODAY, 1, random.Random(s))[0].number for s in range(400)]
        self.assertGreater(firsts.count(1), 2 * firsts.count(2))


class SetStatusTest(unittest.TestCase):
    def test_rewrites_only_the_status_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "1.Two_Sum.md"
            path.write_text("# h\n\n**🔗 Link:** x\n**🟢 Status:** 🔄 Need Review\n\nbody\n", encoding="utf-8")
            self.assertTrue(review.set_status(path, "✅ Solved"))
            self.assertEqual(path.read_text(encoding="utf-8"),
                             "# h\n\n**🔗 Link:** x\n**🟢 Status:** ✅ Solved\n\nbody\n")
            self.assertFalse(review.set_status(path, "✅ Solved"), "no-op when already set")


if __name__ == "__main__":
    unittest.main()
