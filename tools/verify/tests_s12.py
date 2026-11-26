"""Sliding-window notes: 3, 30, 340, 567, 727, 904.

Each note has a brute force and an optimized block; both must agree on random inputs and on
LeetCode's examples, and the optimized one is run once at max constraints.
"""
import random

from harness import case
from tests_b10 import timed_call

R = random.Random(1212)


def both(h, num):
    brute, opt = h.lc_all(num, "Solution")
    return brute["Solution"](), opt["Solution"]()


def rand_str(alphabet, lo, hi):
    return "".join(R.choice(alphabet) for _ in range(R.randint(lo, hi)))


@case(3)
def _(h):
    brute, opt = both(h, 3)
    for s, want in (("abcabcbb", 3), ("bbbbb", 1), ("pwwkew", 3), ("", 0), ("abba", 2), (" ", 1)):
        assert opt.lengthOfLongestSubstring(s) == want and brute.lengthOfLongestSubstring(s) == want, s
    for _ in range(300):
        s = rand_str("abcd 1!", 0, 15)
        assert brute.lengthOfLongestSubstring(s) == opt.lengthOfLongestSubstring(s), s
    big = "".join(chr(R.randint(32, 126)) for _ in range(50_000))
    timed_call(lambda: opt.lengthOfLongestSubstring(big), 1)


@case(30)
def _(h):
    brute, opt = both(h, 30)
    assert sorted(opt.findSubstring("barfoothefoobarman", ["foo", "bar"])) == [0, 9]
    assert opt.findSubstring("wordgoodgoodgoodbestword", ["word", "good", "best", "word"]) == []
    assert sorted(opt.findSubstring("barfoofoobarthefoobarman", ["bar", "foo", "the"])) == [6, 9, 12]
    assert sorted(opt.findSubstring("aaaa", ["a", "a"])) == [0, 1, 2]
    for _ in range(400):
        w = R.randint(1, 3)
        words = [rand_str("ab", w, w) for _ in range(R.randint(1, 4))]
        s = rand_str("abc" if R.random() < 0.3 else "ab", 1, 20)
        assert sorted(brute.findSubstring(s, words)) == sorted(opt.findSubstring(s, words)), (s, words)
    assert opt.findSubstring("a" * 10_000, ["a"] * 5000) == list(range(5001))
    s = rand_str("ab", 10_000, 10_000)
    words = [rand_str("ab", 30, 30) for _ in range(300)]
    timed_call(lambda: opt.findSubstring(s, words), 1)
    timed_call(lambda: opt.findSubstring("ab" * 5000, ["ab"] * 2500 + ["ba"]), 1)


@case(340)
def _(h):
    brute, opt = both(h, 340)
    assert opt.lengthOfLongestSubstringKDistinct("eceba", 2) == 3
    assert opt.lengthOfLongestSubstringKDistinct("aa", 1) == 2
    assert opt.lengthOfLongestSubstringKDistinct("abc", 0) == 0
    for _ in range(400):
        s = rand_str("abcde", 1, 15)
        k = R.randint(0, 6)
        assert brute.lengthOfLongestSubstringKDistinct(s, k) == opt.lengthOfLongestSubstringKDistinct(s, k), (s, k)
    big = rand_str("abcdefghijklmnopqrstuvwxyz", 50_000, 50_000)
    timed_call(lambda: opt.lengthOfLongestSubstringKDistinct(big, 10), 1)


@case(567)
def _(h):
    brute, opt = both(h, 567)
    assert opt.checkInclusion("ab", "eidbaooo") is True
    assert opt.checkInclusion("ab", "eidboaoo") is False
    assert opt.checkInclusion("abc", "ab") is False
    for _ in range(500):
        s1 = rand_str("abc", 1, 4)
        s2 = rand_str("abcd", 1, 12)
        assert brute.checkInclusion(s1, s2) == opt.checkInclusion(s1, s2), (s1, s2)
    s1 = rand_str("abcdefghijklmnopqrstuvwxyz", 5000, 5000)
    s2 = rand_str("abcdefghijklmnopqrstuvwxyz", 10_000, 10_000)
    timed_call(lambda: opt.checkInclusion(s1, s2), 1)


@case(727)
def _(h):
    brute, opt = both(h, 727)
    assert opt.minWindow("abcdebdde", "bde") == "bcde"
    assert opt.minWindow("jmeqksfrsdcmsiwvaovztaqenprpvnbstl", "u") == ""
    assert opt.minWindow("abb", "bb") == "bb" and opt.minWindow("ab", "bb") == ""
    for _ in range(500):
        s1 = rand_str("abc", 1, 15)
        s2 = rand_str("abc", 1, 4)
        assert brute.minWindow(s1, s2) == opt.minWindow(s1, s2), (s1, s2)
    s1 = rand_str("ab", 20_000, 20_000)
    s2 = rand_str("ab", 100, 100)
    timed_call(lambda: opt.minWindow(s1, s2), 2)
    timed_call(lambda: opt.minWindow("a" * 20_000, "a" * 100), 2)


@case(904)
def _(h):
    brute, opt = both(h, 904)
    assert opt.totalFruit([1, 2, 1]) == 3
    assert opt.totalFruit([0, 1, 2, 2]) == 3
    assert opt.totalFruit([1, 2, 3, 2, 2]) == 4
    assert opt.totalFruit([3, 3, 3, 1, 2, 1, 1, 2, 3, 3, 4]) == 5
    for _ in range(400):
        fruits = [R.randint(0, 3) for _ in range(R.randint(1, 15))]
        assert brute.totalFruit(fruits) == opt.totalFruit(fruits), fruits
    big = [R.randint(0, 4) for _ in range(100_000)]
    timed_call(lambda: opt.totalFruit(big), 1)
