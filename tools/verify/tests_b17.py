"""Mock tests 7-10: brute vs optimized on the judge's generators, sample outputs, big inputs."""
from harness import case, run_program
from tests_b10 import check_spec, mock

NL = "\n"
MOCKS_7_10 = {  # key: (random runs, timing limit in seconds with VERIFY_TIMING=1)
    "M7Q1": (300, 5), "M7Q2": (300, 5), "M7Q3": (200, 10),
    "M8Q1": (200, 5), "M8Q2": (200, 5), "M8Q3": (300, 10),
    "M9Q1": (300, 5), "M9Q2": (300, 5), "M9Q3": (200, 10),
    "M10Q1": (300, 5), "M10Q2": (200, 5), "M10Q3": (300, 10),
}


def make_case(key, runs, limit):
    test, q = (int(x) for x in key[1:].split("Q"))

    @case(key)
    def _(h):
        brute, opt, sample_in, sample_out = mock(test, q)  # mock() already checks the optimized sample
        assert run_program(brute, sample_in) == sample_out, "brute force fails the sample"
        check_spec(key, brute, opt, runs=runs, limit=limit)


for _key, (_runs, _limit) in MOCKS_7_10.items():
    make_case(_key, _runs, _limit)


@case("M7Q3-empty")
def _(h):
    _, opt, _, _ = mock(7, 3)
    assert run_program(opt, "3 3 0") == "6"  # C(4, 2), no fences
    assert run_program(opt, f"2 2 2{NL}1 2{NL}2 1") == "0"  # both routes fenced


@case("M10Q3-path")
def _(h):
    _, opt, _, _ = mock(10, 3)
    n = 100_000
    roads = [f"{i} {i + 1} {i}" for i in range(1, n)]  # road i has class i
    out = run_program(opt, NL.join([f"{n} 2"] + roads + [f"1 {n}", "5 9"])).split()
    assert out == [str(n - 1), "8"]
