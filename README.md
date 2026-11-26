## LeetCode-Dump ✨🚀📚

My **personal DSA notebook**: every problem from the major interview sheets, written up as a pattern note with a **brute-force and an optimized Python solution that are checked against each other automatically**. It also includes an exam kit for the **Infosys SP / DSE** online test. 🔍💡📝

| | |
|---|---|
| **LeetCode notes** | **463** (Easy 107 · Medium 269 · Hard 87) in 50 pattern folders → [INDEX.md](INDEX.md) |
| **Sheets covered 100%** | NeetCode 150 · LeetCode Top Interview 150 · Grind 169 · LeetCode 75 · Striver A2Z (its LeetCode problems) → [SHEETS.md](SHEETS.md) |
| **Infosys mock problems** | 30 original stdin/stdout problems (10 mock tests) with an offline judge → [Infosys_SP_DSE](Infosys_SP_DSE/README.md) |
| **Interview round** | SQL (verified on SQLite), OOP, DBMS / OS → [Interview_Prep](Interview_Prep/README.md) |
| **Checks** | 689 automated checks, run in CI on every push to `master` and every pull request (~70 s) |

The live ✅ / 🔄 counts are in [INDEX.md](INDEX.md) and [SHEETS.md](SHEETS.md). Both are regenerated from the notes, so they are always current.

---

### **Start Here** 🎯

| I want to… | Do this |
|---|---|
| Follow a sheet topic by topic | Open [SHEETS.md](SHEETS.md), pick a sheet, work down its topics |
| Revise what I haven't mastered | `python tools/review.py` → solve today's picks unaided → `python tools/review.py log <#> pass` (or `fail`) |
| Practise for the Infosys test | `python tools/judge/paper.py` for a random 3-hour paper, then `python tools/judge/judge.py M1Q2 my_q2.py` to score each answer |
| Find a pattern's problems | [INDEX.md](INDEX.md) (by folder) or the [topic map](Infosys_SP_DSE/README.md#-topic-map--problems-in-this-repo) (by exam slot) |

---

### **What Every Note Contains** 📂

Each note follows [the template](LeetcodeTemplates/ActiveTemplate.md):

* **Header:** `N. Title (Category, Difficulty)`, the LeetCode link, and the status: **✅ Solved** or **🔄 Need Review**.
* **Quick Breakdown, Optimization Path, Solution Breakdown:** the main idea, when to use the pattern, the mistakes to avoid, and *why* the approach works.
* **Pattern Recognition:** related problems; "(in this repo)" marks the ones that have a note here.
* **Complexity Analysis** for both approaches.
* **Code Snippet (Brute Force)** and **Code Snippet (Optimized)**, both in Python. Some older notes also keep their original Java.
* LeetCode Premium problems carry a 🔒 line pointing to a free copy (neetcode.io / LintCode).

---

### **Tools** 🛠️

| Command | What it does |
|---|---|
| `python tools/verify/verify.py [N …]` | Runs every note's code (or only the notes you list). Brute force and optimized are compared on random inputs, plus LeetCode's examples and max-size runs. `VERIFY_TIMING=1` also enforces the time limits. |
| `python tools/build_index.py [--check]` | Lints note format and regenerates `INDEX.md` and `SHEETS.md` (sheet data: `tools/sheets.json`). `--check` fails on drift (used by CI and the hook). |
| `python tools/review.py [today\|log\|show\|stats]` | Spaced-repetition drill over the 🔄 notes. It shows the title and link only, so spotting the pattern is part of the drill. Reviews are spaced 1 → 3 → 7 → 16 → 35 days apart. Two passes in a row flip a note to ✅; a fail flips it back. Progress: `tools/review_state.json`. |
| `python tools/judge/judge.py MxQy file.py` | Offline judge for the mock problems. Scores out of 100: small tests are worth 50 and max-size tests 50, with a time limit that adapts to your machine's speed. |
| `python tools/judge/paper.py` | Random Easy/Medium/Hard paper drawn from three different mocks. |
| `python -m unittest discover -s tools/tests` | Unit tests for the judge and the review drill. |

**One-time setup per clone:** run `git config core.hooksPath .githooks`. This enables a pre-commit hook that runs the format/index check on the staged files in under a second.

**Adding a note:**
1. Copy the template into the right pattern folder as `N.Title_With_Underscores.md`.
2. Write the brute-force and optimized Python blocks. The optimized one must be the **last** Python block.
3. Add a `@case(N)` in a `tools/verify/tests_*.py` file.
4. Run `verify.py N`, then `build_index.py`, and commit.

---

### **Key Problem-Solving Patterns** 🧩

Two Pointers & Sliding Window · Binary Search (incl. on the answer) & Divide and Conquer · Prefix Sums & Difference Arrays · Hashing · Stacks, Queues & Monotonic Stack · Linked Lists · Trees, BSTs, Tries & Binary Lifting · Heaps / Top-K · Greedy & Intervals · Backtracking · Graphs (BFS/DFS, Dijkstra, Bellman-Ford, Floyd-Warshall, topological sort, Union-Find, MST, bridges, SCC) · Dynamic Programming (1-D, grid/strings, knapsack, LIS, interval, bitmask, digit, tree / rerooting, matrix exponentiation) · Segment Tree & Fenwick Tree · Number Theory & Modular Arithmetic · Game Theory · Meet in the Middle · String Matching (KMP, Z, rolling hash, Manacher) · Bit Manipulation

---

### **Roadmap** 🗺️

* Clear the **🔄 Need Review** queue with `tools/review.py`. Each note needs two spaced, unaided passes.
* Sit all ten Infosys mock tests under a 3-hour timer, then random papers. Judge every answer.
* Add flowcharts or step-by-step breakdowns for the hardest problems.

---

**Happy Coding!** ✍️💻😊

> *"The best way to improve problem-solving skills is consistent, structured practice."*
