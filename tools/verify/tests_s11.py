"""Linked list basics: Floyd's cycle entry, intersection, palindrome, odd/even split, middle node.

Pointer-returning problems are checked by node identity; mutating problems get a fresh list per call.
"""
import random

from harness import build_list, case, list_to_py, ListNode
from tests_b10 import timed_call

R = random.Random(1111)


def both(h, num):
    brute, opt = h.lc_all(num, "Solution")
    return brute["Solution"](), opt["Solution"]()


def cyclic_list(vals, pos):
    """List from vals whose tail links to index pos (-1 = no cycle); returns (head, nodes)."""
    nodes = [ListNode(v) for v in vals]
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    if nodes and pos >= 0:
        nodes[-1].next = nodes[pos]
    return (nodes[0] if nodes else None), nodes


def y_lists(a_vals, b_vals, shared_vals):
    """Two lists with private prefixes merging into one shared tail; returns (headA, headB, first shared)."""
    shared = build_list(shared_vals)
    a_head = build_list(a_vals)
    b_head = build_list(b_vals)

    def attach(head):
        if head is None:
            return shared
        node = head
        while node.next:
            node = node.next
        node.next = shared
        return head

    return attach(a_head), attach(b_head), shared


@case(142)
def _(h):
    brute, opt = both(h, 142)
    for vals, pos in [([3, 2, 0, -4], 1), ([1, 2], 0), ([1], -1)]:
        head, nodes = cyclic_list(vals, pos)
        want = nodes[pos] if pos >= 0 else None
        assert opt.detectCycle(head) is want and brute.detectCycle(head) is want, (vals, pos)
    assert opt.detectCycle(None) is None
    for _ in range(300):
        n = R.randint(0, 12)
        pos = R.randint(-1, n - 1)
        head, nodes = cyclic_list([R.randint(-3, 3) for _ in range(n)], pos)
        want = nodes[pos] if pos >= 0 else None
        assert brute.detectCycle(head) is want and opt.detectCycle(head) is want, (n, pos)
    head, _ = cyclic_list(list(range(10_000)), 5_000)
    timed_call(lambda: opt.detectCycle(head), 1)


@case(160)
def _(h):
    brute, opt = both(h, 160)
    a, b, s = y_lists([4, 1], [5, 6, 1], [8, 4, 5])
    assert s is not None and opt.getIntersectionNode(a, b) is s and s.val == 8
    a, b, s = y_lists([1, 9, 1], [3], [2, 4])
    assert s is not None and opt.getIntersectionNode(a, b) is s and s.val == 2
    assert opt.getIntersectionNode(build_list([2, 6, 4]), build_list([1, 5])) is None
    for _ in range(300):
        shared_vals = [R.randint(1, 4) for _ in range(R.randint(0, 5))]
        a_vals = [R.randint(1, 4) for _ in range(R.randint(0 if shared_vals else 1, 5))]
        b_vals = [R.randint(1, 4) for _ in range(R.randint(0 if shared_vals else 1, 5))]
        a, b, s = y_lists(a_vals, b_vals, shared_vals)
        before = (list_to_py(a), list_to_py(b))
        assert brute.getIntersectionNode(a, b) is s and opt.getIntersectionNode(a, b) is s, (a_vals, b_vals, shared_vals)
        assert (list_to_py(a), list_to_py(b)) == before
    a, b, s = y_lists(list(range(20_000)), list(range(10_000)), list(range(10_000)))
    timed_call(lambda: opt.getIntersectionNode(a, b), 1)


@case(234)
def _(h):
    brute, opt = both(h, 234)
    assert opt.isPalindrome(build_list([1, 2, 2, 1])) is True
    assert opt.isPalindrome(build_list([1, 2])) is False
    for _ in range(400):
        n = R.randint(1, 10)
        vals = [R.randint(0, 2) for _ in range(n)]
        if R.random() < 0.4:
            vals = vals[: (n + 1) // 2] + vals[: n // 2][::-1]
        head = build_list(vals)
        got = opt.isPalindrome(head)
        assert got == brute.isPalindrome(build_list(vals)) == (vals == vals[::-1]), vals
        assert list_to_py(head) == vals, "input list must be restored"
    big = [R.randint(0, 9) for _ in range(50_000)]
    big_list = build_list(big + big[::-1])
    timed_call(lambda: opt.isPalindrome(big_list), 1)


@case(287)
def _(h):
    brute, opt = both(h, 287)
    assert opt.findDuplicate([1, 3, 4, 2, 2]) == 2
    assert opt.findDuplicate([3, 1, 3, 4, 2]) == 3
    assert opt.findDuplicate([3, 3, 3, 3, 3]) == 3
    for _ in range(400):
        n = R.randint(1, 12)
        dup = R.randint(1, n)
        copies = R.randint(2, n + 1)
        others = R.sample([v for v in range(1, n + 1) if v != dup], n + 1 - copies)
        nums = [dup] * copies + others
        R.shuffle(nums)
        snapshot = nums[:]
        assert brute.findDuplicate(nums) == opt.findDuplicate(nums) == dup, nums
        assert nums == snapshot
    n = 100_000
    nums = list(range(1, n + 1)) + [R.randint(1, n)]
    R.shuffle(nums)
    timed_call(lambda: opt.findDuplicate(nums), 1)


@case(328)
def _(h):
    brute, opt = both(h, 328)
    assert list_to_py(opt.oddEvenList(build_list([1, 2, 3, 4, 5]))) == [1, 3, 5, 2, 4]
    assert list_to_py(opt.oddEvenList(build_list([2, 1, 3, 5, 6, 4, 7]))) == [2, 3, 6, 7, 1, 5, 4]
    assert opt.oddEvenList(None) is None
    for _ in range(300):
        vals = [R.randint(-5, 5) for _ in range(R.randint(0, 12))]
        want = vals[0::2] + vals[1::2]
        assert list_to_py(brute.oddEvenList(build_list(vals))) == want, vals
        assert list_to_py(opt.oddEvenList(build_list(vals))) == want, vals
    big = build_list(list(range(10_000)))
    timed_call(lambda: opt.oddEvenList(big), 1)


@case(876)
def _(h):
    brute, opt = both(h, 876)
    assert list_to_py(opt.middleNode(build_list([1, 2, 3, 4, 5]))) == [3, 4, 5]
    assert list_to_py(opt.middleNode(build_list([1, 2, 3, 4, 5, 6]))) == [4, 5, 6]
    for _ in range(200):
        vals = [R.randint(1, 100) for _ in range(R.randint(1, 100))]
        head = build_list(vals)
        mid = opt.middleNode(head)
        assert mid is brute.middleNode(head), vals
        assert list_to_py(mid) == vals[len(vals) // 2:], vals


@case(2095)
def _(h):
    brute, opt = both(h, 2095)
    assert list_to_py(opt.deleteMiddle(build_list([1, 3, 4, 7, 1, 2, 6]))) == [1, 3, 4, 1, 2, 6]
    assert list_to_py(opt.deleteMiddle(build_list([1, 2, 3, 4]))) == [1, 2, 4]
    assert list_to_py(opt.deleteMiddle(build_list([2, 1]))) == [2]
    assert opt.deleteMiddle(build_list([7])) is None and brute.deleteMiddle(build_list([7])) is None
    for _ in range(300):
        vals = [R.randint(1, 9) for _ in range(R.randint(1, 15))]
        want = vals[: len(vals) // 2] + vals[len(vals) // 2 + 1:]
        assert list_to_py(brute.deleteMiddle(build_list(vals))) == want, vals
        assert list_to_py(opt.deleteMiddle(build_list(vals))) == want, vals
    big = build_list(list(range(100_000)))
    timed_call(lambda: opt.deleteMiddle(big), 1)
