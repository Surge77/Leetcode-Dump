import heapq
import random
from collections import deque

from harness import case

R = random.Random(6)
INF = float("inf")


def dijkstra(n, adj, src):
    dist = [INF] * n
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


@case(994)
def _(h):
    S = h.lc(994)["Solution"]()
    assert S.orangesRotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4
    assert S.orangesRotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1 and S.orangesRotting([[0, 2]]) == 0
    for _ in range(300):
        m, n = R.randint(1, 5), R.randint(1, 5)
        g = [[R.choice((0, 1, 1, 2)) for _ in range(n)] for _ in range(m)]
        cur, minutes = [r[:] for r in g], 0
        while True:
            nxt = [r[:] for r in cur]
            changed = False
            for i in range(m):
                for j in range(n):
                    if cur[i][j] == 1 and any(0 <= i + a < m and 0 <= j + b < n and cur[i + a][j + b] == 2
                                              for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                        nxt[i][j], changed = 2, True
            if not changed:
                break
            cur, minutes = nxt, minutes + 1
        want = -1 if any(1 in r for r in cur) else minutes
        assert S.orangesRotting([r[:] for r in g]) == want, g


@case(542)
def _(h):
    S = h.lc(542)["Solution"]()
    for _ in range(300):
        m, n = R.randint(1, 6), R.randint(1, 6)
        g = [[R.randint(0, 1) for _ in range(n)] for _ in range(m)]
        g[R.randrange(m)][R.randrange(n)] = 0
        zeros = [(i, j) for i in range(m) for j in range(n) if g[i][j] == 0]
        want = [[min(abs(i - a) + abs(j - b) for a, b in zeros) for j in range(n)] for i in range(m)]
        assert S.updateMatrix([r[:] for r in g]) == want


@case(127)
def _(h):
    S = h.lc(127)["Solution"]()
    assert S.ladderLength("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]) == 5
    assert S.ladderLength("hit", "cog", ["hot", "dot", "dog", "lot", "log"]) == 0
    for _ in range(300):
        L = R.randint(1, 3)
        words = list({"".join(R.choice("abc") for _ in range(L)) for _ in range(R.randint(1, 12))})
        begin = "".join(R.choice("abc") for _ in range(L))
        end = R.choice(words)
        if begin == end:
            continue
        dist, q = {begin: 1}, deque([begin])
        while q:
            w = q.popleft()
            for v in words:
                if v not in dist and sum(a != b for a, b in zip(w, v)) == 1:
                    dist[v] = dist[w] + 1
                    q.append(v)
        assert S.ladderLength(begin, end, words[:]) == dist.get(end, 0), (begin, end, words)


@case(743)
def _(h):
    S = h.lc(743)["Solution"]()
    assert S.networkDelayTime([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2) == 2
    assert S.networkDelayTime([[1, 2, 1]], 2, 2) == -1
    for _ in range(300):
        n = R.randint(1, 6)
        times = [[R.randint(1, n), R.randint(1, n), R.randint(0, 9)] for _ in range(R.randint(0, 12))]
        times = [t for t in times if t[0] != t[1]]
        k = R.randint(1, n)
        adj = [[] for _ in range(n)]
        for u, v, w in times:
            adj[u - 1].append((v - 1, w))
        d = dijkstra(n, adj, k - 1)
        want = -1 if max(d) == INF else max(d)
        assert S.networkDelayTime(times, n, k) == want


@case(787)
def _(h):
    S = h.lc(787)["Solution"]()
    assert S.findCheapestPrice(4, [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], 0, 3, 1) == 700
    assert S.findCheapestPrice(3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1) == 200
    for _ in range(300):
        n = R.randint(2, 5)
        prices = {(R.randrange(n), R.randrange(n)): R.randint(1, 20) for _ in range(R.randint(1, 10))}
        flights = [[u, v, w] for (u, v), w in prices.items() if u != v]
        src, dst = R.sample(range(n), 2)
        k = R.randint(0, 3)
        best = INF

        def dfs(u, cost, edges):
            nonlocal best
            if u == dst:
                best = min(best, cost)
                return
            if edges == k + 1:
                return
            for a, b, w in flights:
                if a == u:
                    dfs(b, cost + w, edges + 1)
        dfs(src, 0, 0)
        assert S.findCheapestPrice(n, flights, src, dst, k) == (-1 if best == INF else best)


@case(1631)
def _(h):
    S = h.lc(1631)["Solution"]()
    assert S.minimumEffortPath([[1, 2, 2], [3, 8, 2], [5, 3, 5]]) == 2
    assert S.minimumEffortPath([[1, 2, 1, 1, 1], [1, 2, 1, 2, 1], [1, 2, 1, 2, 1], [1, 2, 1, 2, 1], [1, 1, 1, 2, 1]]) == 0
    for _ in range(300):
        m, n = R.randint(1, 5), R.randint(1, 5)
        g = [[R.randint(1, 9) for _ in range(n)] for _ in range(m)]

        def ok(t):
            seen, st = {(0, 0)}, [(0, 0)]
            while st:
                i, j = st.pop()
                for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    x, y = i + a, j + b
                    if 0 <= x < m and 0 <= y < n and (x, y) not in seen and abs(g[x][y] - g[i][j]) <= t:
                        seen.add((x, y))
                        st.append((x, y))
            return (m - 1, n - 1) in seen
        assert S.minimumEffortPath(g) == next(t for t in range(10) if ok(t))


@case(1368)
def _(h):
    S = h.lc(1368)["Solution"]()
    assert S.minCost([[1, 1, 1, 1], [2, 2, 2, 2], [1, 1, 1, 1], [2, 2, 2, 2]]) == 3
    assert S.minCost([[1, 1, 3], [3, 2, 2], [1, 1, 4]]) == 0 and S.minCost([[1, 2], [4, 3]]) == 1
    moves = {1: (0, 1), 2: (0, -1), 3: (1, 0), 4: (-1, 0)}
    for _ in range(300):
        m, n = R.randint(1, 5), R.randint(1, 5)
        g = [[R.randint(1, 4) for _ in range(n)] for _ in range(m)]
        adj = [[] for _ in range(m * n)]
        for i in range(m):
            for j in range(n):
                for sign, (a, b) in moves.items():
                    x, y = i + a, j + b
                    if 0 <= x < m and 0 <= y < n:
                        adj[i * n + j].append((x * n + y, 0 if g[i][j] == sign else 1))
        assert S.minCost(g) == dijkstra(m * n, adj, 0)[-1]


@case(1334)
def _(h):
    S = h.lc(1334)["Solution"]()
    assert S.findTheCity(4, [[0, 1, 3], [1, 2, 1], [1, 3, 4], [2, 3, 1]], 4) == 3
    assert S.findTheCity(5, [[0, 1, 2], [0, 4, 8], [1, 2, 3], [1, 4, 2], [2, 3, 1], [3, 4, 1]], 2) == 0
    for _ in range(300):
        n = R.randint(2, 6)
        pairs = {tuple(sorted(R.sample(range(n), 2))): R.randint(1, 9) for _ in range(R.randint(1, 10))}
        edges = [[u, v, w] for (u, v), w in pairs.items()]
        T = R.randint(1, 15)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))
        reach = [sum(1 for d in dijkstra(n, adj, s) if 0 < d <= T) for s in range(n)]
        want = max(i for i in range(n) if reach[i] == min(reach))
        assert S.findTheCity(n, edges, T) == want
