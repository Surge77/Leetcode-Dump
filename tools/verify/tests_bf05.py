"""Brute-force backfill bf05: knapsack, LIS, matrix-exponentiation and tree DP notes.

Each test checks the new brute-force block (first python block) on LeetCode's examples,
then compares it to the optimized block (last python block) on small random inputs.
"""
import random

from harness import TreeNode, blocks_of, build_tree, case, lc_path, ns_from

R = random.Random(505)


def pair(num):
    blocks = blocks_of(lc_path(num))
    return ns_from(blocks[0])["Solution"](), ns_from(blocks[-1])["Solution"]()


def random_tree(n):
    nodes = [TreeNode(R.randint(0, 20)) for _ in range(n)]
    for i in range(1, n):
        while True:
            p = nodes[R.randrange(i)]
            side = R.choice(("left", "right"))
            if getattr(p, side) is None:
                setattr(p, side, nodes[i])
                break
    return nodes[0]


@case("322-brute")
def _(h):
    brute, opt = pair(322)
    assert brute.coinChange([1, 2, 5], 11) == 3
    assert brute.coinChange([2], 3) == -1
    assert brute.coinChange([1], 0) == 0
    for _ in range(200):
        coins = list({R.randint(1, 9) for _ in range(R.randint(1, 3))})
        amt = R.randint(0, 18)
        assert brute.coinChange(coins, amt) == opt.coinChange(coins, amt), (coins, amt)


@case("416-brute")
def _(h):
    brute, opt = pair(416)
    assert brute.canPartition([1, 5, 11, 5]) is True
    assert brute.canPartition([1, 2, 3, 5]) is False
    for _ in range(200):
        a = [R.randint(1, 15) for _ in range(R.randint(1, 10))]
        assert brute.canPartition(a) == opt.canPartition(a), a


@case("494-brute")
def _(h):
    brute, opt = pair(494)
    assert brute.findTargetSumWays([1, 1, 1, 1, 1], 3) == 5
    assert brute.findTargetSumWays([1], 1) == 1
    for _ in range(200):
        a = [R.randint(0, 6) for _ in range(R.randint(1, 10))]
        t = R.randint(-12, 12)
        assert brute.findTargetSumWays(a, t) == opt.findTargetSumWays(a, t), (a, t)


@case("518-brute")
def _(h):
    brute, opt = pair(518)
    assert brute.change(5, [1, 2, 5]) == 4
    assert brute.change(3, [2]) == 0
    assert brute.change(10, [10]) == 1
    for _ in range(200):
        coins = list({R.randint(1, 8) for _ in range(R.randint(1, 4))})
        amt = R.randint(0, 25)
        assert brute.change(amt, coins) == opt.change(amt, coins), (coins, amt)


@case("300-brute")
def _(h):
    brute, opt = pair(300)
    assert brute.lengthOfLIS([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert brute.lengthOfLIS([0, 1, 0, 3, 2, 3]) == 4
    assert brute.lengthOfLIS([7, 7, 7, 7, 7, 7, 7]) == 1
    for _ in range(200):
        a = [R.randint(-5, 10) for _ in range(R.randint(1, 12))]
        assert brute.lengthOfLIS(a) == opt.lengthOfLIS(a), a


@case("354-brute")
def _(h):
    brute, opt = pair(354)
    assert brute.maxEnvelopes([[5, 4], [6, 4], [6, 7], [2, 3]]) == 3
    assert brute.maxEnvelopes([[1, 1], [1, 1], [1, 1]]) == 1
    for _ in range(200):
        env = [[R.randint(1, 6), R.randint(1, 6)] for _ in range(R.randint(1, 10))]
        want = opt.maxEnvelopes([e[:] for e in env])
        assert brute.maxEnvelopes([e[:] for e in env]) == want, env


@case("1220-brute")
def _(h):
    brute, opt = pair(1220)
    assert brute.countVowelPermutation(1) == 5
    assert brute.countVowelPermutation(2) == 10
    assert brute.countVowelPermutation(5) == 68
    for _ in range(100):
        n = R.randint(1, 6)
        assert brute.countVowelPermutation(n) == opt.countVowelPermutation(n), n


@case("935-brute")
def _(h):
    brute, opt = pair(935)
    assert brute.knightDialer(1) == 10
    assert brute.knightDialer(2) == 20
    for _ in range(100):
        n = R.randint(1, 12)
        assert brute.knightDialer(n) == opt.knightDialer(n), n


@case("337-brute")
def _(h):
    brute, opt = pair(337)
    assert brute.rob(build_tree([3, 2, 3, None, 3, None, 1])) == 7
    assert brute.rob(build_tree([3, 4, 5, 1, 3, None, 1])) == 9
    assert brute.rob(None) == 0
    for _ in range(150):
        root = random_tree(R.randint(1, 11))
        assert brute.rob(root) == opt.rob(root)


@case("968-brute")
def _(h):
    brute, opt = pair(968)
    assert brute.minCameraCover(build_tree([0, 0, None, 0, 0])) == 1
    assert brute.minCameraCover(build_tree([0, 0, None, 0, None, 0, None, None, 0])) == 2
    for _ in range(150):
        root = random_tree(R.randint(1, 11))
        assert brute.minCameraCover(root) == opt.minCameraCover(root)
