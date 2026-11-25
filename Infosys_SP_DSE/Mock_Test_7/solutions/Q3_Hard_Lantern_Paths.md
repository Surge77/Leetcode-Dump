# 🔹 Solution — Mock 7 · Q3: Lantern Paths (Combinatorics + DP over Obstacles, Hard)

**Problem statement:** [Q3_Hard_Lantern_Paths.md](../Q3_Hard_Lantern_Paths.md) · judge your own code first with `python tools/judge/judge.py M7Q3 <your_file>.py`

## 🔹 Quick Breakdown

* **Difficulty Level:** Hard (Q3 slot)
* **Main Approach:** Without blocks, the number of right/down paths from `(r1, c1)` to `(r2, c2)` is `C((r2 − r1) + (c2 − c1), r2 − r1)`. The grid is 10⁵ × 10⁵ — no grid DP — but there are only `K ≤ 2000` blocked cells. Sort them (plus the target) by `(row, col)` and let `bad[i]` = paths from the start to cell `i` that touch **no earlier** blocked cell: `bad[i] = paths(start → i) − Σ bad[j] · paths(j → i)` over blocked `j` up-left of `i`. The answer is that value for the target.
* **Core Concept:** counting by complement over the **first** obstacle hit; nCr mod p with precomputed factorials
* **When to Use This Pattern?** Lattice paths on a huge grid with few forbidden points; "paths avoiding a set" via first-hit decomposition.
* **Mistakes to Avoid:**
  * A full grid DP: 10¹⁰ cells.
  * Subtracting `paths(start → j) · paths(j → i)` with the **unrestricted** count for `j` — paths through two blocks get subtracted twice. Use `bad[j]` (first block hit = `j`).
  * Forgetting `% MOD` after the subtraction (Python's `%` makes it non-negative).

## 🔹 Optimization Path

* **Brute Force:** grid DP — O(H · W), only for small grids.
* **Optimized Solution:** O(H + W) factorials + O(K²) pairs.

## 🔹 Solution Breakdown

* **Optimal Approach:** precompute `fact`, `inv_fact` up to `H + W`; sort blocks; for each point `i` in order (target last) compute `bad[i]` as above, only over `j` with `r_j ≤ r_i` and `c_j ≤ c_i`.
* **Why This Works?** Every path from the start to `i` that touches a blocked cell has a unique **first** blocked cell `j`; the part before `j` is counted by `bad[j]`, the part after is unrestricted. Sorting by `(row, col)` guarantees every `j` up-left of `i` is processed before `i`.
* **Edge Cases Considered:**
  * `K = 0` → plain binomial.
  * Blocks that cut off the target entirely → 0.

## 🔹 Pattern Recognition

* **Belongs To:** Combinatorics (nCr mod p) + DP over sorted points
* **Common Problems Using This:**
  * 62. Unique Paths (in this repo — the no-obstacle formula)
  * 63. Unique Paths II (small grid, plain DP)
  * 2400. Number of Ways to Reach a Position After Exactly k Steps (in this repo — nCr mod p)

## 🔹 Tricks & Patterns Used

* **Factorial + inverse-factorial tables:** `inv_fact[n] = pow(fact[n], MOD − 2, MOD)`, then backwards `inv_fact[i − 1] = inv_fact[i] · i`.
* **First-hit decomposition** to avoid inclusion–exclusion over 2ᴷ subsets.

## 🔹 Alternative Data Structures

* Inclusion–exclusion over subsets of blocks — exponential, only for `K ≤ 20`.

## 🔹 Complexity Analysis

* **Time Complexity:** O(H + W + K²)
* **Space Complexity:** O(H + W + K)

## 🔹 Code Snippet (Brute Force — partial score)

```python
import sys

MOD = 10**9 + 7


def main() -> None:
    data = sys.stdin.buffer.read().split()
    h, w, k = int(data[0]), int(data[1]), int(data[2])
    blocked = {(int(data[3 + 2 * i]), int(data[4 + 2 * i])) for i in range(k)}
    ways = [[0] * (w + 1) for _ in range(h + 1)]
    for r in range(1, h + 1):
        for c in range(1, w + 1):
            if (r, c) in blocked:
                continue
            ways[r][c] = 1 if (r, c) == (1, 1) else (ways[r - 1][c] + ways[r][c - 1]) % MOD
    print(ways[h][w])


if __name__ == "__main__":
    main()
```

## 🔹 Code Snippet (Optimized)

```python
import sys

MOD = 10**9 + 7


def main() -> None:
    data = sys.stdin.buffer.read().split()
    h, w, k = int(data[0]), int(data[1]), int(data[2])
    points = sorted((int(data[3 + 2 * i]), int(data[4 + 2 * i])) for i in range(k))
    points.append((h, w))  # the target comes last: every other point is up-left of it or irrelevant

    size = h + w
    fact = [1] * (size + 1)
    for i in range(1, size + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (size + 1)
    inv_fact[size] = pow(fact[size], MOD - 2, MOD)
    for i in range(size, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    def paths(dr: int, dc: int) -> int:
        return fact[dr + dc] * inv_fact[dr] % MOD * inv_fact[dc] % MOD

    bad = []  # bad[i]: paths from (1, 1) to point i that touch no earlier blocked cell
    for i, (r, c) in enumerate(points):
        count = paths(r - 1, c - 1)
        for j in range(i):
            rj, cj = points[j]
            if rj <= r and cj <= c:
                count -= bad[j] * paths(r - rj, c - cj)
        bad.append(count % MOD)
    print(bad[-1])


if __name__ == "__main__":
    main()
```
