"""Gap notes g03: stack, heap/top-k, tree traversal, trie/palindromes, two pointers.

Each note has a brute force and an optimized block; both must agree on random inputs and on
LeetCode's examples, and the optimized one is run once at max constraints where it matters.
"""
import random

from harness import build_tree, case
from tests_b10 import timed_call

R = random.Random(303)


def both(h, num, name="Solution"):
    brute, opt = h.lc_all(num, name)
    return brute[name](), opt[name]()


def random_tree(h, n, lo=-5, hi=5):
    """Random binary tree with n nodes (iterative so it also works for big n)."""
    root = h.TreeNode(R.randint(lo, hi))
    free = [(root, "left"), (root, "right")]
    for _ in range(n - 1):
        pick = R.randrange(len(free))
        parent, side = free[pick]
        free[pick] = free[-1]
        free.pop()
        node = h.TreeNode(R.randint(lo, hi))
        setattr(parent, side, node)
        free += [(node, "left"), (node, "right")]
    return root


def chain(h, n, sides=None, val=1):
    """Path-shaped tree; sides[i] picks the child side of node i (default: always left)."""
    root = cur = h.TreeNode(val)
    for i in range(n - 1):
        node = h.TreeNode(val)
        setattr(cur, sides[i] if sides else "left", node)
        cur = node
    return root


@case(394)
def _(h):
    brute, opt = both(h, 394)
    assert opt.decodeString("3[a]2[bc]") == "aaabcbc"
    assert opt.decodeString("3[a2[c]]") == "accaccacc"
    assert opt.decodeString("2[abc]3[cd]ef") == "abcabccdcdcdef"
    assert opt.decodeString("abc") == "abc"

    def encoded(depth):
        enc, dec = "", ""
        for _ in range(R.randint(1, 3)):
            if depth and R.random() < 0.5:
                k = R.randint(1, 12)
                inner_enc, inner_dec = encoded(depth - 1)
                enc += f"{k}[{inner_enc}]"
                dec += inner_dec * k
            else:
                text = "".join(R.choice("abc") for _ in range(R.randint(1, 3)))
                enc, dec = enc + text, dec + text
        return enc, dec

    for _ in range(200):
        enc, dec = encoded(R.randint(0, 3))
        assert brute.decodeString(enc) == dec == opt.decodeString(enc), enc
    timed_call(lambda: opt.decodeString("46[" * 3 + "a" + "]" * 3), 2)


@case(2390)
def _(h):
    brute, opt = both(h, 2390)
    assert opt.removeStars("leet**cod*e") == "lecoe"
    assert opt.removeStars("erase*****") == ""
    for _ in range(200):
        letters, chars = 0, []
        for _ in range(R.randint(1, 20)):
            if letters and R.random() < 0.4:
                chars.append("*")
                letters -= 1
            else:
                chars.append(R.choice("abc"))
                letters += 1
        s = "".join(chars)
        assert brute.removeStars(s) == opt.removeStars(s), s
    n = 100_000
    timed_call(lambda: opt.removeStars("ab" * (n // 4) + "*" * (n // 2) + "c" * (n // 4)), 2)


@case(632)
def _(h):
    brute, opt = both(h, 632)
    nums = [[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]]
    assert opt.smallestRange(nums) == [20, 24] == brute.smallestRange(nums)
    assert opt.smallestRange([[1, 2, 3], [1, 2, 3], [1, 2, 3]]) == [1, 1]
    for _ in range(300):
        lists = [sorted(R.randint(-10, 10) for _ in range(R.randint(1, 5))) for _ in range(R.randint(1, 4))]
        assert brute.smallestRange(lists) == opt.smallestRange(lists), lists
    big = [sorted(R.randint(-10**5, 10**5) for _ in range(50)) for _ in range(3500)]
    timed_call(lambda: opt.smallestRange(big), 5)


@case(692)
def _(h):
    brute, opt = both(h, 692)
    words = ["i", "love", "leetcode", "i", "love", "coding"]
    assert opt.topKFrequent(words, 2) == ["i", "love"]
    words = ["the", "day", "is", "sunny", "the", "the", "the", "sunny", "is", "is"]
    assert opt.topKFrequent(words, 4) == ["the", "is", "sunny", "day"]
    for _ in range(300):
        words = [R.choice("abcdefg") * R.randint(1, 2) for _ in range(R.randint(1, 15))]
        k = R.randint(1, len(set(words)))
        assert brute.topKFrequent(words, k) == opt.topKFrequent(words, k), (words, k)
    big = ["".join(R.choice("abcdefghij") for _ in range(3)) for _ in range(500)]
    timed_call(lambda: opt.topKFrequent(big, len(set(big))), 1)


@case(2336)
def _(h):
    brute, opt = both(h, 2336, "SmallestInfiniteSet")
    steps = [("add", 2), ("pop",), ("pop",), ("pop",), ("add", 1), ("pop",), ("pop",), ("pop",)]
    out = []
    for step in steps:
        out.append(opt.addBack(step[1]) if step[0] == "add" else opt.popSmallest())
    assert out == [None, 1, 2, 3, None, 1, 4, 5]
    for _ in range(100):
        a, b = brute.__class__(), opt.__class__()
        for _ in range(R.randint(1, 60)):
            if R.random() < 0.55:
                assert a.popSmallest() == b.popSmallest()
            else:
                num = R.randint(1, 12)
                a.addBack(num)
                b.addBack(num)
        assert a.popSmallest() == b.popSmallest()
    big = opt.__class__()

    def run():
        for i in range(1000):
            big.popSmallest()
            big.addBack(R.randint(1, 1000))

    timed_call(run, 1)


@case(2462)
def _(h):
    brute, opt = both(h, 2462)
    assert opt.totalCost([17, 12, 10, 2, 7, 2, 11, 20, 8], 3, 4) == 11
    assert opt.totalCost([1, 2, 4, 1], 3, 3) == 4
    for _ in range(400):
        n = R.randint(1, 12)
        costs = [R.randint(1, 6) for _ in range(n)]
        k, c = R.randint(1, n), R.randint(1, n)
        assert brute.totalCost(costs, k, c) == opt.totalCost(costs, k, c), (costs, k, c)
    n = 100_000
    big = [R.randint(1, 10**5) for _ in range(n)]
    timed_call(lambda: opt.totalCost(big, n // 2, 1000), 2)


@case(2542)
def _(h):
    brute, opt = both(h, 2542)
    assert opt.maxScore([1, 3, 3, 2], [2, 1, 3, 4], 3) == 12
    assert opt.maxScore([4, 2, 3, 1, 1], [7, 5, 10, 9, 6], 1) == 30
    for _ in range(300):
        n = R.randint(1, 8)
        a = [R.randint(0, 10) for _ in range(n)]
        b = [R.randint(0, 10) for _ in range(n)]
        k = R.randint(1, n)
        assert brute.maxScore(a, b, k) == opt.maxScore(a, b, k), (a, b, k)
    n = 100_000
    a = [R.randint(0, 10**5) for _ in range(n)]
    b = [R.randint(0, 10**5) for _ in range(n)]
    timed_call(lambda: opt.maxScore(a, b, n // 2), 2)


@case(113)
def _(h):
    brute, opt = both(h, 113)
    tree = [5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1]
    expected = [[5, 4, 11, 2], [5, 8, 4, 5]]
    assert sorted(opt.pathSum(h.build_tree(tree), 22)) == expected
    assert opt.pathSum(h.build_tree([1, 2, 3]), 5) == []
    assert opt.pathSum(h.build_tree([1, 2]), 0) == []
    assert opt.pathSum(None, 0) == []
    for _ in range(300):
        root = random_tree(h, R.randint(1, 12), -3, 3)
        target = R.randint(-6, 6)
        assert sorted(brute.pathSum(root, target)) == sorted(opt.pathSum(root, target)), target
    assert opt.pathSum(chain(h, 5000), 5000) == [[1] * 5000]
    timed_call(lambda: opt.pathSum(random_tree(h, 5000, -3, 3), 2), 2)


@case(437)
def _(h):
    brute, opt = both(h, 437)
    assert opt.pathSum(h.build_tree([10, 5, -3, 3, 2, None, 11, 3, -2, None, 1]), 8) == 3
    assert opt.pathSum(h.build_tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1]), 22) == 3
    assert opt.pathSum(None, 0) == 0
    for _ in range(300):
        root = random_tree(h, R.randint(1, 14), -4, 4)
        target = R.randint(-8, 8)
        assert brute.pathSum(root, target) == opt.pathSum(root, target), target
    assert opt.pathSum(chain(h, 1000), 500) == 501
    timed_call(lambda: opt.pathSum(random_tree(h, 1000, -10**9, 10**9), 0), 2)


@case(872)
def _(h):
    brute, opt = both(h, 872)
    t1 = [3, 5, 1, 6, 2, 9, 8, None, None, 7, 4]
    t2 = [3, 5, 1, 6, 7, 4, 2, None, None, None, None, None, None, 9, 8]
    assert opt.leafSimilar(h.build_tree(t1), h.build_tree(t2)) is True
    assert opt.leafSimilar(h.build_tree([1, 2, 3]), h.build_tree([1, 3, 2])) is False
    trues = 0
    for _ in range(400):
        a, b = random_tree(h, R.randint(1, 7), 0, 1), random_tree(h, R.randint(1, 7), 0, 1)
        expected = brute.leafSimilar(a, b)
        assert expected == opt.leafSimilar(a, b)
        trues += expected
    assert trues > 10
    timed_call(lambda: opt.leafSimilar(random_tree(h, 200), random_tree(h, 200)), 1)


@case(1161)
def _(h):
    brute, opt = both(h, 1161)
    assert opt.maxLevelSum(h.build_tree([1, 7, 0, 7, -8, None, None])) == 2
    assert opt.maxLevelSum(h.build_tree([989, None, 10250, 98693, -89388, None, None, None, -32127])) == 2
    assert opt.maxLevelSum(h.build_tree([-5])) == 1
    for _ in range(300):
        root = random_tree(h, R.randint(1, 15), -4, 4)
        assert brute.maxLevelSum(root) == opt.maxLevelSum(root)
    timed_call(lambda: opt.maxLevelSum(chain(h, 10_000)), 1)
    timed_call(lambda: opt.maxLevelSum(random_tree(h, 10_000, -10**5, 10**5)), 1)


@case(1372)
def _(h):
    brute, opt = both(h, 1372)
    assert opt.longestZigZag(h.build_tree([1, None, 1, 1, 1, None, None, 1, 1, None, 1, None, None, None, 1])) == 3
    assert opt.longestZigZag(h.build_tree([1, 1, 1, None, 1, None, None, 1, 1, None, 1])) == 4
    assert opt.longestZigZag(h.build_tree([1])) == 0
    for _ in range(300):
        root = random_tree(h, R.randint(1, 15))
        assert brute.longestZigZag(root) == opt.longestZigZag(root)
    n = 50_000
    zigzag = chain(h, n, ["left" if i % 2 else "right" for i in range(n)])
    assert opt.longestZigZag(zigzag) == n - 1
    assert opt.longestZigZag(chain(h, n)) == 1
    timed_call(lambda: opt.longestZigZag(random_tree(h, n)), 2)


@case(336)
def _(h):
    brute, opt = both(h, 336)
    words = ["abcd", "dcba", "lls", "s", "sssll"]
    assert sorted(opt.palindromePairs(words)) == [[0, 1], [1, 0], [2, 4], [3, 2]]
    assert sorted(opt.palindromePairs(["bat", "tab", "cat"])) == [[0, 1], [1, 0]]
    assert sorted(opt.palindromePairs(["a", ""])) == [[0, 1], [1, 0]]
    for _ in range(300):
        pool = {"".join(R.choice("ab") for _ in range(R.randint(0, 4))) for _ in range(R.randint(1, 12))}
        words = list(pool)
        R.shuffle(words)
        got = opt.palindromePairs(words)
        assert len(got) == len({tuple(p) for p in got}), words
        assert sorted(got) == sorted(brute.palindromePairs(words)), words
    big = list({"".join(R.choice("ab") for _ in range(300)) for _ in range(5000)})
    timed_call(lambda: opt.palindromePairs(big), 30)


@case(1268)
def _(h):
    brute, opt = both(h, 1268)
    products = ["mobile", "mouse", "moneypad", "monitor", "mousepad"]
    near = ["mobile", "moneypad", "monitor"]
    assert opt.suggestedProducts(products, "mouse") == [near, near, ["mouse", "mousepad"], ["mouse", "mousepad"], ["mouse", "mousepad"]]
    assert opt.suggestedProducts(["havana"], "havana") == [["havana"]] * 6
    bags = ["bags", "baggage", "banner", "box", "cloths"]
    assert opt.suggestedProducts(bags, "bags") == [["baggage", "bags", "banner"]] * 2 + [["baggage", "bags"], ["bags"]]
    for _ in range(300):
        pool = list({"".join(R.choice("abc") for _ in range(R.randint(1, 4))) for _ in range(R.randint(1, 10))})
        before = list(pool)
        word = "".join(R.choice("abc") for _ in range(R.randint(1, 5)))
        assert brute.suggestedProducts(pool, word) == opt.suggestedProducts(pool, word), (pool, word)
        assert pool == before
    big = list({"".join(R.choice("abcdefgh") for _ in range(R.randint(1, 20))) for _ in range(1000)})
    timed_call(lambda: opt.suggestedProducts(big, "abcdefgh" * 100), 2)


@case(16)
def _(h):
    brute, opt = both(h, 16)
    assert opt.threeSumClosest([-1, 2, 1, -4], 1) == 2
    assert opt.threeSumClosest([0, 0, 0], 1) == 0
    for _ in range(400):
        nums = [R.randint(-10, 10) for _ in range(R.randint(3, 9))]
        target = R.randint(-35, 35)
        before = list(nums)
        got, want = opt.threeSumClosest(nums, target), brute.threeSumClosest(nums, target)
        assert abs(got - target) == abs(want - target), (nums, target)
        assert nums == before
    big = [R.randint(-1000, 1000) for _ in range(500)]
    timed_call(lambda: opt.threeSumClosest(big, 10_000), 2)


@case(345)
def _(h):
    brute, opt = both(h, 345)
    assert opt.reverseVowels("IceCreAm") == "AceCreIm"
    assert opt.reverseVowels("leetcode") == "leotcede"
    for _ in range(300):
        s = "".join(R.choice("aeiouAEIOUbcdxyz .") for _ in range(R.randint(1, 15)))
        assert brute.reverseVowels(s) == opt.reverseVowels(s), s
    timed_call(lambda: opt.reverseVowels("".join(R.choice("aeiouxyz") for _ in range(300_000))), 2)


@case(443)
def _(h):
    brute, opt = both(h, 443)

    def run(sol, chars):
        work = list(chars)
        length = sol.compress(work)
        return length, work[:length]

    assert run(opt, list("aabbccc")) == (6, list("a2b2c3"))
    assert run(opt, ["a"]) == (1, ["a"])
    assert run(opt, list("abbbbbbbbbbbb")) == (4, list("ab12"))
    for _ in range(300):
        chars = []
        for _ in range(R.randint(1, 5)):
            chars += [R.choice("abcX9")] * R.choice((1, 2, 3, 9, 10, 11, 100, 101))
        want = run(brute, chars)
        assert want == run(opt, chars), chars
    timed_call(lambda: run(opt, [R.choice("ab") for _ in range(2000)]), 1)


@case(844)
def _(h):
    brute, opt = both(h, 844)
    assert opt.backspaceCompare("ab#c", "ad#c") is True
    assert opt.backspaceCompare("ab##", "c#d#") is True
    assert opt.backspaceCompare("a#c", "b") is False
    for _ in range(500):
        s = "".join(R.choice("ab##") for _ in range(R.randint(1, 10)))
        t = "".join(R.choice("ab##") for _ in range(R.randint(1, 10)))
        assert brute.backspaceCompare(s, t) == opt.backspaceCompare(s, t), (s, t)
    timed_call(lambda: opt.backspaceCompare("a#" * 100, "b#" * 100), 1)


@case(977)
def _(h):
    brute, opt = both(h, 977)
    assert opt.sortedSquares([-4, -1, 0, 3, 10]) == [0, 1, 9, 16, 100]
    assert opt.sortedSquares([-7, -3, 2, 3, 11]) == [4, 9, 9, 49, 121]
    for _ in range(300):
        nums = sorted(R.randint(-10, 10) for _ in range(R.randint(1, 12)))
        assert brute.sortedSquares(nums) == opt.sortedSquares(nums), nums
    big = sorted(R.randint(-10**4, 10**4) for _ in range(10_000))
    timed_call(lambda: opt.sortedSquares(big), 1)


@case(1679)
def _(h):
    brute, opt = both(h, 1679)
    assert opt.maxOperations([1, 2, 3, 4], 5) == 2
    assert opt.maxOperations([3, 1, 3, 4, 3], 6) == 1
    for _ in range(400):
        nums = [R.randint(1, 8) for _ in range(R.randint(1, 14))]
        k = R.randint(2, 16)
        assert brute.maxOperations(nums, k) == opt.maxOperations(nums, k), (nums, k)
    big = [R.randint(1, 10**9) for _ in range(100_000)]
    timed_call(lambda: opt.maxOperations(big, 10**9), 1)


@case(1768)
def _(h):
    brute, opt = both(h, 1768)
    assert opt.mergeAlternately("abc", "pqr") == "apbqcr"
    assert opt.mergeAlternately("ab", "pqrs") == "apbqrs"
    assert opt.mergeAlternately("abcd", "pq") == "apbqcd"
    for _ in range(300):
        a = "".join(R.choice("abc") for _ in range(R.randint(1, 8)))
        b = "".join(R.choice("xyz") for _ in range(R.randint(1, 8)))
        assert brute.mergeAlternately(a, b) == opt.mergeAlternately(a, b), (a, b)
