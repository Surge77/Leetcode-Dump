# 🔹 Mock 6 · Q1 (Easy): Festival Lamps

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 6, Question 1
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

A street has lamps numbered `1..N`. You are given `K` distinct primes `p[1..K]`. Lamp `x` is switched **on** if `x` is divisible by **at least one** of the primes.

Print how many lamps are on.

**Input Format**
* Line 1: two integers `N` and `K`
* Line 2: `K` distinct primes

**Output Format**
* One integer — the number of lamps that are on.

**Constraints**
* `1 ≤ N ≤ 10¹⁸`, `1 ≤ K ≤ 12`, `2 ≤ p[i] ≤ 100`

**Sample Input**
```text
100 2
2 3
```

**Sample Output**
```text
67
```

**Explanation:** `50` multiples of 2, `33` of 3, minus `16` multiples of 6 counted twice.

---

## 🔹 Practise & Judge

1. Write your solution as a stdin → stdout program, e.g. `my_m6q1.py`.
2. Judge it: `python tools/judge/judge.py M6Q1 my_m6q1.py` — sample, random and max-size tests with
   a time limit, scored per test case like the real exam.
3. Only then open the [solution](solutions/Q1_Easy_Festival_Lamps.md).
