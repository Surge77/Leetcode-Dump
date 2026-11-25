# 🔹 Python Contest Template (Infosys SP / DSE)

**🟢 Status:** 🔄 Memorise — you should be able to type this from memory before the exam.

Infosys questions are full programs: you read raw input from **stdin** and print to **stdout** (no LeetCode-style `class Solution`). Every helper below is a building block that appears in this repo's solutions.

## 🔹 What Each Block Is For

| Block | Use it for | Practised in |
|---|---|---|
| `read_tokens` | Fast input — read everything once, split on whitespace | every mock test |
| `sieve`, `smallest_prime_factors`, `factorize` | Primes, prime factorisation, divisor counts | 204, 2521, Special Numbers |
| `mod_inv`, `Combinatorics.ncr` | Counting answers "mod 10⁹+7", binomials | 62, 1359, 1922 |
| `DSU` | Connectivity, components, Kruskal | 684, 1319, 1584 |
| `dijkstra`, `bfs_grid`, `topo_order` | Shortest paths, grids, dependencies | 743, 994, 207, Toll Pass |
| `iterative_dfs_order` | Tree DP without `RecursionError` | 124, 337, 968 |
| `Fenwick`, `SegTree` | Range sums / min / max with updates (commutative ops only) | 307, 315 |
| `SparseTable` | O(1) range min / max / gcd on a static array | Price Spread |
| `mat_pow` | Linear recurrences mod p with huge `n` | 935, 1220, Stair Climber |
| `strongly_connected_components` | SCCs + condensation order (Kosaraju, iterative) | Gold Roads |
| `first_true` | Binary search on the answer | 875, 410, Factory Output |
| `submasks` | Enumerating submasks (3ⁿ subset-partition DPs) | 1986 (alternative approach) |

## 🔹 Template

```python
import heapq
import sys
from collections import deque
from math import isqrt

MOD = 10**9 + 7
INF = float("inf")


# ---------------- input ----------------
def read_tokens():
    return sys.stdin.buffer.read().split()  # one read, then index into the list


# ---------------- number theory ----------------
def sieve(limit):
    """is_prime[x] (1/0) for x in 0..limit."""
    is_prime = bytearray([1]) * (limit + 1)
    is_prime[0] = 0
    if limit >= 1:
        is_prime[1] = 0
    for p in range(2, isqrt(limit) + 1):
        if is_prime[p]:
            is_prime[p * p::p] = bytes(len(range(p * p, limit + 1, p)))
    return is_prime


def smallest_prime_factors(limit):
    spf = list(range(limit + 1))
    for i in range(2, isqrt(limit) + 1):
        if spf[i] == i:
            for j in range(i * i, limit + 1, i):
                if spf[j] == j:
                    spf[j] = i
    return spf


def factorize(x, spf):
    """{prime: exponent} for x <= len(spf) - 1."""
    factors = {}
    while x > 1:
        p = spf[x]
        while x % p == 0:
            x //= p
            factors[p] = factors.get(p, 0) + 1
    return factors


def mod_inv(a, m=MOD):
    return pow(a, m - 2, m)  # Fermat's little theorem: m must be prime


class Combinatorics:
    def __init__(self, n, m=MOD):
        self.m = m
        self.fact = [1] * (n + 1)
        for i in range(1, n + 1):
            self.fact[i] = self.fact[i - 1] * i % m
        self.inv_fact = [1] * (n + 1)
        self.inv_fact[n] = pow(self.fact[n], m - 2, m)
        for i in range(n, 0, -1):
            self.inv_fact[i - 1] = self.inv_fact[i] * i % m

    def ncr(self, n, r):
        if r < 0 or r > n:
            return 0
        return self.fact[n] * self.inv_fact[r] % self.m * self.inv_fact[n - r] % self.m


# ---------------- union-find ----------------
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # path halving
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.components -= 1
        return True


# ---------------- graphs ----------------
def dijkstra(adj, src):
    """adj[u] = [(v, w), ...] with w >= 0; returns the distance list."""
    dist = [INF] * len(adj)
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))
    return dist


def bfs_grid(grid, sr, sc, wall="#"):
    """Steps from (sr, sc) to every cell; -1 = unreachable."""
    rows, cols = len(grid), len(grid[0])
    dist = [[-1] * cols for _ in range(rows)]
    dist[sr][sc] = 0
    q = deque([(sr, sc)])
    while q:
        i, j = q.popleft()
        for x, y in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= x < rows and 0 <= y < cols and grid[x][y] != wall and dist[x][y] == -1:
                dist[x][y] = dist[i][j] + 1
                q.append((x, y))
    return dist


def topo_order(n, adj):
    """Kahn's algorithm; [] if the graph has a cycle."""
    indeg = [0] * n
    for u in range(n):
        for v in adj[u]:
            indeg[v] += 1
    q = deque(u for u in range(n) if indeg[u] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == n else []


def iterative_dfs_order(adj, root):
    """(order, parent) without recursion; reversed(order) = children before parents."""
    parent = [-1] * len(adj)
    parent[root] = root
    order, stack = [], [root]
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if parent[v] == -1:
                parent[v] = u
                stack.append(v)
    parent[root] = -1
    return order, parent


# ---------------- range queries ----------------
class Fenwick:
    """1-indexed: add(i, delta), prefix(i) = sum of 1..i."""

    def __init__(self, n):
        self.tree = [0] * (n + 1)

    def add(self, i, delta):
        while i < len(self.tree):
            self.tree[i] += delta
            i += i & -i

    def prefix(self, i):
        total = 0
        while i > 0:
            total += self.tree[i]
            i -= i & -i
        return total

    def range_sum(self, l, r):
        return self.prefix(r) - self.prefix(l - 1)


class SegTree:
    """Iterative, 0-indexed, commutative op (sum, min, max, gcd, xor)."""

    def __init__(self, values, op, identity):
        self.n, self.op, self.identity = len(values), op, identity
        self.tree = [identity] * self.n + list(values)
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = op(self.tree[2 * i], self.tree[2 * i + 1])

    def update(self, i, value):
        i += self.n
        self.tree[i] = value
        while i > 1:
            i //= 2
            self.tree[i] = self.op(self.tree[2 * i], self.tree[2 * i + 1])

    def query(self, l, r):
        """op over values[l..r] inclusive."""
        res = self.identity
        l, r = l + self.n, r + self.n + 1
        while l < r:
            if l & 1:
                res = self.op(res, self.tree[l])
                l += 1
            if r & 1:
                r -= 1
                res = self.op(res, self.tree[r])
            l //= 2
            r //= 2
        return res


class SparseTable:
    """Static array, O(1) queries for idempotent ops (min, max, gcd)."""

    def __init__(self, values, op):
        self.op = op
        self.levels = [list(values)]
        j = 1
        while (1 << j) <= len(values):
            prev, half = self.levels[-1], 1 << (j - 1)
            self.levels.append([op(prev[i], prev[i + half]) for i in range(len(values) - (1 << j) + 1)])
            j += 1

    def query(self, l, r):
        """op over values[l..r] inclusive."""
        k = (r - l + 1).bit_length() - 1
        return self.op(self.levels[k][l], self.levels[k][r - (1 << k) + 1])


# ---------------- matrices ----------------
def mat_mult(a, b, m=MOD):
    size, inner = len(a), len(b)
    return [[sum(a[i][t] * b[t][j] for t in range(inner)) % m for j in range(len(b[0]))]
            for i in range(size)]


def mat_pow(mat, e, m=MOD):
    result = [[int(i == j) for j in range(len(mat))] for i in range(len(mat))]
    while e:
        if e & 1:
            result = mat_mult(result, mat, m)
        mat = mat_mult(mat, mat, m)
        e >>= 1
    return result


# ---------------- strongly connected components ----------------
def strongly_connected_components(n, adj):
    """comp[v] for every node; component ids follow a topological order of the condensation."""
    radj = [[] for _ in range(n)]
    for u in range(n):
        for v in adj[u]:
            radj[v].append(u)
    visited, order = [False] * n, []
    for root in range(n):
        if visited[root]:
            continue
        visited[root] = True
        stack = [(root, 0)]
        while stack:
            u, i = stack[-1]
            if i < len(adj[u]):
                stack[-1] = (u, i + 1)
                if not visited[adj[u][i]]:
                    visited[adj[u][i]] = True
                    stack.append((adj[u][i], 0))
            else:
                stack.pop()
                order.append(u)
    comp, count = [-1] * n, 0
    for root in reversed(order):
        if comp[root] != -1:
            continue
        comp[root] = count
        stack = [root]
        while stack:
            u = stack.pop()
            for v in radj[u]:
                if comp[v] == -1:
                    comp[v] = count
                    stack.append(v)
        count += 1
    return comp


# ---------------- binary search on answer ----------------
def first_true(lo, hi, ok):
    """Smallest x in [lo, hi] with ok(x); ok must be monotone and ok(hi) True."""
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


# ---------------- bitmasks ----------------
def submasks(mask):
    """Every submask of mask, including mask and 0."""
    sub = mask
    while True:
        yield sub
        if sub == 0:
            return
        sub = (sub - 1) & mask


# ---------------- solve ----------------
def solve(data):
    # Example only: first token N, then N integers -> their sum. Replace per problem.
    n = int(data[0])
    return str(sum(int(x) for x in data[1:1 + n]))


def main():
    sys.stdout.write(solve(read_tokens()) + "\n")


if __name__ == "__main__":
    main()
```

## 🔹 Deep Recursion Fallback

Python's default recursion limit is 1000. If a recursive DFS is much easier to write than the iterative one, run `main` in a thread with a bigger stack:

```python
import sys
import threading


def main():
    sys.setrecursionlimit(1 << 20)

    def depth(n):
        return 0 if n == 0 else 1 + depth(n - 1)

    print(depth(200000))  # far beyond the default limit of 1000


if __name__ == "__main__":
    threading.stack_size(1 << 27)  # 128 MB stack for the worker thread
    worker = threading.Thread(target=main)
    worker.start()
    worker.join()
```

## 🔹 Exam-Day Checklist

* Read the constraints first — they tell you the allowed complexity:

| Largest input | Aim for |
|---|---|
| N ≤ 12 | O(N!) or O(2ᴺ · N²) |
| N ≤ 20 | O(2ᴺ · N) |
| N ≤ 500 | O(N³) |
| N ≤ 5 000 | O(N²) |
| N ≤ 10⁵ – 10⁶ | O(N log N) or O(N) |
| N ≤ 10¹² – 10¹⁸ | O(√N), O(log N), digit DP, a formula |

* Take `% MOD` after **every** addition/multiplication in counting problems.
* Precompute (sieve, factorials) **once**, outside the query loop.
* Collect answers in a list and print once with `"\n".join(...)`.
* Test: smallest input, all-equal values, negatives, maximum values, unreachable / impossible cases.
