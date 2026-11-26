"""Brute-force backfill bf03: each note's first python block (brute force) vs its last (optimized)."""
import random

from harness import blocks_of, case, lc_path, ns_from


def pair(num):
    blocks = blocks_of(lc_path(num))
    assert len(blocks) >= 2, num
    return ns_from(blocks[0])["Solution"](), ns_from(blocks[-1])["Solution"]()


@case("152-brute")
def _(h):
    brute, opt = pair(152)
    assert brute.maxProduct([2, 3, -2, 4]) == 6 and brute.maxProduct([-2, 0, -1]) == 0
    r = random.Random(1520)
    for _ in range(300):
        a = [r.randint(-4, 4) for _ in range(r.randint(1, 10))]
        assert brute.maxProduct(a[:]) == opt.maxProduct(a[:]), a


@case("309-brute")
def _(h):
    brute, opt = pair(309)
    assert brute.maxProfit([1, 2, 3, 0, 2]) == 3 and brute.maxProfit([1]) == 0
    r = random.Random(3090)
    for _ in range(300):
        p = [r.randint(0, 10) for _ in range(r.randint(1, 10))]
        assert brute.maxProfit(p[:]) == opt.maxProfit(p[:]), p


@case("3335-brute")
def _(h):
    brute, opt = pair(3335)
    assert brute.lengthAfterTransformations("abcyy", 2) == 7
    assert brute.lengthAfterTransformations("azbk", 1) == 5
    r = random.Random(33350)
    for _ in range(200):
        s = "".join(r.choice("abcxyz") for _ in range(r.randint(1, 6)))
        t = r.randint(0, 60)
        assert brute.lengthAfterTransformations(s, t) == opt.lengthAfterTransformations(s, t), (s, t)


@case("53-brute")
def _(h):
    brute, opt = pair(53)
    assert brute.maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert brute.maxSubArray([1]) == 1 and brute.maxSubArray([5, 4, -1, 7, 8]) == 23
    r = random.Random(530)
    for _ in range(300):
        a = [r.randint(-9, 9) for _ in range(r.randint(1, 15))]
        assert brute.maxSubArray(a[:]) == opt.maxSubArray(a[:]), a


@case("1986-brute")
def _(h):
    brute, opt = pair(1986)
    assert brute.minSessions([1, 2, 3], 3) == 2
    assert brute.minSessions([3, 1, 3, 1, 1], 8) == 2
    assert brute.minSessions([1, 2, 3, 4, 5], 15) == 1
    r = random.Random(19860)
    for _ in range(200):
        T = r.randint(1, 12)
        tasks = [r.randint(1, T) for _ in range(r.randint(1, 8))]
        assert brute.minSessions(tasks[:], T) == opt.minSessions(tasks[:], T), (tasks, T)


@case("698-brute")
def _(h):
    brute, opt = pair(698)
    assert brute.canPartitionKSubsets([4, 3, 2, 3, 5, 2, 1], 4)
    assert not brute.canPartitionKSubsets([1, 2, 3, 4], 3)
    r = random.Random(6980)
    for _ in range(300):
        a = [r.randint(1, 6) for _ in range(r.randint(1, 7))]
        k = r.randint(1, min(3, len(a)))
        assert brute.canPartitionKSubsets(a[:], k) == opt.canPartitionKSubsets(a[:], k), (a, k)


@case("847-brute")
def _(h):
    brute, opt = pair(847)
    assert brute.shortestPathLength([[1, 2, 3], [0], [0], [0]]) == 4
    assert brute.shortestPathLength([[1], [0, 2, 4], [1, 3, 4], [2], [1, 2]]) == 4
    r = random.Random(8470)
    for _ in range(150):
        n = r.randint(1, 7)
        edges = {(r.randrange(i), i) for i in range(1, n)}  # spanning tree keeps it connected
        if n > 1:
            edges |= {tuple(sorted(r.sample(range(n), 2))) for _ in range(r.randint(0, 5))}
        g = [[] for _ in range(n)]
        for u, v in edges:
            if v not in g[u]:
                g[u].append(v)
                g[v].append(u)
        assert brute.shortestPathLength(g) == opt.shortestPathLength(g), g


@case("233-brute")
def _(h):
    brute, opt = pair(233)
    assert brute.countDigitOne(13) == 6 and brute.countDigitOne(0) == 0
    r = random.Random(2330)
    for _ in range(150):
        n = r.randint(0, 5000)
        assert brute.countDigitOne(n) == opt.countDigitOne(n), n


@case("902-brute")
def _(h):
    brute, opt = pair(902)
    assert brute.atMostNGivenDigitSet(["1", "3", "5", "7"], 100) == 20
    assert brute.atMostNGivenDigitSet(["7"], 8) == 1
    r = random.Random(9020)
    for _ in range(150):
        ds = sorted(r.sample("123456789", r.randint(1, 5)))
        n = r.randint(1, 5000)
        assert brute.atMostNGivenDigitSet(ds[:], n) == opt.atMostNGivenDigitSet(ds[:], n), (ds, n)


@case("198-brute")
def _(h):
    brute, opt = pair(198)
    assert brute.rob([1, 2, 3, 1]) == 4 and brute.rob([2, 7, 9, 3, 1]) == 12
    r = random.Random(1980)
    for _ in range(300):
        a = [r.randint(0, 20) for _ in range(r.randint(1, 12))]
        assert brute.rob(a[:]) == opt.rob(a[:]), a
