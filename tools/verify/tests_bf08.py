"""Brute-force backfill bf08: graph shortest path, topological sort, traversals.

Each brute force (first python block) is checked on LeetCode's examples and against the optimized
solution (last python block) on small random inputs.
"""
import random

from harness import blocks_of, case, lc_path, ns_from

R = random.Random(808)


def pair(num):
    blocks = blocks_of(lc_path(num))
    return ns_from(blocks[0])["Solution"](), ns_from(blocks[-1])["Solution"]()


@case("1334-brute")
def _(h):
    brute, opt = pair(1334)
    assert brute.findTheCity(4, [[0, 1, 3], [1, 2, 1], [1, 3, 4], [2, 3, 1]], 4) == 3
    assert brute.findTheCity(5, [[0, 1, 2], [0, 4, 8], [1, 2, 3], [1, 4, 2], [2, 3, 1], [3, 4, 1]], 2) == 0
    for _ in range(300):
        n = R.randint(2, 6)
        pairs = {tuple(sorted(R.sample(range(n), 2))): R.randint(1, 9) for _ in range(R.randint(1, 10))}
        edges = [[u, v, w] for (u, v), w in pairs.items()]
        t = R.randint(1, 15)
        assert brute.findTheCity(n, edges, t) == opt.findTheCity(n, edges, t), (n, edges, t)


@case("1368-brute")
def _(h):
    brute, opt = pair(1368)
    assert brute.minCost([[1, 1, 1, 1], [2, 2, 2, 2], [1, 1, 1, 1], [2, 2, 2, 2]]) == 3
    assert brute.minCost([[1, 1, 3], [3, 2, 2], [1, 1, 4]]) == 0
    assert brute.minCost([[1, 2], [4, 3]]) == 1
    for _ in range(200):
        m, n = R.randint(1, 3), R.randint(1, 3)
        g = [[R.randint(1, 4) for _ in range(n)] for _ in range(m)]
        assert brute.minCost([r[:] for r in g]) == opt.minCost([r[:] for r in g]), g


@case("1631-brute")
def _(h):
    brute, opt = pair(1631)
    assert brute.minimumEffortPath([[1, 2, 2], [3, 8, 2], [5, 3, 5]]) == 2
    assert brute.minimumEffortPath([[1, 2, 3], [3, 8, 4], [5, 3, 5]]) == 1
    assert brute.minimumEffortPath([[1, 2, 1, 1, 1], [1, 2, 1, 2, 1], [1, 2, 1, 2, 1], [1, 2, 1, 2, 1], [1, 1, 1, 2, 1]]) == 0
    for _ in range(200):
        m, n = R.randint(1, 4), R.randint(1, 4)
        g = [[R.randint(1, 9) for _ in range(n)] for _ in range(m)]
        assert brute.minimumEffortPath(g) == opt.minimumEffortPath(g), g


@case("743-brute")
def _(h):
    brute, opt = pair(743)
    assert brute.networkDelayTime([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2) == 2
    assert brute.networkDelayTime([[1, 2, 1]], 2, 1) == 1
    assert brute.networkDelayTime([[1, 2, 1]], 2, 2) == -1
    for _ in range(300):
        n = R.randint(1, 6)
        times = [[R.randint(1, n), R.randint(1, n), R.randint(0, 9)] for _ in range(R.randint(0, 12))]
        times = [t for t in times if t[0] != t[1]]
        k = R.randint(1, n)
        assert brute.networkDelayTime(times, n, k) == opt.networkDelayTime(times, n, k), (times, n, k)


@case("787-brute")
def _(h):
    brute, opt = pair(787)
    assert brute.findCheapestPrice(4, [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], 0, 3, 1) == 700
    assert brute.findCheapestPrice(3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1) == 200
    assert brute.findCheapestPrice(3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0) == 500
    for _ in range(300):
        n = R.randint(2, 5)
        prices = {(R.randrange(n), R.randrange(n)): R.randint(1, 20) for _ in range(R.randint(1, 10))}
        flights = [[u, v, w] for (u, v), w in prices.items() if u != v]
        src, dst = R.sample(range(n), 2)
        k = R.randint(0, 3)
        assert brute.findCheapestPrice(n, flights, src, dst, k) == opt.findCheapestPrice(n, flights, src, dst, k)


@case("1857-brute")
def _(h):
    brute, opt = pair(1857)
    assert brute.largestPathValue("abaca", [[0, 1], [0, 2], [2, 3], [3, 4]]) == 3
    assert brute.largestPathValue("a", [[0, 0]]) == -1
    for _ in range(300):
        n = R.randint(1, 7)
        colors = "".join(R.choice("abc") for _ in range(n))
        edges = [list(e) for e in {(R.randrange(n), R.randrange(n)) for _ in range(R.randint(0, 9))}]
        assert brute.largestPathValue(colors, edges) == opt.largestPathValue(colors, edges), (colors, edges)


def random_prereqs(n):
    pre = [[R.randrange(n), R.randrange(n)] for _ in range(R.randint(0, 7))]
    return [p for p in pre if p[0] != p[1]]


@case("207-brute")
def _(h):
    brute, opt = pair(207)
    assert brute.canFinish(2, [[1, 0]]) is True
    assert brute.canFinish(2, [[1, 0], [0, 1]]) is False
    for _ in range(300):
        n = R.randint(1, 6)
        pre = random_prereqs(n)
        assert brute.canFinish(n, pre) == opt.canFinish(n, pre), (n, pre)


@case("210-brute")
def _(h):
    brute, opt = pair(210)

    def valid(n, pre, order):
        pos = {c: i for i, c in enumerate(order)}
        return sorted(order) == list(range(n)) and all(pos[b] < pos[a] for a, b in pre)

    pre = [[1, 0], [2, 0], [3, 1], [3, 2]]
    assert valid(4, pre, brute.findOrder(4, pre))
    assert brute.findOrder(2, [[1, 0]]) == [0, 1]
    assert brute.findOrder(1, []) == [0]
    for _ in range(300):
        n = R.randint(1, 6)
        pre = random_prereqs(n)
        got, want = brute.findOrder(n, pre), opt.findOrder(n, pre)
        if want == []:
            assert got == [], (n, pre)
        else:
            assert valid(n, pre, got), (n, pre, got)


@case("127-brute")
def _(h):
    brute, opt = pair(127)
    assert brute.ladderLength("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]) == 5
    assert brute.ladderLength("hit", "cog", ["hot", "dot", "dog", "lot", "log"]) == 0
    for _ in range(300):
        length = R.randint(1, 3)
        words = list({"".join(R.choice("abc") for _ in range(length)) for _ in range(R.randint(1, 12))})
        begin = "".join(R.choice("abc") for _ in range(length))
        end = R.choice(words)
        if begin == end:
            continue
        assert brute.ladderLength(begin, end, words[:]) == opt.ladderLength(begin, end, words[:]), (begin, end, words)


@case("200-brute")
def _(h):
    brute, opt = pair(200)
    g1 = [["1", "1", "1", "1", "0"], ["1", "1", "0", "1", "0"], ["1", "1", "0", "0", "0"], ["0", "0", "0", "0", "0"]]
    g2 = [["1", "1", "0", "0", "0"], ["1", "1", "0", "0", "0"], ["0", "0", "1", "0", "0"], ["0", "0", "0", "1", "1"]]
    assert brute.numIslands(g1) == 1 and brute.numIslands(g2) == 3
    for _ in range(300):
        m, n = R.randint(1, 6), R.randint(1, 6)
        g = [[R.choice("01") for _ in range(n)] for _ in range(m)]
        assert brute.numIslands([r[:] for r in g]) == opt.numIslands([r[:] for r in g]), g
