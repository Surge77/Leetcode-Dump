"""Binary search notes: median of two arrays, bounds, rotated with duplicates, peak, staircase matrix.

Each note has a brute force and an optimized block; both must agree on random inputs and on
LeetCode's examples.
"""
import random

from harness import case
from tests_b10 import timed_call

R = random.Random(14)


def both(h, num):
    brute, opt = h.lc_all(num, "Solution")
    return brute["Solution"](), opt["Solution"]()


@case(4)
def _(h):
    brute, opt = both(h, 4)
    assert opt.findMedianSortedArrays([1, 3], [2]) == 2.0
    assert opt.findMedianSortedArrays([1, 2], [3, 4]) == 2.5
    assert opt.findMedianSortedArrays([], [1]) == 1.0
    for _ in range(500):
        a = sorted(R.randint(-10, 10) for _ in range(R.randint(0, 8)))
        b = sorted(R.randint(-10, 10) for _ in range(R.randint(0 if a else 1, 8)))
        assert brute.findMedianSortedArrays(a, b) == opt.findMedianSortedArrays(a, b), (a, b)
    big_a = sorted(R.randint(-10**6, 10**6) for _ in range(1000))
    big_b = sorted(R.randint(-10**6, 10**6) for _ in range(1000))
    assert brute.findMedianSortedArrays(big_a, big_b) == opt.findMedianSortedArrays(big_a, big_b)


@case(34)
def _(h):
    brute, opt = both(h, 34)
    assert opt.searchRange([5, 7, 7, 8, 8, 10], 8) == [3, 4]
    assert opt.searchRange([5, 7, 7, 8, 8, 10], 6) == [-1, -1]
    assert opt.searchRange([], 0) == [-1, -1]
    for _ in range(500):
        nums = sorted(R.randint(0, 6) for _ in range(R.randint(0, 12)))
        t = R.randint(-1, 7)
        assert brute.searchRange(nums, t) == opt.searchRange(nums, t), (nums, t)
    big = [7] * 100_000
    assert opt.searchRange(big, 7) == [0, 99_999]
    timed_call(lambda: [opt.searchRange(big, 7) for _ in range(1000)], 1)


@case(35)
def _(h):
    brute, opt = both(h, 35)
    assert opt.searchInsert([1, 3, 5, 6], 5) == 2
    assert opt.searchInsert([1, 3, 5, 6], 2) == 1
    assert opt.searchInsert([1, 3, 5, 6], 7) == 4
    for _ in range(500):
        nums = sorted(R.sample(range(-20, 20), R.randint(1, 12)))
        t = R.randint(-22, 22)
        assert brute.searchInsert(nums, t) == opt.searchInsert(nums, t), (nums, t)


def rotated(values):
    values = sorted(values)
    k = R.randrange(len(values))
    return values[k:] + values[:k]


@case(81)
def _(h):
    brute, opt = both(h, 81)
    assert opt.search([2, 5, 6, 0, 0, 1, 2], 0) is True
    assert opt.search([2, 5, 6, 0, 0, 1, 2], 3) is False
    assert opt.search([1, 0, 1, 1, 1], 0) is True
    for _ in range(1000):
        nums = rotated([R.randint(0, 4) for _ in range(R.randint(1, 10))])
        t = R.randint(-1, 5)
        assert brute.search(nums, t) == opt.search(nums, t), (nums, t)


def is_peak(nums, i):
    left = nums[i - 1] if i > 0 else float("-inf")
    right = nums[i + 1] if i + 1 < len(nums) else float("-inf")
    return 0 <= i < len(nums) and left < nums[i] > right


@case(162)
def _(h):
    brute, opt = both(h, 162)
    assert opt.findPeakElement([1, 2, 3, 1]) == 2
    assert opt.findPeakElement([1, 2, 1, 3, 5, 6, 4]) in (1, 5)
    for _ in range(500):
        nums = [R.randint(-5, 5)]
        for _ in range(R.randint(0, 10)):
            nums.append(R.choice([v for v in range(-5, 6) if v != nums[-1]]))
        assert is_peak(nums, brute.findPeakElement(nums)), nums
        assert is_peak(nums, opt.findPeakElement(nums)), nums
    big = list(range(1000))
    assert opt.findPeakElement(big) == 999


def sorted_matrix(m, n):
    mat = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            up = mat[i - 1][j] if i else -5
            left = mat[i][j - 1] if j else -5
            mat[i][j] = max(up, left) + R.randint(0, 3)
    return mat


@case(240)
def _(h):
    brute, opt = both(h, 240)
    mat = [[1, 4, 7, 11, 15], [2, 5, 8, 12, 19], [3, 6, 9, 16, 22], [10, 13, 14, 17, 24], [18, 21, 23, 26, 30]]
    assert opt.searchMatrix(mat, 5) is True
    assert opt.searchMatrix(mat, 20) is False
    for _ in range(500):
        grid = sorted_matrix(R.randint(1, 6), R.randint(1, 6))
        t = R.randint(-6, max(map(max, grid)) + 2)
        assert brute.searchMatrix(grid, t) == opt.searchMatrix(grid, t), (grid, t)
    big = sorted_matrix(300, 300)
    timed_call(lambda: opt.searchMatrix(big, -100), 1)
