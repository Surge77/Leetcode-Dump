# 🔹 Mock 1 · Q3 (Hard): Stock Ticker Queries

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 1, Question 3
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

A trading desk records the profit `A[i]` (possibly negative) of each of `N` days. It must answer `Q` operations of two types:

* `1 i x` — the profit of day `i` is corrected to `x`.
* `2 l r` — print the **maximum sum of a non-empty contiguous block of days** inside days `l..r`.

**Input Format**
* Line 1: two integers `N` and `Q`
* Line 2: `N` integers `A[1..N]`
* Next `Q` lines: an operation `t a b` as described (1-indexed)

**Output Format**
* For every type-2 operation, print the answer on its own line.

**Constraints**
* `1 ≤ N, Q ≤ 10⁵`
* `-10⁹ ≤ A[i], x ≤ 10⁹`
* `1 ≤ l ≤ r ≤ N`, `1 ≤ i ≤ N`

**Sample Input**
```text
5 4
2 -3 4 -1 2
2 1 5
1 4 -5
2 1 5
2 1 2
```

**Sample Output**
```text
5
4
2
```

**Explanation:** Initially the best block is `4 -1 2` (sum 5). After day 4 becomes `-5`, the best block is just `4`. In days 1..2 the best block is `2`.

---

## 🔹 Practise & Judge

1. Write your solution as a stdin → stdout program, e.g. `my_m1q3.py`.
2. Judge it: `python tools/judge/judge.py M1Q3 my_m1q3.py` — sample, random and max-size tests with
   a time limit, scored per test case like the real exam.
3. Only then open the [solution](solutions/Q3_Hard_Stock_Ticker_Queries.md).
