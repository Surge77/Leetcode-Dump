"""Brute-force backfill bf06: stack/queue adapters, design classes, divide & conquer, fast & slow pointers.

Each note's first python block is the brute force; it must pass LeetCode's examples and agree with
the note's last (optimized) block on random small inputs or random operation sequences.
"""
import random

from harness import (blocks_of, build_list, build_tree, case, lc_path, list_to_py, ns_from,
                     tree_to_list)

R = random.Random(606)


def brute_opt(num):
    blocks = blocks_of(lc_path(num))
    return ns_from(blocks[0]), ns_from(blocks[-1])


def replay(make_brute, make_opt, ops):
    """Run the same random op sequence on both instances; every return value must match."""
    a, b = make_brute(), make_opt()
    for name, args in ops:
        got, want = getattr(a, name)(*args), getattr(b, name)(*args)
        assert got == want, (name, args, got, want)


def stack_ops(count, reads=("pop", "top"), with_empty=True):
    """Random push/read sequence that never reads from an empty structure."""
    ops, size = [], 0
    for _ in range(count):
        if size == 0 or R.random() < 0.45:
            ops.append(("push", (R.randint(-9, 9),)))
            size += 1
        else:
            name = R.choice(reads)
            ops.append((name, ()))
            if name == "pop":
                size -= 1
        if with_empty:
            ops.append(("empty", ()))
    return ops


@case("225-brute")
def _(h):
    brute, opt = brute_opt(225)
    st = brute["MyStack"]()
    st.push(1)
    st.push(2)
    assert st.top() == 2 and st.pop() == 2 and st.empty() is False
    for _ in range(150):
        replay(brute["MyStack"], opt["MyStack"], stack_ops(R.randint(1, 30)))


@case("232-brute")
def _(h):
    brute, opt = brute_opt(232)
    q = brute["MyQueue"]()
    q.push(1)
    q.push(2)
    assert q.peek() == 1 and q.pop() == 1 and q.empty() is False
    for _ in range(150):
        replay(brute["MyQueue"], opt["MyQueue"], stack_ops(R.randint(1, 30), reads=("pop", "peek")))


@case("146-brute")
def _(h):
    brute, opt = brute_opt(146)
    c = brute["LRUCache"](2)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == 1
    c.put(3, 3)
    assert c.get(2) == -1
    c.put(4, 4)
    assert c.get(1) == -1 and c.get(3) == 3 and c.get(4) == 4
    for _ in range(200):
        cap = R.randint(1, 4)
        ops = []
        for _ in range(R.randint(1, 40)):
            key = R.randint(1, 6)
            ops.append(("get", (key,)) if R.random() < 0.5 else ("put", (key, R.randint(1, 99))))
        replay(lambda: brute["LRUCache"](cap), lambda: opt["LRUCache"](cap), ops)


@case("155-brute")
def _(h):
    brute, opt = brute_opt(155)
    st = brute["MinStack"]()
    for v in (-2, 0, -3):
        st.push(v)
    assert st.getMin() == -3
    st.pop()
    assert st.top() == 0 and st.getMin() == -2
    for _ in range(150):
        ops = stack_ops(R.randint(1, 30), reads=("pop", "top", "getMin"), with_empty=False)
        replay(brute["MinStack"], opt["MinStack"], ops)


@case("622-brute")
def _(h):
    brute, opt = brute_opt(622)
    q = brute["MyCircularQueue"](3)
    assert [q.enQueue(1), q.enQueue(2), q.enQueue(3), q.enQueue(4)] == [True, True, True, False]
    assert q.Rear() == 3 and q.isFull() is True and q.deQueue() is True
    assert q.enQueue(4) is True and q.Rear() == 4
    names = ("enQueue", "deQueue", "Front", "Rear", "isEmpty", "isFull")
    for _ in range(200):
        k = R.randint(1, 5)
        ops = []
        for _ in range(R.randint(1, 40)):
            name = R.choice(names)
            ops.append((name, (R.randint(0, 9),) if name == "enQueue" else ()))
        replay(lambda: brute["MyCircularQueue"](k), lambda: opt["MyCircularQueue"](k), ops)


@case("105-brute")
def _(h):
    brute, opt = brute_opt(105)
    S, O = brute["Solution"](), opt["Solution"]()
    assert tree_to_list(S.buildTree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])) == [3, 9, 20, None, None, 15, 7]
    assert tree_to_list(S.buildTree([-1], [-1])) == [-1]
    for _ in range(200):
        n = R.randint(1, 12)
        vals = R.sample(range(-30, 31), n)
        root = build_tree([vals[0]] + [v if R.random() < 0.8 else None for v in vals[1:]])
        pre, ino, stack, node = [], [], [root], root
        while stack:
            cur = stack.pop()
            if cur:
                pre.append(cur.val)
                stack += [cur.right, cur.left]
        stack = []
        while stack or node:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            ino.append(node.val)
            node = node.right
        got = tree_to_list(S.buildTree(list(pre), list(ino)))
        assert got == tree_to_list(O.buildTree(list(pre), list(ino))) == tree_to_list(root), (pre, ino)


@case("23-brute")
def _(h):
    brute, opt = brute_opt(23)
    S, O = brute["Solution"](), opt["Solution"]()
    ex = [[1, 4, 5], [1, 3, 4], [2, 6]]
    assert list_to_py(S.mergeKLists([build_list(x) for x in ex])) == [1, 1, 2, 3, 4, 4, 5, 6]
    assert S.mergeKLists([]) is None and S.mergeKLists([None]) is None
    for _ in range(200):
        lists = [sorted(R.randint(-9, 9) for _ in range(R.randint(0, 5))) for _ in range(R.randint(0, 5))]
        got = list_to_py(S.mergeKLists([build_list(x) for x in lists]))
        assert got == list_to_py(O.mergeKLists([build_list(x) for x in lists])), lists


@case("50-brute")
def _(h):
    brute, opt = brute_opt(50)
    S, O = brute["Solution"](), opt["Solution"]()
    assert abs(S.myPow(2.0, 10) - 1024.0) < 1e-9
    assert abs(S.myPow(2.1, 3) - 9.261) < 1e-9
    assert abs(S.myPow(2.0, -2) - 0.25) < 1e-12
    for _ in range(300):
        x, n = round(R.uniform(-3, 3), 3), R.randint(-12, 12)
        if x == 0 and n < 0:
            continue
        got, want = S.myPow(x, n), O.myPow(x, n)
        assert abs(got - want) <= 1e-9 * max(1, abs(want)), (x, n, got, want)


@case("141-brute")
def _(h):
    brute, opt = brute_opt(141)
    S, O = brute["Solution"](), opt["Solution"]()

    def make(vals, pos):
        head = build_list(vals)
        nodes, node = [], head
        while node:
            nodes.append(node)
            node = node.next
        if pos >= 0:
            nodes[-1].next = nodes[pos]
        return head

    assert S.hasCycle(make([3, 2, 0, -4], 1)) is True
    assert S.hasCycle(make([1, 2], 0)) is True
    assert S.hasCycle(make([1], -1)) is False
    for _ in range(200):
        n = R.randint(0, 10)
        pos = R.randint(-1, n - 1) if n else -1
        vals = [R.randint(-5, 5) for _ in range(n)]
        assert S.hasCycle(make(vals, pos)) == O.hasCycle(make(vals, pos)) == (pos >= 0), (vals, pos)


@case("143-brute")
def _(h):
    brute, opt = brute_opt(143)
    S, O = brute["Solution"](), opt["Solution"]()
    for vals, want in (([1, 2, 3, 4], [1, 4, 2, 3]), ([1, 2, 3, 4, 5], [1, 5, 2, 4, 3])):
        head = build_list(vals)
        S.reorderList(head)
        assert list_to_py(head) == want
    for _ in range(200):
        vals = [R.randint(-9, 9) for _ in range(R.randint(1, 15))]
        a, b = build_list(vals), build_list(vals)
        S.reorderList(a)
        O.reorderList(b)
        assert list_to_py(a, 100) == list_to_py(b, 100), vals
