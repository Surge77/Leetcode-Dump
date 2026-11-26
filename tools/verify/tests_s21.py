"""Math / number theory sheet gaps: digit arithmetic, geometry hashing, Legendre, Floyd, Fibonacci, Detect Squares.

Each note has a brute force and an optimized block; both must agree on random inputs and on
LeetCode's examples, and the optimized one is run once at max constraints where speed matters.
"""
import random

from harness import case
from tests_b10 import timed_call

R = random.Random(21)


def both(h, num, name="Solution"):
    brute, opt = h.lc_all(num, name)
    return brute[name](), opt[name]()


def rand_num_str(max_len):
    if R.random() < 0.1:
        return "0"
    length = R.randint(1, max_len)
    return str(R.randint(1, 9)) + "".join(str(R.randint(0, 9)) for _ in range(length - 1))


@case(43)
def _(h):
    brute, opt = both(h, 43)
    assert opt.multiply("2", "3") == "6" and opt.multiply("123", "456") == "56088"
    assert opt.multiply("0", "52") == "0" and opt.multiply("9", "9") == "81"
    for _ in range(400):
        a, b = rand_num_str(12), rand_num_str(12)
        expected = str(int(a) * int(b))
        assert brute.multiply(a, b) == expected == opt.multiply(a, b), (a, b)
    a, b = "9" * 200, "9" * 200
    assert opt.multiply(a, b) == str(int(a) * int(b))
    timed_call(lambda: opt.multiply(a, b), 1)


@case(66)
def _(h):
    brute, opt = both(h, 66)
    assert opt.plusOne([1, 2, 3]) == [1, 2, 4] and opt.plusOne([4, 3, 2, 1]) == [4, 3, 2, 2]
    assert opt.plusOne([9]) == [1, 0] and opt.plusOne([0]) == [1] and opt.plusOne([9, 9]) == [1, 0, 0]
    for _ in range(300):
        n = R.randint(1, 8)
        digits = [R.randint(1, 9)] + [R.choice((9, 9, R.randint(0, 9))) for _ in range(n - 1)]
        assert brute.plusOne(digits[:]) == opt.plusOne(digits[:]), digits


@case(149)
def _(h):
    brute, opt = both(h, 149)
    assert opt.maxPoints([[1, 1], [2, 2], [3, 3]]) == 3
    assert opt.maxPoints([[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]]) == 4
    assert opt.maxPoints([[0, 0]]) == 1 and opt.maxPoints([[0, 0], [5, -3]]) == 2
    for _ in range(300):
        span = R.choice((2, 4, 8))
        pool = [(x, y) for x in range(-span, span + 1) for y in range(-span, span + 1)]
        pts = [list(p) for p in R.sample(pool, R.randint(1, min(12, len(pool))))]
        assert brute.maxPoints(pts) == opt.maxPoints(pts), pts
    big = [list(p) for p in {(R.randint(-10**4, 10**4), R.randint(-10**4, 10**4)) for _ in range(300)}]
    timed_call(lambda: opt.maxPoints(big), 1)


@case(172)
def _(h):
    brute, opt = both(h, 172)
    assert opt.trailingZeroes(3) == 0 and opt.trailingZeroes(5) == 1 and opt.trailingZeroes(0) == 0
    assert opt.trailingZeroes(25) == 6
    for n in list(range(0, 300)) + [R.randint(300, 3000) for _ in range(30)]:
        assert brute.trailingZeroes(n) == opt.trailingZeroes(n), n
    assert opt.trailingZeroes(10**4) == brute.trailingZeroes(10**4)


@case(202)
def _(h):
    brute, opt = both(h, 202)
    assert opt.isHappy(19) is True and opt.isHappy(2) is False and opt.isHappy(1) is True
    for n in list(range(1, 500)) + [R.randint(1, 2**31 - 1) for _ in range(300)]:
        assert brute.isHappy(n) == opt.isHappy(n), n


@case(509)
def _(h):
    brute, opt = both(h, 509)
    assert opt.fib(2) == 1 and opt.fib(3) == 2 and opt.fib(4) == 3
    assert opt.fib(0) == 0 and opt.fib(1) == 1 and opt.fib(30) == 832040
    for n in range(0, 21):
        assert brute.fib(n) == opt.fib(n), n
    for _ in range(100):
        n = R.randint(0, 18)
        assert brute.fib(n) == opt.fib(n), n


@case(2013)
def _(h):
    brute_ns, opt_ns = h.lc_all(2013, "DetectSquares")
    ds = opt_ns["DetectSquares"]()
    for p in ([3, 10], [11, 2], [3, 2]):
        ds.add(p)
    assert ds.count([11, 10]) == 1 and ds.count([14, 8]) == 0
    ds.add([11, 2])
    assert ds.count([11, 10]) == 2
    for _ in range(150):
        b, o = brute_ns["DetectSquares"](), opt_ns["DetectSquares"]()
        side = R.choice((3, 5))
        for _ in range(R.randint(1, 60)):
            p = [R.randint(0, side), R.randint(0, side)]
            if R.random() < 0.6:
                b.add(p[:])
                o.add(p[:])
            else:
                assert b.count(p[:]) == o.count(p[:]), p
    big = opt_ns["DetectSquares"]()
    for _ in range(1500):
        big.add([R.randint(0, 1000), R.randint(0, 1000)])
    timed_call(lambda: [big.count([R.randint(0, 1000), R.randint(0, 1000)]) for _ in range(1500)], 3)
