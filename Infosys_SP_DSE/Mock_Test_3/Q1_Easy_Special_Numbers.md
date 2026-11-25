# 🔹 Mock 3 · Q1 (Easy): Special Numbers

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 3, Question 1
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

A number is *special* if it has **exactly three** positive divisors (for example, `4` has divisors `1, 2, 4`).

You are given `T` queries. For each query `N`, print how many special numbers lie in `[1, N]`.

**Input Format**
* Line 1: integer `T`
* Next `T` lines: one integer `N`

**Output Format**
* `T` lines — the answer for each query.

**Constraints**
* `1 ≤ T ≤ 10⁵`
* `1 ≤ N ≤ 10¹²`

**Sample Input**
```text
3
10
50
1000000000000
```

**Sample Output**
```text
2
4
78498
```

**Explanation:** Special numbers up to 50 are `4, 9, 25, 49` — squares of the primes `2, 3, 5, 7`. For `N = 10¹²` the answer is the number of primes up to `10⁶`, which is 78498.

---

## 🔹 Practise & Judge

1. Write your solution as a stdin → stdout program, e.g. `my_m3q1.py`.
2. Judge it: `python tools/judge/judge.py M3Q1 my_m3q1.py` — sample, random and max-size tests with
   a time limit, scored per test case like the real exam.
3. Only then open the [solution](solutions/Q1_Easy_Special_Numbers.md).
