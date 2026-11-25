# 🔹 Solution — Mock 10 · Q2: Club Merge (Union-Find with Sizes, Medium)

**Problem statement:** [Q2_Medium_Club_Merge.md](../Q2_Medium_Club_Merge.md) · judge your own code first with `python tools/judge/judge.py M10Q2 <your_file>.py`

## 🔹 Quick Breakdown

* **Difficulty Level:** Medium (Q2 slot)
* **Main Approach:** Clubs only ever **merge**, so keep them in a **disjoint-set union** (DSU) with component sizes. Each new friendship unites two sets; if they were different, the number of clubs drops by one and the merged size may become the new largest. The largest size never decreases, so a single running maximum suffices.
* **Core Concept:** incremental connectivity with union-find (path compression + union by size)
* **When to Use This Pattern?** Edges are only added and you need component counts / sizes after each addition.
* **Mistakes to Avoid:**
  * Re-running BFS after every friendship: O(M · (N + M)).
  * Decreasing the club count when both people are already in the same club.
  * Recursive `find` on a long chain — use the iterative version (or rely on union by size keeping trees shallow).

## 🔹 Optimization Path

* **Brute Force:** rebuild the components after each friendship — O(M · (N + M)).
* **Optimized Solution:** DSU — O((N + M) α(N)).

## 🔹 Solution Breakdown

* **Optimal Approach:** `parent[i] = i`, `size[i] = 1`, `clubs = N`, `largest = 1`. For each pair: find both roots; if different, attach the smaller under the larger, update `size`, `clubs -= 1`, `largest = max(largest, size[root])`; print `clubs largest`.
* **Why This Works?** Union-find maintains exactly the partition into connected components under edge insertions; union by size keeps every tree's height O(log N), and path compression flattens it further.
* **Edge Cases Considered:**
  * Repeated friendship between the same pair → output unchanged.
  * Once everyone is in one club, every remaining line is `1 N`.

## 🔹 Pattern Recognition

* **Belongs To:** Union-Find
* **Common Problems Using This:**
  * 1319. Number of Operations to Make Network Connected (in this repo)
  * 684. Redundant Connection (in this repo)
  * 305. Number of Islands II

## 🔹 Tricks & Patterns Used

* **Iterative find with path halving:** `parent[x] = parent[parent[x]]` while walking up.
* **Monotone running maximum** — merges never shrink a component.

## 🔹 Alternative Data Structures

* With deletions as well, you would need offline tricks (reverse the process) or a dynamic-connectivity structure.

## 🔹 Complexity Analysis

* **Time Complexity:** O((N + M) α(N))
* **Space Complexity:** O(N)

## 🔹 Code Snippet (Brute Force — partial score)

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    adj = [[] for _ in range(n + 1)]
    out = []
    for k in range(m):
        u, v = int(data[2 + 2 * k]), int(data[3 + 2 * k])
        adj[u].append(v)
        adj[v].append(u)
        seen, clubs, largest = [False] * (n + 1), 0, 0
        for s in range(1, n + 1):
            if seen[s]:
                continue
            clubs += 1
            seen[s], stack, size = True, [s], 0
            while stack:
                x = stack.pop()
                size += 1
                for y in adj[x]:
                    if not seen[y]:
                        seen[y] = True
                        stack.append(y)
            largest = max(largest, size)
        out.append(f"{clubs} {largest}")
    print("\n".join(out))


if __name__ == "__main__":
    main()
```

## 🔹 Code Snippet (Optimized)

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    parent, size = list(range(n + 1)), [1] * (n + 1)

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # path halving
            x = parent[x]
        return x

    clubs, largest, out = n, 1, []
    for k in range(m):
        a, b = find(int(data[2 + 2 * k])), find(int(data[3 + 2 * k]))
        if a != b:
            if size[a] < size[b]:
                a, b = b, a
            parent[b] = a  # attach the smaller club under the larger
            size[a] += size[b]
            clubs -= 1
            largest = max(largest, size[a])
        out.append(f"{clubs} {largest}")
    print("\n".join(out))


if __name__ == "__main__":
    main()
```
