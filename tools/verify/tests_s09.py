"""Sheet coverage s09: Kadane circular, grid DP, partition DP, LIS on strings, LCS reconstruction, interval DP.

Each note has a brute force and an optimized block; both must agree on random inputs and on
LeetCode's examples, and the optimized one is run once at max constraints.
"""
import random

from harness import case
from tests_b10 import timed_call

R = random.Random(909)


def both(h, num):
    brute, opt = h.lc_all(num, "Solution")
    return brute["Solution"](), opt["Solution"]()


def is_subsequence(small, big):
    it = iter(big)
    return all(ch in it for ch in small)


@case(918)
def _(h):
    brute, opt = both(h, 918)
    assert opt.maxSubarraySumCircular([1, -2, 3, -2]) == 3
    assert opt.maxSubarraySumCircular([5, -3, 5]) == 10
    assert opt.maxSubarraySumCircular([-3, -2, -3]) == -2
    for _ in range(400):
        nums = [R.randint(-10, 10) for _ in range(R.randint(1, 10))]
        assert brute.maxSubarraySumCircular(nums) == opt.maxSubarraySumCircular(nums), nums
    big = [R.randint(-30_000, 30_000) for _ in range(30_000)]
    timed_call(lambda: opt.maxSubarraySumCircular(big), 1)


@case(931)
def _(h):
    brute, opt = both(h, 931)
    assert opt.minFallingPathSum([[2, 1, 3], [6, 5, 4], [7, 8, 9]]) == 13
    assert opt.minFallingPathSum([[-19, 57], [-40, -5]]) == -59
    for _ in range(200):
        n = R.randint(1, 6)
        matrix = [[R.randint(-100, 100) for _ in range(n)] for _ in range(n)]
        assert brute.minFallingPathSum(matrix) == opt.minFallingPathSum(matrix), matrix
    big = [[R.randint(-100, 100) for _ in range(100)] for _ in range(100)]
    timed_call(lambda: opt.minFallingPathSum(big), 1)


@case(1043)
def _(h):
    brute, opt = both(h, 1043)
    assert opt.maxSumAfterPartitioning([1, 15, 7, 9, 2, 5, 10], 3) == 84
    assert opt.maxSumAfterPartitioning([1, 4, 1, 5, 7, 3, 6, 1, 9, 9, 3], 4) == 83
    assert opt.maxSumAfterPartitioning([1], 1) == 1
    for _ in range(300):
        arr = [R.randint(0, 20) for _ in range(R.randint(1, 10))]
        k = R.randint(1, len(arr))
        assert brute.maxSumAfterPartitioning(arr, k) == opt.maxSumAfterPartitioning(arr, k), (arr, k)
    big = [R.randint(0, 10**9) for _ in range(500)]
    timed_call(lambda: opt.maxSumAfterPartitioning(big, 500), 2)


@case(1048)
def _(h):
    brute, opt = both(h, 1048)
    assert opt.longestStrChain(["a", "b", "ba", "bca", "bda", "bdca"]) == 4
    assert opt.longestStrChain(["xbc", "pcxbcf", "xb", "cxbc", "pcxbc"]) == 5
    assert opt.longestStrChain(["abcd", "dbqca"]) == 1
    for _ in range(300):
        words = list({"".join(R.choice("ab") for _ in range(R.randint(1, 5))) for _ in range(R.randint(1, 15))})
        R.shuffle(words)
        assert brute.longestStrChain(words) == opt.longestStrChain(words), words
    big = list({"".join(R.choice("abc") for _ in range(R.randint(1, 16))) for _ in range(1000)})
    timed_call(lambda: opt.longestStrChain(big), 1)


@case(1092)
def _(h):
    brute, opt = both(h, 1092)

    def check(a, b, expected_len):
        got = opt.shortestCommonSupersequence(a, b)
        assert len(got) == expected_len and is_subsequence(a, got) and is_subsequence(b, got), (a, b, got)

    check("abac", "cab", 5)
    assert opt.shortestCommonSupersequence("aaaaaaaa", "aaaaaaaa") == "aaaaaaaa"
    for _ in range(300):
        a = "".join(R.choice("abc") for _ in range(R.randint(1, 7)))
        b = "".join(R.choice("abc") for _ in range(R.randint(1, 7)))
        reference = brute.shortestCommonSupersequence(a, b)
        assert is_subsequence(a, reference) and is_subsequence(b, reference)
        check(a, b, len(reference))
    a = "".join(R.choice("abcd") for _ in range(1000))
    b = "".join(R.choice("abcd") for _ in range(1000))
    timed_call(lambda: opt.shortestCommonSupersequence(a, b), 3)


@case(1277)
def _(h):
    brute, opt = both(h, 1277)
    assert opt.countSquares([[0, 1, 1, 1], [1, 1, 1, 1], [0, 1, 1, 1]]) == 15
    assert opt.countSquares([[1, 0, 1], [1, 1, 0], [1, 1, 0]]) == 7
    for _ in range(300):
        m, n = R.randint(1, 6), R.randint(1, 6)
        dense = R.random()
        matrix = [[int(R.random() < dense) for _ in range(n)] for _ in range(m)]
        assert brute.countSquares(matrix) == opt.countSquares(matrix), matrix
    assert opt.countSquares([[1] * 300 for _ in range(300)]) == sum(s * s for s in range(1, 301))
    big = [[int(R.random() < 0.9) for _ in range(300)] for _ in range(300)]
    timed_call(lambda: opt.countSquares(big), 1)


@case(1312)
def _(h):
    brute, opt = both(h, 1312)
    assert opt.minInsertions("zzazz") == 0
    assert opt.minInsertions("mbadm") == 2
    assert opt.minInsertions("leetcode") == 5
    for _ in range(300):
        s = "".join(R.choice("abc") for _ in range(R.randint(1, 10)))
        assert brute.minInsertions(s) == opt.minInsertions(s), s
    assert opt.minInsertions("abcdefghijklmnopqrstuvwxyz") == 25
    big = "".join(R.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(500))
    timed_call(lambda: opt.minInsertions(big), 1)


@case(1547)
def _(h):
    brute, opt = both(h, 1547)
    assert opt.minCost(7, [1, 3, 4, 5]) == 16
    assert opt.minCost(9, [5, 6, 1, 4, 2]) == 22
    for _ in range(200):
        n = R.randint(2, 20)
        cuts = R.sample(range(1, n), R.randint(1, min(n - 1, 6)))
        assert brute.minCost(n, list(cuts)) == opt.minCost(n, list(cuts)), (n, cuts)
    big_cuts = R.sample(range(1, 10**6), 100)
    timed_call(lambda: opt.minCost(10**6, big_cuts), 3)
