"""Gap notes g01: arrays, BST, bits, DP, design classes, graph traversals, greedy (part 2 of 2).

Shared helpers: helpers_g01.py.
"""
from helpers_g01 import (  # noqa: F401
    R,
    both,
    case,
    product,
    random_grid,
    random_tree,
    timed_call,
)


@case(1197)
def _(h):
    brute, opt = both(h, 1197)
    assert opt.minKnightMoves(2, 1) == 1 and opt.minKnightMoves(5, 5) == 4
    assert opt.minKnightMoves(0, 0) == 0 and opt.minKnightMoves(1, 0) == 3
    for x, y in product(range(-12, 13), repeat=2):
        assert brute.minKnightMoves(x, y) == opt.minKnightMoves(x, y), (x, y)
    for _ in range(40):
        x, y = R.randint(-40, 40), R.randint(-40, 40)
        assert brute.minKnightMoves(x, y) == opt.minKnightMoves(x, y), (x, y)
    timed_call(lambda: opt.minKnightMoves(300, 300), 5)
    timed_call(lambda: opt.minKnightMoves(-300, 1), 5)


@case(1466)
def _(h):
    brute, opt = both(h, 1466)
    assert opt.minReorder(6, [[0, 1], [1, 3], [2, 3], [4, 0], [4, 5]]) == 3
    assert opt.minReorder(5, [[1, 0], [1, 2], [3, 2], [4, 3]]) == brute.minReorder(5, [[1, 0], [1, 2], [3, 2], [4, 3]]) == 1
    assert opt.minReorder(3, [[1, 0], [2, 0]]) == 0
    for _ in range(150):
        n = R.randint(2, 12)
        roads = [e[::R.choice((1, -1))] for e in random_tree(n)]
        assert brute.minReorder(n, roads) == opt.minReorder(n, roads), roads
    n = 50_000
    assert opt.minReorder(n, [[i, i + 1] for i in range(n - 1)]) == n - 1
    timed_call(lambda: opt.minReorder(n, [e[::R.choice((1, -1))] for e in random_tree(n)]), 3)


@case(1730)
def _(h):
    brute, opt = both(h, 1730)
    x = "X"
    assert opt.getFood([[x] * 6, [x, "*", "O", "O", "O", x], [x, "O", "O", "#", "O", x], [x] * 6]) == 3
    assert opt.getFood([[x] * 5, [x, "*", x, "O", x], [x, "O", x, "#", x], [x] * 5]) == -1
    big_example = [[x] * 8, [x, "*", "O", x, "O", "#", "O", x], [x, "O", "O", x, "O", "O", x, x],
                   [x, "O", "O", "O", "O", "#", "O", x], [x] * 8]
    assert brute.getFood(big_example) == opt.getFood(big_example) == 6
    for _ in range(300):
        grid = random_grid("OOOX#")
        r, c = R.randrange(len(grid)), R.randrange(len(grid[0]))
        grid[r][c] = "*"
        assert brute.getFood(grid) == opt.getFood(grid), grid
    n = 200
    grid = [["O"] * n for _ in range(n)]
    grid[0][0], grid[n - 1][n - 1] = "*", "#"
    assert opt.getFood(grid) == 2 * (n - 1)
    timed_call(lambda: opt.getFood(grid), 3)


@case(1926)
def _(h):
    brute, opt = both(h, 1926)
    maze = [["+", "+", ".", "+"], [".", ".", ".", "+"], ["+", "+", "+", "."]]
    assert opt.nearestExit(maze, [1, 2]) == 1
    assert opt.nearestExit([["+", "+", "+"], [".", ".", "."], ["+", "+", "+"]], [1, 0]) == 2
    assert opt.nearestExit([[".", "+"]], [0, 0]) == -1
    for _ in range(300):
        maze = random_grid("..+")
        cells = [(r, c) for r in range(len(maze)) for c in range(len(maze[0])) if maze[r][c] == "."]
        if not cells:
            continue
        entrance = list(R.choice(cells))
        copy = [row[:] for row in maze]
        assert brute.nearestExit(maze, entrance) == opt.nearestExit(copy, entrance), (maze, entrance)
    n = 200
    big = [["."] * n for _ in range(n)]
    for r in range(1, n - 1):
        for c in range(1, n - 1):
            big[r][c] = "." if R.random() < 0.9 else "+"
    big[100][100] = "."
    timed_call(lambda: opt.nearestExit(big, [100, 100]), 3)


@case(179)
def _(h):
    brute, opt = both(h, 179)
    assert opt.largestNumber([10, 2]) == "210" and opt.largestNumber([3, 30, 34, 5, 9]) == "9534330"
    assert opt.largestNumber([0, 0]) == "0" and opt.largestNumber([1]) == "1"
    pool = [0, 1, 3, 10, 30, 34, 5, 9, 100, 12, 121, 111]
    for _ in range(150):
        nums = [R.choice(pool) for _ in range(R.randint(1, 6))]
        assert brute.largestNumber(nums) == opt.largestNumber(nums), nums
    big = [R.randint(0, 10**9) for _ in range(100)]
    assert len(opt.largestNumber(big)) == sum(len(str(v)) for v in big)
    timed_call(lambda: opt.largestNumber(big), 1)


@case(334)
def _(h):
    brute, opt = both(h, 334)
    assert opt.increasingTriplet([1, 2, 3, 4, 5]) is True
    assert opt.increasingTriplet([5, 4, 3, 2, 1]) is False
    assert opt.increasingTriplet([2, 1, 5, 0, 4, 6]) is True
    for _ in range(400):
        nums = [R.randint(-4, 6) for _ in range(R.randint(1, 9))]
        assert brute.increasingTriplet(nums) == opt.increasingTriplet(nums), nums
    n = 500_000
    assert opt.increasingTriplet(list(range(n, 0, -1))) is False
    timed_call(lambda: opt.increasingTriplet([R.randint(1, 10**9) for _ in range(n)]), 2)


@case(605)
def _(h):
    brute, opt = both(h, 605)
    assert opt.canPlaceFlowers([1, 0, 0, 0, 1], 1) is True
    assert opt.canPlaceFlowers([1, 0, 0, 0, 1], 2) is False
    for _ in range(400):
        bed = [0] * R.randint(1, 12)
        for i in range(len(bed)):
            if R.random() < 0.3 and (i == 0 or bed[i - 1] == 0):
                bed[i] = 1
        n = R.randint(0, 5)
        copy = bed[:]
        assert brute.canPlaceFlowers(bed, n) == opt.canPlaceFlowers(copy, n), (bed, n)
    assert opt.canPlaceFlowers([0] * 20_000, 10_000) is True
    timed_call(lambda: opt.canPlaceFlowers([0] * 20_000, 10_001), 1)


@case(649)
def _(h):
    brute, opt = both(h, 649)
    assert opt.predictPartyVictory("RD") == "Radiant" and opt.predictPartyVictory("RDD") == "Dire"
    for _ in range(400):
        senate = "".join(R.choice("RD") for _ in range(R.randint(1, 12)))
        assert brute.predictPartyVictory(senate) == opt.predictPartyVictory(senate), senate
    timed_call(lambda: opt.predictPartyVictory("".join(R.choice("RD") for _ in range(10_000))), 1)
