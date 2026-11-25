# 🔹 Mock 6 · Q3 (Hard): Rising Streaks

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 6, Question 3
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

Given an array `A` of `N` integers and an integer `K`, count the **strictly increasing subsequences of length exactly `K`** (choose indices `i₁ < i₂ < … < i_K` with `A[i₁] < A[i₂] < … < A[i_K]`). Print the count modulo `10⁹ + 7`.

**Input Format**
* Line 1: two integers `N` and `K`
* Line 2: `N` integers `A[1..N]`

**Output Format**
* One integer — the count modulo `10⁹ + 7`.

**Constraints**
* `1 ≤ N ≤ 10⁴`, `1 ≤ K ≤ 10`, `1 ≤ A[i] ≤ 10⁹`

**Sample Input**
```text
5 2
1 3 2 4 5
```

**Sample Output**
```text
9
```

**Explanation:** Increasing pairs: `(1,3) (1,2) (1,4) (1,5) (3,4) (3,5) (2,4) (2,5) (4,5)`.

---

## 🔹 Practise & Judge

1. Write your solution as a stdin → stdout program, e.g. `my_m6q3.py`.
2. Judge it: `python tools/judge/judge.py M6Q3 my_m6q3.py` — sample, random and max-size tests with
   a time limit, scored per test case like the real exam.
3. Only then open the [solution](solutions/Q3_Hard_Rising_Streaks.md).
