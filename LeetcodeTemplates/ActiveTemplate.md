---
difficulty: {{difficulty}}
tags: [{{tags}}]
---

# {{number}}. {{title}}

**🔗 Link:** [LeetCode {{number}}](https://leetcode.com/problems/{{slug}}/)
**🟢 Status:** 🔄 Need Review

<!-- Created by `python tools/new_note.py`, which fills the {{…}} fields. difficulty: Easy | Medium | Hard.
     tags: 1-4 slugs from tools/taxonomy.json, at least one from the folder's tags_any list.
     `python tools/build_index.py --check` enforces the format. Delete this comment. -->

## 🔹 Problem Statement

A 2-4 sentence paraphrase. Never copy LeetCode's wording.

* **Example:** `input` → `output`
* **Constraints:** sizes and value ranges (they decide the complexity you need)

## 🔹 Recognition Signal

One line: the clue in the statement → the pattern, phrased for spotting it in a NEW problem.

## 🔹 Clarifying Questions

* What you would ask before coding → the answer from the constraints (duplicates? negatives? empty input? sorted?).

## 🔹 Approach Ladder

| Step | Idea | Time | Space |
|---|---|---|---|
| Brute force | the obvious approach (the first code block below) | O(?) | O(?) |
| Better | a real middle step, if there is one (memoization, sorting first, a heap) | O(?) | O(?) |
| Optimal | the approach in the last code block | O(?) | O(?) |

## 🔹 Why It Works

The invariant or exchange argument that makes the optimal approach correct, in 1-3 sentences.

## 🔹 Say It Out Loud

*Yours to write once you have solved it unaided: the approach in about 30 seconds, as you would explain it to an interviewer.*

## 🔹 Dry Run

A short trace of the optimal approach on one small example (a table works well).

## 🔹 Test Cases

* `input` → `expected`: empty, single element, duplicates, maximum size, and the case that breaks the naive idea.

## 🔹 Bugs to Watch

* A pitfall tied to a specific line or boundary of the optimized code.

## 🔹 Follow-ups & Variations

* A likely interviewer follow-up → the short answer.

## 🔹 Related

* [N. Title](../Folder/N.Title.md): how it relates (problems with a note here are links; `build_index.py` keeps the paths right)

## 🔹 Code Snippet (Brute Force)

```python
# the approach from the ladder's first row: same class and method signature as the optimized one
```

## 🔹 Code Snippet (Optimized)

```python
# must be the LAST python block: tools/verify loads it as the reference solution
```

## 🔹 My Attempts

*One line per attempt, e.g. `2026-12-01 · 24 min · ok · missed the empty input`. `python tools/review.py log N <grade> --mins M --note "…"` adds it for you.*
