"""Brute-force backfill bf07: each note's first python block (brute force) vs its last (optimized)."""
import random

from harness import blocks_of, case, lc_path, ns_from

R = random.Random(707)
TRIALS = 200


def pair(num):
    blocks = blocks_of(lc_path(num))
    brute, opt = ns_from(blocks[0]), ns_from(blocks[-1])
    return brute["Solution"](), opt["Solution"]()


@case("1649-brute")
def _(h):
    brute, opt = pair(1649)
    assert brute.createSortedArray([1, 5, 6, 2]) == 1
    assert brute.createSortedArray([1, 2, 3, 6, 5, 4]) == 3
    assert brute.createSortedArray([1, 3, 3, 3, 2, 4, 2, 1, 2]) == 4
    for _ in range(TRIALS):
        ins = [R.randint(1, 12) for _ in range(R.randint(1, 20))]
        assert brute.createSortedArray(ins[:]) == opt.createSortedArray(ins[:]), ins


@case("315-brute")
def _(h):
    brute, opt = pair(315)
    assert brute.countSmaller([5, 2, 6, 1]) == [2, 1, 1, 0]
    assert brute.countSmaller([-1]) == [0] and brute.countSmaller([-1, -1]) == [0, 0]
    for _ in range(TRIALS):
        a = [R.randint(-10, 10) for _ in range(R.randint(1, 20))]
        assert brute.countSmaller(a[:]) == opt.countSmaller(a[:]), a


@case("327-brute")
def _(h):
    brute, opt = pair(327)
    assert brute.countRangeSum([-2, 5, -1], -2, 2) == 3 and brute.countRangeSum([0], 0, 0) == 1
    for _ in range(TRIALS):
        a = [R.randint(-10, 10) for _ in range(R.randint(1, 15))]
        lo = R.randint(-15, 10)
        hi = lo + R.randint(0, 12)
        assert brute.countRangeSum(a[:], lo, hi) == opt.countRangeSum(a[:], lo, hi), (a, lo, hi)


@case("493-brute")
def _(h):
    brute, opt = pair(493)
    assert brute.reversePairs([1, 3, 2, 3, 1]) == 2 and brute.reversePairs([2, 4, 3, 5, 1]) == 3
    for _ in range(TRIALS):
        a = [R.randint(-20, 20) for _ in range(R.randint(1, 20))]
        assert brute.reversePairs(a[:]) == opt.reversePairs(a[:]), a


@case("1394-brute")
def _(h):
    brute, opt = pair(1394)
    assert brute.findLucky([2, 2, 3, 4]) == 2
    assert brute.findLucky([1, 2, 2, 3, 3, 3]) == 3
    assert brute.findLucky([2, 2, 2, 3, 3]) == -1
    for _ in range(TRIALS):
        a = [R.randint(1, 6) for _ in range(R.randint(1, 15))]
        assert brute.findLucky(a[:]) == opt.findLucky(a[:]), a


@case("383-brute")
def _(h):
    brute, opt = pair(383)
    assert brute.canConstruct("a", "b") is False
    assert brute.canConstruct("aa", "ab") is False
    assert brute.canConstruct("aa", "aab") is True
    for _ in range(TRIALS):
        note = "".join(R.choice("abc") for _ in range(R.randint(1, 6)))
        mag = "".join(R.choice("abc") for _ in range(R.randint(1, 8)))
        assert brute.canConstruct(note, mag) == opt.canConstruct(note, mag), (note, mag)


@case("1406-brute")
def _(h):
    brute, opt = pair(1406)
    assert brute.stoneGameIII([1, 2, 3, 7]) == "Bob"
    assert brute.stoneGameIII([1, 2, 3, -9]) == "Alice"
    assert brute.stoneGameIII([1, 2, 3, 6]) == "Tie"
    for _ in range(TRIALS):
        v = [R.randint(-5, 5) for _ in range(R.randint(1, 9))]
        assert brute.stoneGameIII(v[:]) == opt.stoneGameIII(v[:]), v


@case("292-brute")
def _(h):
    brute, opt = pair(292)
    assert brute.canWinNim(4) is False and brute.canWinNim(1) is True and brute.canWinNim(2) is True
    for n in range(1, 301):
        assert brute.canWinNim(n) == opt.canWinNim(n), n


@case("836-brute")
def _(h):
    brute, opt = pair(836)
    assert brute.isRectangleOverlap([0, 0, 2, 2], [1, 1, 3, 3]) is True
    assert brute.isRectangleOverlap([0, 0, 1, 1], [1, 0, 2, 1]) is False
    assert brute.isRectangleOverlap([0, 0, 1, 1], [2, 2, 3, 3]) is False
    assert brute.isRectangleOverlap([0, 1, 3, 2], [1, 0, 2, 3]) is True  # cross shape

    def rect():
        x1, y1 = R.randint(-5, 5), R.randint(-5, 5)
        return [x1, y1, x1 + R.randint(1, 5), y1 + R.randint(1, 5)]

    for _ in range(500):
        a, b = rect(), rect()
        assert brute.isRectangleOverlap(a, b) == opt.isRectangleOverlap(a, b), (a, b)


@case("1192-brute")
def _(h):
    brute, opt = pair(1192)
    assert sorted(map(sorted, brute.criticalConnections(4, [[0, 1], [1, 2], [2, 0], [1, 3]]))) == [[1, 3]]
    assert sorted(map(sorted, brute.criticalConnections(2, [[0, 1]]))) == [[0, 1]]
    for _ in range(TRIALS):
        n = R.randint(2, 9)
        edges = [[i, R.randrange(i)] for i in range(1, n)]
        edges += [R.sample(range(n), 2) for _ in range(R.randint(0, 5))]
        got = sorted(map(sorted, brute.criticalConnections(n, [e[:] for e in edges])))
        want = sorted(map(sorted, opt.criticalConnections(n, [e[:] for e in edges])))
        assert got == want, (n, edges)
