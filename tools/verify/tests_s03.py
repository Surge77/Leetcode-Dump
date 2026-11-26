"""Sheet coverage s03: tree traversals (diameter, level averages, width, distance K, vertical order,
good nodes) and in-place Game of Life.

Each note has a brute force and an optimized block; both must agree on random inputs and on
LeetCode's examples, and the optimized one is run once at max constraints where size matters.
"""
import random

from harness import case
from tests_b10 import timed_call

R = random.Random(303)


def both(h, num):
    brute, opt = h.lc_all(num, "Solution")
    return brute["Solution"](), opt["Solution"]()


def random_tree(h, vals, deep=False):
    """Random binary tree holding `vals`; `deep` keeps growing from the newest node (path-like)."""
    if not vals:
        return None
    root = h.TreeNode(vals[0])
    slots = [(root, "left"), (root, "right")]
    for v in vals[1:]:
        i = len(slots) - 1 - R.randrange(2) if deep else R.randrange(len(slots))
        slots[i], slots[-1] = slots[-1], slots[i]
        parent, side = slots.pop()
        node = h.TreeNode(v)
        setattr(parent, side, node)
        slots += [(node, "left"), (node, "right")]
    return root


def path_tree(h, vals, side=None):
    """One node per level; `side` fixes the direction, otherwise it zig-zags randomly."""
    root = cur = h.TreeNode(vals[0])
    for v in vals[1:]:
        node = h.TreeNode(v)
        setattr(cur, side or R.choice(("left", "right")), node)
        cur = node
    return root


def all_nodes(root):
    out, stack = [], [root]
    while stack:
        node = stack.pop()
        if node:
            out.append(node)
            stack += [node.left, node.right]
    return out


@case(543)
def _(h):
    brute, opt = both(h, 543)
    assert opt.diameterOfBinaryTree(h.build_tree([1, 2, 3, 4, 5])) == 3
    assert opt.diameterOfBinaryTree(h.build_tree([1, 2])) == 1
    assert opt.diameterOfBinaryTree(h.build_tree([1])) == 0
    for _ in range(250):
        vals = [R.randint(-100, 100) for _ in range(R.randint(1, 14))]
        root = random_tree(h, vals, deep=R.random() < 0.3)
        assert brute.diameterOfBinaryTree(root) == opt.diameterOfBinaryTree(root), h.tree_to_list(root)
    n = 10_000
    assert opt.diameterOfBinaryTree(path_tree(h, [0] * n)) == n - 1
    big = random_tree(h, [R.randint(-100, 100) for _ in range(n)])
    timed_call(lambda: opt.diameterOfBinaryTree(big), 1)


@case(637)
def _(h):
    brute, opt = both(h, 637)
    assert opt.averageOfLevels(h.build_tree([3, 9, 20, None, None, 15, 7])) == [3.0, 14.5, 11.0]
    assert opt.averageOfLevels(h.build_tree([3, 9, 20, 15, 7])) == [3.0, 14.5, 11.0]
    for _ in range(250):
        vals = [R.randint(-2**31, 2**31 - 1) for _ in range(R.randint(1, 14))]
        root = random_tree(h, vals, deep=R.random() < 0.3)
        want, got = brute.averageOfLevels(root), opt.averageOfLevels(root)
        assert len(want) == len(got) and all(abs(a - b) <= 1e-5 for a, b in zip(want, got)), h.tree_to_list(root)
    n = 10_000
    top = 2**31 - 1
    assert set(opt.averageOfLevels(random_tree(h, [top] * n))) == {float(top)}
    big = random_tree(h, [R.randint(-2**31, 2**31 - 1) for _ in range(n)])
    timed_call(lambda: opt.averageOfLevels(big), 1)


@case(662)
def _(h):
    brute, opt = both(h, 662)
    assert opt.widthOfBinaryTree(h.build_tree([1, 3, 2, 5, 3, None, 9])) == 4
    assert opt.widthOfBinaryTree(h.build_tree([1, 3, 2, 5, None, None, 9, 6, None, 7])) == 7
    assert opt.widthOfBinaryTree(h.build_tree([1, 3, 2, 5])) == 2
    for _ in range(300):
        vals = [R.randint(-100, 100) for _ in range(R.randint(1, 12))]
        root = random_tree(h, vals, deep=R.random() < 0.3)
        assert brute.widthOfBinaryTree(root) == opt.widthOfBinaryTree(root), h.tree_to_list(root)
    n = 3000
    assert opt.widthOfBinaryTree(path_tree(h, [0] * n)) == 1
    fork = h.TreeNode(0, path_tree(h, [0] * 30, "left"), path_tree(h, [0] * 30, "right"))
    assert opt.widthOfBinaryTree(fork) == 2**30  # two paths diverging at the root, depth 30
    big = random_tree(h, [0] * n)
    timed_call(lambda: opt.widthOfBinaryTree(big), 1)


@case(863)
def _(h):
    brute, opt = both(h, 863)
    root = h.build_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    assert sorted(opt.distanceK(root, h.find_node(root, 5), 2)) == [1, 4, 7]
    one = h.build_tree([1])
    assert opt.distanceK(one, one, 3) == []
    assert opt.distanceK(root, h.find_node(root, 2), 0) == [2]
    for _ in range(300):
        vals = R.sample(range(501), R.randint(1, 15))
        root = random_tree(h, vals, deep=R.random() < 0.3)
        target = R.choice(all_nodes(root))
        k = R.randint(0, 7)
        want, got = sorted(brute.distanceK(root, target, k)), sorted(opt.distanceK(root, target, k))
        assert want == got, (h.tree_to_list(root), target.val, k)
    n = 500
    line = path_tree(h, list(range(n)))
    mid = h.find_node(line, n // 2)
    assert sorted(opt.distanceK(line, mid, n // 2)) == [0]
    assert opt.distanceK(line, mid, 1000) == []
    timed_call(lambda: opt.distanceK(line, mid, 100), 1)


@case(987)
def _(h):
    brute, opt = both(h, 987)
    assert opt.verticalTraversal(h.build_tree([3, 9, 20, None, None, 15, 7])) == [[9], [3, 15], [20], [7]]
    assert opt.verticalTraversal(h.build_tree([1, 2, 3, 4, 5, 6, 7])) == [[4], [2], [1, 5, 6], [3], [7]]
    assert opt.verticalTraversal(h.build_tree([1, 2, 3, 4, 6, 5, 7])) == [[4], [2], [1, 5, 6], [3], [7]]
    for _ in range(300):
        vals = [R.randint(0, 6) for _ in range(R.randint(1, 14))]
        root = random_tree(h, vals, deep=R.random() < 0.3)
        assert brute.verticalTraversal(root) == opt.verticalTraversal(root), h.tree_to_list(root)
    n = 1000
    assert opt.verticalTraversal(path_tree(h, list(range(n)), "left")) == [[v] for v in reversed(range(n))]
    big = random_tree(h, [R.randint(0, 1000) for _ in range(n)])
    timed_call(lambda: opt.verticalTraversal(big), 1)


@case(1448)
def _(h):
    brute, opt = both(h, 1448)
    assert opt.goodNodes(h.build_tree([3, 1, 4, 3, None, 1, 5])) == 4
    assert opt.goodNodes(h.build_tree([3, 3, None, 4, 2])) == 3
    assert opt.goodNodes(h.build_tree([1])) == 1
    for _ in range(300):
        vals = [R.randint(-3, 3) for _ in range(R.randint(1, 15))]
        root = random_tree(h, vals, deep=R.random() < 0.3)
        assert brute.goodNodes(root) == opt.goodNodes(root), h.tree_to_list(root)
    n = 100_000
    assert opt.goodNodes(path_tree(h, list(range(n)))) == n
    assert opt.goodNodes(path_tree(h, list(range(n, 0, -1)))) == 1
    big = random_tree(h, [R.randint(-10**4, 10**4) for _ in range(n)])
    timed_call(lambda: opt.goodNodes(big), 2)


@case(289)
def _(h):
    brute, opt = both(h, 289)
    board = [[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]]
    assert opt.gameOfLife(board) is None
    assert board == [[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0]]
    board = [[1, 1], [1, 0]]
    opt.gameOfLife(board)
    assert board == [[1, 1], [1, 1]]
    for _ in range(300):
        m, n = R.randint(1, 8), R.randint(1, 8)
        start = [[R.randint(0, 1) for _ in range(n)] for _ in range(m)]
        want, got = [row[:] for row in start], [row[:] for row in start]
        brute.gameOfLife(want)
        opt.gameOfLife(got)
        assert want == got, start
