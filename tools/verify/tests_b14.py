"""Contest template helpers added with mocks 4-6: SparseTable, mat_pow, strongly_connected_components."""
import random
from math import gcd

from harness import REPO, blocks_of, case, ns_from

R = random.Random(14)


@case("TEMPLATE2")
def _(h):
    t = ns_from(blocks_of(REPO / "Infosys_SP_DSE" / "Python_Contest_Template.md")[0])

    for _ in range(200):
        vals = [R.randint(-50, 50) for _ in range(R.randint(1, 40))]
        tables = {op: t["SparseTable"](vals, op) for op in (min, max, gcd)}
        for _ in range(20):
            l = R.randrange(len(vals))
            r = R.randrange(l, len(vals))
            seg = vals[l:r + 1]
            g = 0
            for v in seg:
                g = gcd(g, v)
            assert tables[min].query(l, r) == min(seg) and tables[max].query(l, r) == max(seg)
            assert tables[gcd].query(l, r) == g

    fib = [[1, 1], [1, 0]]
    a, b = 0, 1
    for n in range(1, 90):
        a, b = b, a + b
        assert t["mat_pow"](fib, n)[0][1] == a % t["MOD"]
    for _ in range(50):
        size = R.randint(1, 4)
        m = [[R.randint(0, 5) for _ in range(size)] for _ in range(size)]
        e = R.randint(0, 6)
        want = [[int(i == j) for j in range(size)] for i in range(size)]
        for _ in range(e):
            want = [[sum(want[i][k] * m[k][j] for k in range(size)) % t["MOD"] for j in range(size)] for i in range(size)]
        assert t["mat_pow"](m, e) == want

    for _ in range(300):
        n = R.randint(1, 8)
        adj = [[] for _ in range(n)]
        for _ in range(R.randint(0, 14)):
            adj[R.randrange(n)].append(R.randrange(n))
        reach = [[i == j for j in range(n)] for i in range(n)]
        for u in range(n):
            for v in adj[u]:
                reach[u][v] = True
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    reach[i][j] = reach[i][j] or (reach[i][k] and reach[k][j])
        comp = t["strongly_connected_components"](n, adj)
        for u in range(n):
            for v in range(n):
                assert (comp[u] == comp[v]) == (reach[u][v] and reach[v][u])
            for v in adj[u]:
                assert comp[u] <= comp[v]  # ids follow a topological order of the condensation
    chain = [[i + 1] for i in range(99999)] + [[0]]  # one 100000-node cycle: no recursion
    assert len(set(t["strongly_connected_components"](100000, chain))) == 1
