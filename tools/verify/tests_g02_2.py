"""Gap notes g02: hashing, intervals, linked list, GCD, binary search, prefix sum, sliding window, stack (part 2 of 2).

Shared helpers: helpers_g02.py.
"""
from helpers_g02 import (  # noqa: F401
    R,
    both,
    case,
    pair,
    timed_call,
)


@case(528)
def _(h):
    nsb, nso = both(h, 528)
    brute_cls, opt_cls = nsb["Solution"], nso["Solution"]
    import random as rnd

    one_b, one_o = brute_cls([1]), opt_cls([1])
    assert one_b.pickIndex() == 0 and one_o.pickIndex() == 0
    for _ in range(150):
        w = [R.randint(1, 10) for _ in range(R.randint(1, 8))]
        sb, so = brute_cls(w), opt_cls(w)
        for _ in range(5):
            seed = R.randrange(10**6)
            rnd.seed(seed)
            a = sb.pickIndex()
            rnd.seed(seed)
            b = so.pickIndex()
            assert a == b and 0 <= a < len(w), (w, seed)
    rnd.seed(7)
    sol = opt_cls([1, 3])
    hits = sum(sol.pickIndex() for _ in range(20_000))
    assert 0.72 < hits / 20_000 < 0.78, hits
    big = opt_cls([R.randint(1, 10**5) for _ in range(10**4)])
    timed_call(lambda: [big.pickIndex() for _ in range(10**4)], 2)


@case(724)
def _(h):
    brute, opt = pair(h, 724)
    assert opt.pivotIndex([1, 7, 3, 6, 5, 6]) == 3
    assert opt.pivotIndex([1, 2, 3]) == -1
    assert opt.pivotIndex([2, 1, -1]) == 0
    for _ in range(300):
        nums = [R.randint(-3, 3) for _ in range(R.randint(1, 10))]
        assert brute.pivotIndex(nums) == opt.pivotIndex(nums), nums
    timed_call(lambda: opt.pivotIndex([R.randint(-1000, 1000) for _ in range(10**4)]), 1)


@case(1732)
def _(h):
    brute, opt = pair(h, 1732)
    assert opt.largestAltitude([-5, 1, 5, 0, -7]) == 1
    assert opt.largestAltitude([-4, -3, -2, -1, 4, 3, 2]) == 0
    for _ in range(300):
        gain = [R.randint(-100, 100) for _ in range(R.randint(1, 15))]
        assert brute.largestAltitude(gain) == opt.largestAltitude(gain), gain
    timed_call(lambda: opt.largestAltitude([R.randint(-100, 100) for _ in range(100)]), 1)


@case(643)
def _(h):
    brute, opt = pair(h, 643)
    assert opt.findMaxAverage([1, 12, -5, -6, 50, 3], 4) == 12.75
    assert opt.findMaxAverage([5], 1) == 5.0
    for _ in range(300):
        nums = [R.randint(-20, 20) for _ in range(R.randint(1, 15))]
        k = R.randint(1, len(nums))
        assert brute.findMaxAverage(nums, k) == opt.findMaxAverage(nums, k), (nums, k)
    big = [R.randint(-10**4, 10**4) for _ in range(10**5)]
    timed_call(lambda: opt.findMaxAverage(big, 50_000), 1)


@case(1456)
def _(h):
    brute, opt = pair(h, 1456)
    assert opt.maxVowels("abciiidef", 3) == 3 and opt.maxVowels("aeiou", 2) == 2
    assert opt.maxVowels("leetcode", 3) == 2
    for _ in range(300):
        s = "".join(R.choice("abcdeiou") for _ in range(R.randint(1, 15)))
        k = R.randint(1, len(s))
        assert brute.maxVowels(s, k) == opt.maxVowels(s, k), (s, k)
    big = "".join(R.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(10**5))
    timed_call(lambda: opt.maxVowels(big, 50_000), 1)


@case(1493)
def _(h):
    brute, opt = pair(h, 1493)
    assert opt.longestSubarray([1, 1, 0, 1]) == 3
    assert opt.longestSubarray([0, 1, 1, 1, 0, 1, 1, 0, 1]) == 5
    assert opt.longestSubarray([1, 1, 1]) == 2
    assert opt.longestSubarray([1]) == 0 and opt.longestSubarray([0]) == 0
    for _ in range(300):
        nums = [R.randint(0, 1) for _ in range(R.randint(1, 14))]
        assert brute.longestSubarray(nums) == opt.longestSubarray(nums), nums
    timed_call(lambda: opt.longestSubarray([R.choice((0, 1, 1, 1)) for _ in range(10**5)]), 1)


@case(32)
def _(h):
    brute, opt = pair(h, 32)
    assert opt.longestValidParentheses("(()") == 2 and opt.longestValidParentheses(")()())") == 4
    assert opt.longestValidParentheses("") == 0
    for _ in range(400):
        s = "".join(R.choice("()") for _ in range(R.randint(0, 16)))
        assert brute.longestValidParentheses(s) == opt.longestValidParentheses(s), s
    assert opt.longestValidParentheses("()" * 15_000) == 30_000
    assert opt.longestValidParentheses("(" * 30_000) == 0
    timed_call(lambda: opt.longestValidParentheses("".join(R.choice("()") for _ in range(30_000))), 1)
