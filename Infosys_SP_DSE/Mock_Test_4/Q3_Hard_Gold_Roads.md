# 🔹 Problem Name: Gold Roads (SCC Condensation + DAG DP, Hard)

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 4, Question 3
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

A kingdom has `N` cities connected by `M` **one-way** roads. City `i` holds `G[i]` gold. A traveller may start in any city and follow roads as long as they like, visiting cities any number of times. The gold of a city is collected only once.

Print the maximum total gold the traveller can collect.

**Input Format**
* Line 1: two integers `N` and `M`
* Line 2: `N` integers `G[1..N]`
* Next `M` lines: two integers `u v` — a road from `u` to `v`

**Output Format**
* One integer — the maximum gold.

**Constraints**
* `1 ≤ N ≤ 10⁵`, `0 ≤ M ≤ 2·10⁵`
* `1 ≤ G[i] ≤ 10⁹`

**Sample Input**
```text
5 5
1 2 3 4 5
1 2
2 1
2 3
3 4
5 4
```

**Sample Output**
```text
10
```

**Explanation:** Cities 1 and 2 reach each other, so a traveller in either collects both (3 gold), then continues to 3 and 4: `3 + 3 + 4 = 10`. Starting at 5 gives only `5 + 4 = 9`.

## 🔹 Quick Breakdown

* **Difficulty Level:** Hard (Q3 slot)
* **Main Approach:** Inside a **strongly connected component** (SCC) the traveller can visit every city, so collapse each SCC into one node worth its total gold. The collapsed graph is a DAG: `best[c] = gold[c] + max(best[next])`.
* **Core Concept:** Kosaraju SCC + condensation + DP on a DAG
* **When to Use This Pattern?** Directed graphs with cycles where "anything inside a cycle is free" — reachability, max collectable value, 2-SAT.
* **Mistakes to Avoid:**
  * Longest-path DP directly on a graph with cycles — undefined / infinite loops.
  * Recursive DFS in Python on 10⁵ nodes → `RecursionError`. Both Kosaraju passes below are iterative.

## 🔹 Optimization Path

* **Brute Force:** Search over `(city, visited set)` states — exponential (partial score for N ≤ 15).
* **Optimized Solution:** O(N + M).
* **Further Improvements Possible?** Tarjan's algorithm finds SCCs in one pass, same complexity.

## 🔹 Solution Breakdown

* **Optimal Approach:**
  1. Pass 1: iterative DFS on the graph, record nodes by finish time.
  2. Pass 2: DFS on the **reversed** graph in decreasing finish time; each tree is one SCC. Components come out in topological order of the condensation.
  3. Process components in reverse of that order: `best[c] = gold[c] + max(best[d])` over edges `c → d`.
* **Why This Works?** Every walk visits a sequence of SCCs following DAG edges; within an SCC it can collect everything, and it can never return to an earlier SCC.
* **Edge Cases Considered:**
  * No roads → the richest single city.
  * The whole graph is one cycle → total gold.
  * Self-loops and parallel roads.

## 🔹 Pattern Recognition

* **Belongs To:** Graph — Advanced (SCC)
* **Common Problems Using This:**
  * 1857. Largest Color Value in a Directed Graph (in this repo — DAG DP)
  * 2360. Longest Cycle in a Graph
  * CSES "Coin Collector" (classic)

## 🔹 Tricks & Patterns Used

* **Kosaraju's second pass** emits SCCs in topological order of the condensation for free.
* **Iterative DFS with an explicit iterator index** to record finish order.

## 🔹 Alternative Data Structures

* Tarjan's low-link algorithm (one DFS, see 1192's low-link idea).

## 🔹 Complexity Analysis

* **Time Complexity:** O(N + M)
* **Space Complexity:** O(N + M)

## 🔹 Code Snippet (Brute Force — partial score)

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    gold = [int(x) for x in data[2:2 + n]]
    adj = [[] for _ in range(n)]
    for i in range(m):
        u, v = int(data[2 + n + 2 * i]) - 1, int(data[3 + n + 2 * i]) - 1
        adj[u].append(v)
    seen = set()
    stack = [(v, 1 << v) for v in range(n)]
    best = 0
    while stack:  # every (city, visited-set) state reachable from any start
        u, mask = stack.pop()
        if (u, mask) in seen:
            continue
        seen.add((u, mask))
        best = max(best, sum(gold[i] for i in range(n) if mask >> i & 1))
        for v in adj[u]:
            stack.append((v, mask | 1 << v))
    print(best)


if __name__ == "__main__":
    main()
```

## 🔹 Code Snippet (Optimized)

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    gold = [int(x) for x in data[2:2 + n]]
    adj = [[] for _ in range(n)]
    radj = [[] for _ in range(n)]
    pos = 2 + n
    for _ in range(m):
        u, v = int(data[pos]) - 1, int(data[pos + 1]) - 1
        pos += 2
        adj[u].append(v)
        radj[v].append(u)

    # Pass 1: finish order on the original graph (iterative DFS)
    visited = [False] * n
    order = []
    for root in range(n):
        if visited[root]:
            continue
        visited[root] = True
        stack = [(root, 0)]
        while stack:
            u, i = stack[-1]
            if i < len(adj[u]):
                stack[-1] = (u, i + 1)
                v = adj[u][i]
                if not visited[v]:
                    visited[v] = True
                    stack.append((v, 0))
            else:
                stack.pop()
                order.append(u)

    # Pass 2: SCCs on the reversed graph, in topological order of the condensation
    comp = [-1] * n
    comp_gold = []
    for root in reversed(order):
        if comp[root] != -1:
            continue
        cid = len(comp_gold)
        comp[root] = cid
        total, stack = 0, [root]
        while stack:
            u = stack.pop()
            total += gold[u]
            for v in radj[u]:
                if comp[v] == -1:
                    comp[v] = cid
                    stack.append(v)
        comp_gold.append(total)

    # DP on the DAG: later components cannot reach earlier ones
    best = comp_gold[:]
    out_edges = [[] for _ in comp_gold]
    for u in range(n):
        for v in adj[u]:
            if comp[u] != comp[v]:
                out_edges[comp[u]].append(comp[v])
    for c in range(len(comp_gold) - 1, -1, -1):
        for d in out_edges[c]:
            best[c] = max(best[c], comp_gold[c] + best[d])
    print(max(best))


if __name__ == "__main__":
    main()
```
