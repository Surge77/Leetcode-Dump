import random
from itertools import combinations, permutations, product

from harness import case, TreeNode

R = random.Random(3)


def random_tree(n):
    nodes = [TreeNode(R.randint(0, 9)) for _ in range(n)]
    parent = {}
    for i in range(1, n):
        while True:
            p = R.randrange(i)
            side = R.choice(("left", "right"))
            if getattr(nodes[p], side) is None:
                setattr(nodes[p], side, nodes[i])
                parent[i] = p
                break
    return nodes, parent


@case(312)
def _(h):
    S = h.lc(312)["Solution"]()
    assert S.maxCoins([3, 1, 5, 8]) == 167 and S.maxCoins([1, 5]) == 10
    for _ in range(200):
        a = [R.randint(0, 6) for _ in range(R.randint(1, 5))]
        best = 0
        for order in permutations(range(len(a))):
            alive, coins = list(range(len(a))), 0
            for idx in order:
                p = alive.index(idx)
                left = a[alive[p - 1]] if p > 0 else 1
                right = a[alive[p + 1]] if p + 1 < len(alive) else 1
                coins += left * a[idx] * right
                alive.pop(p)
            best = max(best, coins)
        assert S.maxCoins(a) == best, a


@case(516)
def _(h):
    S = h.lc(516)["Solution"]()
    assert S.longestPalindromeSubseq("bbbab") == 4 and S.longestPalindromeSubseq("cbbd") == 2
    for _ in range(300):
        s = "".join(R.choice("abc") for _ in range(R.randint(1, 10)))
        want = max(k for k in range(1, len(s) + 1) for c in combinations(s, k) if list(c) == list(c)[::-1])
        assert S.longestPalindromeSubseq(s) == want, s


@case(698)
def _(h):
    S = h.lc(698)["Solution"]()
    assert S.canPartitionKSubsets([4, 3, 2, 3, 5, 2, 1], 4) and not S.canPartitionKSubsets([1, 2, 3, 4], 3)
    for _ in range(300):
        a = [R.randint(1, 6) for _ in range(R.randint(1, 7))]
        k = R.randint(1, 3)
        want = any(len({sum(x for x, b in zip(a, assign) if b == j) for j in range(k)}) == 1
                   for assign in product(range(k), repeat=len(a)))
        assert S.canPartitionKSubsets(a[:], k) == want, (a, k)


@case(847)
def _(h):
    S = h.lc(847)["Solution"]()
    assert S.shortestPathLength([[1, 2, 3], [0], [0], [0]]) == 4
    assert S.shortestPathLength([[1], [0, 2, 4], [1, 3, 4], [2], [1, 2]]) == 4
    for _ in range(200):
        n = R.randint(1, 6)
        edges = {(i, R.randrange(i)) for i in range(1, n)}  # spanning tree => connected
        edges |= {tuple(sorted(R.sample(range(n), 2))) for _ in range(R.randint(0, 4))} if n > 1 else set()
        g = [[] for _ in range(n)]
        for u, v in edges:
            if v not in g[u]:
                g[u].append(v)
                g[v].append(u)
        INF = 99
        d = [[0 if i == j else (1 if j in g[i] else INF) for j in range(n)] for i in range(n)]
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    d[i][j] = min(d[i][j], d[i][k] + d[k][j])
        want = min(sum(d[p[i]][p[i + 1]] for i in range(n - 1)) for p in permutations(range(n)))
        assert S.shortestPathLength(g) == want, g


@case(1986)
def _(h):
    S = h.lc(1986)["Solution"]()
    assert S.minSessions([1, 2, 3], 3) == 2 and S.minSessions([3, 1, 3, 1, 1], 8) == 2
    for _ in range(300):
        T = R.randint(5, 12)
        tasks = [R.randint(1, T) for _ in range(R.randint(1, 7))]
        best = [len(tasks)]

        def go(i, bins):
            if len(bins) >= best[0]:
                return
            if i == len(tasks):
                best[0] = len(bins)
                return
            for b in range(len(bins)):
                if bins[b] + tasks[i] <= T:
                    bins[b] += tasks[i]
                    go(i + 1, bins)
                    bins[b] -= tasks[i]
            go(i + 1, bins + [tasks[i]])
        go(0, [])
        assert S.minSessions(tasks, T) == best[0], (tasks, T)


@case(233)
def _(h):
    S = h.lc(233)["Solution"]()
    run = 0
    for n in range(0, 3001):
        run += str(n).count("1")
        if n % 7 == 0 or n < 50:
            assert S.countDigitOne(n) == run, n
    assert S.countDigitOne(10**9) == 900000001


@case(902)
def _(h):
    S = h.lc(902)["Solution"]()
    assert S.atMostNGivenDigitSet(["1", "3", "5", "7"], 100) == 20
    assert S.atMostNGivenDigitSet(["1", "4", "9"], 1000000000) == 29523
    assert S.atMostNGivenDigitSet(["7"], 8) == 1
    for _ in range(300):
        ds = sorted(R.sample("123456789", R.randint(1, 4)))
        n = R.randint(1, 3000)
        want = sum(1 for x in range(1, n + 1) if set(str(x)) <= set(ds))
        assert S.atMostNGivenDigitSet(ds, n) == want, (ds, n)


@case(337)
def _(h):
    S = h.lc(337)["Solution"]()
    assert S.rob(h.build_tree([3, 2, 3, None, 3, None, 1])) == 7
    assert S.rob(None) == 0
    for _ in range(300):
        n = R.randint(1, 10)
        nodes, parent = random_tree(n)
        best = 0
        for m in range(1 << n):
            if all(not (m >> c & 1 and m >> p & 1) for c, p in parent.items()):
                best = max(best, sum(nodes[i].val for i in range(n) if m >> i & 1))
        assert S.rob(nodes[0]) == best
    chain = TreeNode(1)
    cur = chain
    for _ in range(20000):
        cur.left = TreeNode(1)
        cur = cur.left
    assert S.rob(chain) == 10001  # deep tree: iterative, no RecursionError


@case(968)
def _(h):
    S = h.lc(968)["Solution"]()
    assert S.minCameraCover(h.build_tree([0, 0, None, 0, 0])) == 1
    assert S.minCameraCover(h.build_tree([0, 0, None, 0, None, 0, None, None, 0])) == 2
    for _ in range(300):
        n = R.randint(1, 10)
        nodes, parent = random_tree(n)
        adj = {i: {i} for i in range(n)}
        for c, p in parent.items():
            adj[c].add(p)
            adj[p].add(c)
        best = min(bin(m).count("1") for m in range(1, 1 << n)
                   if all(any(m >> j & 1 for j in adj[i]) for i in range(n)))
        assert S.minCameraCover(nodes[0]) == best
