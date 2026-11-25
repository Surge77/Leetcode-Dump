# 🔹 Problem Name: Treasure Route (BFS + Bitmask DP, Hard)

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 2, Question 3
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

A robot stands on cell `S` of an `R × C` warehouse grid. Cells are `.` (free), `#` (wall), `S` (start, free) or `T` (a treasure, free). Each move goes to an adjacent free cell (up, down, left, right) and takes one step.

Print the minimum number of steps needed to visit **every** treasure (in any order, ending anywhere), or `-1` if some treasure cannot be reached.

**Input Format**
* Line 1: two integers `R` and `C`
* Next `R` lines: a string of length `C`

**Output Format**
* One integer — the minimum number of steps, or `-1`.

**Constraints**
* `1 ≤ R, C ≤ 50`
* Exactly one `S`; `0 ≤ number of T ≤ 12`

**Sample Input**
```text
4 5
S..T.
.##..
T...#
..#.T
```

**Sample Output**
```text
11
```

**Explanation:** The robot must pick the best order of the three treasures; trying every order with the true walking distances gives the answer.

## 🔹 Quick Breakdown

* **Difficulty Level:** Hard (Q3 slot)
* **Main Approach:** (1) BFS from `S` and from every treasure → walking distance between every pair of key points. (2) Held–Karp DP: `dp[mask][i]` = fewest steps to collect the treasures in `mask`, standing on treasure `i`.
* **Core Concept:** BFS distances + bitmask DP (travelling-salesman path)
* **When to Use This Pattern?** "Visit all K special cells/cities" with `K ≤ 15` — the small `K` is the signal.
* **Mistakes to Avoid:**
  * Trying all `K!` orders — 12! ≈ 4.8·10⁸ (fine only for partial score).
  * BFS over `(cell, mask)` — `2500 · 4096` states; correct but too slow in Python.
  * Forgetting the unreachable case.

## 🔹 Optimization Path

* **Brute Force:** BFS distances + every permutation — O(K · R·C + K! · K) (partial score for K ≤ 8).
* **Optimized Solution:** O(K · R·C + 2ᴷ · K²).
* **Further Improvements Possible?** No for exact answers.

## 🔹 Solution Breakdown

* **Optimal Approach:** `dp[1 << i][i] = dist(S, Tᵢ)`; for each `mask` and each end `i` in it, extend to an unvisited `j`: `dp[mask | 1<<j][j] = min(…, dp[mask][i] + dist(Tᵢ, Tⱼ))`. Answer `min(dp[full][i])`.
* **Why This Works?** Only *which* treasures are collected and *where* the robot stands matter for the future, so `(mask, i)` is a complete state; BFS distances are exact shortest walks between key points.
* **Edge Cases Considered:**
  * No treasures → 0.
  * A walled-off treasure → -1.
  * Treasures adjacent to each other.

## 🔹 Pattern Recognition

* **Belongs To:** DP — Bitmask (TSP) + BFS
* **Common Problems Using This:**
  * 847. Shortest Path Visiting All Nodes (in this repo)
  * 864. Shortest Path to Get All Keys
  * 943. Find the Shortest Superstring

## 🔹 Tricks & Patterns Used

* **Compress the grid to K+1 key points** with BFS, then work on a tiny complete graph.
* **Bit Manipulation:** `mask >> i & 1`, `mask | 1 << j`.

## 🔹 Alternative Data Structures

* Dijkstra instead of BFS if moves had different costs.

## 🔹 Complexity Analysis

* **Time Complexity:** O(K · R · C + 2ᴷ · K²)
* **Space Complexity:** O(K · R · C + 2ᴷ · K)

## 🔹 Code Snippet (Brute Force — partial score)

```python
import sys
from collections import deque
from itertools import permutations


def bfs(grid, r, c, sr, sc):
    dist = [[-1] * c for _ in range(r)]
    dist[sr][sc] = 0
    q = deque([(sr, sc)])
    while q:
        i, j = q.popleft()
        for x, y in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= x < r and 0 <= y < c and grid[x][y] != "#" and dist[x][y] == -1:
                dist[x][y] = dist[i][j] + 1
                q.append((x, y))
    return dist


def main() -> None:
    data = sys.stdin.read().split()
    r, c = int(data[0]), int(data[1])
    grid = data[2:2 + r]
    points = [(i, j) for i in range(r) for j in range(c) if grid[i][j] == "S"]
    points += [(i, j) for i in range(r) for j in range(c) if grid[i][j] == "T"]
    tables = [bfs(grid, r, c, i, j) for i, j in points]
    d = [[tables[a][i][j] for i, j in points] for a in range(len(points))]
    if any(x == -1 for x in d[0]):
        print(-1)
        return
    best = 0 if len(points) == 1 else min(
        sum(d[a][b] for a, b in zip((0,) + order, order))
        for order in permutations(range(1, len(points))))
    print(best)


if __name__ == "__main__":
    main()
```

## 🔹 Code Snippet (Optimized)

```python
import sys
from collections import deque


def bfs(grid, r, c, sr, sc):
    dist = [[-1] * c for _ in range(r)]
    dist[sr][sc] = 0
    q = deque([(sr, sc)])
    while q:
        i, j = q.popleft()
        for x, y in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= x < r and 0 <= y < c and grid[x][y] != "#" and dist[x][y] == -1:
                dist[x][y] = dist[i][j] + 1
                q.append((x, y))
    return dist


def main() -> None:
    data = sys.stdin.read().split()
    r, c = int(data[0]), int(data[1])
    grid = data[2:2 + r]
    start = next((i, j) for i in range(r) for j in range(c) if grid[i][j] == "S")
    treasures = [(i, j) for i in range(r) for j in range(c) if grid[i][j] == "T"]
    k = len(treasures)
    if k == 0:
        print(0)
        return

    points = [start] + treasures  # index 0 = start, 1..k = treasures
    tables = [bfs(grid, r, c, i, j) for i, j in points]
    d = [[tables[a][i][j] for i, j in points] for a in range(k + 1)]
    if any(x == -1 for x in d[0]):
        print(-1)
        return

    INF = float("inf")
    full = (1 << k) - 1
    dp = [[INF] * k for _ in range(1 << k)]  # dp[mask][i]: collected mask, standing on treasure i
    for i in range(k):
        dp[1 << i][i] = d[0][i + 1]
    for mask in range(1, full + 1):
        row = dp[mask]
        for i in range(k):
            cur = row[i]
            if cur == INF:
                continue
            di = d[i + 1]
            for j in range(k):
                if mask >> j & 1:
                    continue
                nxt = mask | 1 << j
                if cur + di[j + 1] < dp[nxt][j]:
                    dp[nxt][j] = cur + di[j + 1]
    print(min(dp[full]))


if __name__ == "__main__":
    main()
```
