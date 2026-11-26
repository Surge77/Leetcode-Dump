"""Sheet-coverage batch s04: zigzag, Roman numerals, common prefix, 4Sum, in-place compaction,
next permutation, last word, text justification.

Each note has a brute force and an optimized block; both must agree on random inputs and on
LeetCode's examples. Roman numerals are checked exhaustively against an independent
per-digit table, the zigzag against the cycle formula.
"""
import os.path
import random
from itertools import groupby, permutations

from harness import case
from tests_b10 import timed_call

R = random.Random(404)

ROMAN_DIGITS = (
    ("", "M", "MM", "MMM"),
    ("", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"),
    ("", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"),
    ("", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"),
)


def both(h, num):
    brute, opt = h.lc_all(num, "Solution")
    return brute["Solution"](), opt["Solution"]()


def roman(num):
    return (ROMAN_DIGITS[0][num // 1000] + ROMAN_DIGITS[1][num // 100 % 10]
            + ROMAN_DIGITS[2][num // 10 % 10] + ROMAN_DIGITS[3][num % 10])


def zigzag(s, rows):
    """Row of index j is its distance from the nearest top-row index in a cycle of 2·rows − 2."""
    cycle = max(1, 2 * rows - 2)
    order = sorted(range(len(s)), key=lambda j: min(j % cycle, cycle - j % cycle))
    return "".join(s[j] for j in order)


@case(6)
def _(h):
    brute, opt = both(h, 6)
    for sol in (brute, opt):
        assert sol.convert("PAYPALISHIRING", 3) == "PAHNAPLSIIGYIR"
        assert sol.convert("PAYPALISHIRING", 4) == "PINALSIGYAHRPI"
        assert sol.convert("A", 1) == "A"
    for _ in range(400):
        s = "".join(R.choice("abcXY,.") for _ in range(R.randint(1, 25)))
        rows = R.randint(1, 30)
        assert brute.convert(s, rows) == opt.convert(s, rows) == zigzag(s, rows), (s, rows)
    s = "".join(R.choice("abcXY,.") for _ in range(1000))
    assert opt.convert(s, 7) == zigzag(s, 7)


@case(12)
def _(h):
    brute, opt = both(h, 12)
    assert opt.intToRoman(3749) == "MMMDCCXLIX"
    assert opt.intToRoman(58) == "LVIII"
    assert opt.intToRoman(1994) == "MCMXCIV"
    assert opt.intToRoman(3888) == "MMMDCCCLXXXVIII"
    for num in range(1, 4000):
        assert brute.intToRoman(num) == opt.intToRoman(num) == roman(num), num
    assert max(range(1, 4000), key=lambda n: len(roman(n))) == 3888


@case(13)
def _(h):
    brute, opt = both(h, 13)
    assert opt.romanToInt("III") == 3
    assert opt.romanToInt("LVIII") == 58
    assert opt.romanToInt("MCMXCIV") == 1994
    for num in range(1, 4000):
        s = roman(num)
        assert brute.romanToInt(s) == opt.romanToInt(s) == num, s


@case(14)
def _(h):
    brute, opt = both(h, 14)
    assert opt.longestCommonPrefix(["flower", "flow", "flight"]) == "fl"
    assert opt.longestCommonPrefix(["dog", "racecar", "car"]) == ""
    assert opt.longestCommonPrefix(["ab", "a"]) == "a"
    for _ in range(400):
        stem = "".join(R.choice("ab") for _ in range(R.randint(0, 4)))
        strs = [stem + "".join(R.choice("ab") for _ in range(R.randint(0, 4))) for _ in range(R.randint(1, 6))]
        expected = os.path.commonprefix(strs)
        assert brute.longestCommonPrefix(strs) == opt.longestCommonPrefix(strs) == expected, strs
    assert opt.longestCommonPrefix(["z" * 200] * 200) == "z" * 200


def canon(quads):
    return sorted(sorted(q) for q in quads)


@case(18)
def _(h):
    brute, opt = both(h, 18)
    assert canon(opt.fourSum([1, 0, -1, 0, -2, 2], 0)) == [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]
    assert canon(opt.fourSum([2, 2, 2, 2, 2], 8)) == [[2, 2, 2, 2]]
    assert opt.fourSum([-3, -2, -1, -1], -7) == [[-3, -2, -1, -1]]
    assert opt.fourSum([10**9] * 4, -(10**9)) == []
    for _ in range(400):
        nums = [R.randint(-6, 6) for _ in range(R.randint(1, 10))]
        target = R.randint(-12, 12)
        got = opt.fourSum(list(nums), target)
        assert len({tuple(sorted(q)) for q in got}) == len(got), (nums, target)
        assert canon(brute.fourSum(list(nums), target)) == canon(got), (nums, target)
    big = [R.randint(-50, 50) for _ in range(200)]
    timed_call(lambda: opt.fourSum(big, 0), 5)


@case(27)
def _(h):
    brute, opt = both(h, 27)

    def check(sol, nums, val):
        arr = list(nums)
        k = sol.removeElement(arr, val)
        keep = [x for x in nums if x != val]
        assert k == len(keep) and sorted(arr[:k]) == sorted(keep), (nums, val, k, arr)
        return k

    assert check(opt, [3, 2, 2, 3], 3) == 2
    assert check(opt, [0, 1, 2, 2, 3, 0, 4, 2], 2) == 5
    for _ in range(400):
        nums = [R.randint(0, 4) for _ in range(R.randint(0, 12))]
        val = R.randint(0, 5)
        assert check(brute, nums, val) == check(opt, nums, val)


@case(31)
def _(h):
    brute, opt = both(h, 31)
    examples = (([1, 2, 3], [1, 3, 2]), ([3, 2, 1], [1, 2, 3]), ([1, 1, 5], [1, 5, 1]),
                ([1, 5, 1], [5, 1, 1]), ([1, 1], [1, 1]), ([7], [7]))
    for nums, expected in examples:
        for sol in (brute, opt):
            arr = list(nums)
            assert sol.nextPermutation(arr) is None and arr == expected, (nums, arr)
    for _ in range(400):
        nums = [R.randint(0, 3) for _ in range(R.randint(1, 7))]
        a, b = list(nums), list(nums)
        brute.nextPermutation(a)
        opt.nextPermutation(b)
        assert a == b, nums
    start = [0, 1, 1, 2, 3]
    every = sorted(set(permutations(start)))
    arr, seen = list(start), []
    for _ in every:
        seen.append(tuple(arr))
        opt.nextPermutation(arr)
    assert seen == every and arr == start


@case(58)
def _(h):
    brute, opt = both(h, 58)
    assert opt.lengthOfLastWord("Hello World") == 5
    assert opt.lengthOfLastWord("   fly me   to   the moon  ") == 4
    assert opt.lengthOfLastWord("luffy is still joyboy") == 6
    for _ in range(400):
        chars = [R.choice("ab  ") for _ in range(R.randint(0, 15))]
        chars.insert(R.randint(0, len(chars)), R.choice("XYZ"))  # guarantees at least one word
        s = "".join(chars)
        assert brute.lengthOfLastWord(s) == opt.lengthOfLastWord(s), s
    assert opt.lengthOfLastWord("q" * 10**4) == 10**4


@case(68)
def _(h):
    brute, opt = both(h, 68)
    assert opt.fullJustify(["This", "is", "an", "example", "of", "text", "justification."], 16) == [
        "This    is    an", "example  of text", "justification.  "]
    assert opt.fullJustify(["What", "must", "be", "acknowledgment", "shall", "be"], 16) == [
        "What   must   be", "acknowledgment  ", "shall be        "]
    words = ["Science", "is", "what", "we", "understand", "well", "enough", "to", "explain",
             "to", "a", "computer.", "Art", "is", "everything", "else", "we", "do"]
    assert opt.fullJustify(words, 20) == [
        "Science  is  what we", "understand      well", "enough to explain to",
        "a  computer.  Art is", "everything  else  we", "do                  "]
    for _ in range(400):
        width = R.randint(1, 16)
        words = ["".join(R.choice("xyz") for _ in range(R.randint(1, width))) for _ in range(R.randint(1, 10))]
        got = opt.fullJustify(words, width)
        assert brute.fullJustify(words, width) == got, (words, width)
        assert all(len(line) == width for line in got) and " ".join(got).split() == words, (words, width, got)
    big = ["".join(R.choice("abc") for _ in range(R.randint(1, 20))) for _ in range(300)]
    timed_call(lambda: opt.fullJustify(big, 100), 1)


def at_most_two(nums):
    return [value for value, group in groupby(nums) for _ in range(min(2, len(list(group))))]


@case(80)
def _(h):
    brute, opt = both(h, 80)
    for nums, k in (([1, 1, 1, 2, 2, 3], 5), ([0, 0, 1, 1, 1, 1, 2, 3, 3], 7)):
        arr = list(nums)
        assert opt.removeDuplicates(arr) == k and arr[:k] == at_most_two(nums), (nums, arr)
    for _ in range(400):
        nums = sorted(R.randint(-3, 3) for _ in range(R.randint(1, 15)))
        want = at_most_two(nums)
        for sol in (brute, opt):
            arr = list(nums)
            k = sol.removeDuplicates(arr)
            assert k == len(want) and arr[:k] == want, (nums, k, arr)
    big = sorted(R.randint(-10**4, 10**4) for _ in range(3 * 10**4))
    timed_call(lambda: opt.removeDuplicates(list(big)), 1)
