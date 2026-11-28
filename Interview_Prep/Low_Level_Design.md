# 🔹 Low-Level Design and Machine Coding

Machine-coding rounds (common at Indian product companies) give you 60–120 minutes to build a small working system in clean, extensible code. LLD rounds ask for the classes and their interactions on a whiteboard. Both reward the same habits. The Python below runs as-is: `python -m unittest tools/tests/test_interview_prep.py` executes every block.

## 🔹 The Approach (say it out loud)

1. **Clarify scope** (5 min): the 3–5 operations that must work; what's out (persistence, auth, UI).
2. **Nouns → classes, verbs → methods.** Find the entities and the one *service* class that coordinates them.
3. **Find what varies** (pricing rules, split types, strategies) and put it behind an interface. That's where interviewers add requirements mid-round.
4. **Code the happy path end to end first**, then validation and errors (custom exceptions, not prints).
5. **Demo it** with a short driver, and say what you'd add next (concurrency, persistence, tests).

Signals graders look for: small classes with one job, no god class, enums instead of magic strings, dependency injection for strategies, meaningful errors, and code that's easy to extend without editing existing classes (open/closed). SOLID and the four pillars are in [OOP.md](OOP.md).

## 🔹 Design Patterns You Will Actually Use

| Pattern | Use it when | Example |
|---|---|---|
| **Strategy** | an algorithm varies (pricing, splitting, eviction) | `SplitStrategy.equal/exact/percent` |
| **Factory** | creation depends on a type value | `VehicleFactory.create("car")` |
| **Observer** | others react to an event | notify riders when a parking slot frees up |
| **State** | behaviour depends on a lifecycle stage | order: created → paid → shipped |
| **Singleton** | exactly one shared instance (use sparingly; prefer injecting it) | a config or ID generator |
| **Builder** | many optional constructor arguments | `Query.builder().where(...).limit(10)` |
| **Decorator** | add behaviour without subclassing | caching or logging around a repository |

## 🔹 Machine Coding 1: Parking Lot

Requirements: multiple floors; slot sizes (bike, car, truck); park → ticket; unpark → fee by duration; show free slots per type.

```python
import itertools
import math
from dataclasses import dataclass, field
from enum import Enum


class Size(Enum):
    BIKE = 1
    CAR = 2
    TRUCK = 3


class ParkingFull(Exception):
    pass


@dataclass
class Slot:
    floor: int
    number: int
    size: Size
    vehicle: str | None = None


@dataclass
class Ticket:
    id: int
    plate: str
    slot: Slot
    entered_at: float


class HourlyPricing:  # strategy: swap in a different pricing rule without touching ParkingLot
    RATES = {Size.BIKE: 10, Size.CAR: 20, Size.TRUCK: 40}

    def fee(self, size, hours):
        return self.RATES[size] * max(1, math.ceil(hours))


@dataclass
class ParkingLot:
    slots: list
    pricing: HourlyPricing = field(default_factory=HourlyPricing)
    tickets: dict = field(default_factory=dict)
    _ids: itertools.count = field(default_factory=lambda: itertools.count(1))

    def park(self, plate, size, now):
        slot = next((s for s in self.slots if s.vehicle is None and s.size == size), None)
        if slot is None:
            raise ParkingFull(f"no free {size.name} slot")
        slot.vehicle = plate
        ticket = Ticket(next(self._ids), plate, slot, now)
        self.tickets[ticket.id] = ticket
        return ticket

    def unpark(self, ticket_id, now):
        ticket = self.tickets.pop(ticket_id)
        ticket.slot.vehicle = None
        return self.pricing.fee(ticket.slot.size, (now - ticket.entered_at) / 3600)

    def free(self):
        return {size: sum(1 for s in self.slots if s.vehicle is None and s.size == size) for size in Size}


lot = ParkingLot([Slot(1, 1, Size.CAR), Slot(1, 2, Size.BIKE), Slot(2, 1, Size.CAR)])
t = lot.park("KA01", Size.CAR, now=0)
assert lot.free()[Size.CAR] == 1
assert lot.unpark(t.id, now=2.5 * 3600) == 60  # 3 started hours × 20
```

Extensions to discuss: a slot-finding strategy (nearest to the entrance; a min-heap per size instead of a linear scan), larger slots accepting smaller vehicles, concurrency (two cars racing for one slot → a lock per floor, or an atomic compare-and-set on the slot), and events for display boards (Observer).

## 🔹 Machine Coding 2: Splitwise (expense sharing)

Requirements: add an expense paid by one user and split equally, by exact amounts or by percentage; show balances; settle up with the fewest transfers.

```python
from collections import defaultdict


class InvalidSplit(Exception):
    pass


def equal(amount, users, _):
    share, extra = divmod(round(amount * 100), len(users))  # work in paise to avoid float drift
    return {u: (share + (1 if i < extra else 0)) / 100 for i, u in enumerate(users)}


def exact(amount, users, values):
    if round(sum(values) * 100) != round(amount * 100):
        raise InvalidSplit("exact amounts must add up to the total")
    return dict(zip(users, values))


def percent(amount, users, values):
    if round(sum(values), 6) != 100:
        raise InvalidSplit("percentages must add up to 100")
    return {u: round(amount * p / 100, 2) for u, p in zip(users, values)}


class Ledger:
    def __init__(self):
        self.net = defaultdict(float)  # > 0: is owed money, < 0: owes money

    def add_expense(self, payer, amount, users, split=equal, values=None):
        for user, owed in split(amount, users, values).items():
            self.net[user] -= owed
        self.net[payer] += amount

    def settle(self):
        """Fewest transfers (greedy): the biggest debtor pays the biggest creditor."""
        debtors = sorted((v, u) for u, v in self.net.items() if v < -0.005)
        creditors = sorted(((-v, u) for u, v in self.net.items() if v > 0.005))
        transfers = []
        while debtors and creditors:
            debt, d = debtors.pop(0)
            credit, c = creditors.pop(0)
            paid = round(min(-debt, -credit), 2)
            transfers.append((d, c, paid))
            if round(-debt - paid, 2) > 0:
                debtors.insert(0, (debt + paid, d))
            if round(-credit - paid, 2) > 0:
                creditors.insert(0, (credit + paid, c))
        return transfers


ledger = Ledger()
ledger.add_expense("asha", 300, ["asha", "ben", "chen"])
ledger.add_expense("ben", 100, ["asha", "ben"], split=exact, values=[60, 40])
assert ledger.settle() == [("chen", "asha", 100.0), ("ben", "asha", 40.0)]
```

Talking points: money as integer paise (never floats in production), the split rules as a strategy (adding "shares" is one function), groups, an expense history so balances can be recomputed, and why the greedy settle isn't always optimal (true minimum transfers is NP-hard; greedy is the standard answer).

## 🔹 Machine Coding 3: In-Memory Key-Value Store with TTL

Requirements: `set(key, value, ttl=None)`, `get`, `delete`, keys expire; bonus `transactions` (begin / rollback / commit).

```python
import heapq


class KVStore:
    def __init__(self, clock):
        self.clock = clock  # injected, so tests control time
        self.data = {}  # key -> (value, expires_at or None)
        self.expiry = []  # min-heap of (expires_at, key) for active cleanup
        self.txns = []  # stack of {key: previous (value, expiry) or None} undo logs

    def set(self, key, value, ttl=None):
        self._remember(key)
        expires = self.clock() + ttl if ttl else None
        self.data[key] = (value, expires)
        if expires:
            heapq.heappush(self.expiry, (expires, key))

    def get(self, key):
        item = self.data.get(key)
        if item is None or (item[1] is not None and item[1] <= self.clock()):
            self.data.pop(key, None)  # lazy expiry on read
            return None
        return item[0]

    def delete(self, key):
        self._remember(key)
        self.data.pop(key, None)

    def purge(self):  # active expiry: call periodically
        while self.expiry and self.expiry[0][0] <= self.clock():
            expires, key = heapq.heappop(self.expiry)
            if key in self.data and self.data[key][1] == expires:
                del self.data[key]

    def begin(self):
        self.txns.append({})

    def rollback(self):
        for key, old in self.txns.pop().items():
            if old is None:
                self.data.pop(key, None)
            else:
                self.data[key] = old

    def commit(self):
        undo = self.txns.pop()
        if self.txns:  # nested: the outer transaction must still be able to undo these keys
            for key, old in undo.items():
                self.txns[-1].setdefault(key, old)

    def _remember(self, key):
        if self.txns and key not in self.txns[-1]:
            self.txns[-1][key] = self.data.get(key)


now = [0]
kv = KVStore(clock=lambda: now[0])
kv.set("a", 1, ttl=10)
kv.begin(); kv.set("a", 2); kv.rollback()
assert kv.get("a") == 1
now[0] = 11
assert kv.get("a") is None
```

Talking points: lazy vs active expiry (Redis does both), why the clock is injected, the undo-log approach to transactions, thread safety (one lock, or sharded locks by key hash), and an LRU size limit ([146. LRU Cache](../Design/146.LRU_Cache.md)).

## 🔹 More to Practise (same approach)

Snake and Ladder · Elevator system (State + scheduling strategy) · Movie ticket booking (seat locking with expiry) · Library management · Vending machine (State) · Logger/rate limiter · Tic-tac-toe with an N×N board. For each: write the class list in 5 minutes, then code the core flow in 45.
