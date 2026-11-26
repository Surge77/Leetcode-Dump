"""Top K / heap notes: two heaps, k-way merge, bounded heaps, heap simulation.

Brute force and optimized blocks must agree on random inputs (design classes: random operation
sequences replayed on both) and on LeetCode's examples; the optimized one runs once at max size.
"""
import random
from collections import Counter

from harness import case
from tests_b10 import timed_call

R = random.Random(23)


def both(h, num):
    brute, opt = h.lc_all(num, "Solution")
    return brute["Solution"](), opt["Solution"]()


@case(295)
def _(h):
    brute, opt = h.lc_all(295, "MedianFinder")
    m = opt["MedianFinder"]()
    m.addNum(1)
    m.addNum(2)
    assert m.findMedian() == 1.5
    m.addNum(3)
    assert m.findMedian() == 2.0
    for _ in range(150):
        b, o = brute["MedianFinder"](), opt["MedianFinder"]()
        for _ in range(R.randint(1, 40)):
            x = R.randint(-20, 20)
            b.addNum(x)
            o.addNum(x)
            if R.random() < 0.5:
                assert b.findMedian() == o.findMedian()
        assert b.findMedian() == o.findMedian()

    def run():
        f = opt["MedianFinder"]()
        for _ in range(25_000):
            f.addNum(R.randint(-10 ** 5, 10 ** 5))
            f.findMedian()
    timed_call(run, 2)


@case(355)
def _(h):
    brute, opt = h.lc_all(355, "Twitter")
    t = opt["Twitter"]()
    t.postTweet(1, 5)
    assert t.getNewsFeed(1) == [5]
    t.follow(1, 2)
    t.postTweet(2, 6)
    assert t.getNewsFeed(1) == [6, 5]
    t.unfollow(1, 2)
    assert t.getNewsFeed(1) == [5]
    for _ in range(150):
        b, o = brute["Twitter"](), opt["Twitter"]()
        next_id = 0
        for _ in range(R.randint(1, 80)):
            op = R.randrange(4)
            u, v = R.randint(1, 5), R.randint(1, 5)
            if op == 0:
                b.postTweet(u, next_id)
                o.postTweet(u, next_id)
                next_id += 1
            elif op == 1:
                assert b.getNewsFeed(u) == o.getNewsFeed(u)
            elif u != v:
                name = "follow" if op == 2 else "unfollow"
                getattr(b, name)(u, v)
                getattr(o, name)(u, v)
        for u in range(1, 6):
            assert b.getNewsFeed(u) == o.getNewsFeed(u)

    def run():
        tw = opt["Twitter"]()
        for i in range(10_000):
            tw.postTweet(R.randint(1, 500), i)
        for v in range(2, 501):
            tw.follow(1, v)
        for _ in range(10_000):
            tw.getNewsFeed(1)
    timed_call(run, 3)


def check_pairs(nums1, nums2, k, got, expected):
    assert len(got) == len(expected)
    assert [a + b for a, b in got] == [a + b for a, b in expected], (nums1, nums2, k, got)
    available = Counter(nums1)
    other = Counter(nums2)
    used = Counter(tuple(p) for p in got)
    for (a, b), cnt in used.items():
        assert cnt <= available[a] * other[b], (a, b)


@case(373)
def _(h):
    brute, opt = both(h, 373)
    assert opt.kSmallestPairs([1, 7, 11], [2, 4, 6], 3) == [[1, 2], [1, 4], [1, 6]]
    assert opt.kSmallestPairs([1, 1, 2], [1, 2, 3], 2) == [[1, 1], [1, 1]]
    for _ in range(300):
        nums1 = sorted(R.randint(-10, 10) for _ in range(R.randint(1, 8)))
        nums2 = sorted(R.randint(-10, 10) for _ in range(R.randint(1, 8)))
        k = R.randint(1, len(nums1) * len(nums2))
        check_pairs(nums1, nums2, k, opt.kSmallestPairs(nums1, nums2, k), brute.kSmallestPairs(nums1, nums2, k))
    big1 = sorted(R.randint(-10 ** 9, 10 ** 9) for _ in range(10 ** 5))
    big2 = sorted(R.randint(-10 ** 9, 10 ** 9) for _ in range(10 ** 5))
    timed_call(lambda: opt.kSmallestPairs(big1, big2, 10 ** 4), 2)


@case(703)
def _(h):
    brute, opt = h.lc_all(703, "KthLargest")
    kl = opt["KthLargest"](3, [4, 5, 8, 2])
    assert [kl.add(x) for x in (3, 5, 10, 9, 4)] == [4, 5, 5, 8, 8]
    kl = opt["KthLargest"](4, [7, 7, 7, 7, 8, 3])
    assert [kl.add(x) for x in (2, 10, 9, 9)] == [7, 7, 7, 8]
    for _ in range(200):
        k = R.randint(1, 8)
        nums = [R.randint(-15, 15) for _ in range(R.randint(k - 1, 12))]
        b, o = brute["KthLargest"](k, list(nums)), opt["KthLargest"](k, list(nums))
        for _ in range(R.randint(1, 30)):
            x = R.randint(-15, 15)
            assert b.add(x) == o.add(x)

    def run():
        o = opt["KthLargest"](10 ** 4, [R.randint(-10 ** 4, 10 ** 4) for _ in range(10 ** 4)])
        for _ in range(10 ** 4):
            o.add(R.randint(-10 ** 4, 10 ** 4))
    timed_call(run, 2)


def dist(p):
    return p[0] * p[0] + p[1] * p[1]


@case(973)
def _(h):
    brute, opt = both(h, 973)
    assert opt.kClosest([[1, 3], [-2, 2]], 1) == [[-2, 2]]
    assert sorted(opt.kClosest([[3, 3], [5, -1], [-2, 4]], 2)) == [[-2, 4], [3, 3]]
    for _ in range(300):
        points = [[R.randint(-6, 6), R.randint(-6, 6)] for _ in range(R.randint(1, 15))]
        k = R.randint(1, len(points))
        got = opt.kClosest([p[:] for p in points], k)
        exp = brute.kClosest([p[:] for p in points], k)
        assert sorted(map(dist, got)) == sorted(map(dist, exp)), (points, k)
        pool = Counter(map(tuple, points))
        assert not Counter(map(tuple, got)) - pool
    big = [[R.randint(-10 ** 4, 10 ** 4), R.randint(-10 ** 4, 10 ** 4)] for _ in range(10 ** 4)]
    timed_call(lambda: opt.kClosest(big, 5000), 2)


@case(1046)
def _(h):
    brute, opt = both(h, 1046)
    assert opt.lastStoneWeight([2, 7, 4, 1, 8, 1]) == 1
    assert opt.lastStoneWeight([1]) == 1
    assert opt.lastStoneWeight([3, 3]) == 0
    for _ in range(300):
        stones = [R.randint(1, 30) for _ in range(R.randint(1, 30))]
        assert brute.lastStoneWeight(list(stones)) == opt.lastStoneWeight(list(stones)), stones
