"""R19 - Internals: hash map, heap, dynamic array (reference solutions)

Compare after you've made your own attempt. Run: python check.py 19 -s
"""
from collections import Counter
from heapq import heappop, heappush

PREDICT = r"""
>>> hash(1) == hash(1.0) == hash(True)
True

>>> hash(-1), hash(-2)
(-2, -2)

>>> hash(10), hash(2**61 - 1), hash(2**61)
(10, 0, 1)

>>> {[1, 2]: 'x'}
TypeError

>>> class Same:
...     def __init__(self, v):
...         self.v = v
...     def __hash__(self):
...         return 42
...     def __eq__(self, other):
...         return self.v == other.v
>>> len({Same(1), Same(2), Same(1)})
2

>>> class Key:
...     def __init__(self, v):
...         self.v = v
...     def __hash__(self):
...         return hash(self.v)
...     def __eq__(self, other):
...         return self.v == other.v
>>> k = Key(1)
>>> d = {k: 'one'}
>>> k.v = 2
>>> Key(1) in d, Key(2) in d, k in d
(False, False, False)

>>> nan = float('nan')
>>> d = {nan: 1}
>>> nan == nan, nan in d, float('nan') in d
(False, True, False)

>>> cap = 8
>>> [key % cap for key in (3, 11, 19, 4)]
[3, 3, 3, 4]

>>> d = {'a': 1, 'b': 2, 'c': 3}
>>> del d['a']
>>> d['a'] = 1
>>> list(d)
['b', 'c', 'a']

>>> d = {'a': 1, 'b': 2}
>>> d['a'] = 99
>>> list(d.items())
[('a', 99), ('b', 2)]

>>> a, sizes = [], []
>>> for i in range(20):
...     a.append(i)
...     sizes.append(sys.getsizeof(a))
>>> len(set(sizes)) < 20
True

>>> cap, size, copies = 1, 0, 0
>>> for _ in range(1000):
...     if size == cap:
...         copies += size
...         cap *= 2
...     size += 1
>>> cap, copies
(1024, 1023)

>>> i = 4
>>> (i - 1) // 2, 2 * i + 1, 2 * i + 2
(1, 9, 10)

>>> h = [5, 3, 8, 1]
>>> heapify(h)
>>> h
[1, 3, 8, 5]

>>> h = []
>>> for x in [5, 1, 4, 2]:
...     heappush(h, x)
>>> h[0], [heappop(h) for _ in range(len(h))]
(1, [1, 2, 4, 5])

>>> h = [3, 5]
>>> heappushpop(h, 1), h
(1, [3, 5])
>>> h = [3, 5]
>>> heapreplace(h, 1), h
(3, [1, 5])
"""


class MyHashMap:
    def __init__(self):
        self.capacity = 8
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]

    def _bucket(self, key):
        return self.buckets[hash(key) % self.capacity]

    def put(self, key, value):
        bucket = self._bucket(key)
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return
        bucket.append([key, value])
        self.size += 1
        if self.size > 0.75 * self.capacity:
            self._resize(2 * self.capacity)

    def _resize(self, capacity):
        old = self.buckets
        self.capacity = capacity
        self.buckets = [[] for _ in range(capacity)]
        for bucket in old:
            for pair in bucket:
                self._bucket(pair[0]).append(pair)

    def get(self, key, default=None):
        for k, v in self._bucket(key):
            if k == key:
                return v
        return default

    def remove(self, key):
        bucket = self._bucket(key)
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = bucket[-1]      # overwrite with the last pair, then drop the last: O(1)
                bucket.pop()
                self.size -= 1
                return True
        return False

    def __contains__(self, key):
        return any(k == key for k, _ in self._bucket(key))

    def __len__(self):
        return self.size


_EMPTY, _TOMBSTONE = object(), object()


class ProbingSet:
    def __init__(self, capacity=8):
        self.slots = [_EMPTY] * capacity
        self.live = 0
        self.used = 0                       # live values + tombstones

    def _find(self, x):
        """(index, found): x's slot if present, else the slot an insert should take."""
        n = len(self.slots)
        i = hash(x) % n
        first_tombstone = None
        while True:
            slot = self.slots[i]
            if slot is _EMPTY:
                return (i if first_tombstone is None else first_tombstone), False
            if slot is _TOMBSTONE:
                if first_tombstone is None:
                    first_tombstone = i
            elif slot == x:
                return i, True
            i = (i + 1) % n

    def _rebuild(self, capacity):
        values = [s for s in self.slots if s is not _EMPTY and s is not _TOMBSTONE]
        self.slots = [_EMPTY] * capacity
        self.live = self.used = 0
        for v in values:
            self.slots[self._find(v)[0]] = v
            self.live += 1
            self.used += 1

    def add(self, x):
        i, found = self._find(x)
        if found:
            return
        if self.slots[i] is _EMPTY:          # reusing a tombstone doesn't use up a slot
            if self.used + 1 > 2 * len(self.slots) / 3:
                self._rebuild(2 * len(self.slots))
                i = self._find(x)[0]
            self.used += 1
        self.slots[i] = x
        self.live += 1

    def discard(self, x):
        i, found = self._find(x)
        if found:
            self.slots[i] = _TOMBSTONE
            self.live -= 1

    def __contains__(self, x):
        return self._find(x)[1]

    def __len__(self):
        return self.live


def is_heap(a):
    return all(a[(i - 1) // 2] <= a[i] for i in range(1, len(a)))


def sift_up(a, i):
    while i > 0:
        parent = (i - 1) // 2
        if not a[i] < a[parent]:
            return
        a[i], a[parent] = a[parent], a[i]
        i = parent


def sift_down(a, i, n):
    while True:
        smallest, left, right = i, 2 * i + 1, 2 * i + 2
        if left < n and a[left] < a[smallest]:
            smallest = left
        if right < n and a[right] < a[smallest]:
            smallest = right
        if smallest == i:
            return
        a[i], a[smallest] = a[smallest], a[i]
        i = smallest


def heapify(a):
    # Most nodes are near the bottom and sift down only a level or two: O(n) total.
    for i in range(len(a) // 2 - 1, -1, -1):
        sift_down(a, i, len(a))


class MinHeap:
    def __init__(self):
        self.a = []

    def push(self, x):
        self.a.append(x)
        sift_up(self.a, len(self.a) - 1)

    def pop(self):
        if not self.a:
            raise IndexError("pop from an empty heap")
        a = self.a
        a[0], a[-1] = a[-1], a[0]
        smallest = a.pop()
        sift_down(a, 0, len(a))
        return smallest

    def peek(self):
        if not self.a:
            raise IndexError("peek at an empty heap")
        return self.a[0]

    def __len__(self):
        return len(self.a)


def heap_sort(a):
    out = list(a)
    heapify(out)
    for end in range(len(out) - 1, 0, -1):
        out[0], out[end] = out[end], out[0]   # move the current minimum behind the heap
        sift_down(out, 0, end)
    out.reverse()                             # a min-heap leaves the list descending
    return out


class DynamicArray:
    def __init__(self):
        self.capacity = 1
        self.slots = [None]
        self.size = 0
        self.copies = 0

    def append(self, x):
        if self.size == self.capacity:
            bigger = [None] * (2 * self.capacity)
            for i in range(self.size):
                bigger[i] = self.slots[i]
            self.copies += self.size
            self.slots, self.capacity = bigger, 2 * self.capacity
        self.slots[self.size] = x
        self.size += 1

    def pop(self):
        if self.size == 0:
            raise IndexError("pop from an empty array")
        self.size -= 1
        x, self.slots[self.size] = self.slots[self.size], None
        return x

    def _index(self, i):
        if i < 0:
            i += self.size
        if not 0 <= i < self.size:
            raise IndexError("index out of range")
        return i

    def __getitem__(self, i):
        return self.slots[self._index(i)]

    def __setitem__(self, i, x):
        self.slots[self._index(i)] = x

    def __len__(self):
        return self.size


class LazyHeap:
    def __init__(self):
        self.heap = []
        self.live = Counter()      # value -> live copies
        self.dead = Counter()      # value -> removed copies still sitting in the heap
        self.size = 0

    def push(self, x):
        heappush(self.heap, x)
        self.live[x] += 1
        self.size += 1

    def remove(self, x):
        if self.live[x] == 0:
            return False
        self.live[x] -= 1
        self.dead[x] += 1
        self.size -= 1
        return True

    def _drop_dead_top(self):
        while self.heap and self.dead[self.heap[0]]:
            self.dead[heappop(self.heap)] -= 1

    def pop(self):
        self._drop_dead_top()
        if not self.heap:
            raise IndexError("pop from an empty heap")
        x = heappop(self.heap)
        self.live[x] -= 1
        self.size -= 1
        return x

    def peek(self):
        self._drop_dead_top()
        if not self.heap:
            raise IndexError("peek at an empty heap")
        return self.heap[0]

    def __len__(self):
        return self.size
