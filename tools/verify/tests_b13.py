"""Mock tests 4-6: brute vs optimized on random inputs, independent references, big inputs."""
import random

from harness import case, run_program
from tests_b10 import agree, mock, timed

R = random.Random(13)


@case("M4Q1")
def _(h):
    brute, opt, _, _ = mock(4, 1)
    agree(brute, opt, lambda: (lambda s: f"{len(s)}\n{s}")("".join(R.choice("01") for _ in range(R.randint(1, 14)))), runs=300)
    timed(opt, "200000\n" + "".join(R.choice("01") for _ in range(200000)), 5)


@case("M4Q2")
def _(h):
    brute, opt, _, _ = mock(4, 2)

    def gen():
        n = R.randint(1, 10)
        pairs = [R.sample(range(1, n + 1), 2) for _ in range(R.randint(0, 8))] if n > 1 else []
        return "\n".join([f"{n} {len(pairs)}"] + [f"{u} {v}" for u, v in pairs])
    agree(brute, opt, gen, runs=300)
    n, m = 2000, 10000
    pairs = [R.sample(range(1, n + 1), 2) for _ in range(m)]
    timed(opt, "\n".join([f"{n} {m}"] + [f"{u} {v}" for u, v in pairs]), 5)
    chain = [f"{i} {i + 1}" for i in range(1, 2000)]  # bipartite path: answer 0
    assert run_program(opt, "\n".join(["2000 1999"] + chain)) == "0"


@case("M4Q3")
def _(h):
    brute, opt, _, _ = mock(4, 3)

    def gen():
        n = R.randint(1, 7)
        roads = [(R.randint(1, n), R.randint(1, n)) for _ in range(R.randint(0, 10))]
        return "\n".join([f"{n} {len(roads)}", " ".join(str(R.randint(1, 9)) for _ in range(n))]
                         + [f"{u} {v}" for u, v in roads])
    agree(brute, opt, gen, runs=300)
    n, m = 100000, 200000
    roads = [(R.randint(1, n), R.randint(1, n)) for _ in range(m)]
    big = "\n".join([f"{n} {m}", " ".join(str(R.randint(1, 10**9)) for _ in range(n))] + [f"{u} {v}" for u, v in roads])
    timed(opt, big, 15)
    cycle = "\n".join(["100000 100000", " ".join(["1"] * 100000)] + [f"{i} {i % 100000 + 1}" for i in range(1, 100001)])
    assert run_program(opt, cycle) == "100000"  # one giant SCC, deep DFS


@case("M5Q1")
def _(h):
    brute, opt, _, _ = mock(5, 1)

    def gen():
        n, k = R.randint(1, 3), R.randint(1, 4)
        return f"{n} {k}\n" + " ".join(str(R.randint(0, 7)) for _ in range(n))
    agree(brute, opt, gen, runs=300)
    timed(opt, "200000 1000000000\n" + " ".join(str(R.randint(0, 10**9)) for _ in range(200000)), 5)


@case("M5Q2")
def _(h):
    brute, opt, _, _ = mock(5, 2)

    def gen():
        n, q = R.randint(1, 12), R.randint(1, 10)
        qs = []
        for _ in range(q):
            l = R.randint(1, n)
            qs.append(f"{l} {R.randint(l, n)}")
        return "\n".join([f"{n} {q}", " ".join(str(R.randint(1, 20)) for _ in range(n))] + qs)
    agree(brute, opt, gen, runs=300)
    n = q = 200000
    qs = []
    for _ in range(q):
        l = R.randint(1, n)
        qs.append(f"{l} {R.randint(l, n)}")
    timed(opt, "\n".join([f"{n} {q}", " ".join(str(R.randint(1, 10**9)) for _ in range(n))] + qs), 10)


@case("M5Q3")
def _(h):
    brute, opt, _, _ = mock(5, 3)

    def gen():
        n = R.randint(1, 8)
        links = [R.sample(range(1, n + 1), 2) for _ in range(R.randint(0, 10))] if n > 1 else []
        return "\n".join([f"{n} {len(links)}"] + [f"{u} {v}" for u, v in links])
    agree(brute, opt, gen, runs=400)
    path = "\n".join(["100000 99999"] + [f"{i} {i + 1}" for i in range(1, 100000)])
    out = run_program(opt, path).split("\n")
    assert out[0] == "99998" and out[1].split()[0] == "2"  # every inner router of a path
    n, m = 100000, 200000
    links = [R.sample(range(1, n + 1), 2) for _ in range(m)]
    timed(opt, "\n".join([f"{n} {m}"] + [f"{u} {v}" for u, v in links]), 15)


@case("M6Q1")
def _(h):
    brute, opt, _, _ = mock(6, 1)
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]

    def gen():
        ps = R.sample(primes, R.randint(1, 5))
        return f"{R.randint(1, 3000)} {len(ps)}\n" + " ".join(map(str, ps))
    agree(brute, opt, gen, runs=200)
    got = int(run_program(opt, f"{10**18} 12\n" + " ".join(map(str, primes))))
    assert 0 < got < 10**18


@case("M6Q2")
def _(h):
    brute, opt, _, _ = mock(6, 2)

    def gen():
        steps = R.sample(range(1, 11), R.randint(1, 4))
        return f"{R.randint(1, 60)} {len(steps)}\n" + " ".join(map(str, steps))
    agree(brute, opt, gen, runs=300)
    timed(opt, f"{10**18} 10\n" + " ".join(map(str, range(1, 11))), 5)


@case("M6Q3")
def _(h):
    brute, opt, _, _ = mock(6, 3)

    def gen():
        n = R.randint(1, 10)
        return f"{n} {R.randint(1, 5)}\n" + " ".join(str(R.randint(1, 6)) for _ in range(n))
    agree(brute, opt, gen, runs=300)
    timed(opt, "10000 10\n" + " ".join(str(R.randint(1, 10**9)) for _ in range(10000)), 10)
