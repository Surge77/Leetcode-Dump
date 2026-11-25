# 🔹 Solution — Mock 5 · Q3: Critical Routers (Articulation Points, Hard)

**Problem statement:** [Q3_Hard_Critical_Routers.md](../Q3_Hard_Critical_Routers.md) · judge your own code first with `python tools/judge/judge.py M5Q3 <your_file>.py`

## 🔹 Quick Breakdown

* **Difficulty Level:** Hard (Q3 slot)
* **Main Approach:** Tarjan's DFS with `disc[u]` (discovery time) and `low[u]` (earliest discovery time reachable from `u`'s subtree with one back edge). A non-root `u` is critical if some child `v` has `low[v] ≥ disc[u]`; the DFS root is critical if it has 2+ DFS children.
* **Core Concept:** Articulation points (cut vertices) via low-link values
* **When to Use This Pattern?** Single points of failure in networks; bridges are the edge version (1192 in this repo).
* **Mistakes to Avoid:**
  * Applying the `low[v] ≥ disc[u]` rule to the root — the root needs the "2+ children" rule.
  * Using `>` (that is the **bridge** condition) instead of `≥`.
  * Recursive DFS on 10⁵ routers in Python → `RecursionError`; the version below is iterative.

## 🔹 Optimization Path

* **Brute Force:** Remove each router and count components — O(N · (N + M)) (partial score).
* **Optimized Solution:** O(N + M) single DFS.
* **Further Improvements Possible?** No.

## 🔹 Solution Breakdown

* **Optimal Approach:** Iterative DFS keeping `(node, parent, next neighbour index)`. On finishing child `v` of `u`: `low[u] = min(low[u], low[v])`; if `u` is not the root and `low[v] ≥ disc[u]`, mark `u`. Count root children separately.
* **Why This Works?** `low[v] ≥ disc[u]` means nothing in `v`'s subtree reaches above `u` without passing through `u`, so removing `u` disconnects that subtree. The root has no ancestors, so it matters only if it joins two separate subtrees.
* **Edge Cases Considered:**
  * Isolated routers (never critical).
  * A cycle (no critical routers).
  * A path (every inner router is critical).
  * Repeated links.

## 🔹 Pattern Recognition

* **Belongs To:** Graph — Advanced (low-link)
* **Common Problems Using This:**
  * 1192. Critical Connections in a Network (in this repo — bridges)
  * 1568. Minimum Number of Days to Disconnect Island

## 🔹 Tricks & Patterns Used

* **Low-link values** summarise back edges of a whole subtree.
* **Explicit stack** to simulate recursion.

## 🔹 Alternative Data Structures

* Block-cut tree (biconnected components) when you need more than the list of cut vertices.

## 🔹 Complexity Analysis

* **Time Complexity:** O(N + M)
* **Space Complexity:** O(N + M)

## 🔹 Code Snippet (Brute Force — partial score)

```python
import sys


def components(n, adj, removed):
    seen, count = {removed}, 0
    for start in range(1, n + 1):
        if start in seen:
            continue
        count += 1
        seen.add(start)
        stack = [start]
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
    return count


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    adj = [[] for _ in range(n + 1)]
    for i in range(m):
        u, v = int(data[2 + 2 * i]), int(data[3 + 2 * i])
        adj[u].append(v)
        adj[v].append(u)
    base = components(n, adj, 0)
    critical = []
    for r in range(1, n + 1):
        if components(n, adj, r) > base:  # an isolated r only lowers the count
            critical.append(r)
    print(len(critical))
    if critical:
        print(" ".join(map(str, critical)))


if __name__ == "__main__":
    main()
```

## 🔹 Code Snippet (Optimized)

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    adj = [[] for _ in range(n + 1)]
    for i in range(m):
        u, v = int(data[2 + 2 * i]), int(data[3 + 2 * i])
        adj[u].append(v)
        adj[v].append(u)

    disc = [0] * (n + 1)  # 0 = not visited; times start at 1
    low = [0] * (n + 1)
    critical = [False] * (n + 1)
    timer = 0
    for root in range(1, n + 1):
        if disc[root]:
            continue
        timer += 1
        disc[root] = low[root] = timer
        root_children = 0
        stack = [(root, 0, 0)]  # (node, parent, next neighbour index)
        while stack:
            u, parent, i = stack[-1]
            if i < len(adj[u]):
                stack[-1] = (u, parent, i + 1)
                v = adj[u][i]
                if v == parent:
                    continue
                if disc[v]:
                    low[u] = min(low[u], disc[v])  # back edge
                else:
                    timer += 1
                    disc[v] = low[v] = timer
                    stack.append((v, u, 0))
                    if u == root:
                        root_children += 1
            else:
                stack.pop()
                if parent:
                    low[parent] = min(low[parent], low[u])
                    if parent != root and low[u] >= disc[parent]:
                        critical[parent] = True
        if root_children >= 2:
            critical[root] = True

    result = [r for r in range(1, n + 1) if critical[r]]
    print(len(result))
    if result:
        print(" ".join(map(str, result)))


if __name__ == "__main__":
    main()
```
