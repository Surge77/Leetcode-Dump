import random
from functools import lru_cache
from itertools import product

from harness import case

R = random.Random(1)


def subsets(n):
    return range(1 << n)


@case(198)
def _(h):
    S = h.lc(198)["Solution"]()
    assert S.rob([1, 2, 3, 1]) == 4 and S.rob([2, 7, 9, 3, 1]) == 12
    for _ in range(300):
        a = [R.randint(0, 20) for _ in range(R.randint(1, 10))]
        best = max(sum(a[i] for i in range(len(a)) if m >> i & 1)
                   for m in subsets(len(a)) if m & (m >> 1) == 0)
        assert S.rob(a) == best, a


@case(139)
def _(h):
    S = h.lc(139)["Solution"]()
    assert S.wordBreak("leetcode", ["leet", "code"])
    assert S.wordBreak("applepenapple", ["apple", "pen"])
    assert not S.wordBreak("catsandog", ["cats", "dog", "sand", "and", "cat"])
    for _ in range(300):
        words = list({"".join(R.choice("ab") for _ in range(R.randint(1, 3))) for _ in range(3)})
        s = "".join(R.choice("ab") for _ in range(R.randint(1, 10)))

        @lru_cache(None)
        def ok(i):
            return i == len(s) or any(s.startswith(w, i) and ok(i + len(w)) for w in words)
        assert S.wordBreak(s, words) == ok(0), (s, words)


@case(309)
def _(h):
    S = h.lc(309)["Solution"]()
    assert S.maxProfit([1, 2, 3, 0, 2]) == 3 and S.maxProfit([1]) == 0
    for _ in range(300):
        p = [R.randint(0, 10) for _ in range(R.randint(1, 9))]

        @lru_cache(None)
        def f(i, holding):
            if i >= len(p):
                return 0
            if holding:
                return max(f(i + 1, True), p[i] + f(i + 2, False))
            return max(f(i + 1, False), -p[i] + f(i + 1, True))
        assert S.maxProfit(p) == f(0, False), p


@case(1235)
def _(h):
    S = h.lc(1235)["Solution"]()
    assert S.jobScheduling([1, 2, 3, 3], [3, 4, 5, 6], [50, 10, 40, 70]) == 120
    assert S.jobScheduling([1, 2, 3, 4, 6], [3, 5, 10, 6, 9], [20, 20, 100, 70, 60]) == 150
    for _ in range(300):
        n = R.randint(1, 8)
        st = [R.randint(1, 10) for _ in range(n)]
        en = [s + R.randint(1, 5) for s in st]
        pr = [R.randint(1, 20) for _ in range(n)]
        best = 0
        for m in subsets(n):
            chosen = sorted((st[i], en[i]) for i in range(n) if m >> i & 1)
            if all(chosen[k][1] <= chosen[k + 1][0] for k in range(len(chosen) - 1)):
                best = max(best, sum(pr[i] for i in range(n) if m >> i & 1))
        assert S.jobScheduling(st, en, pr) == best


@case(322)
def _(h):
    S = h.lc(322)["Solution"]()
    assert S.coinChange([1, 2, 5], 11) == 3 and S.coinChange([2], 3) == -1 and S.coinChange([1], 0) == 0
    for _ in range(300):
        coins = list({R.randint(1, 12) for _ in range(R.randint(1, 4))})
        amt = R.randint(0, 40)
        dist, frontier, seen = None, {0}, {0}
        steps = 0
        while frontier:
            if amt in frontier:
                dist = steps
                break
            frontier = {v + c for v in frontier for c in coins if v + c <= amt} - seen
            seen |= frontier
            steps += 1
        assert S.coinChange(coins, amt) == (-1 if dist is None else dist)


@case(518)
def _(h):
    S = h.lc(518)["Solution"]()
    assert S.change(5, [1, 2, 5]) == 4 and S.change(3, [2]) == 0 and S.change(10, [10]) == 1
    for _ in range(300):
        coins = list({R.randint(1, 8) for _ in range(R.randint(1, 4))})
        amt = R.randint(0, 25)

        @lru_cache(None)
        def ways(i, a):
            if a == 0:
                return 1
            if i == len(coins) or a < 0:
                return 0
            return ways(i, a - coins[i]) + ways(i + 1, a)
        assert S.change(amt, coins) == ways(0, amt)


@case(416)
def _(h):
    S = h.lc(416)["Solution"]()
    for fn in ("canPartition", "can_partition_bitset"):
        f = getattr(S, fn)
        assert f([1, 5, 11, 5]) and not f([1, 2, 3, 5])
        for _ in range(300):
            a = [R.randint(1, 15) for _ in range(R.randint(1, 10))]
            tot = sum(a)
            want = any(2 * sum(a[i] for i in range(len(a)) if m >> i & 1) == tot for m in subsets(len(a)))
            assert f(a) == want, (fn, a)


@case(494)
def _(h):
    S = h.lc(494)["Solution"]()
    assert S.findTargetSumWays([1, 1, 1, 1, 1], 3) == 5 and S.findTargetSumWays([1], 1) == 1
    for _ in range(300):
        a = [R.randint(0, 6) for _ in range(R.randint(1, 10))]
        t = R.randint(-12, 12)
        want = sum(1 for signs in product((1, -1), repeat=len(a)) if sum(x * s for x, s in zip(a, signs)) == t)
        assert S.findTargetSumWays(a, t) == want, (a, t)


@case(1155)
def _(h):
    S = h.lc(1155)["Solution"]()
    assert S.numRollsToTarget(1, 6, 3) == 1 and S.numRollsToTarget(2, 6, 7) == 6
    assert S.numRollsToTarget(30, 30, 500) == 222616187
    for _ in range(200):
        n, k = R.randint(1, 4), R.randint(1, 6)
        t = R.randint(1, 24)
        want = sum(1 for r in product(range(1, k + 1), repeat=n) if sum(r) == t)
        assert S.numRollsToTarget(n, k, t) == want
