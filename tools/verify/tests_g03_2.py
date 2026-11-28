"""Gap notes g03: stack, heap/top-k, tree traversal, trie/palindromes, two pointers (part 2 of 2).

Shared helpers: helpers_g03.py.
"""
from helpers_g03 import (  # noqa: F401
    R,
    both,
    case,
    timed_call,
)


@case(443)
def _(h):
    brute, opt = both(h, 443)

    def run(sol, chars):
        work = list(chars)
        length = sol.compress(work)
        return length, work[:length]

    assert run(opt, list("aabbccc")) == (6, list("a2b2c3"))
    assert run(opt, ["a"]) == (1, ["a"])
    assert run(opt, list("abbbbbbbbbbbb")) == (4, list("ab12"))
    for _ in range(300):
        chars = []
        for _ in range(R.randint(1, 5)):
            chars += [R.choice("abcX9")] * R.choice((1, 2, 3, 9, 10, 11, 100, 101))
        want = run(brute, chars)
        assert want == run(opt, chars), chars
    timed_call(lambda: run(opt, [R.choice("ab") for _ in range(2000)]), 1)


@case(844)
def _(h):
    brute, opt = both(h, 844)
    assert opt.backspaceCompare("ab#c", "ad#c") is True
    assert opt.backspaceCompare("ab##", "c#d#") is True
    assert opt.backspaceCompare("a#c", "b") is False
    for _ in range(500):
        s = "".join(R.choice("ab##") for _ in range(R.randint(1, 10)))
        t = "".join(R.choice("ab##") for _ in range(R.randint(1, 10)))
        assert brute.backspaceCompare(s, t) == opt.backspaceCompare(s, t), (s, t)
    timed_call(lambda: opt.backspaceCompare("a#" * 100, "b#" * 100), 1)


@case(977)
def _(h):
    brute, opt = both(h, 977)
    assert opt.sortedSquares([-4, -1, 0, 3, 10]) == [0, 1, 9, 16, 100]
    assert opt.sortedSquares([-7, -3, 2, 3, 11]) == [4, 9, 9, 49, 121]
    for _ in range(300):
        nums = sorted(R.randint(-10, 10) for _ in range(R.randint(1, 12)))
        assert brute.sortedSquares(nums) == opt.sortedSquares(nums), nums
    big = sorted(R.randint(-10**4, 10**4) for _ in range(10_000))
    timed_call(lambda: opt.sortedSquares(big), 1)


@case(1679)
def _(h):
    brute, opt = both(h, 1679)
    assert opt.maxOperations([1, 2, 3, 4], 5) == 2
    assert opt.maxOperations([3, 1, 3, 4, 3], 6) == 1
    for _ in range(400):
        nums = [R.randint(1, 8) for _ in range(R.randint(1, 14))]
        k = R.randint(2, 16)
        assert brute.maxOperations(nums, k) == opt.maxOperations(nums, k), (nums, k)
    big = [R.randint(1, 10**9) for _ in range(100_000)]
    timed_call(lambda: opt.maxOperations(big, 10**9), 1)


@case(1768)
def _(h):
    brute, opt = both(h, 1768)
    assert opt.mergeAlternately("abc", "pqr") == "apbqcr"
    assert opt.mergeAlternately("ab", "pqrs") == "apbqrs"
    assert opt.mergeAlternately("abcd", "pq") == "apbqcd"
    for _ in range(300):
        a = "".join(R.choice("abc") for _ in range(R.randint(1, 8)))
        b = "".join(R.choice("xyz") for _ in range(R.randint(1, 8)))
        assert brute.mergeAlternately(a, b) == opt.mergeAlternately(a, b), (a, b)
