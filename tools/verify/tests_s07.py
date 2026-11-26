"""Graph traversal gap notes: grid flood fills, union-find merges, reverse topological sort,
board BFS and Dijkstra path counting.

Each note has a brute force and an optimized block; both must agree on random inputs and on
LeetCode's examples, and the optimized one is run once at max constraints.
"""
import copy
import random

from harness import case
from tests_b10 import timed_call

R = random.Random(707)
MOD = 10**9 + 7


def both(h, num):
    brute, opt = h.lc_all(num, "Solution")
    return brute["Solution"](), opt["Solution"]()


def call(fn, *args):
    """Several solutions overwrite their grid argument, so every call gets its own copy."""
    return fn(*copy.deepcopy(args))


def rand_grid(rows, cols, p=0.5):
    return [[int(R.random() < p) for _ in range(cols)] for _ in range(rows)]


def snake_grid(n):
    """One serpentine island: deep enough to break a recursive DFS."""
    return [[1 if r % 2 == 0 or c == (n - 1 if r % 4 == 1 else 0) else 0 for c in range(n)] for r in range(n)]


@case(695)
def _(h):
    brute, opt = both(h, 695)
    example = [[0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
               [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0],
               [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]]
    assert call(opt.maxAreaOfIsland, example) == 6 == call(brute.maxAreaOfIsland, example)
    assert call(opt.maxAreaOfIsland, [[0] * 8]) == 0
    for _ in range(300):
        grid = rand_grid(R.randint(1, 8), R.randint(1, 8), R.random())
        assert call(brute.maxAreaOfIsland, grid) == call(opt.maxAreaOfIsland, grid), grid
    snake = snake_grid(50)
    assert call(opt.maxAreaOfIsland, snake) == sum(map(sum, snake)) == 1275
    timed_call(lambda: call(opt.maxAreaOfIsland, rand_grid(50, 50, 0.6)), 1)


def norm_accounts(result):
    """Accounts may come in any order, but each one must be [name, *sorted emails]."""
    return sorted(map(tuple, result))


@case(721)
def _(h):
    brute, opt = both(h, 721)
    ex1 = [["John", "johnsmith@mail.com", "john_newyork@mail.com"], ["John", "johnsmith@mail.com", "john00@mail.com"],
           ["Mary", "mary@mail.com"], ["John", "johnnybravo@mail.com"]]
    want1 = [["John", "john00@mail.com", "john_newyork@mail.com", "johnsmith@mail.com"], ["Mary", "mary@mail.com"],
             ["John", "johnnybravo@mail.com"]]
    assert norm_accounts(call(opt.accountsMerge, ex1)) == norm_accounts(want1)
    ex2 = [["Gabe", "Gabe0@m.co", "Gabe3@m.co", "Gabe1@m.co"], ["Kevin", "Kevin3@m.co", "Kevin5@m.co", "Kevin0@m.co"],
           ["Ethan", "Ethan5@m.co", "Ethan4@m.co", "Ethan0@m.co"], ["Hanzo", "Hanzo3@m.co", "Hanzo1@m.co", "Hanzo0@m.co"],
           ["Fern", "Fern5@m.co", "Fern1@m.co", "Fern0@m.co"]]
    want2 = [[acc[0]] + sorted(acc[1:]) for acc in ex2]
    assert norm_accounts(call(opt.accountsMerge, ex2)) == norm_accounts(want2)
    for _ in range(300):
        people = R.randint(1, 5)
        accounts = []
        for _ in range(R.randint(1, 8)):
            p = R.randrange(people)
            emails = [f"p{p}e{k}@x.com" for k in R.sample(range(5), R.randint(1, 3))]
            accounts.append(["AB"[p % 2]] + emails)  # different people may share a name
        assert norm_accounts(call(brute.accountsMerge, accounts)) == norm_accounts(call(opt.accountsMerge, accounts)), accounts
    chain = [["Ann"] + [f"e{i + k}@x.com" for k in range(9)] for i in range(1000)]
    R.shuffle(chain)
    merged = call(opt.accountsMerge, chain)
    assert len(merged) == 1 and len(merged[0]) == 1 + 1008
    timed_call(lambda: call(opt.accountsMerge, chain), 1)


@case(733)
def _(h):
    brute, opt = both(h, 733)
    assert call(opt.floodFill, [[1, 1, 1], [1, 1, 0], [1, 0, 1]], 1, 1, 2) == [[2, 2, 2], [2, 2, 0], [2, 0, 1]]
    assert call(opt.floodFill, [[0, 0, 0], [0, 0, 0]], 0, 0, 0) == [[0, 0, 0], [0, 0, 0]]
    for _ in range(300):
        rows, cols = R.randint(1, 7), R.randint(1, 7)
        image = [[R.randint(0, 2) for _ in range(cols)] for _ in range(rows)]
        sr, sc, color = R.randrange(rows), R.randrange(cols), R.randint(0, 2)
        assert call(brute.floodFill, image, sr, sc, color) == call(opt.floodFill, image, sr, sc, color), (image, sr, sc, color)
    snake = snake_grid(50)
    filled = call(opt.floodFill, snake, 0, 0, 7)
    assert sum(row.count(7) for row in filled) == 1275
    timed_call(lambda: call(opt.floodFill, [[0] * 50 for _ in range(50)], 25, 25, 1), 1)


@case(802)
def _(h):
    brute, opt = both(h, 802)
    assert opt.eventualSafeNodes([[1, 2], [2, 3], [5], [0], [5], [], []]) == [2, 4, 5, 6]
    assert opt.eventualSafeNodes([[1, 2, 3, 4], [1, 2], [3, 4], [0, 4], []]) == [4]
    for _ in range(300):
        n = R.randint(1, 9)
        graph = [sorted(R.sample(range(n), R.randint(0, min(n, 3)))) for _ in range(n)]
        assert brute.eventualSafeNodes(graph) == opt.eventualSafeNodes(graph), graph
    n = 10_000
    chain = [[i + 1] for i in range(n - 1)] + [[]]
    assert opt.eventualSafeNodes(chain) == list(range(n))
    assert opt.eventualSafeNodes(chain[:-1] + [[0]]) == []
    big = [sorted(R.sample(range(n), 4)) for _ in range(n)]
    timed_call(lambda: opt.eventualSafeNodes(big), 1)


@case(827)
def _(h):
    brute, opt = both(h, 827)
    assert call(opt.largestIsland, [[1, 0], [0, 1]]) == 3
    assert call(opt.largestIsland, [[1, 1], [1, 0]]) == 4
    assert call(opt.largestIsland, [[1, 1], [1, 1]]) == 4
    for _ in range(300):
        n = R.randint(1, 6)
        grid = rand_grid(n, n, R.random())
        assert call(brute.largestIsland, grid) == call(opt.largestIsland, grid), grid
    assert call(opt.largestIsland, [[0] * 500 for _ in range(500)]) == 1
    assert call(opt.largestIsland, [[1] * 500 for _ in range(500)]) == 250_000
    timed_call(lambda: call(opt.largestIsland, rand_grid(500, 500, 0.55)), 5)


def board_from(cells, n):
    """Inverse of the notes' flattening: cells[s] (s = 1..n²) -> LeetCode's boustrophedon board."""
    rows = [cells[1 + i * n:1 + (i + 1) * n] for i in range(n)]
    return [row if i % 2 == 0 else row[::-1] for i, row in enumerate(rows)][::-1]


def random_board(n):
    last = n * n
    cells = [0] + [-1] * last
    density = R.random() * 0.5
    for s in range(2, last):
        if R.random() < density:
            cells[s] = R.choice([d for d in range(1, last + 1) if d != s])
    return board_from(cells, n)


@case(909)
def _(h):
    brute, opt = both(h, 909)
    example = [[-1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1],
               [-1, 35, -1, -1, 13, -1], [-1, -1, -1, -1, -1, -1], [-1, 15, -1, -1, -1, -1]]
    assert opt.snakesAndLadders(example) == 4 == brute.snakesAndLadders(example)
    assert opt.snakesAndLadders([[-1, -1], [-1, 3]]) == 1
    walled = [0] + [-1] * 36
    for s in range(2, 8):
        walled[s] = 1  # six snakes in a row: no roll from square 1 gets past them
    assert opt.snakesAndLadders(board_from(walled, 6)) == -1 == brute.snakesAndLadders(board_from(walled, 6))
    for _ in range(300):
        board = random_board(R.randint(2, 5))
        assert brute.snakesAndLadders(board) == opt.snakesAndLadders(board), board
    big = random_board(20)
    timed_call(lambda: opt.snakesAndLadders(big), 1)


@case(947)
def _(h):
    brute, opt = both(h, 947)
    assert opt.removeStones([[0, 0], [0, 1], [1, 0], [1, 2], [2, 1], [2, 2]]) == 5
    assert opt.removeStones([[0, 0], [0, 2], [1, 1], [2, 0], [2, 2]]) == 3
    assert opt.removeStones([[0, 0]]) == 0
    assert opt.removeStones([[0, 1], [1, 0]]) == 0  # row 0 and column 0 are different lines
    for _ in range(300):
        side = R.randint(1, 6)
        cells = [[r, c] for r in range(side) for c in range(side)]
        stones = R.sample(cells, R.randint(1, min(len(cells), 12)))
        assert brute.removeStones(stones) == opt.removeStones(stones), stones
    stones = [list(p) for p in {(R.randint(0, 10**4), R.randint(0, 10**4)) for _ in range(1000)}]
    assert brute.removeStones(stones) == opt.removeStones(stones)
    timed_call(lambda: opt.removeStones(stones), 1)


@case(1020)
def _(h):
    brute, opt = both(h, 1020)
    assert call(opt.numEnclaves, [[0, 0, 0, 0], [1, 0, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]]) == 3
    assert call(opt.numEnclaves, [[0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 0, 0]]) == 0
    for _ in range(300):
        grid = rand_grid(R.randint(1, 8), R.randint(1, 8), R.random())
        assert call(brute.numEnclaves, grid) == call(opt.numEnclaves, grid), grid
    inner = snake_grid(498)
    walled = [[0] * 500] + [[0] + row + [0] for row in inner] + [[0] * 500]
    assert call(opt.numEnclaves, walled) == sum(map(sum, inner))
    walled[1][0] = 1  # one land cell on the edge now drains the whole snake
    assert call(opt.numEnclaves, walled) == 0
    timed_call(lambda: call(opt.numEnclaves, rand_grid(500, 500, 0.6)), 3)


def random_roads(n, max_time):
    """Connected graph on 0..n-1, at most one road per pair."""
    labels = list(range(n))
    R.shuffle(labels)
    pairs = {tuple(sorted((labels[R.randrange(i)], labels[i]))) for i in range(1, n)}
    for _ in range(R.randint(0, n * (n - 1) // 2)):
        pairs.add(tuple(sorted(R.sample(range(n), 2))))
    return [[a, b, R.randint(1, max_time)] for a, b in pairs]


@case(1976)
def _(h):
    brute, opt = both(h, 1976)
    roads = [[0, 6, 7], [0, 1, 2], [1, 2, 3], [1, 3, 3], [6, 3, 3], [3, 5, 1], [6, 5, 1], [2, 5, 1], [0, 4, 5], [4, 6, 2]]
    assert opt.countPaths(7, roads) == 4 == brute.countPaths(7, roads)
    assert opt.countPaths(2, [[1, 0, 10]]) == 1
    assert opt.countPaths(1, []) == 1
    for _ in range(300):
        n = R.randint(1, 7)
        roads = random_roads(n, R.choice((2, 3, 10**9)))
        assert brute.countPaths(n, roads) == opt.countPaths(n, roads), (n, roads)
    n, layers = 200, 99
    ladder = [[0, 1, 1], [0, 2, 1], [197, 199, 1], [198, 199, 1]]
    for k in range(layers - 1):
        ladder += [[a, b, 1] for a in (1 + 2 * k, 2 + 2 * k) for b in (3 + 2 * k, 4 + 2 * k)]
    assert opt.countPaths(n, ladder) == pow(2, layers, MOD)
    dense = [[a, b, R.randint(1, 3)] for a in range(n) for b in range(a + 1, n)]
    timed_call(lambda: opt.countPaths(n, dense), 2)
