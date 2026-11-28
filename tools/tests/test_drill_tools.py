"""The drill's tools: stats, plan, quiz, attempt judge, debug drill, Anki export, README numbers, papers."""
import random
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools"))
sys.path.insert(0, str(REPO / "tools" / "judge"))

import build_index  # noqa: E402
import export_anki  # noqa: E402
import paper  # noqa: E402
from build_index import Note  # noqa: E402
from drill import attempt, mutate, plan, quiz, sections, stats  # noqa: E402
from drill import schedule as sched, state as st  # noqa: E402

TODAY = date(2026, 11, 26)
NOTE_139 = next(p for p in build_index.note_paths() if p.name.startswith("139."))
SAMPLE = """# 🔹 Problem Name: 1. X (Arrays, Easy)

## 🔹 Problem Statement

Find two numbers.

## 🔹 Quick Breakdown

* **Main Approach:** hash the complements
* **When to Use This Pattern?** "pair with a given sum"

## **🔹 Complexity Analysis**

* **Time Complexity:** O(n)
* **Space Complexity:** O(n)
"""


def note(number, status="🔄", folder="Arrays", difficulty="Medium"):
    return Note(REPO / folder / f"{number}.X.md", number, f"P{number}", difficulty, status)


class SectionsTest(unittest.TestCase):
    def test_reads_statement_signal_approach_and_complexity(self):
        self.assertEqual(sections.statement(SAMPLE), "Find two numbers.")
        self.assertEqual(sections.signal(SAMPLE), '"pair with a given sum"')
        self.assertEqual(sections.approach(SAMPLE), "hash the complements")
        self.assertEqual(sections.complexity(SAMPLE), "time O(n) · space O(n)")

    def test_every_note_has_a_statement_for_the_quiz(self):
        missing = [p.name for p in build_index.note_paths()
                   if not sections.statement(p.read_text(encoding="utf-8"))]
        self.assertEqual(missing, [])


class StatsTest(unittest.TestCase):
    def test_reports_weak_topics_reasons_and_time(self):
        notes = [note(1, folder="DP"), note(2, folder="DP"), note(3, folder="Arrays", difficulty="Easy")]
        state = st.empty()
        state["notes"] = {
            "1": sched.schedule(sched.schedule(None, "fail", TODAY, why="edge"), "ok", TODAY, mins=30),
            "2": sched.schedule(None, "fail", TODAY, why="edge"),
            "3": sched.schedule(None, "ok", TODAY, mins=10),
        }
        state["quiz"] = [{"date": "2026-11-25", "number": 1, "ok": True}, {"date": "2026-11-25", "number": 2, "ok": False}]
        state["cold"] = [{"date": "2026-11-20", "problem": "x", "result": "pass"}]
        text = stats.summary(notes, state, TODAY)
        self.assertIn("Weakest topics (fails / reviews): DP 2/3", text)
        self.assertIn("Why reviews went wrong: edge 2", text)
        self.assertIn("Time, Easy: median 10 min over 1 timed solves (target 15) — on target", text)
        self.assertIn("Time, Medium: median 30 min over 1 timed solves (target 25) — 5 min over", text)
        self.assertIn("Pattern quiz, last 30 days: 1/2", text)
        self.assertIn("Cold solves (unseen problems), last 30 days: 1/1", text)


class PlanTest(unittest.TestCase):
    def test_daily_starts_needed_and_pace_verdict(self):
        notes = [note(i) for i in range(1, 22)] + [note(99, status="✅")]
        entries = {"1": sched.schedule(None, "ok", date(2026, 11, 24))}
        p = plan.plan(notes, entries, TODAY, date(2026, 12, 6))
        self.assertEqual((p["not_started"], p["in_progress"], p["solved"]), (20, 1, 1))
        self.assertEqual(p["need_per_day"], 3, "20 starts over the 9 days before the 2-day lead")
        self.assertIn("behind", plan.render(p, date(2026, 12, 6)))

    def test_pace_counts_only_notes_in_scope(self):
        entries = {"500": sched.schedule(None, "ok", date(2026, 11, 25))}  # started, but outside the scope
        p = plan.plan([note(1), note(2)], entries, TODAY, date(2026, 12, 6))
        self.assertEqual(p["pace"], 0)

    def test_deadline_too_close_is_an_error(self):
        with self.assertRaises(SystemExit):
            plan.plan([note(1)], {}, TODAY, date(2026, 11, 27))


class QuizTest(unittest.TestCase):
    def test_hides_the_title_then_records_the_self_check(self):
        cards = [(note(1), "Find two numbers.", "pair sum")]
        shown, answers = [], iter(["hashing", "y"])
        results = quiz.run(cards, TODAY, ask=lambda _: next(answers), out=shown.append)
        self.assertNotIn("P1", shown[0], "the title must not appear with the statement")
        self.assertIn("P1", shown[1])
        self.assertEqual(results, [{"date": "2026-11-26", "number": 1, "ok": True}])

    def test_non_interactive_prints_answers_at_the_end(self):
        shown = []
        self.assertEqual(quiz.run([(note(1), "S", "")], TODAY, out=shown.append, interactive=False), [])
        self.assertTrue(any("— Answers —" in line for line in shown))

    def test_draw_is_reproducible_and_without_repeats(self):
        pool = [(note(i), "s", "") for i in range(10)]
        first = quiz.draw(pool, 5, random.Random(1))
        self.assertEqual(first, quiz.draw(pool, 5, random.Random(1)))
        self.assertEqual(len({c[0].number for c in first}), 5)


class AttemptTest(unittest.TestCase):
    def setUp(self):
        self.code = attempt.load_harness().blocks_of(NOTE_139)[-1]

    def test_the_reference_solution_is_accepted(self):
        verdict = attempt.check(139, self.code)
        self.assertTrue(verdict.passed, verdict.report)
        self.assertEqual(verdict.checks, 2)

    def test_a_wrong_solution_is_rejected_with_the_failing_example(self):
        wrong = self.code.replace("return dp[n]", "return not dp[n]")
        verdict = attempt.check(139, wrong)
        self.assertFalse(verdict.passed)
        self.assertIn("expected True, got False", verdict.report)

    def test_the_override_is_removed_afterwards(self):
        attempt.check_here(139, "class Solution:\n    def wordBreak(self, s, words):\n        return True\n")
        self.assertEqual(attempt.load_harness().OVERRIDES, {})

    def test_a_note_without_checks_is_an_error(self):
        with self.assertRaises(SystemExit):
            attempt.check(10**7, self.code)

    def test_an_infinite_loop_is_a_time_limit_not_a_hang(self):
        looping = "class Solution:\n    def wordBreak(self, s, words):\n        while True:\n            pass\n"
        verdict = attempt.check(139, looping, deadline=5)
        self.assertFalse(verdict.passed)
        self.assertTrue(verdict.tle)
        self.assertIn("TIME LIMIT", verdict.report)

    def test_a_missing_class_gets_a_clear_message(self):
        verdict = attempt.check_here(139, "def wordBreak(s, words):\n    return True\n")
        self.assertFalse(verdict.passed)
        self.assertIn("must define class Solution", verdict.report)

    def test_reference_only_helpers_are_lent_but_the_public_method_never_is(self):
        note_416 = next(p for p in build_index.note_paths() if p.name.startswith("416."))
        reference = attempt.load_harness().blocks_of(note_416)[-1]
        only_public = ("class Solution:\n    def canPartition(self, nums):\n        total = sum(nums)\n"
                       "        if total % 2:\n            return False\n        reach = {0}\n"
                       "        for x in nums:\n            reach |= {r + x for r in reach}\n"
                       "        return total // 2 in reach\n")
        self.assertIn("can_partition_bitset", reference)
        self.assertTrue(attempt.check_here(416, only_public).passed)
        no_public = "class Solution:\n    def can_partition_bitset(self, nums):\n        return False\n"
        self.assertFalse(attempt.check_here(416, no_public).passed)


class MutateTest(unittest.TestCase):
    CODE = "class Solution:\n    def f(self, n: int) -> int:\n        return min(n + 1, 3) if n < 2 else 0  # <\n"

    def test_candidates_skip_signatures_comments_and_arrows(self):
        found = {(old, new) for _, _, old, new in mutate.candidates(self.CODE)}
        self.assertEqual(found, {("min", "max"), ("+", "-"), ("1", "0"), ("<", "<="), ("0", "1")})

    def test_apply_changes_exactly_one_token(self):
        row, col, old, new = next(c for c in mutate.candidates(self.CODE) if c[2] == "<")
        mutant = mutate.apply(self.CODE, row, col, old, new)
        self.assertIn("n <= 2", mutant)
        self.assertIn("# <", mutant, "the comment is untouched")

    def test_plant_keeps_only_a_mutant_the_checks_catch(self):
        survivors = iter([True, True, False])  # the first two mutants pass the checks, the third is caught

        def judge(number, code, timing):
            return attempt.Verdict(next(survivors), False, 1, "")

        result = mutate.plant(1, self.CODE, random.Random(0), judge=judge)
        assert result is not None
        self.assertNotEqual(result[2], result[3])

    def test_a_real_drill_round_trip(self):
        code = attempt.load_harness().blocks_of(NOTE_139)[-1]
        result = mutate.plant(139, code, random.Random(5))
        assert result is not None
        self.assertFalse(attempt.check(139, result[0], timing=False).passed)
        with tempfile.TemporaryDirectory() as tmp:
            target = mutate.write_drill(Path(tmp), 139, "Word Break", result)
            row = int(mutate.reveal(Path(tmp), 139).split(":")[0].split()[1])
            self.assertEqual(target.read_text(encoding="utf-8").splitlines()[row - 1].strip(), result[3].strip())


class AnkiTest(unittest.TestCase):
    def test_cards_have_four_tab_free_columns_and_a_stable_id(self):
        n = build_index.parse(NOTE_139)[0]
        assert n is not None
        row = export_anki.card(n)
        self.assertEqual(len(row), 4)
        self.assertEqual(row[0], "leetcode-dump-139")
        self.assertTrue(all("\t" not in field and "\n" not in field for field in row))
        self.assertNotIn("Word Break", row[1], "the front hides the title")
        self.assertIn("Word Break", row[2])

    def test_markdown_to_html(self):
        self.assertEqual(export_anki.to_html("* **a** `x<y`\nnext"), "• <b>a</b> <code>x&lt;y</code><br>next")
        self.assertEqual(export_anki.to_html("\n\nbr\n"), "br", "leading/trailing breaks only")


class GeneratedReadmeTest(unittest.TestCase):
    def test_stats_block_reflects_the_notes(self):
        notes = build_index.checked_notes()
        block = build_index.render_stats(notes)
        self.assertIn(f"**{len(notes)}**", block)
        readme = f"intro\n{build_index.STATS_START}\nstale\n{build_index.STATS_END}\noutro"
        self.assertEqual(build_index.with_stats(readme, notes), f"intro\n{block}\noutro")


class PaperTest(unittest.TestCase):
    def test_held_out_mocks_only_appear_in_the_final_paper(self):
        keys = [f"M{t}Q{q}" for t in range(1, 11) for q in (1, 2, 3)]
        normal, final = paper.pool(keys, False), paper.pool(keys, True)
        self.assertFalse({k.split("Q")[0] for k in normal} & paper.HOLDOUT)
        self.assertEqual({k.split("Q")[0] for k in final}, paper.HOLDOUT)
        self.assertEqual(len(paper.pick(final, random.Random(0))), 3)


if __name__ == "__main__":
    unittest.main()
