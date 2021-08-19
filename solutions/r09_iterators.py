"""R09 - Iterators and generators (reference solutions)

Compare after you've made your own attempt. Run: python check.py 9 -s
"""
import heapq
import itertools
from collections import deque

PREDICT = r"""
>>> it = iter([1, 2])
>>> next(it), next(it)
(1, 2)
>>> next(it, 'done')
'done'
>>> next(it)
StopIteration

>>> g = (x * x for x in range(3))
>>> list(g)
[0, 1, 4]
>>> list(g)
[]

>>> m = map(int, '123')
>>> sum(m), sum(m)
(6, 0)

>>> z = zip('ab', [1, 2])
>>> ('a', 1) in z
True
>>> list(z)
[('b', 2)]

>>> g = iter(range(10))
>>> 5 in g
True
>>> next(g)
6

>>> r = range(3)
>>> list(r), list(r)
([0, 1, 2], [0, 1, 2])
>>> next(r)
TypeError

>>> it = iter([1, 2, 3])
>>> iter(it) is it
True
>>> xs = [1, 2, 3]
>>> iter(xs) is xs
False

>>> def gen():
...     print('start')
...     yield 1
...     print('middle')
...     yield 2
>>> g = gen()
>>> next(g)
start
1
>>> next(g)
middle
2
>>> next(g, 'end')
'end'

>>> def g():
...     yield 1
...     return 99
>>> list(g())
[1]

>>> def both(a, b):
...     yield from a
...     yield from b
>>> list(both('ab', [1, 2]))
['a', 'b', 1, 2]

>>> xs = [1, 2, 3]
>>> g = (x for x in xs)
>>> xs = [9, 9]
>>> list(g)
[1, 2, 3]

>>> limit = 2
>>> g = (x for x in range(5) if x < limit)
>>> limit = 4
>>> list(g)
[0, 1, 2, 3]

>>> def check(x):
...     print('checking', x)
...     return x > 1
>>> any(check(x) for x in [1, 2, 3])
checking 1
checking 2
True
>>> any([check(x) for x in [1, 2, 3]])
checking 1
checking 2
checking 3
True

>>> next((x for x in [1, 3, 5] if x % 2 == 0), None) is None
True
>>> next(x for x in [1, 4, 6] if x % 2 == 0)
4

>>> it = iter([1, 2, 3, 4, 5])
>>> list(zip(it, it))
[(1, 2), (3, 4)]
>>> list(it)
[]

>>> def first_items():
...     it = iter([1])
...     while True:
...         yield next(it)
>>> list(first_items())
RuntimeError

>>> nums = iter([4, 7, 0, 9])
>>> list(iter(lambda: next(nums), 0))
[4, 7]
>>> next(nums)
9

>>> lst = [1]
>>> for x in lst:
...     if x < 4:
...         lst.append(x + 1)
>>> lst
[1, 2, 3, 4]

>>> d = {1: 'a'}
>>> for k in d:
...     d[k + 1] = 'b'
RuntimeError
>>> len(d)
2

>>> dq = deque([1, 2])
>>> for x in dq:
...     dq.append(x)
RuntimeError
>>> dq
deque([1, 2, 1])
"""


class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


_DONE = object()


class Countdown:
    def __init__(self, n):
        self.n = n

    def __iter__(self):
        return self

    def __next__(self):
        if self.n <= 0:
            raise StopIteration
        self.n -= 1
        return self.n + 1


def countdown_gen(n):
    while n > 0:
        yield n
        n -= 1


class Span:
    def __init__(self, start, stop, step=1):
        if step == 0:
            raise ValueError("step must not be zero")
        self.start, self.stop, self.step = start, stop, step

    def __iter__(self):
        # A generator method: every call hands out a brand-new iterator.
        i = self.start
        while (i < self.stop) if self.step > 0 else (i > self.stop):
            yield i
            i += self.step


def take(n, iterable):
    return list(itertools.islice(iterable, n))


def first_match(iterable, pred, default=None):
    return next((x for x in iterable if pred(x)), default)


def chunked(iterable, size):
    if size < 1:
        raise ValueError("size must be at least 1")
    it = iter(iterable)
    while chunk := list(itertools.islice(it, size)):
        yield chunk


def flatten(nested):
    for x in nested:
        if isinstance(x, (list, tuple)):
            yield from flatten(x)
        else:
            yield x


def flatten_iter(nested):
    stack = [iter(nested)]
    while stack:
        for x in stack[-1]:
            if isinstance(x, (list, tuple)):
                stack.append(iter(x))
                break           # descend; the outer iterator remembers where it was
            yield x
        else:
            stack.pop()         # the top iterator ran out


def inorder(root):
    if root:
        yield from inorder(root.left)
        yield root.val
        yield from inorder(root.right)


class InorderIterator:
    def __init__(self, root):
        self.stack = []
        self._push_left(root)

    def _push_left(self, node):
        while node:
            self.stack.append(node)
            node = node.left

    def has_next(self):
        return bool(self.stack)

    def __iter__(self):
        return self

    def __next__(self):
        if not self.stack:
            raise StopIteration
        node = self.stack.pop()
        self._push_left(node.right)
        return node.val


class Peekable:
    def __init__(self, iterable):
        self._it = iter(iterable)
        self._buf = []              # at most one peeked item; a list, so None can be an item

    def peek(self):
        if not self._buf:
            self._buf.append(next(self._it))
        return self._buf[0]

    def has_next(self):
        try:
            self.peek()
        except StopIteration:
            return False
        return True

    def __iter__(self):
        return self

    def __next__(self):
        if self._buf:
            return self._buf.pop()
        return next(self._it)


def merge_sorted(*iterables):
    heap = []
    for i, it in enumerate(map(iter, iterables)):
        first = next(it, _DONE)
        if first is not _DONE:
            heap.append((first, i, it))     # i breaks ties, so iterators are never compared
    heapq.heapify(heap)
    while heap:
        value, i, it = heap[0]
        yield value
        nxt = next(it, _DONE)
        if nxt is _DONE:
            heapq.heappop(heap)
        else:
            heapq.heapreplace(heap, (nxt, i, it))


def round_robin(*iterables):
    queue = deque(map(iter, iterables))
    while queue:
        it = queue.popleft()
        x = next(it, _DONE)
        if x is not _DONE:
            queue.append(it)
            yield x


def prune(d, pred):
    for k in [k for k, v in d.items() if pred(k, v)]:
        del d[k]
