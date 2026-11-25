# 🔹 Mock 1 · Q1 (Easy): Festival Pairs

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 1, Question 1
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

A shop packs festival hampers. There are `N` gift boxes; box `i` weighs `A[i]` grams. Two **different** boxes can be paired into one hamper only if their total weight is divisible by `K`.

Count the number of valid pairs `(i, j)` with `i < j`.

**Input Format**
* Line 1: two integers `N` and `K`
* Line 2: `N` integers `A[1..N]`

**Output Format**
* One integer — the number of valid pairs.

**Constraints**
* `1 ≤ N ≤ 2·10⁵`
* `1 ≤ K ≤ 10⁹`
* `1 ≤ A[i] ≤ 10⁹`

**Sample Input**
```text
6 4
2 2 1 7 5 3
```

**Sample Output**
```text
5
```

**Explanation:** Remainders mod 4 are `2 2 1 3 1 3`. The two `2`s form 1 pair; each of the two `1`s pairs with each of the two `3`s, giving 4 more — 5 in total.

---

## 🔹 Practise & Judge

1. Write your solution as a stdin → stdout program, e.g. `my_m1q1.py`.
2. Judge it: `python tools/judge/judge.py M1Q1 my_m1q1.py` — sample, random and max-size tests with
   a time limit, scored per test case like the real exam.
3. Only then open the [solution](solutions/Q1_Easy_Festival_Pairs.md).
