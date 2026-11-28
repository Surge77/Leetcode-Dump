"""Shared helpers for the tests_g02_*.py checks (Gap notes g02: hashing, intervals, linked list, GCD, binary search, prefix sum, sliding window, stack).
"""
import random

from harness import case
from tests_b10 import timed_call

R = random.Random(202)


def both(h, num, name="Solution"):
    brute, opt = h.lc_all(num, name)
    return brute, opt


def pair(h, num):
    brute, opt = both(h, num)
    return brute["Solution"](), opt["Solution"]()


def iter_nodes(head):
    while head:
        yield head
        head = head.next
