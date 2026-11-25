# 🔹 Mock 4 · Q1 (Easy): Balanced Segments

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 4, Question 1
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

A sensor log is a binary string `S` of length `N` (`1` = signal, `0` = silence). A contiguous segment is *balanced* if it contains the same number of `0`s and `1`s.

Count the balanced segments.

**Input Format**
* Line 1: integer `N`
* Line 2: binary string `S`

**Output Format**
* One integer — the number of balanced segments.

**Constraints**
* `1 ≤ N ≤ 2·10⁵`

**Sample Input**
```text
6
100110
```

**Sample Output**
```text
7
```

**Explanation:** Map `1 → +1` and `0 → -1`; a segment is balanced exactly when its sum is 0.

---

## 🔹 Practise & Judge

1. Write your solution as a stdin → stdout program, e.g. `my_m4q1.py`.
2. Judge it: `python tools/judge/judge.py M4Q1 my_m4q1.py` — sample, random and max-size tests with
   a time limit, scored per test case like the real exam.
3. Only then open the [solution](solutions/Q1_Easy_Balanced_Segments.md).
