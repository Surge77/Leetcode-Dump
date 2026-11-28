# 🔹 Solution — Mock 9 · Q2: Exam Hall (Binary Search on Answer, Medium)

**Problem statement:** [Q2_Medium_Exam_Hall.md](../Q2_Medium_Exam_Hall.md) · judge your own code first with `python tools/judge/judge.py M9Q2 <your_file>.py`

## 🔹 Quick Breakdown

* **Difficulty Level:** Medium (Q2 slot)
* **Main Approach:** "Maximise the minimum gap" → **binary search on the gap `D`**. For a fixed `D`, greedily seat a student at the first seat, then at the next seat at least `D` further, and so on; `D` is feasible iff at least `K` students fit. Feasibility is monotone in `D`, so binary-search the largest feasible `D`.
* **Core Concept:** binary search on the answer + greedy check
* **When to Use This Pattern?** "Maximise the minimum …" / "minimise the maximum …" with a cheap yes/no test for a candidate value.
* **Mistakes to Avoid:**
  * Forgetting to sort the seat positions.
  * An infinite loop in the binary search: with `lo = mid` use `mid = (lo + hi + 1) // 2`.

## 🔹 Optimization Path

* **Brute Force:** try every choice of `K` seats — O(C(N, K) · K).
* **Optimized Solution:** O(N log N) sort + O(N log X) search, `X = 10⁹`.

## 🔹 Solution Breakdown

* **Optimal Approach:** `lo = 0` (always feasible), `hi = (max − min) // (K − 1)` (no gap can exceed this). While `lo < hi`: `mid = (lo + hi + 1) // 2`; if `fits(mid)` then `lo = mid` else `hi = mid − 1`.
* **Why This Works?** Greedy is optimal for the check: taking the leftmost possible seat each time leaves the most room for the rest (any valid seating can be shifted left to the greedy one without breaking a gap).
* **Edge Cases Considered:**
  * `K = N` → the smallest adjacent gap.
  * `K = 2` → `max − min`.

## 🔹 Pattern Recognition

* **Belongs To:** Modified Binary Search — binary search on the answer
* **Common Problems Using This:**
  * 1552. Magnetic Force Between Two Balls
  * [875. Koko Eating Bananas](../../../Binary_Search/875.Koko_Eating_Bananas.md)
  * [410. Split Array Largest Sum](../../../Binary_Search/410.Split_Array_Largest_Sum.md)

## 🔹 Tricks & Patterns Used

* **Upper-mid** `(lo + hi + 1) // 2` when the update is `lo = mid`.
* **Tight initial bound** `(max − min) // (K − 1)`.

## 🔹 Alternative Data Structures

* None needed; `bisect` can jump to the next seat (`bisect_left(pos, last + D)`) making each check O(K log N) instead of O(N).

## 🔹 Complexity Analysis

* **Time Complexity:** O(N log N + N log X)
* **Space Complexity:** O(N)

## 🔹 Code Snippet (Brute Force — partial score)

```python
import sys
from itertools import combinations


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    seats = sorted(int(x) for x in data[2:2 + n])
    best = 0
    for chosen in combinations(seats, k):  # already sorted
        best = max(best, min(b - a for a, b in zip(chosen, chosen[1:])))
    print(best)


if __name__ == "__main__":
    main()
```

## 🔹 Code Snippet (Optimized)

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    seats = sorted(int(x) for x in data[2:2 + n])

    def fits(gap: int) -> bool:
        placed, last = 1, seats[0]
        for s in seats[1:]:
            if s - last >= gap:
                placed, last = placed + 1, s
                if placed == k:
                    return True
        return placed >= k

    lo, hi = 0, (seats[-1] - seats[0]) // (k - 1)
    while lo < hi:
        mid = (lo + hi + 1) // 2  # upper mid: lo = mid must make progress
        if fits(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)


if __name__ == "__main__":
    main()
```
