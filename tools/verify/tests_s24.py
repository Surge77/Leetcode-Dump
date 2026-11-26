"""Greedy notes: cookies, wildcard parentheses, partition labels, straights, lemonade change, merge triplets.

Each note's brute force and optimized blocks must agree on random small inputs and on
LeetCode's examples; the optimized one is run once at max constraints.
"""
import random

from harness import case
from tests_b10 import timed_call

R = random.Random(24)


def both(h, num):
    brute, opt = h.lc_all(num, "Solution")
    return brute["Solution"](), opt["Solution"]()


@case(455)
def _(h):
    brute, opt = both(h, 455)
    assert opt.findContentChildren([1, 2, 3], [1, 1]) == 1
    assert opt.findContentChildren([1, 2], [1, 2, 3]) == 2
    assert opt.findContentChildren([1], []) == 0
    for _ in range(300):
        g = [R.randint(1, 8) for _ in range(R.randint(1, 8))]
        s = [R.randint(1, 8) for _ in range(R.randint(0, 8))]
        assert brute.findContentChildren(list(g), list(s)) == opt.findContentChildren(list(g), list(s)), (g, s)
    n = 30_000
    big_g = [R.randint(1, 2**31 - 1) for _ in range(n)]
    big_s = [R.randint(1, 2**31 - 1) for _ in range(n)]
    timed_call(lambda: opt.findContentChildren(big_g, big_s), 2)


@case(678)
def _(h):
    brute, opt = both(h, 678)
    assert opt.checkValidString("()") is True
    assert opt.checkValidString("(*)") is True
    assert opt.checkValidString("(*))") is True
    assert opt.checkValidString("*(") is False
    assert opt.checkValidString(")") is False
    for _ in range(500):
        s = "".join(R.choice("()*") for _ in range(R.randint(1, 12)))
        assert brute.checkValidString(s) == opt.checkValidString(s), s
    timed_call(lambda: opt.checkValidString("".join(R.choice("()*") for _ in range(100))), 1)


@case(763)
def _(h):
    brute, opt = both(h, 763)
    assert opt.partitionLabels("ababcbacadefegdehijhklij") == [9, 7, 8]
    assert opt.partitionLabels("eccbbbbdec") == [10]
    for _ in range(300):
        s = "".join(R.choice("abcdef") for _ in range(R.randint(1, 20)))
        assert brute.partitionLabels(s) == opt.partitionLabels(s), s
    timed_call(lambda: opt.partitionLabels("".join(R.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(500))), 1)


@case(846)
def _(h):
    brute, opt = both(h, 846)
    assert opt.isNStraightHand([1, 2, 3, 6, 2, 3, 4, 7, 8], 3) is True
    assert opt.isNStraightHand([1, 2, 3, 4, 5], 4) is False
    assert opt.isNStraightHand([1, 2, 4, 5], 2) is True
    for _ in range(400):
        hand = [R.randint(0, 8) for _ in range(R.randint(1, 12))]
        k = R.randint(1, len(hand))
        assert brute.isNStraightHand(list(hand), k) == opt.isNStraightHand(list(hand), k), (hand, k)
    n = 10_000
    big = [v for start in range(0, 10**9 - 10, 10**9 // 2000)[:2000] for v in range(start, start + 5)]
    R.shuffle(big)
    assert len(big) == n
    assert opt.isNStraightHand(big, 5) is True
    timed_call(lambda: opt.isNStraightHand(big, 5), 2)


@case(860)
def _(h):
    brute, opt = both(h, 860)
    assert opt.lemonadeChange([5, 5, 5, 10, 20]) is True
    assert opt.lemonadeChange([5, 5, 10, 10, 20]) is False
    assert opt.lemonadeChange([5, 5, 5, 5, 10, 20, 10, 10]) is True
    assert opt.lemonadeChange([10]) is False
    for _ in range(500):
        bills = [R.choice((5, 5, 10, 20)) for _ in range(R.randint(1, 12))]
        assert brute.lemonadeChange(bills) == opt.lemonadeChange(bills), bills
    timed_call(lambda: opt.lemonadeChange([R.choice((5, 5, 10, 20)) for _ in range(10**5)]), 2)


@case(1899)
def _(h):
    brute, opt = both(h, 1899)
    assert opt.mergeTriplets([[2, 5, 3], [1, 8, 4], [1, 7, 5]], [2, 7, 5]) is True
    assert opt.mergeTriplets([[3, 4, 5], [4, 5, 6]], [3, 2, 5]) is False
    assert opt.mergeTriplets([[2, 5, 3], [2, 3, 4], [1, 2, 5], [5, 2, 3]], [5, 5, 5]) is True
    for _ in range(300):
        triplets = [[R.randint(1, 4) for _ in range(3)] for _ in range(R.randint(1, 8))]
        target = [R.randint(1, 4) for _ in range(3)]
        assert brute.mergeTriplets(triplets, target) == opt.mergeTriplets(triplets, target), (triplets, target)
    big = [[R.randint(1, 1000) for _ in range(3)] for _ in range(10**5)]
    timed_call(lambda: opt.mergeTriplets(big, [1000, 1000, 1000]), 2)
