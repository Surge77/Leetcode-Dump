# 🔹 Problem Name: Toll Pass (Dijkstra on State Graph, Medium)

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 2, Question 2
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

A courier must travel from city `1` to city `N`. There are `M` two-way roads; road `j` connects `u` and `v` and charges a toll `w`. The courier owns **one free pass**: it makes the toll of **one** road on the route zero (it may also stay unused).

Print the minimum total toll from city `1` to city `N`, or `-1` if city `N` is unreachable.

**Input Format**
* Line 1: two integers `N` and `M`
* Next `M` lines: three integers `u v w`

**Output Format**
* One integer — the minimum total toll, or `-1`.

**Constraints**
* `1 ≤ N ≤ 10⁵`, `0 ≤ M ≤ 2·10⁵`
* `1 ≤ u, v ≤ N`
* `1 ≤ w ≤ 10⁹`

**Sample Input**
```text
4 4
1 2 5
2 4 100
1 3 20
3 4 30
```

**Sample Output**
```text
5
```

**Explanation:** Route `1 → 2 → 4` costs `5 + 100`; using the pass on the 100-toll road leaves 5. Route `1 → 3 → 4` with the pass costs at least 20.

## 🔹 Quick Breakdown

* **Difficulty Level:** Medium (Q2 slot)
* **Main Approach:** Duplicate every city into two states: `(city, pass unused)` and `(city, pass used)`. A road gives a normal edge within each layer and a **zero-cost** edge from the unused layer to the used layer. Run Dijkstra on these `2N` states.
* **Core Concept:** Dijkstra on an expanded state graph
* **When to Use This Pattern?** Shortest paths with a limited number of special moves: coupons, k free edges, one wall break, fuel limits.
* **Mistakes to Avoid:**
  * Greedy "use the pass on the most expensive road of the plain shortest path" — the best route with a pass can be a completely different route.
  * Plain BFS — tolls are weighted.

## 🔹 Optimization Path

* **Brute Force:** Try every road as the free one and run Dijkstra each time — O(M · M log N) (partial score).
* **Optimized Solution:** One Dijkstra over `2N` states — O(M log N).
* **Further Improvements Possible?** `k` passes → `(k+1)` layers, same idea.

## 🔹 Solution Breakdown

* **Optimal Approach:** `dist[v][used]`; from state `(u, 0)`: pay `w` to `(v, 0)` or pay 0 to `(v, 1)`; from `(u, 1)`: pay `w` to `(v, 1)`. Answer `min(dist[N][0], dist[N][1])`.
* **Why This Works?** Every route with at most one free road corresponds to exactly one path in the layered graph with the same cost, and all edge weights are non-negative, so Dijkstra is valid.
* **Edge Cases Considered:**
  * `N = 1` → 0.
  * Disconnected graph → -1.
  * Parallel roads between the same pair.

## 🔹 Pattern Recognition

* **Belongs To:** Graph — Shortest Path (state expansion)
* **Common Problems Using This:**
  * 787. Cheapest Flights Within K Stops (in this repo)
  * 1293. Shortest Path in a Grid with Obstacles Elimination
  * 2093. Minimum Cost to Reach City With Discounts

## 🔹 Tricks & Patterns Used

* **Add the resource to the state** (`used` flag).
* **Lazy deletion** of stale heap entries.

## 🔹 Alternative Data Structures

* Two Dijkstras: from `1` (`d1`) and from `N` (`dN`); answer `min over roads (u,v)` of `d1[u] + dN[v]` (both directions) and `d1[N]`.

## 🔹 Complexity Analysis

* **Time Complexity:** O((N + M) log N)
* **Space Complexity:** O(N + M)

## 🔹 Code Snippet (Brute Force — partial score)

```python
import heapq
import sys


def dijkstra(n, roads, free_road):
    adj = [[] for _ in range(n + 1)]
    for j, (u, v, w) in enumerate(roads):
        cost = 0 if j == free_road else w
        adj[u].append((v, cost))
        adj[v].append((u, cost))
    dist = [float("inf")] * (n + 1)
    dist[1] = 0
    pq = [(0, 1)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))
    return dist[n]


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    roads = [tuple(map(int, data[2 + 3 * j: 5 + 3 * j])) for j in range(m)]
    best = min(dijkstra(n, roads, free) for free in range(-1, m))  # -1 = pass unused
    print(best if best < float("inf") else -1)


if __name__ == "__main__":
    main()
```

## 🔹 Code Snippet (Optimized)

```python
import heapq
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    adj = [[] for _ in range(n + 1)]
    pos = 2
    for _ in range(m):
        u, v, w = int(data[pos]), int(data[pos + 1]), int(data[pos + 2])
        pos += 3
        adj[u].append((v, w))
        adj[v].append((u, w))

    INF = float("inf")
    dist = [[INF, INF] for _ in range(n + 1)]  # dist[city][pass used?]
    dist[1][0] = 0
    pq = [(0, 1, 0)]
    while pq:
        d, u, used = heapq.heappop(pq)
        if d > dist[u][used]:
            continue
        for v, w in adj[u]:
            if d + w < dist[v][used]:  # pay the toll
                dist[v][used] = d + w
                heapq.heappush(pq, (d + w, v, used))
            if not used and d < dist[v][1]:  # use the pass on this road
                dist[v][1] = d
                heapq.heappush(pq, (d, v, 1))
    best = min(dist[n])
    print(best if best < INF else -1)


if __name__ == "__main__":
    main()
```
