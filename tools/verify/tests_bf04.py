"""Brute-force backfill bf04: each note's first python block (brute force) must agree with its
last python block (optimized) on LeetCode's examples and on random small inputs."""
import random

from harness import blocks_of, case, lc_path, ns_from

R = random.Random(404)
TRIALS = 150


def pair(num):
    blocks = blocks_of(lc_path(num))
    assert len(blocks) >= 2, f"{num}: expected brute + optimized blocks"
    return ns_from(blocks[0])["Solution"](), ns_from(blocks[-1])["Solution"]()


def rand_str(alphabet, lo, hi):
    return "".join(R.choice(alphabet) for _ in range(R.randint(lo, hi)))


def rand_grid(lo, hi, max_side):
    m, n = R.randint(1, max_side), R.randint(1, max_side)
    return [[R.randint(lo, hi) for _ in range(n)] for _ in range(m)]


@case("70-brute")
def _(h):
    brute, opt = pair(70)
    assert brute.climbStairs(2) == 2 and brute.climbStairs(3) == 3
    for n in range(1, 46):
        assert brute.climbStairs(n) == opt.climbStairs(n), n


@case("1143-brute")
def _(h):
    brute, opt = pair(1143)
    assert brute.longestCommonSubsequence("abcde", "ace") == 3
    assert brute.longestCommonSubsequence("abc", "abc") == 3
    assert brute.longestCommonSubsequence("abc", "def") == 0
    for _ in range(TRIALS):
        a, b = rand_str("abc", 1, 8), rand_str("abc", 1, 8)
        assert brute.longestCommonSubsequence(a, b) == opt.longestCommonSubsequence(a, b), (a, b)


@case("115-brute")
def _(h):
    brute, opt = pair(115)
    assert brute.numDistinct("rabbbit", "rabbit") == 3
    assert brute.numDistinct("babgbag", "bag") == 5
    for _ in range(TRIALS):
        s, t = rand_str("ab", 1, 10), rand_str("ab", 1, 4)
        assert brute.numDistinct(s, t) == opt.numDistinct(s, t), (s, t)


@case("329-brute")
def _(h):
    brute, opt = pair(329)
    assert brute.longestIncreasingPath([[9, 9, 4], [6, 6, 8], [2, 1, 1]]) == 4
    assert brute.longestIncreasingPath([[3, 4, 5], [3, 2, 6], [2, 2, 1]]) == 4
    assert brute.longestIncreasingPath([[1]]) == 1
    for _ in range(TRIALS):
        g = rand_grid(0, 6, 4)
        assert brute.longestIncreasingPath([r[:] for r in g]) == opt.longestIncreasingPath([r[:] for r in g]), g


@case("62-brute")
def _(h):
    brute, opt = pair(62)
    assert brute.uniquePaths(3, 7) == 28 and brute.uniquePaths(3, 2) == 3
    for _ in range(TRIALS):
        m, n = R.randint(1, 7), R.randint(1, 7)
        assert brute.uniquePaths(m, n) == opt.uniquePaths(m, n), (m, n)


@case("64-brute")
def _(h):
    brute, opt = pair(64)
    assert brute.minPathSum([[1, 3, 1], [1, 5, 1], [4, 2, 1]]) == 7
    assert brute.minPathSum([[1, 2, 3], [4, 5, 6]]) == 12
    for _ in range(TRIALS):
        g = rand_grid(0, 9, 5)
        assert brute.minPathSum([r[:] for r in g]) == opt.minPathSum([r[:] for r in g]), g


@case("72-brute")
def _(h):
    brute, opt = pair(72)
    assert brute.minDistance("horse", "ros") == 3
    assert brute.minDistance("intention", "execution") == 5
    for _ in range(TRIALS):
        a, b = rand_str("ab", 0, 6), rand_str("abc", 0, 6)
        assert brute.minDistance(a, b) == opt.minDistance(a, b), (a, b)


@case("312-brute")
def _(h):
    brute, opt = pair(312)
    assert brute.maxCoins([3, 1, 5, 8]) == 167 and brute.maxCoins([1, 5]) == 10
    for _ in range(TRIALS):
        a = [R.randint(0, 6) for _ in range(R.randint(1, 6))]
        assert brute.maxCoins(a[:]) == opt.maxCoins(a[:]), a


@case("516-brute")
def _(h):
    brute, opt = pair(516)
    assert brute.longestPalindromeSubseq("bbbab") == 4 and brute.longestPalindromeSubseq("cbbd") == 2
    for _ in range(TRIALS):
        s = rand_str("abc", 1, 10)
        assert brute.longestPalindromeSubseq(s) == opt.longestPalindromeSubseq(s), s


@case("1155-brute")
def _(h):
    brute, opt = pair(1155)
    assert brute.numRollsToTarget(1, 6, 3) == 1 and brute.numRollsToTarget(2, 6, 7) == 6
    for _ in range(TRIALS):
        n, k, t = R.randint(1, 4), R.randint(1, 6), R.randint(1, 24)
        assert brute.numRollsToTarget(n, k, t) == opt.numRollsToTarget(n, k, t), (n, k, t)
