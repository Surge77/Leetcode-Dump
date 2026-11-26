"""Brute-force blocks for 49, 73, 435, 452, 56, 57, 1359, 1922, 204, 2521 versus the optimized solutions."""
import copy
import random

from harness import blocks_of, case, lc_path, ns_from


def pair(num):
    blocks = blocks_of(lc_path(num))
    return ns_from(blocks[0]), ns_from(blocks[-1])


def normalized(groups):
    return sorted(sorted(g) for g in groups)


@case("49-brute")
def _(h):
    brute, opt = pair(49)
    rng = random.Random(4901)
    got = brute["Solution"]().groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    assert normalized(got) == normalized([["bat"], ["nat", "tan"], ["ate", "eat", "tea"]])
    assert normalized(brute["Solution"]().groupAnagrams([""])) == [[""]]
    assert normalized(brute["Solution"]().groupAnagrams(["a"])) == [["a"]]
    for _ in range(200):
        words = ["".join(rng.choice("abc") for _ in range(rng.randint(0, 4))) for _ in range(rng.randint(1, 10))]
        want = normalized(opt["Solution"]().groupAnagrams(list(words)))
        assert normalized(brute["Solution"]().groupAnagrams(list(words))) == want, words


@case("73-brute")
def _(h):
    brute, opt = pair(73)
    rng = random.Random(7301)
    m = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    brute["Solution"]().setZeroes(m)
    assert m == [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
    m = [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]
    brute["Solution"]().setZeroes(m)
    assert m == [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]
    for _ in range(200):
        rows, cols = rng.randint(1, 5), rng.randint(1, 5)
        matrix = [[rng.choice([0, 1, 2, 3, 3]) for _ in range(cols)] for _ in range(rows)]
        a, b = copy.deepcopy(matrix), copy.deepcopy(matrix)
        brute["Solution"]().setZeroes(a)
        opt["Solution"]().setZeroes(b)
        assert a == b, matrix


@case("435-brute")
def _(h):
    brute, opt = pair(435)
    rng = random.Random(43501)
    assert brute["Solution"]().eraseOverlapIntervals([[1, 2], [2, 3], [3, 4], [1, 3]]) == 1
    assert brute["Solution"]().eraseOverlapIntervals([[1, 2], [1, 2], [1, 2]]) == 2
    assert brute["Solution"]().eraseOverlapIntervals([[1, 2], [2, 3]]) == 0
    for _ in range(150):
        ivs = []
        for _ in range(rng.randint(1, 8)):
            s = rng.randint(-5, 8)
            ivs.append([s, s + rng.randint(1, 6)])
        assert brute["Solution"]().eraseOverlapIntervals(copy.deepcopy(ivs)) == \
            opt["Solution"]().eraseOverlapIntervals(copy.deepcopy(ivs)), ivs


@case("452-brute")
def _(h):
    brute, opt = pair(452)
    rng = random.Random(45201)
    assert brute["Solution"]().findMinArrowShots([[10, 16], [2, 8], [1, 6], [7, 12]]) == 2
    assert brute["Solution"]().findMinArrowShots([[1, 2], [3, 4], [5, 6], [7, 8]]) == 4
    assert brute["Solution"]().findMinArrowShots([[1, 2], [2, 3], [3, 4], [4, 5]]) == 2
    for _ in range(150):
        pts = []
        for _ in range(rng.randint(1, 8)):
            s = rng.randint(-6, 8)
            pts.append([s, s + rng.randint(0, 6)])
        assert brute["Solution"]().findMinArrowShots(copy.deepcopy(pts)) == \
            opt["Solution"]().findMinArrowShots(copy.deepcopy(pts)), pts


@case("56-brute")
def _(h):
    brute, opt = pair(56)
    rng = random.Random(5601)
    assert brute["Solution"]().merge([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
    assert brute["Solution"]().merge([[1, 4], [4, 5]]) == [[1, 5]]
    assert brute["Solution"]().merge([[4, 7], [1, 4]]) == [[1, 7]]
    for _ in range(200):
        ivs = []
        for _ in range(rng.randint(1, 8)):
            s = rng.randint(0, 15)
            ivs.append([s, s + rng.randint(0, 5)])
        assert brute["Solution"]().merge(copy.deepcopy(ivs)) == opt["Solution"]().merge(copy.deepcopy(ivs)), ivs


@case("57-brute")
def _(h):
    brute, opt = pair(57)
    rng = random.Random(5701)
    assert brute["Solution"]().insert([[1, 3], [6, 9]], [2, 5]) == [[1, 5], [6, 9]]
    assert brute["Solution"]().insert([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]) == \
        [[1, 2], [3, 10], [12, 16]]
    assert brute["Solution"]().insert([[1, 5]], [6, 8]) == [[1, 5], [6, 8]]
    for _ in range(200):
        starts = sorted(rng.sample(range(0, 40, 2), rng.randint(0, 6)))
        ivs = [[s, s + rng.randint(0, 1)] for s in starts]
        s = rng.randint(-2, 40)
        new = [s, s + rng.randint(0, 8)]
        want = opt["Solution"]().insert(copy.deepcopy(ivs), list(new))
        assert brute["Solution"]().insert(copy.deepcopy(ivs), list(new)) == want, (ivs, new)


@case("1359-brute")
def _(h):
    brute, opt = pair(1359)
    assert [brute["Solution"]().countOrders(n) for n in (1, 2, 3)] == [1, 6, 90]
    for n in range(1, 5):
        assert brute["Solution"]().countOrders(n) == opt["Solution"]().countOrders(n), n


@case("1922-brute")
def _(h):
    brute, opt = pair(1922)
    assert brute["Solution"]().countGoodNumbers(1) == 5
    assert brute["Solution"]().countGoodNumbers(4) == 400
    for n in range(1, 6):
        assert brute["Solution"]().countGoodNumbers(n) == opt["Solution"]().countGoodNumbers(n), n


@case("204-brute")
def _(h):
    brute, opt = pair(204)
    assert brute["Solution"]().countPrimes(10) == 4
    assert brute["Solution"]().countPrimes(0) == 0 and brute["Solution"]().countPrimes(1) == 0
    for n in range(0, 301):
        assert brute["Solution"]().countPrimes(n) == opt["Solution"]().countPrimes(n), n


@case("2521-brute")
def _(h):
    brute, opt = pair(2521)
    rng = random.Random(252101)
    assert brute["Solution"]().distinctPrimeFactors([2, 4, 3, 7, 10, 6]) == 4
    assert brute["Solution"]().distinctPrimeFactors([2, 4, 8, 16]) == 1
    for _ in range(200):
        nums = [rng.randint(2, 200) for _ in range(rng.randint(1, 6))]
        assert brute["Solution"]().distinctPrimeFactors(nums) == opt["Solution"]().distinctPrimeFactors(nums), nums
