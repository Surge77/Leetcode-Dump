"""Brute-force backfill bf12: 372, 96, 48, 54, 1011, 1201, 153, 2563, 33, 410.

Each note's first python block is the brute force; it must pass LeetCode's examples and agree with
the note's last (optimized) block on random small inputs.
"""
import random
from copy import deepcopy

from harness import blocks_of, case, lc_path, ns_from

R = random.Random(1212)


def brute_opt(num):
    blocks = blocks_of(lc_path(num))
    return ns_from(blocks[0])["Solution"](), ns_from(blocks[-1])["Solution"]()


@case("372-brute")
def _(h):
    brute, opt = brute_opt(372)
    assert brute.superPow(2, [3]) == 8 and brute.superPow(2, [1, 0]) == 1024
    assert brute.superPow(1, [4, 3, 3, 8, 5, 2]) == 1
    for _ in range(150):
        a = R.randint(1, 2**31 - 1)
        b = [R.randint(1, 9)] + [R.randint(0, 9) for _ in range(R.randint(0, 2))]
        assert brute.superPow(a, b) == opt.superPow(a, b), (a, b)


@case("96-brute")
def _(h):
    brute, opt = brute_opt(96)
    assert brute.numTrees(3) == 5 and brute.numTrees(1) == 1
    for n in range(1, 13):
        assert brute.numTrees(n) == opt.numTrees(n), n


@case("48-brute")
def _(h):
    brute, opt = brute_opt(48)
    m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    brute.rotate(m)
    assert m == [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
    m = [[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]
    brute.rotate(m)
    assert m == [[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]]
    for _ in range(120):
        n = R.randint(1, 7)
        a = [[R.randint(-100, 100) for _ in range(n)] for _ in range(n)]
        b = deepcopy(a)
        brute.rotate(a)
        opt.rotate(b)
        assert a == b, (a, b)


@case("54-brute")
def _(h):
    brute, opt = brute_opt(54)
    assert brute.spiralOrder([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [1, 2, 3, 6, 9, 8, 7, 4, 5]
    assert brute.spiralOrder([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]) == [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
    for _ in range(150):
        r, c = R.randint(1, 7), R.randint(1, 7)
        m = [[R.randint(-9, 9) for _ in range(c)] for _ in range(r)]
        assert brute.spiralOrder(m) == opt.spiralOrder(m), m


@case("1011-brute")
def _(h):
    brute, opt = brute_opt(1011)
    assert brute.shipWithinDays([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5) == 15
    assert brute.shipWithinDays([3, 2, 2, 4, 1, 4], 3) == 6
    assert brute.shipWithinDays([1, 2, 3, 1, 1], 4) == 3
    for _ in range(150):
        w = [R.randint(1, 20) for _ in range(R.randint(1, 10))]
        d = R.randint(1, len(w))
        assert brute.shipWithinDays(w, d) == opt.shipWithinDays(w, d), (w, d)


@case("1201-brute")
def _(h):
    brute, opt = brute_opt(1201)
    assert brute.nthUglyNumber(3, 2, 3, 5) == 4 and brute.nthUglyNumber(4, 2, 3, 4) == 6
    assert brute.nthUglyNumber(5, 2, 11, 13) == 10
    for _ in range(150):
        a, b, c, n = R.randint(1, 12), R.randint(1, 12), R.randint(1, 12), R.randint(1, 200)
        assert brute.nthUglyNumber(n, a, b, c) == opt.nthUglyNumber(n, a, b, c), (n, a, b, c)


@case("153-brute")
def _(h):
    brute, opt = brute_opt(153)
    assert brute.findMin([3, 4, 5, 1, 2]) == 1 and brute.findMin([4, 5, 6, 7, 0, 1, 2]) == 0
    assert brute.findMin([11, 13, 15, 17]) == 11
    for _ in range(150):
        n = R.randint(1, 12)
        nums = sorted(R.sample(range(-50, 50), n))
        k = R.randrange(n)
        nums = nums[k:] + nums[:k]
        assert brute.findMin(nums) == opt.findMin(nums), nums


@case("2563-brute")
def _(h):
    brute, opt = brute_opt(2563)
    assert brute.countFairPairs([0, 1, 7, 4, 4, 5], 3, 6) == 6
    assert brute.countFairPairs([1, 7, 9, 2, 5], 11, 11) == 1
    for _ in range(150):
        nums = [R.randint(-20, 20) for _ in range(R.randint(1, 12))]
        lo = R.randint(-30, 30)
        hi = lo + R.randint(0, 30)
        assert brute.countFairPairs(nums, lo, hi) == opt.countFairPairs(nums, lo, hi), (nums, lo, hi)


@case("33-brute")
def _(h):
    brute, opt = brute_opt(33)
    assert brute.search([4, 5, 6, 7, 0, 1, 2], 0) == 4 and brute.search([4, 5, 6, 7, 0, 1, 2], 3) == -1
    assert brute.search([1], 0) == -1
    for _ in range(150):
        n = R.randint(1, 10)
        nums = sorted(R.sample(range(-20, 20), n))
        k = R.randrange(n)
        nums = nums[k:] + nums[:k]
        t = R.randint(-22, 22)
        assert brute.search(nums, t) == opt.search(nums, t), (nums, t)


@case("410-brute")
def _(h):
    brute, opt = brute_opt(410)
    assert brute.splitArray([7, 2, 5, 10, 8], 2) == 18 and brute.splitArray([1, 2, 3, 4, 5], 2) == 9
    assert brute.splitArray([1, 4, 4], 3) == 4
    for _ in range(150):
        nums = [R.randint(0, 20) for _ in range(R.randint(1, 9))]
        k = R.randint(1, len(nums))
        assert brute.splitArray(nums, k) == opt.splitArray(nums, k), (nums, k)
