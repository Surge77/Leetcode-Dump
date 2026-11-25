# 🔹 Mock 8 · Q1 (Easy): Ferry Seats

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 8, Question 1
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

`N` passengers wait at a river crossing; passenger `i` weighs `W[i]`. Every ferry trip uses a fresh boat that carries **at most two** passengers whose total weight is **at most `C`**.

Print the minimum number of boats needed to carry everyone across.

**Input Format**
* Line 1: two integers `N` and `C`
* Line 2: `N` integers `W[1..N]`

**Output Format**
* One integer — the minimum number of boats.

**Constraints**
* `1 ≤ N ≤ 2·10⁵`
* `1 ≤ W[i] ≤ C ≤ 10⁹`

**Sample Input**
```text
5 10
7 2 5 8 3
```

**Sample Output**
```text
3
```

**Explanation:** Boats `{8, 2}`, `{7, 3}` and `{5}`. Two boats cannot carry five people.

---

## 🔹 Practise & Judge

1. Write your solution as a stdin → stdout program, e.g. `my_m8q1.py`.
2. Judge it: `python tools/judge/judge.py M8Q1 my_m8q1.py` — sample, random and max-size tests with
   a time limit, scored per test case like the real exam.
3. Only then open the [solution](solutions/Q1_Easy_Ferry_Seats.md).
