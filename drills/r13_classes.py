"""R13 - Class mechanics

A class is a namespace of methods plus a factory for instances. Instance
attributes live in the instance's own __dict__ (see vars(obj)); class
attributes live on the class and are shared by every instance, so a mutable
class attribute is shared state. `self` is just the first argument:
Cls.method(obj) and obj.method() are the same call. @classmethod receives the
class (alternative constructors that subclasses inherit), @staticmethod
receives nothing, and @property makes a computed attribute with an optional
setter. Attribute lookup checks the instance first, then type(obj).__mro__.

Part 1 - Predict. Each block in PREDICT is a REPL session. Replace every ???
with exactly what Python prints: expression values are echoed the way the REPL
echoes them, and a line that raises prints just the exception name (TypeError).

Part 2 - Drills. Implement every class and function until `python check.py 13`
is green. Don't edit the tests at the bottom; add your own test_* functions if
you like.

Unlocks: comfort with class-based problem templates, design problems (R16),
and graph code you can reuse.
"""

PREDICT = r"""
>>> class Bad:
...     items = []
...     def add(self, x):
...         self.items.append(x)
>>> b1, b2 = Bad(), Bad()
>>> b1.add(1)
>>> b2.items
???

>>> class C:
...     n = 0
>>> a, b = C(), C()
>>> a.n = 5
>>> a.n, b.n, C.n
???

>>> class Tally:
...     count = 0
...     def bump(self):
...         self.count += 1
>>> t = Tally()
>>> t.bump(); t.bump()
>>> t.count, Tally.count, 'count' in vars(t)
???

>>> class Greeter:
...     def hello(self, name):
...         return f'hi {name}'
>>> g = Greeter()
>>> Greeter.hello(g, 'ann') == g.hello('ann')
???
>>> Greeter.hello('ann')
???

>>> class Oops:
...     def f():
...         return 1
>>> Oops().f()
???
>>> Oops.f()
???

>>> class Point:
...     def __init__(self, x, y):
...         self.x, self.y = x, y
...     @classmethod
...     def origin(cls):
...         return cls(0, 0)
>>> class Point3(Point):
...     pass
>>> type(Point3.origin()).__name__, Point3.origin().x
???

>>> class M:
...     @staticmethod
...     def add(a, b):
...         return a + b
>>> M.add(2, 3), M().add(2, 3)
???

>>> class Temp:
...     def __init__(self, c):
...         self.c = c
...     @property
...     def f(self):
...         return self.c * 9 / 5 + 32
>>> t = Temp(100)
>>> t.f
???
>>> t.c = 0
>>> t.f
???
>>> t.f = 50
???

>>> class P:
...     def __repr__(self):
...         return 'P()'
...     def __str__(self):
...         return 'a P'
>>> p = P()
>>> p
???
>>> print(p)
???
>>> [p], f'{p}', f'{p!r}'
???

>>> class Q:
...     def __repr__(self):
...         return 'Q!'
>>> str(Q()), repr(Q())
???

>>> class A:
...     kind = 'a'
...     def __init__(self):
...         self.x = 1
>>> obj = A()
>>> vars(obj)
???
>>> 'kind' in vars(obj), 'kind' in vars(A), obj.kind
???

>>> class Box:
...     pass
>>> b = Box()
>>> setattr(b, 'size', 3)
>>> b.size, hasattr(b, 'color'), getattr(b, 'color', 'none')
???
>>> getattr(b, 'color')
???

>>> class Animal: pass
>>> class Dog(Animal): pass
>>> d = Dog()
>>> isinstance(d, Animal), type(d) is Animal, issubclass(Dog, Animal)
???

>>> class Base:
...     def __init__(self):
...         self.log = ['base']
>>> class Child(Base):
...     def __init__(self):
...         super().__init__()
...         self.log.append('child')
>>> class Forgot(Base):
...     def __init__(self):
...         self.extra = 1
>>> Child().log
???
>>> Forgot().log
???

>>> class K:
...     def who(self):
...         return 'old'
>>> k = K()
>>> K.who = lambda self: 'new'
>>> k.who()
???

>>> class Cfg:
...     limit = 3
...     def get(self):
...         return limit
>>> Cfg().get()
???

>>> class Pt:
...     def __init__(self, x):
...         self.x = x
>>> Pt(1) == Pt(1), len({Pt(1), Pt(1)})
???
"""


# ---------------------------------------------------------------- drills

class Ticket:
    """Every new Ticket gets the next number, starting at 1, counted across ALL
    tickets: the first has .number == 1, the next 2, and so on.
    Ticket.issued is how many have been issued so far: a class attribute,
    readable from the class and from any ticket (but never stored on one).
    Ticket.reset() is a classmethod that starts the numbering over (issued = 0)."""

    issued = 0

    def __init__(self):
        raise NotImplementedError

    @classmethod
    def reset(cls):
        raise NotImplementedError


class Temperature:
    """Temperature(celsius) stores degrees Celsius.
    - .celsius is a property; a value below -273.15 raises ValueError, both in
      the constructor and in the setter, and a rejected value is not stored.
    - .fahrenheit is a computed property (celsius * 9 / 5 + 32) whose setter
      updates celsius.
    - Temperature.from_fahrenheit(f) is a classmethod alternative constructor
      that builds cls(...), so a subclass gets an instance of itself."""

    def __init__(self, celsius):
        raise NotImplementedError

    @property
    def celsius(self):
        raise NotImplementedError

    @celsius.setter
    def celsius(self, value):
        raise NotImplementedError

    @property
    def fahrenheit(self):
        raise NotImplementedError

    @fahrenheit.setter
    def fahrenheit(self, value):
        raise NotImplementedError

    @classmethod
    def from_fahrenheit(cls, f):
        raise NotImplementedError


class Money:
    """Money(cents) for a non-negative int number of cents.
    repr(Money(1234)) == 'Money(1234)'  (eval(repr(m)) rebuilds it)
    str(Money(1234)) == '$12.34' and str(Money(5)) == '$0.05'
    Containers show the repr: repr([Money(5)]) == '[Money(5)]'."""

    def __init__(self, cents):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError


class Graph:
    """Graph(n, directed=False) on nodes 0..n-1, stored as adjacency lists.
    - add_edge(u, v): adds v to u's neighbors (and u to v's when undirected).
    - neighbors(u): list of u's neighbors in insertion order.
    - degree(u): how many neighbors u has.
    - edge_count: a read-only property, edges added so far (an undirected
      edge counts once).
    - Graph.from_edges(n, edges, directed=False): classmethod that builds
      cls(n, directed) and calls add_edge(*edge) for each edge, so a subclass
      whose edges carry extra fields inherits it unchanged.
    - repr(g) == 'Graph(n=3, edges=2, directed=False)', using the class name
      of the actual object (type(self).__name__)."""

    def __init__(self, n, directed=False):
        raise NotImplementedError

    def add_edge(self, u, v):
        raise NotImplementedError

    def neighbors(self, u):
        raise NotImplementedError

    def degree(self, u):
        raise NotImplementedError

    @property
    def edge_count(self):
        raise NotImplementedError

    @classmethod
    def from_edges(cls, n, edges, directed=False):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError


class WeightedGraph(Graph):
    """A Graph whose edges carry weights.
    - __init__(n, directed=False) calls super().__init__ and adds any state
      of its own.
    - add_edge(u, v, w=1): stores (v, w) for u (and (u, w) for v when undirected).
    - neighbors(u): list of (v, w) pairs in insertion order.
    - total_weight(): sum of all edge weights (an undirected edge counts once).
    degree, edge_count, from_edges and repr keep working through inheritance:
    WeightedGraph.from_edges(3, [(0, 1, 5)]) returns a WeightedGraph."""

    def __init__(self, n, directed=False):
        raise NotImplementedError

    def add_edge(self, u, v, w=1):
        raise NotImplementedError

    def total_weight(self):
        raise NotImplementedError


class History(list):
    """A list that also records, in .added, every item that arrives through
    append() or extend() (not the items it was created with):
    h = History([1]); h.append(2); h.extend([3, 4])
    -> h == [1, 2, 3, 4] and h.added == [2, 3, 4].
    Call the real list methods through super(). list.extend does NOT call
    append, so override both, and remember extend() may receive a generator."""

    def __init__(self, items=()):
        raise NotImplementedError

    def append(self, x):
        raise NotImplementedError

    def extend(self, items):
        raise NotImplementedError


class Grid:
    """A rectangular grid of characters.
    - Grid(rows): rows is a list of equal-length strings.
    - Grid.parse(text): classmethod; one row per non-blank line, with the
      surrounding whitespace stripped; builds cls(...).
    - .height and .width: read-only properties.
    - at(r, c): the character at row r, column c.
    - neighbors(r, c): the in-bounds 4-neighbors as (row, col) pairs, in the
      order up, down, left, right.
    - Grid.manhattan(a, b): staticmethod, |r1 - r2| + |c1 - c2| for two
      (row, col) pairs; callable on the class or on an instance.
    - find(ch): (row, col) of the first ch in row-major order, or None."""

    def __init__(self, rows):
        raise NotImplementedError

    @classmethod
    def parse(cls, text):
        raise NotImplementedError

    @property
    def height(self):
        raise NotImplementedError

    @property
    def width(self):
        raise NotImplementedError

    def at(self, r, c):
        raise NotImplementedError

    def neighbors(self, r, c):
        raise NotImplementedError

    @staticmethod
    def manhattan(a, b):
        raise NotImplementedError

    def find(self, ch):
        raise NotImplementedError


def auto_repr(obj):
    """Build a repr from an object's instance attributes, in the order they
    were set, skipping names that start with '_': for a Point with p.x = 1 and
    p.tags = ['a'], auto_repr(p) == "Point(x=1, tags=['a'])". Use the object's
    class name and repr() of each value."""
    raise NotImplementedError


def where_defined(obj, name):
    """Report where attribute lookup finds `name` on obj: 'instance' if it's
    in the object's own __dict__, else the __name__ of the first class in
    type(obj).__mro__ whose own __dict__ has it, else None. Works for any
    object (one without a __dict__ simply has no instance attributes):
    where_defined([], 'append') == 'list'."""
    raise NotImplementedError


def call_all(obj, calls):
    """Replay method calls on obj and return their results in order. calls is
    a list of (method_name, args) pairs: look each method up by name with
    getattr and call it with *args. An unknown name raises AttributeError.
    call_all([], [('append', [1]), ('append', [2]), ('pop', []), ('__len__', [])])
    == [None, None, 2, 1]"""
    raise NotImplementedError


# ---------------------------------------------------------------- tests (don't edit)

def _raises(exc, fn):
    try:
        fn()
    except exc:
        return True
    return False


def test_ticket():
    Ticket.reset()
    a, b, c = Ticket(), Ticket(), Ticket()
    assert (a.number, b.number, c.number) == (1, 2, 3), \
        "numbers must keep counting across tickets: self.issued += 1 creates an instance attribute"
    assert Ticket.issued == 3, "update the counter on the class, not on self"
    assert a.issued == 3 and 'issued' not in vars(a), "issued must live on the class only"
    Ticket.reset()
    assert Ticket.issued == 0 and Ticket().number == 1


def test_temperature():
    t = Temperature(100)
    assert t.celsius == 100 and t.fahrenheit == 212
    t.fahrenheit = 32
    assert t.celsius == 0, "the fahrenheit setter must update celsius"
    t.celsius = -40
    assert t.fahrenheit == -40
    assert _raises(ValueError, lambda: Temperature(-300)), "the constructor must validate too"
    assert _raises(ValueError, lambda: setattr(t, 'celsius', -273.16))
    assert t.celsius == -40, "a rejected value must not be stored"

    class Warmer(Temperature):
        pass

    w = Warmer.from_fahrenheit(212)
    assert type(w) is Warmer and w.celsius == 100, "from_fahrenheit should build cls(...), not Temperature(...)"


def test_money():
    m = Money(1234)
    assert repr(m) == 'Money(1234)' and str(m) == '$12.34'
    assert str(Money(5)) == '$0.05' and str(Money(100)) == '$1.00' and str(Money(0)) == '$0.00'
    assert repr([Money(5)]) == '[Money(5)]', "containers use __repr__, not __str__"
    assert f'{m}' == '$12.34' and f'{m!r}' == 'Money(1234)'
    assert repr(eval(repr(m), {'Money': Money})) == repr(m)


def test_graph():
    g = Graph(4)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(2, 3)
    assert g.neighbors(0) == [1, 2] and g.neighbors(2) == [0, 3] and g.neighbors(3) == [2]
    assert g.degree(0) == 2
    assert g.edge_count == 3, "edge_count is a property: g.edge_count, not g.edge_count()"
    assert repr(g) == 'Graph(n=4, edges=3, directed=False)'
    d = Graph.from_edges(3, [(0, 1), (1, 2)], directed=True)
    assert type(d) is Graph and d.neighbors(1) == [2] and d.neighbors(2) == [], "directed edges go one way"
    assert d.edge_count == 2 and repr(d) == 'Graph(n=3, edges=2, directed=True)'
    a, b = Graph(2), Graph(2)
    a.add_edge(0, 1)
    assert b.neighbors(0) == [], "adjacency lists must belong to each instance"
    assert _raises(AttributeError, lambda: setattr(g, 'edge_count', 0)), "edge_count must be read-only"


def test_weighted_graph():
    w = WeightedGraph.from_edges(3, [(0, 1, 5), (1, 2, 2), (0, 2)])
    assert type(w) is WeightedGraph, "from_edges must build cls(...), not Graph(...)"
    assert w.neighbors(0) == [(1, 5), (2, 1)] and w.neighbors(2) == [(1, 2), (0, 1)]
    assert w.degree(1) == 2 and w.edge_count == 3 and w.total_weight() == 8
    assert repr(w) == 'WeightedGraph(n=3, edges=3, directed=False)'
    assert isinstance(w, Graph)
    dw = WeightedGraph(2, directed=True)
    dw.add_edge(1, 0, 7)
    assert dw.neighbors(1) == [(0, 7)] and dw.neighbors(0) == [] and dw.total_weight() == 7


def test_history():
    h = History([1])
    h.append(2)
    h.extend([3, 4])
    h.extend(x * 10 for x in (5, 6))
    assert h == [1, 2, 3, 4, 50, 60] and isinstance(h, list)
    assert h.added == [2, 3, 4, 50, 60], "a generator can only be read once: materialize it first"
    assert History().added == [] and History() == []
    h2 = History()
    h2.append(9)
    assert h.added[-1] == 60 and h2.added == [9], "each History needs its own .added"


def test_grid():
    g = Grid.parse("  S.#\n\n  ..E  \n")
    assert isinstance(g, Grid) and (g.height, g.width) == (2, 3)
    assert g.at(0, 0) == 'S' and g.at(1, 2) == 'E'
    assert g.find('E') == (1, 2) and g.find('x') is None
    assert g.neighbors(0, 0) == [(1, 0), (0, 1)]
    assert g.neighbors(1, 1) == [(0, 1), (1, 0), (1, 2)]
    assert Grid.manhattan((0, 0), (1, 2)) == 3
    assert g.manhattan((1, 2), (0, 0)) == 3, "manhattan must be a @staticmethod"
    assert _raises(AttributeError, lambda: setattr(g, 'height', 5)), "height must be a read-only property"

    class Big(Grid):
        pass

    assert type(Big.parse("ab\ncd")) is Big, "parse should build cls(...)"


def test_auto_repr():
    class Point:
        pass

    p = Point()
    p.x = 1
    p.tags = ['a']
    p._cache = {}
    assert auto_repr(p) == "Point(x=1, tags=['a'])"

    class Empty:
        pass

    assert auto_repr(Empty()) == 'Empty()'

    class Named:
        def __init__(self):
            self.name = 'n'
            self.size = 2

    assert auto_repr(Named()) == "Named(name='n', size=2)"


def test_where_defined():
    class Animal:
        legs = 4

        def speak(self):
            return '...'

    class Dog(Animal):
        def speak(self):
            return 'woof'

    d = Dog()
    d.name = 'rex'
    assert where_defined(d, 'name') == 'instance'
    assert where_defined(d, 'speak') == 'Dog', "the subclass override is found first"
    assert where_defined(d, 'legs') == 'Animal'
    assert where_defined(d, '__init__') == 'object'
    assert where_defined(d, 'nope') is None
    d.legs = 3
    assert where_defined(d, 'legs') == 'instance', "an instance attribute shadows the class one"
    assert where_defined([], 'append') == 'list' and where_defined(True, 'bit_length') == 'int'


def test_call_all():
    assert call_all([], [('append', [1]), ('append', [2]), ('pop', []), ('__len__', [])]) == [None, None, 2, 1]
    assert call_all({}, [('setdefault', ['k', 0]), ('get', ['k']), ('get', ['x', -1])]) == [0, 0, -1]

    class Stack:
        def __init__(self):
            self.items = []

        def push(self, x):
            self.items.append(x)

        def peek(self):
            return self.items[-1]

    assert call_all(Stack(), [('push', [5]), ('push', [7]), ('peek', [])]) == [None, None, 7]
    assert call_all(Stack(), []) == []
    assert _raises(AttributeError, lambda: call_all([], [('nope', [])])), "an unknown name must raise AttributeError"
