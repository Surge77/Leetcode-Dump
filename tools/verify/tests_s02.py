"""Tree traversal notes: next-pointer linking, root-to-leaf DFS, iterative pre/postorder,
BST iterator, complete-tree counting, path enumeration and a tree codec.

Each note has a brute force and an optimized block; both must agree on random trees and on
LeetCode's examples, and the optimized one is run once at max constraints where speed or
recursion depth is the point.
"""
import random

from harness import TreeNode, build_tree, case, tree_to_list
from tests_b10 import timed_call

R = random.Random(202)
TRAVERSAL_EXAMPLE = [1, 2, 3, 4, 5, None, 8, None, None, 6, 7, 9]


def both(h, num, name="Solution"):
    brute, opt = h.lc_all(num, name)
    return brute[name](), opt[name]()


def random_shape(n, lo, hi):
    """Level-order list of a random n-node binary tree: gaps, chains and bushy parts."""
    if n == 0:
        return []
    root = TreeNode(R.randint(lo, hi))
    slots = [(root, "left"), (root, "right")]
    for _ in range(n - 1):
        # usually a random free slot; sometimes the newest one, which grows long chains
        index = len(slots) - 1 if R.random() < 0.3 else R.randrange(len(slots))
        slots[index], slots[-1] = slots[-1], slots[index]
        parent, side = slots.pop()
        child = TreeNode(R.randint(lo, hi))
        setattr(parent, side, child)
        slots += [(child, "left"), (child, "right")]
    return tree_to_list(root)


def chain_vals(values, side):
    """Level-order list of a path that always continues on `side`."""
    out = [values[0]]
    for v in values[1:]:
        out += [v, None] if side == "left" else [None, v]
    return out


# ---------- 117 helpers: trees made of the note's own Node class ----------

def to_next_nodes(node_cls, vals):
    src = build_tree(vals)
    if src is None:
        return None
    root = node_cls(src.val)
    stack = [(src, root)]
    while stack:
        s, d = stack.pop()
        if s.left:
            d.left = node_cls(s.left.val)
            stack.append((s.left, d.left))
        if s.right:
            d.right = node_cls(s.right.val)
            stack.append((s.right, d.right))
    return root


def check_next(root):
    """Every node's `next` must be its right neighbour on the same level (None at the end)."""
    level = [root] if root else []
    while level:
        for a, b in zip(level, level[1:] + [None]):
            assert a.next is b, (a.val, None if b is None else b.val)
        level = [c for node in level for c in (node.left, node.right) if c]


def next_format(root):
    """LeetCode's output for 117: each level read through `next`, then '#'."""
    out, start = [], root
    while start:
        node, below = start, None
        while node:
            out.append(node.val)
            below = below or node.left or node.right
            node = node.next
        out.append("#")
        start = below
    return out


@case(117)
def _(h):
    brute_ns, opt_ns = h.lc_all(117, "Solution")
    for ns in (brute_ns, opt_ns):
        root = to_next_nodes(ns["Node"], [1, 2, 3, 4, 5, None, 7])
        assert ns["Solution"]().connect(root) is root
        assert next_format(root) == [1, "#", 2, 3, "#", 4, 5, 7, "#"]
        assert ns["Solution"]().connect(None) is None
    for _ in range(250):
        vals = random_shape(R.randint(0, 25), -100, 100)
        formats = []
        for ns in (brute_ns, opt_ns):
            root = to_next_nodes(ns["Node"], vals)
            assert ns["Solution"]().connect(root) is root
            check_next(root)
            assert tree_to_list(root) == vals, vals  # left/right untouched
            formats.append(next_format(root))
        assert formats[0] == formats[1], vals
    n = 6000
    opt = opt_ns["Solution"]()
    for vals in (chain_vals([R.randint(-100, 100) for _ in range(n)], "left"), random_shape(n, -100, 100)):
        root = to_next_nodes(opt_ns["Node"], vals)
        timed_call(lambda: opt.connect(root), 1)
        check_next(root)


@case(129)
def _(h):
    brute, opt = both(h, 129)
    assert opt.sumNumbers(build_tree([1, 2, 3])) == 25
    assert opt.sumNumbers(build_tree([4, 9, 0, 5, 1])) == 1026
    assert opt.sumNumbers(build_tree([1, 2])) == 12
    assert opt.sumNumbers(build_tree([0, 1])) == 1
    assert opt.sumNumbers(build_tree([7])) == 7
    for _ in range(300):
        root = build_tree(random_shape(R.randint(1, 15), 0, 9))
        assert brute.sumNumbers(root) == opt.sumNumbers(root), tree_to_list(root)
    big = build_tree([R.randint(0, 9) for _ in range(1000)])  # complete: depth exactly 10
    assert brute.sumNumbers(big) == opt.sumNumbers(big)


@case(144)
def _(h):
    brute, opt = both(h, 144)
    assert opt.preorderTraversal(build_tree([1, None, 2, 3])) == [1, 2, 3]
    assert opt.preorderTraversal(build_tree(TRAVERSAL_EXAMPLE)) == [1, 2, 4, 5, 6, 7, 3, 8, 9]
    assert opt.preorderTraversal(None) == []
    assert opt.preorderTraversal(build_tree([1])) == [1]
    for _ in range(300):
        root = build_tree(random_shape(R.randint(0, 30), -100, 100))
        assert brute.preorderTraversal(root) == opt.preorderTraversal(root), tree_to_list(root)


@case(145)
def _(h):
    brute, opt = both(h, 145)
    assert opt.postorderTraversal(build_tree([1, None, 2, 3])) == [3, 2, 1]
    assert opt.postorderTraversal(build_tree(TRAVERSAL_EXAMPLE)) == [4, 6, 7, 5, 2, 9, 8, 3, 1]
    assert opt.postorderTraversal(None) == []
    assert opt.postorderTraversal(build_tree([1])) == [1]
    for _ in range(300):
        root = build_tree(random_shape(R.randint(0, 30), -100, 100))
        assert brute.postorderTraversal(root) == opt.postorderTraversal(root), tree_to_list(root)


# ---------- 173 helpers ----------

def bst_from(values):
    """BST built by inserting `values` in order (iterative, so long chains are fine)."""
    root = None
    for v in values:
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


def chain_bst(n, side):
    """1..n as a single path: down-left from n, or down-right from 1."""
    values = range(n, 0, -1) if side == "left" else range(1, n + 1)
    root = cur = None
    for v in values:
        node = TreeNode(v)
        if root is None:
            root = cur = node
        else:
            setattr(cur, side, node)
            cur = node
    return root


def run_iterator(cls, root, ops):
    it = cls(root)
    return [it.next() if op == "next" else it.hasNext() for op in ops]


def drain(cls, root):
    it, out = cls(root), []
    while it.hasNext():
        out.append(it.next())
    return out


@case(173)
def _(h):
    brute_ns, opt_ns = h.lc_all(173, "BSTIterator")
    brute_cls, opt_cls = brute_ns["BSTIterator"], opt_ns["BSTIterator"]
    ops = ["next", "next", "hasNext", "next", "hasNext", "next", "hasNext", "next", "hasNext"]
    for cls in (brute_cls, opt_cls):
        got = run_iterator(cls, build_tree([7, 3, 15, None, None, 9, 20]), ops)
        assert got == [3, 7, True, 9, True, 15, True, 20, False], got
    for _ in range(250):
        values = R.sample(range(10**6 + 1), R.randint(1, 20))
        ops, remaining = [], len(values)
        while remaining:
            if R.random() < 0.4:
                ops.append("hasNext")
            else:
                ops.append("next")
                remaining -= 1
        ops.append("hasNext")
        got = run_iterator(opt_cls, bst_from(values), ops)
        assert got == run_iterator(brute_cls, bst_from(values), ops), (values, ops)
        assert [x for x, op in zip(got, ops) if op == "next"] == sorted(values)
        assert got[-1] is False
    n = 100_000
    for side in ("left", "right"):
        root, out = chain_bst(n, side), []
        timed_call(lambda: out.extend(drain(opt_cls, root)), 2)
        assert out == list(range(1, n + 1)), side


@case(222)
def _(h):
    brute, opt = both(h, 222)
    assert opt.countNodes(build_tree([1, 2, 3, 4, 5, 6])) == 6
    assert opt.countNodes(None) == 0
    assert opt.countNodes(build_tree([1])) == 1
    for n in range(130):  # a complete tree's shape is fixed by n, so this covers every shape
        root = build_tree(list(range(1, n + 1)))
        assert brute.countNodes(root) == opt.countNodes(root) == n, n
    for _ in range(150):
        n = R.randint(0, 3000)
        root = build_tree([R.randint(0, 5 * 10**4) for _ in range(n)])
        assert brute.countNodes(root) == opt.countNodes(root) == n, n
    n = 5 * 10**4
    root, got = build_tree(list(range(n))), []
    timed_call(lambda: got.extend(opt.countNodes(root) for _ in range(1000)), 1)
    assert set(got) == {n}


@case(257)
def _(h):
    brute, opt = both(h, 257)
    assert sorted(opt.binaryTreePaths(build_tree([1, 2, 3, None, 5]))) == ["1->2->5", "1->3"]
    assert opt.binaryTreePaths(build_tree([1])) == ["1"]
    assert opt.binaryTreePaths(build_tree([1, -5])) == ["1->-5"]
    for _ in range(300):
        root = build_tree(random_shape(R.randint(1, 20), -100, 100))
        assert sorted(brute.binaryTreePaths(root)) == sorted(opt.binaryTreePaths(root)), tree_to_list(root)


@case(297)
def _(h):
    brute_ns, opt_ns = h.lc_all(297, "Codec")
    codecs = (brute_ns["Codec"], opt_ns["Codec"])
    for codec in codecs:
        for vals in ([1, 2, 3, None, None, 4, 5], [], [-1000], [1, None, -2, 3]):
            data = codec().serialize(build_tree(vals))  # separate instances, as LeetCode does
            assert isinstance(data, str)
            assert tree_to_list(codec().deserialize(data)) == vals, (vals, data)
    for _ in range(250):
        vals = random_shape(R.randint(0, 30), -1000, 1000)
        for codec in codecs:
            root = build_tree(vals)
            copy = codec().deserialize(codec().serialize(root))
            assert tree_to_list(copy) == vals, vals
            assert root is None or copy is not root
    n = 10**4
    path = chain_vals([R.randint(-1000, 1000) for _ in range(n)], "right")
    for vals in (path, random_shape(n, -1000, 1000)):
        root, out = build_tree(vals), []
        timed_call(lambda: out.append(codecs[1]().deserialize(codecs[1]().serialize(root))), 2)
        assert tree_to_list(out[0]) == vals
