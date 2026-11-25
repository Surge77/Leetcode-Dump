"""Input generators for mock tests 1-6 (see specs.py)."""
from specs import bits, distinct_pairs, ints, lines, path_edges, ranges, register

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]


# Mock 1
def m1q1_small(rng):
    n = rng.randint(1, 12)
    return lines(f"{n} {rng.randint(1, 10)}", ints(rng, n, 1, 30))


def m1q1_large(rng):
    return [lines("200000 1000000000", ints(rng, 200_000, 1, 10**9))]


def m1q2_small(rng):
    n = rng.randint(1, 12)
    return lines(f"{n} {rng.randint(1, 9)}", ints(rng, n, 0, 50))


def m1q2_large(rng):
    return [lines("1000 1000", ints(rng, 1000, 0, 10**9))]


def ticker(rng, n, q, lo, hi, update_share):
    ops = []
    for _ in range(q):
        if rng.random() < update_share:
            ops.append(f"1 {rng.randint(1, n)} {rng.randint(lo, hi)}")
        else:
            left = rng.randint(1, n)
            ops.append(f"2 {left} {rng.randint(left, n)}")
    return lines(f"{n} {q}", ints(rng, n, lo, hi), ops)


def m1q3_small(rng):
    return ticker(rng, rng.randint(1, 10), rng.randint(1, 12), -9, 9, 0.4)


def m1q3_large(rng):
    return [ticker(rng, 100_000, 100_000, -10**9, 10**9, 0.5)]


# Mock 2
def m2q1_small(rng):
    s = bits(rng, rng.randint(1, 8))
    return lines(str(len(s)), s)


def m2q1_large(rng):
    return [lines("200000", bits(rng, 200_000))]


def m2q2_small(rng):
    n, m = rng.randint(1, 6), rng.randint(0, 8)
    roads = [f"{rng.randint(1, n)} {rng.randint(1, n)} {rng.randint(1, 20)}" for _ in range(m)]
    return lines(f"{n} {m}", roads)


def m2q2_large(rng):
    n, m = 100_000, 200_000
    roads = [f"{rng.randint(1, n)} {rng.randint(1, n)} {rng.randint(1, 10**9)}" for _ in range(m)]
    return [lines(f"{n} {m}", roads)]


def treasure_grid(rng, r, c, pool, specials):
    cells = [rng.choice(pool) for _ in range(r * c)]
    spots = rng.sample(range(r * c), min(r * c, specials))
    cells[spots[0]] = "S"
    for t in spots[1:]:
        cells[t] = "T"
    return lines(f"{r} {c}", ["".join(cells[i * c:(i + 1) * c]) for i in range(r)])


def m2q3_small(rng):
    return treasure_grid(rng, rng.randint(1, 5), rng.randint(1, 5), "..#", rng.randint(1, 5))


def m2q3_large(rng):
    return [treasure_grid(rng, 50, 50, "....#", 13)]


# Mock 3
def m3q1_small(rng):
    t = rng.randint(1, 5)
    return lines(str(t), [str(rng.randint(1, 400)) for _ in range(t)])


def m3q1_large(rng):
    return [lines("100000", [str(rng.randint(1, 10**12)) for _ in range(100_000)])]


def m3q2_small(rng):
    k = rng.randint(1, 5)
    return lines(f"{k} {rng.randint(1, 15)}", [f"{rng.randint(0, 10)} {rng.randint(1, 5)}" for _ in range(k)])


def m3q2_large(rng):
    machines = [f"{rng.randint(0, 10**9)} {rng.randint(1, 10**9)}" for _ in range(100_000)]
    return [lines("100000 1000000000", machines)]


def m3q3_small(rng):
    lo = rng.randint(1, 3000)
    return f"{lo} {lo + rng.randint(0, 3000)} {rng.randint(1, 30)}"


def m3q3_large(rng):
    return [f"1 {10**18} 97"]


# Mock 4
def m4q1_small(rng):
    s = bits(rng, rng.randint(1, 14))
    return lines(str(len(s)), s)


def m4q1_large(rng):
    return [lines("200000", bits(rng, 200_000))]


def m4q2_small(rng):
    n = rng.randint(1, 10)
    edges = distinct_pairs(rng, n, rng.randint(0, 8))
    return lines(f"{n} {len(edges)}", edges)


def m4q2_large(rng):
    return [lines("2000 10000", distinct_pairs(rng, 2000, 10_000)),
            lines("2000 1999", path_edges(2000))]  # bipartite path: answer 0


def m4q3_small(rng):
    n = rng.randint(1, 7)
    roads = [f"{rng.randint(1, n)} {rng.randint(1, n)}" for _ in range(rng.randint(0, 10))]
    return lines(f"{n} {len(roads)}", ints(rng, n, 1, 9), roads)


def m4q3_large(rng):
    n, m = 100_000, 200_000
    roads = [f"{rng.randint(1, n)} {rng.randint(1, n)}" for _ in range(m)]
    cycle = [f"{i} {i % n + 1}" for i in range(1, n + 1)]  # one giant SCC: deep DFS
    return [lines(f"{n} {m}", ints(rng, n, 1, 10**9), roads),
            lines(f"{n} {n}", " ".join(["1"] * n), cycle)]


# Mock 5
def m5q1_small(rng):
    n = rng.randint(1, 3)
    return lines(f"{n} {rng.randint(1, 4)}", ints(rng, n, 0, 7))


def m5q1_large(rng):
    return [lines("200000 1000000000", ints(rng, 200_000, 0, 10**9))]


def m5q2_small(rng):
    n, q = rng.randint(1, 12), rng.randint(1, 10)
    return lines(f"{n} {q}", ints(rng, n, 1, 20), ranges(rng, n, q))


def m5q2_large(rng):
    n = q = 200_000
    return [lines(f"{n} {q}", ints(rng, n, 1, 10**9), ranges(rng, n, q))]


def m5q3_small(rng):
    n = rng.randint(1, 8)
    links = distinct_pairs(rng, n, rng.randint(0, 10))
    return lines(f"{n} {len(links)}", links)


def m5q3_large(rng):
    return [lines("100000 99999", path_edges(100_000)),  # every inner router is critical
            lines("100000 200000", distinct_pairs(rng, 100_000, 200_000))]


# Mock 6
def m6q1_small(rng):
    ps = rng.sample(PRIMES, rng.randint(1, 5))
    return lines(f"{rng.randint(1, 3000)} {len(ps)}", " ".join(map(str, ps)))


def m6q1_large(rng):
    return [lines(f"{10**18} 12", " ".join(map(str, PRIMES)))]


def m6q2_small(rng):
    steps = rng.sample(range(1, 11), rng.randint(1, 4))
    return lines(f"{rng.randint(1, 60)} {len(steps)}", " ".join(map(str, steps)))


def m6q2_large(rng):
    return [lines(f"{10**18} 10", " ".join(map(str, range(1, 11))))]


def m6q3_small(rng):
    n = rng.randint(1, 10)
    return lines(f"{n} {rng.randint(1, 5)}", ints(rng, n, 1, 6))


def m6q3_large(rng):
    return [lines("10000 10", ints(rng, 10_000, 1, 10**9))]


for _key, _small, _large in [
    ("M1Q1", m1q1_small, m1q1_large), ("M1Q2", m1q2_small, m1q2_large), ("M1Q3", m1q3_small, m1q3_large),
    ("M2Q1", m2q1_small, m2q1_large), ("M2Q2", m2q2_small, m2q2_large), ("M2Q3", m2q3_small, m2q3_large),
    ("M3Q1", m3q1_small, m3q1_large), ("M3Q2", m3q2_small, m3q2_large), ("M3Q3", m3q3_small, m3q3_large),
    ("M4Q1", m4q1_small, m4q1_large), ("M4Q2", m4q2_small, m4q2_large), ("M4Q3", m4q3_small, m4q3_large),
    ("M5Q1", m5q1_small, m5q1_large), ("M5Q2", m5q2_small, m5q2_large), ("M5Q3", m5q3_small, m5q3_large),
    ("M6Q1", m6q1_small, m6q1_large), ("M6Q2", m6q2_small, m6q2_large), ("M6Q3", m6q3_small, m6q3_large),
]:
    register(_key, _small, _large)
