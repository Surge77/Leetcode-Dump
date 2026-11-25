import random
from bisect import bisect_left, bisect_right, insort

from harness import case

R = random.Random(5)


@case(307)
def _(h):
    NumArray = h.lc(307)["NumArray"]
    for _ in range(200):
        a = [R.randint(-50, 50) for _ in range(R.randint(1, 20))]
        obj = NumArray(a[:])
        for _ in range(30):
            if R.random() < 0.5:
                i = R.randrange(len(a))
                a[i] = R.randint(-50, 50)
                obj.update(i, a[i])
            else:
                l = R.randrange(len(a))
                r = R.randrange(l, len(a))
                assert obj.sumRange(l, r) == sum(a[l:r + 1])


@case(699)
def _(h):
    S = h.lc(699)["Solution"]()
    assert S.fallingSquares([[1, 2], [2, 3], [6, 1]]) == [2, 5, 5]
    assert S.fallingSquares([[100, 100], [200, 100]]) == [100, 100]
    for _ in range(300):
        pos = [[R.randint(1, 20), R.randint(1, 6)] for _ in range(R.randint(1, 10))]
        landed, best, want = [], 0, []
        for left, size in pos:
            base = max([hgt for l2, r2, hgt in landed if l2 < left + size and left < r2], default=0)
            landed.append((left, left + size, base + size))
            best = max(best, base + size)
            want.append(best)
        assert S.fallingSquares(pos) == want, pos


@case(2407)
def _(h):
    S = h.lc(2407)["Solution"]()
    assert S.lengthOfLIS([4, 2, 1, 4, 3, 4, 5, 8, 15], 3) == 5 and S.lengthOfLIS([7, 4, 5, 1, 8, 12, 4, 7], 5) == 4
    assert S.lengthOfLIS([1, 5], 1) == 1
    for _ in range(300):
        a = [R.randint(1, 15) for _ in range(R.randint(1, 12))]
        k = R.randint(1, 5)
        dp = [1] * len(a)
        for i in range(len(a)):
            for j in range(i):
                if 0 < a[i] - a[j] <= k:
                    dp[i] = max(dp[i], dp[j] + 1)
        assert S.lengthOfLIS(a, k) == max(dp), (a, k)


@case(315)
def _(h):
    S = h.lc(315)["Solution"]()
    assert S.countSmaller([5, 2, 6, 1]) == [2, 1, 1, 0] and S.countSmaller([-1, -1]) == [0, 0]
    for _ in range(300):
        a = [R.randint(-10, 10) for _ in range(R.randint(1, 15))]
        assert S.countSmaller(a) == [sum(a[j] < a[i] for j in range(i + 1, len(a))) for i in range(len(a))]


@case(493)
def _(h):
    S = h.lc(493)["Solution"]()
    assert S.reversePairs([1, 3, 2, 3, 1]) == 2 and S.reversePairs([2, 4, 3, 5, 1]) == 3
    for _ in range(300):
        a = [R.randint(-20, 20) for _ in range(R.randint(1, 15))]
        want = sum(a[i] > 2 * a[j] for i in range(len(a)) for j in range(i + 1, len(a)))
        assert S.reversePairs(a) == want, a


@case(327)
def _(h):
    S = h.lc(327)["Solution"]()
    assert S.countRangeSum([-2, 5, -1], -2, 2) == 3 and S.countRangeSum([0], 0, 0) == 1
    for _ in range(300):
        a = [R.randint(-10, 10) for _ in range(R.randint(1, 12))]
        lo = R.randint(-15, 10)
        hi = lo + R.randint(0, 12)
        want = sum(lo <= sum(a[i:j + 1]) <= hi for i in range(len(a)) for j in range(i, len(a)))
        assert S.countRangeSum(a, lo, hi) == want, (a, lo, hi)


@case(1649)
def _(h):
    S = h.lc(1649)["Solution"]()
    assert S.createSortedArray([1, 5, 6, 2]) == 1 and S.createSortedArray([1, 2, 3, 6, 5, 4]) == 3
    assert S.createSortedArray([1, 3, 3, 3, 2, 4, 2, 1, 2]) == 4
    for _ in range(300):
        ins = [R.randint(1, 12) for _ in range(R.randint(1, 15))]
        arr, cost = [], 0
        for x in ins:
            cost += min(bisect_left(arr, x), len(arr) - bisect_right(arr, x))
            insort(arr, x)
        assert S.createSortedArray(ins) == cost % (10**9 + 7)


@case(560)
def _(h):
    S = h.lc(560)["Solution"]()
    assert S.subarraySum([1, 1, 1], 2) == 2 and S.subarraySum([1, 2, 3], 3) == 2
    for _ in range(300):
        a = [R.randint(-5, 5) for _ in range(R.randint(1, 12))]
        k = R.randint(-6, 6)
        assert S.subarraySum(a, k) == sum(sum(a[i:j + 1]) == k for i in range(len(a)) for j in range(i, len(a)))


@case(304)
def _(h):
    NumMatrix = h.lc(304)["NumMatrix"]
    for _ in range(100):
        m, n = R.randint(1, 6), R.randint(1, 6)
        g = [[R.randint(-9, 9) for _ in range(n)] for _ in range(m)]
        obj = NumMatrix(g)
        for _ in range(20):
            r1, c1 = R.randrange(m), R.randrange(n)
            r2, c2 = R.randrange(r1, m), R.randrange(c1, n)
            assert obj.sumRegion(r1, c1, r2, c2) == sum(g[i][j] for i in range(r1, r2 + 1) for j in range(c1, c2 + 1))
