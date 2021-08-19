"""R10 - itertools, functools, operator

Everything in itertools is a lazy, one-shot iterator: wrap it in list() to look.
Know the sizes before generating: permutations of n items -> n!, combinations
(n, k) -> C(n, k), product(range(k), repeat=n) -> k**n. groupby only groups
ADJACENT equal keys (sort by the same key first to group everything), and each
group is a lazy view that dies when you move on. accumulate(xs, initial=0)
gives prefix sums with the leading 0. functools.cache memoizes calls whose
arguments are hashable; cmp_to_key turns a two-argument comparator into a sort
key. itertools.pairwise needs Python 3.10+, itertools.batched 3.12+.

Part 1 - Predict. Each block in PREDICT is a REPL session. Replace every ???
with exactly what Python prints: expression values are echoed the way the REPL
echoes them, and a line that raises prints just the exception name (TypeError).

Part 2 - Drills. The my_* functions rebuild library tools by hand, so don't use
the tool you're rebuilding (the tests compare your output with it); the last
four use the library the way real code does. Implement everything until
`python check.py 10` is green. Don't edit the tests at the bottom; add your own
test_* functions if you like.

Unlocks: brute-force generators for stress tests, prefix sums, run-length and
grouping work, and sorting by a custom comparator.
"""
import functools
import itertools
import operator
import random
from functools import cmp_to_key
from itertools import chain, combinations

PREDICT = r"""
>>> list(accumulate([1, 2, 3, 4]))
???
>>> list(accumulate([1, 2, 3], initial=0))
???
>>> list(accumulate([3, 1, 4, 1, 5], max))
???
>>> list(accumulate([1, 2, 3, 4], operator.mul))
???

>>> list(product('ab', range(2)))
???
>>> len(list(product(range(3), repeat=4)))
???

>>> list(permutations('abc', 2))
???
>>> list(combinations('abcd', 2))
???
>>> list(itertools.combinations_with_replacement('ab', 2))
???

>>> list(combinations([1, 1, 2], 2))
???
>>> len(list(permutations('aab'))), len(set(permutations('aab')))
???

>>> [(k, len(list(g))) for k, g in groupby('aabbbac')]
???
>>> [(k, len(list(g))) for k, g in groupby(sorted('aabbbac'))]
???

>>> groups = list(groupby('aabbbc'))
>>> [list(g) for k, g in groups]
???

>>> [(k, list(g)) for k, g in groupby([1, 3, 2, 4, 5], key=lambda x: x % 2)]
???

>>> list(chain('ab', [1], ()))
???
>>> list(chain.from_iterable([[1, 2], [3]]))
???
>>> list(itertools.islice(itertools.count(10, 5), 3))
???
>>> list(itertools.islice('abcdefg', 1, 6, 2))
???

>>> list(zip('abc', [1]))
???
>>> list(itertools.zip_longest('abc', [1], fillvalue=0))
???

>>> list(itertools.takewhile(lambda x: x < 3, [1, 2, 5, 1]))
???
>>> list(itertools.dropwhile(lambda x: x < 3, [1, 2, 5, 1]))
???
>>> list(itertools.compress('abcd', [1, 0, 1, 0]))
???

>>> list(itertools.pairwise([1, 4, 9, 16]))
???
>>> [b - a for a, b in itertools.pairwise([1, 4, 9, 16])]
???

>>> list(itertools.islice(itertools.cycle('ab'), 5))
???
>>> list(map(pow, [2, 3], itertools.repeat(2)))
???
>>> list(itertools.starmap(pow, [(2, 3), (3, 2)]))
???

>>> reduce(operator.xor, [5, 3, 5])
???
>>> reduce(lambda acc, x: acc * 10 + x, [1, 2, 3], 0)
???
>>> reduce(operator.add, [])
???

>>> calls = []
>>> @cache
... def sq(x):
...     calls.append(x)
...     return x * x
>>> sq(4), sq(4), sq(5)
???
>>> calls
???
>>> sq.cache_info().hits
???

>>> @cache
... def total(xs):
...     return sum(xs)
>>> total((1, 2))
???
>>> total([1, 2])
???

>>> calls = []
>>> @lru_cache(maxsize=None)
... def f(x):
...     calls.append(x)
...     return x
>>> f(1), f(x=1), f(1)
???
>>> len(calls)
???

>>> def by_concat(a, b):
...     return -1 if a + b > b + a else (1 if a + b < b + a else 0)
>>> ''.join(sorted(['3', '30', '34', '5', '9'], key=cmp_to_key(by_concat)))
???

>>> base2 = functools.partial(int, base=2)
>>> base2('1011')
???
>>> base2('12')
???

>>> pairs = [('b', 2), ('a', 2), ('c', 1)]
>>> sorted(pairs, key=operator.itemgetter(1))
???
>>> operator.itemgetter(1, 0)(('x', 'y'))
???
>>> operator.itemgetter(-1)('hello')
???

>>> @functools.total_ordering
... class V:
...     def __init__(self, x):
...         self.x = x
...     def __eq__(self, other):
...         return self.x == other.x
...     def __lt__(self, other):
...         return self.x < other.x
>>> V(1) >= V(2), V(3) > V(2), V(2) <= V(2)
???
"""


# ---------------------------------------------------------------- drills

def my_accumulate(iterable, func=operator.add, *, initial=None):
    """Running results, like itertools.accumulate: yield each partial result
    of func applied left to right; with initial, yield it first.
    list(my_accumulate([1, 2, 3], initial=0)) == [0, 1, 3, 6]. Lazy."""
    raise NotImplementedError


def my_product(*iterables, repeat=1):
    """Cartesian product, like itertools.product: tuples in odometer order (the
    rightmost input changes fastest). Inputs may be one-shot iterators.
    list(my_product('ab', [0, 1])) == [('a', 0), ('a', 1), ('b', 0), ('b', 1)]"""
    raise NotImplementedError


def my_permutations(iterable, r=None):
    """r-length orderings, like itertools.permutations and in the same order.
    It permutes positions, so repeated input values give repeated tuples.
    r defaults to the number of items; r larger than that yields nothing."""
    raise NotImplementedError


def my_combinations(iterable, r):
    """r-length selections that keep input order, like itertools.combinations
    and in the same order.
    list(my_combinations('abc', 2)) == [('a', 'b'), ('a', 'c'), ('b', 'c')]"""
    raise NotImplementedError


def my_groupby(iterable, key=None):
    """Like itertools.groupby, but each group is a plain list: yield
    (key, items) for every run of ADJACENT items with equal key(item). key=None
    means the item itself. Lazy: yield each run as soon as it ends."""
    raise NotImplementedError


def my_pairwise(iterable):
    """Overlapping pairs, like itertools.pairwise: [1, 2, 3] -> (1, 2), (2, 3).
    Lazy, and the input may be a one-shot iterator."""
    raise NotImplementedError


def my_zip_longest(*iterables, fillvalue=None):
    """Like itertools.zip_longest: keep zipping until the LONGEST input runs
    out, padding the finished ones with fillvalue."""
    raise NotImplementedError


def my_reduce(func, iterable, *initial):
    """Like functools.reduce: my_reduce(f, [a, b, c]) == f(f(a, b), c). An
    optional third argument seeds the fold: my_reduce(f, [], 10) == 10. Empty
    input with no seed raises TypeError."""
    raise NotImplementedError


def memoize(func):
    """Decorator that caches results by the tuple of positional arguments (a
    small functools.cache). The wrapper keeps func's name (functools.wraps),
    exposes its dict as wrapper.cache ({(4,): 16, ...}), and wrapper.cache_clear()
    empties it. Unhashable arguments raise TypeError."""
    raise NotImplementedError


def powerset(iterable):
    """Every subset as a tuple, smallest first, each size in combinations order:
    list(powerset('ab')) == [(), ('a',), ('b',), ('a', 'b')]. Build it from
    itertools pieces. The input may be a one-shot iterator."""
    raise NotImplementedError


def biggest_concat(nums):
    """Order non-negative ints so their concatenation is as large as possible
    and return it as a string without leading zeros:
    biggest_concat([3, 30, 34, 5, 9]) == '9534330'. Sort with a pairwise
    comparator wrapped in functools.cmp_to_key."""
    raise NotImplementedError


def compose(*funcs):
    """compose(f, g, h)(x) == f(g(h(x))): the rightmost function runs first.
    compose() returns the identity function."""
    raise NotImplementedError


# ---------------------------------------------------------------- tests (don't edit)

def _endless(start=0, step=1, limit=10_000):
    """Counts like itertools.count, but fails the test instead of running
    forever (and eating memory) when someone tries to read all of it."""
    for i in range(limit):
        yield start + i * step
    raise AssertionError("tried to read an endless input to the end: stay lazy")


def _lib_groupby(xs, key=None):
    return [(k, list(g)) for k, g in itertools.groupby(xs, key)]


def _fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def test_my_accumulate():
    assert list(my_accumulate([1, 2, 3, 4])) == [1, 3, 6, 10]
    assert list(my_accumulate([1, 2, 3], initial=0)) == [0, 1, 3, 6]
    assert list(my_accumulate([], initial=5)) == [5]
    assert list(my_accumulate([])) == []
    assert list(my_accumulate([3, 1, 4, 1, 5], max)) == [3, 3, 4, 4, 5]
    rng = random.Random(10)
    for _ in range(100):
        xs = [rng.randint(-5, 5) for _ in range(rng.randint(0, 8))]
        assert list(my_accumulate(xs, operator.mul)) == list(itertools.accumulate(xs, operator.mul)), xs
        assert list(my_accumulate(xs, initial=1)) == list(itertools.accumulate(xs, initial=1)), xs
    assert list(itertools.islice(my_accumulate(_endless(1)), 4)) == [1, 3, 6, 10]


def test_my_product():
    assert list(my_product('ab', [0, 1])) == [('a', 0), ('a', 1), ('b', 0), ('b', 1)]
    assert list(my_product()) == [()], "the product of nothing is one empty tuple"
    assert list(my_product('ab', [])) == []
    assert list(my_product(range(2), repeat=3)) == list(itertools.product(range(2), repeat=3))
    rng = random.Random(10)
    for _ in range(60):
        pools = [list(range(rng.randint(0, 3))) for _ in range(rng.randint(0, 3))]
        r = rng.randint(0, 2)
        assert list(my_product(*pools, repeat=r)) == list(itertools.product(*pools, repeat=r)), (pools, r)
    assert list(my_product(iter('ab'), iter('cd'))) == list(itertools.product('ab', 'cd')), \
        "an inner one-shot iterator got used up: copy each input to a tuple first"


def test_my_permutations():
    assert list(my_permutations('abc', 2)) == list(itertools.permutations('abc', 2))
    assert list(my_permutations([1, 2, 3])) == list(itertools.permutations([1, 2, 3]))
    assert list(my_permutations('aab')) == list(itertools.permutations('aab')), "permute positions, not values"
    assert list(my_permutations('ab', 0)) == [()]
    assert list(my_permutations('ab', 3)) == []
    assert list(my_permutations([])) == [()]
    assert len(list(my_permutations(range(6)))) == 720
    assert list(my_permutations(iter('xyz'), 2)) == list(itertools.permutations('xyz', 2))


def test_my_combinations():
    cases = [('abcd', 2), ('abcd', 0), ('abcd', 4), ('abc', 5), ([1, 1, 2], 2), (range(6), 3), ('', 0)]
    for items, r in cases:
        assert list(my_combinations(items, r)) == list(itertools.combinations(items, r)), (items, r)
    assert list(my_combinations(iter('wxyz'), 3)) == list(itertools.combinations('wxyz', 3))


def test_my_groupby():
    assert list(my_groupby('aabbbac')) == [('a', ['a', 'a']), ('b', ['b', 'b', 'b']), ('a', ['a']), ('c', ['c'])]
    assert list(my_groupby([])) == []
    assert list(my_groupby([1, 3, 2, 4, 5], key=lambda x: x % 2)) == [(1, [1, 3]), (0, [2, 4]), (1, [5])]
    rng = random.Random(10)
    for _ in range(100):
        xs = [rng.randint(0, 2) for _ in range(rng.randint(0, 10))]
        assert list(my_groupby(xs)) == _lib_groupby(xs), xs
        assert list(my_groupby(xs, key=lambda x: x > 0)) == _lib_groupby(xs, key=lambda x: x > 0), xs
    stream = my_groupby(chain('aab', map(lambda _: 'z', _endless())))
    assert next(stream) == ('a', ['a', 'a']) and next(stream) == ('b', ['b'])


def test_my_pairwise():
    assert list(my_pairwise([1, 4, 9, 16])) == [(1, 4), (4, 9), (9, 16)]
    assert list(my_pairwise([1])) == [] and list(my_pairwise([])) == []
    assert list(my_pairwise(iter('abc'))) == [('a', 'b'), ('b', 'c')], "the input may be a one-shot iterator"
    assert list(itertools.islice(my_pairwise(_endless()), 3)) == [(0, 1), (1, 2), (2, 3)]


def test_my_zip_longest():
    assert list(my_zip_longest('abc', [1], fillvalue=0)) == [('a', 1), ('b', 0), ('c', 0)]
    assert list(my_zip_longest()) == []
    assert list(my_zip_longest([], [])) == []
    rng = random.Random(10)
    for _ in range(100):
        seqs = [list(range(rng.randint(0, 4))) for _ in range(rng.randint(1, 4))]
        assert list(my_zip_longest(*seqs, fillvalue='-')) == list(itertools.zip_longest(*seqs, fillvalue='-')), seqs
    assert list(my_zip_longest(iter('ab'), iter('xyz'))) == [('a', 'x'), ('b', 'y'), (None, 'z')]


def test_my_reduce():
    assert my_reduce(operator.add, [1, 2, 3]) == 6
    assert my_reduce(operator.add, [], 10) == 10
    assert my_reduce(lambda acc, x: acc * 10 + x, [1, 2, 3], 0) == 123
    assert my_reduce(operator.sub, [10, 1, 2]) == 7, "fold from the left: (10 - 1) - 2"
    assert my_reduce(max, iter([3, 9, 2])) == 9
    assert my_reduce(lambda acc, x: [acc, x], [5], None) == [None, 5], "an explicit None seed is still a seed"
    try:
        my_reduce(operator.add, [])
    except TypeError:
        pass
    else:
        raise AssertionError("empty input with no seed should raise TypeError")
    rng = random.Random(10)
    for _ in range(50):
        xs = [rng.randint(-9, 9) for _ in range(rng.randint(1, 8))]
        assert my_reduce(operator.sub, xs) == functools.reduce(operator.sub, xs), xs


def test_memoize():
    calls = []

    @memoize
    def slow_square(x):
        calls.append(x)
        return x * x

    assert slow_square(4) == 16 and slow_square(4) == 16 and slow_square(5) == 25
    assert calls == [4, 5], "a repeated call should come from the cache"
    assert slow_square.cache == {(4,): 16, (5,): 25}
    slow_square.cache_clear()
    assert slow_square.cache == {}
    assert slow_square(4) == 16 and calls == [4, 5, 4]
    assert slow_square.__name__ == 'slow_square', "use functools.wraps to keep the name"
    try:
        slow_square([1])
    except TypeError:
        pass
    else:
        raise AssertionError("a list argument can't be a cache key: expect TypeError")

    @memoize
    def fib(n):
        return n if n < 2 else fib(n - 1) + fib(n - 2)

    assert fib(200) == _fib(200)


def test_powerset():
    assert list(powerset('abc')) == [(), ('a',), ('b',), ('c',), ('a', 'b'), ('a', 'c'), ('b', 'c'), ('a', 'b', 'c')]
    assert list(powerset([])) == [()]
    assert len(list(powerset(range(10)))) == 1024
    assert list(powerset(iter([1, 2]))) == [(), (1,), (2,), (1, 2)], "the input may be a one-shot iterator"


def test_biggest_concat():
    assert biggest_concat([3, 30, 34, 5, 9]) == '9534330'
    assert biggest_concat([10, 2]) == '210'
    assert biggest_concat([0, 0]) == '0', "strip the leading zeros"
    assert biggest_concat([1]) == '1'
    rng = random.Random(10)
    for _ in range(100):
        nums = [rng.randint(0, 120) for _ in range(rng.randint(1, 5))]
        best = max(''.join(map(str, p)) for p in itertools.permutations(nums))
        assert biggest_concat(nums) == str(int(best)), nums


def test_compose():
    inc = lambda x: x + 1
    dbl = lambda x: x * 2
    assert compose(inc, dbl)(5) == 11, "compose(f, g)(x) is f(g(x)): the rightmost runs first"
    assert compose(dbl, inc)(5) == 12
    assert compose()(7) == 7
    assert compose(str, abs, int)('-42') == '42'
    assert compose(*[inc] * 100)(0) == 100
