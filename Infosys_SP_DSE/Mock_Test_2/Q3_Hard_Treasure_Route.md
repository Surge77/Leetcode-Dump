# 🔹 Mock 2 · Q3 (Hard): Treasure Route

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 2, Question 3
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

A robot stands on cell `S` of an `R × C` warehouse grid. Cells are `.` (free), `#` (wall), `S` (start, free) or `T` (a treasure, free). Each move goes to an adjacent free cell (up, down, left, right) and takes one step.

Print the minimum number of steps needed to visit **every** treasure (in any order, ending anywhere), or `-1` if some treasure cannot be reached.

**Input Format**
* Line 1: two integers `R` and `C`
* Next `R` lines: a string of length `C`

**Output Format**
* One integer — the minimum number of steps, or `-1`.

**Constraints**
* `1 ≤ R, C ≤ 50`
* Exactly one `S`; `0 ≤ number of T ≤ 12`

**Sample Input**
```text
4 5
S..T.
.##..
T...#
..#.T
```

**Sample Output**
```text
11
```

**Explanation:** The robot must pick the best order of the three treasures; trying every order with the true walking distances gives the answer.

---

## 🔹 Practise & Judge

1. Write your solution as a stdin → stdout program, e.g. `my_m2q3.py`.
2. Judge it: `python tools/judge/judge.py M2Q3 my_m2q3.py` — sample, random and max-size tests with
   a time limit, scored per test case like the real exam.
3. Only then open the [solution](solutions/Q3_Hard_Treasure_Route.md).
