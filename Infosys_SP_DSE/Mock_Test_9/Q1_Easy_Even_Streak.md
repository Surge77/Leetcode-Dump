# 🔹 Mock 9 · Q1 (Easy): Even Streak

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 9, Question 1
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

A fitness app logs the number of steps a user walked on each of `N` days. The coach likes even step counts and will tolerate **at most `K` odd** days in a streak.

Print the length of the longest run of consecutive days that contains at most `K` odd step counts.

**Input Format**
* Line 1: two integers `N` and `K`
* Line 2: `N` integers `A[1..N]`

**Output Format**
* One integer — the longest valid run (0 if none).

**Constraints**
* `1 ≤ N ≤ 2·10⁵`
* `0 ≤ K ≤ N`
* `1 ≤ A[i] ≤ 10⁹`

**Sample Input**
```text
8 2
2 3 4 6 5 8 7 9
```

**Sample Output**
```text
6
```

**Explanation:** Days 1–6 (`2 3 4 6 5 8`) contain two odd counts. Any longer run includes at least three of `3, 5, 7, 9`.

---

## 🔹 Practise & Judge

1. Write your solution as a stdin → stdout program, e.g. `my_m9q1.py`.
2. Judge it: `python tools/judge/judge.py M9Q1 my_m9q1.py` — sample, random and max-size tests with
   a time limit, scored per test case like the real exam.
3. Only then open the [solution](solutions/Q1_Easy_Even_Streak.md).
