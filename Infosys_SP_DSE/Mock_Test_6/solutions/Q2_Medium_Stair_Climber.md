# 🔹 Solution — Mock 6 · Q2: Stair Climber (Matrix Exponentiation, Medium)

**Problem statement:** [Q2_Medium_Stair_Climber.md](../Q2_Medium_Stair_Climber.md) · judge your own code first with `python tools/judge/judge.py M6Q2 <your_file>.py`

## 🔹 Quick Breakdown

* **Difficulty Level:** Medium (Q2 slot)
* **Main Approach:** `ways[n] = Σ ways[n - s]` is a linear recurrence of order `D = max(s)`. Put the last `D` values in a vector; one step is a multiplication by a `D × D` companion matrix. Raise it to the power `N` with fast exponentiation.
* **Core Concept:** Linear recurrence → companion matrix → matrix power
* **When to Use This Pattern?** DP with a fixed small window of previous values and `N` up to 10¹⁸.
* **Mistakes to Avoid:**
  * Iterating the DP `N` times — impossible for 10¹⁸.
  * Off-by-one in the starting vector (`ways[0] = 1`, negative indices are 0).

## 🔹 Optimization Path

* **Brute Force:** DP over `0..N` — O(N · K) (partial score).
* **Optimized Solution:** O(D³ · log N), D ≤ 10.
* **Further Improvements Possible?** Kitamasa / polynomial methods — O(D² log N), not needed here.

## 🔹 Solution Breakdown

* **Optimal Approach:** State vector `[ways[n], ways[n-1], …, ways[n-D+1]]`. Row 0 of the matrix has a 1 in column `s - 1` for each allowed `s`; rows `1..D-1` shift the vector down. Start from `[1, 0, …, 0]` (= `ways[0]`), apply `M^N`, read entry 0.
* **Why This Works?** Matrix multiplication by `M` maps the window ending at `n` to the window ending at `n + 1`, so `M^N` jumps `N` steps at once.
* **Edge Cases Considered:**
  * Only large steps (some `N` unreachable → 0).
  * `N = 1`.

## 🔹 Pattern Recognition

* **Belongs To:** DP — Matrix Exponentiation
* **Common Problems Using This:**
  * 70. Climbing Stairs (in this repo — steps 1, 2 with small N)
  * [935. Knight Dialer](../../../DP_Advanced/935.Knight_Dialer.md)
  * 1137. N-th Tribonacci Number

## 🔹 Tricks & Patterns Used

* **Companion matrix** for any linear recurrence.
* **Modulo Arithmetic** in every product.

## 🔹 Alternative Data Structures

* None needed at this size.

## 🔹 Complexity Analysis

* **Time Complexity:** O(D³ log N)
* **Space Complexity:** O(D²)

## 🔹 Code Snippet (Brute Force — partial score)

```python
import sys

MOD = 10**9 + 7


def main() -> None:
    data = sys.stdin.read().split()
    n, k = int(data[0]), int(data[1])
    steps = [int(x) for x in data[2:2 + k]]
    ways = [1] + [0] * n
    for i in range(1, n + 1):
        ways[i] = sum(ways[i - s] for s in steps if i - s >= 0) % MOD
    print(ways[n])


if __name__ == "__main__":
    main()
```

## 🔹 Code Snippet (Optimized)

```python
import sys

MOD = 10**9 + 7


def mat_mult(a, b):
    size = len(a)
    return [[sum(a[i][t] * b[t][j] for t in range(size)) % MOD for j in range(size)]
            for i in range(size)]


def mat_pow(m, e):
    result = [[int(i == j) for j in range(len(m))] for i in range(len(m))]
    while e:
        if e & 1:
            result = mat_mult(result, m)
        m = mat_mult(m, m)
        e >>= 1
    return result


def main() -> None:
    data = sys.stdin.read().split()
    n, k = int(data[0]), int(data[1])
    steps = [int(x) for x in data[2:2 + k]]
    d = max(steps)
    step = [[0] * d for _ in range(d)]  # companion matrix
    for s in steps:
        step[0][s - 1] = 1  # ways[n+1] += ways[n+1-s]
    for i in range(1, d):
        step[i][i - 1] = 1  # shift the window down
    power = mat_pow(step, n)
    print(power[0][0] % MOD)  # start vector is [ways[0] = 1, 0, ..., 0]


if __name__ == "__main__":
    main()
```
