# 🔹 Solution — Mock 10 · Q3: Freight Limits (Binary Lifting, Path Maximum, Hard)

**Problem statement:** [Q3_Hard_Freight_Limits.md](../Q3_Hard_Freight_Limits.md) · judge your own code first with `python tools/judge/judge.py M10Q3 <your_file>.py`

## 🔹 Quick Breakdown

* **Difficulty Level:** Hard (Q3 slot)
* **Main Approach:** The road network is a tree, so each query's route is the unique path `u → v`, and the answer is the **heaviest** edge on it. With **binary lifting**, store `up[j][x]` (the `2ʲ`-th ancestor) **and** `heavy[j][x]` (the max edge weight on those `2ʲ` edges). Lift both endpoints to their LCA, taking the max of every jump you make.
* **Core Concept:** binary lifting carrying an aggregate (max) alongside the ancestor table
* **When to Use This Pattern?** Path queries on a static tree for any **associative** aggregate: max, min, sum, gcd.
* **Mistakes to Avoid:**
  * Walking the path per query — O(N) each, 10¹⁰ total.
  * Updating `x` before reading `heavy[j][x]` (read both from the old `x`).
  * `u == v` → 0 (no edges).

## 🔹 Optimization Path

* **Brute Force:** parent pointers + depths; walk the deeper endpoint up until they meet — O(N) per query.
* **Optimized Solution:** O(N log N) preprocessing, O(log N) per query.
* **Further Improvements Possible?** Offline: sort queries and edges and use DSU (Kruskal reconstruction) — also O((N + Q) log N).

## 🔹 Solution Breakdown

* **Optimal Approach:** BFS from 1 for `depth`, `up[0]`, `heavy[0]` (weight to parent). Level `j`: `up[j][x] = up[j−1][up[j−1][x]]`, `heavy[j][x] = max(heavy[j−1][x], heavy[j−1][up[j−1][x]])`. Query: lift the deeper endpoint by the depth difference, then lift both while their ancestors differ, then take the last two parent edges.
* **Why This Works?** A jump of `2ʲ` edges is two jumps of `2ʲ⁻¹`, and max is associative, so the table entries compose; the LCA climb covers each edge of `u → lca` and `v → lca` exactly once.
* **Edge Cases Considered:**
  * `u` is an ancestor of `v` — after equalising depths they coincide.
  * A path-shaped tree (depth 10⁵) — everything is iterative.

## 🔹 Pattern Recognition

* **Belongs To:** Trees — binary lifting / LCA
* **Common Problems Using This:**
  * [2846. Minimum Edge Weight Equilibrium Queries in a Tree](../../../Trees/2846.Minimum_Edge_Weight_Equilibrium_Queries_in_a_Tree.md)
  * [1483. Kth Ancestor of a Tree Node](../../../Trees/1483.Kth_Ancestor_of_a_Tree_Node.md)
  * 1697. Checking Existence of Edge Length Limited Paths (offline DSU alternative)

## 🔹 Tricks & Patterns Used

* **Aggregates ride along with the lifting table.**
* **Level-by-level list comprehensions** build the tables quickly in Python.

## 🔹 Alternative Data Structures

* Heavy-light decomposition + segment tree — needed only if edge weights change between queries.

## 🔹 Complexity Analysis

* **Time Complexity:** O((N + Q) log N)
* **Space Complexity:** O(N log N)

## 🔹 Code Snippet (Brute Force — partial score)

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, q = int(data[0]), int(data[1])
    adj = [[] for _ in range(n + 1)]
    pos = 2
    for _ in range(n - 1):
        u, v, w = int(data[pos]), int(data[pos + 1]), int(data[pos + 2])
        pos += 3
        adj[u].append((v, w))
        adj[v].append((u, w))
    parent, weight_up, depth = [0] * (n + 1), [0] * (n + 1), [0] * (n + 1)
    parent[1], order = -1, [1]
    for x in order:
        for y, w in adj[x]:
            if y != parent[x]:
                parent[y], weight_up[y], depth[y] = x, w, depth[x] + 1
                order.append(y)
    out = []
    for _ in range(q):
        u, v = int(data[pos]), int(data[pos + 1])
        pos += 2
        best = 0
        while u != v:
            if depth[u] < depth[v]:
                u, v = v, u
            best = max(best, weight_up[u])
            u = parent[u]
        out.append(str(best))
    print("\n".join(out))


if __name__ == "__main__":
    main()
```

## 🔹 Code Snippet (Optimized)

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, q = int(data[0]), int(data[1])
    adj = [[] for _ in range(n + 1)]
    pos = 2
    for _ in range(n - 1):
        u, v, w = int(data[pos]), int(data[pos + 1]), int(data[pos + 2])
        pos += 3
        adj[u].append((v, w))
        adj[v].append((u, w))

    log = max(1, n.bit_length())
    parent0, heavy0, depth = [0] * (n + 1), [0] * (n + 1), [0] * (n + 1)
    parent0[1], seen, order = 1, [False] * (n + 1), [1]  # the root is its own ancestor
    seen[1] = True
    for x in order:
        for y, w in adj[x]:
            if not seen[y]:
                seen[y] = True
                parent0[y], heavy0[y], depth[y] = x, w, depth[x] + 1
                order.append(y)
    up, heavy = [parent0], [heavy0]
    for j in range(1, log):
        prev_up, prev_heavy = up[j - 1], heavy[j - 1]
        up.append([prev_up[prev_up[x]] for x in range(n + 1)])
        heavy.append([max(prev_heavy[x], prev_heavy[prev_up[x]]) for x in range(n + 1)])

    out = []
    for _ in range(q):
        u, v = int(data[pos]), int(data[pos + 1])
        pos += 2
        best = 0
        if depth[u] < depth[v]:
            u, v = v, u
        diff, j = depth[u] - depth[v], 0
        while diff:
            if diff & 1:
                best = max(best, heavy[j][u])
                u = up[j][u]
            diff, j = diff >> 1, j + 1
        if u != v:
            for j in range(log - 1, -1, -1):
                if up[j][u] != up[j][v]:
                    best = max(best, heavy[j][u], heavy[j][v])
                    u, v = up[j][u], up[j][v]
            best = max(best, heavy[0][u], heavy[0][v])  # the last edge into the LCA on each side
        out.append(str(best))
    print("\n".join(out))


if __name__ == "__main__":
    main()
```
