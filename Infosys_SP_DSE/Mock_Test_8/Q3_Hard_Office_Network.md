# 🔹 Mock 8 · Q3 (Hard): Office Network

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 8, Question 3
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

A company has `N` offices connected by `N − 1` roads so that every office can reach every other one (the network is a tree). Road `i` joins offices `u` and `v` and is `w` kilometres long. Office `j` has `P[j]` employees.

The company will hold an all-hands meeting at **one** office. Its *travel cost* is the sum, over all employees, of the distance they travel: `Σ P[j] · dist(j, meeting office)`.

Print the minimum travel cost and the office that achieves it. If several offices tie, print the smallest office number.

**Input Format**
* Line 1: an integer `N`
* Line 2: `N` integers `P[1..N]`
* Next `N − 1` lines: three integers `u v w`

**Output Format**
* Two integers: the minimum travel cost and the chosen office.

**Constraints**
* `1 ≤ N ≤ 2·10⁵`
* `0 ≤ P[j] ≤ 1000`
* `1 ≤ w ≤ 1000`

**Sample Input**
```text
5
4 1 0 2 3
1 2 3
1 3 1
3 4 2
3 5 5
```

**Sample Output**
```text
27 1
```

**Explanation:** Meeting at office 1 costs `4·0 + 1·3 + 0·1 + 2·3 + 3·6 = 27`. Office 3 would cost `4·1 + 1·4 + 0 + 2·2 + 3·5 = 27` too, and the tie goes to the smaller number, 1. Every other office costs more.

---

## 🔹 Practise & Judge

1. Write your solution as a stdin → stdout program, e.g. `my_m8q3.py`.
2. Judge it: `python tools/judge/judge.py M8Q3 my_m8q3.py` — sample, random and max-size tests with
   a time limit, scored per test case like the real exam.
3. Only then open the [solution](solutions/Q3_Hard_Office_Network.md).
