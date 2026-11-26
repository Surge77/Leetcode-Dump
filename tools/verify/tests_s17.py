"""Bit manipulation gap notes: digit reversal, shift division, binary addition, XOR/bit-count tricks.

Each note has a brute force and an optimized block; both must agree on random inputs and on
LeetCode's examples.
"""
import random

from harness import case
from tests_b10 import timed_call

R = random.Random(17)
INT_MIN, INT_MAX = -2**31, 2**31 - 1


def both(h, num):
    brute, opt = h.lc_all(num, "Solution")
    return brute["Solution"](), opt["Solution"]()


@case(7)
def _(h):
    brute, opt = both(h, 7)
    for sol in (brute, opt):
        assert sol.reverse(123) == 321 and sol.reverse(-123) == -321 and sol.reverse(120) == 21
        assert sol.reverse(0) == 0 and sol.reverse(1534236469) == 0
        assert sol.reverse(INT_MIN) == 0 and sol.reverse(INT_MAX) == 0
        assert sol.reverse(1463847412) == 2147483641 and sol.reverse(-1463847412) == -2147483641
    for _ in range(2000):
        x = R.choice((R.randint(INT_MIN, INT_MAX), R.randint(-10**6, 10**6), R.randint(10**9, INT_MAX)))
        assert brute.reverse(x) == opt.reverse(x), x


@case(29)
def _(h):
    brute, opt = both(h, 29)
    assert opt.divide(10, 3) == 3 and opt.divide(7, -3) == -2
    assert opt.divide(INT_MIN, -1) == INT_MAX and opt.divide(INT_MIN, 1) == INT_MIN
    assert opt.divide(INT_MAX, 1) == INT_MAX and opt.divide(1, 2) == 0 and opt.divide(INT_MIN, 2) == -2**30
    for _ in range(1000):
        a, b = R.randint(-5000, 5000), R.choice([i for i in range(-60, 61) if i])
        assert brute.divide(a, b) == opt.divide(a, b), (a, b)
    for _ in range(2000):
        a = R.randint(INT_MIN, INT_MAX)
        b = R.choice((R.randint(INT_MIN, INT_MAX), R.randint(-100, 100))) or 1
        expected = abs(a) // abs(b) * (1 if (a < 0) == (b < 0) else -1)
        assert opt.divide(a, b) == min(expected, INT_MAX), (a, b)


@case(67)
def _(h):
    brute, opt = both(h, 67)
    assert opt.addBinary("11", "1") == "100" and opt.addBinary("1010", "1011") == "10101"
    assert opt.addBinary("0", "0") == "0"
    for _ in range(500):
        a, b = R.randint(0, 2**40), R.randint(0, 2**12)
        sa, sb = bin(a)[2:], bin(b)[2:]
        assert brute.addBinary(sa, sb) == opt.addBinary(sa, sb) == bin(a + b)[2:], (sa, sb)
    big = "1" * 10_000
    assert opt.addBinary(big, "1") == "1" + "0" * 10_000
    timed_call(lambda: opt.addBinary(big, big), 1)


@case(137)
def _(h):
    brute, opt = both(h, 137)
    assert opt.singleNumber([2, 2, 3, 2]) == 3 and opt.singleNumber([0, 1, 0, 1, 0, 1, 99]) == 99
    assert opt.singleNumber([INT_MIN, INT_MIN, INT_MIN, -7]) == -7
    for _ in range(300):
        pool = R.sample(range(-50, 51), R.randint(1, 10))
        single, triples = pool[0], pool[1:]
        nums = [single] + triples * 3
        R.shuffle(nums)
        assert brute.singleNumber(nums[:]) == opt.singleNumber(nums[:]) == single, nums
    vals = R.sample(range(INT_MIN, INT_MAX), 10_001)
    nums = [vals[0]] + vals[1:] * 3
    R.shuffle(nums)
    assert opt.singleNumber(nums) == vals[0]
    timed_call(lambda: opt.singleNumber(nums), 1)


@case(201)
def _(h):
    brute, opt = both(h, 201)
    assert opt.rangeBitwiseAnd(5, 7) == 4 and opt.rangeBitwiseAnd(0, 0) == 0
    assert opt.rangeBitwiseAnd(1, INT_MAX) == 0 and opt.rangeBitwiseAnd(INT_MAX, INT_MAX) == INT_MAX
    for _ in range(500):
        lo = R.randint(0, 3000)
        hi = R.randint(lo, lo + R.choice((5, 50, 600)))
        assert brute.rangeBitwiseAnd(lo, hi) == opt.rangeBitwiseAnd(lo, hi), (lo, hi)
    for _ in range(200):
        lo = R.randint(2**30, INT_MAX - 100)
        hi = R.randint(lo, lo + 100)
        assert brute.rangeBitwiseAnd(lo, hi) == opt.rangeBitwiseAnd(lo, hi), (lo, hi)


@case(231)
def _(h):
    brute, opt = both(h, 231)
    assert opt.isPowerOfTwo(1) is True and opt.isPowerOfTwo(16) is True and opt.isPowerOfTwo(3) is False
    assert opt.isPowerOfTwo(0) is False and opt.isPowerOfTwo(INT_MIN) is False and opt.isPowerOfTwo(2**30) is True
    for n in list(range(-100, 5000)) + [R.randint(INT_MIN, INT_MAX) for _ in range(500)] + [2**k for k in range(31)]:
        assert brute.isPowerOfTwo(n) == opt.isPowerOfTwo(n), n


@case(260)
def _(h):
    brute, opt = both(h, 260)
    assert sorted(opt.singleNumber([1, 2, 1, 3, 2, 5])) == [3, 5]
    assert sorted(opt.singleNumber([-1, 0])) == [-1, 0] and sorted(opt.singleNumber([0, 1])) == [0, 1]
    assert sorted(opt.singleNumber([INT_MIN, INT_MAX])) == [INT_MIN, INT_MAX]
    for _ in range(300):
        pool = R.sample(range(-60, 61), R.randint(2, 12))
        nums = pool[:2] + pool[2:] * 2
        R.shuffle(nums)
        assert sorted(brute.singleNumber(nums[:])) == sorted(opt.singleNumber(nums[:])) == sorted(pool[:2]), nums
    vals = R.sample(range(INT_MIN, INT_MAX), 15_001)
    nums = vals[:2] + vals[2:] * 2
    timed_call(lambda: opt.singleNumber(nums), 1)


@case(2220)
def _(h):
    brute, opt = both(h, 2220)
    assert opt.minBitFlips(10, 7) == 3 and opt.minBitFlips(3, 4) == 3 and opt.minBitFlips(5, 5) == 0
    for _ in range(1000):
        s, g = R.randint(0, 10**9), R.randint(0, 10**9)
        assert brute.minBitFlips(s, g) == opt.minBitFlips(s, g) == bin(s ^ g).count("1"), (s, g)
