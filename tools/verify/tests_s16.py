"""Stack / monotonic stack sheet notes: paths, calculators, next-greater, spans, fleets, LFU cache.

Each note's brute force and optimized block must agree on random inputs and on LeetCode's examples.
"""
import ast
import itertools
import operator
import random

from harness import case
from tests_b10 import timed_call

BINARY = {ast.Add: operator.add, ast.Sub: operator.sub}


def arithmetic(expr):
    """Independent oracle for 224: evaluate +, -, unary -, parentheses and integers only (no eval)."""
    def walk(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, int):
            return node.value
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
            value = walk(node.operand)
            return -value if isinstance(node.op, ast.USub) else value
        if isinstance(node, ast.BinOp) and type(node.op) in BINARY:
            return BINARY[type(node.op)](walk(node.left), walk(node.right))
        raise ValueError(f"unexpected syntax: {ast.dump(node)}")
    return walk(ast.parse(expr, mode="eval").body)

R = random.Random(1616)


def both(h, num, name="Solution"):
    brute, opt = h.lc_all(num, name)
    return brute[name](), opt[name]()


@case(71)
def _(h):
    brute, opt = both(h, 71)
    examples = {"/home/": "/home", "/home//foo/": "/home/foo", "/../": "/",
                "/home/user/Documents/../Pictures": "/home/user/Pictures",
                "/.../a/../b/c/../d/./": "/.../b/d"}
    for path, want in examples.items():
        assert opt.simplifyPath(path) == want and brute.simplifyPath(path) == want, path
    pieces = ["a", "bc", ".", "..", "...", "", "_x", "..a"]
    for _ in range(400):
        path = "/" + "/".join(R.choice(pieces) for _ in range(R.randint(0, 10)))
        if R.random() < 0.3:
            path += "/"
        assert brute.simplifyPath(path) == opt.simplifyPath(path), path
    big = "/" + "/".join(R.choice(["a", "..", "."]) for _ in range(1400))
    timed_call(lambda: opt.simplifyPath(big[:3000]), 1)


@case(85)
def _(h):
    brute, opt = both(h, 85)
    grid = [["1", "0", "1", "0", "0"], ["1", "0", "1", "1", "1"],
            ["1", "1", "1", "1", "1"], ["1", "0", "0", "1", "0"]]
    assert opt.maximalRectangle(grid) == 6 and brute.maximalRectangle(grid) == 6
    assert opt.maximalRectangle([["0"]]) == 0 and opt.maximalRectangle([["1"]]) == 1
    for _ in range(300):
        rows, cols = R.randint(1, 6), R.randint(1, 6)
        p = R.random()
        grid = [["1" if R.random() < p else "0" for _ in range(cols)] for _ in range(rows)]
        assert brute.maximalRectangle(grid) == opt.maximalRectangle(grid), grid
    full = [["1"] * 200 for _ in range(200)]
    assert opt.maximalRectangle(full) == 40_000
    noisy = [["1" if R.random() < 0.8 else "0" for _ in range(200)] for _ in range(200)]
    timed_call(lambda: opt.maximalRectangle(noisy), 2)


def random_expr(depth):
    parts = ["-"] if R.random() < 0.3 else []
    for k in range(R.randint(1, 4)):
        if k:
            parts.append(R.choice(["+", "-"]))
        if depth and R.random() < 0.35:
            parts.append("(" + random_expr(depth - 1) + ")")
        else:
            parts.append(str(R.randint(0, 120)))
    return "".join(p + (" " if R.random() < 0.3 else "") for p in parts)


@case(224)
def _(h):
    brute, opt = both(h, 224)
    for s, want in [("1 + 1", 2), (" 2-1 + 2 ", 3), ("(1+(4+5+2)-3)+(6+8)", 23),
                    ("-(2 + 3)", -5), ("1-(-2)", 3), ("- (3 + (4 + 5))", -12)]:
        assert opt.calculate(s) == want and brute.calculate(s) == want, s
    for _ in range(500):
        s = random_expr(3)
        want = arithmetic(s)
        assert brute.calculate(s) == want and opt.calculate(s) == want, s
    depth = 100_000
    deep = "(" * depth + "1-2" + ")" * depth
    assert opt.calculate(deep) == -1
    chain = "+".join("(" + str(i % 10) + "-1)" for i in range(50_000))
    timed_call(lambda: opt.calculate(chain[:300_000]), 2)


@case(402)
def _(h):
    brute, opt = both(h, 402)
    for num, k, want in [("1432219", 3, "1219"), ("10200", 1, "200"), ("10", 2, "0")]:
        assert opt.removeKdigits(num, k) == want and brute.removeKdigits(num, k) == want, num
    for _ in range(400):
        n = R.randint(1, 8)
        num = str(R.randint(1, 9)) + "".join(R.choice("0012349") for _ in range(n - 1))
        if n == 1 and R.random() < 0.2:
            num = "0"
        k = R.randint(1, n)
        got = opt.removeKdigits(num, k)
        assert brute.removeKdigits(num, k) == got, (num, k)
        best = min((int("".join(num[i] for i in keep) or "0")
                    for keep in itertools.combinations(range(n), n - k)), default=0)
        assert got == str(best), (num, k, got, best)
    big = "".join(R.choice("0123456789") for _ in range(100_000))
    big = "1" + big[1:]
    timed_call(lambda: opt.removeKdigits(big, 50_000), 2)


@case(460)
def _(h):
    brute, opt = h.lc_all(460, "LFUCache")
    for cls in (brute["LFUCache"], opt["LFUCache"]):
        c = cls(2)
        out = [c.put(1, 1), c.put(2, 2), c.get(1), c.put(3, 3), c.get(2), c.get(3),
               c.put(4, 4), c.get(1), c.get(3), c.get(4)]
        assert out == [None, None, 1, None, -1, 3, None, -1, 3, 4], out
    for _ in range(200):
        cap = R.randint(1, 4)
        a, b = brute["LFUCache"](cap), opt["LFUCache"](cap)
        for _ in range(R.randint(1, 40)):
            key = R.randint(0, 6)
            if R.random() < 0.5:
                assert a.get(key) == b.get(key), key
            else:
                val = R.randint(0, 100)
                a.put(key, val)
                b.put(key, val)
    big = opt["LFUCache"](10_000)

    def run():
        for i in range(200_000):
            if i % 2:
                big.get(R.randint(0, 20_000))
            else:
                big.put(R.randint(0, 20_000), i)
    timed_call(run, 2)


@case(496)
def _(h):
    brute, opt = both(h, 496)
    assert opt.nextGreaterElement([4, 1, 2], [1, 3, 4, 2]) == [-1, 3, -1]
    assert opt.nextGreaterElement([2, 4], [1, 2, 3, 4]) == [3, -1]
    for _ in range(300):
        nums2 = R.sample(range(0, 30), R.randint(1, 12))
        nums1 = R.sample(nums2, R.randint(1, len(nums2)))
        assert brute.nextGreaterElement(nums1, nums2) == opt.nextGreaterElement(nums1, nums2), (nums1, nums2)


@case(503)
def _(h):
    brute, opt = both(h, 503)
    assert opt.nextGreaterElements([1, 2, 1]) == [2, -1, 2]
    assert opt.nextGreaterElements([1, 2, 3, 4, 3]) == [2, 3, 4, -1, 4]
    for _ in range(300):
        nums = [R.randint(-5, 5) for _ in range(R.randint(1, 12))]
        assert brute.nextGreaterElements(nums) == opt.nextGreaterElements(nums), nums
    big = [R.randint(-10**9, 10**9) for _ in range(10_000)]
    timed_call(lambda: opt.nextGreaterElements(big), 1)


@case(853)
def _(h):
    brute, opt = both(h, 853)
    for args, want in [((12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]), 3), ((10, [3], [3]), 1),
                       ((100, [0, 2, 4], [4, 2, 1]), 1)]:
        assert opt.carFleet(*args) == want and brute.carFleet(*args) == want, args
    for _ in range(400):
        target = R.randint(2, 30)
        n = R.randint(1, min(8, target))
        position = R.sample(range(target), n)
        speed = [R.randint(1, 6) for _ in range(n)]
        assert brute.carFleet(target, position, speed) == opt.carFleet(target, position, speed), \
            (target, position, speed)
    target = 10**6
    position = R.sample(range(target), 100_000)
    speed = [R.randint(1, 10**6) for _ in range(100_000)]
    timed_call(lambda: opt.carFleet(target, position, speed), 2)


@case(901)
def _(h):
    brute, opt = h.lc_all(901, "StockSpanner")
    for cls in (brute["StockSpanner"], opt["StockSpanner"]):
        s = cls()
        assert [s.next(p) for p in [100, 80, 60, 70, 60, 75, 85]] == [1, 1, 1, 2, 1, 4, 6]
    for _ in range(200):
        a, b = brute["StockSpanner"](), opt["StockSpanner"]()
        for _ in range(R.randint(1, 30)):
            p = R.randint(1, 8)
            assert a.next(p) == b.next(p)
    big = opt["StockSpanner"]()
    timed_call(lambda: [big.next(p) for p in range(1, 10_001)], 1)


@case(2104)
def _(h):
    brute, opt = both(h, 2104)
    for nums, want in [([1, 2, 3], 4), ([1, 3, 3], 4), ([4, -2, -3, 4, 1], 59)]:
        assert opt.subArrayRanges(nums) == want and brute.subArrayRanges(nums) == want, nums
    for _ in range(300):
        nums = [R.randint(-4, 4) for _ in range(R.randint(1, 12))]
        assert brute.subArrayRanges(nums) == opt.subArrayRanges(nums), nums
    big = [R.randint(-10**9, 10**9) for _ in range(1000)]
    assert brute.subArrayRanges(big) == opt.subArrayRanges(big)
    timed_call(lambda: opt.subArrayRanges(big), 1)
