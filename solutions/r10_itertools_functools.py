"""R10 - itertools, functools, operator (reference solutions)

Compare after you've made your own attempt. Run: python check.py 10 -s
"""
import functools
import itertools
import operator
from functools import cmp_to_key
from itertools import chain, combinations

PREDICT = r"""
>>> list(accumulate([1, 2, 3, 4]))
[1, 3, 6, 10]
>>> list(accumulate([1, 2, 3], initial=0))
[0, 1, 3, 6]
>>> list(accumulate([3, 1, 4, 1, 5], max))
[3, 3, 4, 4, 5]
>>> list(accumulate([1, 2, 3, 4], operator.mul))
[1, 2, 6, 24]

>>> list(product('ab', range(2)))
[('a', 0), ('a', 1), ('b', 0), ('b', 1)]
>>> len(list(product(range(3), repeat=4)))
81

>>> list(permutations('abc', 2))
[('a', 'b'), ('a', 'c'), ('b', 'a'), ('b', 'c'), ('c', 'a'), ('c', 'b')]
>>> list(combinations('abcd', 2))
[('a', 'b'), ('a', 'c'), ('a', 'd'), ('b', 'c'), ('b', 'd'), ('c', 'd')]
>>> list(itertools.combinations_with_replacement('ab', 2))
[('a', 'a'), ('a', 'b'), ('b', 'b')]

>>> list(combinations([1, 1, 2], 2))
[(1, 1), (1, 2), (1, 2)]
>>> len(list(permutations('aab'))), len(set(permutations('aab')))
(6, 3)

>>> [(k, len(list(g))) for k, g in groupby('aabbbac')]
[('a', 2), ('b', 3), ('a', 1), ('c', 1)]
>>> [(k, len(list(g))) for k, g in groupby(sorted('aabbbac'))]
[('a', 3), ('b', 3), ('c', 1)]

>>> groups = list(groupby('aabbbc'))
>>> [list(g) for k, g in groups]
[[], [], []]

>>> [(k, list(g)) for k, g in groupby([1, 3, 2, 4, 5], key=lambda x: x % 2)]
[(1, [1, 3]), (0, [2, 4]), (1, [5])]

>>> list(chain('ab', [1], ()))
['a', 'b', 1]
>>> list(chain.from_iterable([[1, 2], [3]]))
[1, 2, 3]
>>> list(itertools.islice(itertools.count(10, 5), 3))
[10, 15, 20]
>>> list(itertools.islice('abcdefg', 1, 6, 2))
['b', 'd', 'f']

>>> list(zip('abc', [1]))
[('a', 1)]
>>> list(itertools.zip_longest('abc', [1], fillvalue=0))
[('a', 1), ('b', 0), ('c', 0)]

>>> list(itertools.takewhile(lambda x: x < 3, [1, 2, 5, 1]))
[1, 2]
>>> list(itertools.dropwhile(lambda x: x < 3, [1, 2, 5, 1]))
[5, 1]
>>> list(itertools.compress('abcd', [1, 0, 1, 0]))
['a', 'c']

>>> list(itertools.pairwise([1, 4, 9, 16]))
[(1, 4), (4, 9), (9, 16)]
>>> [b - a for a, b in itertools.pairwise([1, 4, 9, 16])]
[3, 5, 7]

>>> list(itertools.islice(itertools.cycle('ab'), 5))
['a', 'b', 'a', 'b', 'a']
>>> list(map(pow, [2, 3], itertools.repeat(2)))
[4, 9]
>>> list(itertools.starmap(pow, [(2, 3), (3, 2)]))
[8, 9]

>>> reduce(operator.xor, [5, 3, 5])
3
>>> reduce(lambda acc, x: acc * 10 + x, [1, 2, 3], 0)
123
>>> reduce(operator.add, [])
TypeError

>>> calls = []
>>> @cache
... def sq(x):
...     calls.append(x)
...     return x * x
>>> sq(4), sq(4), sq(5)
(16, 16, 25)
>>> calls
[4, 5]
>>> sq.cache_info().hits
1

>>> @cache
... def total(xs):
...     return sum(xs)
>>> total((1, 2))
3
>>> total([1, 2])
TypeError

>>> calls = []
>>> @lru_cache(maxsize=None)
... def f(x):
...     calls.append(x)
...     return x
>>> f(1), f(x=1), f(1)
(1, 1, 1)
>>> len(calls)
2

>>> def by_concat(a, b):
...     return -1 if a + b > b + a else (1 if a + b < b + a else 0)
>>> ''.join(sorted(['3', '30', '34', '5', '9'], key=cmp_to_key(by_concat)))
'9534330'

>>> base2 = functools.partial(int, base=2)
>>> base2('1011')
11
>>> base2('12')
ValueError

>>> pairs = [('b', 2), ('a', 2), ('c', 1)]
>>> sorted(pairs, key=operator.itemgetter(1))
[('c', 1), ('b', 2), ('a', 2)]
>>> operator.itemgetter(1, 0)(('x', 'y'))
('y', 'x')
>>> operator.itemgetter(-1)('hello')
'o'

>>> @functools.total_ordering
... class V:
...     def __init__(self, x):
...         self.x = x
...     def __eq__(self, other):
...         return self.x == other.x
...     def __lt__(self, other):
...         return self.x < other.x
>>> V(1) >= V(2), V(3) > V(2), V(2) <= V(2)
(False, True, True)
"""

_MISSING = object()


def my_accumulate(iterable, func=operator.add, *, initial=None):
    it = iter(iterable)
    total = next(it, _MISSING) if initial is None else initial
    if total is _MISSING:
        return
    yield total
    for x in it:
        total = func(total, x)
        yield total


def my_product(*iterables, repeat=1):
    pools = [tuple(p) for p in iterables] * repeat
    result = [()]
    for pool in pools:
        result = [prefix + (x,) for prefix in result for x in pool]
    yield from result


def my_permutations(iterable, r=None):
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    used, path = [False] * n, []

    def build():
        if len(path) == r:
            yield tuple(path)
            return
        for i in range(n):          # indexes in increasing order -> library order
            if not used[i]:
                used[i] = True
                path.append(pool[i])
                yield from build()
                path.pop()
                used[i] = False

    if r <= n:
        yield from build()


def my_combinations(iterable, r):
    pool = tuple(iterable)
    n = len(pool)
    path = []

    def build(start):
        if len(path) == r:
            yield tuple(path)
            return
        # leave room for the r - len(path) - 1 items still to pick after i
        for i in range(start, n - (r - len(path)) + 1):
            path.append(pool[i])
            yield from build(i + 1)
            path.pop()

    yield from build(0)


def my_groupby(iterable, key=None):
    key = key or (lambda x: x)
    run, run_key = [], None
    for x in iterable:
        k = key(x)
        if not run:
            run_key = k
        elif k != run_key:
            yield run_key, run
            run, run_key = [], k
        run.append(x)
    if run:
        yield run_key, run


def my_pairwise(iterable):
    it = iter(iterable)
    prev = next(it, _MISSING)
    if prev is _MISSING:
        return
    for x in it:
        yield prev, x
        prev = x


def my_zip_longest(*iterables, fillvalue=None):
    iterators = [iter(it) for it in iterables]
    remaining = len(iterators)
    while remaining:
        row = []
        for i, it in enumerate(iterators):
            value = next(it, _MISSING)
            if value is _MISSING:
                remaining -= 1
                if not remaining:
                    return
                iterators[i] = itertools.repeat(fillvalue)
                value = fillvalue
            row.append(value)
        yield tuple(row)


def my_reduce(func, iterable, *initial):
    if len(initial) > 1:
        raise TypeError("my_reduce takes at most 3 arguments")
    it = iter(iterable)
    acc = initial[0] if initial else next(it, _MISSING)
    if acc is _MISSING:
        raise TypeError("my_reduce() of empty iterable with no initial value")
    for x in it:
        acc = func(acc, x)
    return acc


def memoize(func):
    cache = {}

    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    wrapper.cache = cache
    wrapper.cache_clear = cache.clear
    return wrapper


def powerset(iterable):
    items = list(iterable)
    return chain.from_iterable(combinations(items, r) for r in range(len(items) + 1))


def biggest_concat(nums):
    def order(a, b):
        # a goes first when it makes the bigger concatenation
        return (b + a > a + b) - (b + a < a + b)

    return ''.join(sorted(map(str, nums), key=cmp_to_key(order))).lstrip('0') or '0'


def compose(*funcs):
    def composed(x):
        for f in reversed(funcs):
            x = f(x)
        return x

    return composed
