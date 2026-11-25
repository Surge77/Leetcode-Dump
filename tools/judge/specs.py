"""Test-input generators for every mock problem, shared by the judge and tools/verify.

Each spec has
    small(rng) -> str          one random small input (the brute force must finish instantly)
    large(rng) -> list[str]    max-constraint inputs (timing + adversarial shapes)
"""
from dataclasses import dataclass
from typing import Callable, List


@dataclass(frozen=True)
class Spec:
    small: Callable[..., str]
    large: Callable[..., List[str]]


def ints(rng, n, lo, hi):
    return " ".join(str(rng.randint(lo, hi)) for _ in range(n))


def bits(rng, n):
    return "".join(rng.choice("01") for _ in range(n))


def ranges(rng, n, q):
    """q random 1-based ranges `l r` with l <= r."""
    out = []
    for _ in range(q):
        left = rng.randint(1, n)
        out.append(f"{left} {rng.randint(left, n)}")
    return out


def distinct_pairs(rng, n, m):
    """m random edges, each between two distinct vertices of 1..n."""
    if n < 2:
        return []
    return [" ".join(map(str, rng.sample(range(1, n + 1), 2))) for _ in range(m)]


def lines(*parts):
    out = []
    for part in parts:
        out += part if isinstance(part, list) else [part]
    return "\n".join(out)


def path_edges(n):
    return [f"{i} {i + 1}" for i in range(1, n)]


def tree_edges(rng, n):
    """Random tree on 1..n: vertex i attaches to a random earlier vertex."""
    return [f"{rng.randint(1, i - 1)} {i}" for i in range(2, n + 1)]


SPECS = {}


def register(key, small, large):
    SPECS[key] = Spec(small, large)


# Imported for their register() side effects; kept in separate files to stay small.
import specs_mocks_1_6  # noqa: E402,F401
import specs_mocks_7_10  # noqa: E402,F401
