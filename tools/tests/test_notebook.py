"""Note format v2: front matter + tags, link maintenance, generated pages, attempts log, scaffolder, companies."""
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools"))

import new_note  # noqa: E402
import refresh_companies  # noqa: E402
import review  # noqa: E402
from build_index import checked_notes  # noqa: E402
from drill import picks  # noqa: E402
from notebook import links, model, pages, render  # noqa: E402

NOTES = checked_notes()
BY_NUMBER = {n.number: n for n in NOTES}


class FrontMatterTest(unittest.TestCase):
    def test_parses_fields_and_lists(self):
        fields, rest = model.front_matter("---\ndifficulty: Hard\ntags: [dp-1d, trie]\n---\n# 1. X\n")
        self.assertEqual(fields, {"difficulty": "Hard", "tags": ["dp-1d", "trie"]})
        self.assertEqual(rest, "# 1. X\n")

    def test_missing_or_malformed_front_matter_is_an_error(self):
        with self.assertRaises(ValueError):
            model.front_matter("# 1. X\n")
        with self.assertRaises(ValueError):
            model.front_matter("---\nnot a field\n---\n")

    def test_tag_rules(self):
        self.assertEqual(model.check_tags(["dp-1d"], "DP"), [])
        self.assertIn("unknown tags", model.check_tags(["dp-1d", "made-up"], "DP")[0])
        self.assertIn("need one of", model.check_tags(["trie"], "DP")[0])
        self.assertIn("needs 1-4 tags", model.check_tags([], "DP")[0])
        self.assertIn("not in tools/taxonomy.json", " ".join(model.check_tags(["dp-1d"], "Nowhere")))

    def test_every_note_parses_with_a_slug_and_tags(self):
        self.assertGreater(len(NOTES), 400)
        self.assertTrue(all(n.slug and n.tags for n in NOTES))
        self.assertEqual(BY_NUMBER[139].slug, "word-break")


class LinksTest(unittest.TestCase):
    def setUp(self):
        self.index = links.note_index()
        self.dp_dir = REPO / "DP"

    def test_stale_paths_are_repointed(self):
        text = "see [139](../Somewhere_Old/139.Word_Break.md#why) and [ext](https://x.y/1.md)"
        fixed = links.fix_note_links(text, self.dp_dir, self.index)
        self.assertEqual(fixed, "see [139](139.Word_Break.md#why) and [ext](https://x.y/1.md)")

    def test_in_repo_mentions_become_links_and_keep_the_remark(self):
        text = "* 139. Word Break (prefix DP) (in this repo)\n* 99999. Unknown (in this repo)\n"
        out = links.link_mentions(text, REPO / "Trie", self.index, {139: "Word Break"})
        self.assertIn("* [139. Word Break](../DP/139.Word_Break.md) (prefix DP)", out)
        self.assertIn("99999. Unknown (in this repo)", out, "unknown numbers are left alone")

    def test_paths_with_parentheses_are_encoded(self):
        number = next(n for n, (p, _) in self.index.items() if "(" in p.name)
        link = links.rel_link(self.index[number][0], REPO)
        self.assertNotIn("(", link)
        self.assertEqual(links.number_of(link), number)

    def test_the_repo_has_no_stale_links(self):
        self.assertEqual(list(links.updated_files()), [])


class PagesTest(unittest.TestCase):
    def test_ladder_orders_by_difficulty_and_lists_cross_folder_tags(self):
        block = pages.ladder("Stack", NOTES)
        rows = [ln for ln in block.splitlines() if ln.startswith("| ") and ln[2].isdigit()]
        difficulties = [r.split(" | ")[2] for r in rows if "Same pattern" not in r]
        self.assertEqual(difficulties[0], "Easy")
        self.assertIn("Same pattern, filed elsewhere", block)

    def test_page_keeps_hand_written_prose(self):
        current = "# Stack\n\nMy own notes.\n\n<!-- generated:ladder -->\nold\n<!-- /generated:ladder -->\n\nAfter.\n"
        text = pages.page_text("Stack", NOTES, current)
        self.assertTrue(text.startswith("# Stack\n\nMy own notes.\n\n"))
        self.assertTrue(text.endswith("\n\nAfter.\n"))
        self.assertNotIn("\nold\n", text)

    def test_tags_page_lists_every_used_tag(self):
        text = render.render_tags(NOTES)
        for tag in {t for n in NOTES for t in n.tags}:
            self.assertIn(f"\n## {tag}\n", text)

    def test_company_lookup(self):
        data = {"companies": {"Google": {"all": ["two-sum"], "recent": ["lru-cache"]},
                              "Goldman Sachs": {"all": [], "recent": []}}}
        self.assertEqual(pages.company_slugs("google", data), {"two-sum", "lru-cache"})
        with self.assertRaises(SystemExit):
            pages.company_slugs("g", data)


class ScopeTest(unittest.TestCase):
    def test_topic_matches_tags_and_company_matches_slugs(self):
        mono = picks.scope(NOTES, topic="monotonic-stack")
        self.assertTrue(mono and all("monotonic-stack" in n.tags or "monotonic" in n.folder.lower() for n in mono))
        asked = picks.scope(NOTES, company="x", company_slugs={"word-break", "two-sum"})
        self.assertEqual(sorted(n.number for n in asked), [1, 139])


class AttemptsLogTest(unittest.TestCase):
    def test_lines_replace_the_placeholder_and_accumulate(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "1.X.md"
            path.write_text("## 🔹 Code\n\nx\n\n## 🔹 My Attempts\n\n*One line per attempt, e.g. …*\n", encoding="utf-8")
            today = date(2026, 12, 1)
            self.assertTrue(review.add_attempt(path, review.attempt_line(today, "fail", 31, "edge", "empty input")))
            review.add_attempt(path, review.attempt_line(today, "ok"))
            text = path.read_text(encoding="utf-8")
            self.assertTrue(text.endswith("## 🔹 My Attempts\n\n- 2026-12-01 · 31 min · fail · edge: empty input\n"
                                          "- 2026-12-01 · ok\n"), text)
            self.assertNotIn("One line per attempt", text)


class ScaffoldTest(unittest.TestCase):
    def test_creates_a_well_formed_note_and_a_failing_stub(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, verify = Path(tmp), Path(tmp) / "verify"
            verify.mkdir()
            note, tests = new_note.scaffold(99999, "Pow(x, n) Again", "Medium", "Math", ["math"], repo=repo,
                                            verify_dir=verify)
            self.assertEqual(note.name, "99999.Pow(x_n)_Again.md")
            fields, body = model.front_matter(note.read_text(encoding="utf-8"))
            self.assertEqual(fields, {"difficulty": "Medium", "tags": ["math"]})
            self.assertTrue(body.lstrip("\n").startswith("# 99999. Pow(x, n) Again\n"))
            self.assertIn("problems/pow-x-n-again/", body, "default slug from the title (--slug overrides it)")
            self.assertIn("raise NotImplementedError", tests.read_text(encoding="utf-8"))
            with self.assertRaises(SystemExit):
                new_note.scaffold(99999, "Again", "Medium", "Math", ["math"], repo=repo, verify_dir=verify)
            with self.assertRaises(SystemExit):
                new_note.scaffold(99998, "Bad", "Medium", "Math", ["trie"], repo=repo, verify_dir=verify)


class CompaniesRefreshTest(unittest.TestCase):
    def test_reads_lists_most_frequent_first(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "Google"
            folder.mkdir()
            header = "Difficulty,Title,Frequency,Acceptance Rate,Link,Topics\n"
            (folder / "5. All.csv").write_text(header + "EASY,Two Sum,50.0,0.5,https://leetcode.com/problems/two-sum,x\n"
                                               "HARD,Word Ladder,90.0,0.3,https://leetcode.com/problems/word-ladder,y\n",
                                               encoding="utf-8")
            (folder / "3. Six Months.csv").write_text(header, encoding="utf-8")
            self.assertEqual(refresh_companies.slugs(folder / "5. All.csv", 10),
                             [("word-ladder", "Word Ladder", "Hard"), ("two-sum", "Two Sum", "Easy")])
            self.assertEqual(refresh_companies.slugs(folder / "missing.csv", 10), [])


if __name__ == "__main__":
    unittest.main()
