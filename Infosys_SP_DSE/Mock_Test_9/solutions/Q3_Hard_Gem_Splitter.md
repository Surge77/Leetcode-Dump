# 🔹 Solution — Mock 9 · Q3: Gem Splitter (Meet in the Middle Knapsack, Hard)

**Problem statement:** [Q3_Hard_Gem_Splitter.md](../Q3_Hard_Gem_Splitter.md) · judge your own code first with `python tools/judge/judge.py M9Q3 <your_file>.py`

## 🔹 Quick Breakdown

* **Difficulty Level:** Hard (Q3 slot)
* **Main Approach:** A 0/1 knapsack whose capacity is up to 10¹⁵ — the usual `dp[capacity]` table is impossible. But `N ≤ 36`, so **meet in the middle**: list all `2^(N/2)` (weight, value) subsets of each half. Sort the right half by weight and take a **running maximum of value**, so `best_right[i]` = best value among right subsets with weight ≤ `weight[i]`. For each left subset that fits, binary-search the heaviest right subset that still fits and add its best value.
* **Core Concept:** meet in the middle + sorted list with prefix maxima ("best value within a weight budget")
* **When to Use This Pattern?** Knapsack / subset selection with `N ≈ 30–40` and huge weights or values.
* **Mistakes to Avoid:**
  * Binary-searching for the right subset with the largest weight **without** the prefix max: a lighter subset can be worth more.
  * Forgetting the empty subset on either side (value 0).

## 🔹 Optimization Path

* **Brute Force:** all `2ᴺ` subsets — O(2ᴺ · N), only for `N ≤ 20`.
* **Optimized Solution:** O(2^(N/2) · N).

## 🔹 Solution Breakdown

* **Optimal Approach:** `subsets(half)` by doubling a list of `(weight, value)`; sort the right list; `prefix_best[i] = max(prefix_best[i−1], value[i])`; for every left `(w, v)` with `w ≤ W`: `i = bisect_right(right_weights, W − w) − 1`, answer `max(v + prefix_best[i])`.
* **Why This Works?** Every selection is a left part plus a right part; for a fixed left part the best right part is the most valuable one within the remaining capacity, which is exactly `prefix_best` at the last weight ≤ `W − w`.
* **Edge Cases Considered:**
  * No gem fits → 0 (both empty subsets).
  * Every gem fits → total value.

## 🔹 Pattern Recognition

* **Belongs To:** Meet in the Middle
* **Common Problems Using This:**
  * [1755. Closest Subsequence Sum](../../../Divide_and_Conquer/1755.Closest_Subsequence_Sum.md)
  * [2035. Partition Array Into Two Arrays to Minimize Sum Difference](../../../Divide_and_Conquer/2035.Partition_Array_Into_Two_Arrays_to_Minimize_Sum_Difference.md)
  * 416. Partition Equal Subset Sum (in this repo — small-sum DP version)

## 🔹 Tricks & Patterns Used

* **Subset enumeration by doubling.**
* **Sort by weight + prefix max of value** = "best value with weight ≤ x" in O(log) per query.

## 🔹 Alternative Data Structures

* Keep only the Pareto front of the right half (drop subsets that are heavier **and** less valuable) — same answers, smaller list.

## 🔹 Complexity Analysis

* **Time Complexity:** O(2^(N/2) · N)
* **Space Complexity:** O(2^(N/2))

## 🔹 Code Snippet (Brute Force — partial score)

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, cap = int(data[0]), int(data[1])
    gems = [(int(data[2 + 2 * i]), int(data[3 + 2 * i])) for i in range(n)]
    best = 0
    for mask in range(1 << n):
        weight = value = 0
        for i, (w, v) in enumerate(gems):
            if mask >> i & 1:
                weight, value = weight + w, value + v
        if weight <= cap:
            best = max(best, value)
    print(best)


if __name__ == "__main__":
    main()
```

## 🔹 Code Snippet (Optimized)

```python
import sys
from bisect import bisect_right


def subsets(gems):
    """All (weight, value) sums of subsets of `gems`, including the empty one."""
    out = [(0, 0)]
    for w, v in gems:
        out += [(sw + w, sv + v) for sw, sv in out]
    return out


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, cap = int(data[0]), int(data[1])
    gems = [(int(data[2 + 2 * i]), int(data[3 + 2 * i])) for i in range(n)]
    left, right = subsets(gems[: n // 2]), sorted(subsets(gems[n // 2:]))

    right_weights = [w for w, _ in right]
    prefix_best, running = [], 0
    for _, v in right:  # best value among right subsets no heavier than this one
        running = max(running, v)
        prefix_best.append(running)

    best = 0
    for w, v in left:
        if w <= cap:
            i = bisect_right(right_weights, cap - w) - 1  # i >= 0: the empty subset weighs 0
            best = max(best, v + prefix_best[i])
    print(best)


if __name__ == "__main__":
    main()
```
