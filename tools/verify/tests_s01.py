"""Tree traversal notes: inorder, symmetric, level order, zigzag, build from inorder + postorder,
balanced, path sum, flatten.

Each note has a brute force and an optimized block; both must agree on random trees and on
LeetCode's examples. Deep chains run under Python's default recursion limit so a note cannot
pass only because verify.py raised it.
"""
import random
import sys

from harness import TreeNode, build_tree, case, tree_to_list
from tests_b10 import timed_call

R = random.Random(9401)
DEFAULT_RECURSION_LIMIT = 1000


def both(h, num):
    brute, opt = h.lc_all(num, "Solution")
    return brute["Solution"](), opt["Solution"]()


def random_tree(n, lo=-5, hi=5, unique=False):
    """Random-shape tree with n nodes: each new node takes a random free child slot."""
    if n == 0:
        return None
    values = R.sample(range(lo, hi + 1), n) if unique else [R.randint(lo, hi) for _ in range(n)]
    root = TreeNode(values[0])
    slots = [(root, "left"), (root, "right")]
    for v in values[1:]:
        parent, side = slots.pop(R.randrange(len(slots)))
        child = TreeNode(v)
        setattr(parent, side, child)
        slots += [(child, "left"), (child, "right")]
    return root


def chain(n, side="left"):
    """Path 1 -> 2 -> ... -> n going down `side`."""
    root = None
    for v in range(n, 0, -1):
        root = TreeNode(v, root, None) if side == "left" else TreeNode(v, None, root)
    return root


def mirror(node):
    return None if node is None else TreeNode(node.val, mirror(node.right), mirror(node.left))


def preorder_nodes(root):
    out, stack = [], [root] if root else []
    while stack:
        node = stack.pop()
        out.append(node)
        stack += [c for c in (node.right, node.left) if c]
    return out


def inorder(root):
    out, stack, node = [], [], root
    while node or stack:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        out.append(node.val)
        node = node.right
    return out


def postorder(root):
    out, stack = [], [root] if root else []
    while stack:
        node = stack.pop()
        out.append(node.val)
        stack += [c for c in (node.left, node.right) if c]
    return out[::-1]


def leaf_sums(root):
    out, stack = [], [(root, 0)] if root else []
    while stack:
        node, total = stack.pop()
        total += node.val
        if not node.left and not node.right:
            out.append(total)
        stack += [(c, total) for c in (node.left, node.right) if c]
    return out


def with_default_limit(fn):
    """Run fn under LeetCode's default recursion limit, then restore verify.py's."""
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(DEFAULT_RECURSION_LIMIT)
    try:
        return fn()
    finally:
        sys.setrecursionlimit(old)


@case(94)
def _(h):
    brute, opt = both(h, 94)
    assert opt.inorderTraversal(build_tree([1, None, 2, 3])) == [1, 3, 2]
    assert opt.inorderTraversal(build_tree([1, 2, 3, 4, 5, None, 8, None, None, 6, 7, 9])) == [4, 2, 6, 5, 7, 1, 3, 9, 8]
    assert opt.inorderTraversal(None) == [] and opt.inorderTraversal(build_tree([1])) == [1]
    for _ in range(300):
        root = random_tree(R.randint(0, 15))
        assert brute.inorderTraversal(root) == opt.inorderTraversal(root) == inorder(root), tree_to_list(root)
    for side in ("left", "right"):
        assert with_default_limit(lambda: opt.inorderTraversal(chain(100, side))) == list(range(100, 0, -1) if side == "left" else range(1, 101))


def perturb(root):
    node = R.choice(preorder_nodes(root))
    action = R.randrange(3)
    if action == 0:
        node.val += 1
    elif action == 1:
        node.left = None
    else:
        node.right = node.right or TreeNode(0)


@case(101)
def _(h):
    brute, opt = both(h, 101)
    assert opt.isSymmetric(build_tree([1, 2, 2, 3, 4, 4, 3])) is True
    assert opt.isSymmetric(build_tree([1, 2, 2, None, 3, None, 3])) is False
    assert opt.isSymmetric(build_tree([1, 2, 2, 2, None, 2])) is False  # inorder is a palindrome, the shape is not
    assert opt.isSymmetric(build_tree([1])) is True
    symmetric = 0
    for _ in range(400):
        if R.random() < 0.25:
            root = random_tree(R.randint(1, 8), 0, 1)
        else:
            side = random_tree(R.randint(0, 7), 0, 2)
            root = TreeNode(R.randint(0, 2), side, mirror(side))
            if R.random() < 0.5:
                perturb(root)
        got = opt.isSymmetric(root)
        assert brute.isSymmetric(root) == got, tree_to_list(root)
        symmetric += got
    assert 50 < symmetric < 350, symmetric
    deep = chain(499)
    tall = TreeNode(0, deep, mirror(deep))
    for sol in (brute, opt):
        assert with_default_limit(lambda: sol.isSymmetric(tall)) is True


@case(102)
def _(h):
    brute, opt = both(h, 102)
    assert opt.levelOrder(build_tree([3, 9, 20, None, None, 15, 7])) == [[3], [9, 20], [15, 7]]
    assert opt.levelOrder(build_tree([1])) == [[1]] and opt.levelOrder(None) == []
    for _ in range(300):
        root = random_tree(R.randint(0, 15))
        assert brute.levelOrder(root) == opt.levelOrder(root), tree_to_list(root)
    deep = chain(2000, "right")
    assert with_default_limit(lambda: brute.levelOrder(deep)) == [[v] for v in range(1, 2001)]
    timed_call(lambda: opt.levelOrder(random_tree(2000)), 1)


@case(103)
def _(h):
    brute, opt = both(h, 103)
    assert opt.zigzagLevelOrder(build_tree([3, 9, 20, None, None, 15, 7])) == [[3], [20, 9], [15, 7]]
    assert opt.zigzagLevelOrder(build_tree([1])) == [[1]] and opt.zigzagLevelOrder(None) == []
    assert opt.zigzagLevelOrder(build_tree([1, 2, 3, 4, 5, 6, 7, 8, 9])) == [[1], [3, 2], [4, 5, 6, 7], [9, 8]]
    for _ in range(300):
        root = random_tree(R.randint(0, 15))
        assert brute.zigzagLevelOrder(root) == opt.zigzagLevelOrder(root), tree_to_list(root)
    timed_call(lambda: opt.zigzagLevelOrder(random_tree(2000)), 1)


@case(106)
def _(h):
    brute, opt = both(h, 106)
    assert tree_to_list(opt.buildTree([9, 3, 15, 20, 7], [9, 15, 7, 20, 3])) == [3, 9, 20, None, None, 15, 7]
    assert tree_to_list(opt.buildTree([-1], [-1])) == [-1]
    for _ in range(300):
        root = random_tree(R.randint(1, 15), -3000, 3000, unique=True)
        ino, post = inorder(root), postorder(root)
        expected = tree_to_list(root)
        assert tree_to_list(brute.buildTree(ino[:], post[:])) == expected, expected
        assert tree_to_list(opt.buildTree(ino[:], post[:])) == expected, expected
    for side in ("left", "right"):
        deep = chain(3000, side)
        ino, post = inorder(deep), postorder(deep)
        for sol in (brute, opt):
            built = with_default_limit(lambda: sol.buildTree(ino, post))
            assert inorder(built) == ino and postorder(built) == post, side
    big = random_tree(3000, -3000, 3000, unique=True)
    ino, post = inorder(big), postorder(big)
    timed_call(lambda: opt.buildTree(ino, post), 1)


@case(110)
def _(h):
    brute, opt = both(h, 110)
    assert opt.isBalanced(build_tree([3, 9, 20, None, None, 15, 7])) is True
    assert opt.isBalanced(build_tree([1, 2, 2, 3, 3, None, None, 4, 4])) is False
    assert opt.isBalanced(None) is True
    assert opt.isBalanced(build_tree([1, 2, 2, 3, None, None, 3, 4, None, None, 4])) is False  # root alone looks fine
    assert opt.isBalanced(chain(2)) is True and opt.isBalanced(chain(3)) is False
    balanced = 0
    for _ in range(400):
        root = random_tree(R.randint(0, 12))
        got = opt.isBalanced(root)
        assert brute.isBalanced(root) == got, tree_to_list(root)
        balanced += got
    assert 40 < balanced < 360, balanced
    for sol in (brute, opt):
        assert with_default_limit(lambda: sol.isBalanced(chain(5000))) is False
        complete = build_tree(list(range(5000)))
        assert with_default_limit(lambda: sol.isBalanced(complete)) is True
    timed_call(lambda: opt.isBalanced(build_tree(list(range(5000)))), 1)


@case(112)
def _(h):
    brute, opt = both(h, 112)
    assert opt.hasPathSum(build_tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1]), 22) is True
    assert opt.hasPathSum(build_tree([1, 2, 3]), 5) is False
    assert opt.hasPathSum(None, 0) is False
    assert opt.hasPathSum(build_tree([1, 2]), 1) is False  # node 1 is not a leaf
    found = 0
    for _ in range(400):
        root = random_tree(R.randint(0, 12), -4, 4)
        sums = leaf_sums(root)
        target = R.choice(sums) if sums and R.random() < 0.5 else R.randint(-12, 12)
        got = opt.hasPathSum(root, target)
        assert brute.hasPathSum(root, target) == got == (target in sums), (tree_to_list(root), target)
        found += got
    assert 100 < found < 350, found
    deep = chain(5000, "right")
    total = 5000 * 5001 // 2
    for sol in (brute, opt):
        assert with_default_limit(lambda: sol.hasPathSum(deep, total)) is True
        assert with_default_limit(lambda: sol.hasPathSum(deep, total - 1)) is False
    big = random_tree(5000, -1000, 1000)
    timed_call(lambda: opt.hasPathSum(big, 1001), 1)


def flattened(root):
    """Values along the right chain; fails if any left pointer survived."""
    out = []
    while root:
        assert root.left is None, "left pointer not cleared"
        out.append(root)
        root = root.right
    return out


@case(114)
def _(h):
    brute, opt = both(h, 114)
    root = build_tree([1, 2, 5, 3, 4, None, 6])
    opt.flatten(root)
    assert tree_to_list(root) == [1, None, 2, None, 3, None, 4, None, 5, None, 6]
    root = build_tree([0])
    opt.flatten(root)
    assert tree_to_list(root) == [0]
    assert opt.flatten(None) is None and brute.flatten(None) is None
    for _ in range(300):
        shape = tree_to_list(random_tree(R.randint(0, 15)))
        a, b = build_tree(shape), build_tree(shape)
        nodes_b = preorder_nodes(b)
        brute.flatten(a)
        opt.flatten(b)
        assert [n.val for n in flattened(a)] == [n.val for n in nodes_b], shape
        assert flattened(b) == nodes_b, shape  # same node objects, re-linked in preorder
    for side in ("left", "right"):
        deep = chain(2000, side)
        with_default_limit(lambda: opt.flatten(deep))
        assert [n.val for n in flattened(deep)] == list(range(1, 2001))
    big = random_tree(2000)
    expected = preorder_nodes(big)
    timed_call(lambda: opt.flatten(big), 1)
    assert flattened(big) == expected
