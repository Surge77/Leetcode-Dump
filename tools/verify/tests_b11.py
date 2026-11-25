import random
from math import comb, gcd

from harness import REPO, blocks_of, case, ns_from, run_program

R = random.Random(11)
TEMPLATE = REPO / "Infosys_SP_DSE" / "Python_Contest_Template.md"


@case("TEMPLATE")
def _(h):
    blocks = blocks_of(TEMPLATE)
    t = ns_from(blocks[0])
    assert run_program(blocks[0], "4\n1 2 3 4") == "10"
    assert run_program(blocks[1], "") == "200000"

    is_p = t["sieve"](1000)
    naive = [int(x > 1 and all(x % d for d in range(2, int(x ** 0.5) + 1))) for x in range(1001)]
    assert list(is_p) == naive and list(t["sieve"](1)) == [0, 0] and list(t["sieve"](0)) == [0]

    spf = t["smallest_prime_factors"](5000)
    for x in range(2, 5001):
        f = t["factorize"](x, spf)
        prod = 1
        for p, e in f.items():
            assert naive[p] if p <= 1000 else all(p % d for d in range(2, int(p ** 0.5) + 1))
            prod *= p ** e
        assert prod == x

    MOD = t["MOD"]
    for _ in range(100):
        a = R.randint(1, MOD - 1)
        assert a * t["mod_inv"](a) % MOD == 1
    C = t["Combinatorics"](300)
    for _ in range(300):
        n, r = R.randint(0, 300), R.randint(-2, 302)
        assert C.ncr(n, r) == (comb(n, r) % MOD if 0 <= r <= n else 0)

    for _ in range(100):
        n = R.randint(1, 15)
        d = t["DSU"](n)
        naive_comp = list(range(n))
        for _ in range(20):
            a, b = R.randrange(n), R.randrange(n)
            merged = d.union(a, b)
            ca, cb = naive_comp[a], naive_comp[b]
            assert merged == (ca != cb)
            naive_comp = [ca if c == cb else c for c in naive_comp]
            assert d.components == len(set(naive_comp))

    for _ in range(100):
        n = R.randint(1, 7)
        adj = [[] for _ in range(n)]
        W = [[float("inf")] * n for _ in range(n)]
        for i in range(n):
            W[i][i] = 0
        for _ in range(R.randint(0, 12)):
            u, v, w = R.randrange(n), R.randrange(n), R.randint(0, 9)
            adj[u].append((v, w))
            W[u][v] = min(W[u][v], w)
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    W[i][j] = min(W[i][j], W[i][k] + W[k][j])
        s = R.randrange(n)
        assert t["dijkstra"](adj, s) == W[s]

    grid = ["S.#", ".##", "..."]
    assert t["bfs_grid"](grid, 0, 0) == [[0, 1, -1], [1, -1, -1], [2, 3, 4]]

    for _ in range(200):
        n = R.randint(1, 7)
        adj = [[] for _ in range(n)]
        for _ in range(R.randint(0, 9)):
            u, v = R.randrange(n), R.randrange(n)
            if u != v:
                adj[u].append(v)
        order = t["topo_order"](n, adj)
        reach = [[False] * n for _ in range(n)]
        for u in range(n):
            for v in adj[u]:
                reach[u][v] = True
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    reach[i][j] |= reach[i][k] and reach[k][j]
        if any(reach[i][i] for i in range(n)):
            assert order == []
        else:
            pos = {u: i for i, u in enumerate(order)}
            assert sorted(order) == list(range(n)) and all(pos[u] < pos[v] for u in range(n) for v in adj[u])

    n = 50000
    adj = [[] for _ in range(n)]
    for i in range(1, n):
        p = i - 1 if i % 3 else R.randrange(i)
        adj[i].append(p)
        adj[p].append(i)
    order, parent = t["iterative_dfs_order"](adj, 0)
    seen_at = {u: k for k, u in enumerate(reversed(order))}
    assert len(order) == n and parent[0] == -1
    assert all(seen_at[u] < seen_at[parent[u]] for u in range(1, n))

    for _ in range(50):
        vals = [R.randint(-20, 20) for _ in range(R.randint(1, 20))]
        fw = t["Fenwick"](len(vals))
        for i, v in enumerate(vals, 1):
            fw.add(i, v)
        st_sum = t["SegTree"](vals, lambda a, b: a + b, 0)
        st_min = t["SegTree"](vals, min, float("inf"))
        st_gcd = t["SegTree"]([abs(v) for v in vals], gcd, 0)
        for _ in range(30):
            if R.random() < 0.4:
                i, v = R.randrange(len(vals)), R.randint(-20, 20)
                fw.add(i + 1, v - vals[i])
                vals[i] = v
                st_sum.update(i, v)
                st_min.update(i, v)
                st_gcd.update(i, abs(v))
            l = R.randrange(len(vals))
            r = R.randrange(l, len(vals))
            seg = vals[l:r + 1]
            g = 0
            for v in seg:
                g = gcd(g, abs(v))
            assert fw.range_sum(l + 1, r + 1) == sum(seg) == st_sum.query(l, r)
            assert st_min.query(l, r) == min(seg) and st_gcd.query(l, r) == g

    for _ in range(200):
        lo, hi = R.randint(-50, 50), R.randint(50, 150)
        target = R.randint(lo, hi)
        assert t["first_true"](lo, hi, lambda x: x >= target) == target

    for mask in range(64):
        assert sorted(t["submasks"](mask)) == [s for s in range(64) if s & mask == s]
