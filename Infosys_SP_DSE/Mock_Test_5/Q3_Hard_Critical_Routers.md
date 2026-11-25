# 🔹 Mock 5 · Q3 (Hard): Critical Routers

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 5, Question 3
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

A network has `N` routers and `M` two-way links. A router is **critical** if switching it off (together with its links) increases the number of connected groups among the remaining routers.

Print the number of critical routers on the first line. If there is at least one, print their numbers in increasing order on the second line.

**Input Format**
* Line 1: two integers `N` and `M`
* Next `M` lines: two integers `u v` — a link between `u` and `v`

**Output Format**
* Line 1: the count `C`
* Line 2 (only if `C > 0`): the critical routers, increasing, space-separated

**Constraints**
* `1 ≤ N ≤ 10⁵`, `0 ≤ M ≤ 2·10⁵`, `u ≠ v` (links may repeat)

**Sample Input**
```text
5 5
1 2
2 3
3 1
3 4
4 5
```

**Sample Output**
```text
2
3 4
```

**Explanation:** Removing router 3 separates `{1, 2}` from `{4, 5}`; removing router 4 cuts off router 5. Routers 1, 2 and 5 are not critical.

---

## 🔹 Practise & Judge

1. Write your solution as a stdin → stdout program, e.g. `my_m5q3.py`.
2. Judge it: `python tools/judge/judge.py M5Q3 my_m5q3.py` — sample, random and max-size tests with
   a time limit, scored per test case like the real exam.
3. Only then open the [solution](solutions/Q3_Hard_Critical_Routers.md).
