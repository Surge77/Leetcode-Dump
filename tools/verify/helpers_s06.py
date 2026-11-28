"""Shared helpers for the tests_s06_*.py checks (Graph traversal notes: ladders, flood fills, graph cloning, Union-Find, weighted ratios).
"""
import copy
import itertools
import math
import random

from harness import case
from tests_b10 import timed_call

R = random.Random(606)
EMPTY = 2**31 - 1


def both(h, num):
    brute, opt = h.lc_all(num, "Solution")
    return brute["Solution"](), opt["Solution"]()


def random_tree_edges(n):
    labels = list(range(n))
    R.shuffle(labels)
    return [[labels[R.randrange(i)], labels[i]] for i in range(1, n)]


def grid_neighbours(r, c):
    return ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1))


def serpentine(size, open_to_border):
    """Snake of 'O's winding through the interior: one region, ~size²/2 cells long."""
    board = [["X"] * size for _ in range(size)]
    for r in range(1, size - 1, 2):
        for c in range(1, size - 1):
            board[r][c] = "O"
        if r + 2 < size - 1:
            board[r + 1][size - 2 if (r // 2) % 2 == 0 else 1] = "O"
    if open_to_border:
        board[1][0] = "O"
    return board


def build_graph(node_cls, adj):
    nodes = [node_cls(i + 1) for i in range(len(adj))]
    for node, nbs in zip(nodes, adj):
        node.neighbors = [nodes[v - 1] for v in nbs]
    return nodes[0] if nodes else None


def graph_to_adj(start):
    """(adjacency list by value, ids of all nodes reachable from start)."""
    if start is None:
        return [], set()
    seen, stack = {id(start): start}, [start]
    while stack:
        for nb in stack.pop().neighbors:
            if id(nb) not in seen:
                seen[id(nb)] = nb
                stack.append(nb)
    nodes = sorted(seen.values(), key=lambda nd: nd.val)
    assert [nd.val for nd in nodes] == list(range(1, len(nodes) + 1)), "one node per value"
    return [[nb.val for nb in nd.neighbors] for nd in nodes], set(seen)


def random_connected_adj(n):
    edges = {(R.randrange(i), i) for i in range(1, n)}
    if n > 1:
        for _ in range(R.randint(0, n)):
            a, b = sorted(R.sample(range(n), 2))
            edges.add((a, b))
    adj = [[] for _ in range(n)]
    for a, b in sorted(edges):
        adj[a].append(b + 1)
        adj[b].append(a + 1)
    for nbs in adj:
        R.shuffle(nbs)
    return adj


def ratios_match(xs, ys):
    return len(xs) == len(ys) and all(math.isclose(x, y, rel_tol=1e-9) for x, y in zip(xs, ys))
