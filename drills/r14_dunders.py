"""R14 - Special methods and protocols

Operators and built-ins call "dunder" methods: a + b calls a.__add__(b), and
if that returns NotImplemented Python tries b.__radd__(a), then raises
TypeError. len(), bool(), in, iteration, indexing, calling and @ all work the
same way (__len__, __bool__, __contains__, __iter__, __getitem__, __call__,
__matmul__). Defining __eq__ removes __hash__, so equal objects must also get
a matching __hash__ to be dict keys. sorted, min, max and heapq only need
__lt__; functools.total_ordering fills in <=, > and >= from __eq__ + __lt__.

Part 1 - Predict. Each block in PREDICT is a REPL session. Replace every ???
with exactly what Python prints: expression values are echoed the way the REPL
echoes them, and a line that raises prints just the exception name (TypeError).

Part 2 - Drills. Implement every class and function until `python check.py 14`
is green. Don't edit the tests at the bottom; add your own test_* functions if
you like.

Unlocks: custom heap ordering, geometry with vector types, matrix power for
linear recurrences, and hashable state objects.
"""
import functools
import heapq
import itertools
import math
import random

PREDICT = r"""
>>> class P:
...     def __init__(self, x):
...         self.x = x
...     def __eq__(self, other):
...         return self.x == other.x
>>> P(1) == P(1)
???
>>> {P(1)}
???

>>> class W:
...     def __init__(self, v):
...         self.v = v
...     def __lt__(self, other):
...         return self.v < other.v
...     def __repr__(self):
...         return f'W({self.v})'
>>> sorted([W(3), W(1), W(2)])
???
>>> max([W(3), W(1)])
???
>>> W(1) > W(2)
???
>>> W(1) <= W(2)
???

>>> class V:
...     def __init__(self, x, y):
...         self.x, self.y = x, y
...     def __iter__(self):
...         yield self.x
...         yield self.y
>>> a, b = V(3, 4)
>>> a, b, list(V(1, 2)), max(V(5, 9))
???

>>> class Squares:
...     def __getitem__(self, i):
...         if i >= 5:
...             raise IndexError
...         return i * i
>>> list(Squares())
???
>>> 9 in Squares(), 10 in Squares()
???

>>> class Echo:
...     def __getitem__(self, key):
...         return key
>>> e = Echo()
>>> e[3], e[1:5], e[::2], e[1, 2]
???

>>> class Bag:
...     def __init__(self, items):
...         self.items = items
...     def __len__(self):
...         return len(self.items)
>>> bool(Bag([])), bool(Bag([0])), len(Bag('abc'))
???

>>> class Odd:
...     def __bool__(self):
...         return False
...     def __len__(self):
...         return 5
>>> bool(Odd()), len(Odd())
???

>>> class Money:
...     def __init__(self, c):
...         self.c = c
...     def __add__(self, other):
...         if isinstance(other, Money):
...             return Money(self.c + other.c)
...         return NotImplemented
...     def __repr__(self):
...         return f'Money({self.c})'
>>> Money(1) + Money(2)
???
>>> sum([Money(1), Money(2)])
???
>>> sum([Money(1), Money(2)], Money(0))
???

>>> class Num:
...     def __init__(self, v):
...         self.v = v
...     def __add__(self, other):
...         return Num(self.v + (other.v if isinstance(other, Num) else other))
...     __radd__ = __add__
...     def __repr__(self):
...         return f'Num({self.v})'
>>> 1 + Num(2), sum([Num(1), Num(2), Num(3)])
???

>>> class E:
...     def __eq__(self, other):
...         return NotImplemented
>>> e = E()
>>> e == e, e == E(), e != e
???

>>> class Key:
...     def __init__(self, k):
...         self.k = k
...     def __eq__(self, other):
...         return self.k == other.k
...     def __hash__(self):
...         return hash(self.k)
>>> d = {Key(1): 'one'}
>>> d[Key(1)], Key(2) in d
???

>>> class Evens:
...     def __contains__(self, x):
...         return x % 2 == 0
>>> 4 in Evens(), 3 in Evens(), 3 not in Evens()
???

>>> class Adder:
...     def __init__(self, n):
...         self.n = n
...     def __call__(self, x):
...         return x + self.n
>>> add5 = Adder(5)
>>> add5(10), callable(add5), list(map(add5, [1, 2]))
???

>>> class M:
...     def __init__(self, v):
...         self.v = v
...     def __matmul__(self, other):
...         return M(self.v * other.v)
...     def __repr__(self):
...         return f'M({self.v})'
>>> M(2) @ M(3)
???
>>> a = M(2)
>>> a @= M(5)
>>> a
???

>>> class T:
...     def __init__(self, name):
...         self.name = name
>>> h = []
>>> heappush(h, (2, T('b')))
>>> heappush(h, (1, T('a')))
>>> heappop(h)[1].name
???
>>> heappush(h, (2, T('c')))
???

>>> class Rev:
...     def __init__(self, s):
...         self.s = s
...     def __lt__(self, other):
...         return self.s > other.s
>>> h = [Rev(s) for s in ['kiwi', 'apple', 'pear']]
>>> heapify(h)
>>> heappop(h).s, heappop(h).s
???

>>> from functools import total_ordering
>>> @total_ordering
... class Ver:
...     def __init__(self, n):
...         self.n = n
...     def __eq__(self, other):
...         return self.n == other.n
...     def __lt__(self, other):
...         return self.n < other.n
>>> Ver(1) <= Ver(1), Ver(2) >= Ver(3), Ver(2) > Ver(1)
???
"""


# ---------------------------------------------------------------- drills

class Vec2:
    """A 2D integer vector.
    - Vec2(x, y); repr(Vec2(1, -2)) == 'Vec2(1, -2)'
    - v + w and v - w (both Vec2), -v, and v * k and k * v for an int k
    - v == w compares coordinates; equal vectors hash equally (dict keys work)
    - x, y = v unpacks (implement __iter__)
    - abs(v) is the Euclidean length: abs(Vec2(3, 4)) == 5.0
    - Unsupported operands (v + 1, v * v) raise TypeError: return
      NotImplemented from the method and Python raises it for you."""

    def __init__(self, x, y):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError

    def __add__(self, other):
        raise NotImplementedError

    def __sub__(self, other):
        raise NotImplementedError

    def __neg__(self):
        raise NotImplementedError

    def __mul__(self, k):
        raise NotImplementedError

    def __rmul__(self, k):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    def __hash__(self):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def __abs__(self):
        raise NotImplementedError


class Frac:
    """An exact fraction kept in lowest terms with a positive denominator:
    Frac(2, -4) has .num == -1 and .den == 2. Frac(n) means n/1, and a zero
    denominator raises ZeroDivisionError.
    - +, -, *, / with a Frac or an int on the right; sum() of Fracs works
      (sum starts from 0, so 0 + Frac needs __radd__). Any other operand type
      (float, str) raises TypeError: return NotImplemented.
    - ==, <, <=, >, >= against a Frac or an int (Frac(4, 2) == 2): write
      __eq__ and __lt__ and decorate the class with @functools.total_ordering.
    - Equal values hash equally, including hash(Frac(n, 1)) == hash(n).
    - repr(Frac(1, 2)) == 'Frac(1, 2)'; float(Frac(1, 4)) == 0.25."""

    def __init__(self, num, den=1):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError

    def __add__(self, other):
        raise NotImplementedError

    def __radd__(self, other):
        raise NotImplementedError

    def __sub__(self, other):
        raise NotImplementedError

    def __mul__(self, other):
        raise NotImplementedError

    def __truediv__(self, other):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    def __lt__(self, other):
        raise NotImplementedError

    def __hash__(self):
        raise NotImplementedError

    def __float__(self):
        raise NotImplementedError


class Matrix:
    """A matrix of ints, optionally reduced modulo `mod` after every operation.
    - Matrix(rows, mod=None): rows is a list of equal-length lists; store a
      copy (reduced mod `mod` when it's set) in .rows.
    - Matrix.identity(n, mod=None): classmethod.
    - A @ B: the matrix product; A's width must equal B's height, else
      ValueError. The result keeps A's mod.
    - A ** k: square A and int k >= 0, by binary exponentiation (O(log k)
      multiplications); A ** 0 is the identity.
    - A == B compares rows and mod.
    - repr(Matrix([[1, 2]])) == 'Matrix([[1, 2]])', and with a modulus
      repr(Matrix([[9]], mod=7)) == 'Matrix([[2]], mod=7)'."""

    def __init__(self, rows, mod=None):
        raise NotImplementedError

    @classmethod
    def identity(cls, n, mod=None):
        raise NotImplementedError

    def __matmul__(self, other):
        raise NotImplementedError

    def __pow__(self, k):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError


def fib_mod(n, mod=10**9 + 7):
    """The n-th Fibonacci number modulo mod (F(0) = 0, F(1) = 1) for n up to
    10**18, using your Matrix:
    [[1, 1], [1, 0]] ** n == [[F(n+1), F(n)], [F(n), F(n-1)]]."""
    raise NotImplementedError


class CircularBuffer:
    """A fixed-capacity buffer that keeps the most recent `capacity` items.
    - append(x): add x; when full, the oldest item is dropped.
    - len(buf); bool(buf) is False when empty.
    - buf[i]: 0 is the oldest item and -1 the newest; IndexError outside the range.
    - iteration goes oldest -> newest, and `x in buf` works.
    - repr(buf) == 'CircularBuffer([2, 3], capacity=3)'
    Use a fixed-size list plus a start index: no list.pop(0), no deque."""

    def __init__(self, capacity):
        raise NotImplementedError

    def append(self, x):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def __getitem__(self, i):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def __contains__(self, x):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError


class Task:
    """A heap entry: Task(priority, name), smaller priority first, and equal
    priorities in creation order (first in, first out).
    - t1 < t2 compares (priority, creation number); give each Task a creation
      number from a class-level counter (itertools.count()). Names are never
      compared, so they can be anything.
    - repr(Task(2, 'write')) == "Task(2, 'write')"."""

    def __init__(self, priority, name):
        raise NotImplementedError

    def __lt__(self, other):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError


class Reverse:
    """Wraps a value and flips its ordering: Reverse(a) < Reverse(b) exactly
    when a > b. Reverse(a) == Reverse(b) exactly when a == b, equal wrappers
    hash equally, and .value holds the wrapped value.
    Use it for a max-heap of anything comparable, or to sort one field
    descending inside a tuple key: sorted(pairs, key=lambda p: (Reverse(p[0]), p[1]))."""

    def __init__(self, value):
        raise NotImplementedError

    def __lt__(self, other):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    def __hash__(self):
        raise NotImplementedError


class Memo:
    """A callable cache around a function: Memo(fn)(*args) returns fn(*args),
    computing it only the first time those args are seen.
    - .hits and .misses count cache hits and misses
    - len(memo) is how many results are cached
    - memo.clear() empties the cache and resets both counters
    Arguments are positional and hashable."""

    def __init__(self, fn):
        raise NotImplementedError

    def __call__(self, *args):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError


class Bits:
    """A set of small non-negative ints stored in ONE int bitmask.
    - Bits(iterable=()); .mask is the int: Bits([0, 3]).mask == 0b1001
    - add(i) and discard(i) change it in place; `i in b`; len(b) counts members
    - iteration yields members in increasing order
    - b | c, b & c and b - c return NEW Bits (union, intersection, difference)
    - b == c compares members, and equal sets hash equally
    - repr(Bits([3, 0])) == 'Bits([0, 3])'"""

    def __init__(self, items=()):
        raise NotImplementedError

    def add(self, i):
        raise NotImplementedError

    def discard(self, i):
        raise NotImplementedError

    def __contains__(self, i):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def __or__(self, other):
        raise NotImplementedError

    def __and__(self, other):
        raise NotImplementedError

    def __sub__(self, other):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    def __hash__(self):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError


# ---------------------------------------------------------------- tests (don't edit)

def _raises(exc, fn):
    try:
        fn()
    except exc:
        return True
    return False


def _fib_pair(n, mod):
    """(F(n), F(n+1)) mod `mod` by fast doubling, independent of Matrix."""
    if n == 0:
        return 0, 1
    a, b = _fib_pair(n >> 1, mod)
    c = a * ((2 * b - a) % mod) % mod
    d = (a * a + b * b) % mod
    return (d, (c + d) % mod) if n & 1 else (c, d)


def test_vec2():
    a, b = Vec2(1, 2), Vec2(3, -1)
    assert repr(a) == 'Vec2(1, 2)'
    assert a + b == Vec2(4, 1) and a - b == Vec2(-2, 3) and -a == Vec2(-1, -2)
    assert a * 3 == Vec2(3, 6) and 3 * a == Vec2(3, 6), "k * v needs __rmul__"
    assert a == Vec2(1, 2) and a != b and (a == (1, 2)) is False
    seen = {Vec2(0, 0): 'origin'}
    assert seen[Vec2(0, 0)] == 'origin', "equal vectors must hash equally"
    x, y = b
    assert (x, y) == (3, -1) and list(a) == [1, 2]
    assert abs(Vec2(3, 4)) == 5.0
    for bad in (lambda: a + 1, lambda: a * a, lambda: 'x' * a):
        assert _raises(TypeError, bad), "unsupported operands must raise TypeError (return NotImplemented)"
    steps = [Vec2(0, 1), Vec2(1, 0), Vec2(0, -1), Vec2(-1, 0)]
    assert sorted(tuple(Vec2(2, 2) + d) for d in steps) == [(1, 2), (2, 1), (2, 3), (3, 2)]


def test_frac():
    h = Frac(2, -4)
    assert (h.num, h.den) == (-1, 2) and repr(h) == 'Frac(-1, 2)'
    assert repr(Frac(0, 7)) == 'Frac(0, 1)' and repr(Frac(5)) == 'Frac(5, 1)'
    assert _raises(ZeroDivisionError, lambda: Frac(1, 0))
    a, b = Frac(1, 2), Frac(1, 3)
    assert a + b == Frac(5, 6) and a - b == Frac(1, 6) and a * b == Frac(1, 6) and a / b == Frac(3, 2)
    assert a + 1 == Frac(3, 2) and a * 4 == 2 and Frac(4, 2) == 2
    assert sum([Frac(1, 2), Frac(1, 3), Frac(1, 6)]) == 1, "sum() starts at 0: 0 + Frac needs __radd__"
    assert b < a and a > b and a <= Frac(2, 4) and a >= b and not (a < a), "use total_ordering for <=, >, >="
    assert Frac(1, 2) < 1 and 1 > Frac(1, 2)
    assert sorted([Frac(2, 3), Frac(-1, 2), Frac(1, 3)]) == [Frac(-1, 2), Frac(1, 3), Frac(2, 3)]
    assert len({Frac(1, 2), Frac(2, 4), Frac(-3, -6)}) == 1, "equal fractions must hash equally"
    assert hash(Frac(6, 3)) == hash(2) and {2: 'two'}[Frac(4, 2)] == 'two'
    assert float(Frac(1, 4)) == 0.25
    total = Frac(0)
    for k in range(1, 50):
        total = total + Frac(1, k * (k + 1))
    assert total == Frac(49, 50), "telescoping sum: did you reduce by the gcd?"
    assert _raises(TypeError, lambda: a + 0.5), "Frac + float should be unsupported (return NotImplemented)"


def test_matrix():
    A = Matrix([[1, 2], [3, 4]])
    B = Matrix([[0, 1], [1, 0]])
    assert A @ B == Matrix([[2, 1], [4, 3]]) and B @ A == Matrix([[3, 4], [1, 2]])
    assert repr(A) == 'Matrix([[1, 2], [3, 4]])' and repr(Matrix([[9]], mod=7)) == 'Matrix([[2]], mod=7)'
    assert Matrix([[1, 2, 3]]) @ Matrix([[1], [1], [1]]) == Matrix([[6]])
    assert _raises(ValueError, lambda: A @ Matrix([[1, 2, 3]])), "a width/height mismatch must raise ValueError"
    assert A ** 0 == Matrix.identity(2) and A ** 1 == A and A ** 3 == A @ A @ A
    assert Matrix([[2, 0], [0, 3]], mod=5) ** 4 == Matrix([[1, 0], [0, 1]], mod=5)
    rows = [[1, 2], [3, 4]]
    C = Matrix(rows)
    rows[0][0] = 99
    assert C == Matrix([[1, 2], [3, 4]]), "store a copy of the rows"


def test_fib_mod():
    a, b = 0, 1
    for n in range(30):
        assert fib_mod(n) == a, f"fib_mod({n})"
        a, b = b, a + b
    assert fib_mod(90, 10**18) == 2880067194370816120 % 10**18
    for n in (10**18, 10**18 + 1, 123456789123456789):
        assert fib_mod(n) == _fib_pair(n, 10**9 + 7)[0], f"fib_mod({n})"


def test_circular_buffer():
    buf = CircularBuffer(3)
    assert len(buf) == 0 and not buf and list(buf) == []
    for x in (1, 2):
        buf.append(x)
    assert buf and len(buf) == 2 and list(buf) == [1, 2] and buf[0] == 1 and buf[-1] == 2
    for x in (3, 4, 5):
        buf.append(x)
    assert list(buf) == [3, 4, 5], "the oldest items must be dropped when full"
    assert (buf[0], buf[1], buf[2], buf[-1], buf[-3]) == (3, 4, 5, 5, 3)
    assert 4 in buf and 1 not in buf
    assert repr(buf) == 'CircularBuffer([3, 4, 5], capacity=3)'
    for i in (3, -4):
        assert _raises(IndexError, lambda: buf[i]), f"buf[{i}] must raise IndexError"
    rng = random.Random(14)
    ref, big = [], CircularBuffer(5)
    for _ in range(200):
        x = rng.randint(0, 99)
        ref.append(x)
        big.append(x)
        assert list(big) == ref[-5:]
    assert [big[i] for i in range(-5, 5)] == ref[-5:] * 2


def test_task():
    assert repr(Task(2, 'write')) == "Task(2, 'write')"
    h = []
    for p, name in [(2, 'b'), (1, 'a'), (2, 'c'), (0, 'z'), (1, 'd'), (2, 'e')]:
        heapq.heappush(h, Task(p, name))
    order = [heapq.heappop(h).name for _ in range(len(h))]
    assert order == ['z', 'a', 'd', 'b', 'c', 'e'], "equal priorities must pop in creation order"

    class Unorderable:
        pass

    x, y = Task(5, Unorderable()), Task(5, Unorderable())
    assert x < y and not (y < x), "never compare names; compare (priority, creation number)"
    assert sorted([Task(3, 'q'), Task(1, 'r')])[0].name == 'r'


def test_reverse():
    h = [Reverse(w) for w in ['kiwi', 'apple', 'pear', 'fig']]
    heapq.heapify(h)
    assert [heapq.heappop(h).value for _ in range(4)] == ['pear', 'kiwi', 'fig', 'apple']
    pairs = [('b', 2), ('a', 1), ('b', 1), ('a', 3)]
    got = sorted(pairs, key=lambda p: (Reverse(p[0]), p[1]))
    assert got == [('b', 1), ('b', 2), ('a', 1), ('a', 3)], \
        "tuples compare with == before <: without __eq__, ties on the first field never reach the second"
    assert Reverse(3) == Reverse(3) and Reverse(3) != Reverse(4) and len({Reverse(1), Reverse(1)}) == 1
    assert max([Reverse(5), Reverse(2), Reverse(9)]).value == 2


def test_memo():
    calls = []

    def slow_fib(n):
        calls.append(n)
        return n if n < 2 else fib(n - 1) + fib(n - 2)

    fib = Memo(slow_fib)
    assert fib(30) == 832040
    assert len(calls) == 31, "each n should be computed exactly once"
    assert fib.misses == 31 and len(fib) == 31 and fib.hits == 28
    assert fib(30) == 832040 and fib.hits == 29 and len(calls) == 31
    assert callable(fib)
    fib.clear()
    assert len(fib) == 0 and fib.hits == fib.misses == 0
    add = Memo(lambda a, b: a + b)
    assert add(1, 2) == 3 and add(2, 1) == 3 and add.misses == 2
    assert add(1, 2) == 3 and add.hits == 1


def test_bits():
    b = Bits([3, 0])
    assert b.mask == 0b1001 and repr(b) == 'Bits([0, 3])' and len(b) == 2
    assert 3 in b and 1 not in b and list(b) == [0, 3]
    b.add(5)
    b.add(5)
    b.discard(0)
    b.discard(9)
    assert list(b) == [3, 5] and b.mask == 0b101000
    c = Bits([1, 3, 6])
    assert list(b | c) == [1, 3, 5, 6] and list(b & c) == [3] and list(b - c) == [5]
    assert list(b) == [3, 5] and list(c) == [1, 3, 6], "| & - must return new Bits, not change the operands"
    assert Bits([1, 2]) == Bits([2, 1]) and Bits([1]) != Bits([2])
    assert len({Bits([1, 2]), Bits([2, 1])}) == 1
    assert len(Bits()) == 0 and list(Bits()) == [] and repr(Bits()) == 'Bits([])'
    rng = random.Random(14)
    for _ in range(50):
        xs = {rng.randrange(60) for _ in range(rng.randrange(10))}
        ys = {rng.randrange(60) for _ in range(rng.randrange(10))}
        bx, by = Bits(xs), Bits(ys)
        assert list(bx) == sorted(xs) and len(bx) == len(xs)
        assert list(bx | by) == sorted(xs | ys)
        assert list(bx & by) == sorted(xs & ys) and list(bx - by) == sorted(xs - ys)
