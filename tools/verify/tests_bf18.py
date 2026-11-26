"""Brute-force backfill bf18: each note's first python block (brute force) vs its last (optimized)."""
import random

from harness import blocks_of, build_list, case, lc_path, list_to_py, ns_from

R = random.Random(1801)
ROUNDS = 150


def pair(num):
    blocks = blocks_of(lc_path(num))
    return ns_from(blocks[0])["Solution"](), ns_from(blocks[-1])["Solution"]()


@case("421-brute")
def _(h):
    brute, opt = pair(421)
    assert brute.findMaximumXOR([3, 10, 5, 25, 2, 8]) == 28
    assert brute.findMaximumXOR([14, 70, 53, 83, 49, 91, 36, 80, 92, 51, 66, 70]) == 127
    assert brute.findMaximumXOR([7]) == 0
    for _ in range(ROUNDS):
        nums = [R.randint(0, 2 ** 31 - 1) for _ in range(R.randint(1, 12))]
        assert brute.findMaximumXOR(nums[:]) == opt.findMaximumXOR(nums[:]), nums


@case("11-brute")
def _(h):
    brute, opt = pair(11)
    assert brute.maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49 and brute.maxArea([1, 1]) == 1
    for _ in range(ROUNDS):
        height = [R.randint(0, 20) for _ in range(R.randint(2, 14))]
        assert brute.maxArea(height[:]) == opt.maxArea(height[:]), height


@case("125-brute")
def _(h):
    brute, opt = pair(125)
    assert brute.isPalindrome("A man, a plan, a canal: Panama") is True
    assert brute.isPalindrome("race a car") is False and brute.isPalindrome(" ") is True
    alphabet = "aAbB1 ,:"
    for _ in range(ROUNDS):
        half = "".join(R.choice(alphabet) for _ in range(R.randint(0, 5)))
        mid = R.choice(["", "a", "1", " "])
        s = half + mid + (half[::-1] if R.random() < 0.7 else "".join(R.choice(alphabet) for _ in half))
        assert brute.isPalindrome(s) == opt.isPalindrome(s), s


@case("1550-brute")
def _(h):
    brute, opt = pair(1550)
    assert brute.threeConsecutiveOdds([2, 6, 4, 1]) is False
    assert brute.threeConsecutiveOdds([1, 2, 34, 3, 4, 5, 7, 23, 12]) is True
    for _ in range(ROUNDS):
        arr = [R.randint(1, 20) for _ in range(R.randint(1, 10))]
        assert brute.threeConsecutiveOdds(arr[:]) == opt.threeConsecutiveOdds(arr[:]), arr


@case("189-brute")
def _(h):
    brute, opt = pair(189)
    nums = [1, 2, 3, 4, 5, 6, 7]
    brute.rotate(nums, 3)
    assert nums == [5, 6, 7, 1, 2, 3, 4]
    nums = [-1, -100, 3, 99]
    brute.rotate(nums, 2)
    assert nums == [3, 99, -1, -100]
    for _ in range(ROUNDS):
        arr = [R.randint(-9, 9) for _ in range(R.randint(1, 10))]
        k = R.randint(0, 25)
        a, b = arr[:], arr[:]
        brute.rotate(a, k)
        opt.rotate(b, k)
        assert a == b, (arr, k)


@case("19-brute")
def _(h):
    brute, opt = pair(19)
    assert list_to_py(brute.removeNthFromEnd(build_list([1, 2, 3, 4, 5]), 2)) == [1, 2, 3, 5]
    assert list_to_py(brute.removeNthFromEnd(build_list([1]), 1)) == []
    assert list_to_py(brute.removeNthFromEnd(build_list([1, 2]), 1)) == [1]
    for _ in range(ROUNDS):
        vals = [R.randint(-9, 9) for _ in range(R.randint(1, 9))]
        n = R.randint(1, len(vals))
        got = list_to_py(brute.removeNthFromEnd(build_list(vals), n))
        assert got == list_to_py(opt.removeNthFromEnd(build_list(vals), n)), (vals, n)


@case("206-brute")
def _(h):
    brute, opt = pair(206)
    assert list_to_py(brute.reverseList(build_list([1, 2, 3, 4, 5]))) == [5, 4, 3, 2, 1]
    assert list_to_py(brute.reverseList(build_list([1, 2]))) == [2, 1]
    assert brute.reverseList(None) is None
    for _ in range(ROUNDS):
        vals = [R.randint(-9, 9) for _ in range(R.randint(0, 9))]
        got = list_to_py(brute.reverseList(build_list(vals)))
        assert got == list_to_py(opt.reverseList(build_list(vals))) == vals[::-1], vals


@case("21-brute")
def _(h):
    brute, opt = pair(21)
    merge = brute.mergeTwoLists
    assert list_to_py(merge(build_list([1, 2, 4]), build_list([1, 3, 4]))) == [1, 1, 2, 3, 4, 4]
    assert merge(None, None) is None
    assert list_to_py(merge(None, build_list([0]))) == [0]
    for _ in range(ROUNDS):
        a = sorted(R.randint(-9, 9) for _ in range(R.randint(0, 7)))
        b = sorted(R.randint(-9, 9) for _ in range(R.randint(0, 7)))
        got = list_to_py(merge(build_list(a), build_list(b)))
        assert got == list_to_py(opt.mergeTwoLists(build_list(a), build_list(b))) == sorted(a + b), (a, b)


@case("26-brute")
def _(h):
    brute, opt = pair(26)
    nums = [1, 1, 2]
    assert brute.removeDuplicates(nums) == 2 and nums[:2] == [1, 2]
    nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
    assert brute.removeDuplicates(nums) == 5 and nums[:5] == [0, 1, 2, 3, 4]
    for _ in range(ROUNDS):
        arr = sorted(R.randint(-5, 5) for _ in range(R.randint(1, 12)))
        a, b = arr[:], arr[:]
        ka, kb = brute.removeDuplicates(a), opt.removeDuplicates(b)
        assert ka == kb and a[:ka] == b[:kb] == sorted(set(arr)), arr


@case("283-brute")
def _(h):
    brute, opt = pair(283)
    nums = [0, 1, 0, 3, 12]
    brute.moveZeroes(nums)
    assert nums == [1, 3, 12, 0, 0]
    nums = [0]
    brute.moveZeroes(nums)
    assert nums == [0]
    for _ in range(ROUNDS):
        arr = [R.choice([0, 0, 1, 2, 3, -4]) for _ in range(R.randint(1, 12))]
        a, b = arr[:], arr[:]
        brute.moveZeroes(a)
        opt.moveZeroes(b)
        assert a == b, arr
