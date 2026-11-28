"""Shared helpers for the tests_g01_*.py checks (Gap notes g01: arrays, BST, bits, DP, design classes, graph traversals, greedy).
"""
import random
from itertools import product

from harness import case
from tests_b10 import timed_call

R = random.Random(101)


def both(h, num, name="Solution"):
    brute, opt = h.lc_all(num, name)
    return brute[name](), opt[name]()


def random_tree(n):
    labels = list(range(n))
    R.shuffle(labels)
    return [[labels[R.randrange(i)], labels[i]] for i in range(1, n)]


def random_grid(symbols):
    rows, cols = R.randint(1, 6), R.randint(1, 6)
    return [[R.choice(symbols) for _ in range(cols)] for _ in range(rows)]
