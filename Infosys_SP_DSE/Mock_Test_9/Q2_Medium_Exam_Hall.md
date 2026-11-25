# 🔹 Mock 9 · Q2 (Medium): Exam Hall

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 9, Question 2
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

An exam hall has `N` desks in a single long row; desk `i` stands at position `X[i]` metres from the door (all positions are different). `K` students must be seated at `K` different desks. To discourage copying, the invigilator wants the **closest pair** of seated students to be as far apart as possible.

Print the largest possible distance between the two closest seated students.

**Input Format**
* Line 1: two integers `N` and `K`
* Line 2: `N` distinct integers `X[1..N]` (not necessarily sorted)

**Output Format**
* One integer — the maximum achievable minimum distance.

**Constraints**
* `2 ≤ K ≤ N ≤ 2·10⁵`
* `1 ≤ X[i] ≤ 10⁹`

**Sample Input**
```text
5 3
1 2 8 4 9
```

**Sample Output**
```text
3
```

**Explanation:** Seating at `1, 4, 8` gives gaps `3` and `4`, so the closest pair is 3 apart. A minimum gap of 4 is impossible: after `1` the next desk at least 4 away is `8`, and nothing is at `12` or beyond.

---

## 🔹 Practise & Judge

1. Write your solution as a stdin → stdout program, e.g. `my_m9q2.py`.
2. Judge it: `python tools/judge/judge.py M9Q2 my_m9q2.py` — sample, random and max-size tests with
   a time limit, scored per test case like the real exam.
3. Only then open the [solution](solutions/Q2_Medium_Exam_Hall.md).
