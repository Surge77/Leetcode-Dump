# 🔹 Solution — Mock 8 · Q1: Ferry Seats (Greedy, Two Pointers, Easy)

**Problem statement:** [Q1_Easy_Ferry_Seats.md](../Q1_Easy_Ferry_Seats.md) · judge your own code first with `python tools/judge/judge.py M8Q1 <your_file>.py`

## 🔹 Quick Breakdown

* **Difficulty Level:** Easy (Q1 slot)
* **Main Approach:** Sort the weights. The heaviest remaining passenger must board some boat; pair them with the **lightest** remaining passenger if the two fit, otherwise send them alone. Two pointers from both ends.
* **Core Concept:** greedy pairing on a sorted array (exchange argument)
* **When to Use This Pattern?** "At most two per container, capacity limit, minimise containers" — boats, rickshaws, team pairs.
* **Mistakes to Avoid:**
  * Pairing the heaviest with the heaviest partner that fits is also optimal, but needs a search per passenger; the lightest partner gives the same count with a plain two-pointer walk.
  * Trying all pairings — exponential.

## 🔹 Optimization Path

* **Brute Force:** bitmask DP over who has boarded — O(2ᴺ · N), only for tiny `N`.
* **Optimized Solution:** sort + two pointers — O(N log N).

## 🔹 Solution Breakdown

* **Optimal Approach:** `i = 0`, `j = N − 1`; each step uses one boat for `j` (and `i` too if `w[i] + w[j] ≤ C`).
* **Why This Works?** If the heaviest person `j` can share with anyone, they can share with the lightest `i`. In any optimal plan, swapping `i` into `j`'s boat (and `j`'s old partner into `i`'s old place) keeps every boat within capacity, so the greedy choice never hurts. If `j` cannot share with `i`, `j` cannot share with anyone.
* **Edge Cases Considered:**
  * `N = 1` → 1 boat.
  * Everyone heavier than `C / 2` → `N` boats.

## 🔹 Pattern Recognition

* **Belongs To:** Greedy + Two Pointers
* **Common Problems Using This:**
  * 881. Boats to Save People
  * 11. Container With Most Water (in this repo — two pointers from both ends)
  * 2563. Count the Number of Fair Pairs (in this repo)

## 🔹 Tricks & Patterns Used

* **Exchange argument** to justify a greedy pairing.

## 🔹 Alternative Data Structures

* Counting sort when weights are small.

## 🔹 Complexity Analysis

* **Time Complexity:** O(N log N)
* **Space Complexity:** O(N)

## 🔹 Code Snippet (Brute Force — partial score)

```python
import sys
from functools import lru_cache


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, cap = int(data[0]), int(data[1])
    w = [int(x) for x in data[2:2 + n]]

    @lru_cache(maxsize=None)
    def boats(mask: int) -> int:  # mask = passengers already on a boat
        if mask == (1 << n) - 1:
            return 0
        i = next(b for b in range(n) if not mask >> b & 1)  # lowest unseated passenger
        best = 1 + boats(mask | 1 << i)
        for j in range(i + 1, n):
            if not mask >> j & 1 and w[i] + w[j] <= cap:
                best = min(best, 1 + boats(mask | 1 << i | 1 << j))
        return best

    print(boats(0))


if __name__ == "__main__":
    main()
```

## 🔹 Code Snippet (Optimized)

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, cap = int(data[0]), int(data[1])
    w = sorted(int(x) for x in data[2:2 + n])
    i, j, boats = 0, n - 1, 0
    while i <= j:
        if i < j and w[i] + w[j] <= cap:
            i += 1  # the lightest rides with the heaviest
        j -= 1
        boats += 1
    print(boats)


if __name__ == "__main__":
    main()
```
