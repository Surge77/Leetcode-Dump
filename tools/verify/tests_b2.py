import random
from functools import lru_cache
from itertools import combinations
from math import comb

from harness import case

R = random.Random(2)


def lis_n2(a):
    best = [1] * len(a)
    for i in range(len(a)):
        for j in range(i):
            if a[j] < a[i]:
                best[i] = max(best[i], best[j] + 1)
    return max(best, default=0)


@case(300)
def _(h):
    S = h.lc(300)["Solution"]()
    assert S.lengthOfLIS([10, 9, 2, 5, 3, 7, 101, 18]) == 4 and S.lengthOfLIS([7, 7, 7]) == 1
    for _ in range(400):
        a = [R.randint(-5, 10) for _ in range(R.randint(1, 12))]
        assert S.lengthOfLIS(a) == lis_n2(a), a


@case(354)
def _(h):
    S = h.lc(354)["Solution"]()
    assert S.maxEnvelopes([[5, 4], [6, 4], [6, 7], [2, 3]]) == 3 and S.maxEnvelopes([[1, 1]] * 3) == 1
    for _ in range(400):
        env = [[R.randint(1, 6), R.randint(1, 6)] for _ in range(R.randint(1, 9))]
        e = sorted(env)
        best = [1] * len(e)
        for i in range(len(e)):
            for j in range(i):
                if e[j][0] < e[i][0] and e[j][1] < e[i][1]:
                    best[i] = max(best[i], best[j] + 1)
        assert S.maxEnvelopes([x[:] for x in env]) == max(best), env


@case(62)
def _(h):
    S = h.lc(62)["Solution"]()
    for m in range(1, 9):
        for n in range(1, 9):
            assert S.uniquePaths(m, n) == comb(m + n - 2, m - 1)
            assert S.unique_paths_comb(m, n) == comb(m + n - 2, m - 1)


@case(64)
def _(h):
    S = h.lc(64)["Solution"]()
    assert S.minPathSum([[1, 3, 1], [1, 5, 1], [4, 2, 1]]) == 7
    for _ in range(300):
        m, n = R.randint(1, 5), R.randint(1, 5)
        g = [[R.randint(0, 9) for _ in range(n)] for _ in range(m)]

        @lru_cache(None)
        def f(i, j):
            if i == m - 1 and j == n - 1:
                return g[i][j]
            opts = [f(i + 1, j)] if i + 1 < m else []
            opts += [f(i, j + 1)] if j + 1 < n else []
            return g[i][j] + min(opts)
        assert S.minPathSum([r[:] for r in g]) == f(0, 0)


@case(1143)
def _(h):
    S = h.lc(1143)["Solution"]()
    assert S.longestCommonSubsequence("abcde", "ace") == 3 and S.longestCommonSubsequence("abc", "def") == 0
    for _ in range(300):
        a = "".join(R.choice("abc") for _ in range(R.randint(1, 8)))
        b = "".join(R.choice("abc") for _ in range(R.randint(1, 8)))
        want = max(k for k in range(min(len(a), len(b)) + 1)
                   if any("".join(c) in {"".join(d) for d in combinations(b, k)} for c in combinations(a, k)))
        assert S.longestCommonSubsequence(a, b) == want, (a, b)


@case(72)
def _(h):
    S = h.lc(72)["Solution"]()
    assert S.minDistance("horse", "ros") == 3 and S.minDistance("intention", "execution") == 5
    for _ in range(300):
        a = "".join(R.choice("ab") for _ in range(R.randint(0, 7)))
        b = "".join(R.choice("abc") for _ in range(R.randint(0, 7)))

        @lru_cache(None)
        def d(i, j):
            if i == len(a):
                return len(b) - j
            if j == len(b):
                return len(a) - i
            if a[i] == b[j]:
                return d(i + 1, j + 1)
            return 1 + min(d(i + 1, j), d(i, j + 1), d(i + 1, j + 1))
        assert S.minDistance(a, b) == d(0, 0), (a, b)


@case(115)
def _(h):
    S = h.lc(115)["Solution"]()
    assert S.numDistinct("rabbbit", "rabbit") == 3 and S.numDistinct("babgbag", "bag") == 5
    for _ in range(300):
        s = "".join(R.choice("ab") for _ in range(R.randint(1, 10)))
        t = "".join(R.choice("ab") for _ in range(R.randint(1, 4)))
        want = sum(1 for c in combinations(range(len(s)), len(t)) if "".join(s[i] for i in c) == t)
        assert S.numDistinct(s, t) == want, (s, t)


@case(329)
def _(h):
    S = h.lc(329)["Solution"]()
    assert S.longestIncreasingPath([[9, 9, 4], [6, 6, 8], [2, 1, 1]]) == 4
    assert S.longestIncreasingPath([[3, 4, 5], [3, 2, 6], [2, 2, 1]]) == 4
    for _ in range(300):
        m, n = R.randint(1, 5), R.randint(1, 5)
        g = [[R.randint(0, 6) for _ in range(n)] for _ in range(m)]

        @lru_cache(None)
        def f(i, j):
            best = 1
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                x, y = i + di, j + dj
                if 0 <= x < m and 0 <= y < n and g[x][y] > g[i][j]:
                    best = max(best, 1 + f(x, y))
            return best
        assert S.longestIncreasingPath(g) == max(f(i, j) for i in range(m) for j in range(n))
    big = [[r * 200 + c for c in range(200)] for r in range(200)]
    assert S.longestIncreasingPath(big) == 399  # deep path: no recursion limit issues
