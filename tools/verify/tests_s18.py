"""A2Z string basics: atoi, frequency sort, rotation, parentheses depth, substring beauty, odd prefix."""
import random

from harness import case
from tests_b10 import timed_call

R = random.Random(1818)


def both(h, num):
    brute, opt = h.lc_all(num, "Solution")
    return brute["Solution"](), opt["Solution"]()


def random_vps(pairs, fillers=""):
    """Random valid parentheses string with `pairs` pairs, optional filler characters mixed in."""
    out, open_count, closed = [], 0, 0
    while closed < pairs:
        if fillers and R.random() < 0.3:
            out.append(R.choice(fillers))
            continue
        if open_count < pairs and (open_count == closed or R.random() < 0.5):
            out.append("(")
            open_count += 1
        else:
            out.append(")")
            closed += 1
    return "".join(out)


@case(8)
def _(h):
    brute, opt = both(h, 8)
    for s, want in [("42", 42), ("   -042", -42), ("1337c0d3", 1337), ("0-1", 0), ("words and 987", 0),
                    ("-91283472332", -2**31), ("2147483648", 2**31 - 1), ("", 0), ("+-12", 0), ("+ 1", 0)]:
        assert brute.myAtoi(s) == want and opt.myAtoi(s) == want, (s, want)
    alphabet = " +-0123456789a."
    for _ in range(2000):
        s = "".join(R.choice(alphabet) for _ in range(R.randint(0, 15)))
        assert brute.myAtoi(s) == opt.myAtoi(s), s
    for _ in range(300):
        s = " " * R.randint(0, 3) + R.choice(["", "+", "-"]) + "".join(R.choice("0123456789") for _ in range(R.randint(1, 14)))
        assert brute.myAtoi(s) == opt.myAtoi(s), s


def valid_freq_sort(s, out):
    if sorted(s) != sorted(out):
        return False
    groups = []
    for ch in out:
        if groups and groups[-1][0] == ch:
            groups[-1][1] += 1
        else:
            groups.append([ch, 1])
    chars = [g[0] for g in groups]
    counts = [g[1] for g in groups]
    return len(set(chars)) == len(chars) and counts == sorted(counts, reverse=True)


@case(451)
def _(h):
    brute, opt = both(h, 451)
    assert opt.frequencySort("tree") in ("eert", "eetr")
    assert opt.frequencySort("cccaaa") in ("cccaaa", "aaaccc")
    assert opt.frequencySort("Aabb") in ("bbAa", "bbaA")
    for _ in range(300):
        s = "".join(R.choice("aAbB01c") for _ in range(R.randint(1, 20)))
        assert valid_freq_sort(s, brute.frequencySort(s)), s
        assert valid_freq_sort(s, opt.frequencySort(s)), s
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    big = "".join(R.choice(alphabet) for _ in range(500_000))
    assert valid_freq_sort(big, opt.frequencySort(big))
    timed_call(lambda: opt.frequencySort(big), 2)


@case(796)
def _(h):
    brute, opt = both(h, 796)
    assert opt.rotateString("abcde", "cdeab") is True
    assert opt.rotateString("abcde", "abced") is False
    assert opt.rotateString("a", "ab") is False and brute.rotateString("a", "ab") is False
    for _ in range(1000):
        s = "".join(R.choice("ab") for _ in range(R.randint(1, 8)))
        if R.random() < 0.5:
            k = R.randrange(len(s))
            goal = s[k:] + s[:k]
        else:
            goal = "".join(R.choice("ab") for _ in range(R.randint(1, 8)))
        assert brute.rotateString(s, goal) == opt.rotateString(s, goal), (s, goal)


@case(1021)
def _(h):
    brute, opt = both(h, 1021)
    for s, want in [("(()())(())", "()()()"), ("(()())(())(()(()))", "()()()()(())"), ("()()", "")]:
        assert brute.removeOuterParentheses(s) == want and opt.removeOuterParentheses(s) == want, s
    for _ in range(500):
        s = random_vps(R.randint(1, 12))
        assert brute.removeOuterParentheses(s) == opt.removeOuterParentheses(s), s
    big = "(" * 50_000 + ")" * 50_000
    assert opt.removeOuterParentheses(big) == big[1:-1]
    timed_call(lambda: opt.removeOuterParentheses(random_vps(50_000)), 1)


@case(1614)
def _(h):
    brute, opt = both(h, 1614)
    for s, want in [("(1+(2*3)+((8)/4))+1", 3), ("(1)+((2))+(((3)))", 3), ("()(())((()()))", 3), ("1+2", 0), ("", 0)]:
        assert brute.maxDepth(s) == want and opt.maxDepth(s) == want, s
    for _ in range(500):
        s = random_vps(R.randint(0, 15), "12+*/")
        assert brute.maxDepth(s) == opt.maxDepth(s), s


@case(1781)
def _(h):
    brute, opt = both(h, 1781)
    assert brute.beautySum("aabcb") == 5 and opt.beautySum("aabcb") == 5
    assert brute.beautySum("aabcbaa") == 17 and opt.beautySum("aabcbaa") == 17
    assert opt.beautySum("z") == 0
    for _ in range(300):
        s = "".join(R.choice("abcd") for _ in range(R.randint(1, 14)))
        assert brute.beautySum(s) == opt.beautySum(s), s
    big = "".join(R.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(500))
    timed_call(lambda: opt.beautySum(big), 5)


@case(1903)
def _(h):
    brute, opt = both(h, 1903)
    for num, want in [("52", "5"), ("4206", ""), ("35427", "35427"), ("7", "7"), ("8", "")]:
        assert brute.largestOddNumber(num) == want and opt.largestOddNumber(num) == want, num
    for _ in range(500):
        num = R.choice("123456789") + "".join(R.choice("0123456789") for _ in range(R.randint(0, 9)))
        assert brute.largestOddNumber(num) == opt.largestOddNumber(num), num
    big = "1" + "2" * (10**5 - 1)
    assert opt.largestOddNumber(big) == "1"
    timed_call(lambda: opt.largestOddNumber(big), 1)

