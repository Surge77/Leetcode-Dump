# 🔹 Mock 8 · Q2 (Medium): Island Hopping

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 8, Question 2
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

A map of an archipelago is an `R × C` grid: `.` is land, `~` is water. A swimmer starts on the land cell `S` and wants to reach the land cell `T`, moving up, down, left or right one cell at a time. Walking onto a land cell (including `S` and `T`) costs nothing; **entering a water cell costs 1 unit of energy**.

Print the minimum energy needed to reach `T`.

**Input Format**
* Line 1: two integers `R` and `C`
* Next `R` lines: a string of `C` characters from `.`, `~`, `S`, `T` (exactly one `S` and one `T`)

**Output Format**
* One integer — the minimum energy.

**Constraints**
* `1 ≤ R, C ≤ 500`, `R · C ≥ 2`

**Sample Input**
```text
4 5
S.~..
~~~~.
..~~.
.T~..
```

**Sample Output**
```text
1
```

**Explanation:** `S` sits on a two-cell island and `T` on a four-cell island just below it, separated by one row of water. Swim down into `(2, 1)` (1 unit), then walk `(3, 1) → (4, 1) → (4, 2) = T`. Reaching `T` with 0 energy is impossible because every cell next to `S`'s island is water.

---

## 🔹 Practise & Judge

1. Write your solution as a stdin → stdout program, e.g. `my_m8q2.py`.
2. Judge it: `python tools/judge/judge.py M8Q2 my_m8q2.py` — sample, random and max-size tests with
   a time limit, scored per test case like the real exam.
3. Only then open the [solution](solutions/Q2_Medium_Island_Hopping.md).
