"""Input generators for mock tests 7-10 (see specs.py)."""
from specs import distinct_pairs, ints, lines, path_edges, register


def random_tree(rng, n, weight=None):
    """Edges `u v [w]` of a random tree on 1..n with shuffled labels."""
    labels = list(range(1, n + 1))
    rng.shuffle(labels)
    edges = []
    for i in range(1, n):
        u, v = labels[rng.randrange(i)], labels[i]
        edges.append(f"{u} {v}" + (f" {rng.randint(*weight)}" if weight else ""))
    return edges


def weighted_path(rng, n, weight):
    return [f"{e} {rng.randint(*weight)}" for e in path_edges(n)]


# Mock 7
def boosts(rng, n, m, vmax):
    out = []
    for _ in range(m):
        left = rng.randint(1, n)
        out.append(f"{left} {rng.randint(left, n)} {rng.randint(1, vmax)}")
    return out


def m7q1_small(rng):
    n, m = rng.randint(1, 10), rng.randint(1, 6)
    return lines(f"{n} {m}", boosts(rng, n, m, 5))


def m7q1_large(rng):
    return [lines("200000 200000", boosts(rng, 200_000, 200_000, 10**9))]


def m7q2_small(rng):
    n = rng.randint(1, 10)
    return lines(str(n), ints(rng, n, 1, 6))


def m7q2_large(rng):
    n = 100_000
    return [lines(str(n), ints(rng, n, 1, 10**6)),
            lines(str(n), " ".join(map(str, range(1, n + 1))))]  # increasing: deepest stacks


def lantern(rng, h, w, k):
    cells = [(r, c) for r in range(1, h + 1) for c in range(1, w + 1) if (r, c) not in ((1, 1), (h, w))]
    blocked = rng.sample(cells, min(k, len(cells)))
    return lines(f"{h} {w} {len(blocked)}", [f"{r} {c}" for r, c in blocked])


def m7q3_small(rng):
    return lantern(rng, rng.randint(1, 7), rng.randint(1, 7), rng.randint(0, 6))


def m7q3_large(rng):
    h = w = 100_000
    blocked = set()
    while len(blocked) < 2000:
        cell = (rng.randint(1, h), rng.randint(1, w))
        if cell not in ((1, 1), (h, w)):
            blocked.add(cell)
    return [lines(f"{h} {w} 2000", [f"{r} {c}" for r, c in sorted(blocked)])]


# Mock 8
def m8q1_small(rng):
    n, cap = rng.randint(1, 10), rng.randint(5, 20)
    return lines(f"{n} {cap}", ints(rng, n, 1, cap))


def m8q1_large(rng):
    return [lines("200000 1000000000", ints(rng, 200_000, 1, 10**9))]


def islands(rng, rows, cols, water_share):
    cells = ["~" if rng.random() < water_share else "." for _ in range(rows * cols)]
    s, t = rng.sample(range(rows * cols), 2)
    cells[s], cells[t] = "S", "T"
    return lines(f"{rows} {cols}", ["".join(cells[r * cols:(r + 1) * cols]) for r in range(rows)])


def m8q2_small(rng):
    rows, cols = rng.randint(1, 5), rng.randint(2, 5)
    return islands(rng, rows, cols, rng.random())


def m8q2_large(rng):
    return [islands(rng, 500, 500, 0.5), islands(rng, 500, 500, 0.9)]


def m8q3_small(rng):
    n = rng.randint(1, 8)
    return lines(str(n), ints(rng, n, 0, 5), random_tree(rng, n, (1, 5)))


def m8q3_large(rng):
    n = 200_000
    return [lines(str(n), ints(rng, n, 0, 1000), random_tree(rng, n, (1, 1000))),
            lines(str(n), ints(rng, n, 0, 1000), weighted_path(rng, n, (1, 1000)))]


# Mock 9
def m9q1_small(rng):
    n = rng.randint(1, 12)
    return lines(f"{n} {rng.randint(0, 3)}", ints(rng, n, 1, 9))


def m9q1_large(rng):
    return [lines(f"200000 {rng.randint(0, 50_000)}", ints(rng, 200_000, 1, 10**9))]


def m9q2_small(rng):
    n = rng.randint(2, 8)
    seats = rng.sample(range(1, 31), n)
    return lines(f"{n} {rng.randint(2, n)}", " ".join(map(str, seats)))


def m9q2_large(rng):
    n = 200_000
    seats = rng.sample(range(1, 10**9 + 1), n)
    return [lines(f"{n} 1000", " ".join(map(str, seats))), lines(f"{n} {n}", " ".join(map(str, seats)))]


def gems(rng, n, cap, wmax, vmax):
    return lines(f"{n} {cap}", [f"{rng.randint(1, wmax)} {rng.randint(1, vmax)}" for _ in range(n)])


def m9q3_small(rng):
    return gems(rng, rng.randint(1, 12), rng.randint(1, 60), 20, 20)


def m9q3_large(rng):
    return [gems(rng, 36, rng.randint(10**12, 10**13), 10**12, 10**12)]


# Mock 10
def trays(rng, q, xmax):
    ops = []
    for _ in range(q):
        roll = rng.random()
        ops.append(f"1 {rng.randint(1, xmax)}" if roll < 0.45 else "2" if roll < 0.7 else "3")
    return lines(str(q), ops)


def m10q1_small(rng):
    return trays(rng, rng.randint(1, 12), 9)


def m10q1_large(rng):
    return [trays(rng, 200_000, 10**9)]


def m10q2_small(rng):
    n = rng.randint(2, 8)
    pairs = distinct_pairs(rng, n, rng.randint(1, 10))
    return lines(f"{n} {len(pairs)}", pairs)


def m10q2_large(rng):
    return [lines("200000 200000", distinct_pairs(rng, 200_000, 200_000))]


def queries(rng, n, q):
    return [f"{rng.randint(1, n)} {rng.randint(1, n)}" for _ in range(q)]


def m10q3_small(rng):
    n, q = rng.randint(1, 10), rng.randint(1, 8)
    return lines(f"{n} {q}", random_tree(rng, n, (1, 9)), queries(rng, n, q))


def m10q3_large(rng):
    n = q = 100_000
    return [lines(f"{n} {q}", random_tree(rng, n, (1, 10**9)), queries(rng, n, q)),
            lines(f"{n} {q}", weighted_path(rng, n, (1, 10**9)), queries(rng, n, q))]


for _key, _small, _large in [
    ("M7Q1", m7q1_small, m7q1_large), ("M7Q2", m7q2_small, m7q2_large), ("M7Q3", m7q3_small, m7q3_large),
    ("M8Q1", m8q1_small, m8q1_large), ("M8Q2", m8q2_small, m8q2_large), ("M8Q3", m8q3_small, m8q3_large),
    ("M9Q1", m9q1_small, m9q1_large), ("M9Q2", m9q2_small, m9q2_large), ("M9Q3", m9q3_small, m9q3_large),
    ("M10Q1", m10q1_small, m10q1_large), ("M10Q2", m10q2_small, m10q2_large),
    ("M10Q3", m10q3_small, m10q3_large),
]:
    register(_key, _small, _large)
