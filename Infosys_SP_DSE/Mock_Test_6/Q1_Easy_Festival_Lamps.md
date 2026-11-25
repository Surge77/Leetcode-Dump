# 🔹 Problem Name: Festival Lamps (Inclusion–Exclusion, Easy)

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 6, Question 1
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

A street has lamps numbered `1..N`. You are given `K` distinct primes `p[1..K]`. Lamp `x` is switched **on** if `x` is divisible by **at least one** of the primes.

Print how many lamps are on.

**Input Format**
* Line 1: two integers `N` and `K`
* Line 2: `K` distinct primes

**Output Format**
* One integer — the number of lamps that are on.

**Constraints**
* `1 ≤ N ≤ 10¹⁸`, `1 ≤ K ≤ 12`, `2 ≤ p[i] ≤ 100`

**Sample Input**
```text
100 2
2 3
```

**Sample Output**
```text
67
```

**Explanation:** `50` multiples of 2, `33` of 3, minus `16` multiples of 6 counted twice.

## 🔹 Quick Breakdown

* **Difficulty Level:** Easy (Q1 slot)
* **Main Approach:** Inclusion–exclusion over all non-empty subsets of the primes: add `N // product` for odd-sized subsets, subtract for even-sized ones.
* **Core Concept:** Inclusion–exclusion principle + bitmask subset enumeration
* **When to Use This Pattern?** "Divisible by at least one of a few numbers" with a huge `N`.
* **Mistakes to Avoid:**
  * Looping to `N = 10¹⁸`.
  * For non-prime divisors you would need the **LCM**, not the product (primes are coprime, so product = LCM here).

## 🔹 Optimization Path

* **Brute Force:** Check every lamp — O(N · K) (partial score for small N).
* **Optimized Solution:** O(2ᴷ · K).
* **Further Improvements Possible?** Skip subsets whose product already exceeds `N` (they contribute 0).

## 🔹 Solution Breakdown

* **Optimal Approach:** For each mask `1..2ᴷ-1`: product of chosen primes; sign `+` if the subset size is odd, `-` if even.
* **Why This Works?** A lamp divisible by exactly `t ≥ 1` of the primes is counted `C(t,1) - C(t,2) + C(t,3) - … = 1` time; lamps divisible by none are never counted.
* **Edge Cases Considered:**
  * `N` smaller than every prime → 0.
  * Products larger than `N`.

## 🔹 Pattern Recognition

* **Belongs To:** Math — Inclusion–Exclusion
* **Common Problems Using This:**
  * 1201. Ugly Number III (in this repo)
  * 878. Nth Magical Number (in this repo)

## 🔹 Tricks & Patterns Used

* **Bitmask enumeration** of subsets; `bin(mask).count("1")` for the size.

## 🔹 Alternative Data Structures

* DFS over primes, pruning branches once the product exceeds `N`.

## 🔹 Complexity Analysis

* **Time Complexity:** O(2ᴷ · K)
* **Space Complexity:** O(K)

## 🔹 Code Snippet (Brute Force — partial score)

```python
import sys


def main() -> None:
    data = sys.stdin.read().split()
    n, k = int(data[0]), int(data[1])
    primes = [int(x) for x in data[2:2 + k]]
    print(sum(1 for x in range(1, n + 1) if any(x % p == 0 for p in primes)))


if __name__ == "__main__":
    main()
```

## 🔹 Code Snippet (Optimized)

```python
import sys


def main() -> None:
    data = sys.stdin.read().split()
    n, k = int(data[0]), int(data[1])
    primes = [int(x) for x in data[2:2 + k]]
    on = 0
    for mask in range(1, 1 << k):
        product = 1
        for i in range(k):
            if mask >> i & 1:
                product *= primes[i]
                if product > n:
                    break
        if product > n:
            continue  # contributes n // product = 0
        sign = 1 if bin(mask).count("1") % 2 else -1
        on += sign * (n // product)
    print(on)


if __name__ == "__main__":
    main()
```
