"""Graph traversal notes: ladders, flood fills, graph cloning, Union-Find, weighted ratios (part 1 of 1).

Shared helpers: helpers_s06.py.
"""
from helpers_s06 import (  # noqa: F401
    EMPTY,
    R,
    both,
    build_graph,
    case,
    copy,
    graph_to_adj,
    itertools,
    math,
    random_connected_adj,
    random_tree_edges,
    ratios_match,
    serpentine,
    timed_call,
)


@case(126)
def _(h):
    brute, opt = both(h, 126)
    words = ["hot", "dot", "dog", "lot", "log", "cog"]
    expected = [["hit", "hot", "dot", "dog", "cog"], ["hit", "hot", "lot", "log", "cog"]]
    for sol in (brute, opt):
        assert sorted(sol.findLadders("hit", "cog", words)) == expected
        assert sol.findLadders("hit", "cog", words[:-1]) == []
    runs = 0
    while runs < 300:
        pool = ["".join(p) for p in itertools.product(R.choice(("ab", "abc")), repeat=R.randint(1, 3))]
        word_list = R.sample(pool, R.randint(1, min(7, len(pool))))
        begin = R.choice(pool)
        end = R.choice(word_list if R.random() < 0.8 else pool)
        if begin == end:
            continue
        runs += 1
        got = opt.findLadders(begin, end, list(word_list))
        assert sorted(got) == sorted(brute.findLadders(begin, end, list(word_list))), (begin, end, word_list)
    every = ["".join(p) for p in itertools.product("ab", repeat=5)]
    assert len(opt.findLadders("aaaaa", "bbbbb", every)) == math.factorial(5)
    cube = ["".join(p) for p in itertools.product("abc", repeat=5)]
    others = R.sample(["".join(p) for p in itertools.product("defg", repeat=5)], 500 - len(cube))
    ladders = []
    timed_call(lambda: ladders.extend(opt.findLadders("aaaaa", "ccccc", cube + others)), 3)
    assert len(ladders) == math.factorial(5) and all(len(lad) == 6 for lad in ladders)


@case(130)
def _(h):
    brute, opt = both(h, 130)
    for sol in (brute, opt):
        board = [list(row) for row in ("XXXX", "XOOX", "XXOX", "XOXX")]
        assert sol.solve(board) is None
        assert board == [list(row) for row in ("XXXX", "XXXX", "XXXX", "XOXX")]
        board = [["X"]]
        sol.solve(board)
        assert board == [["X"]]
    for _ in range(300):
        m, n = R.randint(1, 7), R.randint(1, 7)
        board = [[R.choice("XOO") for _ in range(n)] for _ in range(m)]
        a, b = copy.deepcopy(board), copy.deepcopy(board)
        brute.solve(a)
        opt.solve(b)
        assert a == b, board
    snake = serpentine(200, True)
    kept = copy.deepcopy(snake)
    opt.solve(kept)
    assert kept == snake
    closed = serpentine(200, False)
    opt.solve(closed)
    assert all(cell == "X" for row in closed for cell in row)
    big = [["O" if R.random() < 0.6 else "X" for _ in range(200)] for _ in range(200)]
    timed_call(lambda: opt.solve(big), 2)


@case(133)
def _(h):
    graphs = [[[2, 4], [1, 3], [2, 4], [1, 3]], [[]]]
    graphs += [random_connected_adj(R.randint(1, 10)) for _ in range(200)]
    graphs.append([[j + 1 for j in range(100) if j != i] for i in range(100)])
    for ns in h.lc_all(133, "Solution"):
        sol, node_cls = ns["Solution"](), ns["Node"]
        assert sol.cloneGraph(None) is None
        for adj in graphs:
            original = build_graph(node_cls, adj)
            clone_adj, clone_ids = graph_to_adj(sol.cloneGraph(original))
            original_adj, original_ids = graph_to_adj(original)
            assert clone_adj == original_adj == adj, adj
            assert not clone_ids & original_ids, "clone shares nodes with the original"


@case(261)
def _(h):
    brute, opt = both(h, 261)
    for sol in (brute, opt):
        assert sol.validTree(5, [[0, 1], [0, 2], [0, 3], [1, 4]]) is True
        assert sol.validTree(5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]) is False
        assert sol.validTree(1, []) is True
        assert sol.validTree(2, []) is False
        assert sol.validTree(4, [[0, 1], [1, 2], [2, 0]]) is False  # n − 1 edges, yet a cycle
    for _ in range(400):
        n = R.randint(1, 8)
        edges = random_tree_edges(n)
        roll = R.random()
        present = {frozenset(e) for e in edges}
        extra = [[a, b] for a in range(n) for b in range(a + 1, n) if frozenset((a, b)) not in present]
        if roll < 0.3 and extra:
            edges.append(R.choice(extra))
        elif roll < 0.5 and edges:
            edges.pop(R.randrange(len(edges)))
        elif roll < 0.6 and edges and extra:
            edges[R.randrange(len(edges))] = R.choice(extra)
        elif roll < 0.8:
            pairs = [[a, b] for a in range(n) for b in range(a + 1, n)]
            edges = R.sample(pairs, R.randint(0, len(pairs)))
        R.shuffle(edges)
        assert brute.validTree(n, edges) == opt.validTree(n, edges), (n, edges)
    n = 2000
    assert opt.validTree(n, [[i, i + 1] for i in range(n - 1)]) is True
    tree = random_tree_edges(n)
    timed_call(lambda: opt.validTree(n, tree), 1)


@case(286)
def _(h):
    brute, opt = both(h, 286)
    inf = EMPTY
    rooms = [[inf, -1, 0, inf], [inf, inf, inf, -1], [inf, -1, inf, -1], [0, -1, inf, inf]]
    expected = [[3, -1, 0, 1], [2, 2, 1, -1], [1, -1, 2, -1], [0, -1, 3, 4]]
    for sol in (brute, opt):
        grid = copy.deepcopy(rooms)
        assert sol.wallsAndGates(grid) is None
        assert grid == expected
        grid = [[-1]]
        sol.wallsAndGates(grid)
        assert grid == [[-1]]
    for _ in range(300):
        m, n = R.randint(1, 7), R.randint(1, 7)
        grid = [[R.choice((-1, 0, inf, inf, inf, inf)) for _ in range(n)] for _ in range(m)]
        a, b = copy.deepcopy(grid), copy.deepcopy(grid)
        brute.wallsAndGates(a)
        opt.wallsAndGates(b)
        assert a == b, grid
    big = [[R.choice((-1, inf, inf, inf)) for _ in range(250)] for _ in range(250)]
    big[0][0] = big[249][249] = 0
    timed_call(lambda: opt.wallsAndGates(big), 2)


@case(323)
def _(h):
    brute, opt = both(h, 323)
    for sol in (brute, opt):
        assert sol.countComponents(5, [[0, 1], [1, 2], [3, 4]]) == 2
        assert sol.countComponents(5, [[0, 1], [1, 2], [2, 3], [3, 4]]) == 1
    for _ in range(300):
        n = R.randint(1, 10)
        pairs = [[a, b] for a in range(n) for b in range(a + 1, n)]
        edges = R.sample(pairs, R.randint(0, min(len(pairs), 12)))
        assert brute.countComponents(n, edges) == opt.countComponents(n, edges), (n, edges)
    n = 2000
    assert opt.countComponents(n, [[i, i + 1] for i in range(0, n - 1, 2)]) == n // 2
    pairs = set()
    while len(pairs) < 5000:
        a, b = sorted(R.sample(range(n), 2))
        pairs.add((a, b))
    big = [list(p) for p in pairs]
    timed_call(lambda: opt.countComponents(n, big), 1)


@case(399)
def _(h):
    brute, opt = both(h, 399)
    examples = [
        ([["a", "b"], ["b", "c"]], [2.0, 3.0],
         [["a", "c"], ["b", "a"], ["a", "e"], ["a", "a"], ["x", "x"]], [6.0, 0.5, -1.0, 1.0, -1.0]),
        ([["a", "b"], ["b", "c"], ["bc", "cd"]], [1.5, 2.5, 5.0],
         [["a", "c"], ["c", "b"], ["bc", "cd"], ["cd", "bc"]], [3.75, 0.4, 5.0, 0.2]),
        ([["a", "b"]], [0.5], [["a", "b"], ["b", "a"], ["a", "c"], ["x", "y"]], [0.5, 2.0, -1.0, -1.0]),
    ]
    for sol in (brute, opt):
        for equations, values, queries, want in examples:
            assert ratios_match(sol.calcEquation(equations, values, queries), want), (equations, queries)
    names = ["a", "b", "c", "x1", "yy", "z9", "q"]
    for _ in range(300):
        pool = names[:R.randint(2, 6)]
        if R.random() < 0.5:
            value = {v: 2.0 ** R.randint(-2, 2) for v in pool}
        else:
            value = {v: R.uniform(1, 4) for v in pool}
        equations = [R.sample(pool, 2) for _ in range(R.randint(1, 6))]
        values = [value[a] / value[b] for a, b in equations]
        queries = [[R.choice(names), R.choice(names)] for _ in range(R.randint(1, 8))]
        got = opt.calcEquation(equations, values, queries)
        assert ratios_match(got, brute.calcEquation(equations, values, queries)), (equations, queries)
        for (c, d), ans in zip(queries, got):
            assert ans == -1.0 or math.isclose(ans, value[c] / value[d], rel_tol=1e-9)


@case(417)
def _(h):
    brute, opt = both(h, 417)
    heights = [[1, 2, 2, 3, 5], [3, 2, 3, 4, 4], [2, 4, 5, 3, 1], [6, 7, 1, 4, 5], [5, 1, 1, 2, 4]]
    expected = [[0, 4], [1, 3], [1, 4], [2, 2], [3, 0], [3, 1], [4, 0]]
    for sol in (brute, opt):
        assert sorted(sol.pacificAtlantic(heights)) == expected
        assert sol.pacificAtlantic([[1]]) == [[0, 0]]
    for _ in range(300):
        m, n = R.randint(1, 7), R.randint(1, 7)
        grid = [[R.randint(0, 4) for _ in range(n)] for _ in range(m)]
        assert sorted(brute.pacificAtlantic(grid)) == sorted(opt.pacificAtlantic(grid)), grid
    flat = [[7] * 200 for _ in range(200)]
    cells = []
    timed_call(lambda: cells.extend(opt.pacificAtlantic(flat)), 2)
    assert len(cells) == 200 * 200


@case(433)
def _(h):
    brute, opt = both(h, 433)
    for sol in (brute, opt):
        assert sol.minMutation("AACCGGTT", "AACCGGTA", ["AACCGGTA"]) == 1
        assert sol.minMutation("AACCGGTT", "AAACGGTA", ["AACCGGTA", "AACCGCTA", "AAACGGTA"]) == 2
        assert sol.minMutation("AAAAACCC", "AACCCCCC", ["AAAACCCC", "AAACCCCC", "AACCCCCC"]) == 3
        assert sol.minMutation("AACCGGTT", "AACCGGTA", []) == -1
        assert sol.minMutation("AACCGGTT", "AACCGGTT", []) == 0
    for _ in range(300):
        letters = R.choice(("AC", "ACG"))
        pool = ["".join(p) + "GGTTA" for p in itertools.product(letters, repeat=3)]
        bank = R.sample(pool, R.randint(0, min(10, len(pool))))
        start = R.choice(pool)
        end = R.choice(bank) if bank and R.random() < 0.8 else R.choice(pool)
        assert brute.minMutation(start, end, bank) == opt.minMutation(start, end, bank), (start, end, bank)


@case(547)
def _(h):
    brute, opt = both(h, 547)
    for sol in (brute, opt):
        assert sol.findCircleNum([[1, 1, 0], [1, 1, 0], [0, 0, 1]]) == 2
        assert sol.findCircleNum([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) == 3
    for _ in range(300):
        n = R.randint(1, 10)
        density = R.random() * 0.4
        matrix = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if R.random() < density:
                    matrix[i][j] = matrix[j][i] = 1
        assert brute.findCircleNum(matrix) == opt.findCircleNum(matrix), matrix
    n = 200
    chain = [[1 if abs(i - j) <= 1 else 0 for j in range(n)] for i in range(n)]
    assert opt.findCircleNum(chain) == 1
    dense = [[1] * n for _ in range(n)]
    timed_call(lambda: opt.findCircleNum(dense), 1)
