"""R14 - Special methods and protocols (reference solutions)

Compare after you've made your own attempt. Run: python check.py 14 -s
"""
import functools
import itertools
import math

PREDICT = r"""
>>> class P:
...     def __init__(self, x):
...         self.x = x
...     def __eq__(self, other):
...         return self.x == other.x
>>> P(1) == P(1)
True
>>> {P(1)}
TypeError

>>> class W:
...     def __init__(self, v):
...         self.v = v
...     def __lt__(self, other):
...         return self.v < other.v
...     def __repr__(self):
...         return f'W({self.v})'
>>> sorted([W(3), W(1), W(2)])
[W(1), W(2), W(3)]
>>> max([W(3), W(1)])
W(3)
>>> W(1) > W(2)
False
>>> W(1) <= W(2)
TypeError

>>> class V:
...     def __init__(self, x, y):
...         self.x, self.y = x, y
...     def __iter__(self):
...         yield self.x
...         yield self.y
>>> a, b = V(3, 4)
>>> a, b, list(V(1, 2)), max(V(5, 9))
(3, 4, [1, 2], 9)

>>> class Squares:
...     def __getitem__(self, i):
...         if i >= 5:
...             raise IndexError
...         return i * i
>>> list(Squares())
[0, 1, 4, 9, 16]
>>> 9 in Squares(), 10 in Squares()
(True, False)

>>> class Echo:
...     def __getitem__(self, key):
...         return key
>>> e = Echo()
>>> e[3], e[1:5], e[::2], e[1, 2]
(3, slice(1, 5, None), slice(None, None, 2), (1, 2))

>>> class Bag:
...     def __init__(self, items):
...         self.items = items
...     def __len__(self):
...         return len(self.items)
>>> bool(Bag([])), bool(Bag([0])), len(Bag('abc'))
(False, True, 3)

>>> class Odd:
...     def __bool__(self):
...         return False
...     def __len__(self):
...         return 5
>>> bool(Odd()), len(Odd())
(False, 5)

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
Money(3)
>>> sum([Money(1), Money(2)])
TypeError
>>> sum([Money(1), Money(2)], Money(0))
Money(3)

>>> class Num:
...     def __init__(self, v):
...         self.v = v
...     def __add__(self, other):
...         return Num(self.v + (other.v if isinstance(other, Num) else other))
...     __radd__ = __add__
...     def __repr__(self):
...         return f'Num({self.v})'
>>> 1 + Num(2), sum([Num(1), Num(2), Num(3)])
(Num(3), Num(6))

>>> class E:
...     def __eq__(self, other):
...         return NotImplemented
>>> e = E()
>>> e == e, e == E(), e != e
(True, False, False)

>>> class Key:
...     def __init__(self, k):
...         self.k = k
...     def __eq__(self, other):
...         return self.k == other.k
...     def __hash__(self):
...         return hash(self.k)
>>> d = {Key(1): 'one'}
>>> d[Key(1)], Key(2) in d
('one', False)

>>> class Evens:
...     def __contains__(self, x):
...         return x % 2 == 0
>>> 4 in Evens(), 3 in Evens(), 3 not in Evens()
(True, False, True)

>>> class Adder:
...     def __init__(self, n):
...         self.n = n
...     def __call__(self, x):
...         return x + self.n
>>> add5 = Adder(5)
>>> add5(10), callable(add5), list(map(add5, [1, 2]))
(15, True, [6, 7])

>>> class M:
...     def __init__(self, v):
...         self.v = v
...     def __matmul__(self, other):
...         return M(self.v * other.v)
...     def __repr__(self):
...         return f'M({self.v})'
>>> M(2) @ M(3)
M(6)
>>> a = M(2)
>>> a @= M(5)
>>> a
M(10)

>>> class T:
...     def __init__(self, name):
...         self.name = name
>>> h = []
>>> heappush(h, (2, T('b')))
>>> heappush(h, (1, T('a')))
>>> heappop(h)[1].name
'a'
>>> heappush(h, (2, T('c')))
TypeError

>>> class Rev:
...     def __init__(self, s):
...         self.s = s
...     def __lt__(self, other):
...         return self.s > other.s
>>> h = [Rev(s) for s in ['kiwi', 'apple', 'pear']]
>>> heapify(h)
>>> heappop(h).s, heappop(h).s
('pear', 'kiwi')

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
(True, False, True)
"""


class Vec2:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return f"Vec2({self.x}, {self.y})"

    def __add__(self, other):
        if not isinstance(other, Vec2):
            return NotImplemented
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Vec2):
            return NotImplemented
        return Vec2(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    def __mul__(self, k):
        if not isinstance(k, int):
            return NotImplemented
        return Vec2(self.x * k, self.y * k)

    __rmul__ = __mul__

    def __eq__(self, other):
        if not isinstance(other, Vec2):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __iter__(self):
        yield self.x
        yield self.y

    def __abs__(self):
        return math.hypot(self.x, self.y)


@functools.total_ordering
class Frac:
    def __init__(self, num, den=1):
        if den == 0:
            raise ZeroDivisionError("zero denominator")
        if den < 0:
            num, den = -num, -den
        g = math.gcd(num, den)
        self.num, self.den = num // g, den // g

    @staticmethod
    def _coerce(other):
        if isinstance(other, Frac):
            return other
        if isinstance(other, int):
            return Frac(other)
        return None

    def __repr__(self):
        return f"Frac({self.num}, {self.den})"

    def __add__(self, other):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return Frac(self.num * o.den + o.num * self.den, self.den * o.den)

    __radd__ = __add__

    def __sub__(self, other):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return Frac(self.num * o.den - o.num * self.den, self.den * o.den)

    def __mul__(self, other):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return Frac(self.num * o.num, self.den * o.den)

    def __truediv__(self, other):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return Frac(self.num * o.den, self.den * o.num)

    def __eq__(self, other):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return (self.num, self.den) == (o.num, o.den)

    def __lt__(self, other):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return self.num * o.den < o.num * self.den      # cross-multiply: dens are positive

    def __hash__(self):
        # must agree with __eq__: Frac(2, 1) == 2, so it has to hash like 2
        return hash(self.num) if self.den == 1 else hash((self.num, self.den))

    def __float__(self):
        return self.num / self.den


class Matrix:
    def __init__(self, rows, mod=None):
        self.mod = mod
        self.rows = [[x % mod if mod else x for x in row] for row in rows]

    @classmethod
    def identity(cls, n, mod=None):
        return cls([[int(i == j) for j in range(n)] for i in range(n)], mod)

    def __matmul__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented
        if len(self.rows[0]) != len(other.rows):
            raise ValueError("width of the left matrix must equal height of the right")
        cols = list(zip(*other.rows))
        rows = [[sum(a * b for a, b in zip(row, col)) for col in cols] for row in self.rows]
        return Matrix(rows, self.mod)

    def __pow__(self, k):
        result, base = Matrix.identity(len(self.rows), self.mod), self
        while k:
            if k & 1:
                result = result @ base
            base = base @ base
            k >>= 1
        return result

    def __eq__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented
        return self.rows == other.rows and self.mod == other.mod

    def __repr__(self):
        extra = f", mod={self.mod}" if self.mod else ""
        return f"Matrix({self.rows}{extra})"


def fib_mod(n, mod=10**9 + 7):
    return (Matrix([[1, 1], [1, 0]], mod) ** n).rows[0][1]


class CircularBuffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self._data = [None] * capacity
        self._start = 0
        self._size = 0

    def append(self, x):
        end = (self._start + self._size) % self.capacity
        self._data[end] = x
        if self._size == self.capacity:
            self._start = (self._start + 1) % self.capacity   # overwrote the oldest
        else:
            self._size += 1

    def __len__(self):
        return self._size

    def __getitem__(self, i):
        if i < 0:
            i += self._size
        if not 0 <= i < self._size:
            raise IndexError("CircularBuffer index out of range")
        return self._data[(self._start + i) % self.capacity]

    def __iter__(self):
        for i in range(self._size):
            yield self[i]

    def __contains__(self, x):
        return any(item == x for item in self)

    def __repr__(self):
        return f"CircularBuffer({list(self)}, capacity={self.capacity})"


class Task:
    _counter = itertools.count()

    def __init__(self, priority, name):
        self.priority = priority
        self.name = name
        self.seq = next(Task._counter)

    def __lt__(self, other):
        return (self.priority, self.seq) < (other.priority, other.seq)

    def __repr__(self):
        return f"Task({self.priority}, {self.name!r})"


class Reverse:
    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        return self.value > other.value

    def __eq__(self, other):
        if not isinstance(other, Reverse):
            return NotImplemented
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)


class Memo:
    def __init__(self, fn):
        self.fn = fn
        self.cache = {}
        self.hits = self.misses = 0

    def __call__(self, *args):
        if args in self.cache:
            self.hits += 1
        else:
            self.misses += 1
            self.cache[args] = self.fn(*args)
        return self.cache[args]

    def __len__(self):
        return len(self.cache)

    def clear(self):
        self.cache.clear()
        self.hits = self.misses = 0


class Bits:
    def __init__(self, items=()):
        self.mask = 0
        for i in items:
            self.add(i)

    @classmethod
    def _from_mask(cls, mask):
        b = cls()
        b.mask = mask
        return b

    def add(self, i):
        self.mask |= 1 << i

    def discard(self, i):
        self.mask &= ~(1 << i)

    def __contains__(self, i):
        return self.mask >> i & 1 == 1

    def __len__(self):
        return self.mask.bit_count()

    def __iter__(self):
        m = self.mask
        while m:
            low = m & -m                # lowest set bit
            yield low.bit_length() - 1
            m ^= low

    def __or__(self, other):
        return Bits._from_mask(self.mask | other.mask)

    def __and__(self, other):
        return Bits._from_mask(self.mask & other.mask)

    def __sub__(self, other):
        return Bits._from_mask(self.mask & ~other.mask)

    def __eq__(self, other):
        if not isinstance(other, Bits):
            return NotImplemented
        return self.mask == other.mask

    def __hash__(self):
        return hash(self.mask)

    def __repr__(self):
        return f"Bits({list(self)})"
