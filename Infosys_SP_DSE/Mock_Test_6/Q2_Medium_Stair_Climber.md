# 🔹 Mock 6 · Q2 (Medium): Stair Climber

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 6, Question 2
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

A robot climbs a staircase of `N` steps. In one move it climbs exactly `s` steps, where `s` is one of `K` allowed step sizes. Count the different move sequences that end exactly on step `N`, modulo `10⁹ + 7`.

**Input Format**
* Line 1: two integers `N` and `K`
* Line 2: `K` distinct step sizes

**Output Format**
* One integer — the number of ways modulo `10⁹ + 7`.

**Constraints**
* `1 ≤ N ≤ 10¹⁸`, `1 ≤ K ≤ 10`, `1 ≤ s ≤ 10`

**Sample Input**
```text
5 2
1 2
```

**Sample Output**
```text
8
```

**Explanation:** With steps 1 and 2 the counts follow the Fibonacci numbers: 1, 1, 2, 3, 5, 8 for `N = 0..5`.

---

## 🔹 Practise & Judge

1. Write your solution as a stdin → stdout program, e.g. `my_m6q2.py`.
2. Judge it: `python tools/judge/judge.py M6Q2 my_m6q2.py` — sample, random and max-size tests with
   a time limit, scored per test case like the real exam.
3. Only then open the [solution](solutions/Q2_Medium_Stair_Climber.md).
