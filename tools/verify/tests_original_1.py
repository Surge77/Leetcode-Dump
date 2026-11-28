"""Checks for the notes that existed before the Infosys expansion (part 1 of 4).

Shared helpers: helpers_original.py.
"""
from helpers_original import (  # noqa: F401
    OrderedDict,
    R,
    TreeNode,
    build_tree,
    case,
    combinations,
    deque,
    inorder,
    permutations,
    product,
    rand_bst,
    rand_tree,
    solvers,
    tree_to_list,
)


# ---------------- backtracking ----------------
@case(17)
def _(h):
    pad = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl", "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
    for S in solvers(17):
        assert S.letterCombinations("") == []
        for digits in ("2", "23", "79", "234"):
            assert sorted(S.letterCombinations(digits)) == sorted("".join(p) for p in product(*(pad[d] for d in digits)))


@case(22)
def _(h):
    for S in solvers(22):
        for n in range(1, 7):
            want = {"".join(p) for p in product("()", repeat=2 * n)
                    if all(p[:i].count("(") >= p[:i].count(")") for i in range(2 * n + 1)) and p.count("(") == n}
            got = S.generateParenthesis(n)
            assert len(got) == len(want) and set(got) == want


@case(46)
def _(h):
    for S in solvers(46):
        for n in range(1, 6):
            nums = R.sample(range(-9, 10), n)
            assert sorted(map(tuple, S.permute(nums[:]))) == sorted(permutations(nums))


@case(77)
def _(h):
    for S in solvers(77):
        for n in range(1, 7):
            for k in range(1, n + 1):
                assert sorted(map(tuple, S.combine(n, k))) == list(combinations(range(1, n + 1), k))


@case(78)
def _(h):
    for S in solvers(78):
        for n in range(0, 7):
            nums = R.sample(range(-9, 10), n)
            want = sorted(tuple(sorted(c)) for r in range(n + 1) for c in combinations(nums, r))
            assert sorted(tuple(sorted(s)) for s in S.subsets(nums[:])) == want


@case(90)
def _(h):
    for S in solvers(90):
        for _ in range(100):
            nums = [R.randint(1, 3) for _ in range(R.randint(0, 6))]
            want = sorted({tuple(sorted(c)) for r in range(len(nums) + 1) for c in combinations(nums, r)})
            got = sorted(tuple(sorted(s)) for s in S.subsetsWithDup(nums[:]))
            assert got == want, nums


# ---------------- bit manipulation ----------------
@case(136)
def _(h):
    for S in solvers(136):
        for _ in range(200):
            pairs = R.sample(range(-50, 50), R.randint(1, 6))
            single, rest = pairs[0], pairs[1:]
            nums = [single] + rest + rest
            R.shuffle(nums)
            assert S.singleNumber(nums) == single


@case(190)
def _(h):
    for S in solvers(190):
        for n in [0, 1, 43261596, 4294967293, 2**31] + [R.randrange(2**32) for _ in range(300)]:
            assert S.reverseBits(n) == int(f"{n:032b}"[::-1], 2), n


@case(191)
def _(h):
    for S in solvers(191):
        for n in [1, 11, 128, 2**31 - 1] + [R.randint(1, 2**31 - 1) for _ in range(300)]:
            assert S.hammingWeight(n) == bin(n).count("1")


@case(268)
def _(h):
    for S in solvers(268):
        for _ in range(200):
            n = R.randint(1, 20)
            missing = R.randint(0, n)
            nums = [x for x in range(n + 1) if x != missing]
            R.shuffle(nums)
            assert S.missingNumber(nums) == missing


@case(338)
def _(h):
    for S in solvers(338):
        for n in range(0, 200):
            assert S.countBits(n) == [bin(i).count("1") for i in range(n + 1)]


@case(371)
def _(h):
    for S in solvers(371):
        for a in range(-60, 61, 7):
            for b in range(-60, 61, 5):
                assert S.getSum(a, b) == a + b, (a, b)
        for _ in range(200):
            a, b = R.randint(-1000, 1000), R.randint(-1000, 1000)
            assert S.getSum(a, b) == a + b, (a, b)


# ---------------- trees ----------------
@case(235)
def _(h):
    for S in solvers(235):
        for _ in range(200):
            vals = R.sample(range(100), R.randint(1, 12))
            root = rand_bst(vals)
            a, b = R.choice(vals), R.choice(vals)
            node = root  # a and b are in the tree, so the walk stops before falling off it
            while node is not None and not (min(a, b) <= node.val <= max(a, b)):
                node = node.left if max(a, b) < node.val else node.right
            got = S.lowestCommonAncestor(root, h.find_node(root, a), h.find_node(root, b))
            assert got is node


@case(105)
def _(h):
    for S in solvers(105):
        for _ in range(200):
            root = rand_tree(R.randint(1, 12), -30, 30, distinct=True)
            pre, stack = [], [root]
            while stack:
                node = stack.pop()
                if node:
                    pre.append(node.val)
                    stack += [node.right, node.left]
            rebuilt = S.buildTree(pre, inorder(root))
            assert tree_to_list(rebuilt) == tree_to_list(root)


@case(100)
def _(h):
    for S in solvers(100):
        for _ in range(200):
            a = rand_tree(R.randint(0, 8), 0, 2)
            vals = tree_to_list(a)
            b = build_tree(vals) if R.random() < 0.5 else rand_tree(R.randint(0, 8), 0, 2)
            assert S.isSameTree(a, b) == (tree_to_list(a) == tree_to_list(b))


@case(104)
def _(h):
    for S in solvers(104):
        for _ in range(200):
            root = rand_tree(R.randint(0, 12))

            def depth(node):
                return 0 if node is None else 1 + max(depth(node.left), depth(node.right))
            assert S.maxDepth(root) == depth(root)


@case(199)
def _(h):
    for S in solvers(199):
        for _ in range(200):
            root = rand_tree(R.randint(0, 12))
            want, level = [], [root] if root else []
            while level:
                want.append(level[-1].val)
                level = [c for n in level for c in (n.left, n.right) if c]
            assert S.rightSideView(root) == want


@case(226)
def _(h):
    for S in solvers(226):
        for _ in range(200):
            root = rand_tree(R.randint(0, 12))

            def mirror(node):
                return None if node is None else TreeNode(node.val, mirror(node.right), mirror(node.left))
            want = tree_to_list(mirror(root))
            assert tree_to_list(S.invertTree(root)) == want


@case(230)
def _(h):
    for S in solvers(230):
        for _ in range(200):
            vals = R.sample(range(100), R.randint(1, 12))
            k = R.randint(1, len(vals))
            assert S.kthSmallest(rand_bst(vals), k) == sorted(vals)[k - 1]


@case(572)
def _(h):
    def ser(node):
        return "#" if node is None else f"({node.val},{ser(node.left)},{ser(node.right)})"
    for S in solvers(572):
        for _ in range(300):
            root = rand_tree(R.randint(1, 10), 0, 2)
            sub = rand_tree(R.randint(1, 3), 0, 2)

            def subtrees(node):
                return [] if node is None else [node] + subtrees(node.left) + subtrees(node.right)
            want = any(ser(n) == ser(sub) for n in subtrees(root))
            assert S.isSubtree(root, sub) == want


@case(98)
def _(h):
    for S in solvers(98):
        for _ in range(300):
            root = rand_bst(R.sample(range(50), R.randint(1, 10))) if R.random() < 0.5 else rand_tree(R.randint(1, 8), 0, 9)
            vals = inorder(root)
            assert S.isValidBST(root) == all(a < b for a, b in zip(vals, vals[1:]))


# ---------------- design ----------------
@case(225)
def _(h):
    for MyStack in solvers(225, "MyStack"):
        for _ in range(50):
            st, ref = MyStack(), []
            for _ in range(40):
                op = R.randrange(4)
                if op == 0 or not ref:
                    x = R.randint(1, 9)
                    st.push(x)
                    ref.append(x)
                elif op == 1:
                    assert st.pop() == ref.pop()
                elif op == 2:
                    assert st.top() == ref[-1]
                assert st.empty() == (not ref)


@case(232)
def _(h):
    for MyQueue in solvers(232, "MyQueue"):
        for _ in range(50):
            q, ref = MyQueue(), deque()
            for _ in range(40):
                op = R.randrange(4)
                if op == 0 or not ref:
                    x = R.randint(1, 9)
                    q.push(x)
                    ref.append(x)
                elif op == 1:
                    assert q.pop() == ref.popleft()
                elif op == 2:
                    assert q.peek() == ref[0]
                assert q.empty() == (not ref)


@case(146)
def _(h):
    for LRUCache in solvers(146, "LRUCache"):
        for _ in range(100):
            cap = R.randint(1, 4)
            cache, ref = LRUCache(cap), OrderedDict()
            for _ in range(60):
                key = R.randint(1, 6)
                if R.random() < 0.5:
                    want = -1
                    if key in ref:
                        ref.move_to_end(key)
                        want = ref[key]
                    assert cache.get(key) == want
                else:
                    val = R.randint(1, 99)
                    cache.put(key, val)
                    ref[key] = val
                    ref.move_to_end(key)
                    if len(ref) > cap:
                        ref.popitem(last=False)
