"""Linked-list sheet notes: carry addition, k-group / range reversal, rotation, run deletion,
stable partition, deep copy with random pointers.

Every call gets a freshly built list because all of these solutions relink their input.
"""
import random

from harness import build_list, case, list_to_py
from tests_b10 import timed_call

R = random.Random(10_010)


def both(h, num):
    brute, opt = h.lc_all(num, "Solution")
    return brute["Solution"](), opt["Solution"]()


def run(sol, method, vals, *args):
    return list_to_py(getattr(sol, method)(build_list(list(vals)), *args))


@case(2)
def _(h):
    brute, opt = both(h, 2)

    def add(sol, a, b):
        return list_to_py(sol.addTwoNumbers(build_list(a), build_list(b)))

    assert add(opt, [2, 4, 3], [5, 6, 4]) == [7, 0, 8]
    assert add(opt, [0], [0]) == [0]
    assert add(opt, [9] * 7, [9] * 4) == [8, 9, 9, 9, 0, 0, 0, 1]
    for _ in range(300):
        a = [R.randint(0, 9) for _ in range(R.randint(1, 12))]
        b = [R.randint(0, 9) for _ in range(R.randint(1, 12))]
        if len(a) > 1 and a[-1] == 0:
            a[-1] = R.randint(1, 9)
        if len(b) > 1 and b[-1] == 0:
            b[-1] = R.randint(1, 9)
        assert add(brute, a, b) == add(opt, a, b), (a, b)
    assert add(opt, [9] * 100, [1]) == [0] * 100 + [1]


@case(25)
def _(h):
    brute, opt = both(h, 25)
    assert run(opt, "reverseKGroup", [1, 2, 3, 4, 5], 2) == [2, 1, 4, 3, 5]
    assert run(opt, "reverseKGroup", [1, 2, 3, 4, 5], 3) == [3, 2, 1, 4, 5]
    for _ in range(300):
        vals = [R.randint(0, 9) for _ in range(R.randint(1, 15))]
        k = R.randint(1, len(vals))
        expected = []
        for i in range(0, len(vals), k):
            chunk = vals[i:i + k]
            expected += chunk[::-1] if len(chunk) == k else chunk
        assert run(brute, "reverseKGroup", vals, k) == expected, (vals, k)
        assert run(opt, "reverseKGroup", vals, k) == expected, (vals, k)
    big = list(range(5000))
    timed_call(lambda: run(opt, "reverseKGroup", big, 7), 1)


@case(61)
def _(h):
    brute, opt = both(h, 61)
    assert run(opt, "rotateRight", [1, 2, 3, 4, 5], 2) == [4, 5, 1, 2, 3]
    assert run(opt, "rotateRight", [0, 1, 2], 4) == [2, 0, 1]
    assert run(opt, "rotateRight", [], 3) == []
    for _ in range(300):
        vals = [R.randint(-100, 100) for _ in range(R.randint(0, 10))]
        k = R.randint(0, 30)
        expected = vals[-(k % len(vals)):] + vals[:-(k % len(vals))] if vals and k % len(vals) else vals
        assert run(brute, "rotateRight", vals, k) == expected, (vals, k)
        assert run(opt, "rotateRight", vals, k) == expected, (vals, k)
    big = list(range(500))
    assert run(opt, "rotateRight", big, 2 * 10**9) == big[-(2 * 10**9 % 500):] + big[:-(2 * 10**9 % 500)]


@case(82)
def _(h):
    brute, opt = both(h, 82)
    assert run(opt, "deleteDuplicates", [1, 2, 3, 3, 4, 4, 5]) == [1, 2, 5]
    assert run(opt, "deleteDuplicates", [1, 1, 1, 2, 3]) == [2, 3]
    assert run(opt, "deleteDuplicates", []) == []
    for _ in range(300):
        vals = sorted(R.randint(-5, 5) for _ in range(R.randint(0, 15)))
        expected = [v for v in vals if vals.count(v) == 1]
        assert run(brute, "deleteDuplicates", vals) == expected, vals
        assert run(opt, "deleteDuplicates", vals) == expected, vals


@case(86)
def _(h):
    brute, opt = both(h, 86)
    assert run(opt, "partition", [1, 4, 3, 2, 5, 2], 3) == [1, 2, 2, 4, 3, 5]
    assert run(opt, "partition", [2, 1], 2) == [1, 2]
    for _ in range(300):
        vals = [R.randint(-10, 10) for _ in range(R.randint(0, 15))]
        x = R.randint(-12, 12)
        expected = [v for v in vals if v < x] + [v for v in vals if v >= x]
        assert run(brute, "partition", vals, x) == expected, (vals, x)
        assert run(opt, "partition", vals, x) == expected, (vals, x)


@case(92)
def _(h):
    brute, opt = both(h, 92)
    assert run(opt, "reverseBetween", [1, 2, 3, 4, 5], 2, 4) == [1, 4, 3, 2, 5]
    assert run(opt, "reverseBetween", [5], 1, 1) == [5]
    for _ in range(300):
        vals = [R.randint(-500, 500) for _ in range(R.randint(1, 15))]
        left = R.randint(1, len(vals))
        right = R.randint(left, len(vals))
        expected = vals[:left - 1] + vals[left - 1:right][::-1] + vals[right:]
        assert run(brute, "reverseBetween", vals, left, right) == expected, (vals, left, right)
        assert run(opt, "reverseBetween", vals, left, right) == expected, (vals, left, right)


@case(138)
def _(h):
    brute_ns, opt_ns = h.lc_all(138, "Solution")

    def build(pairs, node_cls):
        nodes = [node_cls(v) for v, _ in pairs]
        for i, (_, r) in enumerate(pairs):
            if i + 1 < len(nodes):
                nodes[i].next = nodes[i + 1]
            nodes[i].random = None if r is None else nodes[r]
        return nodes[0] if nodes else None, nodes

    def encode(head):
        nodes = []
        while head:
            nodes.append(head)
            head = head.next
        index = {id(n): i for i, n in enumerate(nodes)}
        return [[n.val, None if n.random is None else index[id(n.random)]] for n in nodes], nodes

    def check(ns, pairs):
        head, originals = build(pairs, ns["Node"])
        copy = ns["Solution"]().copyRandomList(head)
        encoded, copies = encode(copy)
        assert encoded == pairs, (pairs, encoded)
        assert not {id(n) for n in originals} & {id(n) for n in copies}, "copy shares nodes with input"
        assert encode(head)[0] == pairs, "input list was not restored"

    example = [[7, None], [13, 0], [11, 4], [10, 2], [1, 0]]
    for ns in (brute_ns, opt_ns):
        check(ns, example)
        check(ns, [[1, 1], [2, 1]])
        check(ns, [[3, None], [3, 0], [3, None]])
        check(ns, [])
    for _ in range(200):
        n = R.randint(0, 12)
        pairs = [[R.randint(-5, 5), R.choice([None] + list(range(n)))] for _ in range(n)]
        check(brute_ns, pairs)
        check(opt_ns, pairs)
    big = [[R.randint(-10**4, 10**4), R.choice([None] + list(range(1000)))] for _ in range(1000)]
    timed_call(lambda: check(opt_ns, big), 1)
