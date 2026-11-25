# 🔹 Problem Name: Stock Ticker Queries (Segment Tree with Custom Merge, Hard)

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 1, Question 3
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

A trading desk records the profit `A[i]` (possibly negative) of each of `N` days. It must answer `Q` operations of two types:

* `1 i x` — the profit of day `i` is corrected to `x`.
* `2 l r` — print the **maximum sum of a non-empty contiguous block of days** inside days `l..r`.

**Input Format**
* Line 1: two integers `N` and `Q`
* Line 2: `N` integers `A[1..N]`
* Next `Q` lines: an operation `t a b` as described (1-indexed)

**Output Format**
* For every type-2 operation, print the answer on its own line.

**Constraints**
* `1 ≤ N, Q ≤ 10⁵`
* `-10⁹ ≤ A[i], x ≤ 10⁹`
* `1 ≤ l ≤ r ≤ N`, `1 ≤ i ≤ N`

**Sample Input**
```text
5 4
2 -3 4 -1 2
2 1 5
1 4 -5
2 1 5
2 1 2
```

**Sample Output**
```text
5
4
2
```

**Explanation:** Initially the best block is `4 -1 2` (sum 5). After day 4 becomes `-5`, the best block is just `4`. In days 1..2 the best block is `2`.

## 🔹 Quick Breakdown

* **Difficulty Level:** Hard (Q3 slot)
* **Main Approach:** Segment tree where every node stores 4 numbers for its range: `sum`, best `prefix`, best `suffix`, best `subarray`. Two children merge in O(1), so updates and queries are O(log N).
* **Core Concept:** Segment tree with a non-trivial (non-commutative) merge
* **When to Use This Pattern?** Range queries whose answer is not a simple sum/min/max but can be **combined from two halves** (max subarray, longest run of 1s, bracket matching, count of inversions in small alphabets).
* **Mistakes to Avoid:**
  * Kadane per query — O(N · Q) = 10¹⁰ (that is the partial-score version).
  * Combining left and right pieces in the wrong order during the iterative query — this merge is **not** commutative.
  * Answer must be non-empty: with all negatives, return the largest single value (not 0).

## 🔹 Optimization Path

* **Brute Force:** O(N) Kadane per query → O(N · Q).
* **Optimized Solution:** O((N + Q) log N).
* **Further Improvements Possible?** No for online queries.

## 🔹 Solution Breakdown

* **Optimal Approach:** `merge(L, R)`:
  * `sum = L.sum + R.sum`
  * `prefix = max(L.prefix, L.sum + R.prefix)`
  * `suffix = max(R.suffix, R.sum + L.suffix)`
  * `best = max(L.best, R.best, L.suffix + R.prefix)`
  Query collects nodes from the left side into `left_acc` (merged on the right) and from the right side into `right_acc` (merged on the left), then merges the two.
* **Why This Works?** The best block of a range lies entirely in the left half, entirely in the right half, or crosses the middle — then it is a suffix of the left plus a prefix of the right. The four numbers capture all three cases.
* **Edge Cases Considered:**
  * All negative values.
  * `l == r`.
  * Repeated updates to the same day.

## 🔹 Pattern Recognition

* **Belongs To:** Segment Tree
* **Common Problems Using This:**
  * 307. Range Sum Query - Mutable (in this repo)
  * 53. Maximum Subarray (in this repo — the single-query version)
  * SPOJ GSS1 / GSS3 (classic)

## 🔹 Tricks & Patterns Used

* **Identity element** `(0, -∞, -∞, -∞)` makes the iterative query branch-free.
* **Power-of-two tree size** keeps the left-to-right order of nodes intact.

## 🔹 Alternative Data Structures

* Recursive segment tree — easier to write under pressure, ~2–3× slower in Python.

## 🔹 Complexity Analysis

* **Time Complexity:** O(N + Q log N)
* **Space Complexity:** O(N)

## 🔹 Code Snippet (Brute Force — partial score)

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, q = int(data[0]), int(data[1])
    a = [int(x) for x in data[2:2 + n]]
    pos = 2 + n
    out = []
    for _ in range(q):
        t, x, y = int(data[pos]), int(data[pos + 1]), int(data[pos + 2])
        pos += 3
        if t == 1:
            a[x - 1] = y
        else:
            best, cur = a[x - 1], 0  # Kadane on a[x-1 .. y-1]
            for v in a[x - 1:y]:
                cur = max(v, cur + v)
                best = max(best, cur)
            out.append(best)
    print("\n".join(map(str, out)))


if __name__ == "__main__":
    main()
```

## 🔹 Code Snippet (Optimized)

```python
import sys

NEG = -(1 << 62)
EMPTY = (0, NEG, NEG, NEG)  # (sum, best prefix, best suffix, best subarray)


def merge(a, b):
    s1, p1, x1, b1 = a
    s2, p2, x2, b2 = b
    return (s1 + s2,
            max(p1, s1 + p2),
            max(x2, s2 + x1),
            max(b1, b2, x1 + p2))


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, q = int(data[0]), int(data[1])
    size = 1
    while size < n:
        size *= 2
    tree = [EMPTY] * (2 * size)
    for i in range(n):
        v = int(data[2 + i])
        tree[size + i] = (v, v, v, v)
    for i in range(size - 1, 0, -1):
        tree[i] = merge(tree[2 * i], tree[2 * i + 1])

    out = []
    pos = 2 + n
    for _ in range(q):
        t, a, b = int(data[pos]), int(data[pos + 1]), int(data[pos + 2])
        pos += 3
        if t == 1:  # day a becomes b
            i = size + a - 1
            tree[i] = (b, b, b, b)
            i //= 2
            while i:
                tree[i] = merge(tree[2 * i], tree[2 * i + 1])
                i //= 2
        else:  # best block inside days a..b
            left_acc, right_acc = EMPTY, EMPTY
            l, r = size + a - 1, size + b  # half-open [l, r)
            while l < r:
                if l & 1:
                    left_acc = merge(left_acc, tree[l])
                    l += 1
                if r & 1:
                    r -= 1
                    right_acc = merge(tree[r], right_acc)
                l //= 2
                r //= 2
            out.append(merge(left_acc, right_acc)[3])
    print("\n".join(map(str, out)))


if __name__ == "__main__":
    main()
```
