"""Brute-force backfill bf14: prefix sums, count-and-say, segment trees, sliding window sum/max.

Each note's first python block is the brute force; it must pass LeetCode's examples and agree with
the note's last (optimized) block on random small inputs or random operation sequences.
"""
import random

from harness import blocks_of, case, lc_path, ns_from

R = random.Random(1414)


def brute_opt(num):
    blocks = blocks_of(lc_path(num))
    return ns_from(blocks[0]), ns_from(blocks[-1])


@case("238-brute")
def _(h):
    brute, opt = brute_opt(238)
    s = brute["Solution"]()
    assert s.productExceptSelf([1, 2, 3, 4]) == [24, 12, 8, 6]
    assert s.productExceptSelf([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]
    for _ in range(150):
        nums = [R.randint(-4, 4) for _ in range(R.randint(2, 8))]
        assert s.productExceptSelf(list(nums)) == opt["Solution"]().productExceptSelf(list(nums)), nums


@case("2894-brute")
def _(h):
    brute, opt = brute_opt(2894)
    s = brute["Solution"]()
    assert s.differenceOfSums(10, 3) == 19
    assert s.differenceOfSums(5, 6) == 15
    assert s.differenceOfSums(5, 1) == -15
    for n in range(1, 41):
        for m in range(1, 41):
            assert s.differenceOfSums(n, m) == opt["Solution"]().differenceOfSums(n, m), (n, m)


@case("304-brute")
def _(h):
    brute, opt = brute_opt(304)
    grid = [[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]]
    nm = brute["NumMatrix"](grid)
    assert nm.sumRegion(2, 1, 4, 3) == 8
    assert nm.sumRegion(1, 1, 2, 2) == 11
    assert nm.sumRegion(1, 2, 2, 4) == 12
    for _ in range(100):
        m, n = R.randint(1, 6), R.randint(1, 6)
        matrix = [[R.randint(-9, 9) for _ in range(n)] for _ in range(m)]
        a, b = brute["NumMatrix"](matrix), opt["NumMatrix"](matrix)
        for _ in range(15):
            r1, r2 = sorted((R.randrange(m), R.randrange(m)))
            c1, c2 = sorted((R.randrange(n), R.randrange(n)))
            assert a.sumRegion(r1, c1, r2, c2) == b.sumRegion(r1, c1, r2, c2), (matrix, r1, c1, r2, c2)


@case("560-brute")
def _(h):
    brute, opt = brute_opt(560)
    s = brute["Solution"]()
    assert s.subarraySum([1, 1, 1], 2) == 2
    assert s.subarraySum([1, 2, 3], 3) == 2
    for _ in range(200):
        nums = [R.randint(-3, 3) for _ in range(R.randint(1, 12))]
        k = R.randint(-4, 4)
        assert s.subarraySum(list(nums), k) == opt["Solution"]().subarraySum(list(nums), k), (nums, k)


@case("38-brute")
def _(h):
    brute, opt = brute_opt(38)
    s = brute["Solution"]()
    assert s.countAndSay(4) == "1211"
    assert s.countAndSay(1) == "1"
    for n in range(1, 21):
        assert s.countAndSay(n) == opt["Solution"]().countAndSay(n), n


@case("2407-brute")
def _(h):
    brute, opt = brute_opt(2407)
    s = brute["Solution"]()
    assert s.lengthOfLIS([4, 2, 1, 4, 3, 4, 5, 8, 15], 3) == 5
    assert s.lengthOfLIS([7, 4, 5, 1, 8, 12, 4, 7], 5) == 4
    assert s.lengthOfLIS([1, 5], 1) == 1
    for _ in range(200):
        nums = [R.randint(1, 15) for _ in range(R.randint(1, 14))]
        k = R.randint(1, 15)
        assert s.lengthOfLIS(list(nums), k) == opt["Solution"]().lengthOfLIS(list(nums), k), (nums, k)


@case("307-brute")
def _(h):
    brute, opt = brute_opt(307)
    na = brute["NumArray"]([1, 3, 5])
    assert na.sumRange(0, 2) == 9
    na.update(1, 2)
    assert na.sumRange(0, 2) == 8
    for _ in range(120):
        nums = [R.randint(-9, 9) for _ in range(R.randint(1, 10))]
        a, b = brute["NumArray"](list(nums)), opt["NumArray"](list(nums))
        n = len(nums)
        for _ in range(30):
            if R.random() < 0.4:
                i, v = R.randrange(n), R.randint(-9, 9)
                a.update(i, v)
                b.update(i, v)
            else:
                lo, hi = sorted((R.randrange(n), R.randrange(n)))
                assert a.sumRange(lo, hi) == b.sumRange(lo, hi), (nums, lo, hi)


@case("699-brute")
def _(h):
    brute, opt = brute_opt(699)
    s = brute["Solution"]()
    assert s.fallingSquares([[1, 2], [2, 3], [6, 1]]) == [2, 5, 5]
    assert s.fallingSquares([[100, 100], [200, 100]]) == [100, 100]
    for _ in range(200):
        positions = [[R.randint(1, 12), R.randint(1, 6)] for _ in range(R.randint(1, 10))]
        assert s.fallingSquares(positions) == opt["Solution"]().fallingSquares(positions), positions


@case("209-brute")
def _(h):
    brute, opt = brute_opt(209)
    s = brute["Solution"]()
    assert s.minSubArrayLen(7, [2, 3, 1, 2, 4, 3]) == 2
    assert s.minSubArrayLen(4, [1, 4, 4]) == 1
    assert s.minSubArrayLen(11, [1, 1, 1, 1, 1, 1, 1, 1]) == 0
    for _ in range(200):
        nums = [R.randint(1, 9) for _ in range(R.randint(1, 12))]
        target = R.randint(1, 40)
        assert s.minSubArrayLen(target, nums) == opt["Solution"]().minSubArrayLen(target, nums), (target, nums)


@case("239-brute")
def _(h):
    brute, opt = brute_opt(239)
    s = brute["Solution"]()
    assert s.maxSlidingWindow([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
    assert s.maxSlidingWindow([1], 1) == [1]
    for _ in range(200):
        nums = [R.randint(-9, 9) for _ in range(R.randint(1, 14))]
        k = R.randint(1, len(nums))
        assert s.maxSlidingWindow(nums, k) == opt["Solution"]().maxSlidingWindow(nums, k), (nums, k)
