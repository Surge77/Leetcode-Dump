# 🔹 Mock 7 · Q2 (Medium): Price Volatility

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 7, Question 2
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

A trader records the price of a stock on `N` consecutive days. The *swing* of a window of consecutive days is its highest price minus its lowest price.

Print the sum of the swings of **all** `N·(N+1)/2` windows of consecutive days.

**Input Format**
* Line 1: an integer `N`
* Line 2: `N` integers `P[1..N]`

**Output Format**
* One integer — the total swing (it fits in a signed 64-bit integer).

**Constraints**
* `1 ≤ N ≤ 10⁵`
* `1 ≤ P[i] ≤ 10⁶`

**Sample Input**
```text
4
3 1 4 1
```

**Sample Output**
```text
17
```

**Explanation:** Windows of length 1 have swing 0. Length 2: `2, 3, 3`. Length 3: `3, 3`. Length 4: `3`. Total `2 + 3 + 3 + 3 + 3 + 3 = 17`.

---

## 🔹 Practise & Judge

1. Write your solution as a stdin → stdout program, e.g. `my_m7q2.py`.
2. Judge it: `python tools/judge/judge.py M7Q2 my_m7q2.py` — sample, random and max-size tests with
   a time limit, scored per test case like the real exam.
3. Only then open the [solution](solutions/Q2_Medium_Price_Volatility.md).
