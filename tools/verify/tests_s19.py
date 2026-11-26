"""Grid and string DP: regex matching, obstacle paths, interleaving, triangle, stock III/IV, maximal square.

Each note has a brute force and an optimized block; both must agree on random inputs and on
LeetCode's examples, and the optimized one is run once at max constraints.
"""
import random
import re

from harness import case
from tests_b10 import timed_call

R = random.Random(1919)


def both(h, num):
    brute, opt = h.lc_all(num, "Solution")
    return brute["Solution"](), opt["Solution"]()


def random_pattern(max_tokens):
    out = []
    for _ in range(R.randint(1, max_tokens)):
        out.append(R.choice("ab."))
        if R.random() < 0.4:
            out.append("*")
    return "".join(out)


@case(10)
def _(h):
    brute, opt = both(h, 10)
    assert opt.isMatch("aa", "a") is False
    assert opt.isMatch("aa", "a*") is True
    assert opt.isMatch("ab", ".*") is True
    assert opt.isMatch("", "a*b*") is True
    for _ in range(400):
        s = "".join(R.choice("ab") for _ in range(R.randint(1, 8)))
        p = random_pattern(6)
        expected = re.fullmatch(p, s) is not None
        assert brute.isMatch(s, p) == expected == opt.isMatch(s, p), (s, p)
    timed_call(lambda: opt.isMatch("a" * 20, "a*" * 9 + "b"), 1)


@case(63)
def _(h):
    brute, opt = both(h, 63)
    assert opt.uniquePathsWithObstacles([[0, 0, 0], [0, 1, 0], [0, 0, 0]]) == 2
    assert opt.uniquePathsWithObstacles([[0, 1], [0, 0]]) == 1
    assert opt.uniquePathsWithObstacles([[1]]) == 0
    for _ in range(300):
        m, n = R.randint(1, 6), R.randint(1, 6)
        grid = [[int(R.random() < 0.2) for _ in range(n)] for _ in range(m)]
        assert brute.uniquePathsWithObstacles(grid) == opt.uniquePathsWithObstacles(grid), grid
    big = [[0] * 100 for _ in range(100)]
    for _ in range(300):
        big[R.randrange(100)][R.randrange(100)] = 1
    big[0][0] = big[99][99] = 0
    timed_call(lambda: opt.uniquePathsWithObstacles(big), 1)


@case(97)
def _(h):
    brute, opt = both(h, 97)
    assert opt.isInterleave("aabcc", "dbbca", "aadbbcbcac") is True
    assert opt.isInterleave("aabcc", "dbbca", "aadbbbaccc") is False
    assert opt.isInterleave("", "", "") is True
    assert opt.isInterleave("a", "", "aa") is False
    for _ in range(400):
        s1 = "".join(R.choice("ab") for _ in range(R.randint(0, 6)))
        s2 = "".join(R.choice("ab") for _ in range(R.randint(0, 6)))
        if R.random() < 0.5:
            merged, i, j = [], 0, 0
            while i < len(s1) or j < len(s2):
                if j == len(s2) or (i < len(s1) and R.random() < 0.5):
                    merged.append(s1[i]); i += 1
                else:
                    merged.append(s2[j]); j += 1
            s3 = "".join(merged)
        else:
            s3 = "".join(R.choice("ab") for _ in range(len(s1) + len(s2) + R.choice((0, 0, 1))))
        assert brute.isInterleave(s1, s2, s3) == opt.isInterleave(s1, s2, s3), (s1, s2, s3)
    a, b = "ab" * 50, "ba" * 50
    timed_call(lambda: opt.isInterleave(a, b, "ab" * 100), 1)


@case(120)
def _(h):
    brute, opt = both(h, 120)
    assert opt.minimumTotal([[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]) == 11
    assert opt.minimumTotal([[-10]]) == -10
    for _ in range(300):
        n = R.randint(1, 10)
        tri = [[R.randint(-20, 20) for _ in range(r + 1)] for r in range(n)]
        snapshot = [row[:] for row in tri]
        assert brute.minimumTotal(tri) == opt.minimumTotal(tri), tri
        assert tri == snapshot
    big = [[R.randint(-10 ** 4, 10 ** 4) for _ in range(r + 1)] for r in range(200)]
    timed_call(lambda: opt.minimumTotal(big), 1)


@case(123)
def _(h):
    brute, opt = both(h, 123)
    assert opt.maxProfit([3, 3, 5, 0, 0, 3, 1, 4]) == 6
    assert opt.maxProfit([1, 2, 3, 4, 5]) == 4
    assert opt.maxProfit([7, 6, 4, 3, 1]) == 0
    assert opt.maxProfit([5]) == 0
    k2 = h.lc_all(188, "Solution")[1]["Solution"]()
    for _ in range(400):
        prices = [R.randint(0, 15) for _ in range(R.randint(1, 12))]
        got = opt.maxProfit(prices)
        assert brute.maxProfit(prices) == got == k2.maxProfit(2, prices), prices
    big = [R.randint(0, 10 ** 5) for _ in range(10 ** 5)]
    timed_call(lambda: opt.maxProfit(big), 2)


@case(188)
def _(h):
    brute, opt = both(h, 188)
    assert opt.maxProfit(2, [2, 4, 1]) == 2
    assert opt.maxProfit(2, [3, 2, 6, 5, 0, 3]) == 7
    assert opt.maxProfit(1, [1]) == 0
    for _ in range(300):
        prices = [R.randint(0, 12) for _ in range(R.randint(1, 10))]
        k = R.randint(1, 6)
        assert brute.maxProfit(k, prices) == opt.maxProfit(k, prices), (k, prices)
    big = [R.randint(0, 1000) for _ in range(1000)]
    assert opt.maxProfit(100, big) <= opt.maxProfit(500, big)
    timed_call(lambda: opt.maxProfit(100, big), 2)


@case(221)
def _(h):
    brute, opt = both(h, 221)
    ex = [["1", "0", "1", "0", "0"], ["1", "0", "1", "1", "1"],
          ["1", "1", "1", "1", "1"], ["1", "0", "0", "1", "0"]]
    assert opt.maximalSquare(ex) == 4
    assert opt.maximalSquare([["0", "1"], ["1", "0"]]) == 1
    assert opt.maximalSquare([["0"]]) == 0
    for _ in range(300):
        m, n = R.randint(1, 7), R.randint(1, 7)
        density = R.choice((0.5, 0.8, 0.95))
        grid = [["1" if R.random() < density else "0" for _ in range(n)] for _ in range(m)]
        assert brute.maximalSquare(grid) == opt.maximalSquare(grid), grid
    full = [["1"] * 300 for _ in range(300)]
    assert opt.maximalSquare(full) == 90_000
    timed_call(lambda: opt.maximalSquare(full), 2)
