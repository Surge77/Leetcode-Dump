# 🔹 Problem Name: Balanced Segments (Prefix Sum + Hashing, Easy)

**🔗 Link:** Original Infosys SP/DSE-style practice problem — Mock Test 4, Question 1
**🟢 Status:** 🔄 Need Review

## 🔹 Problem Statement

A sensor log is a binary string `S` of length `N` (`1` = signal, `0` = silence). A contiguous segment is *balanced* if it contains the same number of `0`s and `1`s.

Count the balanced segments.

**Input Format**
* Line 1: integer `N`
* Line 2: binary string `S`

**Output Format**
* One integer — the number of balanced segments.

**Constraints**
* `1 ≤ N ≤ 2·10⁵`

**Sample Input**
```text
6
100110
```

**Sample Output**
```text
7
```

**Explanation:** Map `1 → +1` and `0 → -1`; a segment is balanced exactly when its sum is 0.

## 🔹 Quick Breakdown

* **Difficulty Level:** Easy (Q1 slot)
* **Main Approach:** With `+1/-1` values, a segment `(i, j]` is balanced iff `prefix[j] == prefix[i]`. Count equal prefix values with a hashmap.
* **Core Concept:** Prefix sum + frequency hashmap
* **When to Use This Pattern?** "Equal number of X and Y", "sum equals k", "sum divisible by k" over subarrays.
* **Mistakes to Avoid:**
  * Forgetting the empty prefix (`count[0] = 1`) — misses segments starting at position 1.
  * O(N²) enumeration (the partial-score version).

## 🔹 Optimization Path

* **Brute Force:** O(N²) — extend every start.
* **Optimized Solution:** O(N).
* **Further Improvements Possible?** Prefix values lie in `[-N, N]`, so an array can replace the dict.

## 🔹 Solution Breakdown

* **Optimal Approach:** Running `prefix`; `answer += seen[prefix]`; `seen[prefix] += 1`.
* **Why This Works?** Every pair of equal prefix values bounds exactly one balanced segment, and every balanced segment comes from such a pair.
* **Edge Cases Considered:**
  * All `1`s → 0.
  * `N = 1` → 0.

## 🔹 Pattern Recognition

* **Belongs To:** Prefix Sum + Hashing
* **Common Problems Using This:**
  * 560. Subarray Sum Equals K (in this repo)
  * 525. Contiguous Array (longest instead of count)

## 🔹 Tricks & Patterns Used

* **Map two symbols to `+1 / -1`** so "equal counts" becomes "sum 0".

## 🔹 Alternative Data Structures

* Array of size `2N + 1` indexed by `prefix + N`.

## 🔹 Complexity Analysis

* **Time Complexity:** O(N)
* **Space Complexity:** O(N)

## 🔹 Code Snippet (Brute Force — partial score)

```python
import sys


def main() -> None:
    data = sys.stdin.read().split()
    s = data[1]
    count = 0
    for i in range(len(s)):
        balance = 0
        for j in range(i, len(s)):
            balance += 1 if s[j] == "1" else -1
            if balance == 0:
                count += 1
    print(count)


if __name__ == "__main__":
    main()
```

## 🔹 Code Snippet (Optimized)

```python
import sys
from collections import defaultdict


def main() -> None:
    data = sys.stdin.read().split()
    s = data[1]
    seen = defaultdict(int)
    seen[0] = 1  # empty prefix
    prefix = count = 0
    for ch in s:
        prefix += 1 if ch == "1" else -1
        count += seen[prefix]  # earlier equal prefixes close a balanced segment
        seen[prefix] += 1
    print(count)


if __name__ == "__main__":
    main()
```
