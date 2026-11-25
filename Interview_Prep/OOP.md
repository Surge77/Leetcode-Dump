# 🔹 OOP for the Infosys Technical Interview

Interviewers usually ask you to **define** a concept, **show** it in code, and say **why** it matters. Examples are in Python (each block runs and checks itself with `assert`; `tools/verify` executes them); the Java equivalent is noted where the languages differ.

## 🔹 The Four Pillars

### 1. Encapsulation — bundle data with the methods that guard it

```python
class BankAccount:
    def __init__(self, owner: str, balance: int = 0):
        self.owner = owner
        self._balance = balance  # "_" = internal by convention

    @property
    def balance(self) -> int:  # read-only from outside
        return self._balance

    def deposit(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self._balance += amount


acct = BankAccount("Asha")
acct.deposit(500)
assert acct.balance == 500
try:
    acct.deposit(-5)
except ValueError:
    pass
else:
    raise AssertionError("invalid deposit was accepted")
```

* **Why:** the object protects its own invariants (balance never changes except through `deposit`).
* **Java:** `private` fields + public getters/setters. Python has no real `private`; `_x` is a convention and `__x` triggers name mangling.

### 2. Abstraction — expose *what* an object does, hide *how*

```python
from abc import ABC, abstractmethod


class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount: int) -> str: ...


class Upi(PaymentMethod):
    def pay(self, amount: int) -> str:
        return f"UPI paid {amount}"


try:
    PaymentMethod()
except TypeError:
    pass  # abstract classes cannot be instantiated
assert Upi().pay(100) == "UPI paid 100"
```

* **Java:** `abstract class` (can have state and implemented methods) or `interface` (a contract; Java 8+ allows `default` methods).

### 3. Inheritance — reuse and extend an existing type ("is-a")

```python
class Employee:
    def __init__(self, name: str, salary: int):
        self.name, self.salary = name, salary

    def annual_pay(self) -> int:
        return 12 * self.salary


class Manager(Employee):
    def __init__(self, name: str, salary: int, bonus: int):
        super().__init__(name, salary)  # reuse the parent's constructor
        self.bonus = bonus

    def annual_pay(self) -> int:  # override
        return super().annual_pay() + self.bonus


assert Manager("Kiran", 100, 50).annual_pay() == 1250
assert isinstance(Manager("Kiran", 1, 1), Employee)
```

* **Java:** single class inheritance (`extends`), multiple interfaces (`implements`). Python allows multiple inheritance and resolves methods with the MRO (C3 linearisation).

### 4. Polymorphism — one interface, many forms

```python
class Shape:
    def area(self) -> float:
        raise NotImplementedError


class Rectangle(Shape):
    def __init__(self, w: float, h: float):
        self.w, self.h = w, h

    def area(self) -> float:
        return self.w * self.h


class Circle(Shape):
    def __init__(self, r: float):
        self.r = r

    def area(self) -> float:
        return 3.14159 * self.r * self.r


shapes = [Rectangle(2, 3), Circle(1)]
assert [round(s.area(), 2) for s in shapes] == [6, 3.14]  # same call, different behaviour
```

* **Runtime polymorphism** = method **overriding** (the call is resolved by the object's actual type).
* **Compile-time polymorphism** = method **overloading** (same name, different parameter lists). Java supports it; Python does not (a later `def` with the same name replaces the earlier one) — use default arguments or `*args` instead.

## 🔹 Frequently Asked Follow-ups

| Question | Short answer |
|---|---|
| Overloading vs overriding? | Overloading: same name, different parameters, same class, resolved at compile time. Overriding: subclass redefines a parent method with the same signature, resolved at runtime. |
| Abstract class vs interface (Java)? | Abstract class: can hold state and constructors, single inheritance. Interface: a contract with no instance state; a class can implement many. |
| Composition vs inheritance? | Composition = "has-a" (an object holds other objects); inheritance = "is-a". Prefer composition when you only need to reuse behaviour — it keeps classes loosely coupled. |
| What is a constructor? | Code that initialises a new object (`__init__` in Python, a method named after the class in Java). Java can overload constructors. |
| `static` members? | Belong to the class, not to an instance (`@staticmethod` / `@classmethod` in Python). |
| `this` / `self`? | The current object; Java passes it implicitly, Python explicitly as the first parameter. |
| `final` (Java)? | Variable: cannot be reassigned. Method: cannot be overridden. Class: cannot be extended. |
| Can a constructor be private? | Yes — used for singletons and factory methods. |

## 🔹 SOLID in One Line Each

* **S**ingle responsibility — a class has one reason to change.
* **O**pen/closed — open for extension, closed for modification (add a new subclass instead of editing a big `if`).
* **L**iskov substitution — a subclass must work wherever its parent is expected.
* **I**nterface segregation — many small interfaces beat one fat one.
* **D**ependency inversion — depend on abstractions, not concrete classes.

```python
from abc import ABC, abstractmethod


class Notifier(ABC):  # abstraction (D) with one job (S)
    @abstractmethod
    def send(self, message: str) -> str: ...


class EmailNotifier(Notifier):
    def send(self, message: str) -> str:
        return f"email: {message}"


class SmsNotifier(Notifier):  # new channel = new class, no edits elsewhere (O)
    def send(self, message: str) -> str:
        return f"sms: {message}"


class OrderService:
    def __init__(self, notifier: Notifier):  # depends on the abstraction (D)
        self.notifier = notifier

    def place(self, item: str) -> str:
        return self.notifier.send(f"order placed: {item}")


assert OrderService(SmsNotifier()).place("book") == "sms: order placed: book"  # any Notifier works (L)
```
