"""Backtracking sheet notes: Sudoku, Combination Sum I/II/III, N-Queens II, Palindrome Partitioning,
Expression Add Operators.

Brute and optimized must agree on LeetCode's examples and on random small inputs; when several
answers are valid (Sudoku with random blanks, list order of combinations) a validator or a
canonical sort is used instead of equality.
"""
import copy
import random

from harness import case
from tests_b10 import timed_call

R = random.Random(20)


def both(h, num):
    brute, opt = h.lc_all(num, "Solution")
    return brute["Solution"](), opt["Solution"]()


def canon(lists):
    return sorted(sorted(x) for x in lists)


def canon_ordered(lists):
    """Canonical form for answers whose inner order matters (partitions) but outer order does not."""
    return sorted(lists)


SUDOKU_EXAMPLE = [
    "53..7....", "6..195...", ".98....6.", "8...6...3", "4..8.3..1",
    "7...2...6", ".6....28.", "...419..5", "....8..79",
]
SUDOKU_EXAMPLE_SOLVED = [
    "534678912", "672195348", "198342567", "859761423", "426853791",
    "713924856", "961537284", "287419635", "345286179",
]
SUDOKU_HARD = [
    "8........", "..36.....", ".7..9.2..", ".5...7...", "....457..",
    "...1...3.", "..1....68", "..85...1.", ".9....4..",
]


def to_board(rows):
    return [list(r) for r in rows]


def is_solution(puzzle, board):
    digits = set("123456789")
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] != "." and puzzle[r][c] != board[r][c]:
                return False
    units = [[(r, c) for c in range(9)] for r in range(9)]
    units += [[(r, c) for r in range(9)] for c in range(9)]
    units += [[(br + i // 3, bc + i % 3) for i in range(9)] for br in (0, 3, 6) for bc in (0, 3, 6)]
    return all({board[r][c] for r, c in unit} == digits for unit in units)


def random_puzzle(blanks):
    digits = list("123456789")
    R.shuffle(digits)
    bands = R.sample(range(3), 3)
    rows = [b * 3 + i for b in bands for i in R.sample(range(3), 3)]
    stacks = R.sample(range(3), 3)
    cols = [s * 3 + i for s in stacks for i in R.sample(range(3), 3)]
    grid = [[digits[(r * 3 + r // 3 + c) % 9] for c in cols] for r in rows]
    for cell in R.sample(range(81), blanks):
        grid[cell // 9][cell % 9] = "."
    return grid


@case(37)
def _(h):
    brute, opt = both(h, 37)
    for solver in (brute, opt):
        board = to_board(SUDOKU_EXAMPLE)
        assert solver.solveSudoku(board) is None
        assert ["".join(r) for r in board] == SUDOKU_EXAMPLE_SOLVED
    for _ in range(100):
        puzzle = random_puzzle(R.randint(20, 45))
        b1, b2 = copy.deepcopy(puzzle), copy.deepcopy(puzzle)
        brute.solveSudoku(b1)
        opt.solveSudoku(b2)
        assert is_solution(puzzle, b1) and is_solution(puzzle, b2), puzzle
    hard = to_board(SUDOKU_HARD)
    timed_call(lambda: opt.solveSudoku(hard), 2)
    assert is_solution(to_board(SUDOKU_HARD), hard)


@case(39)
def _(h):
    brute, opt = both(h, 39)
    assert canon(opt.combinationSum([2, 3, 6, 7], 7)) == [[2, 2, 3], [7]]
    assert canon(opt.combinationSum([2, 3, 5], 8)) == [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
    assert opt.combinationSum([2], 1) == []
    for _ in range(200):
        cands = R.sample(range(2, 15), R.randint(1, 5))
        target = R.randint(1, 16)
        got = opt.combinationSum(cands, target)
        assert canon(brute.combinationSum(cands, target)) == canon(got), (cands, target)
        assert len(got) == len({tuple(sorted(x)) for x in got})
    timed_call(lambda: opt.combinationSum(list(range(2, 41)), 40), 2)


@case(40)
def _(h):
    brute, opt = both(h, 40)
    assert canon(opt.combinationSum2([10, 1, 2, 7, 6, 1, 5], 8)) == [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]
    assert canon(opt.combinationSum2([2, 5, 2, 1, 2], 5)) == [[1, 2, 2], [5]]
    for _ in range(300):
        cands = [R.randint(1, 8) for _ in range(R.randint(1, 12))]
        target = R.randint(1, 20)
        got = opt.combinationSum2(list(cands), target)
        assert canon(brute.combinationSum2(cands, target)) == canon(got), (cands, target)
        assert len(got) == len({tuple(sorted(x)) for x in got})
    assert opt.combinationSum2([1] * 100, 30) == [[1] * 30]
    big = [R.randint(1, 50) for _ in range(100)]
    timed_call(lambda: opt.combinationSum2(big, 30), 2)


@case(52)
def _(h):
    brute, opt = both(h, 52)
    expected = [1, 0, 0, 2, 10, 4, 40, 92, 352]
    # the input space is only n = 1..9, so check all of it instead of random sampling
    for n, want in enumerate(expected, start=1):
        assert opt.totalNQueens(n) == want, n
        assert brute.totalNQueens(n) == want, n
    timed_call(lambda: opt.totalNQueens(9), 1)


@case(131)
def _(h):
    brute, opt = both(h, 131)
    assert canon_ordered(opt.partition("aab")) == [["a", "a", "b"], ["aa", "b"]]
    assert opt.partition("a") == [["a"]]
    for _ in range(300):
        s = "".join(R.choice("ab") for _ in range(R.randint(1, 10)))
        assert canon_ordered(brute.partition(s)) == canon_ordered(opt.partition(s)), s
    assert len(opt.partition("a" * 16)) == 2 ** 15
    timed_call(lambda: opt.partition("a" * 16), 2)


@case(216)
def _(h):
    brute, opt = both(h, 216)
    assert opt.combinationSum3(3, 7) == [[1, 2, 4]]
    assert canon(opt.combinationSum3(3, 9)) == [[1, 2, 6], [1, 3, 5], [2, 3, 4]]
    assert opt.combinationSum3(4, 1) == []
    # every legal input (k in 2..9, n in 1..60) is cheap, so check them all
    for k in range(2, 10):
        for n in range(1, 61):
            assert canon(brute.combinationSum3(k, n)) == canon(opt.combinationSum3(k, n)), (k, n)


@case(282)
def _(h):
    brute, opt = both(h, 282)
    assert sorted(opt.addOperators("123", 6)) == ["1*2*3", "1+2+3"]
    assert sorted(opt.addOperators("232", 8)) == ["2*3+2", "2+3*2"]
    assert opt.addOperators("3456237490", 9191) == []
    assert sorted(opt.addOperators("105", 5)) == ["1*0+5", "10-5"]
    assert sorted(opt.addOperators("00", 0)) == ["0*0", "0+0", "0-0"]
    for _ in range(200):
        num = "".join(R.choice("0123456789") for _ in range(R.randint(1, 6)))
        # digit sum and the whole number are always reachable, so many cases have non-empty answers
        target = R.choice((R.randint(-50, 100), sum(map(int, num)), int(num)))
        assert sorted(brute.addOperators(num, target)) == sorted(opt.addOperators(num, target)), (num, target)
    timed_call(lambda: opt.addOperators("1234567890", 45), 5)
