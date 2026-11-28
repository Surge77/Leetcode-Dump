"""Shared helpers for the tests_g03_*.py checks (Gap notes g03: stack, heap/top-k, tree traversal, trie/palindromes, two pointers).
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
