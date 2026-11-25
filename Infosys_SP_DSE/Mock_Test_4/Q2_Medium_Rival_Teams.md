# 🔹 Mock 4 · Q2 (Medium): Rival Teams

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 4, Question 2
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

`N` students (numbered `1..N`) must be split into **two teams** (a team may be empty), and every student must join exactly one. There are `M` rival pairs; two rivals may not be on the same team.

If no valid split exists, print `-1`. Otherwise print the **minimum possible difference** between the two team sizes.

**Input Format**
* Line 1: two integers `N` and `M`
* Next `M` lines: two integers `u v` — students `u` and `v` are rivals

**Output Format**
* One integer — the minimum size difference, or `-1`.

**Constraints**
* `1 ≤ N ≤ 2000`, `0 ≤ M ≤ 10⁴`, `u ≠ v`

**Sample Input**
```text
6 3
1 2
2 3
4 5
```

**Sample Output**
```text
0
```

**Explanation:** `{1, 3}` must be opposite `{2}`, and `4` opposite `5`; student 6 is free. Putting `{1, 3}`, `4` on one team and `{2}`, `5`, `6` on the other gives sizes 3 and 3.

---

## 🔹 Practise & Judge

1. Write your solution as a stdin → stdout program, e.g. `my_m4q2.py`.
2. Judge it: `python tools/judge/judge.py M4Q2 my_m4q2.py` — sample, random and max-size tests with
   a time limit, scored per test case like the real exam.
3. Only then open the [solution](solutions/Q2_Medium_Rival_Teams.md).
