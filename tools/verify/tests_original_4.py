"""Checks for the notes that existed before the Infosys expansion (part 4 of 4).

Shared helpers: helpers_original.py.
"""
from helpers_original import (  # noqa: F401
    Counter,
    R,
    case,
    permutations,
    product,
    solvers,
)


@case(1920)
def _(h):
    for S in solvers(1920):
        for n in range(1, 12):
            nums = list(range(n))
            R.shuffle(nums)
            assert S.buildArray(nums[:]) == [nums[x] for x in nums]


@case(2094)
def _(h):
    for S in solvers(2094):
        for _ in range(200):
            digits = [R.randint(0, 9) for _ in range(R.randint(3, 7))]
            want = sorted({int("".join(map(str, p))) for p in permutations(digits, 3) if p[0] != 0 and p[2] % 2 == 0})
            assert S.findEvenNumbers(digits) == want


@case(2918)
def _(h):
    for S in solvers(2918):
        assert S.minSum([3, 2, 0, 1, 0], [6, 5, 0]) == 12 and S.minSum([2, 0, 2, 0], [1, 4]) == -1
        for _ in range(300):
            a = [R.choice((0, 0, 1, 2, 3)) for _ in range(R.randint(1, 4))]
            b = [R.choice((0, 0, 1, 2, 3)) for _ in range(R.randint(1, 4))]
            za, zb = a.count(0), b.count(0)
            # a zero may become any positive integer; 1..40 covers every reachable minimum here
            sums_a = {sum(a) + sum(v) for v in product(range(1, 41), repeat=za)}
            sums_b = {sum(b) + sum(v) for v in product(range(1, 41), repeat=zb)}
            common = sums_a & sums_b
            assert S.minSum(a, b) == (min(common) if common else -1), (a, b)


@case(1)
def _(h):
    for S in solvers(1):
        for _ in range(300):
            nums = [R.randint(-9, 9) for _ in range(R.randint(2, 10))]
            i, j = R.sample(range(len(nums)), 2)
            target = nums[i] + nums[j]
            a, b = S.twoSum(nums, target)
            assert a != b and nums[a] + nums[b] == target


@case(1399)
def _(h):
    for S in solvers(1399):
        for n in range(1, 400):
            groups = Counter(sum(map(int, str(x))) for x in range(1, n + 1))
            assert S.countLargestGroup(n) == list(groups.values()).count(max(groups.values()))


@case(217)
def _(h):
    for S in solvers(217):
        for _ in range(300):
            a = [R.randint(0, 12) for _ in range(R.randint(1, 8))]
            assert S.containsDuplicate(a) == (len(set(a)) < len(a))


@case(2176)
def _(h):
    for S in solvers(2176):
        for _ in range(300):
            a = [R.randint(1, 3) for _ in range(R.randint(1, 12))]
            k = R.randint(1, 8)
            want = sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] == a[j] and i * j % k == 0)
            assert S.countPairs(a, k) == want


@case(242)
def _(h):
    for S in solvers(242):
        for _ in range(300):
            s = "".join(R.choice("abc") for _ in range(R.randint(1, 6)))
            t = "".join(R.sample(s, len(s))) if R.random() < 0.5 else "".join(R.choice("abc") for _ in range(R.randint(1, 6)))
            assert S.isAnagram(s, t) == (sorted(s) == sorted(t))


@case(49)
def _(h):
    for S in solvers(49):
        for _ in range(200):
            words = ["".join(R.choice("ab") for _ in range(R.randint(0, 3))) for _ in range(R.randint(1, 8))]
            got = sorted(sorted(g) for g in S.groupAnagrams(words))
            by_key = {}
            for w in words:
                by_key.setdefault("".join(sorted(w)), []).append(w)
            assert got == sorted(sorted(g) for g in by_key.values())


@case(2563)
def _(h):
    for S in solvers(2563):
        for _ in range(300):
            a = [R.randint(-9, 9) for _ in range(R.randint(1, 10))]
            lo = R.randint(-15, 10)
            hi = lo + R.randint(0, 10)
            want = sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if lo <= a[i] + a[j] <= hi)
            assert S.countFairPairs(a, lo, hi) == want


@case(704)
def _(h):
    for S in solvers(704):
        for _ in range(300):
            a = sorted(R.sample(range(-20, 20), R.randint(1, 10)))
            t = R.randint(-21, 21)
            assert S.search(a, t) == (a.index(t) if t in a else -1)


@case(238)
def _(h):
    for S in solvers(238):
        for _ in range(300):
            a = [R.randint(-3, 3) for _ in range(R.randint(2, 8))]
            want = []
            for i in range(len(a)):
                p = 1
                for j, x in enumerate(a):
                    if j != i:
                        p *= x
                want.append(p)
            assert S.productExceptSelf(a) == want


@case(2894)
def _(h):
    for S in solvers(2894):
        for n in range(1, 60):
            for m in range(1, 12):
                want = sum(x for x in range(1, n + 1) if x % m) - sum(x for x in range(1, n + 1) if x % m == 0)
                assert S.differenceOfSums(n, m) == want


@case(38)
def _(h):
    seq = ["1", "11", "21", "1211", "111221", "312211", "13112221", "1113213211", "31131211131221"]
    for S in solvers(38):
        for n, want in enumerate(seq, 1):
            assert S.countAndSay(n) == want


@case(2444)
def _(h):
    for S in solvers(2444):
        assert S.countSubarrays([1, 3, 5, 2, 7, 5], 1, 5) == 2 and S.countSubarrays([1, 1, 1, 1], 1, 1) == 10
        for _ in range(300):
            a = [R.randint(1, 5) for _ in range(R.randint(1, 10))]
            lo = R.randint(1, 5)
            hi = R.randint(lo, 5)
            want = sum(1 for i in range(len(a)) for j in range(i, len(a)) if min(a[i:j + 1]) == lo and max(a[i:j + 1]) == hi)
            assert S.countSubarrays(a, lo, hi) == want


@case(2799)
def _(h):
    for S in solvers(2799):
        for _ in range(300):
            a = [R.randint(1, 4) for _ in range(R.randint(1, 10))]
            k = len(set(a))
            assert S.countCompleteSubarrays(a) == sum(1 for i in range(len(a)) for j in range(i, len(a)) if len(set(a[i:j + 1])) == k)


@case(3392)
def _(h):
    for S in solvers(3392):
        assert S.countSubarrays([1, 2, 1, 4, 1]) == 1 and S.countSubarrays([1, 1, 1]) == 0
        for _ in range(300):
            a = [R.randint(-6, 6) for _ in range(R.randint(3, 10))]
            assert S.countSubarrays(a) == sum(1 for i in range(len(a) - 2) if a[i] + a[i + 2] == a[i + 1] / 2)


@case(347)
def _(h):
    for S in solvers(347):
        for _ in range(300):
            a = [R.randint(1, 6) for _ in range(R.randint(1, 15))]
            cnt = Counter(a)
            k = R.randint(1, len(cnt))
            got = S.topKFrequent(a, k)
            assert len(got) == k == len(set(got))
            assert sorted((cnt[x] for x in got), reverse=True) == sorted(cnt.values(), reverse=True)[:k]


@case(125)
def _(h):
    for S in solvers(125):
        assert S.isPalindrome("A man, a plan, a canal: Panama") and not S.isPalindrome("race a car") and S.isPalindrome(" ")
        for _ in range(300):
            s = "".join(R.choice("aA b,1") for _ in range(R.randint(1, 10)))
            clean = [c.lower() for c in s if c.isalnum()]
            assert S.isPalindrome(s) == (clean == clean[::-1]), s


@case(1550)
def _(h):
    for S in solvers(1550):
        for _ in range(300):
            a = [R.randint(1, 6) for _ in range(R.randint(1, 10))]
            assert S.threeConsecutiveOdds(a) == any(all(x % 2 for x in a[i:i + 3]) for i in range(len(a) - 2))


@case(26)
def _(h):
    for S in solvers(26):
        for _ in range(300):
            a = sorted(R.randint(-5, 5) for _ in range(R.randint(1, 12)))
            k = S.removeDuplicates(a_copy := a[:])
            assert a_copy[:k] == sorted(set(a))


@case(283)
def _(h):
    for S in solvers(283):
        for _ in range(300):
            a = [R.choice((0, 0, 1, 2, 3)) for _ in range(R.randint(1, 10))]
            b = a[:]
            S.moveZeroes(b)
            assert b == [x for x in a if x] + [0] * a.count(0)


@case(2900)
def _(h):
    for S in solvers(2900):
        for _ in range(300):
            n = R.randint(1, 10)
            words = [f"w{i}" for i in range(n)]
            groups = [R.randint(0, 1) for _ in range(n)]
            got = S.getLongestSubsequence(words, groups)
            idx = [words.index(w) for w in got]
            assert idx == sorted(set(idx)) and all(groups[a] != groups[b] for a, b in zip(idx, idx[1:]))
            assert len(got) == 1 + sum(1 for a, b in zip(groups, groups[1:]) if a != b)


@case(75)
def _(h):
    for S in solvers(75):
        for _ in range(300):
            a = [R.randint(0, 2) for _ in range(R.randint(1, 12))]
            b = a[:]
            S.sortColors(b)
            assert b == sorted(a)


@case(9)
def _(h):
    for S in solvers(9):
        for x in list(range(-20, 2000)) + [R.randint(-2**31, 2**31 - 1) for _ in range(300)]:
            assert S.isPalindrome(x) == (str(x) == str(x)[::-1]), x


@case("3335-mod")
def _(h):
    # answers far beyond 10^9 + 7, compared with exact big-integer counting
    for S in solvers(3335):
        for s, t in (("zzzzz", 5000), ("abcxyz", 3000)):
            cnt = [0] * 26
            for c in s:
                cnt[ord(c) - 97] += 1
            for _ in range(t):
                cnt = [cnt[25], cnt[0] + cnt[25]] + cnt[1:25]
            assert sum(cnt) > 10**9 + 7
            assert S.lengthAfterTransformations(s, t) == sum(cnt) % (10**9 + 7)
