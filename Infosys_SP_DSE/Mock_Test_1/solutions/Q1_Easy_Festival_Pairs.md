# 🔹 Solution — Mock 1 · Q1: Festival Pairs (Hashing / Remainders, Easy)

**Problem statement:** [Q1_Easy_Festival_Pairs.md](../Q1_Easy_Festival_Pairs.md) · judge your own code first with `python tools/judge/judge.py M1Q1 <your_file>.py`

## 🔹 Quick Breakdown

* **Difficulty Level:** Easy (Q1 slot)
* **Main Approach:** Only `A[i] % K` matters. For each box, the partner remainder is `(K - r) % K`; count how many earlier boxes had it with a hashmap.
* **Core Concept:** Hashing + modular remainders ("Two Sum" on remainders)
* **When to Use This Pattern?** Counting pairs whose sum/difference is divisible by K, or whose sum equals a target.
* **Mistakes to Avoid:**
  * O(N²) pair loop — times out at N = 2·10⁵ (that is the partial-score version below).
  * Remainder 0 pairs with remainder 0 — `(K - 0) % K = 0` handles it.
  * An array of size `K` — K can be 10⁹; use a dict.

## 🔹 Optimization Path

* **Brute Force:** O(N²) — check every pair (passes small test cases only).
* **Optimized Solution:** O(N) with a remainder hashmap.
* **Further Improvements Possible?** No.

## 🔹 Solution Breakdown

* **Optimal Approach:** Scan once; `pairs += seen[(K - r) % K]`, then `seen[r] += 1`.
* **Why This Works?** `(a + b) % K == 0` ⇔ `(a % K + b % K) % K == 0` ⇔ `b % K == (K - a % K) % K`. Counting before inserting guarantees `i < j` and no box pairs with itself.
* **Edge Cases Considered:**
  * `K = 1` → every pair is valid: `N(N-1)/2`.
  * `N = 1` → 0.

## 🔹 Pattern Recognition

* **Belongs To:** Hashing / Frequency count
* **Common Problems Using This:**
  * [1. Two Sum](../../../Arrays_and_Hashing/1.Two_Sum.md)
  * 1010. Pairs of Songs With Total Durations Divisible by 60
  * 974. Subarray Sums Divisible by K

## 🔹 Tricks & Patterns Used

* **Modulo Arithmetic:** work with remainders, never with sums.
* **Count-then-insert** for ordered pairs `i < j`.

## 🔹 Alternative Data Structures

* `Counter` of remainders, then combine counts: `C(c0, 2) + Σ c[r]·c[K-r]` — same result, needs care for `r = K/2`.

## 🔹 Complexity Analysis

* **Time Complexity:** O(N)
* **Space Complexity:** O(min(N, K))

## 🔹 Code Snippet (Brute Force — partial score)

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    a = list(map(int, data[2:2 + n]))
    pairs = 0
    for i in range(n):
        for j in range(i + 1, n):
            if (a[i] + a[j]) % k == 0:
                pairs += 1
    print(pairs)


if __name__ == "__main__":
    main()
```

## 🔹 Code Snippet (Optimized)

```python
import sys
from collections import defaultdict


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    seen = defaultdict(int)  # remainder -> boxes seen so far with that remainder
    pairs = 0
    for token in data[2:2 + n]:
        r = int(token) % k
        pairs += seen[(k - r) % k]  # partner remainder makes the sum divisible by k
        seen[r] += 1
    print(pairs)


if __name__ == "__main__":
    main()
```
