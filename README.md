## LeetCode-Dump ✨🚀📚

My **personal DSA notebook and practice system**. Every problem from the major interview sheets is a pattern note with a **brute-force and an optimized Python solution that are checked against each other and against LeetCode's official examples**. A drill schedules your reviews, judges your own attempts, and quizzes you on pattern recognition. It also includes an exam kit for the **Infosys SP / DSE** online test. 🔍💡📝

<!-- generated:stats -->
| | |
|---|---|
| **LeetCode notes** | **463** (Easy 108 · Medium 268 · Hard 87) in 50 pattern folders · ✅ 89 · 🔄 374 → [INDEX.md](INDEX.md) |
| **Sheets** | NeetCode 150 150/150 · LeetCode Top Interview 150 150/150 · Striver A2Z DSA Sheet (LeetCode problems) 232/232 · Grind 169 169/169 · LeetCode 75 75/75 → [SHEETS.md](SHEETS.md) |
| **Infosys mock problems** | 30 original stdin/stdout problems (10 mock tests) with an offline judge → [Infosys_SP_DSE](Infosys_SP_DSE/README.md) |
| **Checks** | 1122 automated checks, run in CI on every push, every pull request and weekly |
<!-- /generated:stats -->

**Interview round:** SQL (verified on SQLite), OOP, DBMS / OS → [Interview_Prep](Interview_Prep/README.md)

---

### **Start Here** 🎯

| I want to… | Do this |
|---|---|
| Practise today | `python tools/review.py` → solve each pick in your own file → `python tools/review.py check <#> my.py --log --mins <m>` |
| Follow one sheet | `python tools/review.py today --sheet neetcode` (or `grind`, `"top interview"`, `striver`, `"leetcode 75"`) |
| Train pattern recognition | `python tools/review.py quiz -n 10`: statement only, name the pattern |
| Train debugging | `python tools/review.py debug <#>`: find the bug planted in a verified solution |
| Revise on my phone | `python tools/export_anki.py` → import `exports/leetcode-dump-anki.tsv` into Anki |
| Know if I'll finish in time | `python tools/review.py plan --by 2027-01-15 --sheet neetcode` |
| See my weak spots | `python tools/review.py stats`: weakest topics, why reviews fail, time vs target |
| Practise for the Infosys test | `python tools/judge/paper.py` for a random 3-hour paper; `python tools/judge/judge.py M1Q2 my_q2.py` to score each answer. Save `--final` for the last week |

---

### **Daily Routine** 🔁

1. `python tools/review.py`: three picks, title and link only. Due reviews come first, then new problems.
2. Solve each in a plain file without opening the note. Time yourself; targets are Easy 15 / Medium 25 / Hard 40 minutes.
3. `python tools/review.py check <#> my.py --log --mins <m>` judges it with the note's own checks (official examples, random tests against the brute force, a max-size time limit) and logs the verdict. If you solved it on LeetCode instead, log it by hand: `log <#> ok|easy|hard|fail [--why pattern|approach|edge|bug|tle|forgot]`.
4. Once a week: a `quiz`, a `debug` drill, and one **cold solve**, a problem you have never seen (a LeetCode weekly contest is ideal). Log it with `review.py cold <slug> pass|fail --mins <m>`. Reviews measure memory; cold solves measure what interviews test.

Reviews are spaced 1 → 3 → 7 → 16 → 35 → 75 → 150 → 300 days, so a mastered repo costs about two reviews a day. Two clean reviews in a row turn a note ✅, and any fail turns it back to 🔄. Progress lives in `tools/review_state.json`; commit it.

---

### **What Every Note Contains** 📂

Each note follows [the template](LeetcodeTemplates/ActiveTemplate.md):

* **Header:** `N. Title (Category, Difficulty)`, the LeetCode link, and the status: **✅ Solved** or **🔄 Need Review**.
* **Problem Statement:** a paraphrase with one example and the constraints.
* **Quick Breakdown, Optimization Path, Solution Breakdown:** the main idea, when to use the pattern, the mistakes to avoid, and *why* the approach works.
* **Pattern Recognition:** related problems; "(in this repo)" marks the ones that have a note here.
* **Complexity Analysis** for both approaches.
* **Code Snippet (Brute Force)** and **Code Snippet (Optimized)**, both in Python. Some older notes also keep their original Java.
* LeetCode Premium problems carry a 🔒 line pointing to a free copy (neetcode.io / LintCode).

---

### **Tools** 🛠️

| Command | What it does |
|---|---|
| `python tools/review.py [today\|log\|check\|show\|quiz\|debug\|cold\|plan\|stats]` | The practice drill (above). `--help` on any command lists its options. |
| `python tools/export_anki.py [--status review]` | Anki deck (TSV) of every note. Re-importing updates cards instead of duplicating them. |
| `python tools/verify/verify.py [N …]` | Runs every note's code (or only the notes you list) against its checks. `--where N` prints which file holds a check. `VERIFY_TIMING=1` also enforces the time limits. |
| `python tools/build_index.py [--check]` | Lints note format and regenerates `INDEX.md`, `SHEETS.md` and this README's numbers. `--check` fails on drift (used by CI and the hook). |
| `python tools/judge/judge.py MxQy file.py` | Offline judge for the mock problems. Scores out of 100: small tests are worth 50 and max-size tests 50. |
| `python tools/judge/paper.py [--final]` | Random Easy/Medium/Hard paper drawn from three different mocks; `--final` uses the held-out mocks 8–10. |
| `python -m unittest discover -s tools/tests` | Unit tests for the drill, judge and generators. |

**One-time setup per clone:** run `git config core.hooksPath .githooks`. This enables a pre-commit hook that runs the format/index check on the staged files in under a second.

**Adding a note:**
1. Copy the template into the right pattern folder as `N.Title_With_Underscores.md`.
2. Write the brute-force and optimized Python blocks. The optimized one must be the **last** Python block.
3. Add a `@case(N)` in a `tools/verify/tests_*.py` file.
4. Run `verify.py N`, then `build_index.py`, and commit.

---

### **How These Notes Were Made** 🤖

About 95 notes predate the tooling. The other ~370, and the tooling itself, were built in late 2026 with AI assistance (Claude Code) under my direction. Every note is held to the same bar: its solutions run in CI against LeetCode's official examples and a brute force on random inputs, and its prose was audited against the official problem statement. What makes a note *mine* is the review history in `tools/review_state.json`: a ✅ means I solved it unaided, twice, days apart.

---

### **Key Problem-Solving Patterns** 🧩

Two Pointers & Sliding Window · Binary Search (incl. on the answer) & Divide and Conquer · Prefix Sums & Difference Arrays · Hashing · Stacks, Queues & Monotonic Stack · Linked Lists · Trees, BSTs, Tries & Binary Lifting · Heaps / Top-K · Greedy & Intervals · Backtracking · Graphs (BFS/DFS, Dijkstra, Bellman-Ford, Floyd-Warshall, topological sort, Union-Find, MST, bridges, SCC) · Dynamic Programming (1-D, grid/strings, knapsack, LIS, interval, bitmask, digit, tree / rerooting, matrix exponentiation) · Segment Tree & Fenwick Tree · Number Theory & Modular Arithmetic · Game Theory · Meet in the Middle · String Matching (KMP, Z, rolling hash, Manacher) · Bit Manipulation

---

### **Related** 🔗

* [dsa-lab](https://github.com/Surge77/dsa-lab): the data structures themselves (arrays, linked lists, trees, heaps, graphs), implemented from scratch in Python without built-ins. Use it when you need to know *how* a heap or a union-find works inside; use this repo to practise *using* them.
* [NOTICE.md](NOTICE.md): what belongs to LeetCode and the other sources, and what the MIT license covers.

---

**Happy Coding!** ✍️💻😊

> *"The best way to improve problem-solving skills is consistent, structured practice."*
