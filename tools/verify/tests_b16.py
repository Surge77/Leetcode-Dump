"""Hard-slot gap notes: nCr mod p, rerooting, difference arrays, sweep line, meet in the middle, binary lifting.

Each note has a brute force and an optimized block; both must agree on random inputs and on
LeetCode's examples, and the optimized one is run once at max constraints.
"""
import random

from harness import case
from tests_b10 import timed_call

R = random.Random(16)


def both(h, num):
    brute, opt = h.lc_all(num, "Solution")
    return brute["Solution"](), opt["Solution"]()


def random_tree(n):
    """Edges of a random tree on 0..n-1 with shuffled labels."""
    labels = list(range(n))
    R.shuffle(labels)
    return [[labels[R.randrange(i)], labels[i]] for i in range(1, n)]


@case(2400)
def _(h):
    brute, opt = both(h, 2400)
    assert opt.numberOfWays(1, 2, 3) == 3 and opt.numberOfWays(2, 5, 10) == 0
    for _ in range(300):
        s, e, k = R.randint(1, 20), R.randint(1, 20), R.randint(1, 25)
        assert brute.numberOfWays(s, e, k) == opt.numberOfWays(s, e, k), (s, e, k)
    timed_call(lambda: opt.numberOfWays(1, 1000, 1000), 2)


@case(1569)
def _(h):
    brute, opt = both(h, 1569)
    assert opt.numOfWays([2, 1, 3]) == 1 and opt.numOfWays([3, 4, 5, 1, 2]) == 5 and opt.numOfWays([1, 2, 3]) == 0
    for _ in range(80):
        nums = list(range(1, R.randint(1, 7) + 1))
        R.shuffle(nums)
        assert brute.numOfWays(nums) == opt.numOfWays(nums), nums
    assert opt.numOfWays(list(range(1, 1001))) == 0  # a path: depth 1000, only one order
    big = list(range(1, 1001))
    R.shuffle(big)
    timed_call(lambda: opt.numOfWays(big), 5)


@case(834)
def _(h):
    brute, opt = both(h, 834)
    assert opt.sumOfDistancesInTree(6, [[0, 1], [0, 2], [2, 3], [2, 4], [2, 5]]) == [8, 12, 6, 10, 10, 10]
    assert opt.sumOfDistancesInTree(1, []) == [0]
    for _ in range(150):
        n = R.randint(1, 12)
        edges = random_tree(n)
        assert brute.sumOfDistancesInTree(n, edges) == opt.sumOfDistancesInTree(n, edges), edges
    n = 30_000
    path = [[i, i + 1] for i in range(n - 1)]
    assert opt.sumOfDistancesInTree(n, path)[0] == n * (n - 1) // 2
    timed_call(lambda: opt.sumOfDistancesInTree(n, random_tree(n)), 3)


@case(2581)
def _(h):
    brute, opt = both(h, 2581)
    assert opt.rootCount([[0, 1], [1, 2], [1, 3], [4, 2]], [[1, 3], [0, 1], [1, 0], [2, 4]], 3) == 3
    assert opt.rootCount([[0, 1], [1, 2], [2, 3], [3, 4]], [[1, 0], [3, 4], [2, 1], [3, 2]], 1) == 5
    for _ in range(200):
        n = R.randint(2, 10)
        edges = random_tree(n)
        guesses = [R.choice(edges)[::R.choice((1, -1))] for _ in range(R.randint(1, 8))]
        k = R.randint(0, len(guesses))
        assert brute.rootCount(edges, guesses, k) == opt.rootCount(edges, guesses, k), (edges, guesses, k)
    n = 100_000
    edges = [[i, i + 1] for i in range(n - 1)]
    timed_call(lambda: opt.rootCount(edges, [e[::-1] for e in edges[::2]], n // 4), 3)


@case(1094)
def _(h):
    brute, opt = both(h, 1094)
    assert opt.carPooling([[2, 1, 5], [3, 3, 7]], 4) is False
    assert opt.carPooling([[2, 1, 5], [3, 3, 7]], 5) is True
    for _ in range(300):
        trips = []
        for _ in range(R.randint(1, 6)):
            start = R.randint(0, 15)
            trips.append([R.randint(1, 5), start, R.randint(start + 1, 20)])
        cap = R.randint(1, 15)
        assert brute.carPooling(trips, cap) == opt.carPooling(trips, cap), (trips, cap)


@case(2381)
def _(h):
    brute, opt = both(h, 2381)
    assert opt.shiftingLetters("abc", [[0, 1, 0], [1, 2, 1], [0, 2, 1]]) == "ace"
    assert opt.shiftingLetters("dztz", [[0, 0, 0], [1, 1, 1]]) == "catz"
    for _ in range(300):
        s = "".join(R.choice("abyz") for _ in range(R.randint(1, 10)))
        shifts = []
        for _ in range(R.randint(1, 8)):
            lo = R.randrange(len(s))
            shifts.append([lo, R.randint(lo, len(s) - 1), R.randint(0, 1)])
        assert brute.shiftingLetters(s, shifts) == opt.shiftingLetters(s, shifts), (s, shifts)
    n = 50_000
    big = [[R.randrange(n // 2), R.randrange(n // 2, n), R.randint(0, 1)] for _ in range(n)]
    timed_call(lambda: opt.shiftingLetters("a" * n, big), 2)


@case(2251)
def _(h):
    brute, opt = both(h, 2251)
    assert opt.fullBloomFlowers([[1, 6], [3, 7], [9, 12], [4, 13]], [2, 3, 7, 11]) == [1, 2, 2, 2]
    assert opt.fullBloomFlowers([[1, 10], [3, 3]], [3, 3, 2]) == [2, 2, 1]
    for _ in range(300):
        flowers = []
        for _ in range(R.randint(1, 8)):
            lo = R.randint(1, 12)
            flowers.append([lo, R.randint(lo, 14)])
        people = [R.randint(1, 15) for _ in range(R.randint(1, 8))]
        assert brute.fullBloomFlowers(flowers, people) == opt.fullBloomFlowers(flowers, people), (flowers, people)
    n = 50_000
    flowers = [sorted((R.randint(1, 10**9), R.randint(1, 10**9))) for _ in range(n)]
    timed_call(lambda: opt.fullBloomFlowers(flowers, [R.randint(1, 10**9) for _ in range(n)]), 2)


@case(1755)
def _(h):
    brute, opt = both(h, 1755)
    assert opt.minAbsDifference([5, -7, 3, 5], 6) == 0
    assert opt.minAbsDifference([7, -9, 15, -2], -5) == 1
    assert opt.minAbsDifference([1, 2, 3], -7) == 7
    for _ in range(300):
        nums = [R.randint(-30, 30) for _ in range(R.randint(1, 12))]
        goal = R.randint(-150, 150)
        assert brute.minAbsDifference(nums, goal) == opt.minAbsDifference(nums, goal), (nums, goal)
    big = [R.randint(-10**7, 10**7) for _ in range(40)]
    timed_call(lambda: opt.minAbsDifference(big, R.randint(-10**9, 10**9)), 10)


@case(2035)
def _(h):
    brute, opt = both(h, 2035)
    assert opt.minimumDifference([3, 9, 7, 3]) == 2
    assert opt.minimumDifference([-36, 36]) == 72
    assert opt.minimumDifference([2, -1, 0, 4, -2, -9]) == 0
    for _ in range(300):
        nums = [R.randint(-20, 20) for _ in range(2 * R.randint(1, 5))]
        assert brute.minimumDifference(nums) == opt.minimumDifference(nums), nums
    big = [R.randint(-10**7, 10**7) for _ in range(30)]
    timed_call(lambda: opt.minimumDifference(big), 10)


@case(2836)
def _(h):
    brute, opt = both(h, 2836)
    assert opt.getMaxFunctionValue([2, 0, 1], 4) == 6
    assert opt.getMaxFunctionValue([1, 1, 1, 2, 3], 3) == 10
    for _ in range(300):
        n = R.randint(1, 8)
        receiver = [R.randrange(n) for _ in range(n)]
        k = R.randint(1, 40)
        assert brute.getMaxFunctionValue(receiver, k) == opt.getMaxFunctionValue(receiver, k), (receiver, k)
    n = 100_000
    timed_call(lambda: opt.getMaxFunctionValue([R.randrange(n) for _ in range(n)], 10**10), 10)


@case(2846)
def _(h):
    brute, opt = both(h, 2846)
    edges = [[0, 1, 1], [1, 2, 1], [2, 3, 1], [3, 4, 2], [4, 5, 2], [5, 6, 2]]
    assert opt.minOperationsQueries(7, edges, [[0, 3], [3, 6], [2, 6], [0, 6]]) == [0, 0, 1, 3]
    assert opt.minOperationsQueries(1, [], [[0, 0]]) == [0]
    for _ in range(200):
        n = R.randint(1, 12)
        tree = [e + [R.randint(1, 3)] for e in random_tree(n)]
        queries = [[R.randrange(n), R.randrange(n)] for _ in range(R.randint(1, 8))]
        assert brute.minOperationsQueries(n, tree, queries) == opt.minOperationsQueries(n, tree, queries), (tree, queries)
    n, q = 10_000, 20_000
    tree = [e + [R.randint(1, 26)] for e in random_tree(n)]
    queries = [[R.randrange(n), R.randrange(n)] for _ in range(q)]
    timed_call(lambda: opt.minOperationsQueries(n, tree, queries), 5)
