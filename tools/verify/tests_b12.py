import random
from functools import lru_cache
from itertools import product
from math import comb

from harness import case

R = random.Random(12)
MOD = 10**9 + 7


def two_colourable(n, edges):
    return any(all(c[u] != c[v] for u, v in edges) for c in product((0, 1), repeat=n))


@case(785)
def _(h):
    S = h.lc(785)["Solution"]()
    assert not S.isBipartite([[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]]) and S.isBipartite([[1, 3], [0, 2], [1, 3], [0, 2]])
    for _ in range(300):
        n = R.randint(1, 8)
        edges = {tuple(sorted(R.sample(range(n), 2))) for _ in range(R.randint(0, 9))} if n > 1 else set()
        graph = [[] for _ in range(n)]
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
        assert S.isBipartite(graph) == two_colourable(n, edges)


@case(886)
def _(h):
    S = h.lc(886)["Solution"]()
    assert S.possibleBipartition(4, [[1, 2], [1, 3], [2, 4]]) and not S.possibleBipartition(3, [[1, 2], [1, 3], [2, 3]])
    for _ in range(300):
        n = R.randint(1, 8)
        edges = {tuple(sorted(R.sample(range(1, n + 1), 2))) for _ in range(R.randint(0, 9))} if n > 1 else set()
        assert S.possibleBipartition(n, [list(e) for e in edges]) == two_colourable(n + 1, edges)


@case(2223)
def _(h):
    S = h.lc(2223)["Solution"]()
    assert S.sumScores("babab") == 9 and S.sumScores("azbazbzaz") == 14
    for _ in range(300):
        s = "".join(R.choice("ab") for _ in range(R.randint(1, 15)))
        want = 0
        for i in range(len(s)):
            k = 0
            while i + k < len(s) and s[k] == s[i + k]:
                k += 1
            want += k
        assert S.sumScores(s) == want, s


@case(1044)
def _(h):
    S = h.lc(1044)["Solution"]()
    assert S.longestDupSubstring("banana") == "ana" and S.longestDupSubstring("abcd") == ""
    for _ in range(300):
        s = "".join(R.choice("ab") for _ in range(R.randint(2, 14)))
        best = max((L for L in range(1, len(s)) for i in range(len(s) - L + 1) if s.find(s[i:i + L], i + 1) != -1), default=0)
        got = S.longestDupSubstring(s)
        assert len(got) == best and (best == 0 or s.count(got) >= 2 or s.find(got, s.find(got) + 1) != -1), (s, got)


@case(187)
def _(h):
    S = h.lc(187)["Solution"]()
    assert sorted(S.findRepeatedDnaSequences("AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT")) == ["AAAAACCCCC", "CCCCCAAAAA"]
    for _ in range(200):
        s = "".join(R.choice("AC") for _ in range(R.randint(1, 30)))
        subs = [s[i:i + 10] for i in range(len(s) - 9)]
        assert sorted(S.findRepeatedDnaSequences(s)) == sorted({x for x in subs if subs.count(x) > 1})


@case(647)
def _(h):
    S = h.lc(647)["Solution"]()
    assert S.countSubstrings("abc") == 3 and S.countSubstrings("aaa") == 6
    for _ in range(400):
        s = "".join(R.choice("ab") for _ in range(R.randint(1, 14)))
        want = sum(1 for i in range(len(s)) for j in range(i + 1, len(s) + 1) if s[i:j] == s[i:j][::-1])
        assert S.countSubstrings(s) == want, s


KNIGHT = {0: [4, 6], 1: [6, 8], 2: [7, 9], 3: [4, 8], 4: [0, 3, 9], 5: [], 6: [0, 1, 7], 7: [2, 6], 8: [1, 3], 9: [2, 4]}


@case(935)
def _(h):
    S = h.lc(935)["Solution"]()
    assert S.knightDialer(1) == 10 and S.knightDialer(2) == 20 and S.knightDialer(3131) == 136006598
    for n in range(1, 60):
        dp = [1] * 10
        for _ in range(n - 1):
            dp = [sum(dp[b] for b in KNIGHT[a]) % MOD for a in range(10)]
        assert S.knightDialer(n) == sum(dp) % MOD


@case(1220)
def _(h):
    S = h.lc(1220)["Solution"]()
    nxt = {"a": "e", "e": "ai", "i": "aeou", "o": "iu", "u": "a"}
    assert S.countVowelPermutation(1) == 5 and S.countVowelPermutation(2) == 10 and S.countVowelPermutation(5) == 68
    for n in range(1, 60):
        dp = {v: 1 for v in "aeiou"}
        for _ in range(n - 1):
            new = dict.fromkeys("aeiou", 0)
            for v, c in dp.items():
                for w in nxt[v]:
                    new[w] = (new[w] + c) % MOD
            dp = new
        assert S.countVowelPermutation(n) == sum(dp.values()) % MOD


@case(96)
def _(h):
    ns = h.lc(96)
    S = ns["Solution"]()

    @lru_cache(None)
    def shapes(lo, hi):
        return 1 if lo >= hi else sum(shapes(lo, r - 1) * shapes(r + 1, hi) for r in range(lo, hi + 1))
    for n in range(1, 20):
        assert S.numTrees(n) == shapes(1, n) == comb(2 * n, n) // (n + 1) == S.num_trees_formula(n)


@case(878)
def _(h):
    S = h.lc(878)["Solution"]()
    assert S.nthMagicalNumber(1, 2, 3) == 2 and S.nthMagicalNumber(4, 2, 3) == 6
    assert S.nthMagicalNumber(10**9, 40000, 40000) == 999720007
    for _ in range(300):
        n, a, b = R.randint(1, 40), R.randint(1, 12), R.randint(1, 12)
        seq = [x for x in range(1, 1000) if x % a == 0 or x % b == 0]
        assert S.nthMagicalNumber(n, a, b) == seq[n - 1] % MOD


@case(292)
def _(h):
    S = h.lc(292)["Solution"]()
    win = [False] * 200
    for n in range(1, 200):
        win[n] = any(not win[n - k] for k in (1, 2, 3) if n - k >= 0)
    for n in range(1, 200):
        assert S.canWinNim(n) == win[n]


@case(1406)
def _(h):
    S = h.lc(1406)["Solution"]()
    assert S.stoneGameIII([1, 2, 3, 7]) == "Bob" and S.stoneGameIII([1, 2, 3, -9]) == "Alice" and S.stoneGameIII([1, 2, 3, 6]) == "Tie"
    for _ in range(300):
        v = [R.randint(-5, 5) for _ in range(R.randint(1, 10))]

        @lru_cache(None)
        def diff(i):  # best (current player - other) from i
            return 0 if i >= len(v) else max(sum(v[i:i + k]) - diff(i + k) for k in (1, 2, 3) if i + k <= len(v))
        d = diff(0)
        assert S.stoneGameIII(v) == ("Alice" if d > 0 else "Bob" if d < 0 else "Tie")
