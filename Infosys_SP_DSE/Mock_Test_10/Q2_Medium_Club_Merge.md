# 🔹 Mock 10 · Q2 (Medium): Club Merge

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 10, Question 2
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

A college has `N` students, each initially in a club of their own. Over the semester `M` friendships form, one at a time. When students `u` and `v` become friends, their two clubs (if different) merge into one club.

After **each** friendship, print the current number of clubs and the size of the largest club.

**Input Format**
* Line 1: two integers `N` and `M`
* Next `M` lines: two integers `u v` (`u ≠ v`; the same pair may appear more than once)

**Output Format**
* `M` lines: two integers each — the number of clubs and the largest club size after that friendship.

**Constraints**
* `2 ≤ N ≤ 2·10⁵`
* `1 ≤ M ≤ 2·10⁵`

**Sample Input**
```text
5 4
1 2
3 4
2 1
2 3
```

**Sample Output**
```text
4 2
3 2
3 2
2 4
```

**Explanation:** After `1–2` and `3–4` the clubs are `{1,2} {3,4} {5}`. `2–1` changes nothing. `2–3` merges the two pairs into `{1,2,3,4}`, leaving 2 clubs, the largest of size 4.

---

## 🔹 Practise & Judge

1. Write your solution as a stdin → stdout program, e.g. `my_m10q2.py`.
2. Judge it: `python tools/judge/judge.py M10Q2 my_m10q2.py` — sample, random and max-size tests with
   a time limit, scored per test case like the real exam.
3. Only then open the [solution](solutions/Q2_Medium_Club_Merge.md).
