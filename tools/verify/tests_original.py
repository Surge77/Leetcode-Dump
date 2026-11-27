"""Checks for the notes that existed before the Infosys expansion.

Notes with several python blocks (brute force + optimized) have every block checked.
"""
import random
import re
from collections import Counter, OrderedDict, deque
from itertools import combinations, permutations, product
from math import comb, isqrt

from harness import TreeNode, build_list, build_tree, case, lc_all, lc_path, list_to_py, tree_to_list

R = random.Random(2024)
BRUTE_HEADING_RE = re.compile(r"^#+ .*Code Snippet \(Brute Force\)", re.M)


def solvers(num, name="Solution"):
    """Every solution block except the brute force: brute forces are checked on small inputs by the
    '<num>-brute' cases, and the inputs here (e.g. t = 5000 for 3335) are sized for real solutions."""
    namespaces = lc_all(num, name)
    if BRUTE_HEADING_RE.search(lc_path(num).read_text(encoding="utf-8")) and len(namespaces) > 1:
        namespaces = namespaces[1:]  # the brute-force section always holds the note's first python block
    return [ns[name]() if name == "Solution" else ns[name] for ns in namespaces]


def rand_tree(n, lo=-9, hi=9, distinct=False):
    vals = R.sample(range(lo, hi + 1), n) if distinct else [R.randint(lo, hi) for _ in range(n)]
    if not vals:
        return None
    nodes = [TreeNode(v) for v in vals]
    for i in range(1, n):
        while True:
            p, side = R.randrange(i), R.choice(("left", "right"))
            if getattr(nodes[p], side) is None:
                setattr(nodes[p], side, nodes[i])
                break
    return nodes[0]


def rand_bst(vals):
    root = None
    for v in vals:
        new = TreeNode(v)
        if root is None:
            root = new
            continue
        node = root
        while True:
            side = "left" if v < node.val else "right"
            if getattr(node, side) is None:
                setattr(node, side, new)
                break
            node = getattr(node, side)
    return root


def inorder(root):
    out, stack, node = [], [], root
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        out.append(node.val)
        node = node.right
    return out


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


@case(155)
def _(h):
    for MinStack in solvers(155, "MinStack"):
        for _ in range(50):
            st, ref = MinStack(), []
            for _ in range(50):
                op = R.randrange(4)
                if op == 0 or not ref:
                    x = R.randint(-9, 9)
                    st.push(x)
                    ref.append(x)
                elif op == 1:
                    st.pop()
                    ref.pop()
                elif op == 2:
                    assert st.top() == ref[-1]
                else:
                    assert st.getMin() == min(ref)


@case(622)
def _(h):
    for Q in solvers(622, "MyCircularQueue"):
        for _ in range(50):
            k = R.randint(1, 5)
            q, ref = Q(k), deque()
            for _ in range(50):
                op = R.randrange(4)
                if op == 0:
                    x = R.randint(1, 9)
                    assert q.enQueue(x) == (len(ref) < k)
                    if len(ref) < k:
                        ref.append(x)
                elif op == 1:
                    assert q.deQueue() == bool(ref)
                    if ref:
                        ref.popleft()
                elif op == 2:
                    assert q.Front() == (ref[0] if ref else -1)
                    assert q.Rear() == (ref[-1] if ref else -1)
                assert q.isEmpty() == (not ref) and q.isFull() == (len(ref) == k)


@case(380)
def _(h):
    for RS in solvers(380, "RandomizedSet"):
        for _ in range(50):
            rs, ref = RS(), set()
            for _ in range(60):
                x, op = R.randint(1, 8), R.randrange(3)
                if op == 0:
                    assert rs.insert(x) == (x not in ref)
                    ref.add(x)
                elif op == 1:
                    assert rs.remove(x) == (x in ref)
                    ref.discard(x)
                elif ref:
                    assert rs.getRandom() in ref


# ---------------- divide & conquer, linked lists ----------------
@case(23)
def _(h):
    for S in solvers(23):
        assert S.mergeKLists([]) is None
        for _ in range(200):
            lists = [sorted(R.randint(-9, 9) for _ in range(R.randint(0, 5))) for _ in range(R.randint(0, 5))]
            got = S.mergeKLists([build_list(x) for x in lists])
            assert list_to_py(got) == sorted(v for x in lists for v in x)


@case(50)
def _(h):
    for S in solvers(50):
        for _ in range(300):
            x, n = round(R.uniform(-3, 3), 3), R.randint(-12, 12)
            if x == 0 and n < 0:
                continue
            want = x ** n
            assert abs(S.myPow(x, n) - want) <= 1e-9 * max(1, abs(want)), (x, n)
        assert S.myPow(2.0, -2147483648) == 0.0 and S.myPow(1.0, 2147483647) == 1.0


@case(141)
def _(h):
    for S in solvers(141):
        for _ in range(200):
            n = R.randint(0, 8)
            head = build_list(list(range(n)))
            pos = R.randint(-1, n - 1) if n else -1
            if pos >= 0:
                nodes, node = [], head
                while node:
                    nodes.append(node)
                    node = node.next
                nodes[-1].next = nodes[pos]  # tail links back to node `pos`
            assert S.hasCycle(head) == (pos >= 0)


@case(143)
def _(h):
    for S in solvers(143):
        for n in range(1, 12):
            head = build_list(list(range(n)))
            S.reorderList(head)
            want, l, r = [], 0, n - 1
            while l <= r:
                want.append(l)
                if l != r:
                    want.append(r)
                l, r = l + 1, r - 1
            assert list_to_py(head) == want


@case(19)
def _(h):
    for S in solvers(19):
        for size in range(1, 9):
            for k in range(1, size + 1):
                vals = list(range(size))
                got = list_to_py(S.removeNthFromEnd(build_list(vals), k))
                assert got == vals[:size - k] + vals[size - k + 1:]


@case(21)
def _(h):
    for S in solvers(21):
        for _ in range(200):
            a = sorted(R.randint(-9, 9) for _ in range(R.randint(0, 6)))
            b = sorted(R.randint(-9, 9) for _ in range(R.randint(0, 6)))
            assert list_to_py(S.mergeTwoLists(build_list(a), build_list(b))) == sorted(a + b)


@case(206)
def _(h):
    for S in solvers(206):
        for n in range(0, 10):
            assert list_to_py(S.reverseList(build_list(list(range(n))))) == list(range(n))[::-1]


# ---------------- DP & arrays ----------------
@case(152)
def _(h):
    for S in solvers(152):
        for _ in range(300):
            a = [R.randint(-4, 4) for _ in range(R.randint(1, 9))]
            best = max(eval("*".join(map(str, a[i:j + 1]))) for i in range(len(a)) for j in range(i, len(a)))
            assert S.maxProduct(a) == best, a


@case(53)
def _(h):
    for S in solvers(53):
        for _ in range(300):
            a = [R.randint(-9, 9) for _ in range(R.randint(1, 12))]
            assert S.maxSubArray(a) == max(sum(a[i:j + 1]) for i in range(len(a)) for j in range(i, len(a)))


@case(118)
def _(h):
    for S in solvers(118):
        for rows in range(1, 15):
            assert S.generate(rows) == [[comb(r, c) for c in range(r + 1)] for r in range(rows)]


@case(1394)
def _(h):
    for S in solvers(1394):
        for _ in range(300):
            a = [R.randint(1, 6) for _ in range(R.randint(1, 12))]
            cnt = Counter(a)
            assert S.findLucky(a) == max([v for v, c in cnt.items() if v == c], default=-1)


@case(383)
def _(h):
    nss = lc_all(383, "Solution")
    fns = [ns["Solution"]().canConstruct for ns in nss] + [ns["can_construct"] for ns in lc_all(383, "can_construct")]
    for f in fns:
        for _ in range(300):
            note = "".join(R.choice("abc") for _ in range(R.randint(1, 6)))
            mag = "".join(R.choice("abc") for _ in range(R.randint(1, 8)))
            assert f(note, mag) == (not Counter(note) - Counter(mag))


@case(200)
def _(h):
    for S in solvers(200):
        for _ in range(200):
            m, n = R.randint(1, 6), R.randint(1, 6)
            g = [[R.choice("01") for _ in range(n)] for _ in range(m)]
            seen, count = set(), 0
            for i in range(m):
                for j in range(n):
                    if g[i][j] == "1" and (i, j) not in seen:
                        count += 1
                        stack = [(i, j)]
                        seen.add((i, j))
                        while stack:
                            a, b = stack.pop()
                            for x, y in ((a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)):
                                if 0 <= x < m and 0 <= y < n and g[x][y] == "1" and (x, y) not in seen:
                                    seen.add((x, y))
                                    stack.append((x, y))
            assert S.numIslands([r[:] for r in g]) == count


@case(36)
def _(h):
    def valid(board):
        units = [[(r, c) for c in range(9)] for r in range(9)] + [[(r, c) for r in range(9)] for c in range(9)]
        units += [[(br + i, bc + j) for i in range(3) for j in range(3)] for br in (0, 3, 6) for bc in (0, 3, 6)]
        for unit in units:
            digits = [board[r][c] for r, c in unit if board[r][c] != "."]
            if len(digits) != len(set(digits)):
                return False
        return True
    for S in solvers(36):
        for _ in range(300):
            board = [["."] * 9 for _ in range(9)]
            for _ in range(R.randint(0, 25)):
                board[R.randrange(9)][R.randrange(9)] = str(R.randint(1, 9))
            assert S.isValidSudoku([r[:] for r in board]) == valid(board)


@case(73)
def _(h):
    for S in solvers(73):
        for _ in range(200):
            m, n = R.randint(1, 5), R.randint(1, 5)
            g = [[R.choice((0, 1, 2, 3)) for _ in range(n)] for _ in range(m)]
            rows = {i for i in range(m) if 0 in g[i]}
            cols = {j for j in range(n) if any(g[i][j] == 0 for i in range(m))}
            want = [[0 if i in rows or j in cols else g[i][j] for j in range(n)] for i in range(m)]
            S.setZeroes(g)
            assert g == want


def ref_merge(intervals):
    out = []
    for a, b in sorted(intervals):
        if out and a <= out[-1][1]:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return out


@case(435)
def _(h):
    for S in solvers(435):
        for _ in range(200):
            iv = []
            for _ in range(R.randint(1, 7)):
                a = R.randint(-5, 5)
                iv.append([a, a + R.randint(1, 4)])
            keep = max(r for r in range(len(iv) + 1) for sub in combinations(iv, r)
                       if all(x[1] <= y[0] for x, y in zip(sorted(sub), sorted(sub)[1:])))
            assert S.eraseOverlapIntervals([x[:] for x in iv]) == len(iv) - keep, iv


@case(56)
def _(h):
    for S in solvers(56):
        for _ in range(300):
            iv = []
            for _ in range(R.randint(1, 8)):
                a = R.randint(0, 15)
                iv.append([a, a + R.randint(0, 4)])
            assert sorted(S.merge([x[:] for x in iv])) == ref_merge(iv)


@case(57)
def _(h):
    for S in solvers(57):
        for _ in range(300):
            base = ref_merge([[a, a + R.randint(0, 3)] for a in (R.randint(0, 20) for _ in range(R.randint(0, 6)))])
            a = R.randint(0, 22)
            new = [a, a + R.randint(0, 5)]
            assert S.insert([x[:] for x in base], new[:]) == ref_merge(base + [new]), (base, new)


@case(48)
def _(h):
    for S in solvers(48):
        for n in range(1, 7):
            m = [[R.randint(0, 9) for _ in range(n)] for _ in range(n)]
            want = [list(r) for r in zip(*m[::-1])]
            S.rotate(m)
            assert m == want


@case(54)
def _(h):
    for S in solvers(54):
        for _ in range(200):
            m, n = R.randint(1, 6), R.randint(1, 6)
            g = [[R.randint(0, 99) for _ in range(n)] for _ in range(m)]
            want, grid = [], [r[:] for r in g]
            while grid:
                want += grid.pop(0)
                grid = [list(r) for r in zip(*grid)][::-1]
            assert S.spiralOrder([r[:] for r in g]) == want


@case(153)
def _(h):
    for S in solvers(153):
        for _ in range(300):
            a = sorted(R.sample(range(-50, 50), R.randint(1, 12)))
            k = R.randrange(len(a))
            assert S.findMin(a[k:] + a[:k]) == a[0]


@case(33)
def _(h):
    for S in solvers(33):
        for _ in range(300):
            a = sorted(R.sample(range(-20, 20), R.randint(1, 10)))
            k = R.randrange(len(a))
            rot = a[k:] + a[:k]
            t = R.randint(-21, 21)
            assert S.search(rot, t) == (rot.index(t) if t in rot else -1)


@case(69)
def _(h):
    for S in solvers(69):
        for x in list(range(0, 2000)) + [2**31 - 1] + [R.randint(0, 2**31 - 1) for _ in range(200)]:
            assert S.mySqrt(x) == isqrt(x), x


@case(74)
def _(h):
    for S in solvers(74):
        for _ in range(300):
            m, n = R.randint(1, 5), R.randint(1, 5)
            flat = sorted(R.sample(range(100), m * n))
            g = [flat[i * n:(i + 1) * n] for i in range(m)]
            t = R.randint(-1, 100)
            assert S.searchMatrix(g, t) == (t in flat)


@case(735)
def _(h):
    for S in solvers(735):
        for _ in range(300):
            a = [R.choice((-1, 1)) * R.randint(1, 5) for _ in range(R.randint(1, 9))]
            cur = a[:]
            while True:
                for i in range(len(cur) - 1):
                    if cur[i] > 0 > cur[i + 1]:
                        x, y = cur[i], -cur[i + 1]
                        cur[i:i + 2] = [cur[i]] if x > y else ([cur[i + 1]] if y > x else [])
                        break
                else:
                    break
            assert S.asteroidCollision(a[:]) == cur, a


@case(739)
def _(h):
    for S in solvers(739):
        for _ in range(300):
            t = [R.randint(30, 40) for _ in range(R.randint(1, 12))]
            want = [next((j - i for j in range(i + 1, len(t)) if t[j] > t[i]), 0) for i in range(len(t))]
            assert S.dailyTemperatures(t) == want


@case(209)
def _(h):
    for S in solvers(209):
        for _ in range(300):
            a = [R.randint(1, 6) for _ in range(R.randint(1, 10))]
            target = R.randint(1, 25)
            lens = [j - i + 1 for i in range(len(a)) for j in range(i, len(a)) if sum(a[i:j + 1]) >= target]
            assert S.minSubArrayLen(target, a) == min(lens, default=0)


@case(3423)
def _(h):
    for S in solvers(3423):
        for _ in range(300):
            a = [R.randint(-20, 20) for _ in range(R.randint(2, 10))]
            assert S.maxAdjacentDistance(a) == max(abs(a[i] - a[(i + 1) % len(a)]) for i in range(len(a)))


@case(424)
def _(h):
    for S in solvers(424):
        for _ in range(300):
            s = "".join(R.choice("AB") for _ in range(R.randint(1, 10)))
            k = R.randint(0, 3)
            want = max(j - i for i in range(len(s)) for j in range(i + 1, len(s) + 1)
                       if (j - i) - max(Counter(s[i:j]).values()) <= k)
            assert S.characterReplacement(s, k) == want, (s, k)


@case(438)
def _(h):
    for S in solvers(438):
        for _ in range(300):
            s = "".join(R.choice("ab") for _ in range(R.randint(1, 12)))
            p = "".join(R.choice("ab") for _ in range(R.randint(1, 4)))
            want = [i for i in range(len(s) - len(p) + 1) if Counter(s[i:i + len(p)]) == Counter(p)]
            assert sorted(S.findAnagrams(s, p)) == want


@case(150)
def _(h):
    def ref(tokens):
        st = []
        for t in tokens:
            if t in "+-*/" and len(t) == 1:
                b, a = st.pop(), st.pop()
                st.append(a + b if t == "+" else a - b if t == "-" else a * b if t == "*" else int(a / b))
            else:
                st.append(int(t))
        return st[0]
    for S in solvers(150):
        assert S.evalRPN(["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]) == 22
        for _ in range(300):
            tokens, depth = [str(R.randint(-9, 9))], 1
            for _ in range(R.randint(0, 5)):
                tokens.append(str(R.choice([x for x in range(-9, 10) if x != 0])))
                tokens.append(R.choice("+-*/"))
            try:
                want = ref(tokens)
            except ZeroDivisionError:
                continue
            assert S.evalRPN(tokens[:]) == want, tokens


@case(20)
def _(h):
    for S in solvers(20):
        for _ in range(500):
            s = "".join(R.choice("()[]{}") for _ in range(R.randint(1, 10)))
            t = s
            while any(p in t for p in ("()", "[]", "{}")):
                t = t.replace("()", "").replace("[]", "").replace("{}", "")
            assert S.isValid(s) == (t == ""), s


@case(227)
def _(h):
    def ref(expr):
        nums, ops = [], []
        for tok in expr.replace(" ", "").replace("+", " + ").replace("-", " - ").replace("*", " * ").replace("/", " / ").split():
            (ops if tok in "+-*/" else nums).append(tok if tok in "+-*/" else int(tok))
        vals, signs = [nums[0]], []
        for op, x in zip(ops, nums[1:]):
            if op == "*":
                vals[-1] *= x
            elif op == "/":
                vals[-1] = int(vals[-1] / x)
            else:
                signs.append(op)
                vals.append(x)
        total = vals[0]
        for op, v in zip(signs, vals[1:]):
            total = total + v if op == "+" else total - v
        return total
    for S in solvers(227):
        assert S.calculate("3+2*2") == 7 and S.calculate(" 3/2 ") == 1 and S.calculate(" 3+5 / 2 ") == 5
        for _ in range(300):
            parts = [str(R.randint(0, 20))]
            for _ in range(R.randint(0, 5)):
                op = R.choice("+-*/")
                parts += [op, str(R.randint(1, 20) if op == "/" else R.randint(0, 20))]
            expr = R.choice(("", " ")).join(parts)
            assert S.calculate(expr) == ref(expr), expr


@case(215)
def _(h):
    for S in solvers(215):
        for _ in range(300):
            a = [R.randint(-9, 9) for _ in range(R.randint(1, 12))]
            k = R.randint(1, len(a))
            assert S.findKthLargest(a[:], k) == sorted(a)[-k]


@case(11)
def _(h):
    for S in solvers(11):
        for _ in range(300):
            a = [R.randint(0, 9) for _ in range(R.randint(2, 10))]
            assert S.maxArea(a) == max(min(a[i], a[j]) * (j - i) for i in range(len(a)) for j in range(i + 1, len(a)))


@case(189)
def _(h):
    for S in solvers(189):
        for _ in range(300):
            a = list(range(R.randint(1, 10)))
            k = R.randint(0, 25)
            want = a[-(k % len(a)):] + a[:-(k % len(a))] if k % len(a) else a[:]
            S.rotate(a, k)
            assert a == want


@case(5)
def _(h):
    for S in solvers(5):
        for _ in range(300):
            s = "".join(R.choice("ab") for _ in range(R.randint(1, 12)))
            best = max(j - i for i in range(len(s)) for j in range(i + 1, len(s) + 1) if s[i:j] == s[i:j][::-1])
            got = S.longestPalindrome(s)
            assert len(got) == best and got == got[::-1] and got in s, (s, got)


# ---------------- notes that were Java-only (Python versions added) ----------------
@case(121)
def _(h):
    for S in solvers(121):
        for _ in range(300):
            p = [R.randint(0, 20) for _ in range(R.randint(1, 10))]
            assert S.maxProfit(p) == max([p[j] - p[i] for i in range(len(p)) for j in range(i, len(p))])


@case(169)
def _(h):
    for S in solvers(169):
        for _ in range(300):
            n = R.randint(1, 11)
            major = R.randint(0, 5)
            nums = [major] * (n // 2 + 1) + [R.choice([x for x in range(6) if x != major]) for _ in range(n - n // 2 - 1)]
            R.shuffle(nums)
            assert S.majorityElement(nums) == major


@case(3335)
def _(h):
    for S in solvers(3335):
        assert S.lengthAfterTransformations("abcyy", 2) == 7 and S.lengthAfterTransformations("azbk", 1) == 5
        for _ in range(100):
            s = "".join(R.choice("xyzab") for _ in range(R.randint(1, 6)))
            t = R.randint(1, 30)
            cur = s
            for _ in range(t):
                cur = "".join("ab" if c == "z" else chr(ord(c) + 1) for c in cur)
            assert S.lengthAfterTransformations(s, t) == len(cur) % (10**9 + 7)


@case(70)
def _(h):
    for S in solvers(70):
        a, b = 1, 1
        for n in range(1, 46):
            assert S.climbStairs(n) == b
            a, b = b, a + b


@case(1920)
def _(h):
    for S in solvers(1920):
        for n in range(1, 12):
            nums = list(range(n))
            R.shuffle(nums)
            assert S.buildArray(nums[:]) == [nums[x] for x in nums]


@case(2094)
def _(h):
    for S in solvers(2094):
        for _ in range(200):
            digits = [R.randint(0, 9) for _ in range(R.randint(3, 7))]
            want = sorted({int("".join(map(str, p))) for p in permutations(digits, 3) if p[0] != 0 and p[2] % 2 == 0})
            assert S.findEvenNumbers(digits) == want


@case(2918)
def _(h):
    for S in solvers(2918):
        assert S.minSum([3, 2, 0, 1, 0], [6, 5, 0]) == 12 and S.minSum([2, 0, 2, 0], [1, 4]) == -1
        for _ in range(300):
            a = [R.choice((0, 0, 1, 2, 3)) for _ in range(R.randint(1, 4))]
            b = [R.choice((0, 0, 1, 2, 3)) for _ in range(R.randint(1, 4))]
            za, zb = a.count(0), b.count(0)
            # a zero may become any positive integer; 1..40 covers every reachable minimum here
            sums_a = {sum(a) + sum(v) for v in product(range(1, 41), repeat=za)}
            sums_b = {sum(b) + sum(v) for v in product(range(1, 41), repeat=zb)}
            common = sums_a & sums_b
            assert S.minSum(a, b) == (min(common) if common else -1), (a, b)


@case(1)
def _(h):
    for S in solvers(1):
        for _ in range(300):
            nums = [R.randint(-9, 9) for _ in range(R.randint(2, 10))]
            i, j = R.sample(range(len(nums)), 2)
            target = nums[i] + nums[j]
            a, b = S.twoSum(nums, target)
            assert a != b and nums[a] + nums[b] == target


@case(1399)
def _(h):
    for S in solvers(1399):
        for n in range(1, 400):
            groups = Counter(sum(map(int, str(x))) for x in range(1, n + 1))
            assert S.countLargestGroup(n) == list(groups.values()).count(max(groups.values()))


@case(217)
def _(h):
    for S in solvers(217):
        for _ in range(300):
            a = [R.randint(0, 12) for _ in range(R.randint(1, 8))]
            assert S.containsDuplicate(a) == (len(set(a)) < len(a))


@case(2176)
def _(h):
    for S in solvers(2176):
        for _ in range(300):
            a = [R.randint(1, 3) for _ in range(R.randint(1, 12))]
            k = R.randint(1, 8)
            want = sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] == a[j] and i * j % k == 0)
            assert S.countPairs(a, k) == want


@case(242)
def _(h):
    for S in solvers(242):
        for _ in range(300):
            s = "".join(R.choice("abc") for _ in range(R.randint(1, 6)))
            t = "".join(R.sample(s, len(s))) if R.random() < 0.5 else "".join(R.choice("abc") for _ in range(R.randint(1, 6)))
            assert S.isAnagram(s, t) == (sorted(s) == sorted(t))


@case(49)
def _(h):
    for S in solvers(49):
        for _ in range(200):
            words = ["".join(R.choice("ab") for _ in range(R.randint(0, 3))) for _ in range(R.randint(1, 8))]
            got = sorted(sorted(g) for g in S.groupAnagrams(words))
            by_key = {}
            for w in words:
                by_key.setdefault("".join(sorted(w)), []).append(w)
            assert got == sorted(sorted(g) for g in by_key.values())


@case(2563)
def _(h):
    for S in solvers(2563):
        for _ in range(300):
            a = [R.randint(-9, 9) for _ in range(R.randint(1, 10))]
            lo = R.randint(-15, 10)
            hi = lo + R.randint(0, 10)
            want = sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if lo <= a[i] + a[j] <= hi)
            assert S.countFairPairs(a, lo, hi) == want


@case(704)
def _(h):
    for S in solvers(704):
        for _ in range(300):
            a = sorted(R.sample(range(-20, 20), R.randint(1, 10)))
            t = R.randint(-21, 21)
            assert S.search(a, t) == (a.index(t) if t in a else -1)


@case(238)
def _(h):
    for S in solvers(238):
        for _ in range(300):
            a = [R.randint(-3, 3) for _ in range(R.randint(2, 8))]
            want = []
            for i in range(len(a)):
                p = 1
                for j, x in enumerate(a):
                    if j != i:
                        p *= x
                want.append(p)
            assert S.productExceptSelf(a) == want


@case(2894)
def _(h):
    for S in solvers(2894):
        for n in range(1, 60):
            for m in range(1, 12):
                want = sum(x for x in range(1, n + 1) if x % m) - sum(x for x in range(1, n + 1) if x % m == 0)
                assert S.differenceOfSums(n, m) == want


@case(38)
def _(h):
    seq = ["1", "11", "21", "1211", "111221", "312211", "13112221", "1113213211", "31131211131221"]
    for S in solvers(38):
        for n, want in enumerate(seq, 1):
            assert S.countAndSay(n) == want


@case(2444)
def _(h):
    for S in solvers(2444):
        assert S.countSubarrays([1, 3, 5, 2, 7, 5], 1, 5) == 2 and S.countSubarrays([1, 1, 1, 1], 1, 1) == 10
        for _ in range(300):
            a = [R.randint(1, 5) for _ in range(R.randint(1, 10))]
            lo = R.randint(1, 5)
            hi = R.randint(lo, 5)
            want = sum(1 for i in range(len(a)) for j in range(i, len(a)) if min(a[i:j + 1]) == lo and max(a[i:j + 1]) == hi)
            assert S.countSubarrays(a, lo, hi) == want


@case(2799)
def _(h):
    for S in solvers(2799):
        for _ in range(300):
            a = [R.randint(1, 4) for _ in range(R.randint(1, 10))]
            k = len(set(a))
            assert S.countCompleteSubarrays(a) == sum(1 for i in range(len(a)) for j in range(i, len(a)) if len(set(a[i:j + 1])) == k)


@case(3392)
def _(h):
    for S in solvers(3392):
        assert S.countSubarrays([1, 2, 1, 4, 1]) == 1 and S.countSubarrays([1, 1, 1]) == 0
        for _ in range(300):
            a = [R.randint(-6, 6) for _ in range(R.randint(3, 10))]
            assert S.countSubarrays(a) == sum(1 for i in range(len(a) - 2) if a[i] + a[i + 2] == a[i + 1] / 2)


@case(347)
def _(h):
    for S in solvers(347):
        for _ in range(300):
            a = [R.randint(1, 6) for _ in range(R.randint(1, 15))]
            cnt = Counter(a)
            k = R.randint(1, len(cnt))
            got = S.topKFrequent(a, k)
            assert len(got) == k == len(set(got))
            assert sorted((cnt[x] for x in got), reverse=True) == sorted(cnt.values(), reverse=True)[:k]


@case(125)
def _(h):
    for S in solvers(125):
        assert S.isPalindrome("A man, a plan, a canal: Panama") and not S.isPalindrome("race a car") and S.isPalindrome(" ")
        for _ in range(300):
            s = "".join(R.choice("aA b,1") for _ in range(R.randint(1, 10)))
            clean = [c.lower() for c in s if c.isalnum()]
            assert S.isPalindrome(s) == (clean == clean[::-1]), s


@case(1550)
def _(h):
    for S in solvers(1550):
        for _ in range(300):
            a = [R.randint(1, 6) for _ in range(R.randint(1, 10))]
            assert S.threeConsecutiveOdds(a) == any(all(x % 2 for x in a[i:i + 3]) for i in range(len(a) - 2))


@case(26)
def _(h):
    for S in solvers(26):
        for _ in range(300):
            a = sorted(R.randint(-5, 5) for _ in range(R.randint(1, 12)))
            k = S.removeDuplicates(a_copy := a[:])
            assert a_copy[:k] == sorted(set(a))


@case(283)
def _(h):
    for S in solvers(283):
        for _ in range(300):
            a = [R.choice((0, 0, 1, 2, 3)) for _ in range(R.randint(1, 10))]
            b = a[:]
            S.moveZeroes(b)
            assert b == [x for x in a if x] + [0] * a.count(0)


@case(2900)
def _(h):
    for S in solvers(2900):
        for _ in range(300):
            n = R.randint(1, 10)
            words = [f"w{i}" for i in range(n)]
            groups = [R.randint(0, 1) for _ in range(n)]
            got = S.getLongestSubsequence(words, groups)
            idx = [words.index(w) for w in got]
            assert idx == sorted(set(idx)) and all(groups[a] != groups[b] for a, b in zip(idx, idx[1:]))
            assert len(got) == 1 + sum(1 for a, b in zip(groups, groups[1:]) if a != b)


@case(75)
def _(h):
    for S in solvers(75):
        for _ in range(300):
            a = [R.randint(0, 2) for _ in range(R.randint(1, 12))]
            b = a[:]
            S.sortColors(b)
            assert b == sorted(a)


@case(9)
def _(h):
    for S in solvers(9):
        for x in list(range(-20, 2000)) + [R.randint(-2**31, 2**31 - 1) for _ in range(300)]:
            assert S.isPalindrome(x) == (str(x) == str(x)[::-1]), x


@case("3335-mod")
def _(h):
    # answers far beyond 10^9 + 7, compared with exact big-integer counting
    for S in solvers(3335):
        for s, t in (("zzzzz", 5000), ("abcxyz", 3000)):
            cnt = [0] * 26
            for c in s:
                cnt[ord(c) - 97] += 1
            for _ in range(t):
                cnt = [cnt[25], cnt[0] + cnt[25]] + cnt[1:25]
            assert sum(cnt) > 10**9 + 7
            assert S.lengthAfterTransformations(s, t) == sum(cnt) % (10**9 + 7)
