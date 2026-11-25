# 🔹 Solution — Mock 5 · Q2: Price Spread (Sparse Table, Medium)

**Problem statement:** [Q2_Medium_Price_Spread.md](../Q2_Medium_Price_Spread.md) · judge your own code first with `python tools/judge/judge.py M5Q2 <your_file>.py`

## 🔹 Quick Breakdown

* **Difficulty Level:** Medium (Q2 slot)
* **Main Approach:** Static array + many range min/max queries → **sparse table**: `table[j][i]` = max of `P[i .. i + 2ʲ - 1]`. Any range is covered by two overlapping power-of-two blocks, so each query is O(1).
* **Core Concept:** Sparse table (idempotent range queries)
* **When to Use This Pattern?** No updates, many min/max/gcd range queries (operations where overlap does not matter).
* **Mistakes to Avoid:**
  * O(N) per query — 4·10¹⁰ operations.
  * Using a sparse table for **sums** — overlapping blocks double-count; use prefix sums there.

## 🔹 Optimization Path

* **Brute Force:** Scan each range — O(N · Q) (partial score).
* **Segment tree:** O(log N) per query — also passes.
* **Optimized Solution:** O(N log N) build, O(1) per query.

## 🔹 Solution Breakdown

* **Optimal Approach:** `k = (r - l + 1).bit_length() - 1`; `max = max(hi[k][l], hi[k][r - 2ᵏ + 1])`, same for `min`.
* **Why This Works?** The two blocks of length `2ᵏ` (with `2ᵏ ≤ length < 2ᵏ⁺¹`) start at `l` and end at `r`, so together they cover the range exactly (overlap allowed because max/min are idempotent).
* **Edge Cases Considered:**
  * `l == r` → 0.
  * All prices equal → 0.

## 🔹 Pattern Recognition

* **Belongs To:** Range Queries — Sparse Table
* **Common Problems Using This:**
  * 239. Sliding Window Maximum (in this repo — fixed-size windows)
  * 307. Range Sum Query - Mutable (in this repo — when updates exist)
  * LCA via Euler tour + sparse table

## 🔹 Tricks & Patterns Used

* **`bit_length() - 1`** = floor(log₂) without floats.
* **Build level `j` from level `j - 1`** with list comprehensions (fast in Python).

## 🔹 Alternative Data Structures

* Segment tree storing `(min, max)` — needed if prices get updated.

## 🔹 Complexity Analysis

* **Time Complexity:** O(N log N + Q)
* **Space Complexity:** O(N log N)

## 🔹 Code Snippet (Brute Force — partial score)

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, q = int(data[0]), int(data[1])
    p = [int(x) for x in data[2:2 + n]]
    out = []
    pos = 2 + n
    for _ in range(q):
        l, r = int(data[pos]) - 1, int(data[pos + 1])
        pos += 2
        window = p[l:r]
        out.append(max(window) - min(window))
    print("\n".join(map(str, out)))


if __name__ == "__main__":
    main()
```

## 🔹 Code Snippet (Optimized)

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, q = int(data[0]), int(data[1])
    p = [int(x) for x in data[2:2 + n]]

    hi, lo = [p], [p]  # hi[j][i] / lo[j][i]: max / min of p[i .. i + 2^j - 1]
    j = 1
    while (1 << j) <= n:
        half = 1 << (j - 1)
        prev_hi, prev_lo = hi[-1], lo[-1]
        size = n - (1 << j) + 1
        hi.append([max(prev_hi[i], prev_hi[i + half]) for i in range(size)])
        lo.append([min(prev_lo[i], prev_lo[i + half]) for i in range(size)])
        j += 1

    out = []
    pos = 2 + n
    for _ in range(q):
        l, r = int(data[pos]) - 1, int(data[pos + 1]) - 1
        pos += 2
        k = (r - l + 1).bit_length() - 1
        start2 = r - (1 << k) + 1  # second block ends exactly at r
        out.append(max(hi[k][l], hi[k][start2]) - min(lo[k][l], lo[k][start2]))
    print("\n".join(map(str, out)))


if __name__ == "__main__":
    main()
```
