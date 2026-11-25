# 🔹 Solution — Mock 3 · Q1: Special Numbers (Number Theory — Sieve, Easy)

**Problem statement:** [Q1_Easy_Special_Numbers.md](../Q1_Easy_Special_Numbers.md) · judge your own code first with `python tools/judge/judge.py M3Q1 <your_file>.py`

## 🔹 Quick Breakdown

* **Difficulty Level:** Easy (Q1 slot)
* **Main Approach:** `d(n) = Π (eᵢ + 1)` equals 3 only when `n = p²` for a prime `p`. So the answer is the number of primes `≤ √N`. Sieve once up to `√(max N) ≤ 10⁶`, keep prefix counts, answer each query in O(1).
* **Core Concept:** Divisor-count formula + Sieve of Eratosthenes + prefix sums
* **When to Use This Pattern?** Properties defined by divisors (exactly k divisors, perfect numbers) — reduce them to prime structure first.
* **Mistakes to Avoid:**
  * Counting divisors of every number up to 10¹² — impossible.
  * `int(N ** 0.5)` floating-point errors near perfect squares — use `math.isqrt`.
  * Re-sieving for every query — sieve once.

## 🔹 Optimization Path

* **Brute Force:** Count divisors of each number up to `N` — O(N√N) per query (partial score for tiny N).
* **Optimized Solution:** O(√max N · log log) sieve + O(1) per query.
* **Further Improvements Possible?** No.

## 🔹 Solution Breakdown

* **Optimal Approach:** `top = isqrt(max(N))`; sieve to `top`; `prime_count[i]` = primes `≤ i`; answer `prime_count[isqrt(N)]`.
* **Why This Works?** If `n = p₁^e₁ ⋯ p_k^e_k`, then `d(n) = (e₁+1)⋯(e_k+1)`. Since 3 is prime, the product is 3 only with a single prime and `e = 2`. And `p² ≤ N` ⇔ `p ≤ √N`.
* **Edge Cases Considered:**
  * `N < 4` → 0.
  * `N` a perfect square of a prime (inclusive).

## 🔹 Pattern Recognition

* **Belongs To:** Math — Number Theory
* **Common Problems Using This:**
  * 204. Count Primes (in this repo)
  * 1952. Three Divisors
  * 2521. Distinct Prime Factors of Product of Array (in this repo)

## 🔹 Tricks & Patterns Used

* **Divisor function** from the prime factorisation.
* **Offline max:** sieve only up to `√(largest query)`.
* **`itertools.accumulate`** for prefix counts.

## 🔹 Alternative Data Structures

* Store the sorted list of primes and use `bisect_right(primes, isqrt(N))`.

## 🔹 Complexity Analysis

* **Time Complexity:** O(√M log log M + T), M = max N
* **Space Complexity:** O(√M)

## 🔹 Code Snippet (Brute Force — partial score)

```python
import sys


def divisor_count(x: int) -> int:
    count, d = 0, 1
    while d * d <= x:
        if x % d == 0:
            count += 1 if d * d == x else 2
        d += 1
    return count


def main() -> None:
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    for token in data[1:1 + t]:
        n = int(token)
        out.append(sum(1 for x in range(1, n + 1) if divisor_count(x) == 3))
    print("\n".join(map(str, out)))


if __name__ == "__main__":
    main()
```

## 🔹 Code Snippet (Optimized)

```python
import sys
from itertools import accumulate
from math import isqrt


def main() -> None:
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    queries = [int(x) for x in data[1:1 + t]]
    top = max(1, isqrt(max(queries)))
    sieve = bytearray([1]) * (top + 1)  # sieve[x] == 1 => x is prime
    sieve[0] = sieve[1] = 0
    for p in range(2, isqrt(top) + 1):
        if sieve[p]:
            sieve[p * p::p] = bytes(len(range(p * p, top + 1, p)))
    prime_count = list(accumulate(sieve))  # primes <= i
    print("\n".join(str(prime_count[isqrt(n)]) for n in queries))  # special = p^2


if __name__ == "__main__":
    main()
```
