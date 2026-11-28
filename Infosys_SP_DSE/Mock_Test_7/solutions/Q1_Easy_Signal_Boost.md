# 🔹 Solution — Mock 7 · Q1: Signal Boost (Difference Array, Easy)

**Problem statement:** [Q1_Easy_Signal_Boost.md](../Q1_Easy_Signal_Boost.md) · judge your own code first with `python tools/judge/judge.py M7Q1 <your_file>.py`

## 🔹 Quick Breakdown

* **Difficulty Level:** Easy (Q1 slot)
* **Main Approach:** Each boost adds `v` to every bulb in `[l, r]`. Record it as `diff[l] += v`, `diff[r + 1] -= v`; one prefix-sum pass gives every bulb's final brightness. Then take the max and count it.
* **Core Concept:** difference array (range add, read once)
* **When to Use This Pattern?** Many range additions, all before the reads.
* **Mistakes to Avoid:**
  * Looping over every bulb of every boost: up to 4·10¹⁰ steps.
  * `diff` of length `N + 1` only — `r + 1` can be `N + 1`; allocate `N + 2`.

## 🔹 Optimization Path

* **Brute Force:** O(N · M).
* **Optimized Solution:** O(N + M).

## 🔹 Solution Breakdown

* **Optimal Approach:** fill `diff`, then a running sum over bulbs `1..N` tracking the best value and its count.
* **Why This Works?** The prefix sum of `diff` at `i` adds `v` for every boost with `l ≤ i` and removes it for every boost with `r < i` — exactly the boosts covering `i`.
* **Edge Cases Considered:**
  * Untouched bulbs stay at 0; since `M ≥ 1` and `v ≥ 1` the maximum is positive, so they never count.
  * One boost over `[1, N]` → every bulb ties, count is `N`.

## 🔹 Pattern Recognition

* **Belongs To:** Prefix Sum — difference array
* **Common Problems Using This:**
  * [1094. Car Pooling](../../../Prefix_Sum/1094.Car_Pooling.md)
  * [2381. Shifting Letters II](../../../Prefix_Sum/2381.Shifting_Letters_II.md)
  * 1109. Corporate Flight Bookings

## 🔹 Tricks & Patterns Used

* **Difference array:** `diff[l] += v; diff[r + 1] -= v`.
* **Fast input:** read all tokens once with `sys.stdin.buffer.read().split()`.

## 🔹 Alternative Data Structures

* A Fenwick tree with range-update/point-query if reads were interleaved with boosts.

## 🔹 Complexity Analysis

* **Time Complexity:** O(N + M)
* **Space Complexity:** O(N)

## 🔹 Code Snippet (Brute Force — partial score)

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    light = [0] * (n + 1)
    for k in range(m):
        l, r, v = (int(x) for x in data[2 + 3 * k: 5 + 3 * k])
        for i in range(l, r + 1):
            light[i] += v
    best = max(light[1:])
    print(best, light[1:].count(best))


if __name__ == "__main__":
    main()
```

## 🔹 Code Snippet (Optimized)

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    diff = [0] * (n + 2)
    for k in range(m):
        l, r, v = int(data[2 + 3 * k]), int(data[3 + 3 * k]), int(data[4 + 3 * k])
        diff[l] += v
        diff[r + 1] -= v
    best, count, level = -1, 0, 0
    for i in range(1, n + 1):
        level += diff[i]
        if level > best:
            best, count = level, 1
        elif level == best:
            count += 1
    print(best, count)


if __name__ == "__main__":
    main()
```
