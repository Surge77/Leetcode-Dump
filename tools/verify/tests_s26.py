"""Sheet coverage s26: two pointers, divide and conquer, topo sort, Euler path, minimax Dijkstra, tries.

Each note has a brute force and an optimized block; both must agree on random inputs and on
LeetCode's examples, and the optimized one is run once at max constraints where speed matters.
"""
import random
import string

from harness import build_list, case, list_to_py
from tests_b10 import timed_call

R = random.Random(26)


def both(h, num, name="Solution"):
    brute, opt = h.lc_all(num, name)
    return brute[name](), opt[name]()


@case(167)
def _(h):
    brute, opt = both(h, 167)
    assert opt.twoSum([2, 7, 11, 15], 9) == [1, 2]
    assert opt.twoSum([2, 3, 4], 6) == [1, 3]
    assert opt.twoSum([-1, 0], -1) == [1, 2]
    for _ in range(300):
        nums = sorted(R.randint(-20, 20) for _ in range(R.randint(2, 12)))
        i, j = sorted(R.sample(range(len(nums)), 2))
        target = nums[i] + nums[j]
        got = opt.twoSum(nums, target)
        assert got[0] < got[1] and nums[got[0] - 1] + nums[got[1] - 1] == target, (nums, target, got)
        b = brute.twoSum(nums, target)
        assert nums[b[0] - 1] + nums[b[1] - 1] == target
    n = 30_000
    big = list(range(-1000, -1000 + n))
    timed_call(lambda: opt.twoSum(big, big[n // 2] + big[n // 2 + 1]), 1)


@case(392)
def _(h):
    brute, opt = both(h, 392)
    assert opt.isSubsequence("abc", "ahbgdc") is True
    assert opt.isSubsequence("axc", "ahbgdc") is False
    assert opt.isSubsequence("", "") is True and opt.isSubsequence("", "abc") is True
    assert opt.isSubsequence("aa", "ab") is False
    for _ in range(400):
        s = "".join(R.choice("abc") for _ in range(R.randint(0, 5)))
        t = "".join(R.choice("abc") for _ in range(R.randint(0, 10)))
        assert brute.isSubsequence(s, t) == opt.isSubsequence(s, t), (s, t)


def _balanced_bst_height(node, lo, hi):
    """Height of `node` if it is a height-balanced BST within (lo, hi), else None."""
    if node is None:
        return 0
    if not (lo < node.val < hi):
        return None
    left = _balanced_bst_height(node.left, lo, node.val)
    right = _balanced_bst_height(node.right, node.val, hi)
    if left is None or right is None or abs(left - right) > 1:
        return None
    return 1 + max(left, right)


def _inorder(node):
    out, stack = [], []
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        out.append(node.val)
        node = node.right
    return out


@case(108)
def _(h):
    brute, opt = both(h, 108)
    for sol in (brute, opt):
        root = sol.sortedArrayToBST([-10, -3, 0, 5, 9])
        assert _inorder(root) == [-10, -3, 0, 5, 9]
        assert _balanced_bst_height(root, float("-inf"), float("inf")) is not None
    for _ in range(200):
        nums = sorted(R.sample(range(-50, 50), R.randint(1, 30)))
        for sol in (brute, opt):
            root = sol.sortedArrayToBST(list(nums))
            assert _inorder(root) == nums, nums
            assert _balanced_bst_height(root, float("-inf"), float("inf")) is not None, nums
    big = list(range(-5000, 5000))
    timed_call(lambda: opt.sortedArrayToBST(big), 1)


@case(148)
def _(h):
    brute, opt = both(h, 148)
    assert list_to_py(opt.sortList(build_list([4, 2, 1, 3]))) == [1, 2, 3, 4]
    assert list_to_py(opt.sortList(build_list([-1, 5, 3, 4, 0]))) == [-1, 0, 3, 4, 5]
    assert opt.sortList(None) is None
    for _ in range(300):
        vals = [R.randint(-10, 10) for _ in range(R.randint(0, 20))]
        assert list_to_py(brute.sortList(build_list(vals))) == sorted(vals), vals
        assert list_to_py(opt.sortList(build_list(vals))) == sorted(vals), vals
    big = [R.randint(-10**5, 10**5) for _ in range(50_000)]
    out = []
    timed_call(lambda: out.append(opt.sortList(build_list(big))), 3)
    assert list_to_py(out[0], 100_000) == sorted(big)


def _quad(node):
    """Canonical form of a quad tree: leaf value, or a tuple of the four children."""
    if node.isLeaf:
        assert all(k is None for k in (node.topLeft, node.topRight, node.bottomLeft, node.bottomRight))
        return bool(node.val)
    return (_quad(node.topLeft), _quad(node.topRight), _quad(node.bottomLeft), _quad(node.bottomRight))


@case(427)
def _(h):
    brute, opt = both(h, 427)
    assert _quad(opt.construct([[0, 1], [1, 0]])) == (False, True, True, False)
    assert _quad(opt.construct([[1]])) is True
    assert _quad(opt.construct([[0] * 4 for _ in range(4)])) is False
    grid = [[1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0]]
    assert _quad(opt.construct(grid)) == (True, (False, False, True, True), True, False)
    for _ in range(200):
        n = 2 ** R.randint(0, 3)
        density = R.random()
        grid = [[int(R.random() < density) for _ in range(n)] for _ in range(n)]
        assert _quad(brute.construct(grid)) == _quad(opt.construct(grid)), grid
    big = [[int(R.random() < 0.5) for _ in range(64)] for _ in range(64)]
    timed_call(lambda: opt.construct(big), 1)


def _is_valid_alien_order(words, order):
    if sorted(order) != sorted(set("".join(words))):
        return False
    rank = {ch: i for i, ch in enumerate(order)}
    keys = [[rank[ch] for ch in w] for w in words]
    return all(keys[i] <= keys[i + 1] for i in range(len(keys) - 1))


@case(269)
def _(h):
    brute, opt = both(h, 269)
    assert opt.alienOrder(["wrt", "wrf", "er", "ett", "rftt"]) == "wertf"  # unique order
    assert opt.alienOrder(["z", "x"]) == "zx"
    assert opt.alienOrder(["z", "x", "z"]) == ""
    assert opt.alienOrder(["abc", "ab"]) == ""
    assert _is_valid_alien_order(["z", "z"], opt.alienOrder(["z", "z"]))
    for _ in range(300):
        alphabet = "abcde"[:R.randint(1, 5)]
        words = ["".join(R.choice(alphabet) for _ in range(R.randint(1, 4))) for _ in range(R.randint(1, 6))]
        if R.random() < 0.6:
            secret = list(alphabet)
            R.shuffle(secret)
            rank = {ch: i for i, ch in enumerate(secret)}
            words.sort(key=lambda w: [rank[ch] for ch in w])
        expected = brute.alienOrder(words)
        got = opt.alienOrder(words)
        if expected == "":
            assert got == "", (words, got)
        else:
            assert _is_valid_alien_order(words, got), (words, got)
    secret = list(string.ascii_lowercase)
    R.shuffle(secret)
    rank = {ch: i for i, ch in enumerate(secret)}
    big = sorted(("".join(R.choice(secret) for _ in range(100)) for _ in range(100)),
                 key=lambda w: [rank[ch] for ch in w])
    timed_call(lambda: opt.alienOrder(big), 1)


def _random_itinerary(rng, length, airports):
    route = ["JFK"]
    for _ in range(length):
        route.append(rng.choice(airports))
    tickets = [[a, b] for a, b in zip(route, route[1:])]
    rng.shuffle(tickets)
    return tickets


@case(332)
def _(h):
    brute, opt = both(h, 332)
    ex1 = [["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]]
    assert opt.findItinerary(ex1) == ["JFK", "MUC", "LHR", "SFO", "SJC"]
    ex2 = [["JFK", "SFO"], ["JFK", "ATL"], ["SFO", "ATL"], ["ATL", "JFK"], ["ATL", "SFO"]]
    assert opt.findItinerary(ex2) == ["JFK", "ATL", "JFK", "SFO", "ATL", "SFO"]
    assert opt.findItinerary([["JFK", "KUL"], ["JFK", "NRT"], ["NRT", "JFK"]]) == ["JFK", "NRT", "JFK", "KUL"]
    airports = ["JFK", "AAA", "BBB", "CCC", "DDD"]
    for _ in range(300):
        tickets = _random_itinerary(R, R.randint(1, 8), airports)
        got = opt.findItinerary([t[:] for t in tickets])
        assert got == brute.findItinerary([t[:] for t in tickets]), tickets
        assert sorted(zip(got, got[1:])) == sorted(map(tuple, tickets))
    big = _random_itinerary(R, 300, ["JFK"] + [f"A{i:02d}" for i in range(20)])
    timed_call(lambda: opt.findItinerary(big), 1)


@case(778)
def _(h):
    brute, opt = both(h, 778)
    assert opt.swimInWater([[0, 2], [1, 3]]) == 3
    spiral = [[0, 1, 2, 3, 4], [24, 23, 22, 21, 5], [12, 13, 14, 15, 16], [11, 17, 18, 19, 20], [10, 9, 8, 7, 6]]
    assert opt.swimInWater(spiral) == 16
    assert opt.swimInWater([[0]]) == 0
    for _ in range(200):
        n = R.randint(1, 6)
        cells = list(range(n * n))
        R.shuffle(cells)
        grid = [cells[i * n:(i + 1) * n] for i in range(n)]
        assert brute.swimInWater(grid) == opt.swimInWater(grid), grid
    n = 50
    cells = list(range(n * n))
    R.shuffle(cells)
    big = [cells[i * n:(i + 1) * n] for i in range(n)]
    timed_call(lambda: opt.swimInWater(big), 2)


@case(211)
def _(h):
    brute_ns, opt_ns = h.lc_all(211, "WordDictionary")
    wd = opt_ns["WordDictionary"]()
    for w in ("bad", "dad", "mad"):
        wd.addWord(w)
    assert [wd.search(p) for p in ("pad", "bad", ".ad", "b..")] == [False, True, True, True]
    assert wd.search("ba") is False and wd.search("....") is False
    for _ in range(150):
        brute, opt = brute_ns["WordDictionary"](), opt_ns["WordDictionary"]()
        for _ in range(R.randint(1, 40)):
            word = "".join(R.choice("abc") for _ in range(R.randint(1, 4)))
            if R.random() < 0.4:
                brute.addWord(word)
                opt.addWord(word)
            else:
                pattern = list(word)
                for i in R.sample(range(len(pattern)), min(len(pattern), R.randint(0, 2))):
                    pattern[i] = "."
                pattern = "".join(pattern)
                assert brute.search(pattern) == opt.search(pattern), pattern

    def heavy():
        d = opt_ns["WordDictionary"]()
        for _ in range(5_000):
            d.addWord("".join(R.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(R.randint(1, 25))))
        for _ in range(5_000):
            d.search(".." + "".join(R.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(R.randint(0, 23))))

    timed_call(heavy, 3)


@case(212)
def _(h):
    brute, opt = both(h, 212)
    board = [["o", "a", "a", "n"], ["e", "t", "a", "e"], ["i", "h", "k", "r"], ["i", "f", "l", "v"]]
    assert sorted(opt.findWords([r[:] for r in board], ["oath", "pea", "eat", "rain"])) == ["eat", "oath"]
    assert opt.findWords([["a", "b"], ["c", "d"]], ["abcb"]) == []
    assert sorted(opt.findWords([["a", "a"]], ["a", "aa", "aaa"])) == ["a", "aa"]
    for _ in range(200):
        m, n = R.randint(1, 4), R.randint(1, 4)
        board = [[R.choice("abc") for _ in range(n)] for _ in range(m)]
        words = list({"".join(R.choice("abc") for _ in range(R.randint(1, 5))) for _ in range(R.randint(1, 10))})
        expected = sorted(brute.findWords([r[:] for r in board], words))
        assert sorted(opt.findWords([r[:] for r in board], words)) == expected, (board, words)
    big_board = [[R.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(12)] for _ in range(12)]
    big_words = list({"".join(R.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(R.randint(1, 10)))
                      for _ in range(30_000)})
    timed_call(lambda: opt.findWords(big_board, big_words), 3)
    dense = [["a"] * 12 for _ in range(12)]
    timed_call(lambda: opt.findWords(dense, ["a" * k for k in range(1, 11)] + ["a" * 9 + "b"]), 5)
