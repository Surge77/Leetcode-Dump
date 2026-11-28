"""Checks for the notes that existed before the Infosys expansion (part 2 of 4).

Shared helpers: helpers_original.py.
"""
from helpers_original import (  # noqa: F401
    Counter,
    R,
    build_list,
    case,
    comb,
    combinations,
    deque,
    lc_all,
    list_to_py,
    ref_merge,
    solvers,
)


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
