# 🔹 Solution — Mock 10 · Q1: Tray Stack (Stack with Running Maximum, Easy)

**Problem statement:** [Q1_Easy_Tray_Stack.md](../Q1_Easy_Tray_Stack.md) · judge your own code first with `python tools/judge/judge.py M10Q1 <your_file>.py`

## 🔹 Quick Breakdown

* **Difficulty Level:** Easy (Q1 slot)
* **Main Approach:** Next to every pushed weight, store the **maximum of the stack up to and including it**: `best = max(x, best_below)`. A pop removes the pair, so the new top's stored maximum is again correct. The heaviest tray is always the stored maximum at the top.
* **Core Concept:** augmenting a stack with a prefix aggregate (min / max stack)
* **When to Use This Pattern?** O(1) max/min queries on a structure that only changes at one end (stack); for a queue, use two such stacks.
* **Mistakes to Avoid:**
  * Recomputing `max(stack)` per query — O(Q²).
  * Keeping one global max: after the max is popped you no longer know the next one.
  * Popping from an empty stack — the statement says to ignore it.

## 🔹 Optimization Path

* **Brute Force:** `max(stack)` per query — O(Q²).
* **Optimized Solution:** O(1) per operation.

## 🔹 Solution Breakdown

* **Optimal Approach:** keep `maxes`, a stack of prefix maxima: push `max(x, maxes[-1])`, pop with `maxes.pop()`, query `maxes[-1]` (or −1 when empty).
* **Why This Works?** The stack below any element never changes while that element is on the stack, so its prefix maximum computed at push time stays valid until it is popped.
* **Edge Cases Considered:**
  * Query on an empty stack → `-1`.
  * Equal weights — the running max simply repeats.

## 🔹 Pattern Recognition

* **Belongs To:** Stack — design
* **Common Problems Using This:**
  * [155. Min Stack](../../../Design/155.Min_Stack.md)
  * 716. Max Stack
  * 232. Implement Queue using Stacks (in this repo — two stacks make a queue with the same trick)

## 🔹 Tricks & Patterns Used

* **Store the aggregate with each element**, not once globally.
* **Buffered output:** collect answers and print once.

## 🔹 Alternative Data Structures

* A heap with lazy deletion — O(log Q), more code, no benefit here.

## 🔹 Complexity Analysis

* **Time Complexity:** O(Q)
* **Space Complexity:** O(Q)

## 🔹 Code Snippet (Brute Force — partial score)

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    q, i, stack, out = int(data[0]), 1, [], []
    for _ in range(q):
        op = data[i]
        i += 1
        if op == b"1":
            stack.append(int(data[i]))
            i += 1
        elif op == b"2":
            if stack:
                stack.pop()
        else:
            out.append(str(max(stack)) if stack else "-1")
    print("\n".join(out))


if __name__ == "__main__":
    main()
```

## 🔹 Code Snippet (Optimized)

```python
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    q, i, maxes, out = int(data[0]), 1, [], []
    for _ in range(q):
        op = data[i]
        i += 1
        if op == b"1":
            x = int(data[i])
            i += 1
            maxes.append(max(x, maxes[-1]) if maxes else x)  # max of the stack up to this tray
        elif op == b"2":
            if maxes:
                maxes.pop()
        else:
            out.append(str(maxes[-1]) if maxes else "-1")
    print("\n".join(out))


if __name__ == "__main__":
    main()
```
