"""Shared helpers for the tests_original_*.py checks (Checks for the notes that existed before the Infosys expansion).
"""
import random
import re
from collections import Counter, OrderedDict, deque
from itertools import combinations, permutations, product
from math import comb, isqrt

from harness import TreeNode, build_list, build_tree, case, lc_all, lc_path, list_to_py, tree_to_list

R = random.Random(2024)
BRUTE_HEADING_RE = re.compile(r"^#+ .*Code Snippet \(Brute Force\)", re.M)


def solvers(num, name="Solution"):
    """Every solution block except the brute force: brute forces are checked on small inputs by the
    '<num>-brute' cases, and the inputs here (e.g. t = 5000 for 3335) are sized for real solutions."""
    namespaces = lc_all(num, name)
    if BRUTE_HEADING_RE.search(lc_path(num).read_text(encoding="utf-8")) and len(namespaces) > 1:
        namespaces = namespaces[1:]  # the brute-force section always holds the note's first python block
    return [ns[name]() if name == "Solution" else ns[name] for ns in namespaces]


def rand_tree(n, lo=-9, hi=9, distinct=False):
    vals = R.sample(range(lo, hi + 1), n) if distinct else [R.randint(lo, hi) for _ in range(n)]
    if not vals:
        return None
    nodes = [TreeNode(v) for v in vals]
    for i in range(1, n):
        while True:
            p, side = R.randrange(i), R.choice(("left", "right"))
            if getattr(nodes[p], side) is None:
                setattr(nodes[p], side, nodes[i])
                break
    return nodes[0]


def rand_bst(vals):
    root = None
    for v in vals:
        new = TreeNode(v)
        if root is None:
            root = new
            continue
        node = root
        while True:
            side = "left" if v < node.val else "right"
            if getattr(node, side) is None:
                setattr(node, side, new)
                break
            node = getattr(node, side)
    return root


def inorder(root):
    out, stack, node = [], [], root
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        out.append(node.val)
        node = node.right
    return out


def ref_merge(intervals):
    out = []
    for a, b in sorted(intervals):
        if out and a <= out[-1][1]:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return out
