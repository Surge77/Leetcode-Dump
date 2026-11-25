# 🔹 Mock 10 · Q3 (Hard): Freight Limits

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 10, Question 3
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

A logistics company serves `N` warehouses joined by `N − 1` roads; every warehouse can reach every other one, so there is exactly one route between any two. Road `i` joins `u` and `v` and has a toll class `w`. A truck driving from one warehouse to another needs a permit for the **highest** toll class on its route.

Answer `Q` queries: for warehouses `a` and `b`, print the highest toll class on the route between them (`0` if `a = b`).

**Input Format**
* Line 1: two integers `N` and `Q`
* Next `N − 1` lines: three integers `u v w`
* Next `Q` lines: two integers `a b`

**Output Format**
* `Q` lines, one answer each.

**Constraints**
* `1 ≤ N, Q ≤ 10⁵`
* `1 ≤ w ≤ 10⁹`

**Sample Input**
```text
6 3
1 2 4
2 3 7
2 4 1
4 5 9
4 6 2
3 5
6 6
1 6
```

**Sample Output**
```text
9
0
4
```

**Explanation:** Route `3 → 2 → 4 → 5` uses classes `7, 1, 9`, so it needs class 9. Route `6 → 6` uses no road. Route `1 → 2 → 4 → 6` uses `4, 1, 2`, so it needs class 4.

---

## 🔹 Practise & Judge

1. Write your solution as a stdin → stdout program, e.g. `my_m10q3.py`.
2. Judge it: `python tools/judge/judge.py M10Q3 my_m10q3.py` — sample, random and max-size tests with
   a time limit, scored per test case like the real exam.
3. Only then open the [solution](solutions/Q3_Hard_Freight_Limits.md).
