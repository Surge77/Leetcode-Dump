"""Sheet coverage s15: binary search on index parity, floor lookup, answer space, gap counting, 2D peaks.

Each note has a brute force and an optimized block; both must agree on random inputs and on
LeetCode's examples, and the optimized one is run once at max constraints.
"""
import random

from harness import case
from tests_b10 import timed_call

R = random.Random(15)


def both(h, num):
    brute, opt = h.lc_all(num, "Solution")
    return brute["Solution"](), opt["Solution"]()


@case(540)
def _(h):
    brute, opt = both(h, 540)
    assert opt.singleNonDuplicate([1, 1, 2, 3, 3, 4, 4, 8, 8]) == 2
    assert opt.singleNonDuplicate([3, 3, 7, 7, 10, 11, 11]) == 10
    assert opt.singleNonDuplicate([5]) == 5
    for _ in range(300):
        values = sorted(R.sample(range(0, 60), R.randint(1, 15)))
        single = R.choice(values)
        nums = sorted([v for v in values for _ in range(1 if v == single else 2)])
        assert brute.singleNonDuplicate(nums) == opt.singleNonDuplicate(nums) == single, nums
    big = sorted([v for v in range(0, 100_000, 2) for _ in range(2)] + [100_001])
    timed_call(lambda: opt.singleNonDuplicate(big), 1)


@case(981)
def _(h):
    brute_ns, opt_ns = h.lc_all(981, "TimeMap")
    tm = opt_ns["TimeMap"]()
    tm.set("foo", "bar", 1)
    assert tm.get("foo", 1) == "bar" and tm.get("foo", 3) == "bar"
    tm.set("foo", "bar2", 4)
    assert tm.get("foo", 4) == "bar2" and tm.get("foo", 5) == "bar2"
    assert tm.get("foo", 0) == "" and tm.get("nope", 9) == ""
    for _ in range(150):
        brute, opt = brute_ns["TimeMap"](), opt_ns["TimeMap"]()
        clock = 0
        for _ in range(R.randint(1, 40)):
            key = R.choice("abc")
            if R.random() < 0.5:
                clock += R.randint(1, 3)
                value = R.choice(["x", "y", "z", "w"])
                brute.set(key, value, clock)
                opt.set(key, value, clock)
            else:
                t = R.randint(0, clock + 3)
                assert brute.get(key, t) == opt.get(key, t), (key, t)
    opt = opt_ns["TimeMap"]()

    def run():
        for t in range(1, 100_001):
            opt.set("k", "v", t)
        for t in range(1, 100_001):
            opt.get("k", t)
    timed_call(run, 2)


@case(1283)
def _(h):
    brute, opt = both(h, 1283)
    assert opt.smallestDivisor([1, 2, 5, 9], 6) == 5
    assert opt.smallestDivisor([44, 22, 33, 11, 1], 5) == 44
    for _ in range(300):
        nums = [R.randint(1, 60) for _ in range(R.randint(1, 10))]
        threshold = R.randint(len(nums), 200)
        assert brute.smallestDivisor(nums, threshold) == opt.smallestDivisor(nums, threshold), (nums, threshold)
    big = [R.randint(1, 10**6) for _ in range(50_000)]
    timed_call(lambda: opt.smallestDivisor(big, 50_000), 3)


@case(1482)
def _(h):
    brute, opt = both(h, 1482)
    assert opt.minDays([1, 10, 3, 10, 2], 3, 1) == 3
    assert opt.minDays([1, 10, 3, 10, 2], 3, 2) == -1
    assert opt.minDays([7, 7, 7, 7, 12, 7, 7], 2, 3) == 12
    for _ in range(300):
        n = R.randint(1, 12)
        bloom = [R.randint(1, 20) for _ in range(n)]
        m, k = R.randint(1, 6), R.randint(1, n)
        assert brute.minDays(bloom, m, k) == opt.minDays(bloom, m, k), (bloom, m, k)
    big = [R.randint(1, 10**9) for _ in range(100_000)]
    timed_call(lambda: opt.minDays(big, 300, 100), 3)


@case(1539)
def _(h):
    brute, opt = both(h, 1539)
    assert opt.findKthPositive([2, 3, 4, 7, 11], 5) == 9
    assert opt.findKthPositive([1, 2, 3, 4], 2) == 6
    for _ in range(300):
        arr = sorted(R.sample(range(1, 40), R.randint(1, 15)))
        k = R.randint(1, 40)
        assert brute.findKthPositive(arr, k) == opt.findKthPositive(arr, k), (arr, k)


def is_peak(mat, i, j):
    rows, cols = len(mat), len(mat[0])
    for r, c in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
        if 0 <= r < rows and 0 <= c < cols and mat[r][c] >= mat[i][j]:
            return False
    return True


@case(1901)
def _(h):
    brute, opt = both(h, 1901)
    assert opt.findPeakGrid([[1, 4], [3, 2]]) in ([0, 1], [1, 0])
    assert opt.findPeakGrid([[10, 20, 15], [21, 30, 14], [7, 16, 32]]) in ([1, 1], [2, 2])
    for _ in range(300):
        rows, cols = R.randint(1, 7), R.randint(1, 7)
        flat = R.sample(range(1, 200), rows * cols)
        mat = [flat[r * cols:(r + 1) * cols] for r in range(rows)]
        bi, bj = brute.findPeakGrid(mat)
        oi, oj = opt.findPeakGrid(mat)
        assert is_peak(mat, bi, bj) and is_peak(mat, oi, oj), mat
    flat = R.sample(range(1, 10**6), 500 * 500)
    big = [flat[r * 500:(r + 1) * 500] for r in range(500)]
    timed_call(lambda: opt.findPeakGrid(big), 1)
