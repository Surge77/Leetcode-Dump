import os
import random
import re
import time
from collections import deque
from itertools import permutations

from harness import REPO, blocks_of, case, run_program

R = random.Random(10)
IN_RE = re.compile(r"\*\*Sample Input\*\*\s*```text\n(.*?)```", re.S)
OUT_RE = re.compile(r"\*\*Sample Output\*\*\s*```text\n(.*?)```", re.S)


def mock(test, q):
    path = next((REPO / "Infosys_SP_DSE" / f"Mock_Test_{test}").glob(f"Q{q}_*.md"))
    text = path.read_text(encoding="utf-8")
    brute, opt = blocks_of(path)
    sample_in, sample_out = IN_RE.search(text).group(1), OUT_RE.search(text).group(1).strip()
    assert run_program(opt, sample_in) == sample_out, "optimized fails sample"
    return brute, opt, sample_in, sample_out


def agree(brute, opt, gen, runs=200):
    for _ in range(runs):
        inp = gen()
        b, o = run_program(brute, inp), run_program(opt, inp)
        assert b == o, (inp, b, o)


def timed(opt, inp, limit):
    t = time.perf_counter()
    run_program(opt, inp)
    dt = time.perf_counter() - t
    print(f"    max-constraint run: {dt:.2f}s")
    if os.environ.get("VERIFY_TIMING") == "1":
        assert dt < limit, dt


@case("M1Q1")
def _(h):
    brute, opt, sin, _ = mock(1, 1)
    assert run_program(brute, sin) == "5"

    def gen():
        n, k = R.randint(1, 12), R.randint(1, 10)
        return f"{n} {k}\n" + " ".join(str(R.randint(1, 30)) for _ in range(n))
    agree(brute, opt, gen)
    timed(opt, "200000 1000000000\n" + " ".join(str(R.randint(1, 10**9)) for _ in range(200000)), 5)


@case("M1Q2")
def _(h):
    brute, opt, _, _ = mock(1, 2)

    def gen():
        n, m = R.randint(1, 12), R.randint(1, 9)
        return f"{n} {m}\n" + " ".join(str(R.randint(0, 50)) for _ in range(n))
    agree(brute, opt, gen)
    assert run_program(opt, "3 1\n5 6 7") == "7"
    timed(opt, "1000 1000\n" + " ".join(str(R.randint(0, 10**9)) for _ in range(1000)), 10)


@case("M1Q3")
def _(h):
    brute, opt, _, _ = mock(1, 3)

    def gen():
        n, q = R.randint(1, 10), R.randint(1, 12)
        lines = [f"{n} {q}", " ".join(str(R.randint(-9, 9)) for _ in range(n))]
        for _ in range(q):
            if R.random() < 0.4:
                lines.append(f"1 {R.randint(1, n)} {R.randint(-9, 9)}")
            else:
                l = R.randint(1, n)
                lines.append(f"2 {l} {R.randint(l, n)}")
        return "\n".join(lines)
    agree(brute, opt, gen, runs=300)
    n = q = 100000
    lines = [f"{n} {q}", " ".join(str(R.randint(-10**9, 10**9)) for _ in range(n))]
    for _ in range(q):
        l = R.randint(1, n)
        lines.append(f"1 {l} {R.randint(-10**9, 10**9)}" if R.random() < 0.5 else f"2 {l} {R.randint(l, n)}")
    timed(opt, "\n".join(lines), 15)


@case("M2Q1")
def _(h):
    brute, opt, _, _ = mock(2, 1)

    def bfs_answer(s):  # true minimum swaps by BFS over strings (tiny n only)
        n, k = len(s), s.count("1")
        targets = {("1" * k + "0" * (n - k))[i:] + ("1" * k + "0" * (n - k))[:i] for i in range(n)}
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

    for _ in range(150):
        s = "".join(R.choice("01") for _ in range(R.randint(1, 8)))
        inp = f"{len(s)}\n{s}"
        want = str(bfs_answer(s))
        assert run_program(brute, inp) == want and run_program(opt, inp) == want, (s, want)
    timed(opt, "200000\n" + "".join(R.choice("01") for _ in range(200000)), 5)


@case("M2Q2")
def _(h):
    brute, opt, _, _ = mock(2, 2)

    def gen():
        n, m = R.randint(1, 6), R.randint(0, 8)
        edges = [f"{R.randint(1, n)} {R.randint(1, n)} {R.randint(1, 20)}" for _ in range(m)]
        return "\n".join([f"{n} {m}"] + edges)
    agree(brute, opt, gen, runs=300)
    n, m = 100000, 200000
    edges = [f"{R.randint(1, n)} {R.randint(1, n)} {R.randint(1, 10**9)}" for _ in range(m)]
    timed(opt, "\n".join([f"{n} {m}"] + edges), 15)


@case("M2Q3")
def _(h):
    brute, opt, _, _ = mock(2, 3)

    def state_bfs(grid):  # independent: BFS over (cell, collected mask)
        r, c = len(grid), len(grid[0])
        tid = {}
        for i in range(r):
            for j in range(c):
                if grid[i][j] == "T":
                    tid[(i, j)] = len(tid)
        full = (1 << len(tid)) - 1
        s = next((i, j) for i in range(r) for j in range(c) if grid[i][j] == "S")
        start = (s[0], s[1], 0)
        seen, q = {start}, deque([(start, 0)])
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

    for _ in range(200):
        r, c = R.randint(1, 5), R.randint(1, 5)
        cells = [R.choice("..#") for _ in range(r * c)]
        idx = R.sample(range(r * c), min(r * c, R.randint(1, 5)))
        cells[idx[0]] = "S"
        for t in idx[1:]:
            cells[t] = "T"
        grid = ["".join(cells[i * c:(i + 1) * c]) for i in range(r)]
        inp = f"{r} {c}\n" + "\n".join(grid)
        want = str(state_bfs(grid))
        assert run_program(brute, inp) == want and run_program(opt, inp) == want, (grid, want)
    cells = [R.choice("....#") for _ in range(2500)]
    spots = R.sample(range(2500), 13)
    cells[spots[0]] = "S"
    for t in spots[1:]:
        cells[t] = "T"
    timed(opt, "50 50\n" + "\n".join("".join(cells[i * 50:(i + 1) * 50]) for i in range(50)), 15)


@case("M3Q1")
def _(h):
    brute, opt, _, _ = mock(3, 1)

    def gen():
        t = R.randint(1, 5)
        return f"{t}\n" + "\n".join(str(R.randint(1, 400)) for _ in range(t))
    agree(brute, opt, gen, runs=100)
    timed(opt, "100000\n" + "\n".join(str(R.randint(1, 10**12)) for _ in range(100000)), 5)


@case("M3Q2")
def _(h):
    brute, opt, _, _ = mock(3, 2)

    def gen():
        k, x = R.randint(1, 5), R.randint(1, 15)
        return f"{k} {x}\n" + "\n".join(f"{R.randint(0, 10)} {R.randint(1, 5)}" for _ in range(k))
    agree(brute, opt, gen, runs=300)
    k = 100000
    timed(opt, f"{k} 1000000000\n" + "\n".join(f"{R.randint(0, 10**9)} {R.randint(1, 10**9)}" for _ in range(k)), 20)


@case("M3Q3")
def _(h):
    brute, opt, _, _ = mock(3, 3)

    def gen():
        l = R.randint(1, 3000)
        return f"{l} {l + R.randint(0, 3000)} {R.randint(1, 30)}"
    agree(brute, opt, gen, runs=60)
    timed(opt, f"1 {10**18} 97", 10)
