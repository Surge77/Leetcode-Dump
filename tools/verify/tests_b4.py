import random
from itertools import permutations, product
from math import gcd

from harness import case

R = random.Random(4)


def is_prime(x):
    return x > 1 and all(x % d for d in range(2, int(x ** 0.5) + 1))


@case(204)
def _(h):
    S = h.lc(204)["Solution"]()
    cnt = 0
    for n in range(0, 2000):
        assert S.countPrimes(n) == cnt, n
        cnt += is_prime(n)
    assert S.countPrimes(10**6) == 78498


@case(372)
def _(h):
    ns = h.lc(372)
    S = ns["Solution"]()
    assert S.superPow(2, [3]) == 8 and S.superPow(2, [1, 0]) == 1024 and S.superPow(1, [4, 3, 3, 8, 5, 2]) == 1
    for _ in range(300):
        a = R.randint(1, 2**31 - 1)
        b = [R.randint(1, 9)] + [R.randint(0, 9) for _ in range(R.randint(0, 12))]
        assert S.superPow(a, b) == pow(a, int("".join(map(str, b))), 1337)
        base, e, m = R.randint(0, 10**9), R.randint(0, 10**6), R.randint(1, 10**9)
        assert ns["mod_pow"](base, e, m) == pow(base, e, m)


@case(1922)
def _(h):
    S = h.lc(1922)["Solution"]()
    assert S.countGoodNumbers(1) == 5 and S.countGoodNumbers(4) == 400 and S.countGoodNumbers(50) == 564908303
    for n in range(1, 6):
        want = sum(1 for digs in product(range(10), repeat=n)
                   if all((d % 2 == 0) if i % 2 == 0 else d in (2, 3, 5, 7) for i, d in enumerate(digs)))
        assert S.countGoodNumbers(n) == want
    assert S.countGoodNumbers(10**15) == (pow(5, (10**15 + 1) // 2, 10**9 + 7) * pow(4, 10**15 // 2, 10**9 + 7)) % (10**9 + 7)


@case(2521)
def _(h):
    S = h.lc(2521)["Solution"]()
    assert S.distinctPrimeFactors([2, 4, 3, 7, 10, 6]) == 4 and S.distinctPrimeFactors([2, 4, 8, 16]) == 1
    for _ in range(300):
        nums = [R.randint(2, 1000) for _ in range(R.randint(1, 8))]
        want = {p for x in nums for p in range(2, x + 1) if x % p == 0 and is_prime(p)}
        assert S.distinctPrimeFactors(nums) == len(want), nums


@case(1359)
def _(h):
    S = h.lc(1359)["Solution"]()
    assert S.countOrders(1) == 1 and S.countOrders(2) == 6 and S.countOrders(3) == 90
    for n in range(1, 5):
        items = [(i, t) for i in range(n) for t in "PD"]
        want = sum(1 for p in permutations(items) if all(p.index((i, "P")) < p.index((i, "D")) for i in range(n)))
        assert S.countOrders(n) == want
    assert S.countOrders(500) == 764678010


@case(875)
def _(h):
    S = h.lc(875)["Solution"]()
    assert S.minEatingSpeed([3, 6, 7, 11], 8) == 4 and S.minEatingSpeed([30, 11, 23, 4, 20], 5) == 30
    for _ in range(300):
        piles = [R.randint(1, 30) for _ in range(R.randint(1, 6))]
        hrs = R.randint(len(piles), 40)
        want = next(k for k in range(1, 31) if sum(-(-p // k) for p in piles) <= hrs)
        assert S.minEatingSpeed(piles, hrs) == want


@case(1011)
def _(h):
    S = h.lc(1011)["Solution"]()
    assert S.shipWithinDays([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5) == 15 and S.shipWithinDays([1, 2, 3, 1, 1], 4) == 3
    for _ in range(300):
        w = [R.randint(1, 10) for _ in range(R.randint(1, 8))]
        d = R.randint(1, len(w))

        def days(cap):
            cnt, load = 1, 0
            for x in w:
                if load + x > cap:
                    cnt, load = cnt + 1, 0
                load += x
            return cnt
        want = next(c for c in range(max(w), sum(w) + 1) if days(c) <= d)
        assert S.shipWithinDays(w, d) == want


@case(410)
def _(h):
    S = h.lc(410)["Solution"]()
    assert S.splitArray([7, 2, 5, 10, 8], 2) == 18 and S.splitArray([1, 2, 3, 4, 5], 2) == 9
    for _ in range(300):
        a = [R.randint(0, 10) for _ in range(R.randint(1, 7))]
        k = R.randint(1, len(a))
        best = None
        for cuts in product((0, 1), repeat=len(a) - 1):
            if sum(cuts) != k - 1:
                continue
            parts, cur = [], a[0]
            for x, c in zip(a[1:], cuts):
                if c:
                    parts.append(cur)
                    cur = 0
                cur += x
            parts.append(cur)
            best = max(parts) if best is None else min(best, max(parts))
        assert S.splitArray(a, k) == best, (a, k)


@case(1201)
def _(h):
    S = h.lc(1201)["Solution"]()
    assert S.nthUglyNumber(3, 2, 3, 5) == 4 and S.nthUglyNumber(4, 2, 3, 4) == 6 and S.nthUglyNumber(5, 2, 11, 13) == 10
    assert S.nthUglyNumber(1000000000, 2, 217983653, 336916467) == 1999999984
    for _ in range(300):
        a, b, c = (R.randint(1, 12) for _ in range(3))
        n = R.randint(1, 30)
        seq = [x for x in range(1, 400) if x % a == 0 or x % b == 0 or x % c == 0]
        assert S.nthUglyNumber(n, a, b, c) == seq[n - 1], (n, a, b, c)
