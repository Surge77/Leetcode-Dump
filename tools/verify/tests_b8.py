import heapq
import random
from collections import Counter, deque
from itertools import combinations, permutations

from harness import case

R = random.Random(8)


@case(621)
def _(h):
    S = h.lc(621)["Solution"]()
    assert S.leastInterval(["A", "A", "A", "B", "B", "B"], 2) == 8
    assert S.leastInterval(["A", "C", "A", "B", "D", "B"], 1) == 6
    for _ in range(300):
        tasks = [R.choice("ABCD") for _ in range(R.randint(1, 12))]
        n = R.randint(0, 4)
        heap = [-c for c in Counter(tasks).values()]
        heapq.heapify(heap)
        cool, t = deque(), 0
        while heap or cool:
            t += 1
            if heap:
                c = heapq.heappop(heap) + 1
                if c:
                    cool.append((c, t + n))
            if cool and cool[0][1] == t:
                heapq.heappush(heap, cool.popleft()[0])
        assert S.leastInterval(tasks, n) == t, (tasks, n)


@case(502)
def _(h):
    S = h.lc(502)["Solution"]()
    assert S.findMaximizedCapital(2, 0, [1, 2, 3], [0, 1, 1]) == 4
    assert S.findMaximizedCapital(3, 0, [1, 2, 3], [0, 1, 2]) == 6
    for _ in range(200):
        n = R.randint(1, 5)
        prof = [R.randint(0, 6) for _ in range(n)]
        cap = [R.randint(0, 6) for _ in range(n)]
        k, w = R.randint(1, n), R.randint(0, 3)
        best = w
        for r in range(1, k + 1):
            for order in permutations(range(n), r):
                cur, ok = w, True
                for i in order:
                    if cap[i] > cur:
                        ok = False
                        break
                    cur += prof[i]
                if ok:
                    best = max(best, cur)
        assert S.findMaximizedCapital(k, w, prof, cap) == best


@case(55)
def _(h):
    S = h.lc(55)["Solution"]()
    for _ in range(400):
        a = [R.randint(0, 3) for _ in range(R.randint(1, 10))]
        reach = [False] * len(a)
        reach[0] = True
        for i in range(len(a)):
            if reach[i]:
                for j in range(i + 1, min(len(a), i + a[i] + 1)):
                    reach[j] = True
        assert S.canJump(a) == reach[-1], a


@case(45)
def _(h):
    S = h.lc(45)["Solution"]()
    assert S.jump([2, 3, 1, 1, 4]) == 2 and S.jump([0]) == 0
    for _ in range(400):
        a = [R.randint(1, 4) for _ in range(R.randint(1, 10))]
        INF = 99
        d = [0] + [INF] * (len(a) - 1)
        for i in range(len(a)):
            for j in range(i + 1, min(len(a), i + a[i] + 1)):
                d[j] = min(d[j], d[i] + 1)
        assert S.jump(a) == d[-1], a


@case(134)
def _(h):
    S = h.lc(134)["Solution"]()
    assert S.canCompleteCircuit([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]) == 3 and S.canCompleteCircuit([2, 3, 4], [3, 4, 3]) == -1
    for _ in range(400):
        n = R.randint(1, 7)
        gas = [R.randint(0, 5) for _ in range(n)]
        cost = [R.randint(0, 5) for _ in range(n)]
        starts = []
        for s in range(n):
            tank, ok = 0, True
            for k in range(n):
                i = (s + k) % n
                tank += gas[i] - cost[i]
                if tank < 0:
                    ok = False
                    break
            if ok:
                starts.append(s)
        got = S.canCompleteCircuit(gas, cost)
        assert (got == -1 and not starts) or got in starts, (gas, cost, got)


@case(630)
def _(h):
    S = h.lc(630)["Solution"]()
    assert S.scheduleCourse([[100, 200], [200, 1300], [1000, 1250], [2000, 3200]]) == 3
    assert S.scheduleCourse([[3, 2], [4, 3]]) == 0
    for _ in range(300):
        courses = [[R.randint(1, 6), R.randint(1, 15)] for _ in range(R.randint(1, 7))]
        best = 0
        for r in range(1, len(courses) + 1):
            for sub in combinations(courses, r):
                t, ok = 0, True
                for d, last in sorted(sub, key=lambda c: c[1]):
                    t += d
                    ok &= t <= last
                if ok:
                    best = max(best, r)
        assert S.scheduleCourse([c[:] for c in courses]) == best, courses


@case(452)
def _(h):
    S = h.lc(452)["Solution"]()
    assert S.findMinArrowShots([[10, 16], [2, 8], [1, 6], [7, 12]]) == 2
    assert S.findMinArrowShots([[1, 2], [2, 3], [3, 4], [4, 5]]) == 2
    for _ in range(300):
        iv = []
        for _ in range(R.randint(1, 6)):
            a = R.randint(-5, 10)
            iv.append([a, a + R.randint(0, 5)])
        ends = sorted({e for _, e in iv})
        want = next(r for r in range(1, len(iv) + 1)
                    for pts in combinations(ends, r) if all(any(a <= p <= b for p in pts) for a, b in iv))
        assert S.findMinArrowShots([x[:] for x in iv]) == want, iv


@case(84)
def _(h):
    S = h.lc(84)["Solution"]()
    assert S.largestRectangleArea([2, 1, 5, 6, 2, 3]) == 10 and S.largestRectangleArea([2, 4]) == 4
    for _ in range(400):
        a = [R.randint(0, 8) for _ in range(R.randint(1, 12))]
        assert S.largestRectangleArea(a) == max(min(a[i:j + 1]) * (j - i + 1) for i in range(len(a)) for j in range(i, len(a)))


@case(907)
def _(h):
    S = h.lc(907)["Solution"]()
    assert S.sumSubarrayMins([3, 1, 2, 4]) == 17 and S.sumSubarrayMins([11, 81, 94, 43, 3]) == 444
    for _ in range(400):
        a = [R.randint(1, 6) for _ in range(R.randint(1, 12))]
        want = sum(min(a[i:j + 1]) for i in range(len(a)) for j in range(i, len(a))) % (10**9 + 7)
        assert S.sumSubarrayMins(a) == want, a


@case(42)
def _(h):
    S = h.lc(42)["Solution"]()
    assert S.trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6 and S.trap([4, 2, 0, 3, 2, 5]) == 9
    for _ in range(400):
        a = [R.randint(0, 6) for _ in range(R.randint(1, 12))]
        assert S.trap(a) == sum(max(0, min(max(a[:i + 1]), max(a[i:])) - a[i]) for i in range(len(a)))


@case(239)
def _(h):
    S = h.lc(239)["Solution"]()
    assert S.maxSlidingWindow([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
    for _ in range(400):
        a = [R.randint(-5, 5) for _ in range(R.randint(1, 12))]
        k = R.randint(1, len(a))
        assert S.maxSlidingWindow(a, k) == [max(a[i:i + k]) for i in range(len(a) - k + 1)]


@case(76)
def _(h):
    S = h.lc(76)["Solution"]()
    assert S.minWindow("ADOBECODEBANC", "ABC") == "BANC" and S.minWindow("a", "aa") == ""
    for _ in range(400):
        s = "".join(R.choice("abc") for _ in range(R.randint(1, 10)))
        t = "".join(R.choice("abc") for _ in range(R.randint(1, 3)))
        need = Counter(t)
        valid = [s[i:j] for i in range(len(s)) for j in range(i + 1, len(s) + 1) if not need - Counter(s[i:j])]
        got = S.minWindow(s, t)
        if not valid:
            assert got == ""
        else:
            assert len(got) == min(map(len, valid)) and not need - Counter(got) and got in s, (s, t, got)
