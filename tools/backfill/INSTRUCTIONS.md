# Task: interview-ready sections for LeetCode notes (structured output only)

All paths are relative to the repo root. Your manifest is `tools/backfill/manifests/manifest_XX.json`; the list of every
note is `tools/backfill/catalog.tsv`. Each note is a Markdown file of one LeetCode problem with
a Problem Statement, prose sections (Quick Breakdown, Optimization Path, Solution Breakdown, Pattern Recognition,
Tricks & Patterns Used, Alternative Data Structures, Complexity Analysis) and two verified Python solutions
(brute force + optimized). A script will REPLACE the old prose sections with new ones built from your JSON, and keep
the Problem Statement, the code sections and any non-standard sections exactly as they are.

**Do not edit any file in the repo.** Read the notes listed in your manifest and write ONE JSON file.
`tools/backfill/sample_139.json` is a complete, correct example entry.

## Output

Write `tools/backfill/out/batch_XX.json` (XX = your manifest number): a JSON object keyed by the note number as a
string. UTF-8. Validate it parses (e.g. `python -c "import json;json.load(open(...,encoding='utf-8'))"`) before finishing.

```json
{
  "139": {
    "tags": ["dp-1d", "dp-strings", "trie"],
    "signal": "\"Can the string be cut into dictionary words?\" (or how many ways / minimum cuts) → DP over prefixes: dp[i] = the first i characters can be split.",
    "clarify": [
      "Can a dictionary word be reused? → Yes, any number of times.",
      "Are the words unique, and is everything lowercase? → Yes to both.",
      "Return a bool, or the actual split? → Just whether a split exists (Word Break II asks for all splits)."
    ],
    "ladder": [
      {"step": "Brute force", "idea": "Recursively try every dictionary word as the next piece.", "time": "O(2ⁿ)", "space": "O(n)"},
      {"step": "Better", "idea": "Memoize the recursion on the start index, so each suffix is solved once.", "time": "O(n² · L)", "space": "O(n)"},
      {"step": "Optimal", "idea": "Bottom-up dp[i] over prefixes; only try last words up to the longest dictionary word, and break once dp[i] is True.", "time": "O(n · L²)", "space": "O(n + dictionary)"}
    ],
    "why": "Any valid split of s[:i] ends with some word s[j:i], and what remains, s[:j], must itself be splittable. So dp[i] only depends on smaller prefixes, and bounding j by the longest word length L keeps the inner loop short.",
    "dry_run": "`s = \"leetcode\"`, words `{leet, code}`, L = 4\n\n| i | prefix | last word tried | dp[i] |\n|---|---|---|---|\n| 0 | \"\" | (base) | T |\n| 4 | leet | s[0:4] = leet, dp[0] = T | T |\n| 8 | leetcode | s[4:8] = code, dp[4] = T | **T** |",
    "tests": [
      "Whole string is one word: `\"apple\"`, `[\"apple\"]` → true",
      "Words that prefix each other: `\"catsandog\"`, `[\"cats\",\"dog\",\"sand\",\"and\",\"cat\"]` → false",
      "Reuse a word: `\"aaaa\"`, `[\"a\"]` → true",
      "Exponential trap for plain recursion: `\"aaaaaaaaaaaaaaaaaaaab\"`, `[\"a\",\"aa\",\"aaa\"]` → false (must be fast)"
    ],
    "bugs": [
      "`dp` needs n + 1 slots with `dp[0] = True`; an n-slot array is off by one on the last prefix.",
      "`range(max(0, i - max_len), i)`: forgetting `max(0, …)` makes j negative and silently slices from the end.",
      "Keep `words` a set: `s[j:i] in wordDict` on a list is O(m) per lookup."
    ],
    "followups": [
      "Return every sentence (Word Break II) → DFS from each index with memoized lists of sentences.",
      "Minimum number of words → dp[i] = 1 + min over valid j, initialised to infinity.",
      "Very long dictionary words → walk a Trie forward from each reachable index instead of slicing and hashing."
    ],
    "related": [
      {"number": 140, "title": "Word Break II", "why": "return all splits: DFS + memo"},
      {"number": 132, "title": "Palindrome Partitioning II", "why": "same prefix DP, minimise cuts"},
      {"number": 91, "title": "Decode Ways", "why": "count the splits instead"}
    ]
  }
}
```

## Fields (all required unless stated)

* **tags**: 1–4 slugs from the vocabulary below, most specific first. At least one must be in the `tags_any` list of
  the note's `folder` from the manifest (see "Folders").
* **signal**: ONE line, at most about 200 characters: the clue in the problem statement → the pattern. Phrase it as
  what you'd notice when reading a NEW problem, not a summary of this one.
* **clarify**: 2–3 questions a strong candidate asks before coding, each with ` → ` and the answer taken from the
  statement and constraints (duplicates? negatives? empty input? sorted? ties? return format? overflow?).
* **ladder**: 2–3 steps, `Brute force` first, `Optimal` last, an optional `Better` in between when a real middle
  step exists (memoization, sorting first, a heap instead of sorting, and so on). The Brute force and Optimal steps
  MUST describe the note's two code blocks and match their complexities. Use the note's Optimization Path and
  Complexity Analysis, and correct them if they disagree with the code.
* **why**: 1–3 sentences: the invariant or exchange argument that makes the optimal approach correct.
* **dry_run**: a short trace of the optimal approach on ONE small example, at most ~10 lines of Markdown (a table is
  ideal). It must be correct: actually trace the code.
* **tests**: 3–6 edge cases, each with its input and the expected result. Include the case that breaks the naive idea,
  if there is one. Fold in the note's "Edge Cases Considered".
* **bugs**: 2–4 concrete pitfalls tied to the actual optimized code (name the line, condition or boundary). Fold in the
  note's "Mistakes to Avoid" when they are concrete; drop generic advice.
* **followups**: 2–4 likely interviewer follow-ups, each `question → short answer`. Fold in the useful content of
  "Further Improvements", "Tricks & Patterns Used" and "Alternative Data Structures" so nothing valuable is lost.
* **related**: 2–5 problems from the note's "Common Problems Using This" or that you know. Prefer problems that are in
  the repo (see `catalog.tsv`). `number` must be the real LeetCode number and `title` its real title; `why` is a few words.
* **statement** (ONLY for a note that has no "Problem Statement" section): a 2–4 sentence paraphrase, then
  `* **Example:** …` and `* **Constraints:** …` lines, in the style of the other notes. Never copy LeetCode's wording.

## Rules

* Accuracy first. Every complexity, trace and expected output must be correct. If the old prose was wrong, fix it in
  your JSON; never repeat an error.
* Write in plain, direct English. Use `code` for identifiers and inputs. No filler ("This problem is a classic…"),
  no emojis, no headings inside fields, no HTML.
* Do not invent constraints. Take them from the Problem Statement section.
* Notes with unusual extra sections (for example "80/20", "Common Misconceptions", "Step 1 …"): leave those sections
  alone (the script keeps them); just write the fields. Never write the personal sections ("Say It Out Loud",
  "My Attempts").
* Each manifest row has the note's current `tags`, derived automatically. Keep them if they are right; refine
  them (e.g. add `trie` or `dp-strings`) when they miss a pattern the solution really uses.
* Keep the whole batch consistent: similar problems get the same tags and similar phrasing for the same idea.

## Folders and their accepted tags

See `tools/taxonomy.json` in the repo: `folders.<name>.tags_any`. The full tag vocabulary is its `tags` object; use
only those slugs.

## Finish

Report in at most 5 lines: the file written, how many notes, and any note where the old prose or code looked wrong
(number + one line). Do not paste the JSON into your report.
