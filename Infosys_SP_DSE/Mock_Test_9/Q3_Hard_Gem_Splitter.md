# 🔹 Mock 9 · Q3 (Hard): Gem Splitter

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 9, Question 3
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

A courier can carry gems with a total weight of at most `W`. There are `N` gems; gem `i` weighs `w[i]` and is worth `v[i]`. Each gem is either taken whole or left behind.

Print the maximum total value the courier can carry.

**Input Format**
* Line 1: two integers `N` and `W`
* Next `N` lines: two integers `w[i] v[i]`

**Output Format**
* One integer — the maximum total value (0 if nothing fits).

**Constraints**
* `1 ≤ N ≤ 36`
* `1 ≤ W ≤ 10¹⁵`
* `1 ≤ w[i], v[i] ≤ 10¹²`

**Sample Input**
```text
4 10
5 10
4 40
6 30
3 50
```

**Sample Output**
```text
90
```

**Explanation:** Take the gems weighing `4` and `3` (total weight 7, value `40 + 50 = 90`). Adding any other gem would exceed weight 10, and every other selection that fits is worth less.

---

## 🔹 Practise & Judge

1. Write your solution as a stdin → stdout program, e.g. `my_m9q3.py`.
2. Judge it: `python tools/judge/judge.py M9Q3 my_m9q3.py` — sample, random and max-size tests with
   a time limit, scored per test case like the real exam.
3. Only then open the [solution](solutions/Q3_Hard_Gem_Splitter.md).
