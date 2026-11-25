# 🔹 Mock 1 · Q2 (Medium): Lucky Subsets

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 1, Question 2
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

A team has `N` coupons with values `A[1..N]`. A **non-empty** set of coupons is *lucky* if the sum of its values is divisible by `M`.

Count the lucky sets. Two sets are different if they contain different coupon **indices** (coupons with equal values are still different coupons). Print the answer modulo `10⁹ + 7`.

**Input Format**
* Line 1: two integers `N` and `M`
* Line 2: `N` integers `A[1..N]`

**Output Format**
* One integer — the number of lucky sets modulo `10⁹ + 7`.

**Constraints**
* `1 ≤ N ≤ 1000`
* `1 ≤ M ≤ 1000`
* `0 ≤ A[i] ≤ 10⁹`

**Sample Input**
```text
4 3
1 2 3 4
```

**Sample Output**
```text
5
```

**Explanation:** The sets with a sum divisible by 3 are exactly `{3}`, `{1, 2}`, `{2, 4}`, `{1, 2, 3}` and `{2, 3, 4}`.

---

## 🔹 Practise & Judge

1. Write your solution as a stdin → stdout program, e.g. `my_m1q2.py`.
2. Judge it: `python tools/judge/judge.py M1Q2 my_m1q2.py` — sample, random and max-size tests with
   a time limit, scored per test case like the real exam.
3. Only then open the [solution](solutions/Q2_Medium_Lucky_Subsets.md).
