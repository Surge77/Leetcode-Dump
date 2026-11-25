# 🔹 Mock 7 · Q1 (Easy): Signal Boost

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 7, Question 1
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

A street has `N` lamps numbered `1..N`, all starting at brightness 0. The city runs `M` boosts; boost `i` adds `v` to the brightness of every lamp from `l` to `r` (inclusive).

After all boosts, print the maximum brightness on the street and how many lamps have exactly that brightness.

**Input Format**
* Line 1: two integers `N` and `M`
* Next `M` lines: three integers `l r v`

**Output Format**
* Two integers: the maximum brightness and the number of lamps that reach it.

**Constraints**
* `1 ≤ N, M ≤ 2·10⁵`
* `1 ≤ l ≤ r ≤ N`
* `1 ≤ v ≤ 10⁹`

**Sample Input**
```text
5 3
1 3 2
2 5 1
3 4 4
```

**Sample Output**
```text
7 1
```

**Explanation:** Final brightness of lamps 1..5 is `2 3 7 5 1`; only lamp 3 reaches 7.

---

## 🔹 Practise & Judge

1. Write your solution as a stdin → stdout program, e.g. `my_m7q1.py`.
2. Judge it: `python tools/judge/judge.py M7Q1 my_m7q1.py` — sample, random and max-size tests with
   a time limit, scored per test case like the real exam.
3. Only then open the [solution](solutions/Q1_Easy_Signal_Boost.md).
