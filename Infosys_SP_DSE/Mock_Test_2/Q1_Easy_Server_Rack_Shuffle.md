# 🔹 Mock 2 · Q1 (Easy): Server Rack Shuffle

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 2, Question 1
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

`N` server slots are arranged in a **circle**. Slot `i` holds an active server (`1`) or is empty (`0`), given as a binary string `S`. In one operation you may **swap the contents of any two slots**.

Find the minimum number of operations needed so that all active servers occupy **consecutive** slots of the circle.

**Input Format**
* Line 1: integer `N`
* Line 2: binary string `S` of length `N`

**Output Format**
* One integer — the minimum number of swaps.

**Constraints**
* `1 ≤ N ≤ 2·10⁵`
* `S` contains only `0` and `1`

**Sample Input**
```text
7
1010011
```

**Sample Output**
```text
1
```

**Explanation:** There are four `1`s. Because the circle wraps, the window `1 1 1 0` (slots 6, 7, 1, 2) already holds three of them; one swap fixes the remaining `0`.

---

## 🔹 Practise & Judge

1. Write your solution as a stdin → stdout program, e.g. `my_m2q1.py`.
2. Judge it: `python tools/judge/judge.py M2Q1 my_m2q1.py` — sample, random and max-size tests with
   a time limit, scored per test case like the real exam.
3. Only then open the [solution](solutions/Q1_Easy_Server_Rack_Shuffle.md).
