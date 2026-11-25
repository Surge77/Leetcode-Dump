# 🔹 Solution — Mock 3 · Q3: Smooth Numbers (Digit DP, Hard)

**Problem statement:** [Q3_Hard_Smooth_Numbers.md](../Q3_Hard_Smooth_Numbers.md) · judge your own code first with `python tools/judge/judge.py M3Q3 <your_file>.py`

## 🔹 Quick Breakdown

* **Difficulty Level:** Hard (Q3 slot)
* **Main Approach:** `answer = f(R) - f(L - 1)`, where `f(n)` counts smooth numbers in `[1, n]` with a digit DP. State: `(position, digit-sum mod D, previous digit, tight, started)`.
* **Core Concept:** Digit DP with extra state + modulo
* **When to Use This Pattern?** Counting numbers up to 10¹⁸ with digit-level rules (sums, adjacency, forbidden digits, divisibility).
* **Mistakes to Avoid:**
  * Iterating over the range — up to 10¹⁸ numbers.
  * Treating leading zeros as real digits — `0012` would wrongly fail "adjacent equal" on `00`. The `started` flag fixes this.
  * Negative result after `f(R) - f(L-1)` under the modulus — apply `% MOD` again.

## 🔹 Optimization Path

* **Brute Force:** Check every number in `[L, R]` — O((R - L) · 18) (partial score for small ranges).
* **Optimized Solution:** O(19 · D · 11 · 2 · 2 · 10) per call — under a million transitions.
* **Further Improvements Possible?** Iterative tabulation is faster, but the memoised version is easier to get right in the exam.

## 🔹 Solution Breakdown

* **Optimal Approach:** `go(pos, rem, prev, tight, started)` tries every digit `≤ limit`; skips `dig == prev` once started; leading zeros keep `started = False` and do not touch `rem`/`prev`. At the end count 1 if `started and rem == 0`.
* **Why This Works?** Each number `≤ n` is one path through the digits; the future only depends on the five state values, so memoisation counts each state's completions once.
* **Edge Cases Considered:**
  * `L = 1` → `f(0) = 0`.
  * `D = 1` → only the adjacency rule matters.
  * Single-digit numbers (always satisfy rule 1).

## 🔹 Pattern Recognition

* **Belongs To:** DP — Digit DP
* **Common Problems Using This:**
  * 233. Number of Digit One (in this repo)
  * 902. Numbers At Most N Given Digit Set (in this repo)
  * 2719. Count of Integers

## 🔹 Tricks & Patterns Used

* **Range by subtraction:** `f(R) - f(L - 1)`.
* **`started` flag** for leading zeros; **`prev = -1`** before the first real digit.
* **Modulo Arithmetic** inside the DP.

## 🔹 Alternative Data Structures

* Bottom-up table over positions with dictionaries of states — same complexity, no recursion.

## 🔹 Complexity Analysis

* **Time Complexity:** O(19 · D · 11 · 4 · 10)
* **Space Complexity:** O(19 · D · 11 · 4)

## 🔹 Code Snippet (Brute Force — partial score)

```python
import sys

MOD = 10**9 + 7


def smooth(x: int, d: int) -> bool:
    s = str(x)
    no_equal_neighbours = all(a != b for a, b in zip(s, s[1:]))
    return no_equal_neighbours and sum(map(int, s)) % d == 0


def main() -> None:
    l, r, d = map(int, sys.stdin.read().split())
    print(sum(1 for x in range(l, r + 1) if smooth(x, d)) % MOD)


if __name__ == "__main__":
    main()
```

## 🔹 Code Snippet (Optimized)

```python
import sys
from functools import lru_cache

MOD = 10**9 + 7


def count_upto(n: int, d: int) -> int:
    """Smooth numbers in [1, n], modulo MOD."""
    if n <= 0:
        return 0
    digits = list(map(int, str(n)))
    length = len(digits)

    @lru_cache(maxsize=None)
    def go(pos: int, rem: int, prev: int, tight: bool, started: bool) -> int:
        if pos == length:
            return 1 if started and rem == 0 else 0
        limit = digits[pos] if tight else 9
        total = 0
        for dig in range(limit + 1):
            if started and dig == prev:
                continue  # equal adjacent digits
            now_started = started or dig != 0
            total += go(pos + 1,
                        (rem + dig) % d if now_started else 0,
                        dig if now_started else -1,
                        tight and dig == limit,
                        now_started)
        return total % MOD

    return go(0, 0, -1, True, False)


def main() -> None:
    l, r, d = map(int, sys.stdin.read().split())
    print((count_upto(r, d) - count_upto(l - 1, d)) % MOD)


if __name__ == "__main__":
    main()
```
