"""R02 - Functions, scope, closures, recursion (reference solutions)

Compare after you've made your own attempt. Run: python check.py 2 -s
"""
import functools

PREDICT = r"""
>>> best = 0
>>> def update(v):
...     best = max(best, v)
...     return best
>>> update(5)
UnboundLocalError

>>> count = 10
>>> def show():
...     return count + 1
>>> show()
11

>>> def outer():
...     x = 1
...     def inner():
...         print(x)
...         x = 2
...     inner()
>>> outer()
UnboundLocalError

>>> def outer():
...     total = 0
...     def add(v):
...         nonlocal total
...         total += v
...     for v in (1, 2, 3):
...         add(v)
...     return total
>>> outer()
6

>>> def outer():
...     seen = []
...     def visit(v):
...         seen.append(v)
...     visit(1); visit(2)
...     return seen
>>> outer()
[1, 2]

>>> fs = [lambda: i for i in range(3)]
>>> [f() for f in fs]
[2, 2, 2]
>>> fs = [lambda i=i: i for i in range(3)]
>>> [f() for f in fs]
[0, 1, 2]

>>> len = lambda s: 42
>>> len('abc')
42
>>> del len
>>> len('abc')
3

>>> x = 1
>>> def g(y=x):
...     return y
>>> x = 2
>>> g()
1

>>> def make_counter():
...     n = 0
...     def inc():
...         nonlocal n
...         n += 1
...         return n
...     return inc
>>> c1, c2 = make_counter(), make_counter()
>>> c1(), c1(), c2()
(1, 2, 1)

>>> def f(a, /, b, *args, c, d=4, **kw):
...     return a, b, args, c, d, kw
>>> f(1, 2, c=3)
(1, 2, (), 3, 4, {})
>>> f(1, 2, 3, 4, c=5, e=6)
(1, 2, (3, 4), 5, 4, {'e': 6})
>>> f(a=1, b=2, c=3)
TypeError
>>> f(1, 2, 3)
TypeError

>>> def g(a, *, b):
...     return a + b
>>> g(1, b=2)
3
>>> g(1, 2)
TypeError

>>> def h(*args, **kwargs):
...     return args, kwargs
>>> h(1, 2, x=3)
((1, 2), {'x': 3})
>>> h(*[1, 2], **{'x': 3})
((1, 2), {'x': 3})

>>> sys.getrecursionlimit()
1000
>>> def depth(n):
...     return 0 if n == 0 else 1 + depth(n - 1)
>>> depth(100)
100
>>> depth(5000)
RecursionError

>>> @cache
... def total(xs):
...     return sum(xs)
>>> total((1, 2, 3))
6
>>> total([1, 2, 3])
TypeError

>>> @lru_cache(maxsize=None)
... def fib(n):
...     return n if n < 2 else fib(n - 1) + fib(n - 2)
>>> fib(30)
832040
>>> fib.cache_info().hits, fib.cache_info().misses
(28, 31)

>>> def shout(fn):
...     def wrapper(*args):
...         return fn(*args).upper()
...     return wrapper
>>> @shout
... def greet(name):
...     return 'hi ' + name
>>> greet('ada'), greet.__name__
('HI ADA', 'wrapper')

>>> def shout(fn):
...     @functools.wraps(fn)
...     def wrapper(*args):
...         return fn(*args).upper()
...     return wrapper
>>> @shout
... def greet(name):
...     return 'hi ' + name
>>> greet.__name__
'greet'

>>> ops = {'sq': lambda v: v * v, 'neg': lambda v: -v}
>>> [ops[k](3) for k in ('sq', 'neg')]
[9, -3]
"""


def make_counter(start=0):
    n = start

    def counter():
        nonlocal n
        n += 1
        return n

    return counter


def make_accumulator():
    running = 0

    def add(x):
        nonlocal running
        running += x
        return running

    def total():
        return running

    return add, total


def make_multipliers(n):
    return [lambda x, i=i: x * i for i in range(n)]  # i=i binds the value now


def compose(*fns):
    def composed(x):
        for f in reversed(fns):
            x = f(x)
        return x

    return composed


def my_partial(fn, *args, **kwargs):
    def call(*more_args, **more_kwargs):
        return fn(*args, *more_args, **{**kwargs, **more_kwargs})

    return call


def clamp(x, /, lo=0, hi=1, *, strict=False):
    if strict and not lo <= x <= hi:
        raise ValueError(f"{x} is outside [{lo}, {hi}]")
    return max(lo, min(x, hi))


def count_calls(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return fn(*args, **kwargs)

    wrapper.calls = 0
    return wrapper


def once(fn):
    called, result = False, None

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        nonlocal called, result
        if not called:
            called, result = True, fn(*args, **kwargs)
        return result

    return wrapper


def memo(fn):
    cache = {}

    @functools.wraps(fn)
    def wrapper(*args):
        if args not in cache:
            cache[args] = fn(*args)
        return cache[args]

    wrapper.cache = cache
    return wrapper


def flatten(nested):
    out = []

    def walk(items):
        for item in items:
            if isinstance(item, list):
                walk(item)
            else:
                out.append(item)

    walk(nested)
    return out


def max_depth(nested):
    best = 0

    def walk(items, depth):
        nonlocal best
        best = max(best, depth)
        for item in items:
            if isinstance(item, list):
                walk(item, depth + 1)

    walk(nested, 1)
    return best


def flatten_iterative(nested):
    out, stack = [], list(reversed(nested))
    while stack:
        item = stack.pop()
        if isinstance(item, list):
            stack.extend(reversed(item))  # reversed, so the first child pops first
        else:
            out.append(item)
    return out
