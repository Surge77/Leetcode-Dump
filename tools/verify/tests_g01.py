"""Gap notes g01: arrays, BST, bits, DP, design classes, graph traversals, greedy.

Each note has a brute force and an optimized block; both must agree on random inputs and on
LeetCode's examples, and the optimized one is run once at max constraints where it matters.
"""
import random
from itertools import product

from harness import case
from tests_b10 import timed_call

R = random.Random(101)


def both(h, num, name="Solution"):
    brute, opt = h.lc_all(num, name)
    return brute[name](), opt[name]()


def random_tree(n):
    labels = list(range(n))
    R.shuffle(labels)
    return [[labels[R.randrange(i)], labels[i]] for i in range(1, n)]


@case(41)
def _(h):
    brute, opt = both(h, 41)
    assert opt.firstMissingPositive([1, 2, 0]) == 3
    assert opt.firstMissingPositive([3, 4, -1, 1]) == 2
    assert opt.firstMissingPositive([7, 8, 9, 11, 12]) == 1
    assert opt.firstMissingPositive([1, 1]) == 2
    for _ in range(300):
        nums = [R.randint(-3, 9) for _ in range(R.randint(1, 9))]
        assert brute.firstMissingPositive(nums[:]) == opt.firstMissingPositive(nums[:]), nums
    big = list(range(1, 100_001))
    R.shuffle(big)
    assert opt.firstMissingPositive(big) == 100_001
    timed_call(lambda: opt.firstMissingPositive([R.randint(-5, 10**5) for _ in range(10**5)]), 2)


@case(1431)
def _(h):
    brute, opt = both(h, 1431)
    assert opt.kidsWithCandies([2, 3, 5, 1, 3], 3) == [True, True, True, False, True]
    assert opt.kidsWithCandies([4, 2, 1, 1, 2], 1) == [True, False, False, False, False]
    assert opt.kidsWithCandies([12, 1, 12], 10) == [True, False, True]
    for _ in range(200):
        candies = [R.randint(1, 10) for _ in range(R.randint(1, 8))]
        extra = R.randint(1, 10)
        assert brute.kidsWithCandies(candies, extra) == opt.kidsWithCandies(candies, extra), (candies, extra)
    timed_call(lambda: opt.kidsWithCandies([R.randint(1, 100) for _ in range(100)], 50), 1)


@case(285)
def _(h):
    brute, opt = both(h, 285)
    root = h.build_tree([2, 1, 3])
    assert opt.inorderSuccessor(root, h.find_node(root, 1)).val == 2
    root = h.build_tree([5, 3, 6, 2, 4, None, None, 1])
    assert opt.inorderSuccessor(root, h.find_node(root, 6)) is None
    for _ in range(150):
        values = R.sample(range(1, 40), R.randint(1, 12))
        root = h.TreeNode(values[0])
        nodes = [root]
        for v in values[1:]:
            cur = root
            while True:
                side = "left" if v < cur.val else "right"
                nxt = getattr(cur, side)
                if nxt is None:
                    node = h.TreeNode(v)
                    setattr(cur, side, node)
                    nodes.append(node)
                    break
                cur = nxt
        p = R.choice(nodes)
        assert brute.inorderSuccessor(root, p) is opt.inorderSuccessor(root, p), values
    root = h.TreeNode(1)
    cur = root
    for v in range(2, 10_001):
        cur.right = h.TreeNode(v)
        cur = cur.right
    assert opt.inorderSuccessor(root, h.find_node(root, 5000)).val == 5001
    timed_call(lambda: opt.inorderSuccessor(root, cur), 1)


@case(1318)
def _(h):
    brute, opt = both(h, 1318)
    assert opt.minFlips(2, 6, 5) == 3 and opt.minFlips(4, 2, 7) == 1 and opt.minFlips(1, 2, 3) == 0
    for _ in range(400):
        limit = R.choice((8, 1000, 10**9))
        a, b, c = (R.randint(1, limit) for _ in range(3))
        assert brute.minFlips(a, b, c) == opt.minFlips(a, b, c), (a, b, c)
    assert opt.minFlips(10**9, 10**9, 1) == brute.minFlips(10**9, 10**9, 1)


@case(790)
def _(h):
    brute, opt = both(h, 790)
    assert opt.numTilings(3) == 5 and opt.numTilings(1) == 1
    for n in range(1, 11):
        assert brute.numTilings(n) == opt.numTilings(n), n
    mod = 10**9 + 7
    f = [1, 1, 2]
    for n in range(3, 1001):
        f.append((f[-1] + f[-2] + 2 * sum(f[:n - 2])) % mod)  # the un-collapsed recurrence
    for n in (4, 5, 30, 500, 1000):
        assert opt.numTilings(n) == f[n], n
    timed_call(lambda: opt.numTilings(1000), 1)


@case(1137)
def _(h):
    brute, opt = both(h, 1137)
    assert opt.tribonacci(4) == 4 and opt.tribonacci(25) == 1389537
    assert opt.tribonacci(0) == 0 and opt.tribonacci(1) == 1 and opt.tribonacci(2) == 1
    assert opt.tribonacci(37) == 2082876103
    for n in range(0, 21):
        assert brute.tribonacci(n) == opt.tribonacci(n), n


@case(377)
def _(h):
    brute, opt = both(h, 377)
    assert opt.combinationSum4([1, 2, 3], 4) == 7 and opt.combinationSum4([9], 3) == 0
    for _ in range(150):
        nums = R.sample(range(1, 8), R.randint(1, 4))
        target = R.randint(1, 12)
        assert brute.combinationSum4(nums, target) == opt.combinationSum4(nums, target), (nums, target)
    timed_call(lambda: opt.combinationSum4(list(range(1, 201)), 1000), 5)


@case(933)
def _(h):
    brute, opt = both(h, 933, "RecentCounter")
    assert [opt.ping(t) for t in (1, 100, 3001, 3002)] == [1, 2, 3, 3]
    for _ in range(100):
        a, b = brute.__class__(), opt.__class__()
        t = 0
        for _ in range(R.randint(1, 30)):
            t += R.randint(1, 1500)
            assert a.ping(t) == b.ping(t), t
    fast = opt.__class__()
    timed_call(lambda: [fast.ping(t) for t in range(1, 10_001)], 2)


@case(362)
def _(h):
    brute, opt = both(h, 362, "HitCounter")
    c = opt.__class__()
    for t in (1, 2, 3):
        c.hit(t)
    assert c.getHits(4) == 3
    c.hit(300)
    assert c.getHits(300) == 4 and c.getHits(301) == 3
    for _ in range(100):
        a, b = brute.__class__(), opt.__class__()
        t = 1
        for _ in range(R.randint(1, 40)):
            t += R.randint(0, 120)
            if R.random() < 0.6:
                a.hit(t)
                b.hit(t)
            else:
                assert a.getHits(t) == b.getHits(t), t
    fast = opt.__class__()

    def run():
        for i in range(100_000):
            fast.hit(1 + i // 50)
        fast.getHits(2000)

    timed_call(run, 3)


@case(588)
def _(h):
    brute, opt = h.lc_all(588, "FileSystem")
    fs = opt["FileSystem"]()
    assert fs.ls("/") == []
    fs.mkdir("/a/b/c")
    fs.addContentToFile("/a/b/c/d", "hello")
    assert fs.ls("/") == ["a"] and fs.readContentFromFile("/a/b/c/d") == "hello"
    assert fs.ls("/a/b/c/d") == ["d"] and fs.ls("/a/b/c") == ["d"]
    for _ in range(100):
        a, b = brute["FileSystem"](), opt["FileSystem"]()
        dirs, files = ["/"], []
        for _ in range(R.randint(1, 40)):
            op = R.choice("mafrl")
            name = R.choice("abcd")
            if op == "m":
                parent = R.choice(dirs)
                path = (parent.rstrip("/") + "/" + name)
                if path in files:
                    continue
                a.mkdir(path)
                b.mkdir(path)
                for i in range(1, path.count("/") + 1):
                    sub = "/" + "/".join(path.split("/")[1:i + 1])
                    if sub not in dirs:
                        dirs.append(sub)
            elif op == "a":
                path = R.choice(dirs).rstrip("/") + "/" + name
                if path in dirs:
                    continue
                text = R.choice(["x", "yz", "w"])
                a.addContentToFile(path, text)
                b.addContentToFile(path, text)
                if path not in files:
                    files.append(path)
            elif op == "r" and files:
                path = R.choice(files)
                assert a.readContentFromFile(path) == b.readContentFromFile(path), path
            elif op == "l":
                path = R.choice(dirs + files)
                assert a.ls(path) == b.ls(path), path
    big = opt["FileSystem"]()
    timed_call(lambda: [big.addContentToFile(f"/d{i % 50}/f{i}", "x") for i in range(5000)] and big.ls("/d1"), 3)


@case(895)
def _(h):
    brute, opt = both(h, 895, "FreqStack")
    for v in (5, 7, 5, 7, 4, 5):
        opt.push(v)
    assert [opt.pop() for _ in range(4)] == [5, 7, 5, 4]
    for _ in range(150):
        a, b = brute.__class__(), opt.__class__()
        size = 0
        for _ in range(R.randint(1, 40)):
            if size and R.random() < 0.4:
                assert a.pop() == b.pop()
                size -= 1
            else:
                v = R.randint(0, 5)
                a.push(v)
                b.push(v)
                size += 1
    fast = opt.__class__()

    def run():
        for i in range(10_000):
            fast.push(R.randint(0, 100))
        for _ in range(10_000):
            fast.pop()

    timed_call(run, 2)


@case(310)
def _(h):
    brute, opt = both(h, 310)
    assert sorted(opt.findMinHeightTrees(4, [[1, 0], [1, 2], [1, 3]])) == [1]
    assert sorted(opt.findMinHeightTrees(6, [[3, 0], [3, 1], [3, 2], [3, 4], [5, 4]])) == [3, 4]
    assert opt.findMinHeightTrees(1, []) == [0]
    for _ in range(200):
        n = R.randint(1, 14)
        edges = random_tree(n)
        assert sorted(brute.findMinHeightTrees(n, edges)) == sorted(opt.findMinHeightTrees(n, edges)), edges
    n = 20_000
    assert sorted(opt.findMinHeightTrees(n, [[i, i + 1] for i in range(n - 1)])) == [n // 2 - 1, n // 2]
    timed_call(lambda: opt.findMinHeightTrees(n, random_tree(n)), 3)


@case(815)
def _(h):
    brute, opt = both(h, 815)
    assert opt.numBusesToDestination([[1, 2, 7], [3, 6, 7]], 1, 6) == 2
    assert opt.numBusesToDestination([[7, 12], [4, 5, 15], [6], [15, 19], [9, 12, 13]], 15, 12) == -1
    assert opt.numBusesToDestination([[1, 2]], 1, 1) == 0
    for _ in range(200):
        routes = [R.sample(range(10), R.randint(1, 4)) for _ in range(R.randint(1, 6))]
        s, t = R.randrange(10), R.randrange(10)
        assert brute.numBusesToDestination(routes, s, t) == opt.numBusesToDestination(routes, s, t), (routes, s, t)
    routes = [R.sample(range(10**6), 200) for _ in range(500)]
    timed_call(lambda: opt.numBusesToDestination(routes, routes[0][0], routes[-1][-1]), 3)


@case(841)
def _(h):
    brute, opt = both(h, 841)
    assert opt.canVisitAllRooms([[1], [2], [3], []]) is True
    assert opt.canVisitAllRooms([[1, 3], [3, 0, 1], [2], [0]]) is False
    for _ in range(300):
        n = R.randint(1, 8)
        rooms = [[R.randrange(n) for _ in range(R.randint(0, 3))] for _ in range(n)]
        assert brute.canVisitAllRooms(rooms) == opt.canVisitAllRooms(rooms), rooms
    n = 1000
    chain = [[i + 1] for i in range(n - 1)] + [[]]
    assert opt.canVisitAllRooms(chain) is True
    timed_call(lambda: opt.canVisitAllRooms(chain), 1)


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


def random_grid(symbols):
    rows, cols = R.randint(1, 6), R.randint(1, 6)
    return [[R.choice(symbols) for _ in range(cols)] for _ in range(rows)]


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
