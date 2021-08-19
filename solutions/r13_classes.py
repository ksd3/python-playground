"""R13 - Class mechanics (reference solutions)

Compare after you've made your own attempt. Run: python check.py 13 -s
"""

PREDICT = r"""
>>> class Bad:
...     items = []
...     def add(self, x):
...         self.items.append(x)
>>> b1, b2 = Bad(), Bad()
>>> b1.add(1)
>>> b2.items
[1]

>>> class C:
...     n = 0
>>> a, b = C(), C()
>>> a.n = 5
>>> a.n, b.n, C.n
(5, 0, 0)

>>> class Tally:
...     count = 0
...     def bump(self):
...         self.count += 1
>>> t = Tally()
>>> t.bump(); t.bump()
>>> t.count, Tally.count, 'count' in vars(t)
(2, 0, True)

>>> class Greeter:
...     def hello(self, name):
...         return f'hi {name}'
>>> g = Greeter()
>>> Greeter.hello(g, 'ann') == g.hello('ann')
True
>>> Greeter.hello('ann')
TypeError

>>> class Oops:
...     def f():
...         return 1
>>> Oops().f()
TypeError
>>> Oops.f()
1

>>> class Point:
...     def __init__(self, x, y):
...         self.x, self.y = x, y
...     @classmethod
...     def origin(cls):
...         return cls(0, 0)
>>> class Point3(Point):
...     pass
>>> type(Point3.origin()).__name__, Point3.origin().x
('Point3', 0)

>>> class M:
...     @staticmethod
...     def add(a, b):
...         return a + b
>>> M.add(2, 3), M().add(2, 3)
(5, 5)

>>> class Temp:
...     def __init__(self, c):
...         self.c = c
...     @property
...     def f(self):
...         return self.c * 9 / 5 + 32
>>> t = Temp(100)
>>> t.f
212.0
>>> t.c = 0
>>> t.f
32.0
>>> t.f = 50
AttributeError

>>> class P:
...     def __repr__(self):
...         return 'P()'
...     def __str__(self):
...         return 'a P'
>>> p = P()
>>> p
P()
>>> print(p)
a P
>>> [p], f'{p}', f'{p!r}'
([P()], 'a P', 'P()')

>>> class Q:
...     def __repr__(self):
...         return 'Q!'
>>> str(Q()), repr(Q())
('Q!', 'Q!')

>>> class A:
...     kind = 'a'
...     def __init__(self):
...         self.x = 1
>>> obj = A()
>>> vars(obj)
{'x': 1}
>>> 'kind' in vars(obj), 'kind' in vars(A), obj.kind
(False, True, 'a')

>>> class Box:
...     pass
>>> b = Box()
>>> setattr(b, 'size', 3)
>>> b.size, hasattr(b, 'color'), getattr(b, 'color', 'none')
(3, False, 'none')
>>> getattr(b, 'color')
AttributeError

>>> class Animal: pass
>>> class Dog(Animal): pass
>>> d = Dog()
>>> isinstance(d, Animal), type(d) is Animal, issubclass(Dog, Animal)
(True, False, True)

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
['base', 'child']
>>> Forgot().log
AttributeError

>>> class K:
...     def who(self):
...         return 'old'
>>> k = K()
>>> K.who = lambda self: 'new'
>>> k.who()
'new'

>>> class Cfg:
...     limit = 3
...     def get(self):
...         return limit
>>> Cfg().get()
NameError

>>> class Pt:
...     def __init__(self, x):
...         self.x = x
>>> Pt(1) == Pt(1), len({Pt(1), Pt(1)})
(False, 2)
"""


class Ticket:
    issued = 0

    def __init__(self):
        Ticket.issued += 1          # through the class: self.issued += 1 would shadow it
        self.number = Ticket.issued

    @classmethod
    def reset(cls):
        cls.issued = 0


class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius      # goes through the property setter, so it's validated

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError(f"below absolute zero: {value}")
        self._celsius = value

    @property
    def fahrenheit(self):
        return self.celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) * 5 / 9

    @classmethod
    def from_fahrenheit(cls, f):
        return cls((f - 32) * 5 / 9)


class Money:
    def __init__(self, cents):
        self.cents = cents

    def __repr__(self):
        return f"Money({self.cents})"

    def __str__(self):
        return f"${self.cents // 100}.{self.cents % 100:02d}"


class Graph:
    def __init__(self, n, directed=False):
        self.n = n
        self.directed = directed
        self.adj = [[] for _ in range(n)]
        self._edges = 0

    def add_edge(self, u, v):
        self.adj[u].append(v)
        if not self.directed:
            self.adj[v].append(u)
        self._edges += 1

    def neighbors(self, u):
        return self.adj[u]

    def degree(self, u):
        return len(self.adj[u])

    @property
    def edge_count(self):
        return self._edges

    @classmethod
    def from_edges(cls, n, edges, directed=False):
        g = cls(n, directed)
        for edge in edges:
            g.add_edge(*edge)
        return g

    def __repr__(self):
        return f"{type(self).__name__}(n={self.n}, edges={self.edge_count}, directed={self.directed})"


class WeightedGraph(Graph):
    def __init__(self, n, directed=False):
        super().__init__(n, directed)
        self._total = 0

    def add_edge(self, u, v, w=1):
        self.adj[u].append((v, w))
        if not self.directed:
            self.adj[v].append((u, w))
        self._edges += 1
        self._total += w

    def total_weight(self):
        return self._total


class History(list):
    def __init__(self, items=()):
        super().__init__(items)
        self.added = []

    def append(self, x):
        super().append(x)
        self.added.append(x)

    def extend(self, items):
        items = list(items)         # a generator can only be consumed once
        super().extend(items)
        self.added.extend(items)


class Grid:
    def __init__(self, rows):
        self.rows = list(rows)

    @classmethod
    def parse(cls, text):
        return cls([line.strip() for line in text.splitlines() if line.strip()])

    @property
    def height(self):
        return len(self.rows)

    @property
    def width(self):
        return len(self.rows[0]) if self.rows else 0

    def at(self, r, c):
        return self.rows[r][c]

    def neighbors(self, r, c):
        out = []
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.height and 0 <= nc < self.width:
                out.append((nr, nc))
        return out

    @staticmethod
    def manhattan(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find(self, ch):
        for r, row in enumerate(self.rows):
            c = row.find(ch)
            if c != -1:
                return (r, c)
        return None


def auto_repr(obj):
    fields = ", ".join(f"{k}={v!r}" for k, v in vars(obj).items() if not k.startswith("_"))
    return f"{type(obj).__name__}({fields})"


def where_defined(obj, name):
    if name in getattr(obj, "__dict__", {}):
        return "instance"
    for cls in type(obj).__mro__:
        if name in vars(cls):
            return cls.__name__
    return None


def call_all(obj, calls):
    return [getattr(obj, name)(*args) for name, args in calls]
