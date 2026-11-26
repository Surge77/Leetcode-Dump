"""Brute-force backfill bf01: each note's first python block (brute force) vs its last (optimized)."""
import random

from harness import TreeNode, blocks_of, case, find_node, lc_path, ns_from

R = random.Random(2601)


def pair(num):
    blocks = blocks_of(lc_path(num))
    return ns_from(blocks[0])["Solution"](), ns_from(blocks[-1])["Solution"]()


def canon(lists):
    return sorted(map(tuple, lists))


@case("121-brute")
def _(h):
    brute, opt = pair(121)
    assert brute.maxProfit([7, 1, 5, 3, 6, 4]) == 5 and brute.maxProfit([7, 6, 4, 3, 1]) == 0
    for _ in range(300):
        p = [R.randint(0, 20) for _ in range(R.randint(1, 12))]
        assert brute.maxProfit(p[:]) == opt.maxProfit(p[:]), p


@case("169-brute")
def _(h):
    brute, opt = pair(169)
    assert brute.majorityElement([3, 2, 3]) == 3 and brute.majorityElement([2, 2, 1, 1, 1, 2, 2]) == 2
    for _ in range(300):
        n = R.randint(1, 11)
        major = R.randint(0, 5)
        nums = [major] * (n // 2 + 1) + [R.randint(0, 5) for _ in range(n - n // 2 - 1)]
        R.shuffle(nums)
        assert brute.majorityElement(nums[:]) == opt.majorityElement(nums[:]) == major, nums


def bst_from(vals):
    root = None
    for v in vals:
        node = TreeNode(v)
        if root is None:
            root = node
            continue
        cur = root
        while True:
            side = "left" if v < cur.val else "right"
            nxt = getattr(cur, side)
            if nxt is None:
                setattr(cur, side, node)
                break
            cur = nxt
    return root


@case("235-brute")
def _(h):
    brute, opt = pair(235)
    root = bst_from([6, 2, 8, 0, 4, 7, 9, 3, 5])
    for a, b, want in ((2, 8, 6), (2, 4, 2)):
        assert brute.lowestCommonAncestor(root, find_node(root, a), find_node(root, b)).val == want
    root = bst_from([2, 1])
    assert brute.lowestCommonAncestor(root, find_node(root, 2), find_node(root, 1)).val == 2
    for _ in range(300):
        vals = R.sample(range(100), R.randint(1, 12))
        root = bst_from(vals)
        p, q = find_node(root, R.choice(vals)), find_node(root, R.choice(vals))
        assert brute.lowestCommonAncestor(root, p, q) is opt.lowestCommonAncestor(root, p, q), vals


@case("17-brute")
def _(h):
    brute, opt = pair(17)
    assert sorted(brute.letterCombinations("23")) == ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]
    assert brute.letterCombinations("") == []
    assert sorted(brute.letterCombinations("2")) == ["a", "b", "c"]
    for _ in range(100):
        digits = "".join(R.choice("23456789") for _ in range(R.randint(0, 3)))
        assert sorted(brute.letterCombinations(digits)) == sorted(opt.letterCombinations(digits)), digits


@case("22-brute")
def _(h):
    brute, opt = pair(22)
    assert sorted(brute.generateParenthesis(3)) == sorted(["((()))", "(()())", "(())()", "()(())", "()()()"])
    assert brute.generateParenthesis(1) == ["()"]
    for _ in range(100):
        n = R.randint(1, 7)
        assert sorted(brute.generateParenthesis(n)) == sorted(opt.generateParenthesis(n)), n


@case("46-brute")
def _(h):
    brute, opt = pair(46)
    assert canon(brute.permute([1, 2, 3])) == canon([[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]])
    assert canon(brute.permute([0, 1])) == [(0, 1), (1, 0)] and brute.permute([1]) == [[1]]
    for _ in range(100):
        nums = R.sample(range(-10, 11), R.randint(1, 6))
        got = brute.permute(nums[:])
        assert len(got) == len(set(map(tuple, got))) and canon(got) == canon(opt.permute(nums[:])), nums


@case("51-brute")
def _(h):
    brute, opt = pair(51)
    assert sorted(brute.solveNQueens(4)) == sorted([[".Q..", "...Q", "Q...", "..Q."], ["..Q.", "Q...", "...Q", ".Q.."]])
    assert brute.solveNQueens(1) == [["Q"]]
    for _ in range(100):
        n = R.randint(1, 7)
        assert sorted(brute.solveNQueens(n)) == sorted(opt.solveNQueens(n)), n


@case("77-brute")
def _(h):
    brute, opt = pair(77)
    assert canon(brute.combine(4, 2)) == [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
    assert brute.combine(1, 1) == [[1]]
    for _ in range(100):
        n = R.randint(1, 10)
        k = R.randint(1, n)
        assert canon(brute.combine(n, k)) == canon(opt.combine(n, k)), (n, k)


@case("78-brute")
def _(h):
    brute, opt = pair(78)
    want = [(), (1,), (1, 2), (1, 2, 3), (1, 3), (2,), (2, 3), (3,)]
    assert sorted(tuple(sorted(s)) for s in brute.subsets([1, 2, 3])) == want
    assert canon(brute.subsets([0])) == [(), (0,)]
    for _ in range(100):
        nums = R.sample(range(-10, 11), R.randint(0, 8))
        got = sorted(tuple(sorted(s)) for s in brute.subsets(nums[:]))
        assert got == sorted(tuple(sorted(s)) for s in opt.subsets(nums[:])), nums


@case("79-brute")
def _(h):
    brute, opt = pair(79)
    board = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
    assert brute.exist([r[:] for r in board], "ABCCED") and brute.exist([r[:] for r in board], "SEE")
    assert not brute.exist([r[:] for r in board], "ABCB")
    for _ in range(300):
        m, n = R.randint(1, 4), R.randint(1, 4)
        g = [[R.choice("ab") for _ in range(n)] for _ in range(m)]
        word = "".join(R.choice("ab") for _ in range(R.randint(1, 6)))
        assert brute.exist([r[:] for r in g], word) == opt.exist([r[:] for r in g], word), (g, word)
