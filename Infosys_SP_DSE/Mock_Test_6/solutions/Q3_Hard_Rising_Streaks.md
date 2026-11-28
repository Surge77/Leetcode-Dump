# 🔹 Solution — Mock 6 · Q3: Rising Streaks (DP + Fenwick Tree, Hard)

**Problem statement:** [Q3_Hard_Rising_Streaks.md](../Q3_Hard_Rising_Streaks.md) · judge your own code first with `python tools/judge/judge.py M6Q3 <your_file>.py`

## 🔹 Quick Breakdown

* **Difficulty Level:** Hard (Q3 slot)
* **Main Approach:** `end[k][i]` = increasing subsequences of length `k` ending at index `i` = Σ `end[k-1][j]` over earlier `j` with `A[j] < A[i]`. Keep one Fenwick tree per length over compressed values to get that sum in O(log N).
* **Core Concept:** DP with Fenwick-tree prefix sums (+ coordinate compression, mod)
* **When to Use This Pattern?** Counting increasing/decreasing subsequences, inversions of length k, "pairs/triples with order constraints".
* **Mistakes to Avoid:**
  * Equal values must **not** chain — query ranks strictly below `rank(x)`.
  * Reading and updating the same index in one pass — safe here because the query is strictly below `rank(x)`, so an update at `rank(x)` is never seen; with a non-strict `≤` query you would have to read everything before writing.
  * Forgetting the modulo inside the Fenwick tree.

## 🔹 Optimization Path

* **Brute Force:** Try every index combination — O(C(N, K)) (partial score).
* **Plain DP:** O(N² · K).
* **Optimized Solution:** O(N · K · log N).

## 🔹 Solution Breakdown

* **Optimal Approach:** For each `x` in order: `cur[1] = 1`; for `k = 2..K`: `cur[k] = bit[k-1].prefix(rank(x) - 1)`; then add `cur[k]` into `bit[k]` at `rank(x)`. The answer is the total added to `bit[K]`.
* **Why This Works?** When `x` is processed, `bit[k-1]` holds exactly the length-`(k-1)` subsequences ending at earlier indices; the prefix query keeps only those ending with a smaller value, so appending `x` keeps them increasing.
* **Edge Cases Considered:**
  * `K = 1` → `N`.
  * All values equal → 0 for `K ≥ 2`.
  * `K > N` → 0.

## 🔹 Pattern Recognition

* **Belongs To:** Fenwick Tree + DP
* **Common Problems Using This:**
  * 1395. Count Number of Teams (K = 3)
  * 673. Number of Longest Increasing Subsequence
  * [315. Count of Smaller Numbers After Self](../../../Range_Queries/315.Count_of_Smaller_Numbers_After_Self.md)

## 🔹 Tricks & Patterns Used

* **One Fenwick tree per length**, all over the same compressed ranks.
* **Coordinate compression** because values reach 10⁹.

## 🔹 Alternative Data Structures

* Segment tree per length — same complexity, more code.

## 🔹 Complexity Analysis

* **Time Complexity:** O(N · K · log N)
* **Space Complexity:** O(N · K)

## 🔹 Code Snippet (Brute Force — partial score)

```python
import sys
from itertools import combinations

MOD = 10**9 + 7


def main() -> None:
    data = sys.stdin.read().split()
    n, k = int(data[0]), int(data[1])
    a = [int(x) for x in data[2:2 + n]]
    count = sum(1 for idx in combinations(range(n), k)
                if all(a[idx[t]] < a[idx[t + 1]] for t in range(k - 1)))
    print(count % MOD)


if __name__ == "__main__":
    main()
```

## 🔹 Code Snippet (Optimized)

```python
import sys

MOD = 10**9 + 7


def main() -> None:
    data = sys.stdin.read().split()
    n, k = int(data[0]), int(data[1])
    a = [int(x) for x in data[2:2 + n]]
    rank = {v: i + 1 for i, v in enumerate(sorted(set(a)))}
    size = len(rank)
    bits = [[0] * (size + 1) for _ in range(k + 1)]  # bits[length]: Fenwick over ranks

    def add(tree, i, delta):
        while i <= size:
            tree[i] = (tree[i] + delta) % MOD
            i += i & -i

    def prefix(tree, i):
        total = 0
        while i > 0:
            total += tree[i]
            i -= i & -i
        return total % MOD

    answer = 0
    for x in a:
        r = rank[x]
        cur = [0] * (k + 1)
        cur[1] = 1
        for length in range(2, k + 1):
            cur[length] = prefix(bits[length - 1], r - 1)  # strictly smaller values only
        for length in range(1, k + 1):
            if cur[length]:
                add(bits[length], r, cur[length])
        answer = (answer + cur[k]) % MOD
    print(answer)


if __name__ == "__main__":
    main()
```
