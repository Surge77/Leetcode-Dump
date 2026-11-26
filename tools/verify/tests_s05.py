"""Arrays sheet notes (s05): merge, stock II, candy, reverse words, majority II, h-index,
max consecutive ones, sort, sorted-and-rotated, rearrange by sign.

Each note has a brute force and an optimized block; both must agree on LeetCode's examples
and on random inputs, and the optimized one runs once at max constraints where speed matters.
"""
import random

from harness import case
from tests_b10 import timed_call

R = random.Random(505)


def both(h, num):
    brute, opt = h.lc_all(num, "Solution")
    return brute["Solution"](), opt["Solution"]()


@case(88)
def _(h):
    brute, opt = both(h, 88)

    def run(sol, nums1, m, nums2, n):
        arr = nums1[:]
        assert sol.merge(arr, m, nums2[:], n) is None
        return arr

    assert run(opt, [1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3) == [1, 2, 2, 3, 5, 6]
    assert run(opt, [1], 1, [], 0) == [1]
    assert run(opt, [0], 0, [1], 1) == [1]
    for _ in range(300):
        m = R.randint(0, 8)
        n = R.randint(0 if m else 1, 8)
        a = sorted(R.randint(-10**9, 10**9) if R.random() < 0.2 else R.randint(-4, 4) for _ in range(m)) + [0] * n
        b = sorted(R.randint(-4, 4) for _ in range(n))
        expected = sorted(a[:m] + b)
        assert run(brute, a, m, b, n) == run(opt, a, m, b, n) == expected, (a, m, b, n)


@case(122)
def _(h):
    brute, opt = both(h, 122)
    assert opt.maxProfit([7, 1, 5, 3, 6, 4]) == 7
    assert opt.maxProfit([1, 2, 3, 4, 5]) == 4
    assert opt.maxProfit([7, 6, 4, 3, 1]) == 0
    for _ in range(300):
        prices = [R.randint(0, 10) for _ in range(R.randint(1, 11))]
        assert brute.maxProfit(prices) == opt.maxProfit(prices), prices
    big = [R.randint(0, 10**4) for _ in range(3 * 10**4)]
    timed_call(lambda: opt.maxProfit(big), 1)


@case(135)
def _(h):
    brute, opt = both(h, 135)
    assert opt.candy([1, 0, 2]) == 5
    assert opt.candy([1, 2, 2]) == 4
    for _ in range(300):
        ratings = [R.randint(0, 4) for _ in range(R.randint(1, 12))]
        assert brute.candy(ratings) == opt.candy(ratings), ratings
    n = 2 * 10**4
    assert opt.candy(list(range(n, 0, -1))) == n * (n + 1) // 2
    big = [R.randint(0, 2 * 10**4) for _ in range(n)]
    timed_call(lambda: opt.candy(big), 1)


@case(151)
def _(h):
    brute, opt = both(h, 151)
    assert opt.reverseWords("the sky is blue") == "blue is sky the"
    assert opt.reverseWords("  hello world  ") == "world hello"
    assert opt.reverseWords("a good   example") == "example good a"
    for _ in range(400):
        s = "".join(R.choice("aB1   ") for _ in range(R.randint(1, 15)))
        if not s.strip():
            s += "x"
        expected = " ".join(reversed(s.split()))
        assert brute.reverseWords(s) == opt.reverseWords(s) == expected, repr(s)
    big = (" " + " ".join("w" * R.randint(1, 5) for _ in range(3000)))[:10**4]
    timed_call(lambda: opt.reverseWords(big), 1)


@case(229)
def _(h):
    brute, opt = both(h, 229)
    assert sorted(opt.majorityElement([3, 2, 3])) == [3]
    assert sorted(opt.majorityElement([1])) == [1]
    assert sorted(opt.majorityElement([1, 2])) == [1, 2]
    for _ in range(500):
        spread = R.choice((1, 2, 3))
        nums = [R.randint(-spread, spread) for _ in range(R.randint(1, 12))]
        assert sorted(brute.majorityElement(nums)) == sorted(opt.majorityElement(nums)), nums
    n = 5 * 10**4
    third = n // 3 + 1
    big = [7] * third + [-7] * third + [R.randint(-10**9, 10**9) for _ in range(n - 2 * third)]
    R.shuffle(big)
    assert sorted(opt.majorityElement(big)) == [-7, 7]
    timed_call(lambda: opt.majorityElement(big), 1)


@case(274)
def _(h):
    brute, opt = both(h, 274)
    assert opt.hIndex([3, 0, 6, 1, 5]) == 3
    assert opt.hIndex([1, 3, 1]) == 1
    for _ in range(400):
        citations = [R.randint(0, 12) for _ in range(R.randint(1, 10))]
        assert brute.hIndex(citations) == opt.hIndex(citations), citations
    assert opt.hIndex([1000] * 5000) == 1000
    assert opt.hIndex([0] * 5000) == 0
    big = [R.randint(0, 1000) for _ in range(5000)]
    timed_call(lambda: opt.hIndex(big), 1)


@case(485)
def _(h):
    brute, opt = both(h, 485)
    assert opt.findMaxConsecutiveOnes([1, 1, 0, 1, 1, 1]) == 3
    assert opt.findMaxConsecutiveOnes([1, 0, 1, 1, 0, 1]) == 2
    for _ in range(400):
        nums = [R.randint(0, 1) for _ in range(R.randint(1, 15))]
        assert brute.findMaxConsecutiveOnes(nums) == opt.findMaxConsecutiveOnes(nums), nums
    assert opt.findMaxConsecutiveOnes([1] * 10**5) == 10**5
    big = [R.randint(0, 1) for _ in range(10**5)]
    timed_call(lambda: opt.findMaxConsecutiveOnes(big), 1)


@case(912)
def _(h):
    brute, opt = both(h, 912)
    assert opt.sortArray([5, 2, 3, 1]) == [1, 2, 3, 5]
    assert opt.sortArray([5, 1, 1, 2, 0, 0]) == [0, 0, 1, 1, 2, 5]
    for _ in range(300):
        nums = [R.randint(-5, 5) for _ in range(R.randint(1, 20))]
        assert brute.sortArray(nums[:]) == opt.sortArray(nums[:]) == sorted(nums), nums
    n = 5 * 10**4
    for big in ([R.randint(-n, n) for _ in range(n)], [3] * n, list(range(n, 0, -1))):
        assert opt.sortArray(big[:]) == sorted(big)
    big = [R.randint(-n, n) for _ in range(n)]
    timed_call(lambda: opt.sortArray(big[:]), 3)


@case(1752)
def _(h):
    brute, opt = both(h, 1752)
    assert opt.check([3, 4, 5, 1, 2]) is True
    assert opt.check([2, 1, 3, 4]) is False
    assert opt.check([1, 2, 3]) is True
    for _ in range(400):
        n = R.randint(1, 8)
        if R.random() < 0.5:
            base = sorted(R.randint(1, 5) for _ in range(n))
            k = R.randrange(n)
            nums = base[k:] + base[:k]
            assert opt.check(nums) is True, nums
        else:
            nums = [R.randint(1, 5) for _ in range(n)]
        assert brute.check(nums) == opt.check(nums), nums


@case(2149)
def _(h):
    brute, opt = both(h, 2149)
    assert opt.rearrangeArray([3, 1, -2, -5, 2, -4]) == [3, -2, 1, -5, 2, -4]
    assert opt.rearrangeArray([-1, 1]) == [1, -1]
    for _ in range(300):
        half = R.randint(1, 6)
        nums = [R.randint(1, 9) for _ in range(half)] + [-R.randint(1, 9) for _ in range(half)]
        R.shuffle(nums)
        original = nums[:]
        got = opt.rearrangeArray(nums[:])
        assert brute.rearrangeArray(nums[:]) == got, original
        assert [x for x in got if x > 0] == [x for x in original if x > 0], original
        assert [x for x in got if x < 0] == [x for x in original if x < 0], original
        assert all((x > 0) == (i % 2 == 0) for i, x in enumerate(got)), original
    n = 2 * 10**5
    big = [R.randint(1, 10**5) for _ in range(n // 2)] + [-R.randint(1, 10**5) for _ in range(n // 2)]
    R.shuffle(big)
    timed_call(lambda: opt.rearrangeArray(big), 1)
