"""Brute-force blocks for bf02 notes: each must match LeetCode examples and agree with the optimized block."""
import random

from harness import blocks_of, case, lc_path, ns_from

R = random.Random(202)
TRIALS = 150


def pair(num):
    blocks = blocks_of(lc_path(num))
    return ns_from(blocks[0])["Solution"](), ns_from(blocks[-1])["Solution"]()


def canon(subsets):
    return sorted(tuple(sorted(s)) for s in subsets)


@case("90-brute")
def _(h):
    brute, opt = pair(90)
    assert canon(brute.subsetsWithDup([1, 2, 2])) == canon([[], [1], [1, 2], [1, 2, 2], [2], [2, 2]])
    assert canon(brute.subsetsWithDup([0])) == canon([[], [0]])
    for _ in range(TRIALS):
        nums = [R.randint(-3, 3) for _ in range(R.randint(1, 8))]
        assert canon(brute.subsetsWithDup(nums[:])) == canon(opt.subsetsWithDup(nums[:])), nums


@case("136-brute")
def _(h):
    brute, opt = pair(136)
    assert brute.singleNumber([2, 2, 1]) == 1
    assert brute.singleNumber([4, 1, 2, 1, 2]) == 4
    assert brute.singleNumber([1]) == 1
    for _ in range(TRIALS):
        vals = R.sample(range(-30, 30), R.randint(1, 8))
        nums = vals + vals[1:]
        R.shuffle(nums)
        assert brute.singleNumber(nums) == opt.singleNumber(nums) == vals[0], nums


@case("190-brute")
def _(h):
    brute, opt = pair(190)
    assert brute.reverseBits(43261596) == 964176192
    assert brute.reverseBits(4294967293) == 3221225471
    for _ in range(TRIALS):
        n = R.randrange(2**32)
        assert brute.reverseBits(n) == opt.reverseBits(n), n


@case("191-brute")
def _(h):
    brute, opt = pair(191)
    assert brute.hammingWeight(11) == 3
    assert brute.hammingWeight(128) == 1
    assert brute.hammingWeight(2147483645) == 30
    for _ in range(TRIALS):
        n = R.randint(1, 2**31 - 1)
        assert brute.hammingWeight(n) == opt.hammingWeight(n), n


@case("268-brute")
def _(h):
    brute, opt = pair(268)
    assert brute.missingNumber([3, 0, 1]) == 2
    assert brute.missingNumber([0, 1]) == 2
    assert brute.missingNumber([9, 6, 4, 2, 3, 5, 7, 0, 1]) == 8
    for _ in range(TRIALS):
        n = R.randint(1, 20)
        missing = R.randint(0, n)
        nums = [x for x in range(n + 1) if x != missing]
        R.shuffle(nums)
        assert brute.missingNumber(nums[:]) == opt.missingNumber(nums[:]), nums


@case("338-brute")
def _(h):
    brute, opt = pair(338)
    assert brute.countBits(2) == [0, 1, 1]
    assert brute.countBits(5) == [0, 1, 1, 2, 1, 2]
    for _ in range(TRIALS):
        n = R.randint(0, 300)
        assert brute.countBits(n) == opt.countBits(n), n


@case("371-brute")
def _(h):
    brute, opt = pair(371)
    assert brute.getSum(1, 2) == 3
    assert brute.getSum(2, 3) == 5
    for _ in range(TRIALS):
        a, b = R.randint(-1000, 1000), R.randint(-1000, 1000)
        assert brute.getSum(a, b) == opt.getSum(a, b) == a + b, (a, b)


@case("118-brute")
def _(h):
    brute, opt = pair(118)
    assert brute.generate(5) == [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]
    assert brute.generate(1) == [[1]]
    for _ in range(TRIALS):
        rows = R.randint(1, 30)
        assert brute.generate(rows) == opt.generate(rows), rows


@case("1235-brute")
def _(h):
    brute, opt = pair(1235)
    assert brute.jobScheduling([1, 2, 3, 3], [3, 4, 5, 6], [50, 10, 40, 70]) == 120
    assert brute.jobScheduling([1, 2, 3, 4, 6], [3, 5, 10, 6, 9], [20, 20, 100, 70, 60]) == 150
    assert brute.jobScheduling([1, 1, 1], [2, 3, 4], [5, 6, 4]) == 6
    for _ in range(TRIALS):
        n = R.randint(1, 9)
        st = [R.randint(1, 10) for _ in range(n)]
        en = [s + R.randint(1, 5) for s in st]
        pr = [R.randint(1, 20) for _ in range(n)]
        assert brute.jobScheduling(st[:], en[:], pr[:]) == opt.jobScheduling(st[:], en[:], pr[:]), (st, en, pr)


@case("139-brute")
def _(h):
    brute, opt = pair(139)
    assert brute.wordBreak("leetcode", ["leet", "code"])
    assert brute.wordBreak("applepenapple", ["apple", "pen"])
    assert not brute.wordBreak("catsandog", ["cats", "dog", "sand", "and", "cat"])
    for _ in range(TRIALS):
        words = list({"".join(R.choice("ab") for _ in range(R.randint(1, 3))) for _ in range(3)})
        s = "".join(R.choice("ab") for _ in range(R.randint(1, 12)))
        assert brute.wordBreak(s, words[:]) == opt.wordBreak(s, words[:]), (s, words)
