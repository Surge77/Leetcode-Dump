# 🔹 Language Internals: Python and Java

Interviewers ask about the language you code in. Know why your solution is fast or slow in it. The Python blocks run as-is (`python -m unittest tools/tests/test_interview_prep.py` executes them).

## 🔹 Python

### Data structures and their costs

| Operation | Cost | Why |
|---|---|---|
| `list.append`, `pop()` | O(1) amortised | dynamic array that over-allocates (grows ~1.125×) |
| `list.insert(0, x)`, `pop(0)`, `x in list` | O(n) | shifting / linear scan → use `collections.deque` or a set |
| `dict` / `set` get, set, `in` | O(1) average, O(n) worst | open-addressing hash table; insertion-ordered since 3.7 |
| `heapq.heappush/heappop` | O(log n) | binary min-heap in a list; negate values for a max-heap |
| `deque.appendleft/popleft` | O(1) | doubly linked blocks |
| `sorted`, `list.sort` | O(n log n), stable | Timsort (run-adaptive merge sort) |
| `s + t` in a loop | O(n²) total | strings are immutable → collect parts and `"".join(parts)` |

### The questions that come up

* **GIL**: CPython lets one thread run Python bytecode at a time. Threads still help for I/O-bound work (the GIL is released while waiting). For CPU-bound work use `multiprocessing` / `ProcessPoolExecutor`. Free-threaded builds without a GIL (PEP 703) are an opt-in build: experimental in 3.13, officially supported from 3.14, still not the default.
* **Memory**: reference counting frees most objects immediately; a cyclic garbage collector (generational) handles reference cycles. `sys.getrefcount`, `gc.collect()`.
* **Everything is an object; variables are names bound to objects.** Assignment never copies. `copy.copy` is shallow and `copy.deepcopy` deep.
* **Mutable vs immutable**: `list`, `dict`, `set` are mutable; `int`, `str`, `tuple`, `frozenset` are immutable (hashable, so they can be dict keys).
* **`is` vs `==`**: identity vs equality. Small ints (−5…256) and some strings are cached, so `is` can surprise you; compare values with `==`.
* **Default argument trap**: defaults are evaluated once, at definition time.
* **Generators** produce values lazily with `yield`: O(1) memory for a stream. A generator expression is `(x for x in …)`.
* **Decorators** wrap a function: `@lru_cache` memoises (arguments must be hashable), `@dataclass` writes `__init__`/`__eq__`/`__repr__`.
* **`__slots__`** removes the per-instance `__dict__`: less memory, no new attributes.
* **Recursion limit** is ~1000 by default. Deep DFS needs `sys.setrecursionlimit` (plus a bigger thread stack) or an iterative rewrite.

```python
import sys
from functools import lru_cache


def append_to(item, bucket=[]):  # the default list is created ONCE
    bucket.append(item)
    return bucket


assert append_to(1) == [1] and append_to(2) == [1, 2]  # surprise: shared state


def append_fixed(item, bucket=None):
    bucket = [] if bucket is None else bucket
    bucket.append(item)
    return bucket


assert append_fixed(1) == [1] and append_fixed(2) == [2]

a = [[0] * 3] * 2  # two references to ONE inner list
a[0][0] = 9
assert a == [[9, 0, 0], [9, 0, 0]]
grid = [[0] * 3 for _ in range(2)]  # the correct way: a new inner list per row
grid[0][0] = 9
assert grid == [[9, 0, 0], [0, 0, 0]]


@lru_cache(maxsize=None)
def ways(n):  # memoised recursion: O(n) instead of O(2^n)
    return 1 if n <= 1 else ways(n - 1) + ways(n - 2)


assert ways(80) == 37889062373143906
squares = (i * i for i in range(10**9))  # a generator: nothing is computed yet
assert next(squares) == 0 and sys.getsizeof(squares) < 500
```

### Contest and interview idioms

`from collections import Counter, defaultdict, deque` · `heapq.nlargest(k, xs)` · `bisect.bisect_left(sorted_xs, x)` · `itertools.accumulate` (prefix sums), `combinations`, `permutations`, `product` · `math.gcd`, `math.comb`, `pow(a, b, mod)`, `pow(a, -1, mod)` (modular inverse) · `sys.stdin.readline` for fast input. Full template: [Python_Contest_Template.md](../Infosys_SP_DSE/Python_Contest_Template.md).

## 🔹 Java

### Collections and their costs

| Type | Backed by | Notes |
|---|---|---|
| `ArrayList` | resizable array (grows 1.5×) | O(1) get, amortised O(1) add at the end |
| `LinkedList` | doubly linked list | O(1) add/remove at the ends, O(n) get(i); prefer `ArrayDeque` for stacks and queues |
| `HashMap` | array of buckets | O(1) average; buckets become red-black trees past 8 entries (O(log n) worst); resizes at load factor 0.75 |
| `LinkedHashMap` | HashMap + linked list | insertion or access order; `removeEldestEntry` gives an LRU cache in a few lines |
| `TreeMap` / `TreeSet` | red-black tree | O(log n), sorted, `floorKey`/`ceilingKey` |
| `PriorityQueue` | binary heap | min-heap by default; `new PriorityQueue<>(Comparator.reverseOrder())` for max |
| `ConcurrentHashMap` | segmented / CAS buckets | thread-safe without locking the whole map |

### The questions that come up

* **`equals` and `hashCode`**: override both or neither. Equal objects must have equal hash codes, or `HashMap` lookups fail.
* **`String` is immutable** and interned literals share memory; build strings in loops with `StringBuilder`. `==` compares references, `.equals` compares content.
* **JVM memory**: heap (objects, garbage collected: young generation with eden and survivors, then old) vs stack (frames and locals, one per thread) vs metaspace (class metadata). The default collector is G1; ZGC is the low-pause option.
* **Autoboxing**: `Integer` caches −128…127, so `==` on boxed values outside that range compares references; use `.equals`. Boxing in hot loops costs allocations.
* **`final` vs `finally` vs `finalize`**: can't reassign or override / always runs after `try` / deprecated GC hook.
* **Checked vs unchecked exceptions**: must declare or catch (`IOException`) vs runtime (`NullPointerException`).
* **Interfaces vs abstract classes**: a class implements many interfaces (default methods since Java 8) but extends one class (which can hold state and constructors).
* **Concurrency**: `synchronized` (intrinsic lock), `volatile` (visibility, not atomicity), `AtomicInteger` (CAS), `ExecutorService` thread pools, `CompletableFuture`. Java 21 virtual threads make blocking I/O cheap at high concurrency.
* **Pass-by-value**: Java always passes by value; for objects the value is the reference, so you can mutate the object but not rebind the caller's variable.

```java
// LRU cache in Java: the access-ordered LinkedHashMap does the bookkeeping.
class LRU<K, V> extends LinkedHashMap<K, V> {
    private final int capacity;
    LRU(int capacity) { super(16, 0.75f, true); this.capacity = capacity; }
    @Override protected boolean removeEldestEntry(Map.Entry<K, V> eldest) { return size() > capacity; }
}
```

## 🔹 Comparing Them (a common question)

| | Python | Java |
|---|---|---|
| Typing | dynamic (optional hints) | static |
| Execution | interpreted bytecode (CPython) | JIT-compiled bytecode on the JVM, usually 10–50× faster for loops |
| Concurrency | GIL limits CPU-bound threads | real parallel threads |
| Integers | arbitrary precision | `int` 32-bit, `long` 64-bit; overflow wraps silently |
| In interviews | shortest code; watch constant factors (recursion, slicing copies) | verbose but predictable; watch overflow and boxing |
