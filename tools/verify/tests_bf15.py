"""Brute-force backfill bf15: sliding-window counting/strings and stack parsers.

Each note's first python block is the brute force; it must pass LeetCode's examples and agree with
the note's last (optimized) block on random small inputs.
"""
import random

from harness import blocks_of, case, lc_path, ns_from

R = random.Random(1515)


def brute_opt(num):
    blocks = blocks_of(lc_path(num))
    return ns_from(blocks[0]), ns_from(blocks[-1])


def rand_str(alphabet, lo, hi):
    return "".join(R.choice(alphabet) for _ in range(R.randint(lo, hi)))


@case("2444-brute")
def _(h):
    brute, opt = brute_opt(2444)
    s = brute["Solution"]()
    assert s.countSubarrays([1, 3, 5, 2, 7, 5], 1, 5) == 2
    assert s.countSubarrays([1, 1, 1, 1], 1, 1) == 10
    for _ in range(200):
        nums = [R.randint(1, 5) for _ in range(R.randint(1, 12))]
        lo = R.randint(1, 5)
        hi = R.randint(lo, 5)
        assert s.countSubarrays(nums, lo, hi) == opt["Solution"]().countSubarrays(nums, lo, hi), (nums, lo, hi)


@case("2799-brute")
def _(h):
    brute, opt = brute_opt(2799)
    s = brute["Solution"]()
    assert s.countCompleteSubarrays([1, 3, 1, 2, 2]) == 4
    assert s.countCompleteSubarrays([5, 5, 5, 5]) == 10
    for _ in range(200):
        nums = [R.randint(1, 5) for _ in range(R.randint(1, 12))]
        assert s.countCompleteSubarrays(nums) == opt["Solution"]().countCompleteSubarrays(nums), nums


@case("3392-brute")
def _(h):
    brute, opt = brute_opt(3392)
    s = brute["Solution"]()
    assert s.countSubarrays([1, 2, 1, 4, 1]) == 1
    assert s.countSubarrays([1, 1, 1]) == 0
    for _ in range(200):
        nums = [R.randint(-6, 6) for _ in range(R.randint(3, 12))]
        assert s.countSubarrays(nums) == opt["Solution"]().countSubarrays(nums), nums


@case("3423-brute")
def _(h):
    brute, opt = brute_opt(3423)
    s = brute["Solution"]()
    assert s.maxDiff([1, 2, 4]) == 3
    assert s.maxDiff([-5, -10, -5]) == 5
    for _ in range(200):
        nums = [R.randint(-20, 20) for _ in range(R.randint(2, 10))]
        assert s.maxDiff(nums) == opt["Solution"]().maxDiff(nums), nums


@case("424-brute")
def _(h):
    brute, opt = brute_opt(424)
    s = brute["Solution"]()
    assert s.characterReplacement("ABAB", 2) == 4
    assert s.characterReplacement("AABABBA", 1) == 4
    for _ in range(200):
        text = rand_str("ABC", 1, 12)
        k = R.randint(0, len(text))
        assert s.characterReplacement(text, k) == opt["Solution"]().characterReplacement(text, k), (text, k)


@case("438-brute")
def _(h):
    brute, opt = brute_opt(438)
    s = brute["Solution"]()
    assert s.findAnagrams("cbaebabacd", "abc") == [0, 6]
    assert s.findAnagrams("abab", "ab") == [0, 1, 2]
    for _ in range(200):
        text, p = rand_str("abc", 1, 12), rand_str("abc", 1, 4)
        assert s.findAnagrams(text, p) == opt["Solution"]().findAnagrams(text, p), (text, p)


@case("76-brute")
def _(h):
    brute, opt = brute_opt(76)
    s = brute["Solution"]()
    assert s.minWindow("ADOBECODEBANC", "ABC") == "BANC"
    assert s.minWindow("a", "a") == "a"
    assert s.minWindow("a", "aa") == ""
    for _ in range(200):
        text, t = rand_str("abc", 1, 12), rand_str("abc", 1, 4)
        assert s.minWindow(text, t) == opt["Solution"]().minWindow(text, t), (text, t)


def rand_rpn(depth):
    """Random valid RPN token list; divisors are non-zero so evaluation never fails."""
    if depth == 0 or R.random() < 0.3:
        return [str(R.randint(-9, 9))]
    left, right = rand_rpn(depth - 1), rand_rpn(depth - 1)
    op = R.choice("+-*/")
    if op == "/":
        right = [str(R.choice([-7, -3, -1, 1, 2, 5, 9]))]
    return left + right + [op]


@case("150-brute")
def _(h):
    brute, opt = brute_opt(150)
    s = brute["Solution"]()
    assert s.evalRPN(["2", "1", "+", "3", "*"]) == 9
    assert s.evalRPN(["4", "13", "5", "/", "+"]) == 6
    assert s.evalRPN(["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]) == 22
    for _ in range(200):
        tokens = rand_rpn(3)
        assert s.evalRPN(list(tokens)) == opt["Solution"]().evalRPN(list(tokens)), tokens


@case("20-brute")
def _(h):
    brute, opt = brute_opt(20)
    s = brute["Solution"]()
    assert s.isValid("()") and s.isValid("()[]{}") and s.isValid("([])")
    assert not s.isValid("(]") and not s.isValid("([)]") and not s.isValid("(")
    for _ in range(300):
        text = rand_str("()[]{}", 1, 10)
        assert s.isValid(text) == opt["Solution"]().isValid(text), text


@case("227-brute")
def _(h):
    brute, opt = brute_opt(227)
    s = brute["Solution"]()
    assert s.calculate("3+2*2") == 7
    assert s.calculate(" 3/2 ") == 1
    assert s.calculate(" 3+5 / 2 ") == 5
    for _ in range(300):
        parts = [str(R.randint(0, 20))]
        for _ in range(R.randint(0, 5)):
            op = R.choice("+-*/")
            operand = R.randint(1, 20) if op == "/" else R.randint(0, 20)
            parts += [R.choice(["", " "]) + op + R.choice(["", " "]), str(operand)]
        expr = "".join(parts)
        assert s.calculate(expr) == opt["Solution"]().calculate(expr), expr
