"""Mock tests 4-6: brute vs optimized on the judge's generators, plus known answers on big inputs."""
from harness import case, run_program
from tests_b10 import check_spec, mock

NL = "\n"


@case("M4Q1")
def _(h):
    brute, opt, _, _ = mock(4, 1)
    check_spec("M4Q1", brute, opt, runs=300, limit=5)


@case("M4Q2")
def _(h):
    brute, opt, _, _ = mock(4, 2)
    check_spec("M4Q2", brute, opt, runs=300, limit=5)
    chain = [f"{i} {i + 1}" for i in range(1, 2000)]  # bipartite path: answer 0
    assert run_program(opt, NL.join(["2000 1999"] + chain)) == "0"


@case("M4Q3")
def _(h):
    brute, opt, _, _ = mock(4, 3)
    check_spec("M4Q3", brute, opt, runs=300, limit=15)
    n = 100_000
    cycle = NL.join([f"{n} {n}", " ".join(["1"] * n)] + [f"{i} {i % n + 1}" for i in range(1, n + 1)])
    assert run_program(opt, cycle) == str(n)  # one giant SCC, deep DFS


@case("M5Q1")
def _(h):
    brute, opt, _, _ = mock(5, 1)
    check_spec("M5Q1", brute, opt, runs=300, limit=5)


@case("M5Q2")
def _(h):
    brute, opt, _, _ = mock(5, 2)
    check_spec("M5Q2", brute, opt, runs=300, limit=10)


@case("M5Q3")
def _(h):
    brute, opt, _, _ = mock(5, 3)
    check_spec("M5Q3", brute, opt, runs=400, limit=15)
    path = NL.join(["100000 99999"] + [f"{i} {i + 1}" for i in range(1, 100_000)])
    out = run_program(opt, path).split(NL)
    assert out[0] == "99998" and out[1].split()[0] == "2"  # every inner router of a path


@case("M6Q1")
def _(h):
    brute, opt, _, _ = mock(6, 1)
    check_spec("M6Q1", brute, opt, runs=200, limit=5)
    got = int(run_program(opt, f"{10**18} 12{NL}2 3 5 7 11 13 17 19 23 29 31 37"))
    assert 0 < got < 10**18


@case("M6Q2")
def _(h):
    brute, opt, _, _ = mock(6, 2)
    check_spec("M6Q2", brute, opt, runs=300, limit=5)


@case("M6Q3")
def _(h):
    brute, opt, _, _ = mock(6, 3)
    check_spec("M6Q3", brute, opt, runs=300, limit=10)
