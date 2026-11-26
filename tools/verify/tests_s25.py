"""Sheet coverage s25: hashing (128, 205, 219, 271, 290), intervals (228, 252, 253, 1851), 3Sum (15).

Each note has a brute force and an optimized block; both must agree on random inputs and on
LeetCode's examples, and the optimized one is run once at max constraints where speed matters.
"""
import random
import string

from harness import case
from tests_b10 import timed_call

R = random.Random(25)


def both(h, num, name="Solution"):
    brute, opt = h.lc_all(num, name)
    return brute[name](), opt[name]()


def random_intervals(count, hi):
    out = []
    for _ in range(count):
        start = R.randint(0, hi - 1)
        out.append([start, R.randint(start + 1, hi)])
    return out


@case(128)
def _(h):
    brute, opt = both(h, 128)
    assert opt.longestConsecutive([100, 4, 200, 1, 3, 2]) == 4
    assert opt.longestConsecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
    assert opt.longestConsecutive([1, 0, 1, 2]) == 3
    assert opt.longestConsecutive([]) == 0
    for _ in range(300):
        nums = [R.randint(-15, 15) for _ in range(R.randint(0, 20))]
        assert brute.longestConsecutive(nums) == opt.longestConsecutive(nums), nums
    big = list(range(100_000))
    R.shuffle(big)
    timed_call(lambda: opt.longestConsecutive(big), 1)
    assert opt.longestConsecutive(big) == 100_000


@case(205)
def _(h):
    brute, opt = both(h, 205)
    assert opt.isIsomorphic("egg", "add") is True
    assert opt.isIsomorphic("foo", "bar") is False
    assert opt.isIsomorphic("paper", "title") is True
    assert opt.isIsomorphic("badc", "baba") is False
    for _ in range(400):
        n = R.randint(1, 10)
        s = "".join(R.choice("abc1") for _ in range(n))
        t = "".join(R.choice("xyz!") for _ in range(n))
        assert brute.isIsomorphic(s, t) == opt.isIsomorphic(s, t), (s, t)
        assert opt.isIsomorphic(s, s) is True
    s = "".join(R.choice(string.printable) for _ in range(50_000))
    timed_call(lambda: opt.isIsomorphic(s, s[::-1]), 1)


@case(219)
def _(h):
    brute, opt = both(h, 219)
    assert opt.containsNearbyDuplicate([1, 2, 3, 1], 3) is True
    assert opt.containsNearbyDuplicate([1, 0, 1, 1], 1) is True
    assert opt.containsNearbyDuplicate([1, 2, 3, 1, 2, 3], 2) is False
    for _ in range(400):
        nums = [R.randint(0, 8) for _ in range(R.randint(1, 15))]
        k = R.randint(0, 16)
        assert brute.containsNearbyDuplicate(nums, k) == opt.containsNearbyDuplicate(nums, k), (nums, k)
    big = list(range(100_000))
    timed_call(lambda: opt.containsNearbyDuplicate(big, 100_000), 1)


@case(271)
def _(h):
    brute, opt = both(h, 271, "Codec")
    samples = [["Hello", "World"], [""], [], ["", ""], ["3#a", "#", "12#"], ["neet", "code", "love", "you"]]
    alphabet = [chr(i) for i in range(256)]
    for _ in range(300):
        samples.append(["".join(R.choice(alphabet) for _ in range(R.randint(0, 6))) for _ in range(R.randint(0, 6))])
    for strs in samples:
        for codec in (brute, opt):
            assert codec.decode(codec.encode(list(strs))) == strs, strs
    big = ["".join(R.choice(alphabet) for _ in range(200)) for _ in range(200)]
    timed_call(lambda: opt.decode(opt.encode(big)), 1)


@case(290)
def _(h):
    brute, opt = both(h, 290)
    assert opt.wordPattern("abba", "dog cat cat dog") is True
    assert opt.wordPattern("abba", "dog cat cat fish") is False
    assert opt.wordPattern("aaaa", "dog cat cat dog") is False
    assert opt.wordPattern("abba", "dog dog dog dog") is False
    assert opt.wordPattern("aaa", "dog dog dog dog") is False
    for _ in range(400):
        pattern = "".join(R.choice("abc") for _ in range(R.randint(1, 7)))
        s = " ".join(R.choice(["a", "dog", "cat", "b"]) for _ in range(R.randint(1, 7)))
        assert brute.wordPattern(pattern, s) == opt.wordPattern(pattern, s), (pattern, s)


@case(228)
def _(h):
    brute, opt = both(h, 228)
    assert opt.summaryRanges([0, 1, 2, 4, 5, 7]) == ["0->2", "4->5", "7"]
    assert opt.summaryRanges([0, 2, 3, 4, 6, 8, 9]) == ["0", "2->4", "6", "8->9"]
    assert opt.summaryRanges([]) == []
    assert opt.summaryRanges([-2 ** 31, 2 ** 31 - 1]) == ["-2147483648", "2147483647"]
    for _ in range(400):
        nums = sorted(R.sample(range(-10, 15), R.randint(0, 20)))
        assert brute.summaryRanges(nums) == opt.summaryRanges(nums), nums


@case(252)
def _(h):
    brute, opt = both(h, 252)
    assert opt.canAttendMeetings([[0, 30], [5, 10], [15, 20]]) is False
    assert opt.canAttendMeetings([[7, 10], [2, 4]]) is True
    assert opt.canAttendMeetings([[1, 5], [5, 8]]) is True
    assert opt.canAttendMeetings([]) is True
    for _ in range(400):
        iv = random_intervals(R.randint(0, 6), 30)
        assert brute.canAttendMeetings([x[:] for x in iv]) == opt.canAttendMeetings([x[:] for x in iv]), iv
    big = [[2 * i, 2 * i + 1] for i in range(10_000)]
    R.shuffle(big)
    timed_call(lambda: opt.canAttendMeetings(big), 1)


@case(253)
def _(h):
    brute, opt = both(h, 253)
    assert opt.minMeetingRooms([[0, 30], [5, 10], [15, 20]]) == 2
    assert opt.minMeetingRooms([[7, 10], [2, 4]]) == 1
    assert opt.minMeetingRooms([[1, 5], [5, 10]]) == 1
    assert opt.minMeetingRooms([[1, 3]] * 4) == 4
    for _ in range(400):
        iv = random_intervals(R.randint(1, 10), 20)
        assert brute.minMeetingRooms([x[:] for x in iv]) == opt.minMeetingRooms([x[:] for x in iv]), iv
    big = random_intervals(10_000, 1_000_000)
    timed_call(lambda: opt.minMeetingRooms(big), 1)


@case(1851)
def _(h):
    brute, opt = both(h, 1851)
    assert opt.minInterval([[1, 4], [2, 4], [3, 6], [4, 4]], [2, 3, 4, 5]) == [3, 3, 1, 4]
    assert opt.minInterval([[2, 3], [2, 5], [1, 8], [20, 25]], [2, 19, 5, 22]) == [2, -1, 4, 6]
    for _ in range(400):
        iv = []
        for _ in range(R.randint(1, 8)):
            lo = R.randint(1, 20)
            iv.append([lo, R.randint(lo, 22)])
        qs = [R.randint(0, 24) for _ in range(R.randint(1, 8))]
        assert brute.minInterval([x[:] for x in iv], qs[:]) == opt.minInterval([x[:] for x in iv], qs[:]), (iv, qs)
    n = 100_000
    big_iv = []
    for _ in range(n):
        lo = R.randint(1, 10 ** 7)
        big_iv.append([lo, R.randint(lo, 10 ** 7)])
    big_q = [R.randint(1, 10 ** 7) for _ in range(n)]
    timed_call(lambda: opt.minInterval(big_iv, big_q), 3)


def canon(triplets):
    return sorted(sorted(t) for t in triplets)


@case(15)
def _(h):
    brute, opt = both(h, 15)
    assert canon(opt.threeSum([-1, 0, 1, 2, -1, -4])) == [[-1, -1, 2], [-1, 0, 1]]
    assert opt.threeSum([0, 1, 1]) == []
    assert opt.threeSum([0, 0, 0]) == [[0, 0, 0]]
    assert opt.threeSum([0, 0, 0, 0]) == [[0, 0, 0]]
    for _ in range(300):
        nums = [R.randint(-6, 6) for _ in range(R.randint(3, 14))]
        res = opt.threeSum(nums[:])
        assert len(res) == len({tuple(sorted(t)) for t in res}), (nums, res)
        assert canon(brute.threeSum(nums[:])) == canon(res), nums
    big = [R.randint(-10 ** 5, 10 ** 5) for _ in range(3000)]
    timed_call(lambda: opt.threeSum(big), 3)
