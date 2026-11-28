"""tools/backfill/apply_prose_v2.py: v2 sections in template order, code and personal sections untouched."""
import json
import re
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools"))
sys.path.insert(0, str(REPO / "tools" / "backfill"))

import apply_prose_v2 as backfill  # noqa: E402
from notebook.links import note_index  # noqa: E402

SAMPLE = json.loads((REPO / "tools" / "backfill" / "sample_139.json").read_text(encoding="utf-8"))["139"]
INDEX = note_index()
PATH = INDEX[139][0]
ORDER = ["Problem Statement", "Recognition Signal", "Clarifying Questions", "Approach Ladder", "Why It Works",
         "Say It Out Loud", "Dry Run", "Test Cases", "Bugs to Watch", "Follow-ups & Variations", "Related",
         "Code Snippet (Brute Force)", "Code Snippet (Optimized)", "My Attempts"]


def headings(text):
    return [re.sub(r"[*🔹]", "", h).strip() for h in re.findall(r"^## (.+)$", text, re.M)]


class ApplyTest(unittest.TestCase):
    def setUp(self):
        self.text = PATH.read_text(encoding="utf-8").replace("\r\n", "\n")

    def test_template_order_with_code_and_personal_sections_kept(self):
        new = backfill.rebuild(self.text, SAMPLE, PATH, INDEX)
        self.assertEqual(headings(new), ORDER)
        self.assertEqual(backfill.fences(new), backfill.fences(self.text))
        attempts = self.text[self.text.index("## 🔹 My Attempts"):]
        self.assertTrue(new.endswith(attempts))
        self.assertIn("tags: [dp-1d, dp-strings, trie]", new)
        self.assertIn("[132. Palindrome Partitioning II](132.Palindrome_Partitioning_II.md)", new)

    def test_rebuilding_twice_is_stable(self):
        once = backfill.rebuild(self.text, SAMPLE, PATH, INDEX)
        self.assertEqual(backfill.rebuild(once, SAMPLE, PATH, INDEX), once)

    def test_invalid_tags_fall_back_to_the_current_ones(self):
        entry = {**SAMPLE, "tags": ["not-a-tag"]}
        new = backfill.rebuild(self.text, entry, PATH, INDEX)
        current = re.search(r"^tags: .*$", self.text, re.M)
        assert current is not None
        self.assertIn(current.group(0), new)

    def test_a_ladder_must_run_from_brute_force_to_optimal(self):
        with self.assertRaises(ValueError):
            backfill.rebuild(self.text, {**SAMPLE, "ladder": SAMPLE["ladder"][::-1]}, PATH, INDEX)
        with self.assertRaises(ValueError):
            backfill.rebuild(self.text, {k: v for k, v in SAMPLE.items() if k != "bugs"}, PATH, INDEX)


if __name__ == "__main__":
    unittest.main()
