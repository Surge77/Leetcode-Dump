# 🔹 Solution — Mock 4 · Q2: Rival Teams (Bipartite Check + Subset-Sum DP, Medium)

**Problem statement:** [Q2_Medium_Rival_Teams.md](../Q2_Medium_Rival_Teams.md) · judge your own code first with `python tools/judge/judge.py M4Q2 <your_file>.py`

## 🔹 Quick Breakdown

* **Difficulty Level:** Medium (Q2 slot)
* **Main Approach:** (1) 2-colour each connected component; any conflict → `-1`. (2) Component `c` has sides of sizes `xᶜ`, `yᶜ`; team A gets either `xᶜ` or `yᶜ` from it. (3) Subset-sum DP over components for every reachable size of team A, then minimise `|N - 2A|`.
* **Core Concept:** Bipartite colouring + knapsack-style reachability
* **When to Use This Pattern?** Constraints force *relative* placement inside groups, but each group can be flipped as a whole.
* **Mistakes to Avoid:**
  * Colouring greedily across components — each component can be flipped independently, and the flip choice matters.
  * Forgetting isolated students (components of size 1: sides `1` and `0`).

## 🔹 Optimization Path

* **Brute Force:** Try all 2ᴺ splits (partial score for N ≤ 18).
* **Optimized Solution:** O(N + M) colouring + O(C · N / 64) bitset DP.
* **Further Improvements Possible?** Group equal components to cut the DP for huge N.

## 🔹 Solution Breakdown

* **Optimal Approach:** BFS colouring records `(x, y)` per component. Bitset `reach` (bit `a` = team A can have size `a`): `reach = (reach << x) | (reach << y)` per component.
* **Why This Works?** Inside a component, the colouring is forced up to a global flip, so the component's contribution to team A is exactly `x` or `y`; components are independent, so it is a subset-sum choice.
* **Edge Cases Considered:**
  * Odd cycle of rivals → `-1`.
  * No rivalries → difference `N % 2`.

## 🔹 Pattern Recognition

* **Belongs To:** Graph Colouring + DP (0/1 knapsack)
* **Common Problems Using This:**
  * 886. Possible Bipartition (in this repo)
  * 416. Partition Equal Subset Sum (in this repo — the bitset trick)

## 🔹 Tricks & Patterns Used

* **Bitset knapsack with Python big ints:** one shift-or per component.

## 🔹 Alternative Data Structures

* Union-Find with parity ("enemy of my enemy") instead of BFS colouring.

## 🔹 Complexity Analysis

* **Time Complexity:** O(N + M + C · N / 64), C = number of components
* **Space Complexity:** O(N + M)

## 🔹 Code Snippet (Brute Force — partial score)

```python
import sys


def main() -> None:
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    pairs = [(int(data[2 + 2 * i]) - 1, int(data[3 + 2 * i]) - 1) for i in range(m)]
    best = -1
    for mask in range(1 << n):  # bit i set => student i+1 is on team A
        if all((mask >> u & 1) != (mask >> v & 1) for u, v in pairs):
            diff = abs(n - 2 * bin(mask).count("1"))
            best = diff if best == -1 else min(best, diff)
    print(best)


if __name__ == "__main__":
    main()
```

## 🔹 Code Snippet (Optimized)

```python
import sys
from collections import deque


def main() -> None:
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    adj = [[] for _ in range(n + 1)]
    for i in range(m):
        u, v = int(data[2 + 2 * i]), int(data[3 + 2 * i])
        adj[u].append(v)
        adj[v].append(u)

    colour = [-1] * (n + 1)
    reach = 1  # bit a set <=> team A can have exactly a students
    for start in range(1, n + 1):
        if colour[start] != -1:
            continue
        colour[start] = 0
        sides = [1, 0]
        q = deque([start])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if colour[v] == -1:
                    colour[v] = 1 - colour[u]
                    sides[colour[v]] += 1
                    q.append(v)
                elif colour[v] == colour[u]:
                    print(-1)  # odd cycle of rivals
                    return
        reach = (reach << sides[0]) | (reach << sides[1])  # this component adds x or y to team A

    print(min(abs(n - 2 * a) for a in range(n + 1) if reach >> a & 1))


if __name__ == "__main__":
    main()
```
