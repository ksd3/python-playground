"""R09 - Iterators and generators

iter(x) turns an iterable into an iterator; next(it) pulls one value and raises
StopIteration when it runs out (next(it, default) returns the default instead).
Iterators are one-shot: map, zip, filter, enumerate and generator expressions
are used up after a single pass. A function containing `yield` returns a
generator, and none of its body runs until the first next(). `yield from sub`
hands off to a sub-iterator: the clean way to write recursive generators.
Changing a container while looping over it: a list may grow (the loop sees the
new items), but a dict, set or deque raises RuntimeError.

Part 1 - Predict. Each block in PREDICT is a REPL session. Replace every ???
with exactly what Python prints: expression values are echoed the way the REPL
echoes them, and a line that raises prints just the exception name (TypeError).

Part 2 - Drills. Implement every function and class until `python check.py 9`
is green. Don't edit the tests at the bottom; add your own test_* functions if
you like.

Unlocks: iterator-design problems, tree iterators, merging sorted streams, and
lazy pipelines over input too big to hold in memory.
"""
import heapq
import itertools
import random
from collections import deque

PREDICT = r"""
>>> it = iter([1, 2])
>>> next(it), next(it)
???
>>> next(it, 'done')
???
>>> next(it)
???

>>> g = (x * x for x in range(3))
>>> list(g)
???
>>> list(g)
???

>>> m = map(int, '123')
>>> sum(m), sum(m)
???

>>> z = zip('ab', [1, 2])
>>> ('a', 1) in z
???
>>> list(z)
???

>>> g = iter(range(10))
>>> 5 in g
???
>>> next(g)
???

>>> r = range(3)
>>> list(r), list(r)
???
>>> next(r)
???

>>> it = iter([1, 2, 3])
>>> iter(it) is it
???
>>> xs = [1, 2, 3]
>>> iter(xs) is xs
???

>>> def gen():
...     print('start')
...     yield 1
...     print('middle')
...     yield 2
>>> g = gen()
>>> next(g)
???
>>> next(g)
???
>>> next(g, 'end')
???

>>> def g():
...     yield 1
...     return 99
>>> list(g())
???

>>> def both(a, b):
...     yield from a
...     yield from b
>>> list(both('ab', [1, 2]))
???

>>> xs = [1, 2, 3]
>>> g = (x for x in xs)
>>> xs = [9, 9]
>>> list(g)
???

>>> limit = 2
>>> g = (x for x in range(5) if x < limit)
>>> limit = 4
>>> list(g)
???

>>> def check(x):
...     print('checking', x)
...     return x > 1
>>> any(check(x) for x in [1, 2, 3])
???
>>> any([check(x) for x in [1, 2, 3]])
???

>>> next((x for x in [1, 3, 5] if x % 2 == 0), None) is None
???
>>> next(x for x in [1, 4, 6] if x % 2 == 0)
???

>>> it = iter([1, 2, 3, 4, 5])
>>> list(zip(it, it))
???
>>> list(it)
???

>>> def first_items():
...     it = iter([1])
...     while True:
...         yield next(it)
>>> list(first_items())
???

>>> nums = iter([4, 7, 0, 9])
>>> list(iter(lambda: next(nums), 0))
???
>>> next(nums)
???

>>> lst = [1]
>>> for x in lst:
...     if x < 4:
...         lst.append(x + 1)
>>> lst
???

>>> d = {1: 'a'}
>>> for k in d:
...     d[k + 1] = 'b'
???
>>> len(d)
???

>>> dq = deque([1, 2])
>>> for x in dq:
...     dq.append(x)
???
>>> dq
???
"""


class Node:
    """A binary tree node (given). Used by inorder and InorderIterator."""

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ---------------------------------------------------------------- drills

class Countdown:
    """An iterator counting down from n to 1: list(Countdown(3)) == [3, 2, 1].
    __iter__ returns self; __next__ raises StopIteration when it's done, and
    keeps raising it if called again."""

    def __init__(self, n):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def __next__(self):
        raise NotImplementedError


def countdown_gen(n):
    """The same countdown as a generator function:
    list(countdown_gen(3)) == [3, 2, 1]."""
    raise NotImplementedError


class Span:
    """A re-iterable range: Span(start, stop, step=1) yields the same values as
    range(start, stop, step), and every loop over it starts fresh (two nested
    loops over one Span must not interfere). Span(0, 5, 0) raises ValueError."""

    def __init__(self, start, stop, step=1):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError


def take(n, iterable):
    """Return the first n items as a list, consuming exactly n items (or all of
    them if there are fewer). Works on endless input:
    take(2, itertools.count()) == [0, 1]."""
    raise NotImplementedError


def first_match(iterable, pred, default=None):
    """Return the first item for which pred(item) is true, else default, and
    stop consuming at the match.
    first_match([1, 4, 6], lambda x: x % 2 == 0) == 4"""
    raise NotImplementedError


def chunked(iterable, size):
    """Lazily yield lists of `size` items; the last one may be shorter.
    list(chunked(range(5), 2)) == [[0, 1], [2, 3], [4]]. Must work on endless
    input. size < 1 raises ValueError. (Python 3.12 adds itertools.batched,
    which yields tuples.)"""
    raise NotImplementedError


def flatten(nested):
    """Recursive generator (use `yield from`): yield the leaves of nested lists
    and tuples in order. Anything that isn't a list or tuple is a leaf, strings
    included. list(flatten([1, [2, [3, (4,)]], 'ab'])) == [1, 2, 3, 4, 'ab']"""
    raise NotImplementedError


def flatten_iter(nested):
    """Same output as flatten, but with an explicit stack of iterators instead
    of recursion, so 5000 levels of nesting work. Still a generator."""
    raise NotImplementedError


def inorder(root):
    """Recursive generator yielding a binary tree's values in order (left
    subtree, node, right subtree). inorder(None) yields nothing."""
    raise NotImplementedError


class InorderIterator:
    """Step-by-step inorder traversal with an explicit stack: O(height) memory
    and no recursion. has_next() says whether a value is left; next(it) returns
    the next value or raises StopIteration. A for loop over it must work too."""

    def __init__(self, root):
        raise NotImplementedError

    def has_next(self):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def __next__(self):
        raise NotImplementedError


class Peekable:
    """Wrap any iterable. peek() returns the next item without consuming it
    (raising StopIteration if there is none); has_next() returns True/False;
    next(p) and for loops work as usual. Only pull from the wrapped iterator
    when a value is actually needed. None and 0 are ordinary items."""

    def __init__(self, iterable):
        raise NotImplementedError

    def peek(self):
        raise NotImplementedError

    def has_next(self):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def __next__(self):
        raise NotImplementedError


def merge_sorted(*iterables):
    """Lazily merge already-sorted iterables into one sorted stream with a heap
    (don't use sorted() or heapq.merge). Must work on endless inputs, and on
    ties it must never compare the iterators themselves.
    list(merge_sorted([1, 4], [2, 3])) == [1, 2, 3, 4]"""
    raise NotImplementedError


def round_robin(*iterables):
    """Yield one item from each iterable in turn, dropping each one as it runs
    out: ''.join(round_robin('ABC', 'D', 'EF')) == 'ADEBFC'. Lazy."""
    raise NotImplementedError


def prune(d, pred):
    """Delete, in place, every key of dict d for which pred(key, value) is
    true, and return None. (Deleting while looping over d raises RuntimeError.)
    d = {'a': 1, 'b': 2}; prune(d, lambda k, v: v > 1)  ->  d == {'a': 1}"""
    raise NotImplementedError


# ---------------------------------------------------------------- tests (don't edit)

def _endless(start=0, step=1, limit=10_000):
    """Counts like itertools.count, but fails the test instead of running
    forever (and eating memory) when someone tries to read all of it."""
    for i in range(limit):
        yield start + i * step
    raise AssertionError("tried to read an endless input to the end: stay lazy")


def _raises_stop(call):
    try:
        call()
    except StopIteration:
        return True
    return False


def _bst(values):
    root = None
    for v in values:
        if root is None:
            root = Node(v)
            continue
        node = root
        while True:
            side = 'left' if v < node.val else 'right'
            child = getattr(node, side)
            if child is None:
                setattr(node, side, Node(v))
                break
            node = child
    return root


def test_countdown():
    c = Countdown(3)
    assert iter(c) is c, "__iter__ should return self"
    assert next(c) == 3
    assert list(c) == [2, 1]
    assert _raises_stop(lambda: next(c)), "an exhausted iterator must keep raising StopIteration"
    assert list(Countdown(0)) == []


def test_countdown_gen():
    g = countdown_gen(3)
    assert iter(g) is g, "return a generator (use yield), not a list"
    assert list(g) == [3, 2, 1]
    assert list(g) == [], "a generator is one-shot"
    assert list(countdown_gen(0)) == []


def test_span():
    s = Span(0, 5)
    assert list(s) == [0, 1, 2, 3, 4]
    assert list(s) == [0, 1, 2, 3, 4], "the second loop got nothing: __iter__ must return a fresh iterator"
    assert iter(s) is not s
    assert len([(x, y) for x in s for y in s]) == 25, "nested loops over one Span interfered"
    rng = random.Random(9)
    for _ in range(200):
        a, b = rng.randint(-10, 10), rng.randint(-10, 10)
        step = rng.choice([-3, -2, -1, 1, 2, 3])
        assert list(Span(a, b, step)) == list(range(a, b, step)), (a, b, step)
    try:
        Span(0, 5, 0)
    except ValueError:
        pass
    else:
        raise AssertionError("Span(0, 5, 0) should raise ValueError")


def test_take():
    assert take(3, 'abcdef') == ['a', 'b', 'c']
    assert take(0, [1, 2]) == []
    assert take(5, [1, 2]) == [1, 2]
    assert take(4, _endless()) == [0, 1, 2, 3]
    it = iter(range(10))
    assert take(3, it) == [0, 1, 2]
    assert next(it) == 3, "take consumed more than n items"
    it = iter(range(10))
    take(0, it)
    assert next(it) == 0, "take(0, ...) must not consume anything"


def test_first_match():
    assert first_match([1, 3, 4, 6], lambda x: x % 2 == 0) == 4
    assert first_match([1, 3], lambda x: x % 2 == 0) is None
    assert first_match([1, 3], lambda x: x % 2 == 0, default=-1) == -1
    assert first_match(_endless(1), lambda x: x * x > 50) == 8
    it = iter([5, 10, 15, 20])
    assert first_match(it, lambda x: x > 7) == 10
    assert next(it) == 15, "first_match must stop at the first hit"
    assert first_match([0, None, ''], lambda x: True) == 0, "a falsy match is still a match"


def test_chunked():
    assert list(chunked(range(7), 3)) == [[0, 1, 2], [3, 4, 5], [6]]
    assert list(chunked([], 2)) == []
    assert list(chunked('abcd', 2)) == [['a', 'b'], ['c', 'd']]
    stream = chunked(_endless(), 2)
    assert next(stream) == [0, 1] and next(stream) == [2, 3]
    try:
        list(chunked([1], 0))
    except ValueError:
        pass
    else:
        raise AssertionError("size < 1 should raise ValueError")


def test_flatten():
    assert list(flatten([1, [2, [3, (4,)]], [], 5])) == [1, 2, 3, 4, 5]
    assert list(flatten(['ab', ['c', ['de']]])) == ['ab', 'c', 'de'], "strings are leaves, not containers"
    assert list(flatten([])) == []
    g = flatten([[1], [2]])
    assert iter(g) is g, "flatten should be a generator"


def test_flatten_iter():
    assert list(flatten_iter([1, [2, [3, (4,)]], [], 5])) == [1, 2, 3, 4, 5]
    assert list(flatten_iter(['ab', ['c', ['de']]])) == ['ab', 'c', 'de']
    assert list(flatten_iter([])) == []
    deep = [7]
    for _ in range(5000):
        deep = [deep]
    try:
        out = list(flatten_iter(deep))
    except RecursionError:
        raise AssertionError("hit the recursion limit: keep a stack of iterators instead of recursing")
    assert out == [7]
    g = flatten_iter([[1], [2]])
    assert iter(g) is g, "flatten_iter should be a generator"


def test_inorder():
    root = _bst([5, 3, 8, 1, 4, 7, 9])
    assert list(inorder(root)) == [1, 3, 4, 5, 7, 8, 9]
    assert list(inorder(None)) == []
    g = inorder(root)
    assert iter(g) is g, "inorder should be a generator"
    assert next(g) == 1


def test_inorder_iterator():
    it = InorderIterator(_bst([5, 3, 8, 1, 4, 7, 9]))
    assert iter(it) is it
    out = []
    while it.has_next():
        assert it.has_next(), "has_next() must not advance the iterator"
        out.append(next(it))
    assert out == [1, 3, 4, 5, 7, 8, 9]
    assert not it.has_next()
    assert _raises_stop(lambda: next(it)), "an exhausted iterator should raise StopIteration"
    assert list(InorderIterator(None)) == []
    chain_root = None
    for v in range(3000):
        chain_root = Node(v, left=chain_root)
    try:
        assert list(InorderIterator(chain_root)) == list(range(3000))
    except RecursionError:
        raise AssertionError("hit the recursion limit: use an explicit stack")


def test_peekable():
    p = Peekable([1, 2])
    assert iter(p) is p
    assert p.peek() == 1 and p.peek() == 1, "peek must not consume"
    assert next(p) == 1
    assert p.has_next() and p.peek() == 2
    assert next(p) == 2
    assert p.has_next() is False
    assert _raises_stop(p.peek), "peek on an exhausted Peekable should raise StopIteration"
    assert _raises_stop(lambda: next(p))
    pulls = []

    def source():
        for x in 'abc':
            pulls.append(x)
            yield x

    q = Peekable(source())
    assert pulls == [], "don't pull anything before it's needed"
    assert q.peek() == 'a' and pulls == ['a'], "peek should pull exactly one item"
    assert list(q) == ['a', 'b', 'c']
    assert list(Peekable([None, 0])) == [None, 0], "None and 0 are real items: don't use None as a marker"


def test_merge_sorted():
    assert list(merge_sorted([1, 4, 9], [2, 3], [], [5])) == [1, 2, 3, 4, 5, 9]
    assert list(merge_sorted()) == []
    rng = random.Random(9)
    for _ in range(100):
        lists = [sorted(rng.randint(0, 20) for _ in range(rng.randint(0, 6))) for _ in range(rng.randint(1, 5))]
        assert list(merge_sorted(*lists)) == sorted(itertools.chain(*lists)), lists
    try:
        out = list(merge_sorted([1, 1], [1, 1], [1]))
    except TypeError:
        raise AssertionError("a tie compared two iterators: put a unique index in each heap entry")
    assert out == [1, 1, 1, 1, 1]
    stream = merge_sorted(_endless(0, 2), _endless(1, 2))
    assert list(itertools.islice(stream, 6)) == [0, 1, 2, 3, 4, 5]


def test_round_robin():
    assert ''.join(round_robin('ABC', 'D', 'EF')) == 'ADEBFC'
    assert list(round_robin()) == []
    assert list(round_robin([], [1], [])) == [1]
    assert list(itertools.islice(round_robin(_endless(), 'xy'), 6)) == [0, 'x', 1, 'y', 2, 3]


def test_prune():
    d = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    alias = d
    assert prune(d, lambda k, v: v % 2 == 0) is None
    assert alias is d and d == {'a': 1, 'c': 3}
    assert list(d) == ['a', 'c'], "the remaining keys should keep their order"
    d = {i: i for i in range(100)}
    prune(d, lambda k, v: True)
    assert d == {}
