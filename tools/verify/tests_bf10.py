"""Brute-force blocks for 55, 621, 630, 1, 1399, 217, 2176, 242, 36, 380 versus the optimized solutions."""
import copy
import random

from harness import blocks_of, case, lc_path, ns_from


def pair(num):
    blocks = blocks_of(lc_path(num))
    return ns_from(blocks[0]), ns_from(blocks[-1])


@case("55-brute")
def _(h):
    brute, opt = pair(55)
    rng = random.Random(5501)
    assert brute["Solution"]().canJump([2, 3, 1, 1, 4]) is True
    assert brute["Solution"]().canJump([3, 2, 1, 0, 4]) is False
    assert brute["Solution"]().canJump([0]) is True
    for _ in range(200):
        nums = [rng.randint(0, 4) for _ in range(rng.randint(1, 9))]
        assert brute["Solution"]().canJump(nums) == opt["Solution"]().canJump(nums), nums


@case("621-brute")
def _(h):
    brute, opt = pair(621)
    rng = random.Random(62101)
    assert brute["Solution"]().leastInterval(["A", "A", "A", "B", "B", "B"], 2) == 8
    assert brute["Solution"]().leastInterval(["A", "C", "A", "B", "D", "B"], 1) == 6
    assert brute["Solution"]().leastInterval(["A", "A", "A", "B", "B", "B"], 3) == 10
    for _ in range(200):
        tasks = [rng.choice("ABCDE") for _ in range(rng.randint(1, 12))]
        n = rng.randint(0, 5)
        assert brute["Solution"]().leastInterval(tasks, n) == opt["Solution"]().leastInterval(tasks, n), (tasks, n)


@case("630-brute")
def _(h):
    brute, opt = pair(630)
    rng = random.Random(63001)
    assert brute["Solution"]().scheduleCourse([[100, 200], [200, 1300], [1000, 1250], [2000, 3200]]) == 3
    assert brute["Solution"]().scheduleCourse([[1, 2]]) == 1
    assert brute["Solution"]().scheduleCourse([[3, 2], [4, 3]]) == 0
    for _ in range(150):
        courses = [[rng.randint(1, 8), rng.randint(1, 20)] for _ in range(rng.randint(1, 8))]
        got = brute["Solution"]().scheduleCourse(copy.deepcopy(courses))
        assert got == opt["Solution"]().scheduleCourse(copy.deepcopy(courses)), courses


@case("1-brute")
def _(h):
    brute, opt = pair(1)
    rng = random.Random(101)
    assert brute["Solution"]().twoSum([2, 7, 11, 15], 9) == [0, 1]
    assert brute["Solution"]().twoSum([3, 2, 4], 6) == [1, 2]
    assert brute["Solution"]().twoSum([3, 3], 6) == [0, 1]
    for _ in range(200):
        nums = [rng.randint(-5, 10) for _ in range(rng.randint(2, 9))]
        target = rng.randint(-8, 18)
        want = opt["Solution"]().twoSum(nums, target)
        got = brute["Solution"]().twoSum(nums, target)
        assert (want == [-1, -1]) == (got == [-1, -1]), (nums, target)
        if got != [-1, -1]:
            i, j = got
            assert i != j and nums[i] + nums[j] == target, (nums, target, got)


@case("1399-brute")
def _(h):
    brute, opt = pair(1399)
    assert brute["Solution"]().countLargestGroup(13) == 4
    assert brute["Solution"]().countLargestGroup(2) == 2
    for n in range(1, 301):
        assert brute["Solution"]().countLargestGroup(n) == opt["Solution"]().countLargestGroup(n), n


@case("217-brute")
def _(h):
    brute, opt = pair(217)
    rng = random.Random(21701)
    assert brute["Solution"]().containsDuplicate([1, 2, 3, 1]) is True
    assert brute["Solution"]().containsDuplicate([1, 2, 3, 4]) is False
    assert brute["Solution"]().containsDuplicate([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]) is True
    for _ in range(200):
        nums = [rng.randint(-10, 10) for _ in range(rng.randint(1, 10))]
        assert brute["Solution"]().containsDuplicate(nums) == opt["Solution"]().containsDuplicate(nums), nums


@case("2176-brute")
def _(h):
    brute, opt = pair(2176)
    rng = random.Random(217601)
    assert brute["Solution"]().countPairs([3, 1, 2, 2, 2, 1, 3], 2) == 4
    assert brute["Solution"]().countPairs([1, 2, 3, 4], 1) == 0
    for _ in range(200):
        nums = [rng.randint(1, 4) for _ in range(rng.randint(1, 15))]
        k = rng.randint(1, 20)
        assert brute["Solution"]().countPairs(nums, k) == opt["Solution"]().countPairs(nums, k), (nums, k)


@case("242-brute")
def _(h):
    brute, opt = pair(242)
    rng = random.Random(24201)
    assert brute["Solution"]().isAnagram("anagram", "nagaram") is True
    assert brute["Solution"]().isAnagram("rat", "car") is False
    for _ in range(300):
        s = "".join(rng.choice("abc ") for _ in range(rng.randint(0, 7)))
        t = list(s) if rng.random() < 0.5 else [rng.choice("abc ") for _ in range(rng.randint(0, 7))]
        rng.shuffle(t)
        t = "".join(t)
        assert brute["Solution"]().isAnagram(s, t) == opt["Solution"]().isAnagram(s, t), (s, t)


def blank_board():
    return [["."] * 9 for _ in range(9)]


@case("36-brute")
def _(h):
    brute, opt = pair(36)
    rng = random.Random(3601)
    valid = [list(r) for r in (
        "53..7....", "6..195...", ".98....6.", "8...6...3", "4..8.3..1",
        "7...2...6", ".6....28.", "...419..5", "....8..79")]
    assert brute["Solution"]().isValidSudoku(valid) is True
    invalid = copy.deepcopy(valid)
    invalid[0][0] = "8"
    assert brute["Solution"]().isValidSudoku(invalid) is False
    for _ in range(300):
        board = blank_board()
        for _ in range(rng.randint(0, 14)):
            board[rng.randrange(9)][rng.randrange(9)] = str(rng.randint(1, 9))
        assert brute["Solution"]().isValidSudoku(board) == opt["Solution"]().isValidSudoku(board), board


@case("380-brute")
def _(h):
    brute, opt = pair(380)
    rng = random.Random(38001)
    for _ in range(120):
        b, o = brute["RandomizedSet"](), opt["RandomizedSet"]()
        model = set()
        for _ in range(rng.randint(1, 40)):
            op, val = rng.choice(["insert", "remove", "random"]), rng.randint(0, 6)
            if op == "random":
                if model:
                    assert b.getRandom() in model and o.getRandom() in model
                continue
            assert getattr(b, op)(val) == getattr(o, op)(val)
            model.add(val) if op == "insert" else model.discard(val)
    s = brute["RandomizedSet"]()
    assert s.insert(1) and s.remove(2) is False and s.insert(2) and s.getRandom() in (1, 2)
    assert s.remove(1) and s.insert(2) is False and s.getRandom() == 2
