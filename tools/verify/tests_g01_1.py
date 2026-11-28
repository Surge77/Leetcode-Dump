"""Gap notes g01: arrays, BST, bits, DP, design classes, graph traversals, greedy (part 1 of 2).

Shared helpers: helpers_g01.py.
"""
from helpers_g01 import (  # noqa: F401
    R,
    both,
    case,
    random_tree,
    timed_call,
)


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
