# 🔹 Mock 3 · Q3 (Hard): Smooth Numbers

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 3, Question 3
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

An integer is *smooth* if:
1. no two **adjacent** digits are equal (e.g., `1213` is fine, `1223` is not), and
2. the **sum of its digits is divisible by `D`**.

Given `L`, `R` and `D`, count the smooth integers in `[L, R]`. Print the answer modulo `10⁹ + 7`.

**Input Format**
* One line: three integers `L R D`

**Output Format**
* One integer — the count modulo `10⁹ + 7`.

**Constraints**
* `1 ≤ L ≤ R ≤ 10¹⁸`
* `1 ≤ D ≤ 100`

**Sample Input**
```text
1 100 3
```

**Sample Output**
```text
30
```

**Explanation:** `3, 6, 9` qualify, as do two-digit numbers like `12, 21, 30` — but not `33` or `66` (equal adjacent digits).

---

## 🔹 Practise & Judge

1. Write your solution as a stdin → stdout program, e.g. `my_m3q3.py`.
2. Judge it: `python tools/judge/judge.py M3Q3 my_m3q3.py` — sample, random and max-size tests with
   a time limit, scored per test case like the real exam.
3. Only then open the [solution](solutions/Q3_Hard_Smooth_Numbers.md).
