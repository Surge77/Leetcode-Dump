"""Drill scheduling, picking, state file and status flips.  python -m unittest discover -s tools/tests"""
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
from drill import picks, schedule as sched, state as st  # noqa: E402

TODAY = date(2026, 11, 26)


def note(number, status="🔄", folder="Arrays", difficulty="Medium"):
    return Note(REPO / folder / f"{number}.X.md", number, f"P{number}", difficulty, status)


def reviews(grades, start=None, solved_before=False):
    entry = start
    for grade in grades:
        entry = sched.schedule(entry, grade, TODAY, solved_before=solved_before)
    return entry


class ScheduleTest(unittest.TestCase):
    def test_first_ok_is_due_tomorrow(self):
        entry = sched.schedule(None, "ok", TODAY)
        self.assertEqual((entry["streak"], entry["step"], entry["due"]), (1, 1, "2026-11-27"))

    def test_pass_is_an_alias_for_ok(self):
        self.assertEqual(sched.schedule(None, "pass", TODAY), sched.schedule(None, "ok", TODAY))

    def test_ok_reviews_walk_the_whole_interval_ladder(self):
        entry, waits = None, []
        for _ in range(len(sched.INTERVALS) + 2):
            entry = sched.schedule(entry, "ok", TODAY)
            waits.append((date.fromisoformat(entry["due"]) - TODAY).days)
        self.assertEqual(waits, list(sched.INTERVALS) + [300, 300], "gaps grow, then stay at the top step")

    def test_easy_skips_a_step_and_hard_repeats_one(self):
        first = sched.schedule(None, "ok", TODAY)  # step 1
        easy = sched.schedule(first, "easy", TODAY)
        hard = sched.schedule(first, "hard", TODAY)
        self.assertEqual((easy["step"], easy["due"]), (3, "2026-12-03"), "easy waits step 2's 7 days")
        self.assertEqual((hard["step"], hard["due"]), (1, "2026-11-29"), "hard waits step 1's 3 days again")

    def test_fail_resets_and_records_minutes_and_reason(self):
        passed = sched.schedule(None, "ok", TODAY)
        failed = sched.schedule(passed, "fail", TODAY, mins=31, why="edge")
        self.assertEqual((failed["streak"], failed["step"], failed["due"]), (0, 0, "2026-11-27"))
        self.assertEqual(failed["history"][-1], {"date": "2026-11-26", "grade": "fail", "mins": 31, "why": "edge"})
        self.assertEqual(passed["streak"], 1, "schedule must not mutate its input")

    def test_a_note_solved_before_the_drill_starts_further_up(self):
        entry = sched.schedule(None, "ok", TODAY, solved_before=True)
        self.assertEqual((entry["step"], entry["streak"], entry["due"]), (3, 3, "2026-12-03"))
        self.assertIsNone(sched.new_status_after("ok", 1))
        self.assertEqual(sched.new_status_after("ok", entry["streak"]), "✅ Solved")

    def test_status_flips(self):
        self.assertEqual(sched.new_status_after("hard", sched.MASTERED_STREAK), "✅ Solved")
        self.assertEqual(sched.new_status_after("fail", 0), "🔄 Need Review")

    def test_unknown_grade_is_rejected(self):
        with self.assertRaises(ValueError):
            sched.schedule(None, "great", TODAY)

    def test_detects_a_review_already_logged_today(self):
        entry = sched.schedule(None, "ok", TODAY)
        self.assertTrue(sched.logged_on(entry, TODAY))
        self.assertFalse(sched.logged_on(entry, date(2026, 11, 27)))
        self.assertFalse(sched.logged_on(None, TODAY))


class PickTest(unittest.TestCase):
    def test_overdue_reviews_come_before_new_problems(self):
        notes = [note(1), note(2), note(3, status="✅")]
        entries = {"3": {"step": 1, "streak": 1, "due": "2026-11-20", "history": [{"date": "2026-11-19", "grade": "ok"}]}}
        chosen = picks.pick(notes, entries, TODAY, 2, random.Random(0))
        self.assertEqual(chosen[0].number, 3)
        self.assertIn(chosen[1].number, (1, 2))

    def test_never_reviewed_solved_notes_are_drawn_for_a_recheck(self):
        notes = [note(1, status="✅")]
        self.assertEqual([n.number for n in picks.pick(notes, {}, TODAY, 3, random.Random(0))], [1])

    def test_reviews_not_yet_due_are_skipped(self):
        notes = [note(1)]
        entries = {"1": {"step": 2, "streak": 2, "due": "2026-12-30", "history": [{"date": "2026-11-20", "grade": "ok"}]}}
        self.assertEqual(picks.pick(notes, entries, TODAY, 3, random.Random(0)), [])

    def test_logging_a_pick_does_not_reshuffle_the_rest_of_the_day(self):
        notes = [note(i, folder="DP" if i % 2 else "Arrays") for i in range(1, 30)]
        notes.append(note(99, status="✅"))
        entries = {"99": {"step": 1, "streak": 1, "due": "2026-11-25", "history": [{"date": "2026-11-24", "grade": "ok"}]}}
        before = [n.number for n in picks.pick(notes, entries, TODAY, 4, random.Random(7))]
        for number in before:  # log every pick, one at a time
            entries = {**entries, str(number): sched.schedule(entries.get(str(number)), "ok", TODAY)}
            after = [n.number for n in picks.pick(notes, entries, TODAY, 4, random.Random(7))]
            self.assertEqual(after, before)

    def test_exam_topics_are_drawn_more_often(self):
        notes = [note(1, folder="DP_Knapsack"), note(2, folder="Arrays")]
        firsts = [picks.pick(notes, {}, TODAY, 1, random.Random(s))[0].number for s in range(400)]
        self.assertGreater(firsts.count(1), 2 * firsts.count(2))

    def test_scope_by_sheet_and_topic(self):
        with tempfile.TemporaryDirectory() as tmp:
            sheets = Path(tmp) / "sheets.json"
            sheets.write_text('{"NeetCode 150": {"source": "x", "topics": [{"topic": "t", "problems": [1, 3]}]},'
                              ' "Grind 169": {"source": "y", "topics": []}}', encoding="utf-8")
            notes = [note(1), note(2), note(3, folder="DP_Knapsack")]
            self.assertEqual([n.number for n in picks.scope(notes, sheet="neet", sheets_file=sheets)], [1, 3])
            self.assertEqual([n.number for n in picks.scope(notes, topic="dp", sheets_file=sheets)], [3])
            with self.assertRaises(SystemExit):
                picks.scope(notes, sheet="nothing", sheets_file=sheets)


class StateFileTest(unittest.TestCase):
    def test_round_trip_one_record_per_line_and_corrupt_file_message(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            self.assertEqual(st.load_state(path), st.empty())
            state = st.empty()
            state["notes"] = {"10": reviews(["ok"]), "2": reviews(["fail"])}
            state["cold"] = [{"date": "2026-11-26", "problem": "two-sum", "result": "pass"}]
            st.save_state(state, path)
            loaded = st.load_state(path)
            self.assertEqual(loaded, state)
            self.assertEqual(list(loaded["notes"]), ["2", "10"], "saved in numeric order")
            text = path.read_text(encoding="utf-8")
            self.assertIn('  "2": {', text, "one note per line")
            path.write_text("", encoding="utf-8")
            with self.assertRaises(SystemExit) as raised:
                st.load_state(path)
            self.assertIn("not valid JSON", str(raised.exception))

    def test_a_v1_file_is_migrated_not_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            path.write_text('{"322": {"streak": 2, "due": "2026-12-03", "history": ["2026-11-25:pass", '
                            '"2026-11-26:pass"]}, "7": {"streak": 0, "due": "2026-11-27", "history": '
                            '["2026-11-26:fail"]}}', encoding="utf-8")
            state = st.load_state(path)
            self.assertEqual(state["version"], st.VERSION)
            self.assertEqual(state["notes"]["322"], {"step": 2, "streak": 2, "due": "2026-12-03", "history": [
                {"date": "2026-11-25", "grade": "ok"}, {"date": "2026-11-26", "grade": "ok"}]})
            self.assertEqual(state["notes"]["7"]["history"], [{"date": "2026-11-26", "grade": "fail"}])
            path.write_text('{"version": 99, "notes": {}}', encoding="utf-8")
            with self.assertRaises(SystemExit):
                st.load_state(path)

    def test_an_empty_state_still_serialises_to_valid_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            st.save_state(st.empty(), path)
            self.assertEqual(st.load_state(path), st.empty())


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
