"""Runnable examples must actually run (each block carries its own asserts): Interview_Prep pages and the
template on every pattern page (<Folder>/README.md)."""
import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RUNNABLE = ("Low_Level_Design.md", "Language_Internals.md")
BLOCK_RE = re.compile(r"^```python\n(.*?)^```", re.S | re.M)


class PatternTemplatesTest(unittest.TestCase):
    def test_every_pattern_page_has_a_template_that_runs(self):
        folders = json.loads((REPO / "tools" / "taxonomy.json").read_text(encoding="utf-8"))["folders"]
        for folder in folders:
            with self.subTest(folder=folder):
                blocks = BLOCK_RE.findall((REPO / folder / "README.md").read_text(encoding="utf-8"))
                self.assertTrue(blocks, f"{folder}/README.md has no template")
                for code in blocks:
                    exec(compile(code, f"{folder}/README.md", "exec"), {"__name__": f"pattern_{folder}"})


class RunnableExamplesTest(unittest.TestCase):
    def test_every_python_block_runs(self):
        for name in RUNNABLE:
            blocks = BLOCK_RE.findall((REPO / "Interview_Prep" / name).read_text(encoding="utf-8"))
            self.assertTrue(blocks, f"{name} has no python blocks")
            for i, code in enumerate(blocks):
                with self.subTest(page=name, block=i):
                    exec(compile(code, f"{name} block {i}", "exec"), {"__name__": f"prep_{i}"})


if __name__ == "__main__":
    unittest.main()
