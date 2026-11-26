"""Gap notes g02: hashing, intervals, linked list, GCD, binary search, prefix sum, sliding window, stack.

Each note has a brute force and an optimized block; both must agree on random inputs and on
LeetCode's examples, and the optimized one is run once at max constraints.
"""
import random

from harness import case
from tests_b10 import timed_call

R = random.Random(202)


def both(h, num, name="Solution"):
    brute, opt = h.lc_all(num, name)
    return brute, opt


def pair(h, num):
    brute, opt = both(h, num)
    return brute["Solution"](), opt["Solution"]()


@case(409)
def _(h):
    brute, opt = pair(h, 409)
    assert opt.longestPalindrome("abccccdd") == 7 and opt.longestPalindrome("a") == 1
    for _ in range(300):
        s = "".join(R.choice("abcAB") for _ in range(R.randint(1, 14)))
        assert brute.longestPalindrome(s) == opt.longestPalindrome(s), s
    timed_call(lambda: opt.longestPalindrome("".join(R.choice("abcdefABCDEF") for _ in range(2000))), 1)


@case(1207)
def _(h):
    brute, opt = pair(h, 1207)
    assert opt.uniqueOccurrences([1, 2, 2, 1, 1, 3]) is True
    assert opt.uniqueOccurrences([1, 2]) is False
    assert opt.uniqueOccurrences([-3, 0, 1, -3, 1, 1, 1, -3, 10, 0]) is True
    for _ in range(300):
        arr = [R.randint(-4, 4) for _ in range(R.randint(1, 20))]
        assert brute.uniqueOccurrences(arr) == opt.uniqueOccurrences(arr), arr
    timed_call(lambda: opt.uniqueOccurrences([R.randint(-1000, 1000) for _ in range(1000)]), 1)


@case(1657)
def _(h):
    brute, opt = pair(h, 1657)
    assert opt.closeStrings("abc", "bca") is True
    assert opt.closeStrings("a", "aa") is False
    assert opt.closeStrings("cabbba", "abbccc") is True
    assert opt.closeStrings("aab", "bbc") is False
    for _ in range(300):
        w1 = "".join(R.choice("abc") for _ in range(R.randint(1, 5)))
        if R.random() < 0.5:
            letters = list("abc")
            R.shuffle(letters)
            mapping = dict(zip("abc", letters))
            chars = [mapping[c] for c in w1]
            R.shuffle(chars)
            w2 = "".join(chars)
            if R.random() < 0.3 and w2:
                w2 = w2[:-1] + R.choice("abc")
        else:
            w2 = "".join(R.choice("abc") for _ in range(len(w1) + R.choice((0, 0, 1))))
        assert brute.closeStrings(w1, w2) == opt.closeStrings(w1, w2), (w1, w2)
    big1 = "".join(R.choice("abcdefghij") for _ in range(100_000))
    big2 = "".join(R.sample(big1, len(big1)))
    assert opt.closeStrings(big1, big2) is True
    timed_call(lambda: opt.closeStrings(big1, big2), 2)


@case(2215)
def _(h):
    brute, opt = pair(h, 2215)

    def norm(res):
        return [sorted(res[0]), sorted(res[1])]

    assert norm(opt.findDifference([1, 2, 3], [2, 4, 6])) == [[1, 3], [4, 6]]
    assert norm(opt.findDifference([1, 2, 3, 3], [1, 1, 2, 2])) == [[3], []]
    for _ in range(300):
        a = [R.randint(-6, 6) for _ in range(R.randint(1, 12))]
        b = [R.randint(-6, 6) for _ in range(R.randint(1, 12))]
        got, want = opt.findDifference(a[:], b[:]), brute.findDifference(a[:], b[:])
        assert norm(got) == norm(want), (a, b)
        assert len(set(got[0])) == len(got[0]) and len(set(got[1])) == len(got[1])
    big = [R.randint(-1000, 1000) for _ in range(1000)]
    timed_call(lambda: opt.findDifference(big, big[::-1]), 1)


@case(2352)
def _(h):
    brute, opt = pair(h, 2352)
    assert opt.equalPairs([[3, 2, 1], [1, 7, 6], [2, 7, 7]]) == 1
    assert opt.equalPairs([[3, 1, 2, 2], [1, 4, 4, 5], [2, 4, 2, 2], [2, 4, 2, 2]]) == 3
    for _ in range(300):
        n = R.randint(1, 5)
        grid = [[R.randint(1, 2) for _ in range(n)] for _ in range(n)]
        assert brute.equalPairs(grid) == opt.equalPairs(grid), grid
    n = 200
    grid = [[R.randint(1, 2) for _ in range(n)] for _ in range(n)]
    timed_call(lambda: opt.equalPairs(grid), 2)


@case(759)
def _(h):
    brute, opt = pair(h, 759)

    def build(ns, schedule):
        return [[ns["Interval"](a, b) for a, b in emp] for emp in schedule]

    def run(sol, ns, schedule):
        return [[iv.start, iv.end] for iv in sol.employeeFreeTime(build(ns, schedule))]

    nsb, nso = h.lc_all(759, "Solution")
    assert run(opt, nso, [[[1, 2], [5, 6]], [[1, 3]], [[4, 10]]]) == [[3, 4]]
    assert run(opt, nso, [[[1, 3], [6, 7]], [[2, 4]], [[2, 5], [9, 12]]]) == [[5, 6], [7, 9]]
    for _ in range(300):
        schedule = []
        for _ in range(R.randint(1, 4)):
            points = sorted(R.sample(range(0, 25), R.choice((2, 4, 6))))
            emp = [[points[i], points[i + 1]] for i in range(0, len(points), 2)]
            schedule.append(emp)
        assert run(brute, nsb, schedule) == run(opt, nso, schedule), schedule
    big = []
    for _ in range(50):
        points = sorted(R.sample(range(0, 10**8), 100))
        big.append([[points[i], points[i + 1]] for i in range(0, 100, 2)])
    timed_call(lambda: run(opt, nso, big), 1)


@case(24)
def _(h):
    brute, opt = pair(h, 24)
    py = h.list_to_py
    assert py(opt.swapPairs(h.build_list([1, 2, 3, 4]))) == [2, 1, 4, 3]
    assert py(opt.swapPairs(h.build_list([]))) == []
    assert py(opt.swapPairs(h.build_list([1]))) == [1]
    assert py(opt.swapPairs(h.build_list([1, 2, 3]))) == [2, 1, 3]
    for _ in range(200):
        vals = [R.randint(0, 100) for _ in range(R.randint(0, 12))]
        assert py(brute.swapPairs(h.build_list(vals))) == py(opt.swapPairs(h.build_list(vals))), vals
    head = h.build_list([1, 2, 3, 4, 5])
    originals = {id(n) for n in iter_nodes(head)}
    res = opt.swapPairs(head)
    assert {id(n) for n in iter_nodes(res)} == originals, "optimized version must re-link, not copy"
    timed_call(lambda: opt.swapPairs(h.build_list(list(range(100)))), 1)


def iter_nodes(head):
    while head:
        yield head
        head = head.next


@case(2130)
def _(h):
    brute, opt = pair(h, 2130)
    assert opt.pairSum(h.build_list([5, 4, 2, 1])) == 6
    assert opt.pairSum(h.build_list([4, 2, 2, 3])) == 7
    assert opt.pairSum(h.build_list([1, 100000])) == 100001
    for _ in range(300):
        vals = [R.randint(1, 100) for _ in range(2 * R.randint(1, 8))]
        assert brute.pairSum(h.build_list(vals)) == opt.pairSum(h.build_list(vals)), vals
    big = [R.randint(1, 10**5) for _ in range(100_000)]
    assert opt.pairSum(h.build_list(big)) == brute.pairSum(h.build_list(big))
    timed_call(lambda: opt.pairSum(h.build_list(big)), 2)


@case(1071)
def _(h):
    brute, opt = pair(h, 1071)
    assert opt.gcdOfStrings("ABCABC", "ABC") == "ABC"
    assert opt.gcdOfStrings("ABABAB", "ABAB") == "AB"
    assert opt.gcdOfStrings("LEET", "CODE") == ""
    for _ in range(300):
        base = "".join(R.choice("AB") for _ in range(R.randint(1, 3)))
        if R.random() < 0.7:
            s1, s2 = base * R.randint(1, 6), base * R.randint(1, 6)
        else:
            s1 = "".join(R.choice("AB") for _ in range(R.randint(1, 8)))
            s2 = "".join(R.choice("AB") for _ in range(R.randint(1, 8)))
        assert brute.gcdOfStrings(s1, s2) == opt.gcdOfStrings(s1, s2), (s1, s2)
    timed_call(lambda: opt.gcdOfStrings("AB" * 500, "AB" * 499 + "AB"), 1)


@case(278)
def _(h):
    brute, opt = both(h, 278)
    calls = []

    def install(ns, bad):
        def is_bad(version):
            calls.append(version)
            return version >= bad
        ns["isBadVersion"] = is_bad

    sol_b, sol_o = brute["Solution"](), opt["Solution"]()
    install(opt, 4)
    assert sol_o.firstBadVersion(5) == 4
    install(opt, 1)
    assert sol_o.firstBadVersion(1) == 1
    for _ in range(300):
        n = R.randint(1, 40)
        bad = R.randint(1, n)
        install(brute, bad)
        install(opt, bad)
        assert sol_b.firstBadVersion(n) == sol_o.firstBadVersion(n) == bad, (n, bad)
    n = 2**31 - 1
    install(opt, 1_234_567_890)
    calls.clear()
    timed_call(lambda: sol_o.firstBadVersion(n), 1)
    assert sol_o.firstBadVersion(n) == 1_234_567_890 and len(calls) <= 2 * 32


@case(374)
def _(h):
    brute, opt = both(h, 374)
    sol_b, sol_o = brute["Solution"](), opt["Solution"]()
    calls = []

    def install(ns, pick):
        def guess(num):
            calls.append(num)
            return 0 if num == pick else (-1 if num > pick else 1)
        ns["guess"] = guess

    install(opt, 6)
    assert sol_o.guessNumber(10) == 6
    install(opt, 1)
    assert sol_o.guessNumber(1) == 1 and sol_o.guessNumber(2) == 1
    for _ in range(300):
        n = R.randint(1, 40)
        pick = R.randint(1, n)
        install(brute, pick)
        install(opt, pick)
        assert sol_b.guessNumber(n) == sol_o.guessNumber(n) == pick, (n, pick)
    n = 2**31 - 1
    install(opt, 987_654_321)
    calls.clear()
    assert sol_o.guessNumber(n) == 987_654_321 and len(calls) <= 32
    install(opt, n)
    assert sol_o.guessNumber(n) == n


@case(658)
def _(h):
    brute, opt = pair(h, 658)
    assert opt.findClosestElements([1, 2, 3, 4, 5], 4, 3) == [1, 2, 3, 4]
    assert opt.findClosestElements([1, 1, 2, 3, 4, 5], 4, -1) == [1, 1, 2, 3]
    assert opt.findClosestElements([1, 2, 3, 4, 5], 4, -1) == [1, 2, 3, 4]
    for _ in range(400):
        arr = sorted(R.randint(-8, 8) for _ in range(R.randint(1, 12)))
        k = R.randint(1, len(arr))
        x = R.randint(-12, 12)
        assert brute.findClosestElements(arr, k, x) == opt.findClosestElements(arr, k, x), (arr, k, x)
    big = sorted(R.randint(-10**4, 10**4) for _ in range(10**4))
    timed_call(lambda: opt.findClosestElements(big, 5000, 0), 1)


@case(2300)
def _(h):
    brute, opt = pair(h, 2300)
    assert opt.successfulPairs([5, 1, 3], [1, 2, 3, 4, 5], 7) == [4, 0, 3]
    assert opt.successfulPairs([3, 1, 2], [8, 5, 8], 16) == [2, 0, 2]
    for _ in range(300):
        spells = [R.randint(1, 10) for _ in range(R.randint(1, 8))]
        potions = [R.randint(1, 10) for _ in range(R.randint(1, 8))]
        success = R.randint(1, 100)
        want = brute.successfulPairs(spells[:], potions[:], success)
        assert opt.successfulPairs(spells[:], potions[:], success) == want, (spells, potions, success)
    spells = [R.randint(1, 10**5) for _ in range(10**5)]
    potions = [R.randint(1, 10**5) for _ in range(10**5)]
    timed_call(lambda: opt.successfulPairs(spells, potions[:], 10**10), 3)
    assert opt.successfulPairs([10**5], [10**5], 10**10) == [1]


@case(525)
def _(h):
    brute, opt = pair(h, 525)
    assert opt.findMaxLength([0, 1]) == 2 and opt.findMaxLength([0, 1, 0]) == 2
    assert opt.findMaxLength([0, 1, 1, 1, 1, 1, 0, 0, 0]) == 6
    for _ in range(300):
        nums = [R.randint(0, 1) for _ in range(R.randint(1, 16))]
        assert brute.findMaxLength(nums) == opt.findMaxLength(nums), nums
    timed_call(lambda: opt.findMaxLength([R.randint(0, 1) for _ in range(10**5)]), 1)


@case(528)
def _(h):
    nsb, nso = both(h, 528)
    brute_cls, opt_cls = nsb["Solution"], nso["Solution"]
    import random as rnd

    one_b, one_o = brute_cls([1]), opt_cls([1])
    assert one_b.pickIndex() == 0 and one_o.pickIndex() == 0
    for _ in range(150):
        w = [R.randint(1, 10) for _ in range(R.randint(1, 8))]
        sb, so = brute_cls(w), opt_cls(w)
        for _ in range(5):
            seed = R.randrange(10**6)
            rnd.seed(seed)
            a = sb.pickIndex()
            rnd.seed(seed)
            b = so.pickIndex()
            assert a == b and 0 <= a < len(w), (w, seed)
    rnd.seed(7)
    sol = opt_cls([1, 3])
    hits = sum(sol.pickIndex() for _ in range(20_000))
    assert 0.72 < hits / 20_000 < 0.78, hits
    big = opt_cls([R.randint(1, 10**5) for _ in range(10**4)])
    timed_call(lambda: [big.pickIndex() for _ in range(10**4)], 2)


@case(724)
def _(h):
    brute, opt = pair(h, 724)
    assert opt.pivotIndex([1, 7, 3, 6, 5, 6]) == 3
    assert opt.pivotIndex([1, 2, 3]) == -1
    assert opt.pivotIndex([2, 1, -1]) == 0
    for _ in range(300):
        nums = [R.randint(-3, 3) for _ in range(R.randint(1, 10))]
        assert brute.pivotIndex(nums) == opt.pivotIndex(nums), nums
    timed_call(lambda: opt.pivotIndex([R.randint(-1000, 1000) for _ in range(10**4)]), 1)


@case(1732)
def _(h):
    brute, opt = pair(h, 1732)
    assert opt.largestAltitude([-5, 1, 5, 0, -7]) == 1
    assert opt.largestAltitude([-4, -3, -2, -1, 4, 3, 2]) == 0
    for _ in range(300):
        gain = [R.randint(-100, 100) for _ in range(R.randint(1, 15))]
        assert brute.largestAltitude(gain) == opt.largestAltitude(gain), gain
    timed_call(lambda: opt.largestAltitude([R.randint(-100, 100) for _ in range(100)]), 1)


@case(643)
def _(h):
    brute, opt = pair(h, 643)
    assert opt.findMaxAverage([1, 12, -5, -6, 50, 3], 4) == 12.75
    assert opt.findMaxAverage([5], 1) == 5.0
    for _ in range(300):
        nums = [R.randint(-20, 20) for _ in range(R.randint(1, 15))]
        k = R.randint(1, len(nums))
        assert brute.findMaxAverage(nums, k) == opt.findMaxAverage(nums, k), (nums, k)
    big = [R.randint(-10**4, 10**4) for _ in range(10**5)]
    timed_call(lambda: opt.findMaxAverage(big, 50_000), 1)


@case(1456)
def _(h):
    brute, opt = pair(h, 1456)
    assert opt.maxVowels("abciiidef", 3) == 3 and opt.maxVowels("aeiou", 2) == 2
    assert opt.maxVowels("leetcode", 3) == 2
    for _ in range(300):
        s = "".join(R.choice("abcdeiou") for _ in range(R.randint(1, 15)))
        k = R.randint(1, len(s))
        assert brute.maxVowels(s, k) == opt.maxVowels(s, k), (s, k)
    big = "".join(R.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(10**5))
    timed_call(lambda: opt.maxVowels(big, 50_000), 1)


@case(1493)
def _(h):
    brute, opt = pair(h, 1493)
    assert opt.longestSubarray([1, 1, 0, 1]) == 3
    assert opt.longestSubarray([0, 1, 1, 1, 0, 1, 1, 0, 1]) == 5
    assert opt.longestSubarray([1, 1, 1]) == 2
    assert opt.longestSubarray([1]) == 0 and opt.longestSubarray([0]) == 0
    for _ in range(300):
        nums = [R.randint(0, 1) for _ in range(R.randint(1, 14))]
        assert brute.longestSubarray(nums) == opt.longestSubarray(nums), nums
    timed_call(lambda: opt.longestSubarray([R.choice((0, 1, 1, 1)) for _ in range(10**5)]), 1)


@case(32)
def _(h):
    brute, opt = pair(h, 32)
    assert opt.longestValidParentheses("(()") == 2 and opt.longestValidParentheses(")()())") == 4
    assert opt.longestValidParentheses("") == 0
    for _ in range(400):
        s = "".join(R.choice("()") for _ in range(R.randint(0, 16)))
        assert brute.longestValidParentheses(s) == opt.longestValidParentheses(s), s
    assert opt.longestValidParentheses("()" * 15_000) == 30_000
    assert opt.longestValidParentheses("(" * 30_000) == 0
    timed_call(lambda: opt.longestValidParentheses("".join(R.choice("()") for _ in range(30_000))), 1)
