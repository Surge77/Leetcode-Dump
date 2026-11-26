"""Brute-force backfill bf09: graph traversals (542, 785, 886, 994) and greedy (134, 1920, 2094, 2918, 45, 502).

Each brute force is the first python block of its note; it is checked on LeetCode's examples and
against the optimized (last) block on random small inputs.
"""
import random

from harness import blocks_of, case, lc_path, ns_from

R = random.Random(909)


def pair(num):
    blocks = blocks_of(lc_path(num))
    return ns_from(blocks[0])["Solution"](), ns_from(blocks[-1])["Solution"]()


def grid(m, n, choices):
    return [[R.choice(choices) for _ in range(n)] for _ in range(m)]


def copy2d(g):
    return [row[:] for row in g]


def random_edges(n, lo, max_edges):
    if n < 2:
        return set()
    return {tuple(sorted(R.sample(range(lo, lo + n), 2))) for _ in range(R.randint(0, max_edges))}


@case("542-brute")
def _(h):
    brute, opt = pair(542)
    assert brute.updateMatrix([[0, 0, 0], [0, 1, 0], [0, 0, 0]]) == [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    assert brute.updateMatrix([[0, 0, 0], [0, 1, 0], [1, 1, 1]]) == [[0, 0, 0], [0, 1, 0], [1, 2, 1]]
    for _ in range(200):
        m, n = R.randint(1, 6), R.randint(1, 6)
        g = grid(m, n, (0, 1, 1))
        g[R.randrange(m)][R.randrange(n)] = 0
        assert brute.updateMatrix(copy2d(g)) == opt.updateMatrix(copy2d(g)), g


@case("785-brute")
def _(h):
    brute, opt = pair(785)
    assert brute.isBipartite([[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]]) is False
    assert brute.isBipartite([[1, 3], [0, 2], [1, 3], [0, 2]]) is True
    for _ in range(300):
        n = R.randint(1, 9)
        graph = [[] for _ in range(n)]
        for u, v in random_edges(n, 0, 10):
            graph[u].append(v)
            graph[v].append(u)
        assert brute.isBipartite(graph) == opt.isBipartite(graph), graph


@case("886-brute")
def _(h):
    brute, opt = pair(886)
    assert brute.possibleBipartition(4, [[1, 2], [1, 3], [2, 4]]) is True
    assert brute.possibleBipartition(3, [[1, 2], [1, 3], [2, 3]]) is False
    for _ in range(300):
        n = R.randint(1, 9)
        dislikes = [list(e) for e in random_edges(n, 1, 10)]
        assert brute.possibleBipartition(n, dislikes) == opt.possibleBipartition(n, dislikes), (n, dislikes)


@case("994-brute")
def _(h):
    brute, opt = pair(994)
    assert brute.orangesRotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4
    assert brute.orangesRotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1
    assert brute.orangesRotting([[0, 2]]) == 0
    for _ in range(300):
        g = grid(R.randint(1, 6), R.randint(1, 6), (0, 1, 1, 2))
        assert brute.orangesRotting(copy2d(g)) == opt.orangesRotting(copy2d(g)), g


@case("134-brute")
def _(h):
    brute, opt = pair(134)
    assert brute.canCompleteCircuit([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]) == 3
    assert brute.canCompleteCircuit([2, 3, 4], [3, 4, 3]) == -1
    for _ in range(400):
        n = R.randint(1, 8)
        gas = [R.randint(0, 5) for _ in range(n)]
        cost = [R.randint(0, 5) for _ in range(n)]
        b = brute.canCompleteCircuit(gas[:], cost[:])
        o = opt.canCompleteCircuit(gas[:], cost[:])
        # LeetCode guarantees a unique answer; with random data several starts may work, so validate instead.
        assert (b == -1) == (o == -1), (gas, cost)
        if b != -1:
            for s in (b, o):
                tank = 0
                for k in range(n):
                    tank += gas[(s + k) % n] - cost[(s + k) % n]
                    assert tank >= 0, (gas, cost, s)


@case("1920-brute")
def _(h):
    brute, opt = pair(1920)
    assert brute.buildArray([0, 2, 1, 5, 3, 4]) == [0, 1, 2, 4, 5, 3]
    assert brute.buildArray([5, 0, 1, 2, 3, 4]) == [4, 5, 0, 1, 2, 3]
    for _ in range(200):
        nums = list(range(R.randint(1, 15)))
        R.shuffle(nums)
        assert brute.buildArray(nums[:]) == opt.buildArray(nums[:]), nums


@case("2094-brute")
def _(h):
    brute, opt = pair(2094)
    assert brute.findEvenNumbers([2, 1, 3, 0]) == [102, 120, 130, 132, 210, 230, 302, 310, 312, 320]
    assert brute.findEvenNumbers([2, 2, 8, 8, 2]) == [222, 228, 282, 288, 822, 828, 882]
    assert brute.findEvenNumbers([3, 7, 5]) == []
    for _ in range(300):
        digits = [R.randint(0, 9) for _ in range(R.randint(3, 9))]
        assert brute.findEvenNumbers(digits[:]) == opt.findEvenNumbers(digits[:]), digits


@case("2918-brute")
def _(h):
    brute, opt = pair(2918)
    assert brute.minSum([3, 2, 0, 1, 0], [6, 5, 0]) == 12
    assert brute.minSum([2, 0, 2, 0], [1, 4]) == -1
    for _ in range(300):
        a = [R.choice((0, 0, 1, 2, 3, 5)) for _ in range(R.randint(1, 5))]
        b = [R.choice((0, 0, 1, 2, 3, 5)) for _ in range(R.randint(1, 5))]
        assert brute.minSum(a[:], b[:]) == opt.minSum(a[:], b[:]), (a, b)


@case("45-brute")
def _(h):
    brute, opt = pair(45)
    assert brute.jump([2, 3, 1, 1, 4]) == 2
    assert brute.jump([2, 3, 0, 1, 4]) == 2
    for _ in range(400):
        a = [R.randint(1, 4) for _ in range(R.randint(1, 12))]
        assert brute.jump(a[:]) == opt.jump(a[:]), a


@case("502-brute")
def _(h):
    brute, opt = pair(502)
    assert brute.findMaximizedCapital(2, 0, [1, 2, 3], [0, 1, 1]) == 4
    assert brute.findMaximizedCapital(3, 0, [1, 2, 3], [0, 1, 2]) == 6
    for _ in range(300):
        n = R.randint(1, 6)
        profits = [R.randint(0, 6) for _ in range(n)]
        capital = [R.randint(0, 6) for _ in range(n)]
        k, w = R.randint(1, n + 1), R.randint(0, 3)
        args = (k, w, profits, capital)
        assert brute.findMaximizedCapital(k, w, profits[:], capital[:]) == opt.findMaximizedCapital(*args), args
