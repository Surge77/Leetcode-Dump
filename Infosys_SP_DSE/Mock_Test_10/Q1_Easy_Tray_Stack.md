# 🔹 Mock 10 · Q1 (Easy): Tray Stack

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 10, Question 1
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

A canteen keeps a stack of trays. You must process `Q` operations in order:

* `1 x` — put a tray weighing `x` on top of the stack.
* `2` — remove the top tray (do nothing if the stack is empty).
* `3` — report the weight of the **heaviest** tray currently in the stack, or `-1` if it is empty.

**Input Format**
* Line 1: an integer `Q`
* Next `Q` lines: one operation each, as above

**Output Format**
* One line per operation of type `3`, in order.

**Constraints**
* `1 ≤ Q ≤ 2·10⁵`
* `1 ≤ x ≤ 10⁹`

**Sample Input**
```text
8
1 5
1 9
3
2
3
2
2
3
```

**Sample Output**
```text
9
5
-1
```

**Explanation:** The stack is `[5, 9]` at the first query, `[5]` at the second, and empty at the third (the second removal on an empty stack is ignored).

---

## 🔹 Practise & Judge

1. Write your solution as a stdin → stdout program, e.g. `my_m10q1.py`.
2. Judge it: `python tools/judge/judge.py M10Q1 my_m10q1.py` — sample, random and max-size tests with
   a time limit, scored per test case like the real exam.
3. Only then open the [solution](solutions/Q1_Easy_Tray_Stack.md).
