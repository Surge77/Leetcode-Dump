"""Brute-force backfill bf17: each note's first python block (brute force) vs its last (optimized)."""
import random

from harness import TreeNode, blocks_of, build_tree, case, find_node, lc_path, ns_from, tree_to_list

R = random.Random(2617)


def pair(num, name="Solution"):
    blocks = blocks_of(lc_path(num))
    return ns_from(blocks[0])[name], ns_from(blocks[-1])[name]


def spec_tree(n, lo, hi):
    """Random tree shape as nested (val, left, right) tuples; None = empty."""
    if n == 0:
        return None
    left = R.randint(0, n - 1)
    return (R.randint(lo, hi), spec_tree(left, lo, hi), spec_tree(n - 1 - left, lo, hi))


def make(spec):
    if spec is None:
        return None
    return TreeNode(spec[0], make(spec[1]), make(spec[2]))


def subspecs(spec):
    if spec is None:
        return []
    return [spec] + subspecs(spec[1]) + subspecs(spec[2])


def mirror(spec):
    return None if spec is None else (spec[0], mirror(spec[2]), mirror(spec[1]))


def bst_spec(vals):
    """BST built by inserting vals in order, as a spec."""
    root = None

    def insert(node, v):
        if node is None:
            return (v, None, None)
        if v < node[0]:
            return (node[0], insert(node[1], v), node[2])
        return (node[0], node[1], insert(node[2], v))

    for v in vals:
        root = insert(root, v)
    return root


@case("100-brute")
def _(h):
    brute, opt = (cls() for cls in pair(100))
    assert brute.isSameTree(build_tree([1, 2, 3]), build_tree([1, 2, 3])) is True
    assert brute.isSameTree(build_tree([1, 2]), build_tree([1, None, 2])) is False
    assert brute.isSameTree(build_tree([1, 2, 1]), build_tree([1, 1, 2])) is False
    assert brute.isSameTree(None, None) is True
    for _ in range(300):
        p = spec_tree(R.randint(0, 7), 0, 2)
        mode = R.randrange(3)
        q = p if mode == 0 else mirror(p) if mode == 1 else spec_tree(R.randint(0, 7), 0, 2)
        want = p == q
        assert brute.isSameTree(make(p), make(q)) == opt.isSameTree(make(p), make(q)) == want, (p, q)


@case("104-brute")
def _(h):
    brute, opt = (cls() for cls in pair(104))
    assert brute.maxDepth(build_tree([3, 9, 20, None, None, 15, 7])) == 3
    assert brute.maxDepth(build_tree([1, None, 2])) == 2 and brute.maxDepth(None) == 0
    for _ in range(300):
        spec = spec_tree(R.randint(0, 12), 0, 9)
        assert brute.maxDepth(make(spec)) == opt.maxDepth(make(spec)), spec


@case("124-brute")
def _(h):
    brute, opt = (cls() for cls in pair(124))
    assert brute.maxPathSum(build_tree([1, 2, 3])) == 6
    assert brute.maxPathSum(build_tree([-10, 9, 20, None, None, 15, 7])) == 42
    assert brute.maxPathSum(build_tree([-3])) == -3
    for _ in range(300):
        spec = spec_tree(R.randint(1, 10), -10, 10)
        assert brute.maxPathSum(make(spec)) == opt.maxPathSum(make(spec)), spec


@case("199-brute")
def _(h):
    brute, opt = (cls() for cls in pair(199))
    assert brute.rightSideView(build_tree([1, 2, 3, None, 5, None, 4])) == [1, 3, 4]
    assert brute.rightSideView(build_tree([1, None, 3])) == [1, 3] and brute.rightSideView(None) == []
    for _ in range(300):
        spec = spec_tree(R.randint(0, 12), 0, 9)
        assert brute.rightSideView(make(spec)) == opt.rightSideView(make(spec)), spec


@case("226-brute")
def _(h):
    brute, opt = (cls() for cls in pair(226))
    got = brute.invertTree(build_tree([4, 2, 7, 1, 3, 6, 9]))
    assert tree_to_list(got) == [4, 7, 2, 9, 6, 3, 1]
    assert tree_to_list(brute.invertTree(build_tree([2, 1, 3]))) == [2, 3, 1] and brute.invertTree(None) is None
    for _ in range(300):
        spec = spec_tree(R.randint(0, 12), 0, 9)
        original = make(spec)
        got = brute.invertTree(original)
        assert tree_to_list(got) == tree_to_list(opt.invertTree(make(spec))) == tree_to_list(make(mirror(spec)))
        assert tree_to_list(original) == tree_to_list(make(spec)), spec  # brute force builds a copy


@case("230-brute")
def _(h):
    brute, opt = (cls() for cls in pair(230))
    assert brute.kthSmallest(build_tree([3, 1, 4, None, 2]), 1) == 1
    assert brute.kthSmallest(build_tree([5, 3, 6, 2, 4, None, None, 1]), 3) == 3
    for _ in range(300):
        vals = R.sample(range(30), R.randint(1, 12))
        spec = bst_spec(vals)
        k = R.randint(1, len(vals))
        got = brute.kthSmallest(make(spec), k)
        assert got == opt.kthSmallest(make(spec), k) == sorted(vals)[k - 1], (vals, k)


@case("236-brute")
def _(h):
    brute, opt = (cls() for cls in pair(236))
    root = build_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    assert brute.lowestCommonAncestor(root, find_node(root, 5), find_node(root, 1)).val == 3
    assert brute.lowestCommonAncestor(root, find_node(root, 5), find_node(root, 4)).val == 5
    for _ in range(300):
        n = R.randint(2, 12)
        vals = R.sample(range(40), n)
        shape = spec_tree(n, 0, 0)
        it = iter(vals)

        def relabel(s):
            if s is None:
                return None
            return (next(it), relabel(s[1]), relabel(s[2]))

        root = make(relabel(shape))
        p, q = (find_node(root, v) for v in R.sample(vals, 2))
        assert brute.lowestCommonAncestor(root, p, q) is opt.lowestCommonAncestor(root, p, q)


@case("572-brute")
def _(h):
    brute, opt = (cls() for cls in pair(572))
    assert brute.isSubtree(build_tree([3, 4, 5, 1, 2]), build_tree([4, 1, 2])) is True
    assert brute.isSubtree(build_tree([3, 4, 5, 1, 2, None, None, None, None, 0]), build_tree([4, 1, 2])) is False
    for _ in range(300):
        spec = spec_tree(R.randint(1, 10), 0, 2)
        if R.random() < 0.5:
            sub, want = R.choice(subspecs(spec)), True
        else:
            sub, want = spec_tree(R.randint(1, 4), 0, 2), None
        got = brute.isSubtree(make(spec), make(sub))
        assert got == opt.isSubtree(make(spec), make(sub)), (spec, sub)
        assert want is None or got is want, (spec, sub)


@case("98-brute")
def _(h):
    brute, opt = (cls() for cls in pair(98))
    assert brute.isValidBST(build_tree([2, 1, 3])) is True
    assert brute.isValidBST(build_tree([5, 1, 4, None, None, 3, 6])) is False
    assert brute.isValidBST(build_tree([2, 2, 2])) is False
    for _ in range(300):
        if R.random() < 0.5:
            spec = bst_spec(R.sample(range(30), R.randint(1, 10)))
            if R.random() < 0.5:  # break one value so invalid trees show up too
                nodes = subspecs(spec)
                broken = R.choice(nodes)
                spec = swap_val(spec, broken, R.randint(0, 29))
        else:
            spec = spec_tree(R.randint(1, 8), 0, 8)
        assert brute.isValidBST(make(spec)) == opt.isValidBST(make(spec)), spec


def swap_val(spec, target, new_val):
    if spec is None:
        return None
    if spec is target:
        return (new_val, spec[1], spec[2])
    return (spec[0], swap_val(spec[1], target, new_val), swap_val(spec[2], target, new_val))


@case("208-brute")
def _(h):
    brute_cls, opt_cls = pair(208, "Trie")
    trie = brute_cls()
    trie.insert("apple")
    assert trie.search("apple") is True and trie.search("app") is False
    assert trie.startsWith("app") is True
    trie.insert("app")
    assert trie.search("app") is True
    for _ in range(200):
        brute, opt = brute_cls(), opt_cls()
        for _ in range(30):
            word = "".join(R.choice("ab") for _ in range(R.randint(1, 4)))
            op = R.choice(["insert", "search", "startsWith"])
            got, want = getattr(brute, op)(word), getattr(opt, op)(word)
            assert got == want, (op, word)
