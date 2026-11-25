# 🔹 Problem Name: Factory Output (Binary Search on Answer, Medium)

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

## 🔹 Quick Breakdown

* **Difficulty Level:** Medium (Q2 slot)
* **Main Approach:** `items(T)` never decreases as `T` grows, so binary search the smallest `T` with `items(T) ≥ X`. Upper bound: the best single machine alone, `min(W[i] + P[i]·X)`.
* **Core Concept:** Binary search on the answer + monotone feasibility check
* **When to Use This Pattern?** "Minimum time / capacity / speed so that a total reaches a target" where the total is easy to compute for a fixed guess.
* **Mistakes to Avoid:**
  * Simulating minute by minute — answers reach 10¹⁸.
  * Negative counts for `T < W[i]` — `(T - W) // P` is negative in Python; skip those machines.
  * Upper bound too small (must be feasible) or summing to huge totals without an early exit.

## 🔹 Optimization Path

* **Brute Force:** Try `T = 0, 1, 2, …` — O(answer · K) (partial score for tiny answers).
* **Optimized Solution:** O(K · log(answer)) ≈ 60 · K operations.
* **Further Improvements Possible?** Sort machines by `W` to stop the check early.

## 🔹 Solution Breakdown

* **Optimal Approach:** `lo = 0`, `hi = min(W[i] + P[i]·X)`; standard "first true" binary search; inside the check, stop adding once the total reaches `X`.
* **Why This Works?** Each machine's count is non-decreasing in `T`, so their sum is too; therefore all feasible times form a suffix `[T*, ∞)` and binary search finds `T*`.
* **Edge Cases Considered:**
  * One machine.
  * Warm-up longer than the time another machine needs on its own.
  * `W[i] = 0`.

## 🔹 Pattern Recognition

* **Belongs To:** Modified Binary Search — search on answer
* **Common Problems Using This:**
  * 875. Koko Eating Bananas (in this repo)
  * 2187. Minimum Time to Complete Trips
  * 1011. Capacity To Ship Packages Within D Days (in this repo)

## 🔹 Tricks & Patterns Used

* **Early exit** in the feasibility check keeps it fast and the numbers small.
* **Feasible upper bound** from a single machine.

## 🔹 Alternative Data Structures

* None needed.

## 🔹 Complexity Analysis

* **Time Complexity:** O(K · log(min(W + P·X)))
* **Space Complexity:** O(K)

## 🔹 Code Snippet (Brute Force — partial score)

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    k, x = int(data[0]), int(data[1])
    machines = [(int(data[2 + 2 * i]), int(data[3 + 2 * i])) for i in range(k)]
    t = 0
    while sum((t - w) // p for w, p in machines if t >= w) < x:
        t += 1  # only for tiny answers
    print(t)


if __name__ == "__main__":
    main()
```

## 🔹 Code Snippet (Optimized)

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    k, x = int(data[0]), int(data[1])
    machines = [(int(data[2 + 2 * i]), int(data[3 + 2 * i])) for i in range(k)]

    def enough(t: int) -> bool:
        total = 0
        for w, p in machines:
            if t >= w:
                total += (t - w) // p
                if total >= x:
                    return True  # early exit
        return False

    lo = 0
    hi = min(w + p * x for w, p in machines)  # one machine alone reaches x
    while lo < hi:
        mid = (lo + hi) // 2
        if enough(mid):
            hi = mid
        else:
            lo = mid + 1
    print(lo)


if __name__ == "__main__":
    main()
```
