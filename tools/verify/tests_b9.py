import random

from harness import case

R = random.Random(9)


@case(28)
def _(h):
    S = h.lc(28)["Solution"]()
    assert S.strStr("sadbutsad", "sad") == 0 and S.strStr("leetcode", "leeto") == -1
    for _ in range(500):
        hay = "".join(R.choice("ab") for _ in range(R.randint(1, 15)))
        needle = "".join(R.choice("ab") for _ in range(R.randint(1, 4)))
        assert S.strStr(hay, needle) == hay.find(needle), (hay, needle)


@case(214)
def _(h):
    S = h.lc(214)["Solution"]()
    assert S.shortestPalindrome("aacecaaa") == "aaacecaaa" and S.shortestPalindrome("abcd") == "dcbabcd"
    assert S.shortestPalindrome("") == ""
    for _ in range(500):
        s = "".join(R.choice("abc") for _ in range(R.randint(1, 10)))
        want = next(s[len(s) - k:][::-1] + s for k in range(len(s) + 1)
                    if (s[len(s) - k:][::-1] + s) == (s[len(s) - k:][::-1] + s)[::-1])
        assert S.shortestPalindrome(s) == want, s


@case(1392)
def _(h):
    S = h.lc(1392)["Solution"]()
    assert S.longestPrefix("level") == "l" and S.longestPrefix("ababab") == "abab"
    for _ in range(500):
        s = "".join(R.choice("ab") for _ in range(R.randint(1, 12)))
        want = next((s[:k] for k in range(len(s) - 1, 0, -1) if s[:k] == s[-k:]), "")
        assert S.longestPrefix(s) == want, s


@case(208)
def _(h):
    Trie = h.lc(208)["Trie"]
    for _ in range(100):
        t, words = Trie(), set()
        for _ in range(40):
            w = "".join(R.choice("abc") for _ in range(R.randint(1, 4)))
            op = R.randrange(3)
            if op == 0:
                t.insert(w)
                words.add(w)
            elif op == 1:
                assert t.search(w) == (w in words)
            else:
                assert t.startsWith(w) == any(x.startswith(w) for x in words)


@case(421)
def _(h):
    S = h.lc(421)["Solution"]()
    assert S.findMaximumXOR([3, 10, 5, 25, 2, 8]) == 28 and S.findMaximumXOR([0]) == 0
    for _ in range(300):
        a = [R.randint(0, 2**31 - 1) if R.random() < 0.5 else R.randint(0, 64) for _ in range(R.randint(1, 10))]
        assert S.findMaximumXOR(a) == max(x ^ y for x in a for y in a)


@case(51)
def _(h):
    S = h.lc(51)["Solution"]()
    expected = {1: 1, 2: 0, 3: 0, 4: 2, 5: 10, 6: 4, 7: 40, 8: 92}
    for n, cnt in expected.items():
        boards = S.solveNQueens(n)
        assert len(boards) == cnt and len({tuple(b) for b in boards}) == cnt
        for b in boards:
            qs = [(r, row.index("Q")) for r, row in enumerate(b)]
            assert all(row.count("Q") == 1 and len(row) == n for row in b)
            assert len({c for _, c in qs}) == n and len({r - c for r, c in qs}) == n and len({r + c for r, c in qs}) == n


@case(79)
def _(h):
    S = h.lc(79)["Solution"]()
    board = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
    assert S.exist([r[:] for r in board], "ABCCED") and S.exist([r[:] for r in board], "SEE")
    assert not S.exist([r[:] for r in board], "ABCB")
    for _ in range(300):
        m, n = R.randint(1, 4), R.randint(1, 4)
        g = [[R.choice("ab") for _ in range(n)] for _ in range(m)]
        word = "".join(R.choice("ab") for _ in range(R.randint(1, 6)))

        def found(i, j, k, used):
            if g[i][j] != word[k]:
                return False
            if k == len(word) - 1:
                return True
            used = used | {(i, j)}
            return any(found(x, y, k + 1, used) for x, y in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1))
                       if 0 <= x < m and 0 <= y < n and (x, y) not in used)
        want = any(found(i, j, 0, frozenset()) for i in range(m) for j in range(n))
        assert S.exist([r[:] for r in g], word) == want, (g, word)


@case(836)
def _(h):
    S = h.lc(836)["Solution"]()
    assert S.isRectangleOverlap([0, 0, 2, 2], [1, 1, 3, 3]) and not S.isRectangleOverlap([0, 0, 1, 1], [1, 0, 2, 1])
    assert not S.isRectangleOverlap([0, 0, 1, 1], [2, 2, 3, 3])
    for _ in range(500):
        def rect():
            x1, y1 = R.randint(-5, 5), R.randint(-5, 5)
            return [x1, y1, x1 + R.randint(1, 5), y1 + R.randint(1, 5)]
        a, b = rect(), rect()
        cells = lambda r: {(x, y) for x in range(r[0], r[2]) for y in range(r[1], r[3])}
        assert S.isRectangleOverlap(a, b) == bool(cells(a) & cells(b)), (a, b)
