# 🔹 Solution — Mock 2 · Q1: Server Rack Shuffle (Sliding Window on a Circle, Easy)

**Problem statement:** [Q1_Easy_Server_Rack_Shuffle.md](../Q1_Easy_Server_Rack_Shuffle.md) · judge your own code first with `python tools/judge/judge.py M2Q1 <your_file>.py`

## 🔹 Quick Breakdown

* **Difficulty Level:** Easy (Q1 slot)
* **Main Approach:** Let `k` = number of `1`s. The final block is some circular window of length `k`; each `0` inside it needs exactly one swap with a `1` outside. Answer = `k - (max 1s in any circular window of length k)`.
* **Core Concept:** Fixed-size sliding window + circular array (double the string)
* **When to Use This Pattern?** "Group all X together with minimum swaps", circular subarray questions.
* **Mistakes to Avoid:**
  * Simulating swaps — the counting argument gives the answer directly.
  * Forgetting the wrap-around (`S + S`, or index `% N`).
  * `k = 0` or `k = N` → 0.

## 🔹 Optimization Path

* **Brute Force:** O(N · k) — count zeros in every window from scratch (partial score).
* **Optimized Solution:** O(N) — slide the window, add the entering character, remove the leaving one.
* **Further Improvements Possible?** No.

## 🔹 Solution Breakdown

* **Optimal Approach:** Count `1`s in the first window of `S + S`, slide it across the `N` starting positions, track the maximum.
* **Why This Works?** A swap can move at most one `1` into the chosen window, so `zeros in window` swaps are necessary; swapping each such `0` with an outside `1` shows they are sufficient.
* **Edge Cases Considered:**
  * No `1`s or all `1`s.
  * The best window wraps around the end.

## 🔹 Pattern Recognition

* **Belongs To:** Sliding Window
* **Common Problems Using This:**
  * 2134. Minimum Swaps to Group All 1's Together II
  * 1151. Minimum Swaps to Group All 1's Together
  * 918. Maximum Sum Circular Subarray

## 🔹 Tricks & Patterns Used

* **Double the string** to linearise a circle.
* **Lower bound + construction** argument for the swap count.

## 🔹 Alternative Data Structures

* Prefix sums over `S + S` — window count = `P[i + k] - P[i]`.

## 🔹 Complexity Analysis

* **Time Complexity:** O(N)
* **Space Complexity:** O(N)

## 🔹 Code Snippet (Brute Force — partial score)

```python
import sys


def main() -> None:
    data = sys.stdin.read().split()
    n, s = int(data[0]), data[1]
    k = s.count("1")
    best = 0 if k in (0, n) else n
    if 0 < k < n:
        for start in range(n):  # every circular window of length k
            zeros = sum(1 for j in range(k) if s[(start + j) % n] == "0")
            best = min(best, zeros)
    print(best)


if __name__ == "__main__":
    main()
```

## 🔹 Code Snippet (Optimized)

```python
import sys


def main() -> None:
    data = sys.stdin.read().split()
    n, s = int(data[0]), data[1]
    k = s.count("1")
    if k == 0 or k == n:
        print(0)
        return
    doubled = s + s  # linearise the circle
    ones = doubled[:k].count("1")
    best = ones
    for end in range(k, n + k - 1):  # windows starting at 1 .. n-1
        ones += (doubled[end] == "1") - (doubled[end - k] == "1")
        best = max(best, ones)
    print(k - best)  # zeros inside the best window


if __name__ == "__main__":
    main()
```
