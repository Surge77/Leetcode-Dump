# 🔹 Mock 5 · Q2 (Medium): Price Spread

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 5, Question 2
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

You are given the closing prices `P[1..N]` of a stock. Answer `Q` queries: for days `l..r`, print the **spread** = (highest price) − (lowest price) in that range. Prices never change.

**Input Format**
* Line 1: two integers `N` and `Q`
* Line 2: `N` integers `P[1..N]`
* Next `Q` lines: two integers `l r`

**Output Format**
* `Q` lines — the spread for each query.

**Constraints**
* `1 ≤ N, Q ≤ 2·10⁵`, `1 ≤ P[i] ≤ 10⁹`, `1 ≤ l ≤ r ≤ N`

**Sample Input**
```text
6 3
4 2 7 1 8 3
1 3
2 5
6 6
```

**Sample Output**
```text
5
7
0
```

**Explanation:** Days 1..3: `7 - 2 = 5`. Days 2..5: `8 - 1 = 7`. A single day has spread 0.

---

## 🔹 Practise & Judge

1. Write your solution as a stdin → stdout program, e.g. `my_m5q2.py`.
2. Judge it: `python tools/judge/judge.py M5Q2 my_m5q2.py` — sample, random and max-size tests with
   a time limit, scored per test case like the real exam.
3. Only then open the [solution](solutions/Q2_Medium_Price_Spread.md).
