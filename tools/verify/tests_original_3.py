"""Checks for the notes that existed before the Infosys expansion (part 3 of 4).

Shared helpers: helpers_original.py.
"""
from helpers_original import (  # noqa: F401
    Counter,
    R,
    case,
    isqrt,
    solvers,
)


@case(48)
def _(h):
    for S in solvers(48):
        for n in range(1, 7):
            m = [[R.randint(0, 9) for _ in range(n)] for _ in range(n)]
            want = [list(r) for r in zip(*m[::-1])]
            S.rotate(m)
            assert m == want


@case(54)
def _(h):
    for S in solvers(54):
        for _ in range(200):
            m, n = R.randint(1, 6), R.randint(1, 6)
            g = [[R.randint(0, 99) for _ in range(n)] for _ in range(m)]
            want, grid = [], [r[:] for r in g]
            while grid:
                want += grid.pop(0)
                grid = [list(r) for r in zip(*grid)][::-1]
            assert S.spiralOrder([r[:] for r in g]) == want


@case(153)
def _(h):
    for S in solvers(153):
        for _ in range(300):
            a = sorted(R.sample(range(-50, 50), R.randint(1, 12)))
            k = R.randrange(len(a))
            assert S.findMin(a[k:] + a[:k]) == a[0]


@case(33)
def _(h):
    for S in solvers(33):
        for _ in range(300):
            a = sorted(R.sample(range(-20, 20), R.randint(1, 10)))
            k = R.randrange(len(a))
            rot = a[k:] + a[:k]
            t = R.randint(-21, 21)
            assert S.search(rot, t) == (rot.index(t) if t in rot else -1)


@case(69)
def _(h):
    for S in solvers(69):
        for x in list(range(0, 2000)) + [2**31 - 1] + [R.randint(0, 2**31 - 1) for _ in range(200)]:
            assert S.mySqrt(x) == isqrt(x), x


@case(74)
def _(h):
    for S in solvers(74):
        for _ in range(300):
            m, n = R.randint(1, 5), R.randint(1, 5)
            flat = sorted(R.sample(range(100), m * n))
            g = [flat[i * n:(i + 1) * n] for i in range(m)]
            t = R.randint(-1, 100)
            assert S.searchMatrix(g, t) == (t in flat)


@case(735)
def _(h):
    for S in solvers(735):
        for _ in range(300):
            a = [R.choice((-1, 1)) * R.randint(1, 5) for _ in range(R.randint(1, 9))]
            cur = a[:]
            while True:
                for i in range(len(cur) - 1):
                    if cur[i] > 0 > cur[i + 1]:
                        x, y = cur[i], -cur[i + 1]
                        cur[i:i + 2] = [cur[i]] if x > y else ([cur[i + 1]] if y > x else [])
                        break
                else:
                    break
            assert S.asteroidCollision(a[:]) == cur, a


@case(739)
def _(h):
    for S in solvers(739):
        for _ in range(300):
            t = [R.randint(30, 40) for _ in range(R.randint(1, 12))]
            want = [next((j - i for j in range(i + 1, len(t)) if t[j] > t[i]), 0) for i in range(len(t))]
            assert S.dailyTemperatures(t) == want


@case(209)
def _(h):
    for S in solvers(209):
        for _ in range(300):
            a = [R.randint(1, 6) for _ in range(R.randint(1, 10))]
            target = R.randint(1, 25)
            lens = [j - i + 1 for i in range(len(a)) for j in range(i, len(a)) if sum(a[i:j + 1]) >= target]
            assert S.minSubArrayLen(target, a) == min(lens, default=0)


@case(3423)
def _(h):
    for S in solvers(3423):
        for _ in range(300):
            a = [R.randint(-20, 20) for _ in range(R.randint(2, 10))]
            assert S.maxAdjacentDistance(a) == max(abs(a[i] - a[(i + 1) % len(a)]) for i in range(len(a)))


@case(424)
def _(h):
    for S in solvers(424):
        for _ in range(300):
            s = "".join(R.choice("AB") for _ in range(R.randint(1, 10)))
            k = R.randint(0, 3)
            want = max(j - i for i in range(len(s)) for j in range(i + 1, len(s) + 1)
                       if (j - i) - max(Counter(s[i:j]).values()) <= k)
            assert S.characterReplacement(s, k) == want, (s, k)


@case(438)
def _(h):
    for S in solvers(438):
        for _ in range(300):
            s = "".join(R.choice("ab") for _ in range(R.randint(1, 12)))
            p = "".join(R.choice("ab") for _ in range(R.randint(1, 4)))
            want = [i for i in range(len(s) - len(p) + 1) if Counter(s[i:i + len(p)]) == Counter(p)]
            assert sorted(S.findAnagrams(s, p)) == want


@case(150)
def _(h):
    def ref(tokens):
        st = []
        for t in tokens:
            if t in "+-*/" and len(t) == 1:
                b, a = st.pop(), st.pop()
                st.append(a + b if t == "+" else a - b if t == "-" else a * b if t == "*" else int(a / b))
            else:
                st.append(int(t))
        return st[0]
    for S in solvers(150):
        assert S.evalRPN(["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]) == 22
        for _ in range(300):
            tokens, depth = [str(R.randint(-9, 9))], 1
            for _ in range(R.randint(0, 5)):
                tokens.append(str(R.choice([x for x in range(-9, 10) if x != 0])))
                tokens.append(R.choice("+-*/"))
            try:
                want = ref(tokens)
            except ZeroDivisionError:
                continue
            assert S.evalRPN(tokens[:]) == want, tokens


@case(20)
def _(h):
    for S in solvers(20):
        for _ in range(500):
            s = "".join(R.choice("()[]{}") for _ in range(R.randint(1, 10)))
            t = s
            while any(p in t for p in ("()", "[]", "{}")):
                t = t.replace("()", "").replace("[]", "").replace("{}", "")
            assert S.isValid(s) == (t == ""), s


@case(227)
def _(h):
    def ref(expr):
        nums, ops = [], []
        for tok in expr.replace(" ", "").replace("+", " + ").replace("-", " - ").replace("*", " * ").replace("/", " / ").split():
            (ops if tok in "+-*/" else nums).append(tok if tok in "+-*/" else int(tok))
        vals, signs = [nums[0]], []
        for op, x in zip(ops, nums[1:]):
            if op == "*":
                vals[-1] *= x
            elif op == "/":
                vals[-1] = int(vals[-1] / x)
            else:
                signs.append(op)
                vals.append(x)
        total = vals[0]
        for op, v in zip(signs, vals[1:]):
            total = total + v if op == "+" else total - v
        return total
    for S in solvers(227):
        assert S.calculate("3+2*2") == 7 and S.calculate(" 3/2 ") == 1 and S.calculate(" 3+5 / 2 ") == 5
        for _ in range(300):
            parts = [str(R.randint(0, 20))]
            for _ in range(R.randint(0, 5)):
                op = R.choice("+-*/")
                parts += [op, str(R.randint(1, 20) if op == "/" else R.randint(0, 20))]
            expr = R.choice(("", " ")).join(parts)
            assert S.calculate(expr) == ref(expr), expr


@case(215)
def _(h):
    for S in solvers(215):
        for _ in range(300):
            a = [R.randint(-9, 9) for _ in range(R.randint(1, 12))]
            k = R.randint(1, len(a))
            assert S.findKthLargest(a[:], k) == sorted(a)[-k]


@case(11)
def _(h):
    for S in solvers(11):
        for _ in range(300):
            a = [R.randint(0, 9) for _ in range(R.randint(2, 10))]
            assert S.maxArea(a) == max(min(a[i], a[j]) * (j - i) for i in range(len(a)) for j in range(i + 1, len(a)))


@case(189)
def _(h):
    for S in solvers(189):
        for _ in range(300):
            a = list(range(R.randint(1, 10)))
            k = R.randint(0, 25)
            want = a[-(k % len(a)):] + a[:-(k % len(a))] if k % len(a) else a[:]
            S.rotate(a, k)
            assert a == want


@case(5)
def _(h):
    for S in solvers(5):
        for _ in range(300):
            s = "".join(R.choice("ab") for _ in range(R.randint(1, 12)))
            best = max(j - i for i in range(len(s)) for j in range(i + 1, len(s) + 1) if s[i:j] == s[i:j][::-1])
            got = S.longestPalindrome(s)
            assert len(got) == best and got == got[::-1] and got in s, (s, got)


# ---------------- notes that were Java-only (Python versions added) ----------------
@case(121)
def _(h):
    for S in solvers(121):
        for _ in range(300):
            p = [R.randint(0, 20) for _ in range(R.randint(1, 10))]
            assert S.maxProfit(p) == max([p[j] - p[i] for i in range(len(p)) for j in range(i, len(p))])


@case(169)
def _(h):
    for S in solvers(169):
        for _ in range(300):
            n = R.randint(1, 11)
            major = R.randint(0, 5)
            nums = [major] * (n // 2 + 1) + [R.choice([x for x in range(6) if x != major]) for _ in range(n - n // 2 - 1)]
            R.shuffle(nums)
            assert S.majorityElement(nums) == major


@case(3335)
def _(h):
    for S in solvers(3335):
        assert S.lengthAfterTransformations("abcyy", 2) == 7 and S.lengthAfterTransformations("azbk", 1) == 5
        for _ in range(100):
            s = "".join(R.choice("xyzab") for _ in range(R.randint(1, 6)))
            t = R.randint(1, 30)
            cur = s
            for _ in range(t):
                cur = "".join("ab" if c == "z" else chr(ord(c) + 1) for c in cur)
            assert S.lengthAfterTransformations(s, t) == len(cur) % (10**9 + 7)


@case(70)
def _(h):
    for S in solvers(70):
        a, b = 1, 1
        for n in range(1, 46):
            assert S.climbStairs(n) == b
            a, b = b, a + b
