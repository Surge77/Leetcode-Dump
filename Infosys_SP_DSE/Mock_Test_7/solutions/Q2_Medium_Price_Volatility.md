# 🔹 Solution — Mock 7 · Q2: Price Volatility (Monotonic Stack, Contribution Technique, Medium)

**Problem statement:** [Q2_Medium_Price_Volatility.md](../Q2_Medium_Price_Volatility.md) · judge your own code first with `python tools/judge/judge.py M7Q2 <your_file>.py`

## 🔹 Quick Breakdown

* **Difficulty Level:** Medium (Q2 slot)
* **Main Approach:** `Σ (max − min) = Σ max − Σ min` over all windows. Count, for every day `i`, **how many windows have `A[i]` as their maximum**: `(i − p) · (q − i)`, where `p` is the previous day with price `≥ A[i]` and `q` the next day with price `> A[i]` (monotonic stack). Same for minima — or reuse the max routine on `−A`.
* **Core Concept:** contribution technique — sum over windows → sum over elements × number of windows they win
* **When to Use This Pattern?** "Sum of min / max / range over all subarrays" (907, 2104), "count subarrays where `A[i]` is the max".
* **Mistakes to Avoid:**
  * Equal prices counted twice (or zero times): make one boundary non-strict (previous `≥` on the left) and the other strict (next `>` on the right), so each window is credited to its **leftmost** maximum.
  * O(N²) window scanning — `N = 10⁵` gives 5·10⁹ windows.

## 🔹 Optimization Path

* **Brute Force:** extend every start, tracking running max/min — O(N²).
* **Optimized Solution:** two monotonic-stack passes for maxima, two for minima — O(N).

## 🔹 Solution Breakdown

* **Optimal Approach:** `sum_of_max(A)`: left pass pops while `A[top] < A[i]` (so the survivor is `≥ A[i]`), right pass pops while `A[top] ≤ A[i]` (survivor `> A[i]`). Answer `sum_of_max(A) + sum_of_max([−x for x in A])`.
* **Why This Works?** A window `[l, r]` has `A[i]` as its leftmost maximum iff `p < l ≤ i ≤ r < q`. There are `(i − p)` choices for `l` and `(q − i)` for `r`. Every window has exactly one leftmost maximum, so the sum is exact. `min(A) = −max(−A)`.
* **Edge Cases Considered:**
  * All prices equal → every range is 0.
  * `N = 1` → 0.

## 🔹 Pattern Recognition

* **Belongs To:** Monotonic Stack
* **Common Problems Using This:**
  * [907. Sum of Subarray Minimums](../../../Stack/907.Sum_of_Subarray_Minimums.md)
  * 2104. Sum of Subarray Ranges
  * 84. Largest Rectangle in Histogram (in this repo — same previous/next smaller boundaries)

## 🔹 Tricks & Patterns Used

* **Previous ≥ / next >** boundaries to break ties.
* **Negate to flip max ↔ min** and reuse one function.

## 🔹 Alternative Data Structures

* Sparse table + divide and conquer on the max position: O(N log N), more code.

## 🔹 Complexity Analysis

* **Time Complexity:** O(N)
* **Space Complexity:** O(N)

## 🔹 Code Snippet (Brute Force — partial score)

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]
    total = 0
    for i in range(n):
        hi = lo = a[i]
        for j in range(i, n):
            hi, lo = max(hi, a[j]), min(lo, a[j])
            total += hi - lo
    print(total)


if __name__ == "__main__":
    main()
```

## 🔹 Code Snippet (Optimized)

```python
import sys


def sum_of_max(a):
    """Sum over all windows of the window maximum (each window credited to its leftmost max)."""
    n = len(a)
    left, right, stack = [0] * n, [0] * n, []
    for i in range(n):
        while stack and a[stack[-1]] < a[i]:
            stack.pop()
        left[i] = i - (stack[-1] if stack else -1)  # previous index with a[p] >= a[i]
        stack.append(i)
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and a[stack[-1]] <= a[i]:
            stack.pop()
        right[i] = (stack[-1] if stack else n) - i  # next index with a[q] > a[i]
        stack.append(i)
    return sum(x * l * r for x, l, r in zip(a, left, right))


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]
    print(sum_of_max(a) + sum_of_max([-x for x in a]))  # sum of max - sum of min


if __name__ == "__main__":
    main()
```
