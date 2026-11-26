"""BST notes: recover, delete, min difference, two sum, search, insert, build from preorder.

Each note has a brute force and an optimized block; both must agree on random inputs and on
LeetCode's examples. Trees are rebuilt from level-order lists before every call because the
methods mutate them.
"""
import random

from harness import case, build_tree, tree_to_list, find_node
from tests_b10 import timed_call

R = random.Random(22)


def both(h, num):
    brute, opt = h.lc_all(num, "Solution")
    return brute["Solution"](), opt["Solution"]()


def bst_insert(root, val, node_cls):
    if root is None:
        return node_cls(val)
    node = root
    while True:
        side = "left" if val < node.val else "right"
        child = getattr(node, side)
        if child is None:
            setattr(node, side, node_cls(val))
            return root
        node = child


def random_bst_list(h, n, lo=-50, hi=50):
    """Level-order list of a random BST with n distinct values."""
    vals = R.sample(range(lo, hi + 1), n)
    root = None
    for v in vals:
        root = bst_insert(root, v, h.TreeNode)
    return tree_to_list(root), vals


def path_list(n):
    """Level-order list of a right-leaning path 0..n-1 (a degenerate BST)."""
    out = [0]
    for i in range(1, n):
        out += [None, i]
    return out


def inorder(root):
    out, stack, cur = [], [], root
    while stack or cur:
        while cur:
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        out.append(cur.val)
        cur = cur.right
    return out


def is_bst(root):
    vals = inorder(root)
    return all(a < b for a, b in zip(vals, vals[1:]))


@case(99)
def _(h):
    brute, opt = both(h, 99)
    for sol in (brute, opt):
        root = build_tree([1, 3, None, None, 2])
        sol.recoverTree(root)
        assert tree_to_list(root) == [3, 1, None, None, 2]
        root = build_tree([3, 1, 4, None, None, 2])
        sol.recoverTree(root)
        assert tree_to_list(root) == [2, 1, 4, None, None, 3]
    for _ in range(300):
        good, vals = random_bst_list(h, R.randint(2, 12))
        a, b = R.sample(vals, 2)
        for sol in (brute, opt):
            root = build_tree(good)
            na, nb = find_node(root, a), find_node(root, b)
            na.val, nb.val = nb.val, na.val
            sol.recoverTree(root)
            assert tree_to_list(root) == good, (good, a, b)
    n = 1000
    good = path_list(n)
    root = build_tree(good)
    lo, hi = find_node(root, 0), find_node(root, n - 1)
    lo.val, hi.val = hi.val, lo.val
    timed_call(lambda: opt.recoverTree(root), 1)
    assert tree_to_list(root) == good


@case(450)
def _(h):
    brute, opt = both(h, 450)
    out = tree_to_list(opt.deleteNode(build_tree([5, 3, 6, 2, 4, None, 7]), 3))
    assert out == [5, 4, 6, 2, None, None, 7]
    assert tree_to_list(opt.deleteNode(build_tree([5, 3, 6, 2, 4, None, 7]), 0)) == [5, 3, 6, 2, 4, None, 7]
    assert opt.deleteNode(None, 0) is None and brute.deleteNode(None, 0) is None
    for _ in range(300):
        lst, vals = random_bst_list(h, R.randint(1, 12))
        key = R.choice(vals) if R.random() < 0.8 else R.randint(-60, 60)
        expected = sorted(v for v in vals if v != key)
        for sol in (brute, opt):
            root = sol.deleteNode(build_tree(lst), key)
            assert inorder(root) == expected and is_bst(root), (lst, key)
    n = 10_000
    lst = path_list(n)
    root = build_tree(lst)
    timed_call(lambda: opt.deleteNode(root, n - 2), 1)
    assert inorder(root) == [v for v in range(n) if v != n - 2]


@case(530)
def _(h):
    brute, opt = both(h, 530)
    for sol in (brute, opt):
        assert sol.getMinimumDifference(build_tree([4, 2, 6, 1, 3])) == 1
        assert sol.getMinimumDifference(build_tree([1, 0, 48, None, None, 12, 49])) == 1
    for _ in range(300):
        lst, _vals = random_bst_list(h, R.randint(2, 15), 0, 200)
        assert brute.getMinimumDifference(build_tree(lst)) == opt.getMinimumDifference(build_tree(lst)), lst
    lst = path_list(10_000)
    root = build_tree([None if v is None else 3 * v for v in lst])
    timed_call(lambda: opt.getMinimumDifference(root), 1)
    assert opt.getMinimumDifference(root) == 3


@case(653)
def _(h):
    brute, opt = both(h, 653)
    for sol in (brute, opt):
        assert sol.findTarget(build_tree([5, 3, 6, 2, 4, None, 7]), 9) is True
        assert sol.findTarget(build_tree([5, 3, 6, 2, 4, None, 7]), 28) is False
        assert sol.findTarget(build_tree([1]), 2) is False
    for _ in range(400):
        lst, _vals = random_bst_list(h, R.randint(1, 12), -20, 20)
        k = R.randint(-45, 45)
        assert brute.findTarget(build_tree(lst), k) == opt.findTarget(build_tree(lst), k), (lst, k)
    root = build_tree(path_list(10_000))
    timed_call(lambda: opt.findTarget(root, 10**5), 1)


@case(700)
def _(h):
    brute, opt = both(h, 700)
    for sol in (brute, opt):
        assert tree_to_list(sol.searchBST(build_tree([4, 2, 7, 1, 3]), 2)) == [2, 1, 3]
        assert sol.searchBST(build_tree([4, 2, 7, 1, 3]), 5) is None
    for _ in range(300):
        lst, _vals = random_bst_list(h, R.randint(1, 12))
        val = R.randint(-55, 55)
        root = build_tree(lst)
        a, b = brute.searchBST(root, val), opt.searchBST(root, val)
        assert a is b, (lst, val)
    root = build_tree(path_list(5000))
    timed_call(lambda: opt.searchBST(root, 4999), 1)


@case(701)
def _(h):
    brute, opt = both(h, 701)
    assert tree_to_list(opt.insertIntoBST(build_tree([4, 2, 7, 1, 3]), 5)) == [4, 2, 7, 1, 3, 5]
    assert tree_to_list(opt.insertIntoBST(build_tree([40, 20, 60, 10, 30, 50, 70]), 25)) == \
        [40, 20, 60, 10, 30, 50, 70, None, None, 25]
    assert tree_to_list(opt.insertIntoBST(None, 5)) == [5]
    for _ in range(300):
        n = R.randint(0, 12)
        lst, vals = random_bst_list(h, n) if n else ([], [])
        val = R.choice([v for v in range(-60, 61) if v not in vals])
        expected = sorted(vals + [val])
        for sol in (brute, opt):
            root = sol.insertIntoBST(build_tree(lst), val)
            assert inorder(root) == expected, (lst, val)
    root = build_tree(path_list(10_000))
    timed_call(lambda: opt.insertIntoBST(root, 10_000), 1)
    assert inorder(root) == list(range(10_001))


@case(1008)
def _(h):
    brute, opt = both(h, 1008)
    for sol in (brute, opt):
        assert tree_to_list(sol.bstFromPreorder([8, 5, 1, 7, 10, 12])) == [8, 5, 10, 1, 7, None, 12]
        assert tree_to_list(sol.bstFromPreorder([1, 3])) == [1, None, 3]
    for _ in range(300):
        vals = R.sample(range(1, 1001), R.randint(1, 20))
        root = None
        for v in vals:
            root = bst_insert(root, v, h.TreeNode)
        pre, stack = [], [root]
        while stack:
            node = stack.pop()
            if node:
                pre.append(node.val)
                stack += [node.right, node.left]
        expected = tree_to_list(root)
        assert tree_to_list(brute.bstFromPreorder(pre)) == expected, pre
        assert tree_to_list(opt.bstFromPreorder(pre)) == expected, pre
    assert inorder(opt.bstFromPreorder(list(range(100, 0, -1)))) == list(range(1, 101))
