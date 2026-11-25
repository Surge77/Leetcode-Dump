# 🔹 Solution — Mock 1 · Q2: Lucky Subsets (DP over Remainders, Medium)

**Problem statement:** [Q2_Medium_Lucky_Subsets.md](../Q2_Medium_Lucky_Subsets.md) · judge your own code first with `python tools/judge/judge.py M1Q2 <your_file>.py`

## 🔹 Quick Breakdown

* **Difficulty Level:** Medium (Q2 slot)
* **Main Approach:** Only sums **mod M** matter. `dp[r]` = number of subsets (including the empty one) of the coupons seen so far with sum `≡ r (mod M)`. Each coupon is either skipped (`dp[r]`) or taken (`dp[r - x]`).
* **Core Concept:** 0/1 knapsack over remainders + modulo counting
* **When to Use This Pattern?** "Count subsets/subsequences whose sum is divisible by M" with `N · M ≤ ~10⁷`.
* **Mistakes to Avoid:**
  * Enumerating subsets — 2¹⁰⁰⁰.
  * Updating `dp` in place — a coupon would be used twice. Build a new array per coupon.
  * Forgetting to subtract the empty set (and to keep the result non-negative mod p).

## 🔹 Optimization Path

* **Brute Force:** O(2ᴺ · N) — every subset (partial score for N ≤ 20).
* **Optimized Solution:** O(N · M).
* **Further Improvements Possible?** Pigeonhole tricks only answer "does one exist?", not "how many".

## 🔹 Solution Breakdown

* **Optimal Approach:** Start `dp = [1, 0, …, 0]` (empty set). For each `x` (reduced mod M): `new[r] = dp[r] + dp[(r - x) % M]`. Answer `dp[0] - 1`.
* **Why This Works?** Every subset of the first `i` coupons either excludes coupon `i` (remainder unchanged) or includes it (remainder shifted by `x`); these cases are disjoint and cover everything.
* **Edge Cases Considered:**
  * `M = 1` → every non-empty set: `2ᴺ - 1`.
  * Values that are multiples of `M` (each doubles the count).
  * Zeros in `A`.

## 🔹 Pattern Recognition

* **Belongs To:** DP — 0/1 Knapsack (counting, mod)
* **Common Problems Using This:**
  * 494. Target Sum (in this repo)
  * 1155. Number of Dice Rolls With Target Sum (in this repo)
  * 1262. Greatest Sum Divisible by Three

## 🔹 Tricks & Patterns Used

* **Remainder state space** replaces huge sums.
* **Python negative indexing:** `dp[r - x]` with `r - x < 0` reads `dp[M + r - x]`, i.e. `dp[(r - x) % M]`.

## 🔹 Alternative Data Structures

* 2D table `dp[i][r]` — same recurrence, more memory, easier to explain.

## 🔹 Complexity Analysis

* **Time Complexity:** O(N · M)
* **Space Complexity:** O(M)

## 🔹 Code Snippet (Brute Force — partial score)

```python
import sys

MOD = 10**9 + 7


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    a = list(map(int, data[2:2 + n]))
    lucky = 0
    for mask in range(1, 1 << n):  # every non-empty subset (only for small n)
        total = sum(a[i] for i in range(n) if mask >> i & 1)
        if total % m == 0:
            lucky += 1
    print(lucky % MOD)


if __name__ == "__main__":
    main()
```

## 🔹 Code Snippet (Optimized)

```python
import sys

MOD = 10**9 + 7


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    dp = [0] * m  # dp[r]: subsets (incl. empty) with sum % m == r
    dp[0] = 1
    for token in data[2:2 + n]:
        x = int(token) % m
        # skip the coupon -> dp[r]; take it -> remainder came from r - x
        dp = [(dp[r] + dp[r - x]) % MOD for r in range(m)]
    print((dp[0] - 1) % MOD)  # drop the empty set


if __name__ == "__main__":
    main()
```
