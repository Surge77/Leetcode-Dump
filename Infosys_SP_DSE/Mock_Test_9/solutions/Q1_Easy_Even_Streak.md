# 🔹 Solution — Mock 9 · Q1: Even Streak (Sliding Window, Easy)

**Problem statement:** [Q1_Easy_Even_Streak.md](../Q1_Easy_Even_Streak.md) · judge your own code first with `python tools/judge/judge.py M9Q1 <your_file>.py`

## 🔹 Quick Breakdown

* **Difficulty Level:** Easy (Q1 slot)
* **Main Approach:** Longest window with **at most `K` odd** numbers. Grow the right end; whenever the window holds more than `K` odds, move the left end forward until it is valid again. Track the best length.
* **Core Concept:** variable-size sliding window with a monotone condition
* **When to Use This Pattern?** "Longest subarray with at most K bad elements / K distinct / sum ≤ S (non-negative values)".
* **Mistakes to Avoid:**
  * Restarting from scratch after each violation (O(N²)).
  * Forgetting `K = 0`: the window may be empty when the current number is odd.

## 🔹 Optimization Path

* **Brute Force:** every start, extend while valid — O(N²).
* **Optimized Solution:** two pointers — O(N).

## 🔹 Solution Breakdown

* **Optimal Approach:** `odd += a[r] & 1`; `while odd > K: odd -= a[l] & 1; l += 1`; `best = max(best, r − l + 1)`.
* **Why This Works?** Validity is monotone: shrinking a valid window keeps it valid, and if `[l, r]` is invalid so is `[l, r']` for every `r' > r`. So the left end never needs to move back.
* **Edge Cases Considered:**
  * All numbers odd and `K = 0` → 0.
  * `K ≥` number of odds → `N`.

## 🔹 Pattern Recognition

* **Belongs To:** Sliding Window
* **Common Problems Using This:**
  * 1004. Max Consecutive Ones III
  * [424. Longest Repeating Character Replacement](../../../Sliding_Window/424.Longest_Repeating_Character_Replacement.md)
  * [209. Minimum Size Subarray Sum](../../../Sliding_Window/209.Minimum_size_subarray_sum.md)

## 🔹 Tricks & Patterns Used

* **Parity with `x & 1`.**

## 🔹 Alternative Data Structures

* Positions of odd numbers in a list: the answer is the max gap spanning `K + 1` consecutive odd positions — same O(N).

## 🔹 Complexity Analysis

* **Time Complexity:** O(N)
* **Space Complexity:** O(1) extra

## 🔹 Code Snippet (Brute Force — partial score)

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    a = [int(x) for x in data[2:2 + n]]
    best = 0
    for left in range(n):
        odd = 0
        for right in range(left, n):
            odd += a[right] & 1
            if odd > k:
                break
            best = max(best, right - left + 1)
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
    a = [int(x) for x in data[2:2 + n]]
    best = left = odd = 0
    for right, x in enumerate(a):
        odd += x & 1
        while odd > k:
            odd -= a[left] & 1
            left += 1
        best = max(best, right - left + 1)
    print(best)


if __name__ == "__main__":
    main()
```
