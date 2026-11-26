"""Brute-force backfill bf16: each note's first python block (brute force) vs its last (optimized)."""
import random

from harness import blocks_of, case, lc_path, ns_from

R = random.Random(2616)


def pair(num, name="Solution"):
    blocks = blocks_of(lc_path(num))
    return ns_from(blocks[0])[name], ns_from(blocks[-1])[name]


def rand_str(alphabet, lo, hi):
    return "".join(R.choice(alphabet) for _ in range(R.randint(lo, hi)))


def occurrences(s, sub):
    return sum(s.startswith(sub, i) for i in range(len(s) - len(sub) + 1))


@case("1044-brute")
def _(h):
    brute, opt = (cls() for cls in pair(1044))
    assert brute.longestDupSubstring("banana") == "ana" and brute.longestDupSubstring("abcd") == ""
    assert brute.longestDupSubstring("aaaa") == "aaa"
    for _ in range(200):
        s = rand_str("abc", 1, 14)
        got, want = brute.longestDupSubstring(s), opt.longestDupSubstring(s)
        assert len(got) == len(want), (s, got, want)
        assert got == "" or occurrences(s, got) >= 2, (s, got)


@case("1392-brute")
def _(h):
    brute, opt = (cls() for cls in pair(1392))
    assert brute.longestPrefix("level") == "l" and brute.longestPrefix("ababab") == "abab"
    assert brute.longestPrefix("a") == "" and brute.longestPrefix("aaaa") == "aaa"
    for _ in range(300):
        s = rand_str("ab", 1, 14)
        assert brute.longestPrefix(s) == opt.longestPrefix(s), s


@case("187-brute")
def _(h):
    brute, opt = (cls() for cls in pair(187))
    s = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"
    assert sorted(brute.findRepeatedDnaSequences(s)) == ["AAAAACCCCC", "CCCCCAAAAA"]
    assert brute.findRepeatedDnaSequences("AAAAAAAAAAAAA") == ["AAAAAAAAAA"]
    assert brute.findRepeatedDnaSequences("ACGT") == []
    for _ in range(300):
        s = rand_str("AC", 0, 30)
        assert sorted(brute.findRepeatedDnaSequences(s)) == sorted(opt.findRepeatedDnaSequences(s)), s


@case("214-brute")
def _(h):
    brute, opt = (cls() for cls in pair(214))
    assert brute.shortestPalindrome("aacecaaa") == "aaacecaaa"
    assert brute.shortestPalindrome("abcd") == "dcbabcd" and brute.shortestPalindrome("") == ""
    for _ in range(300):
        s = rand_str("ab", 0, 10)
        assert brute.shortestPalindrome(s) == opt.shortestPalindrome(s), s


@case("2223-brute")
def _(h):
    brute, opt = (cls() for cls in pair(2223))
    assert brute.sumScores("babab") == 9 and brute.sumScores("azbazbzaz") == 14
    for _ in range(300):
        s = rand_str("ab", 1, 14)
        assert brute.sumScores(s) == opt.sumScores(s), s


@case("28-brute")
def _(h):
    brute, opt = (cls() for cls in pair(28))
    assert brute.strStr("sadbutsad", "sad") == 0 and brute.strStr("leetcode", "leeto") == -1
    for _ in range(300):
        hay, needle = rand_str("ab", 1, 12), rand_str("ab", 1, 4)
        got = brute.strStr(hay, needle)
        assert got == opt.strStr(hay, needle) == hay.find(needle), (hay, needle)


@case("647-brute")
def _(h):
    brute, opt = (cls() for cls in pair(647))
    assert brute.countSubstrings("abc") == 3 and brute.countSubstrings("aaa") == 6
    for _ in range(300):
        s = rand_str("ab", 1, 14)
        assert brute.countSubstrings(s) == opt.countSubstrings(s), s


@case("215-brute")
def _(h):
    brute, opt = (cls() for cls in pair(215))
    assert brute.findKthLargest([3, 2, 1, 5, 6, 4], 2) == 5
    assert brute.findKthLargest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
    for _ in range(300):
        nums = [R.randint(-8, 8) for _ in range(R.randint(1, 12))]
        k = R.randint(1, len(nums))
        assert brute.findKthLargest(nums[:], k) == opt.findKthLargest(nums[:], k), (nums, k)


@case("347-brute")
def _(h):
    brute, opt = (cls() for cls in pair(347))
    assert sorted(brute.topKFrequent([1, 1, 1, 2, 2, 3], 2)) == [1, 2]
    assert brute.topKFrequent([1], 1) == [1]
    for _ in range(300):
        nums = [R.randint(-4, 4) for _ in range(R.randint(1, 14))]
        freq = {v: nums.count(v) for v in nums}
        k = R.randint(1, len(freq))
        got, want = brute.topKFrequent(nums[:], k), opt.topKFrequent(nums[:], k)
        assert len(set(got)) == k and set(got) <= set(freq), (nums, k, got)
        assert sorted(freq[v] for v in got) == sorted(freq[v] for v in want), (nums, k, got, want)
        cutoff = sorted(freq.values(), reverse=True)[k - 1]
        assert all(freq[v] >= cutoff for v in got), (nums, k, got)


@case("1483-brute")
def _(h):
    brute_cls, opt_cls = pair(1483, "TreeAncestor")
    tree = brute_cls(7, [-1, 0, 0, 1, 1, 2, 2])
    assert tree.getKthAncestor(3, 1) == 1 and tree.getKthAncestor(5, 2) == 0
    assert tree.getKthAncestor(6, 3) == -1
    for _ in range(150):
        n = R.randint(1, 15)
        parent = [-1] + [R.randrange(i) for i in range(1, n)]
        brute, opt = brute_cls(n, parent[:]), opt_cls(n, parent[:])
        for _ in range(20):
            node, k = R.randrange(n), R.randint(1, n)
            assert brute.getKthAncestor(node, k) == opt.getKthAncestor(node, k), (parent, node, k)
