"""Brute-force backfill bf13: 69, 704, 74, 875, 878, 42, 735, 739, 84, 907.

Each note's first python block is the brute force; it must pass LeetCode's examples and agree with
the note's last (optimized) block on random small inputs.
"""
import random

from harness import blocks_of, case, lc_path, ns_from

R = random.Random(1313)


def brute_opt(num):
    blocks = blocks_of(lc_path(num))
    return ns_from(blocks[0])["Solution"](), ns_from(blocks[-1])["Solution"]()


@case("69-brute")
def _(h):
    brute, opt = brute_opt(69)
    assert brute.mySqrt(4) == 2 and brute.mySqrt(8) == 2 and brute.mySqrt(0) == 0 and brute.mySqrt(1) == 1
    for x in range(0, 400):
        assert brute.mySqrt(x) == opt.mySqrt(x), x
    for _ in range(100):
        x = R.randint(0, 10**6)
        assert brute.mySqrt(x) == opt.mySqrt(x), x


@case("704-brute")
def _(h):
    brute, opt = brute_opt(704)
    assert brute.search([-1, 0, 3, 5, 9, 12], 9) == 4 and brute.search([-1, 0, 3, 5, 9, 12], 2) == -1
    for _ in range(150):
        nums = sorted(R.sample(range(-30, 30), R.randint(1, 12)))
        t = R.randint(-32, 32)
        assert brute.search(nums, t) == opt.search(nums, t), (nums, t)


@case("74-brute")
def _(h):
    brute, opt = brute_opt(74)
    m = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
    assert brute.searchMatrix(m, 3) is True and brute.searchMatrix(m, 13) is False
    for _ in range(150):
        r, c = R.randint(1, 5), R.randint(1, 5)
        flat = sorted(R.sample(range(-40, 40), r * c))
        m = [flat[i * c:(i + 1) * c] for i in range(r)]
        t = R.randint(-42, 42)
        assert brute.searchMatrix(m, t) == opt.searchMatrix(m, t), (m, t)


@case("875-brute")
def _(h):
    brute, opt = brute_opt(875)
    assert brute.minEatingSpeed([3, 6, 7, 11], 8) == 4
    assert brute.minEatingSpeed([30, 11, 23, 4, 20], 5) == 30
    assert brute.minEatingSpeed([30, 11, 23, 4, 20], 6) == 23
    for _ in range(150):
        piles = [R.randint(1, 30) for _ in range(R.randint(1, 8))]
        hours = R.randint(len(piles), len(piles) + 40)
        assert brute.minEatingSpeed(piles, hours) == opt.minEatingSpeed(piles, hours), (piles, hours)


@case("878-brute")
def _(h):
    brute, opt = brute_opt(878)
    assert brute.nthMagicalNumber(1, 2, 3) == 2 and brute.nthMagicalNumber(4, 2, 3) == 6
    for _ in range(150):
        n, a, b = R.randint(1, 300), R.randint(2, 20), R.randint(2, 20)
        assert brute.nthMagicalNumber(n, a, b) == opt.nthMagicalNumber(n, a, b), (n, a, b)


@case("42-brute")
def _(h):
    brute, opt = brute_opt(42)
    assert brute.trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
    assert brute.trap([4, 2, 0, 3, 2, 5]) == 9
    for _ in range(150):
        height = [R.randint(0, 8) for _ in range(R.randint(1, 15))]
        assert brute.trap(height) == opt.trap(height), height


@case("735-brute")
def _(h):
    brute, opt = brute_opt(735)
    assert brute.asteroidCollision([5, 10, -5]) == [5, 10]
    assert brute.asteroidCollision([8, -8]) == []
    assert brute.asteroidCollision([10, 2, -5]) == [10]
    for _ in range(200):
        rocks = [R.choice([-1, 1]) * R.randint(1, 10) for _ in range(R.randint(1, 12))]
        before = list(rocks)
        assert brute.asteroidCollision(rocks) == opt.asteroidCollision(list(rocks)), rocks
        assert rocks == before


@case("739-brute")
def _(h):
    brute, opt = brute_opt(739)
    assert brute.dailyTemperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
    assert brute.dailyTemperatures([30, 40, 50, 60]) == [1, 1, 1, 0]
    assert brute.dailyTemperatures([30, 60, 90]) == [1, 1, 0]
    for _ in range(150):
        t = [R.randint(30, 50) for _ in range(R.randint(1, 15))]
        assert brute.dailyTemperatures(t) == opt.dailyTemperatures(t), t


@case("84-brute")
def _(h):
    brute, opt = brute_opt(84)
    assert brute.largestRectangleArea([2, 1, 5, 6, 2, 3]) == 10 and brute.largestRectangleArea([2, 4]) == 4
    for _ in range(150):
        heights = [R.randint(0, 10) for _ in range(R.randint(1, 14))]
        assert brute.largestRectangleArea(list(heights)) == opt.largestRectangleArea(list(heights)), heights


@case("907-brute")
def _(h):
    brute, opt = brute_opt(907)
    assert brute.sumSubarrayMins([3, 1, 2, 4]) == 17
    assert brute.sumSubarrayMins([11, 81, 94, 43, 3]) == 444
    for _ in range(150):
        arr = [R.randint(1, 30) for _ in range(R.randint(1, 14))]
        assert brute.sumSubarrayMins(arr) == opt.sumSubarrayMins(arr), arr
