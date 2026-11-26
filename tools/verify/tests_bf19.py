"""Brute-force backfill bf19: each note's first python block (brute force) vs its last (optimized)."""
import random

from harness import blocks_of, case, lc_path, ns_from

R = random.Random(1901)
ROUNDS = 150


def pair(num):
    blocks = blocks_of(lc_path(num))
    return ns_from(blocks[0])["Solution"](), ns_from(blocks[-1])["Solution"]()


def is_valid_subsequence(words, groups, got):
    """`got` must be a subsequence of words whose matching groups alternate."""
    picked, i = [], 0
    for w in got:
        while i < len(words) and words[i] != w:
            i += 1
        if i == len(words):
            return False
        picked.append(groups[i])
        i += 1
    return all(a != b for a, b in zip(picked, picked[1:]))


@case("2900-brute")
def _(h):
    brute, opt = pair(2900)
    assert brute.getLongestSubsequence(["e", "a", "b"], [0, 0, 1]) in (["e", "b"], ["a", "b"])
    assert brute.getLongestSubsequence(["a", "b", "c", "d"], [1, 0, 1, 1]) in (["a", "b", "c"], ["a", "b", "d"])
    for _ in range(ROUNDS):
        n = R.randint(1, 10)
        words = [chr(ord("a") + i) for i in range(n)]
        groups = [R.randint(0, 1) for _ in range(n)]
        got, want = brute.getLongestSubsequence(words[:], groups[:]), opt.getLongestSubsequence(words[:], groups[:])
        assert is_valid_subsequence(words, groups, got) and len(got) == len(want), (words, groups)


@case("5-brute")
def _(h):
    brute, opt = pair(5)
    assert brute.longestPalindrome("babad") in ("bab", "aba") and brute.longestPalindrome("cbbd") == "bb"
    assert brute.longestPalindrome("a") == "a"
    for _ in range(ROUNDS):
        s = "".join(R.choice("abc") for _ in range(R.randint(1, 12)))
        got, want = brute.longestPalindrome(s), opt.longestPalindrome(s)
        assert got in s and got == got[::-1] and len(got) == len(want), s


@case("75-brute")
def _(h):
    brute, opt = pair(75)
    nums = [2, 0, 2, 1, 1, 0]
    brute.sortColors(nums)
    assert nums == [0, 0, 1, 1, 2, 2]
    nums = [2, 0, 1]
    brute.sortColors(nums)
    assert nums == [0, 1, 2]
    for _ in range(ROUNDS):
        arr = [R.randint(0, 2) for _ in range(R.randint(1, 12))]
        a, b = arr[:], arr[:]
        brute.sortColors(a)
        opt.sortColors(b)
        assert a == b == sorted(arr), arr


@case("9-brute")
def _(h):
    brute, opt = pair(9)
    assert brute.isPalindrome(121) is True and brute.isPalindrome(-121) is False
    assert brute.isPalindrome(10) is False and brute.isPalindrome(0) is True
    for x in list(range(-30, 1300)) + [R.randint(0, 2 ** 31 - 1) for _ in range(ROUNDS)]:
        assert brute.isPalindrome(x) == opt.isPalindrome(x), x


def random_graph(n, m):
    edges = set()
    while len(edges) < m:
        a, b = R.sample(range(n), 2)
        edges.add((min(a, b), max(a, b)))
    return [list(e) for e in edges]


@case("1319-brute")
def _(h):
    brute, opt = pair(1319)
    assert brute.makeConnected(4, [[0, 1], [0, 2], [1, 2]]) == 1
    assert brute.makeConnected(6, [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3]]) == 2
    assert brute.makeConnected(6, [[0, 1], [0, 2], [0, 3], [1, 2]]) == -1
    for _ in range(ROUNDS):
        n = R.randint(1, 8)
        m = R.randint(0, min(n * (n - 1) // 2, 10))
        edges = random_graph(n, m) if n > 1 else []
        assert brute.makeConnected(n, [e[:] for e in edges]) == opt.makeConnected(n, [e[:] for e in edges]), (n, edges)


@case("1584-brute")
def _(h):
    brute, opt = pair(1584)
    assert brute.minCostConnectPoints([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]) == 20
    assert brute.minCostConnectPoints([[3, 12], [-2, 5], [-4, 1]]) == 18
    assert brute.minCostConnectPoints([[0, 0]]) == 0
    for _ in range(ROUNDS):
        n = R.randint(1, 6)
        pts = []
        while len(pts) < n:
            p = [R.randint(-8, 8), R.randint(-8, 8)]
            if p not in pts:
                pts.append(p)
        assert brute.minCostConnectPoints([p[:] for p in pts]) == opt.minCostConnectPoints([p[:] for p in pts]), pts


@case("684-brute")
def _(h):
    brute, opt = pair(684)
    assert brute.findRedundantConnection([[1, 2], [1, 3], [2, 3]]) == [2, 3]
    assert brute.findRedundantConnection([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]) == [1, 4]
    for _ in range(ROUNDS):
        n = R.randint(3, 9)
        labels = list(range(1, n + 1))
        R.shuffle(labels)
        edges = [[labels[R.randrange(i)], labels[i]] for i in range(1, n)]
        extra = R.sample(labels, 2)
        edges.append(extra)
        R.shuffle(edges)
        assert brute.findRedundantConnection([e[:] for e in edges]) == opt.findRedundantConnection([e[:] for e in edges]), edges
