# 🔹 Mock 7 · Q3 (Hard): Lantern Paths

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 7, Question 3
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

A festival ground is a grid of `H` rows and `W` columns. A lantern carrier starts at the top-left cell `(1, 1)` and must reach the bottom-right cell `(H, W)`, moving only **down** or **right** one cell at a time. `K` cells are fenced off and cannot be entered.

Count the different routes, modulo `10⁹ + 7`.

**Input Format**
* Line 1: three integers `H W K`
* Next `K` lines: two integers `r c` — a fenced cell (all distinct, never `(1, 1)` or `(H, W)`)

**Output Format**
* One integer — the number of routes modulo `10⁹ + 7`.

**Constraints**
* `1 ≤ H, W ≤ 10⁵`
* `0 ≤ K ≤ 2000`

**Sample Input**
```text
3 4 2
2 2
1 4
```

**Sample Output**
```text
3
```

**Explanation:** Of the 10 unrestricted routes, the ones that avoid `(2, 2)` and `(1, 4)` are: right-right-down-right-down, right-right-down-down-right, and down-down-right-right-right.

---

## 🔹 Practise & Judge

1. Write your solution as a stdin → stdout program, e.g. `my_m7q3.py`.
2. Judge it: `python tools/judge/judge.py M7Q3 my_m7q3.py` — sample, random and max-size tests with
   a time limit, scored per test case like the real exam.
3. Only then open the [solution](solutions/Q3_Hard_Lantern_Paths.md).
