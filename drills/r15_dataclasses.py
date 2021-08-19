"""R15 - dataclasses, namedtuples, slots, inheritance

@dataclass writes __init__, __repr__ and __eq__ from annotated fields (and
sets __hash__ to None unless frozen=True). order=True adds comparisons in
field order, field(default_factory=list) gives each instance its own mutable
default, field(compare=False) leaves a field out of ==/<, and
field(init=False) + __post_init__ makes derived fields. namedtuple and
typing.NamedTuple are real tuples with names. __slots__ removes the
per-instance __dict__ (smaller objects, no new attributes). super() means
"next class in the MRO", which is what makes cooperative mixins work.

Part 1 - Predict. Each block in PREDICT is a REPL session. Replace every ???
with exactly what Python prints: expression values are echoed the way the REPL
echoes them, and a line that raises prints just the exception name (TypeError).

Part 2 - Drills. Several stubs say "rewrite as ...": replace the whole stub
class with a dataclass / NamedTuple / ABC of the same name. Work until
`python check.py 15` is green. Don't edit the tests at the bottom; add your
own test_* functions if you like.

Unlocks: clean state objects, heap entries that never compare payloads,
memory-light trie nodes, and readable class hierarchies.
"""
import dataclasses
import heapq
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
???

>>> @dataclass
... class Q:
...     x: int
>>> hash(Q(1))
???

>>> @dataclass(frozen=True)
... class F:
...     x: int
>>> f = F(1)
>>> {f: 'ok'}[F(1)]
???
>>> f.x = 2
???

>>> @dataclass(frozen=True)
... class G:
...     xs: list
>>> g = G([1])
>>> g.xs.append(2); g
???
>>> hash(g)
???

>>> @dataclass(order=True)
... class V:
...     major: int
...     minor: int
>>> sorted([V(1, 5), V(0, 9), V(1, 2)])
???
>>> V(1, 2) < V(1, 10)
???

>>> @dataclass
... class D:
...     xs: list = []
???

>>> @dataclass
... class Bag:
...     items: list = field(default_factory=list)
>>> a, b = Bag(), Bag()
>>> a.items.append(1)
>>> a, b
???

>>> @dataclass(order=True)
... class Job:
...     priority: int
...     name: str = field(compare=False)
>>> Job(1, 'b') == Job(1, 'a'), Job(2, 'a') > Job(1, 'z')
???

>>> @dataclass
... class Bad:
...     a: int = 0
...     b: int
???

>>> @dataclass
... class C:
...     x: int
...     y = 5
>>> C(1), C(1).y
???

>>> @dataclass
... class Base:
...     x: int
>>> @dataclass
... class Child(Base):
...     y: int = 0
>>> Child(1, 2), Child(5)
???

>>> from dataclasses import asdict, astuple, replace
>>> @dataclass
... class Item:
...     name: str
...     qty: int = 1
>>> it = Item('pen', 3)
>>> asdict(it), astuple(it), replace(it, qty=0)
???

>>> Point = namedtuple('Point', 'x y')
>>> p = Point(1, 2)
>>> p, p.x, p[1], p == (1, 2)
???
>>> x, y = p
>>> p._replace(x=9), x + y
???
>>> p.x = 5
???

>>> Point = namedtuple('Point', 'x y')
>>> sorted([Point(2, 1), Point(1, 5), Point(1, 2)])
???
>>> len({Point(1, 2), (1, 2)}), isinstance(Point(1, 2), tuple), Point._fields
???

>>> from typing import NamedTuple
>>> class Edge(NamedTuple):
...     u: int
...     v: int
...     w: int = 1
>>> Edge(0, 1), Edge(0, 1, 5).w, Edge(0, 1)._asdict()
???

>>> class Slim:
...     __slots__ = ('a', 'b')
...     def __init__(self):
...         self.a = 1
>>> s = Slim()
>>> s.b = 2
>>> s.a + s.b
???
>>> s.c = 3
???
>>> hasattr(s, '__dict__'), hasattr(Slim(), 'b')
???

>>> class S:
...     __slots__ = 'ab'
>>> s = S()
>>> s.ab = 1
>>> s.a = 2
???
>>> s.ab, S.__slots__
???

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
???
>>> [k.__name__ for k in D.__mro__]
???

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
???
>>> Shape()
???
"""


# ---------------------------------------------------------------- drills

class Point:
    """Rewrite as @dataclass(frozen=True, order=True) with int fields x, y.
    - repr(Point(1, 2)) == 'Point(x=1, y=2)'; points sort by (x, y)
    - frozen: assigning p.x raises dataclasses.FrozenInstanceError, and points
      are hashable (dict keys, set members)
    - moved(dx, dy) returns a NEW Point; manhattan(other) is |dx| + |dy|"""

    def __init__(self, x, y):
        raise NotImplementedError

    def moved(self, dx, dy):
        raise NotImplementedError

    def manhattan(self, other):
        raise NotImplementedError


class Job:
    """Rewrite as an ordered dataclass for heaps: Job(priority, name, tags).
    - compares by (priority, creation order) and nothing else: equal
      priorities pop first-in, first-out, and names are never compared
    - tags defaults to a NEW empty list for every Job
    - repr shows priority, name and tags but not the creation number:
      repr(Job(2, 'write')) == "Job(priority=2, name='write', tags=[])"
    Hint: a module-level counter = itertools.count() plus a field like
    field(default_factory=lambda: next(counter), init=False, repr=False)."""

    def __init__(self, priority, name, tags=None):
        raise NotImplementedError


class Edge:
    """Rewrite as a typing.NamedTuple with int fields u, v and w (default 1).
    - Edge(0, 1) == (0, 1, 1): it's a real tuple, so indexing, unpacking,
      hashing and sorting all work; e.w is the weight
    - reversed() returns Edge(v, u, w)
    - e._replace(w=5) gives a changed copy (NamedTuple provides it)"""

    def __new__(cls, u, v, w=1):
        raise NotImplementedError

    def reversed(self):
        raise NotImplementedError


class Box:
    """Rewrite as a dataclass: Box(width, height) plus a derived field `area`
    that is NOT an __init__ argument (field(init=False)) and is set in
    __post_init__. A negative width or height raises ValueError.
    repr(Box(2, 3)) == 'Box(width=2, height=3, area=6)'"""

    def __init__(self, width, height):
        raise NotImplementedError


class Version:
    """Rewrite as @dataclass(frozen=True, order=True) with int fields major,
    minor and patch, plus:
    - Version.parse('1.10.2') -> Version(1, 10, 2) (a classmethod)
    - str(v) == '1.10.2' (define __str__; the generated repr stays)
    Ordering is numeric per field, so 1.10.0 > 1.9.0 (strings get this wrong)."""

    def __init__(self, major, minor, patch):
        raise NotImplementedError

    @classmethod
    def parse(cls, text):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError


class TrieNode:
    """A trie node with __slots__ = ('children', 'end'), so instances have no
    per-instance __dict__. TrieNode() starts with children == {} (its own
    dict) and end == False; assigning any other attribute raises AttributeError."""

    def __init__(self):
        raise NotImplementedError


def memory_per_object(factory, n=20_000):
    """Average bytes allocated per object when you create n objects with
    factory() and keep them all alive, measured with tracemalloc: start it,
    read get_traced_memory() before and after, stop it, return a float.
    memory_per_object(lambda: [0] * 100) is about 860 on 64-bit CPython."""
    raise NotImplementedError


class Shape:
    """Rewrite as an abstract base class: subclass abc.ABC, mark area() and
    perimeter() with @abstractmethod, and keep a concrete describe() that
    returns e.g. 'Square area=4 perimeter=8' (class name from
    type(self).__name__). Shape() must raise TypeError, and so must any
    subclass that doesn't implement both abstract methods."""

    def area(self):
        raise NotImplementedError

    def perimeter(self):
        raise NotImplementedError

    def describe(self):
        raise NotImplementedError


class Rectangle(Shape):
    """Rectangle(w, h) implementing area() and perimeter()."""

    def __init__(self, w, h):
        raise NotImplementedError

    def area(self):
        raise NotImplementedError

    def perimeter(self):
        raise NotImplementedError


class Square(Rectangle):
    """Square(side): its __init__ just calls super().__init__(side, side); it
    inherits everything else (don't redefine area, perimeter or describe)."""

    def __init__(self, side):
        raise NotImplementedError


class Pipeline:
    """Given: the end of a cooperative chain. It returns the items as a list."""

    def process(self, items):
        return list(items)


class DropNone(Pipeline):
    """Drop None items, then pass the rest on: return super().process(...).
    super() is the NEXT class in the instance's MRO, not necessarily Pipeline,
    so steps combined in one class run in MRO order."""

    def process(self, items):
        raise NotImplementedError


class Increment(Pipeline):
    """Add 1 to every item, then pass them on with super().process(...)."""

    def process(self, items):
        raise NotImplementedError


class KeepEven(Pipeline):
    """Keep only even items, then pass them on with super().process(...)."""

    def process(self, items):
        raise NotImplementedError


# ---------------------------------------------------------------- tests (don't edit)

def _raises(exc, fn):
    try:
        fn()
    except exc:
        return True
    return False


class _PlainPair:
    def __init__(self):
        self.a = 1
        self.b = 2


class _SlotPair:
    __slots__ = ('a', 'b')

    def __init__(self):
        self.a = 1
        self.b = 2


def test_point():
    p = Point(1, 2)
    assert dataclasses.is_dataclass(Point), "write Point with @dataclass"
    assert repr(p) == 'Point(x=1, y=2)' and p == Point(1, 2)
    assert _raises(dataclasses.FrozenInstanceError, lambda: setattr(p, 'x', 5)), "Point must be frozen"
    assert {p: 'here'}[Point(1, 2)] == 'here' and len({Point(0, 0), Point(0, 0)}) == 1
    assert sorted([Point(2, 0), Point(1, 5), Point(1, -1)]) == [Point(1, -1), Point(1, 5), Point(2, 0)]
    q = p.moved(2, -3)
    assert q == Point(3, -1) and p == Point(1, 2), "moved must return a new Point"
    assert p.manhattan(q) == 5 and q.manhattan(p) == 5


def test_job():
    j = Job(2, 'write')
    assert dataclasses.is_dataclass(Job), "write Job with @dataclass"
    assert repr(j) == "Job(priority=2, name='write', tags=[])", "keep the creation number out of the repr"
    a, b = Job(1, 'a'), Job(1, 'b')
    a.tags.append('x')
    assert b.tags == [], "each Job needs its own tags list: field(default_factory=list)"
    assert a < b and not (b < a), "equal priorities: the earlier job comes first"

    class Opaque:
        pass

    h = []
    for p in [3, 1, 2, 1, 3]:
        heapq.heappush(h, Job(p, Opaque()))
    pops = [heapq.heappop(h) for _ in range(5)]
    assert [x.priority for x in pops] == [1, 1, 2, 3, 3], "names must never be compared (compare=False)"
    assert pops[0] < pops[1] and pops[3] < pops[4]
    assert Job(5, 'z', ['t']).tags == ['t']


def test_edge():
    e = Edge(0, 1)
    assert e == (0, 1, 1) and isinstance(e, tuple), "write Edge as a typing.NamedTuple"
    assert e.w == 1 and e[1] == 1
    u, v, w = Edge(2, 3, 7)
    assert (u, v, w) == (2, 3, 7)
    assert Edge(2, 3, 7).reversed() == Edge(3, 2, 7)
    assert e._replace(w=5) == (0, 1, 5) and e == (0, 1, 1)
    edges = [Edge(1, 2, 9), Edge(0, 1, 3), Edge(0, 2, 3)]
    assert sorted(edges, key=lambda x: (x.w, x.u, x.v)) == [(0, 1, 3), (0, 2, 3), (1, 2, 9)]
    assert len({Edge(0, 1), (0, 1, 1)}) == 1
    assert repr(Edge(4, 5, 6)) == 'Edge(u=4, v=5, w=6)' and Edge._fields == ('u', 'v', 'w')


def test_box():
    b = Box(2, 3)
    assert dataclasses.is_dataclass(Box), "write Box with @dataclass"
    assert b.area == 6 and repr(b) == 'Box(width=2, height=3, area=6)'
    assert Box(0, 5).area == 0 and Box(2, 3) == b
    assert _raises(ValueError, lambda: Box(-1, 2)) and _raises(ValueError, lambda: Box(2, -1)), \
        "validate in __post_init__"
    assert _raises(TypeError, lambda: Box(1, 2, 3)), "area must not be an __init__ argument: field(init=False)"


def test_version():
    v = Version.parse('1.10.2')
    assert dataclasses.is_dataclass(Version), "write Version with @dataclass"
    assert v == Version(1, 10, 2) and str(v) == '1.10.2'
    assert repr(v) == 'Version(major=1, minor=10, patch=2)', "keep the generated repr; only add __str__"
    tags = ['1.9.0', '1.10.0', '1.2.10', '0.99.99', '1.2.9']
    assert [str(x) for x in sorted(map(Version.parse, tags))] == ['0.99.99', '1.2.9', '1.2.10', '1.9.0', '1.10.0']
    assert Version.parse('2.0.0') > Version.parse('1.99.99')
    assert max(map(Version.parse, tags)) == Version(1, 10, 0)
    assert len({Version.parse('1.0.0'), Version(1, 0, 0)}) == 1, "frozen dataclasses are hashable"


def test_trie_node():
    node = TrieNode()
    assert node.children == {} and node.end is False
    assert not hasattr(node, '__dict__'), "use __slots__ so nodes carry no per-instance __dict__"
    assert set(TrieNode.__slots__) == {'children', 'end'}, "__slots__ = ('children', 'end'), a tuple, not one string"
    a, b = TrieNode(), TrieNode()
    a.children['x'] = b
    assert TrieNode().children == {}, "each node needs its own children dict"
    assert _raises(AttributeError, lambda: setattr(node, 'count', 1)), "with __slots__, new attributes raise AttributeError"


def test_memory_per_object():
    per_list = memory_per_object(lambda: [0] * 100, 2000)
    assert isinstance(per_list, float)
    assert 820 <= per_list <= 960, f"a 100-slot list is about 860 bytes; measured {per_list:.0f}"
    plain, slim = memory_per_object(_PlainPair), memory_per_object(_SlotPair)
    assert 0 < slim < plain, "objects with __slots__ should be smaller than plain ones"
    assert not tracemalloc.is_tracing(), "stop tracemalloc when you're done measuring"


def test_shapes():
    sq = Square(2)
    assert sq.area() == 4 and sq.perimeter() == 8
    assert sq.describe() == 'Square area=4 perimeter=8', "describe() should use type(self).__name__"
    assert Rectangle(2, 3).describe() == 'Rectangle area=6 perimeter=10'
    assert isinstance(sq, Rectangle) and isinstance(sq, Shape)
    assert 'area' not in vars(Square) and 'describe' not in vars(Square), "Square should inherit, not re-implement"
    assert _raises(TypeError, Shape), "Shape must be abstract: subclass abc.ABC and use @abstractmethod"

    class Half(Shape):
        def area(self):
            return 1

    assert _raises(TypeError, Half), "a subclass missing perimeter() must not be instantiable"

    class Unit(Shape):
        def area(self):
            return 1

        def perimeter(self):
            return 4

    assert Unit().describe() == 'Unit area=1 perimeter=4'


def test_pipeline_steps():
    class A(DropNone, Increment, KeepEven, Pipeline):
        pass

    class B(DropNone, KeepEven, Increment, Pipeline):
        pass

    assert A().process([1, None, 2, 3]) == [2, 4], \
        "each step must call super().process(...), not Pipeline.process(...), so no step is skipped"
    assert B().process([1, None, 2, 3]) == [3], "steps must chain through super(), in MRO order"
    assert [k.__name__ for k in A.__mro__] == ['A', 'DropNone', 'Increment', 'KeepEven', 'Pipeline', 'object']
    assert Increment().process([1, 2]) == [2, 3] and DropNone().process([None]) == []
    assert KeepEven().process(x for x in range(5)) == [0, 2, 4], "items can be any iterable"
