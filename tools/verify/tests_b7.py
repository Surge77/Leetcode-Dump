import random
from functools import lru_cache
from itertools import combinations

from harness import case, TreeNode

R = random.Random(7)


def reach_matrix(n, edges):
    r = [[False] * n for _ in range(n)]
    for u, v in edges:
        r[u][v] = True
    for k in range(n):
        for i in range(n):
            if r[i][k]:
                for j in range(n):
                    r[i][j] = r[i][j] or r[k][j]
    return r


def components(n, edges, skip=None):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x
    for idx, (u, v) in enumerate(edges):
        if idx != skip:
            parent[find(u)] = find(v)
    return len({find(i) for i in range(n)})


@case(207)
def _(h):
    S = h.lc(207)["Solution"]()
    assert S.canFinish(2, [[1, 0]]) and not S.canFinish(2, [[1, 0], [0, 1]])
    for _ in range(300):
        n = R.randint(1, 6)
        pre = [[R.randrange(n), R.randrange(n)] for _ in range(R.randint(0, 7))]
        pre = [p for p in pre if p[0] != p[1]]
        r = reach_matrix(n, [(b, a) for a, b in pre])
        assert S.canFinish(n, pre) == (not any(r[i][i] for i in range(n)))


@case(210)
def _(h):
    S = h.lc(210)["Solution"]()
    for _ in range(300):
        n = R.randint(1, 6)
        pre = [[R.randrange(n), R.randrange(n)] for _ in range(R.randint(0, 7))]
        pre = [p for p in pre if p[0] != p[1]]
        r = reach_matrix(n, [(b, a) for a, b in pre])
        order = S.findOrder(n, pre)
        if any(r[i][i] for i in range(n)):
            assert order == []
        else:
            pos = {c: i for i, c in enumerate(order)}
            assert sorted(order) == list(range(n)) and all(pos[b] < pos[a] for a, b in pre)


@case(1857)
def _(h):
    S = h.lc(1857)["Solution"]()
    assert S.largestPathValue("abaca", [[0, 1], [0, 2], [2, 3], [3, 4]]) == 3
    assert S.largestPathValue("a", [[0, 0]]) == -1
    for _ in range(300):
        n = R.randint(1, 6)
        colors = "".join(R.choice("ab") for _ in range(n))
        edges = list({(R.randrange(n), R.randrange(n)) for _ in range(R.randint(0, 7))})
        r = reach_matrix(n, edges)
        if any(r[i][i] for i in range(n)):
            want = -1
        else:
            adj = [[v for u, v in edges if u == x] for x in range(n)]

            @lru_cache(None)
            def best(u, c):
                return (colors[u] == c) + max([best(v, c) for v in adj[u]], default=0)
            want = max(best(u, c) for u in range(n) for c in "ab")
        assert S.largestPathValue(colors, [list(e) for e in edges]) == want, (colors, edges)


@case(684)
def _(h):
    S = h.lc(684)["Solution"]()
    assert S.findRedundantConnection([[1, 2], [1, 3], [2, 3]]) == [2, 3]
    assert S.findRedundantConnection([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]) == [1, 4]
    for _ in range(300):
        n = R.randint(3, 8)
        edges = [[i + 1, R.randint(1, i)] for i in range(1, n)]
        while True:
            u, v = R.sample(range(1, n + 1), 2)
            if [u, v] not in edges and [v, u] not in edges:
                break
        edges.insert(R.randint(0, len(edges)), [u, v])
        zero = [[a - 1, b - 1] for a, b in edges]
        want = next(edges[i] for i in range(len(edges) - 1, -1, -1) if components(n, zero, skip=i) == 1)
        assert S.findRedundantConnection([e[:] for e in edges]) == want


@case(1319)
def _(h):
    S = h.lc(1319)["Solution"]()
    assert S.makeConnected(4, [[0, 1], [0, 2], [1, 2]]) == 1
    assert S.makeConnected(6, [[0, 1], [0, 2], [0, 3], [1, 2]]) == -1
    for _ in range(300):
        n = R.randint(1, 8)
        conns = list({tuple(sorted(R.sample(range(n), 2))) for _ in range(R.randint(0, 9))}) if n > 1 else []
        want = -1 if len(conns) < n - 1 else components(n, conns) - 1
        assert S.makeConnected(n, [list(c) for c in conns]) == want


@case(1584)
def _(h):
    S = h.lc(1584)["Solution"]()
    assert S.minCostConnectPoints([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]) == 20
    for _ in range(200):
        pts = [[R.randint(-20, 20), R.randint(-20, 20)] for _ in range(R.randint(1, 12))]
        n = len(pts)
        in_tree, dist, total = [False] * n, [float("inf")] * n, 0
        dist[0] = 0
        for _ in range(n):
            u = min((d, i) for i, d in enumerate(dist) if not in_tree[i])[1]
            in_tree[u] = True
            total += dist[u]
            for v in range(n):
                if not in_tree[v]:
                    dist[v] = min(dist[v], abs(pts[u][0] - pts[v][0]) + abs(pts[u][1] - pts[v][1]))
        assert S.minCostConnectPoints(pts) == total


@case(1192)
def _(h):
    S = h.lc(1192)["Solution"]()
    assert sorted(map(sorted, S.criticalConnections(4, [[0, 1], [1, 2], [2, 0], [1, 3]]))) == [[1, 3]]
    for _ in range(300):
        n = R.randint(2, 8)
        edges = [[i, R.randrange(i)] for i in range(1, n)]
        edges += [R.sample(range(n), 2) for _ in range(R.randint(0, 4))]
        base = components(n, edges)
        want = sorted(sorted(e) for i, e in enumerate(edges) if components(n, edges, skip=i) > base)
        assert sorted(map(sorted, S.criticalConnections(n, [e[:] for e in edges]))) == want, edges
    big = [[i, i + 1] for i in range(99999)]
    assert len(S.criticalConnections(100000, big)) == 99999  # deep graph: iterative DFS


@case(1483)
def _(h):
    TreeAncestor = h.lc(1483)["TreeAncestor"]
    for _ in range(200):
        n = R.randint(1, 30)
        parent = [-1] + [R.randrange(i) for i in range(1, n)]
        obj = TreeAncestor(n, parent)
        for _ in range(30):
            node, k = R.randrange(n), R.randint(1, n)
            want = node
            for _ in range(k):
                want = parent[want] if want != -1 else -1
            assert obj.getKthAncestor(node, k) == want


def random_tree(n):
    nodes = [TreeNode(R.randint(-10, 10)) for _ in range(n)]
    par = {}
    for i in range(1, n):
        while True:
            p = R.randrange(i)
            side = R.choice(("left", "right"))
            if getattr(nodes[p], side) is None:
                setattr(nodes[p], side, nodes[i])
                par[i] = p
                break
    return nodes, par


def path(par, a):
    out = [a]
    while out[-1] in par:
        out.append(par[out[-1]])
    return out


@case(236)
def _(h):
    S = h.lc(236)["Solution"]()
    for _ in range(300):
        n = R.randint(1, 12)
        nodes, par = random_tree(n)
        a, b = R.randrange(n), R.randrange(n)
        pa = path(par, a)
        want = next(x for x in path(par, b) if x in pa)
        assert S.lowestCommonAncestor(nodes[0], nodes[a], nodes[b]) is nodes[want]


@case(124)
def _(h):
    S = h.lc(124)["Solution"]()
    assert S.maxPathSum(h.build_tree([1, 2, 3])) == 6
    assert S.maxPathSum(h.build_tree([-10, 9, 20, None, None, 15, 7])) == 42
    for _ in range(300):
        n = R.randint(1, 10)
        nodes, par = random_tree(n)
        best = -10**9
        for a, b in list(combinations(range(n), 2)) + [(i, i) for i in range(n)]:
            pa, pb = path(par, a), path(par, b)
            lca = next(x for x in pb if x in pa)
            seq = pa[:pa.index(lca) + 1] + pb[:pb.index(lca)]
            best = max(best, sum(nodes[i].val for i in seq))
        assert S.maxPathSum(nodes[0]) == best
    chain = TreeNode(1)
    cur = chain
    for _ in range(20000):
        cur.right = TreeNode(1)
        cur = cur.right
    assert S.maxPathSum(chain) == 20001
