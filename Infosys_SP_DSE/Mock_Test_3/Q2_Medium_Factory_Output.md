# 🔹 Mock 3 · Q2 (Medium): Factory Output

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 3, Question 2
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

A factory has `K` machines that all start at time `0`. Machine `i` first needs `W[i]` minutes to warm up, then produces one item every `P[i]` minutes. So by time `T` it has produced `⌊(T - W[i]) / P[i]⌋` items if `T ≥ W[i]`, and `0` otherwise.

Find the minimum time `T` at which the machines together have produced **at least `X`** items.

**Input Format**
* Line 1: two integers `K` and `X`
* Next `K` lines: two integers `W[i] P[i]`

**Output Format**
* One integer — the minimum time `T`.

**Constraints**
* `1 ≤ K ≤ 10⁵`
* `1 ≤ X ≤ 10⁹`
* `0 ≤ W[i] ≤ 10⁹`, `1 ≤ P[i] ≤ 10⁹`

**Sample Input**
```text
3 10
0 3
5 2
20 1
```

**Sample Output**
```text
15
```

**Explanation:** At `T = 15`: machine 1 made `15 // 3 = 5`, machine 2 made `(15 - 5) // 2 = 5`, machine 3 is still warming up → 10 items. At `T = 14` the total is only `4 + 4 = 8`.

---

## 🔹 Practise & Judge

1. Write your solution as a stdin → stdout program, e.g. `my_m3q2.py`.
2. Judge it: `python tools/judge/judge.py M3Q2 my_m3q2.py` — sample, random and max-size tests with
   a time limit, scored per test case like the real exam.
3. Only then open the [solution](solutions/Q2_Medium_Factory_Output.md).
