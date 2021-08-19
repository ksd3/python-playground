"""R02 - Functions, scope, closures, recursion

Names resolve Local -> Enclosing -> Global -> Built-in (LEGB). Assigning to a
name anywhere in a function makes it local for the whole function, so
rebinding an outer name needs `nonlocal` (enclosing function) or `global`;
mutating an outer object (seen.append(x)) needs neither. Closures capture
variables, not values: lambdas made in a loop all see the loop variable's last
value unless you bind it early (lambda i=i: ...). Defaults are evaluated once,
when the def runs. Recursion stops at sys.getrecursionlimit() (1000), so deep
inputs need an explicit stack; functools.cache (3.9+) needs hashable args.

Part 1 - Predict. Each block in PREDICT is a REPL session. Replace every ???
with exactly what Python prints: expression values are echoed the way the REPL
echoes them, and a line that raises prints just the exception name (TypeError).

Part 2 - Drills. Implement every function until `python check.py 2` is green.
Don't edit the tests at the bottom; add your own test_* functions if you like.

Unlocks: every DFS/DP helper nested inside a method, memoization, decorators,
and iterative DFS when recursion goes too deep.
"""
import functools

PREDICT = r"""
>>> best = 0
>>> def update(v):
...     best = max(best, v)
...     return best
>>> update(5)
???

>>> count = 10
>>> def show():
...     return count + 1
>>> show()
???

>>> def outer():
...     x = 1
...     def inner():
...         print(x)
...         x = 2
...     inner()
>>> outer()
???

>>> def outer():
...     total = 0
...     def add(v):
...         nonlocal total
...         total += v
...     for v in (1, 2, 3):
...         add(v)
...     return total
>>> outer()
???

>>> def outer():
...     seen = []
...     def visit(v):
...         seen.append(v)
...     visit(1); visit(2)
...     return seen
>>> outer()
???

>>> fs = [lambda: i for i in range(3)]
>>> [f() for f in fs]
???
>>> fs = [lambda i=i: i for i in range(3)]
>>> [f() for f in fs]
???

>>> len = lambda s: 42
>>> len('abc')
???
>>> del len
>>> len('abc')
???

>>> x = 1
>>> def g(y=x):
...     return y
>>> x = 2
>>> g()
???

>>> def make_counter():
...     n = 0
...     def inc():
...         nonlocal n
...         n += 1
...         return n
...     return inc
>>> c1, c2 = make_counter(), make_counter()
>>> c1(), c1(), c2()
???

>>> def f(a, /, b, *args, c, d=4, **kw):
...     return a, b, args, c, d, kw
>>> f(1, 2, c=3)
???
>>> f(1, 2, 3, 4, c=5, e=6)
???
>>> f(a=1, b=2, c=3)
???
>>> f(1, 2, 3)
???

>>> def g(a, *, b):
...     return a + b
>>> g(1, b=2)
???
>>> g(1, 2)
???

>>> def h(*args, **kwargs):
...     return args, kwargs
>>> h(1, 2, x=3)
???
>>> h(*[1, 2], **{'x': 3})
???

>>> sys.getrecursionlimit()
???
>>> def depth(n):
...     return 0 if n == 0 else 1 + depth(n - 1)
>>> depth(100)
???
>>> depth(5000)
???

>>> @cache
... def total(xs):
...     return sum(xs)
>>> total((1, 2, 3))
???
>>> total([1, 2, 3])
???

>>> @lru_cache(maxsize=None)
... def fib(n):
...     return n if n < 2 else fib(n - 1) + fib(n - 2)
>>> fib(30)
???
>>> fib.cache_info().hits, fib.cache_info().misses
???

>>> def shout(fn):
...     def wrapper(*args):
...         return fn(*args).upper()
...     return wrapper
>>> @shout
... def greet(name):
...     return 'hi ' + name
>>> greet('ada'), greet.__name__
???

>>> def shout(fn):
...     @functools.wraps(fn)
...     def wrapper(*args):
...         return fn(*args).upper()
...     return wrapper
>>> @shout
... def greet(name):
...     return 'hi ' + name
>>> greet.__name__
???

>>> ops = {'sq': lambda v: v * v, 'neg': lambda v: -v}
>>> [ops[k](3) for k in ('sq', 'neg')]
???
"""


# ---------------------------------------------------------------- drills

def make_counter(start=0):
    """Return a function that returns start + 1, start + 2, ... on successive
    calls. Counters made by separate make_counter calls are independent."""
    raise NotImplementedError


def make_accumulator():
    """Return a pair of functions (add, total) sharing one running sum that
    starts at 0: add(x) adds x and returns the new sum; total() returns it."""
    raise NotImplementedError


def make_multipliers(n):
    """Return a list of n functions where the i-th one multiplies its argument
    by i: [f(10) for f in make_multipliers(3)] == [0, 10, 20]."""
    raise NotImplementedError


def compose(*fns):
    """Return a function that applies fns right to left, so compose(f, g)(x)
    == f(g(x)). compose() with no functions returns its argument unchanged."""
    raise NotImplementedError


def my_partial(fn, *args, **kwargs):
    """Like functools.partial, without using functools: return a function
    that calls fn with args followed by its own positional args, and with
    kwargs updated by its own keyword args (call-time keywords win)."""
    raise NotImplementedError


def clamp(*args, **kwargs):
    """Rewrite this signature as clamp(x, /, lo=0, hi=1, *, strict=False):
    x positional-only, lo and hi ordinary, strict keyword-only. Return x
    limited to [lo, hi]; when strict is True and x is outside the range,
    raise ValueError instead.
    clamp(5, 0, 3) == 3, while clamp(x=5) and clamp(5, 0, 3, True) are TypeErrors."""
    raise NotImplementedError


def count_calls(fn):
    """Decorator: the result behaves exactly like fn (positional and keyword
    args) and has an attribute .calls counting how many times it was called.
    Keep fn's __name__ (functools.wraps)."""
    raise NotImplementedError


def once(fn):
    """Decorator: call fn only the first time; every later call returns that
    first result without calling fn again, even when the result was None."""
    raise NotImplementedError


def memo(fn):
    """Decorator that memoizes fn by its positional args, without functools:
    the wrapper has an attribute .cache, the dict mapping each args tuple to
    its result."""
    raise NotImplementedError


def flatten(nested):
    """Return the non-list items of an arbitrarily nested list, in order.
    Only lists count as nesting (strings stay whole):
    flatten([1, [2, [3, 'ab']], [], 4]) == [1, 2, 3, 'ab', 4]"""
    raise NotImplementedError


def max_depth(nested):
    """Return the nesting depth of a list: a list with no lists inside has
    depth 1 (so does []), and each level of lists inside adds one:
    max_depth([1, [2, [3]], []]) == 3"""
    raise NotImplementedError


def flatten_iterative(nested):
    """Same result as flatten, but without recursion, so nesting 10**4 levels
    deep works. Use an explicit stack."""
    raise NotImplementedError


# ---------------------------------------------------------------- tests (don't edit)

def test_make_counter():
    c = make_counter()
    assert [c(), c(), c()] == [1, 2, 3]
    d = make_counter(10)
    assert d() == 11 and c() == 4, "counters must be independent"


def test_make_accumulator():
    add, total = make_accumulator()
    assert total() == 0
    assert add(3) == 3 and add(4) == 7 and total() == 7
    add2, total2 = make_accumulator()
    add2(100)
    assert total() == 7 and total2() == 100, "each pair needs its own sum"


def test_make_multipliers():
    fs = make_multipliers(4)
    assert [f(10) for f in fs] == [0, 10, 20, 30], "late binding: every closure sees the last i"
    assert make_multipliers(0) == []


def test_compose():
    inc, dbl = (lambda v: v + 1), (lambda v: v * 2)
    assert compose(inc, dbl)(5) == 11, "right to left: dbl runs first, then inc"
    assert compose(dbl, inc)(5) == 12
    assert compose()(7) == 7
    assert compose(len, str, abs)(-123) == 3


def test_my_partial():
    def f(a, b, c=0, d=0):
        return a, b, c, d

    g = my_partial(f, 1, c=3)
    assert g(2) == (1, 2, 3, 0)
    assert g(2, d=4) == (1, 2, 3, 4)
    assert g(2, c=9) == (1, 2, 9, 0), "call-time keywords should win"
    assert g(5) == (1, 5, 3, 0), "the stored kwargs must not change between calls"
    assert my_partial(f)(1, 2) == (1, 2, 0, 0)


def test_clamp():
    assert clamp(5, 0, 3) == 3 and clamp(-2) == 0 and clamp(0.5) == 0.5
    assert clamp(7, hi=10) == 7 and clamp(2, 0, 3, strict=True) == 2
    for bad, why in ((lambda: clamp(x=1), "x must be positional-only"),
                     (lambda: clamp(5, 0, 3, True), "strict must be keyword-only")):
        try:
            bad()
        except TypeError:
            pass
        else:
            raise AssertionError(why)
    try:
        clamp(5, 0, 3, strict=True)
    except ValueError:
        pass
    else:
        raise AssertionError("strict=True should raise ValueError when x is out of range")


def test_count_calls():
    @count_calls
    def add(a, b):
        return a + b

    assert add.calls == 0
    assert add(1, 2) == 3 and add(b=4, a=3) == 7
    assert add.calls == 2
    assert add.__name__ == 'add', "use functools.wraps to keep the name"

    @count_calls
    def other():
        return 'x'

    other()
    assert other.calls == 1 and add.calls == 2, "each decorated function needs its own counter"


def test_once():
    calls = []

    def setup(v):
        calls.append(v)
        return v * 10

    f = once(setup)
    assert f(1) == 10 and f(2) == 10 and calls == [1]
    hits = []
    g = once(lambda: hits.append(1))
    g(), g(), g()
    assert hits == [1], "None is a valid first result: track 'already called' separately"


def test_memo():
    calls = []

    @memo
    def fib(n):
        calls.append(n)
        return n if n < 2 else fib(n - 1) + fib(n - 2)

    assert fib(80) == 23416728348467685
    assert len(calls) == 81, "every n should be computed exactly once"
    assert fib.cache[(10,)] == 55

    @memo
    def paths(r, c):
        return 1 if r == 0 or c == 0 else paths(r - 1, c) + paths(r, c - 1)

    assert paths(10, 10) == 184756 and (3, 4) in paths.cache


def test_flatten():
    assert flatten([1, [2, [3, 'ab']], [], 4]) == [1, 2, 3, 'ab', 4]
    assert flatten([]) == [] and flatten([[[[]]]]) == []
    assert flatten([[1, [2]], [[3]], 4]) == [1, 2, 3, 4]
    assert flatten(['xy', ['z']]) == ['xy', 'z'], "strings aren't nesting"


def test_max_depth():
    assert max_depth([]) == 1 and max_depth([1, 2]) == 1
    assert max_depth([1, [2, [3]], []]) == 3
    assert max_depth([[[]]]) == 3
    assert max_depth([[1], [[2]], [3]]) == 3
    assert max_depth(['abc']) == 1, "strings aren't nesting"


def test_flatten_iterative():
    assert flatten_iterative([1, [2, [3, 'ab']], [], 4]) == [1, 2, 3, 'ab', 4]
    assert flatten_iterative([]) == [] and flatten_iterative([[[[]]]]) == []
    assert flatten_iterative([[1, [2]], [[3]], 4]) == [1, 2, 3, 4]
    deep = [0]
    for i in range(1, 10**4):
        deep = [deep, i]
    assert flatten_iterative(deep) == list(range(10**4)), "order matters: push children in reverse"
