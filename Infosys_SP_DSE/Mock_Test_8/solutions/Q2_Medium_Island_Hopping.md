# 🔹 Solution — Mock 8 · Q2: Island Hopping (0-1 BFS, Medium)

**Problem statement:** [Q2_Medium_Island_Hopping.md](../Q2_Medium_Island_Hopping.md) · judge your own code first with `python tools/judge/judge.py M8Q2 <your_file>.py`

## 🔹 Quick Breakdown

* **Difficulty Level:** Medium (Q2 slot)
* **Main Approach:** Shortest path where every move costs **0** (onto land) or **1** (into water). Use a **0-1 BFS**: a deque where 0-cost neighbours go to the **front** and 1-cost neighbours to the **back**. The deque then pops cells in non-decreasing distance, like Dijkstra without a heap.
* **Core Concept:** 0-1 BFS (shortest paths with edge weights in {0, 1})
* **When to Use This Pattern?** Grids or graphs where moves are "free" or "cost one": min walls to break, min direction changes, min cells to flip.
* **Mistakes to Avoid:**
  * Plain BFS counts steps, not swims.
  * Marking a cell "visited" when it is pushed: a later 0-cost route can still improve it. Relax with `dist[next] > dist[cur] + cost`.

## 🔹 Optimization Path

* **Brute Force:** repeat "relax every cell from its neighbours" until nothing changes (Bellman–Ford) — O((RC)²).
* **Dijkstra with a heap:** O(RC log RC).
* **Optimized Solution:** 0-1 BFS — O(RC).

## 🔹 Solution Breakdown

* **Optimal Approach:** `dist[S] = 0`; pop from the left; for each neighbour `cost = 1 if water else 0`; if it improves, `appendleft` for cost 0, `append` for cost 1.
* **Why This Works?** The deque always holds distances `d` (front) and `d + 1` (back) only, so cells leave it in non-decreasing distance order — the same invariant Dijkstra's heap provides.
* **Edge Cases Considered:**
  * `S` and `T` on the same island → 0.
  * Swimming through several water cells in a row costs one per cell.

## 🔹 Pattern Recognition

* **Belongs To:** Graph — Shortest Path (0-1 BFS)
* **Common Problems Using This:**
  * 1368. Minimum Cost to Make at Least One Valid Path in a Grid (in this repo)
  * 2290. Minimum Obstacle Removal to Reach Corner
  * 1631. Path With Minimum Effort (in this repo — Dijkstra variant)

## 🔹 Tricks & Patterns Used

* **Flatten the grid:** cell `(r, c)` → `r · C + c`; one flat `dist` list is faster than a 2-D list in Python.
* **Cost of a move = property of the cell you enter.**

## 🔹 Alternative Data Structures

* `heapq` Dijkstra — correct, a log factor slower.

## 🔹 Complexity Analysis

* **Time Complexity:** O(R · C)
* **Space Complexity:** O(R · C)

## 🔹 Code Snippet (Brute Force — partial score)

```python
import sys


def main() -> None:
    data = sys.stdin.read().split()
    rows, cols = int(data[0]), int(data[1])
    grid = data[2:2 + rows]
    inf = float("inf")
    dist = [[inf] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "S":
                dist[r][c] = 0
    changed = True
    while changed:  # Bellman-Ford: relax until stable
        changed = False
        for r in range(rows):
            for c in range(cols):
                cost = 1 if grid[r][c] == "~" else 0
                for pr, pc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                    if 0 <= pr < rows and 0 <= pc < cols and dist[pr][pc] + cost < dist[r][c]:
                        dist[r][c] = dist[pr][pc] + cost
                        changed = True
    print(next(dist[r][c] for r in range(rows) for c in range(cols) if grid[r][c] == "T"))


if __name__ == "__main__":
    main()
```

## 🔹 Code Snippet (Optimized)

```python
import sys
from collections import deque


def main() -> None:
    data = sys.stdin.read().split()
    rows, cols = int(data[0]), int(data[1])
    cells = "".join(data[2:2 + rows])
    start, target = cells.index("S"), cells.index("T")
    dist = [rows * cols] * (rows * cols)  # larger than any real distance
    dist[start] = 0
    queue = deque([start])
    while queue:
        cur = queue.popleft()
        if cur == target:
            break
        r, c = divmod(cur, cols)
        for nxt, ok in ((cur - cols, r > 0), (cur + cols, r < rows - 1), (cur - 1, c > 0), (cur + 1, c < cols - 1)):
            if not ok:
                continue
            cost = 1 if cells[nxt] == "~" else 0
            if dist[cur] + cost < dist[nxt]:
                dist[nxt] = dist[cur] + cost
                if cost:
                    queue.append(nxt)
                else:
                    queue.appendleft(nxt)
    print(dist[target])


if __name__ == "__main__":
    main()
```
