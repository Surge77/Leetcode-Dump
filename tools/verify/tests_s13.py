"""Sliding-window counting notes: "at most K" subtraction, longest window with a budget, end-picking.

Each note has a brute force and an optimized block; both must agree on random inputs and on
LeetCode's examples, and the optimized one is run once at max constraints.
"""
import random

from harness import case
from tests_b10 import timed_call

R = random.Random(13)


def both(h, num):
    brute, opt = h.lc_all(num, "Solution")
    return brute["Solution"](), opt["Solution"]()


@case(930)
def _(h):
    brute, opt = both(h, 930)
    assert opt.numSubarraysWithSum([1, 0, 1, 0, 1], 2) == 4
    assert opt.numSubarraysWithSum([0, 0, 0, 0, 0], 0) == 15
    for _ in range(300):
        nums = [R.randint(0, 1) for _ in range(R.randint(1, 14))]
        goal = R.randint(0, len(nums))
        assert brute.numSubarraysWithSum(nums, goal) == opt.numSubarraysWithSum(nums, goal), (nums, goal)
    big = [R.randint(0, 1) for _ in range(30_000)]
    timed_call(lambda: opt.numSubarraysWithSum(big, 100), 2)


@case(992)
def _(h):
    brute, opt = both(h, 992)
    assert opt.subarraysWithKDistinct([1, 2, 1, 2, 3], 2) == 7
    assert opt.subarraysWithKDistinct([1, 2, 1, 3, 4], 3) == 3
    for _ in range(300):
        n = R.randint(1, 14)
        nums = [R.randint(1, min(n, 4)) for _ in range(n)]
        k = R.randint(1, n)
        assert brute.subarraysWithKDistinct(nums, k) == opt.subarraysWithKDistinct(nums, k), (nums, k)
    n = 20_000
    big = [R.randint(1, 50) for _ in range(n)]
    timed_call(lambda: opt.subarraysWithKDistinct(big, 25), 2)


@case(1004)
def _(h):
    brute, opt = both(h, 1004)
    assert opt.longestOnes([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2) == 6
    assert opt.longestOnes([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], 3) == 10
    assert opt.longestOnes([0, 0, 0], 0) == 0
    for _ in range(300):
        nums = [R.randint(0, 1) for _ in range(R.randint(1, 15))]
        k = R.randint(0, len(nums))
        assert brute.longestOnes(nums, k) == opt.longestOnes(nums, k), (nums, k)
    big = [R.randint(0, 1) for _ in range(100_000)]
    timed_call(lambda: opt.longestOnes(big, 5_000), 2)


@case(1248)
def _(h):
    brute, opt = both(h, 1248)
    assert opt.numberOfSubarrays([1, 1, 2, 1, 1], 3) == 2
    assert opt.numberOfSubarrays([2, 4, 6], 1) == 0
    assert opt.numberOfSubarrays([2, 2, 2, 1, 2, 2, 1, 2, 2, 2], 2) == 16
    for _ in range(300):
        nums = [R.randint(1, 9) for _ in range(R.randint(1, 14))]
        k = R.randint(1, len(nums))
        assert brute.numberOfSubarrays(nums, k) == opt.numberOfSubarrays(nums, k), (nums, k)
    big = [R.randint(1, 10**5) for _ in range(50_000)]
    timed_call(lambda: opt.numberOfSubarrays(big, 100), 2)


@case(1358)
def _(h):
    brute, opt = both(h, 1358)
    assert opt.numberOfSubstrings("abcabc") == 10
    assert opt.numberOfSubstrings("aaacb") == 3
    assert opt.numberOfSubstrings("abc") == 1
    for _ in range(300):
        s = "".join(R.choice("abc") for _ in range(R.randint(3, 15)))
        assert brute.numberOfSubstrings(s) == opt.numberOfSubstrings(s), s
    big = "".join(R.choice("abc") for _ in range(50_000))
    timed_call(lambda: opt.numberOfSubstrings(big), 2)


@case(1423)
def _(h):
    brute, opt = both(h, 1423)
    assert opt.maxScore([1, 2, 3, 4, 5, 6, 1], 3) == 12
    assert opt.maxScore([2, 2, 2], 2) == 4
    assert opt.maxScore([9, 7, 7, 9, 7, 7, 9], 7) == 55
    assert opt.maxScore([3, 100, 1, 1, 4], 2) == 103
    for _ in range(300):
        cards = [R.randint(1, 20) for _ in range(R.randint(1, 12))]
        k = R.randint(1, len(cards))
        assert brute.maxScore(cards, k) == opt.maxScore(cards, k), (cards, k)
    big = [R.randint(1, 10**4) for _ in range(100_000)]
    timed_call(lambda: opt.maxScore(big, 100_000), 2)
