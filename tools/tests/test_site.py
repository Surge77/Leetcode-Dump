"""Site staging (tools/site/build_site.py): link rewriting, home page, difficulty tags."""
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "site"))

import build_site  # noqa: E402

GH = build_site.GITHUB


class RewriteLinksTest(unittest.TestCase):
    def setUp(self):
        self.staged = {Path("README.md"), Path("DP/139.Word_Break.md"), Path("Interview_Prep/SQL.md")}

    def rewrite(self, text, rel):
        return build_site.rewrite_links(text, Path(rel), self.staged, REPO)

    def test_links_between_staged_pages_stay_relative(self):
        self.assertEqual(self.rewrite("[a](../DP/139.Word_Break.md)", "Trie/README.md"), "[a](../DP/139.Word_Break.md)")

    def test_github_emoji_anchors_lose_their_leading_dash(self):
        self.assertEqual(self.rewrite("[q](SQL.md#-quick-theory)", "Interview_Prep/README.md"), "[q](SQL.md#quick-theory)")

    def test_the_root_readme_becomes_the_home_page(self):
        self.assertEqual(self.rewrite("[home](../README.md#start)", "DP/README.md"), "[home](../index.md#start)")

    def test_files_outside_the_site_point_to_github(self):
        self.assertEqual(self.rewrite("[t](tools/review.py)", "README.md"), f"[t]({GH}/blob/master/tools/review.py)")
        self.assertEqual(self.rewrite("[d](tools)", "README.md"), f"[d]({GH}/tree/master/tools)")

    def test_external_and_anchor_links_are_untouched(self):
        for text in ("[x](https://leetcode.com/problems/a/)", "[y](#local)"):
            self.assertEqual(self.rewrite(text, "README.md"), text)


class StageTest(unittest.TestCase):
    def test_difficulty_becomes_a_tag(self):
        text = "---\ndifficulty: Hard\ntags: [dp-1d, trie]\n---\n\n# 1. X\n"
        self.assertTrue(build_site.add_difficulty_tag(text).startswith("---\ndifficulty: Hard\ntags: [dp-1d, trie, hard]\n"))

    def test_stage_skips_tooling_and_renames_the_readme(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, out = Path(tmp) / "repo", Path(tmp) / "out"
            for rel, text in {"README.md": "# Home\n[n](DP/1.X.md)\n", "DP/1.X.md": "# 1. X\n",
                              "tools/notes.md": "# tool\n", "CLAUDE.md": "# private\n"}.items():
                (repo / rel).parent.mkdir(parents=True, exist_ok=True)
                (repo / rel).write_text(text, encoding="utf-8")
            self.assertEqual(build_site.stage(repo, out), 2)
            self.assertEqual(sorted(p.relative_to(out).as_posix() for p in out.rglob("*.md")), ["DP/1.X.md", "index.md"])
            self.assertIn("[n](DP/1.X.md)", (out / "index.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
