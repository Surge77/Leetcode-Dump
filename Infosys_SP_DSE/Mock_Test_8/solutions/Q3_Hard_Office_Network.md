# 🔹 Solution — Mock 8 · Q3: Office Network (Rerooting DP on a Weighted Tree, Hard)

**Problem statement:** [Q3_Hard_Office_Network.md](../Q3_Hard_Office_Network.md) · judge your own code first with `python tools/judge/judge.py M8Q3 <your_file>.py`

## 🔹 Quick Breakdown

* **Difficulty Level:** Hard (Q3 slot)
* **Main Approach:** `cost(v) = Σ P[u] · dist(u, v)`. Compute `cost(1)` with one BFS (weighted depths). Then **reroot**: moving the meeting point across an edge `p — v` of length `w` brings everyone in `v`'s subtree (`sub[v]` people) `w` closer and everyone else (`total − sub[v]`) `w` farther: `cost(v) = cost(p) + w · (total − 2 · sub[v])`.
* **Core Concept:** rerooting DP with subtree **weights** (populations) instead of subtree sizes
* **When to Use This Pattern?** "Best node to place a facility on a tree", "sum of weighted distances to every node" — 834 with weights.
* **Mistakes to Avoid:**
  * Running Dijkstra/BFS from every node: O(N²).
  * Recursive DFS — `N = 2·10⁵` on a path overflows Python's stack. Use the BFS order.
  * Tie-breaking: the **smallest** office number among equal costs.

## 🔹 Optimization Path

* **Brute Force:** distances from every office — O(N²).
* **Optimized Solution:** two passes over a BFS order — O(N).

## 🔹 Solution Breakdown

* **Optimal Approach:** BFS from office 1 → `parent`, `up_w` (edge weight to parent), `depth` (weighted), order. Reverse order: `sub[p] += sub[v]`. `cost[1] = Σ P[u] · depth[u]`. Forward order: the transition above. Report `min(cost)` with the smallest index.
* **Why This Works?** For a neighbour `v` of `p`, `dist(u, v) = dist(u, p) − w` for `u` in `v`'s subtree and `dist(u, p) + w` otherwise; weighting by `P[u]` and summing gives the formula.
* **Edge Cases Considered:**
  * `N = 1` → cost 0 at office 1.
  * Offices with `P = 0` still count as candidate meeting points.

## 🔹 Pattern Recognition

* **Belongs To:** DP on Trees — rerooting
* **Common Problems Using This:**
  * 834. Sum of Distances in Tree (in this repo — unweighted version)
  * 2581. Count Number of Possible Root Nodes (in this repo)
  * Tree "median" / facility-location problems

## 🔹 Tricks & Patterns Used

* **BFS order** for both bottom-up (reversed) and top-down (forward) passes.
* **Exact integers:** the worst case is about 4·10¹⁶ — fits in 64-bit, and Python never overflows anyway.

## 🔹 Alternative Data Structures

* The optimum is a **weighted median** of the tree (a node whose every branch holds at most half of the total population) — an O(N) alternative once subtree sums are known.

## 🔹 Complexity Analysis

* **Time Complexity:** O(N)
* **Space Complexity:** O(N)

## 🔹 Code Snippet (Brute Force — partial score)

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    people = [0] + [int(x) for x in data[1:1 + n]]
    adj = [[] for _ in range(n + 1)]
    for k in range(n - 1):
        u, v, w = (int(x) for x in data[1 + n + 3 * k: 4 + n + 3 * k])
        adj[u].append((v, w))
        adj[v].append((u, w))
    best = None
    for meet in range(1, n + 1):
        dist = [-1] * (n + 1)
        dist[meet], stack = 0, [meet]
        while stack:  # tree: any traversal order gives the unique path lengths
            x = stack.pop()
            for y, w in adj[x]:
                if dist[y] < 0:
                    dist[y] = dist[x] + w
                    stack.append(y)
        cost = sum(people[u] * dist[u] for u in range(1, n + 1))
        if best is None or cost < best[0]:
            best = (cost, meet)
    print(*best)


if __name__ == "__main__":
    main()
```

## 🔹 Code Snippet (Optimized)

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    people = [0] + [int(x) for x in data[1:1 + n]]
    adj = [[] for _ in range(n + 1)]
    for k in range(n - 1):
        u, v, w = int(data[1 + n + 3 * k]), int(data[2 + n + 3 * k]), int(data[3 + n + 3 * k])
        adj[u].append((v, w))
        adj[v].append((u, w))

    parent, up_w, depth = [0] * (n + 1), [0] * (n + 1), [0] * (n + 1)
    parent[1], order = -1, [1]
    for x in order:  # BFS from office 1
        for y, w in adj[x]:
            if y != parent[x]:
                parent[y], up_w[y], depth[y] = x, w, depth[x] + w
                order.append(y)

    sub = people[:]  # population of each subtree
    for x in reversed(order[1:]):
        sub[parent[x]] += sub[x]
    total = sub[1]

    cost = [0] * (n + 1)
    cost[1] = sum(people[u] * depth[u] for u in range(1, n + 1))
    for x in order[1:]:  # move the meeting point from parent[x] to x
        cost[x] = cost[parent[x]] + up_w[x] * (total - 2 * sub[x])

    best = min(range(1, n + 1), key=lambda v: (cost[v], v))
    print(cost[best], best)


if __name__ == "__main__":
    main()
```
