# 🔹 Mock 4 · Q3 (Hard): Gold Roads

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 4, Question 3
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

A kingdom has `N` cities connected by `M` **one-way** roads. City `i` holds `G[i]` gold. A traveller may start in any city and follow roads as long as they like, visiting cities any number of times. The gold of a city is collected only once.

Print the maximum total gold the traveller can collect.

**Input Format**
* Line 1: two integers `N` and `M`
* Line 2: `N` integers `G[1..N]`
* Next `M` lines: two integers `u v` — a road from `u` to `v`

**Output Format**
* One integer — the maximum gold.

**Constraints**
* `1 ≤ N ≤ 10⁵`, `0 ≤ M ≤ 2·10⁵`
* `1 ≤ G[i] ≤ 10⁹`

**Sample Input**
```text
5 5
1 2 3 4 5
1 2
2 1
2 3
3 4
5 4
```

**Sample Output**
```text
10
```

**Explanation:** Cities 1 and 2 reach each other, so a traveller in either collects both (3 gold), then continues to 3 and 4: `3 + 3 + 4 = 10`. Starting at 5 gives only `5 + 4 = 9`.

---

## 🔹 Practise & Judge

1. Write your solution as a stdin → stdout program, e.g. `my_m4q3.py`.
2. Judge it: `python tools/judge/judge.py M4Q3 my_m4q3.py` — sample, random and max-size tests with
   a time limit, scored per test case like the real exam.
3. Only then open the [solution](solutions/Q3_Hard_Gold_Roads.md).
