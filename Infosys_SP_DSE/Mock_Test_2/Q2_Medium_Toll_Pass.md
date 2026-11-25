# 🔹 Mock 2 · Q2 (Medium): Toll Pass

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 2, Question 2
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

A courier must travel from city `1` to city `N`. There are `M` two-way roads; road `j` connects `u` and `v` and charges a toll `w`. The courier owns **one free pass**: it makes the toll of **one** road on the route zero (it may also stay unused).

Print the minimum total toll from city `1` to city `N`, or `-1` if city `N` is unreachable.

**Input Format**
* Line 1: two integers `N` and `M`
* Next `M` lines: three integers `u v w`

**Output Format**
* One integer — the minimum total toll, or `-1`.

**Constraints**
* `1 ≤ N ≤ 10⁵`, `0 ≤ M ≤ 2·10⁵`
* `1 ≤ u, v ≤ N`
* `1 ≤ w ≤ 10⁹`

**Sample Input**
```text
4 4
1 2 5
2 4 100
1 3 20
3 4 30
```

**Sample Output**
```text
5
```

**Explanation:** Route `1 → 2 → 4` costs `5 + 100`; using the pass on the 100-toll road leaves 5. Route `1 → 3 → 4` with the pass costs at least 20.

---

## 🔹 Practise & Judge

1. Write your solution as a stdin → stdout program, e.g. `my_m2q2.py`.
2. Judge it: `python tools/judge/judge.py M2Q2 my_m2q2.py` — sample, random and max-size tests with
   a time limit, scored per test case like the real exam.
3. Only then open the [solution](solutions/Q2_Medium_Toll_Pass.md).
