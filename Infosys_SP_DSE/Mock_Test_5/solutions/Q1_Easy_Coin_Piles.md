# 🔹 Solution — Mock 5 · Q1: Coin Piles (Game Theory — Sprague–Grundy, Easy)

**Problem statement:** [Q1_Easy_Coin_Piles.md](../Q1_Easy_Coin_Piles.md) · judge your own code first with `python tools/judge/judge.py M5Q1 <your_file>.py`

## 🔹 Quick Breakdown

* **Difficulty Level:** Easy (Q1 slot — once you know the theorem)
* **Main Approach:** A single pile with "take 1..K" has Grundy number `a % (K + 1)`. Independent piles combine by **XOR** (Sprague–Grundy). First wins iff the XOR is non-zero.
* **Core Concept:** Sprague–Grundy theorem / Nim
* **When to Use This Pattern?** Several independent games played side by side, normal play (no move ⇒ lose).
* **Mistakes to Avoid:**
  * Adding Grundy numbers instead of XOR-ing them.
  * Searching the game tree — positions are astronomically many.

## 🔹 Optimization Path

* **Brute Force:** Memoised search over tuples of pile sizes (partial score for tiny piles).
* **Optimized Solution:** O(N).
* **Further Improvements Possible?** No.

## 🔹 Solution Breakdown

* **Optimal Approach:** `x = XOR of (A[i] % (K + 1))`; print `First` if `x` else `Second`.
* **Why This Works?** For one pile, positions that are multiples of `K + 1` are losing (any move leaves a non-multiple, which can be reduced back to a multiple), and in general the mex recursion gives `a % (K + 1)`. Sprague–Grundy: a sum of games is losing iff the XOR of the components' Grundy numbers is 0.
* **Edge Cases Considered:**
  * All piles empty → `Second`.
  * `K` larger than every pile → plain Nim (XOR of the pile sizes).

## 🔹 Pattern Recognition

* **Belongs To:** Game Theory
* **Common Problems Using This:**
  * 292. Nim Game (in this repo — one pile, K = 3)
  * 1908. Game of Nim
  * 877. Stone Game

## 🔹 Tricks & Patterns Used

* **Grundy number = mex of the Grundy numbers of reachable positions.** Compute it by brute force for small sizes to discover patterns.

## 🔹 Alternative Data Structures

* None — one XOR accumulator.

## 🔹 Complexity Analysis

* **Time Complexity:** O(N)
* **Space Complexity:** O(1) beyond the input

## 🔹 Code Snippet (Brute Force — partial score)

```python
import sys
from functools import lru_cache


def main() -> None:
    data = sys.stdin.read().split()
    n, k = int(data[0]), int(data[1])
    piles = tuple(sorted(int(x) for x in data[2:2 + n]))

    @lru_cache(maxsize=None)
    def wins(state: tuple) -> bool:  # does the player to move win?
        for i, pile in enumerate(state):
            for take in range(1, min(k, pile) + 1):
                nxt = tuple(sorted(state[:i] + (pile - take,) + state[i + 1:]))
                if not wins(nxt):
                    return True
        return False

    print("First" if wins(piles) else "Second")


if __name__ == "__main__":
    main()
```

## 🔹 Code Snippet (Optimized)

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    xor = 0
    for token in data[2:2 + n]:
        xor ^= int(token) % (k + 1)  # Grundy number of one pile
    print("First" if xor else "Second")


if __name__ == "__main__":
    main()
```
