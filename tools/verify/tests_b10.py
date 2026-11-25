"""Mock tests 1-3: brute vs optimized on the judge's generators, independent references, big inputs."""
import os
import random
import re
import sys
import time
from collections import deque
from typing import Deque, Set, Tuple

from harness import REPO, blocks_of, case, run_program

sys.path.insert(0, str(REPO / "tools" / "judge"))
from specs import SPECS  # noqa: E402

R = random.Random(10)
IN_RE = re.compile(r"\*\*Sample Input\*\*\s*```text\n(.*?)```", re.S)
OUT_RE = re.compile(r"\*\*Sample Output\*\*\s*```text\n(.*?)```", re.S)


def mock(test, q):
    """(brute, optimized, sample_in, sample_out): code from solutions/, sample from the statement."""
    folder = REPO / "Infosys_SP_DSE" / f"Mock_Test_{test}"
    statement = next(folder.glob(f"Q{q}_*.md"))
    text = statement.read_text(encoding="utf-8")
    brute, opt = blocks_of(folder / "solutions" / statement.name)
    found_in, found_out = IN_RE.search(text), OUT_RE.search(text)
    assert found_in and found_out, f"{statement.name}: no sample input/output block"
    sample_in, sample_out = found_in.group(1), found_out.group(1).strip()
    assert run_program(opt, sample_in) == sample_out, "optimized fails sample"
    return brute, opt, sample_in, sample_out


def agree(brute, opt, gen, runs=200):
    for _ in range(runs):
        inp = gen()
        b, o = run_program(brute, inp), run_program(opt, inp)
        assert b == o, (inp, b, o)


def check_spec(key, brute, opt, runs, limit):
    """Brute == optimized on the spec's small inputs; time the optimized one on its large inputs."""
    spec = SPECS[key]
    agree(brute, opt, lambda: spec.small(R), runs)
    for big in spec.large(R):
        timed(opt, big, limit)


def timed(opt, inp, limit):
    timed_call(lambda: run_program(opt, inp), limit)


def timed_call(fn, limit):
    """Run fn once at max constraints; print the time, enforce `limit` only with VERIFY_TIMING=1."""
    t = time.perf_counter()
    fn()
    dt = time.perf_counter() - t
    print(f"    max-constraint run: {dt:.2f}s")
    if os.environ.get("VERIFY_TIMING") == "1":
        assert dt < limit, dt


@case("M1Q1")
def _(h):
    brute, opt, sin, _ = mock(1, 1)
    assert run_program(brute, sin) == "5"
    check_spec("M1Q1", brute, opt, runs=200, limit=5)


@case("M1Q2")
def _(h):
    brute, opt, _, _ = mock(1, 2)
    assert run_program(opt, "3 1\n5 6 7") == "7"
    check_spec("M1Q2", brute, opt, runs=200, limit=10)


@case("M1Q3")
def _(h):
    brute, opt, _, _ = mock(1, 3)
    check_spec("M1Q3", brute, opt, runs=300, limit=15)


def min_swaps_bfs(s):
    """True minimum swaps to group the 1s on a circle, by BFS over strings (tiny n only)."""
    n, k = len(s), s.count("1")
    base = "1" * k + "0" * (n - k)
    targets = {base[i:] + base[:i] for i in range(n)}
    dist, q = {s: 0}, deque([s])
    while q:
        cur = q.popleft()
        if cur in targets:
            return dist[cur]
        for i in range(n):
            for j in range(i + 1, n):
                if cur[i] != cur[j]:
                    nxt = list(cur)
                    nxt[i], nxt[j] = nxt[j], nxt[i]
                    nxt = "".join(nxt)
                    if nxt not in dist:
                        dist[nxt] = dist[cur] + 1
                        q.append(nxt)


@case("M2Q1")
def _(h):
    brute, opt, _, _ = mock(2, 1)
    spec = SPECS["M2Q1"]
    for _ in range(150):
        inp = spec.small(R)
        want = str(min_swaps_bfs(inp.split()[1]))
        assert run_program(brute, inp) == want and run_program(opt, inp) == want, (inp, want)
    for big in spec.large(R):
        timed(opt, big, 5)


@case("M2Q2")
def _(h):
    brute, opt, _, _ = mock(2, 2)
    check_spec("M2Q2", brute, opt, runs=300, limit=15)


def treasure_bfs(grid):
    """Independent reference: BFS over (cell, collected-treasure mask)."""
    r, c = len(grid), len(grid[0])
    tid = {}
    for i in range(r):
        for j in range(c):
            if grid[i][j] == "T":
                tid[(i, j)] = len(tid)
    full = (1 << len(tid)) - 1
    s = next((i, j) for i in range(r) for j in range(c) if grid[i][j] == "S")
    start: Tuple[int, int, int] = (s[0], s[1], 0)
    seen: Set[Tuple[int, int, int]] = {start}
    q: Deque[Tuple[Tuple[int, int, int], int]] = deque([(start, 0)])
    while q:
        (i, j, mask), d = q.popleft()
        if mask == full:
            return d
        for x, y in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= x < r and 0 <= y < c and grid[x][y] != "#":
                nm = mask | (1 << tid[(x, y)] if (x, y) in tid else 0)
                if (x, y, nm) not in seen:
                    seen.add((x, y, nm))
                    q.append(((x, y, nm), d + 1))
    return -1


@case("M2Q3")
def _(h):
    brute, opt, _, _ = mock(2, 3)
    spec = SPECS["M2Q3"]
    for _ in range(200):
        inp = spec.small(R)
        want = str(treasure_bfs(inp.split("\n")[1:]))
        assert run_program(brute, inp) == want and run_program(opt, inp) == want, (inp, want)
    for big in spec.large(R):
        timed(opt, big, 15)


@case("M3Q1")
def _(h):
    brute, opt, _, _ = mock(3, 1)
    check_spec("M3Q1", brute, opt, runs=100, limit=5)


@case("M3Q2")
def _(h):
    brute, opt, _, _ = mock(3, 2)
    check_spec("M3Q2", brute, opt, runs=300, limit=20)


@case("M3Q3")
def _(h):
    brute, opt, _, _ = mock(3, 3)
    check_spec("M3Q3", brute, opt, runs=60, limit=10)
