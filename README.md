## LeetCode-Dump ✨🚀📚

This repository is my **personal collection of LeetCode problem solutions**. It is designed to track my learning journey and serve as a quick reference for revisiting problem-solving techniques. Each solution is written with a focus on **clarity, clean code, and optimal approaches**. 🔍💡📝

---

### **What's Inside?** 🎯📂🔑

* **Organized solutions:** Grouped by pattern folders — browse them all in **[INDEX.md](INDEX.md)** (number, difficulty, status).
* **Every famous sheet, complete:** all of **NeetCode 150** (incl. Blind 75), **LeetCode Top Interview 150**, **Grind 169**, **LeetCode 75** and the LeetCode problems of **Striver's A2Z sheet** (which covers the SDE sheet) — follow them topic by topic in **[SHEETS.md](SHEETS.md)**.
* **Step-by-step approaches:** From brute force to optimized solutions.
* **Clear explanations:** Each solution includes **core logic**, **time/space complexity**, and important **edge cases**.
* **Language:** Every note has a **Python** solution; some older notes also keep their original **Java** version.
* **Verified code:** `python tools/verify/verify.py` runs the code of every note against brute-force or reference checks; GitHub Actions runs it on pushes to `master` and on pull requests.
* **Consistent format:** `python tools/build_index.py --check` rejects a note whose header, status or link line drifts from [the template](LeetcodeTemplates/ActiveTemplate.md).

---

### **Infosys SP / DSE Prep** 🎯

[`Infosys_SP_DSE/`](Infosys_SP_DSE/README.md) maps this repo onto the Infosys Specialist Programmer / Digital Specialist Engineer online test (3 questions, 3 hours, Easy → Medium → Hard): ten original mock tests in the exam's stdin/stdout format, an offline **judge** that scores your own solution per test case (`python tools/judge/judge.py M1Q2 my_q2.py`), random 3-question papers (`python tools/judge/paper.py`), a Python contest template, and a topic map from each exam slot to the problems here.

[`Interview_Prep/`](Interview_Prep/README.md) covers the technical interview that follows: SQL queries (each verified against SQLite), OOP with runnable examples, and DBMS / OS essentials.

---

### **Key Problem-Solving Patterns** 🧩🎓⚡

The solutions in this repository cover common problem-solving patterns like:

* **Two Pointers & Sliding Window**
* **Binary Search & Divide and Conquer**
* **Dynamic Programming (DP)**
* **Dynamic Programming variants** (knapsack, LIS, interval, bitmask, digit, tree DP)
* **Graph Algorithms (DFS, BFS, Dijkstra, Bellman-Ford, Floyd-Warshall, Topological Sort, Union-Find, Bridges)**
* **Range Queries (Prefix Sums, Segment Tree, Fenwick Tree)**
* **Number Theory & Modular Arithmetic**
* **Tree Traversals, BSTs & Recursion**
* **Linked Lists & String Processing**
* **Meet in the Middle & Binary Lifting**
* **Greedy and Backtracking**
* **Heap, Stack, and Queue problems**
* **String Matching (KMP) & Tries**

---

### **How I Use This Repository** 🛠️📖🚀

1. **Practice problems:** I use this repository as a log of problems I’ve solved.
2. **Review patterns:** Revisiting solutions helps me quickly identify and recall patterns.
3. **Iterative improvement:** I update solutions as I discover better or more efficient approaches.
4. **Daily review:** `python tools/review.py` picks today's problems from the 🔄 notes (title and link only — spotting the pattern is part of the drill). After solving, run `python tools/review.py log 322 pass` (or `fail`). Reviews are spaced 1 → 3 → 7 → 16 → 35 days apart. Two passes in a row flip the note to ✅ and a fail flips it back. `python tools/review.py stats` shows progress.
5. **Run the checks:** `python tools/verify/verify.py` (all notes) or `python tools/verify/verify.py 322 704` (selected ones). After adding a note, run `python tools/build_index.py` to refresh the index.
6. **One-time setup per clone:** `git config core.hooksPath .githooks` enables a pre-commit hook. It runs the format/index check in under a second.

---

### **Best Practices I Follow** 🧠✔️🔧

* Documenting **time & space complexity** for every solution.
* Writing **readable, clean code** with intuitive variable names.
* Showing **multiple approaches** for comparison.
* Including **detailed reasoning** for tricky or less obvious solutions.

---

### **Personal Roadmap** 🗺️🚧📈

* Clear the **🔄 Need Review** queue with `tools/review.py` (each note needs two spaced, unaided passes).
* Sit every Infosys mock test under a 3-hour timer, then random papers, and judge every answer.
* Add **flowcharts or step-by-step breakdowns** for complex problems.
* Maintain **regular updates** as I practice new problems.

---

**Happy Coding!** ✍️💻😊

> *"The best way to improve problem-solving skills is consistent, structured practice."*
