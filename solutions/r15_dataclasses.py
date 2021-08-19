"""R15 - dataclasses, namedtuples, slots, inheritance (reference solutions)

Compare after you've made your own attempt. Run: python check.py 15 -s
"""
import itertools
import tracemalloc
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import NamedTuple

PREDICT = r"""
>>> @dataclass
... class P:
...     x: int
...     y: int = 0
>>> P(1), P(1) == P(1, 0), P(1) is P(1)
(P(x=1, y=0), True, False)

>>> @dataclass
... class Q:
...     x: int
>>> hash(Q(1))
TypeError

>>> @dataclass(frozen=True)
... class F:
...     x: int
>>> f = F(1)
>>> {f: 'ok'}[F(1)]
'ok'
>>> f.x = 2
FrozenInstanceError

>>> @dataclass(frozen=True)
... class G:
...     xs: list
>>> g = G([1])
>>> g.xs.append(2); g
G(xs=[1, 2])
>>> hash(g)
TypeError

>>> @dataclass(order=True)
... class V:
...     major: int
...     minor: int
>>> sorted([V(1, 5), V(0, 9), V(1, 2)])
[V(major=0, minor=9), V(major=1, minor=2), V(major=1, minor=5)]
>>> V(1, 2) < V(1, 10)
True

>>> @dataclass
... class D:
...     xs: list = []
ValueError

>>> @dataclass
... class Bag:
...     items: list = field(default_factory=list)
>>> a, b = Bag(), Bag()
>>> a.items.append(1)
>>> a, b
(Bag(items=[1]), Bag(items=[]))

>>> @dataclass(order=True)
... class Job:
...     priority: int
...     name: str = field(compare=False)
>>> Job(1, 'b') == Job(1, 'a'), Job(2, 'a') > Job(1, 'z')
(True, True)

>>> @dataclass
... class Bad:
...     a: int = 0
...     b: int
TypeError

>>> @dataclass
... class C:
...     x: int
...     y = 5
>>> C(1), C(1).y
(C(x=1), 5)

>>> @dataclass
... class Base:
...     x: int
>>> @dataclass
... class Child(Base):
...     y: int = 0
>>> Child(1, 2), Child(5)
(Child(x=1, y=2), Child(x=5, y=0))

>>> from dataclasses import asdict, astuple, replace
>>> @dataclass
... class Item:
...     name: str
...     qty: int = 1
>>> it = Item('pen', 3)
>>> asdict(it), astuple(it), replace(it, qty=0)
({'name': 'pen', 'qty': 3}, ('pen', 3), Item(name='pen', qty=0))

>>> Point = namedtuple('Point', 'x y')
>>> p = Point(1, 2)
>>> p, p.x, p[1], p == (1, 2)
(Point(x=1, y=2), 1, 2, True)
>>> x, y = p
>>> p._replace(x=9), x + y
(Point(x=9, y=2), 3)
>>> p.x = 5
AttributeError

>>> Point = namedtuple('Point', 'x y')
>>> sorted([Point(2, 1), Point(1, 5), Point(1, 2)])
[Point(x=1, y=2), Point(x=1, y=5), Point(x=2, y=1)]
>>> len({Point(1, 2), (1, 2)}), isinstance(Point(1, 2), tuple), Point._fields
(1, True, ('x', 'y'))

>>> from typing import NamedTuple
>>> class Edge(NamedTuple):
...     u: int
...     v: int
...     w: int = 1
>>> Edge(0, 1), Edge(0, 1, 5).w, Edge(0, 1)._asdict()
(Edge(u=0, v=1, w=1), 5, {'u': 0, 'v': 1, 'w': 1})

>>> class Slim:
...     __slots__ = ('a', 'b')
...     def __init__(self):
...         self.a = 1
>>> s = Slim()
>>> s.b = 2
>>> s.a + s.b
3
>>> s.c = 3
AttributeError
>>> hasattr(s, '__dict__'), hasattr(Slim(), 'b')
(False, False)

>>> class S:
...     __slots__ = 'ab'
>>> s = S()
>>> s.ab = 1
>>> s.a = 2
AttributeError
>>> s.ab, S.__slots__
(1, 'ab')

>>> class A:
...     def who(self):
...         return 'A'
>>> class B(A):
...     def who(self):
...         return 'B' + super().who()
>>> class C(A):
...     def who(self):
...         return 'C' + super().who()
>>> class D(B, C):
...     def who(self):
...         return 'D' + super().who()
>>> D().who()
'DBCA'
>>> [k.__name__ for k in D.__mro__]
['D', 'B', 'C', 'A', 'object']

>>> from abc import ABC, abstractmethod
>>> class Shape(ABC):
...     @abstractmethod
...     def area(self):
...         ...
>>> class Sq(Shape):
...     def __init__(self, s):
...         self.s = s
...     def area(self):
...         return self.s ** 2
>>> Sq(3).area()
9
>>> Shape()
TypeError
"""


@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int

    def moved(self, dx, dy):
        return Point(self.x + dx, self.y + dy)

    def manhattan(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


_job_counter = itertools.count()


@dataclass(order=True)
class Job:
    priority: int
    name: str = field(compare=False)
    tags: list = field(default_factory=list, compare=False)
    # compared after priority, so equal priorities come out in creation order
    seq: int = field(default_factory=lambda: next(_job_counter), init=False, repr=False)


class Edge(NamedTuple):
    u: int
    v: int
    w: int = 1

    def reversed(self):
        return Edge(self.v, self.u, self.w)


@dataclass
class Box:
    width: int
    height: int
    area: int = field(init=False)

    def __post_init__(self):
        if self.width < 0 or self.height < 0:
            raise ValueError("width and height must be non-negative")
        self.area = self.width * self.height


@dataclass(frozen=True, order=True)
class Version:
    major: int
    minor: int
    patch: int

    @classmethod
    def parse(cls, text):
        return cls(*map(int, text.split(".")))

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"


class TrieNode:
    __slots__ = ("children", "end")

    def __init__(self):
        self.children = {}
        self.end = False


def memory_per_object(factory, n=20_000):
    tracemalloc.start()
    try:
        before = tracemalloc.get_traced_memory()[0]
        objs = [factory() for _ in range(n)]        # keep them alive while measuring
        after = tracemalloc.get_traced_memory()[0]
    finally:
        tracemalloc.stop()
    del objs
    return (after - before) / n


class Shape(ABC):
    @abstractmethod
    def area(self):
        ...

    @abstractmethod
    def perimeter(self):
        ...

    def describe(self):
        return f"{type(self).__name__} area={self.area()} perimeter={self.perimeter()}"


class Rectangle(Shape):
    def __init__(self, w, h):
        self.w, self.h = w, h

    def area(self):
        return self.w * self.h

    def perimeter(self):
        return 2 * (self.w + self.h)


class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)


class Pipeline:
    def process(self, items):
        return list(items)


class DropNone(Pipeline):
    def process(self, items):
        return super().process(x for x in items if x is not None)


class Increment(Pipeline):
    def process(self, items):
        return super().process(x + 1 for x in items)


class KeepEven(Pipeline):
    def process(self, items):
        return super().process(x for x in items if x % 2 == 0)
