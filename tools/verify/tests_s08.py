"""Sheet-coverage DP notes: wildcard matching, decode ways, palindrome partitioning, circular robber,
divisible subset, counting LIS, stock with fee, min-cost stairs.

Each note has a brute force and an optimized block; both must agree on random inputs and on
LeetCode's examples, and the optimized one is run once at max constraints.
"""
import random

from harness import case
from tests_b10 import timed_call

R = random.Random(808)


def both(h, num):
    brute, opt = h.lc_all(num, "Solution")
    return brute["Solution"](), opt["Solution"]()


@case(44)
def _(h):
    brute, opt = both(h, 44)
    assert opt.isMatch("aa", "a") is False
    assert opt.isMatch("aa", "*") is True
    assert opt.isMatch("cb", "?a") is False
    assert opt.isMatch("", "***") is True and opt.isMatch("", "?") is False
    for _ in range(1500):
        s = "".join(R.choice("ab") for _ in range(R.randint(0, 8)))
        p = "".join(R.choice("ab?**") for _ in range(R.randint(0, 7)))
        assert brute.isMatch(s, p) == opt.isMatch(s, p), (s, p)
    assert opt.isMatch("a" * 2000, "*" + "a" * 999 + "b") is False
    timed_call(lambda: opt.isMatch("a" * 2000, "*" + "a" * 999 + "b"), 5)  # forces O(m·n) backtracking


@case(91)
def _(h):
    brute, opt = both(h, 91)
    assert opt.numDecodings("12") == 2 and opt.numDecodings("226") == 3 and opt.numDecodings("06") == 0
    assert opt.numDecodings("10") == 1 and opt.numDecodings("100") == 0
    for _ in range(500):
        s = "".join(R.choice("0112236789") for _ in range(R.randint(1, 15)))
        assert brute.numDecodings(s) == opt.numDecodings(s), s
    timed_call(lambda: opt.numDecodings("1" * 100), 1)


@case(132)
def _(h):
    brute, opt = both(h, 132)
    assert opt.minCut("aab") == 1 and opt.minCut("a") == 0 and opt.minCut("ab") == 1
    for _ in range(400):
        s = "".join(R.choice("aab") for _ in range(R.randint(1, 12)))
        assert brute.minCut(s) == opt.minCut(s), s
    assert opt.minCut("a" * 2000) == 0
    timed_call(lambda: opt.minCut("a" * 2000), 5)


@case(213)
def _(h):
    brute, opt = both(h, 213)
    assert opt.rob([2, 3, 2]) == 3 and opt.rob([1, 2, 3, 1]) == 4 and opt.rob([1, 2, 3]) == 3
    assert opt.rob([5]) == 5
    for _ in range(500):
        nums = [R.randint(0, 20) for _ in range(R.randint(1, 12))]
        assert brute.rob(nums) == opt.rob(nums), nums


def is_divisible_chain(subset, nums):
    if len(set(subset)) != len(subset) or not set(subset) <= set(nums):
        return False
    ordered = sorted(subset)
    return all(b % a == 0 for a, b in zip(ordered, ordered[1:]))


@case(368)
def _(h):
    brute, opt = both(h, 368)
    assert sorted(opt.largestDivisibleSubset([1, 2, 3])) in ([1, 2], [1, 3])
    assert sorted(opt.largestDivisibleSubset([1, 2, 4, 8])) == [1, 2, 4, 8]
    for _ in range(300):
        nums = R.sample(range(1, 61), R.randint(1, 11))
        got, want = opt.largestDivisibleSubset(list(nums)), brute.largestDivisibleSubset(list(nums))
        assert len(got) == len(want) and is_divisible_chain(got, nums), (nums, got, want)
    big = R.sample(range(1, 2 * 10**9), 1000)
    timed_call(lambda: opt.largestDivisibleSubset(big), 3)


@case(673)
def _(h):
    brute, opt = both(h, 673)
    assert opt.findNumberOfLIS([1, 3, 5, 4, 7]) == 2 and opt.findNumberOfLIS([2, 2, 2, 2, 2]) == 5
    for _ in range(400):
        nums = [R.randint(-5, 5) for _ in range(R.randint(1, 12))]
        assert brute.findNumberOfLIS(nums) == opt.findNumberOfLIS(nums), nums
    big = [R.randint(-10**6, 10**6) for _ in range(2000)]
    timed_call(lambda: opt.findNumberOfLIS(big), 5)


@case(714)
def _(h):
    brute, opt = both(h, 714)
    assert opt.maxProfit([1, 3, 2, 8, 4, 9], 2) == 8
    assert opt.maxProfit([1, 3, 7, 5, 10, 3], 3) == 6
    for _ in range(500):
        prices = [R.randint(1, 15) for _ in range(R.randint(1, 12))]
        fee = R.randint(0, 6)
        assert brute.maxProfit(prices, fee) == opt.maxProfit(prices, fee), (prices, fee)
    big = [R.randint(1, 5 * 10**4) for _ in range(5 * 10**4)]
    timed_call(lambda: opt.maxProfit(big, 100), 1)


@case(746)
def _(h):
    brute, opt = both(h, 746)
    assert opt.minCostClimbingStairs([10, 15, 20]) == 15
    assert opt.minCostClimbingStairs([1, 100, 1, 1, 1, 100, 1, 1, 100, 1]) == 6
    for _ in range(500):
        cost = [R.randint(0, 999) for _ in range(R.randint(2, 14))]
        assert brute.minCostClimbingStairs(cost) == opt.minCostClimbingStairs(cost), cost
