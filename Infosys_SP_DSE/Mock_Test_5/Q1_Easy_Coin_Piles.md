# 🔹 Mock 5 · Q1 (Easy): Coin Piles

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 5, Question 1
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

There are `N` piles of coins; pile `i` has `A[i]` coins. Two players move alternately; **First** moves first. A move removes between `1` and `K` coins from **one** pile. A player who cannot move (all piles empty) loses.

Both play optimally. Print `First` or `Second` — the winner.

**Input Format**
* Line 1: two integers `N` and `K`
* Line 2: `N` integers `A[1..N]`

**Output Format**
* `First` or `Second`

**Constraints**
* `1 ≤ N ≤ 2·10⁵`, `1 ≤ K ≤ 10⁹`, `0 ≤ A[i] ≤ 10⁹`

**Sample Input**
```text
3 2
3 4 5
```

**Sample Output**
```text
First
```

**Explanation:** Grundy values with `K = 2` are `3 % 3 = 0`, `4 % 3 = 1`, `5 % 3 = 2`; their XOR is 3 ≠ 0.

---

## 🔹 Practise & Judge

1. Write your solution as a stdin → stdout program, e.g. `my_m5q1.py`.
2. Judge it: `python tools/judge/judge.py M5Q1 my_m5q1.py` — sample, random and max-size tests with
   a time limit, scored per test case like the real exam.
3. Only then open the [solution](solutions/Q1_Easy_Coin_Piles.md).
