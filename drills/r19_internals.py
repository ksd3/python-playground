"""R19 - Internals: hash map, heap, dynamic array

A dict or set is an array of slots indexed by hash(key) % capacity. Lookups are
O(1) on average because the table grows before it gets crowded; they degrade
to O(n) when every key collides. Equal keys must hash equal, which is why
mutable lists can't be keys. A binary heap is just a list: the children of i
sit at 2i+1 and 2i+2 and its parent at (i-1)//2; push sifts up, pop sifts down,
and bottom-up heapify is O(n). A dynamic array doubles its capacity when full,
so n appends copy fewer than 2n elements in total: amortized O(1) each.

Part 1 - Predict. Each block in PREDICT is a REPL session. Replace every ???
with exactly what Python prints: expression values are echoed the way the REPL
echoes them, and a line that raises prints just the exception name (TypeError).
(The hash() values here are CPython's on a 64-bit machine.)

Part 2 - Drills. Implement every function until `python check.py 19` is green.
Don't edit the tests at the bottom; add your own test_* functions if you like.

Unlocks: complexity reasoning you can trust, designing your own hash set/map,
and custom heap operations such as lazy deletion.
"""

PREDICT = r"""
>>> hash(1) == hash(1.0) == hash(True)
???

>>> hash(-1), hash(-2)
???

>>> hash(10), hash(2**61 - 1), hash(2**61)
???

>>> {[1, 2]: 'x'}
???

>>> class Same:
...     def __init__(self, v):
...         self.v = v
...     def __hash__(self):
...         return 42
...     def __eq__(self, other):
...         return self.v == other.v
>>> len({Same(1), Same(2), Same(1)})
???

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
???

>>> nan = float('nan')
>>> d = {nan: 1}
>>> nan == nan, nan in d, float('nan') in d
???

>>> cap = 8
>>> [key % cap for key in (3, 11, 19, 4)]
???

>>> d = {'a': 1, 'b': 2, 'c': 3}
>>> del d['a']
>>> d['a'] = 1
>>> list(d)
???

>>> d = {'a': 1, 'b': 2}
>>> d['a'] = 99
>>> list(d.items())
???

>>> a, sizes = [], []
>>> for i in range(20):
...     a.append(i)
...     sizes.append(sys.getsizeof(a))
>>> len(set(sizes)) < 20
???

>>> cap, size, copies = 1, 0, 0
>>> for _ in range(1000):
...     if size == cap:
...         copies += size
...         cap *= 2
...     size += 1
>>> cap, copies
???

>>> i = 4
>>> (i - 1) // 2, 2 * i + 1, 2 * i + 2
???

>>> h = [5, 3, 8, 1]
>>> heapify(h)
>>> h
???

>>> h = []
>>> for x in [5, 1, 4, 2]:
...     heappush(h, x)
>>> h[0], [heappop(h) for _ in range(len(h))]
???

>>> h = [3, 5]
>>> heappushpop(h, 1), h
???
>>> h = [3, 5]
>>> heapreplace(h, 1), h
???
"""


# ---------------------------------------------------------------- drills

class MyHashMap:
    """A hash map with separate chaining, built on plain lists (no dict or set).
    A key's bucket is hash(key) % self.capacity. Start with capacity 8 and double
    it (rehashing every entry) as soon as len(self) > 0.75 * capacity.

    put(key, value)           insert, or overwrite an existing key
    get(key, default=None)    the value, or default
    remove(key) -> bool       True if the key was there
    key in m, len(m)
    self.capacity             the current number of buckets
    """

    def __init__(self):
        raise NotImplementedError

    def put(self, key, value):
        raise NotImplementedError

    def get(self, key, default=None):
        raise NotImplementedError

    def remove(self, key):
        raise NotImplementedError

    def __contains__(self, key):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError


class ProbingSet:
    """A hash set with open addressing and linear probing, on a plain list of
    slots (no dict or set). A value's first slot is hash(x) % capacity, then
    (slot + 1) % capacity, and so on. discard() leaves a tombstone: lookups probe
    past it and inserts may reuse it. Start with capacity 8; before an insert that
    would fill an empty slot, rebuild into a table twice as big (dropping the
    tombstones) if live values + tombstones would exceed 2/3 of the capacity.

    add(x), discard(x) (no error if absent), x in s, len(s)
    """

    def __init__(self):
        raise NotImplementedError

    def add(self, x):
        raise NotImplementedError

    def discard(self, x):
        raise NotImplementedError

    def __contains__(self, x):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError


def is_heap(a):
    """Return True if the list a is a min-heap: a[(i - 1) // 2] <= a[i] for every
    i > 0. Empty and one-element lists are heaps."""
    raise NotImplementedError


def sift_up(a, i):
    """a is a min-heap except that a[i] may be smaller than its parent (it was
    just appended, say). Swap it upward with its parent (i - 1) // 2 while it's
    smaller. In place, O(log n)."""
    raise NotImplementedError


def sift_down(a, i, n):
    """a[:n] is a min-heap except that a[i] may be bigger than its children. Swap
    it with its smaller child (2i + 1 or 2i + 2, only indices below n) while that
    child is smaller. Leave a[n:] alone. In place, O(log n)."""
    raise NotImplementedError


def heapify(a):
    """Turn the list a into a min-heap in place in O(n): sift down every parent,
    from the last one (len(a) // 2 - 1) back to the root. Returns None."""
    raise NotImplementedError


class MinHeap:
    """A min-heap on a plain list, without heapq. push(x); pop() and peek()
    return the smallest item and raise IndexError when empty; len(h).
    O(log n) push and pop."""

    def __init__(self):
        raise NotImplementedError

    def push(self, x):
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError

    def peek(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError


def heap_sort(a):
    """Return a NEW ascending list of a's items using heapify and sift_down (no
    sorted(), no heapq); leave a unchanged. O(n log n)."""
    raise NotImplementedError


class DynamicArray:
    """A growable array on a fixed-size list of slots: self.slots always has
    length self.capacity. Start with capacity 1. When append finds the array full,
    allocate a list twice as long, copy the items over and add the number copied
    to self.copies. Never call append or pop on self.slots itself.

    append(x); pop() -> last item (IndexError when empty)
    a[i] and a[i] = x, negative indices allowed (IndexError when out of range)
    len(a), self.capacity, self.copies
    """

    def __init__(self):
        raise NotImplementedError

    def append(self, x):
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError

    def __getitem__(self, i):
        raise NotImplementedError

    def __setitem__(self, i, x):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError


class LazyHeap:
    """A min-heap (heapq is fine here) that can remove any value by lazy deletion:
    remove(x) only records that one copy of x is dead, and dead entries are thrown
    away when they reach the top. Values may repeat.

    push(x)
    remove(x) -> bool       False, changing nothing, if no live copy of x exists
    pop(), peek()           the smallest live value (IndexError when empty)
    len(h)                  the number of live values
    """

    def __init__(self):
        raise NotImplementedError

    def push(self, x):
        raise NotImplementedError

    def remove(self, x):
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError

    def peek(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError


# ---------------------------------------------------------------- tests (don't edit)

import heapq
import random


class _Collider:
    """Every instance hashes the same, so they all collide."""

    def __init__(self, v):
        self.v = v

    def __hash__(self):
        return 7

    def __eq__(self, other):
        return isinstance(other, _Collider) and self.v == other.v


class _Counted:
    """Counts every comparison made on it."""
    count = 0

    def __init__(self, v):
        self.v = v

    def __lt__(self, other):
        _Counted.count += 1
        return self.v < other.v

    def __le__(self, other):
        _Counted.count += 1
        return self.v <= other.v

    def __gt__(self, other):
        _Counted.count += 1
        return self.v > other.v

    def __ge__(self, other):
        _Counted.count += 1
        return self.v >= other.v


def _no_tables(obj):
    return not any(isinstance(v, (dict, set, frozenset)) for v in vars(obj).values())


def _heap_ok(a):
    return all(a[(i - 1) // 2] <= a[i] for i in range(1, len(a)))


def _raises(fn, exc=IndexError):
    try:
        fn()
    except exc:
        return True
    return False


def test_my_hash_map():
    m = MyHashMap()
    assert len(m) == 0 and m.capacity == 8
    assert m.get('x') is None and m.get('x', 5) == 5 and 'x' not in m
    assert _no_tables(m), "build it from lists: no dict or set inside"
    m.put('a', 1)
    m.put('a', 2)
    assert len(m) == 1 and m.get('a') == 2, "put on an existing key overwrites it"
    assert m.remove('a') is True and m.remove('a') is False and 'a' not in m and len(m) == 0
    m, cap = MyHashMap(), 8
    for i in range(100):
        m.put(i, i * i)
        if len(m) > 0.75 * cap:
            cap *= 2
        assert m.capacity == cap, f"after {i + 1} keys the capacity should be {cap}"
    assert all(m.get(i) == i * i for i in range(100)), "entries were lost while resizing"
    m = MyHashMap()
    for v in range(20):
        m.put(_Collider(v), v)
    assert len(m) == 20 and all(m.get(_Collider(v)) == v for v in range(20)), "colliding keys must share a bucket"
    assert m.remove(_Collider(5)) is True and _Collider(5) not in m and len(m) == 19
    rng = random.Random(19)
    m, model = MyHashMap(), {}
    for _ in range(3000):
        key = rng.choice([rng.randint(0, 50), str(rng.randint(0, 50)), (rng.randint(0, 3), 'x')])
        r = rng.random()
        if r < 0.5:
            value = rng.randint(0, 9)
            m.put(key, value)
            model[key] = value
        elif r < 0.75:
            assert m.remove(key) == (key in model), key
            model.pop(key, None)
        else:
            assert m.get(key, 'missing') == model.get(key, 'missing'), key
            assert (key in m) == (key in model), key
        assert len(m) == len(model)


def test_probing_set():
    s = ProbingSet()
    assert len(s) == 0 and 3 not in s
    assert _no_tables(s), "build it from a list of slots: no dict or set inside"
    s.add(3)
    s.add(3)
    assert len(s) == 1 and 3 in s, "adding a value that's already there changes nothing"
    s.discard(3)
    s.discard(3)
    assert len(s) == 0 and 3 not in s, "discarding a missing value is a no-op"
    s = ProbingSet()
    for x in (1, 9, 17):                     # all three start probing at slot 1 of 8
        s.add(x)
    s.discard(1)
    assert 9 in s and 17 in s, "lookups must probe past a tombstone, not stop at it"
    s.add(9)
    assert len(s) == 2, "an insert must check the rest of the probe run before reusing a tombstone"
    s.discard(9)
    s.add(25)
    s.add(17)
    assert [x for x in (1, 9, 17, 25) if x in s] == [17, 25] and len(s) == 2
    churn = ProbingSet()
    for x in range(2000):
        churn.add(x)
        churn.discard(x)
    assert len(churn) == 0 and -1 not in churn, "count tombstones toward the resize, or they fill the table"
    rng = random.Random(19)
    s, model = ProbingSet(), set()
    for _ in range(4000):
        x = rng.randint(0, 60)
        r = rng.random()
        if r < 0.45:
            s.add(x)
            model.add(x)
        elif r < 0.8:
            s.discard(x)
            model.discard(x)
        else:
            assert (x in s) == (x in model), x
        assert len(s) == len(model)


def test_is_heap():
    assert is_heap([]) is True and is_heap([5]) is True
    assert is_heap([1, 3, 2, 7, 4]) is True
    assert is_heap([1, 3, 2, 2, 4]) is False, "a[3] = 2 is smaller than its parent a[1] = 3"
    assert is_heap([2, 2, 2]) is True, "equal parent and child is fine"
    rng = random.Random(19)
    for _ in range(300):
        a = [rng.randint(0, 9) for _ in range(rng.randint(0, 10))]
        if rng.random() < 0.5:
            heapq.heapify(a)
        assert is_heap(a) == _heap_ok(a), a


def test_sift_up():
    rng = random.Random(19)
    for _ in range(300):
        a = [rng.randint(0, 50) for _ in range(rng.randint(0, 15))]
        heapq.heapify(a)
        a.append(rng.randint(-5, 55))
        want = sorted(a)
        sift_up(a, len(a) - 1)
        assert _heap_ok(a) and sorted(a) == want, a


def test_sift_down():
    rng = random.Random(19)
    for _ in range(300):
        a = [rng.randint(0, 50) for _ in range(rng.randint(1, 15))]
        heapq.heapify(a)
        a[0] = rng.randint(0, 60)
        tail = [rng.randint(-100, -50) for _ in range(rng.randint(0, 3))]
        a += tail                                  # junk past n must not be touched
        n = len(a) - len(tail)
        want = sorted(a[:n])
        sift_down(a, 0, n)
        assert _heap_ok(a[:n]) and sorted(a[:n]) == want, a
        assert a[n:] == tail, "only indices below n belong to the heap"


def test_heapify():
    rng = random.Random(19)
    for _ in range(300):
        a = [rng.randint(0, 9) for _ in range(rng.randint(0, 20))]
        b, want = a, sorted(a)
        assert heapify(a) is None and a is b
        assert _heap_ok(a) and sorted(a) == want, a
    for values in (range(1024, 0, -1), rng.sample(range(1024), 1024)):
        items = [_Counted(v) for v in values]
        _Counted.count = 0
        heapify(items)
        assert _heap_ok([x.v for x in items])
        assert _Counted.count <= 4 * 1024, f"{_Counted.count} comparisons for 1024 items: that's not O(n)"


def test_min_heap():
    h = MinHeap()
    assert len(h) == 0 and _raises(h.pop) and _raises(h.peek), "pop()/peek() on an empty heap should raise IndexError"
    rng = random.Random(19)
    model = []
    for _ in range(2000):
        if model and rng.random() < 0.4:
            if rng.random() < 0.3:
                assert h.peek() == model[0]
            else:
                assert h.pop() == heapq.heappop(model)
        else:
            x = rng.randint(0, 100)
            h.push(x)
            heapq.heappush(model, x)
        assert len(h) == len(model)


def test_heap_sort():
    rng = random.Random(19)
    for n in list(range(12)) + [500]:
        a = [rng.randint(-20, 20) for _ in range(n)]
        before = a[:]
        out = heap_sort(a)
        assert out == sorted(before), before
        assert a == before and (out is not a or n == 0), "return a new list and leave the input alone"


def test_dynamic_array():
    a = DynamicArray()
    assert len(a) == 0 and a.capacity == 1 and a.copies == 0
    assert _raises(a.pop) and _raises(lambda: a[0]), "pop()/indexing an empty array should raise IndexError"
    for i in range(1000):
        a.append(i)
        assert len(a.slots) == a.capacity, "self.slots must stay exactly capacity long (don't append to it)"
        assert a.capacity >= len(a) and a.capacity & (a.capacity - 1) == 0, "capacity should go 1, 2, 4, 8, ..."
    assert len(a) == 1000 and a.capacity == 1024
    assert a.copies == 1023, "1 + 2 + 4 + ... + 512 copies: fewer than 2n"
    assert a[0] == 0 and a[999] == 999 and a[-1] == 999 and a[-1000] == 0
    a[-1] = 'x'
    assert a[999] == 'x'
    assert _raises(lambda: a[1000]) and _raises(lambda: a[-1001]), "out-of-range indexes should raise IndexError"
    assert a.pop() == 'x' and len(a) == 999 and a[-1] == 998
    rng = random.Random(19)
    a, model = DynamicArray(), []
    for step in range(2000):
        r = rng.random()
        if model and r < 0.3:
            assert a.pop() == model.pop()
        elif model and r < 0.5:
            i = rng.randrange(-len(model), len(model))
            a[i] = step
            model[i] = step
        else:
            a.append(step)
            model.append(step)
        assert len(a) == len(model) and [a[i] for i in range(len(a))] == model


def test_lazy_heap():
    h = LazyHeap()
    assert len(h) == 0 and _raises(h.pop) and _raises(h.peek), "pop()/peek() on an empty heap should raise IndexError"
    assert h.remove(3) is False, "removing a value that isn't there returns False"
    h.push(5)
    h.push(5)
    h.push(1)
    assert h.remove(5) is True and len(h) == 2
    assert h.pop() == 1 and h.peek() == 5 and h.pop() == 5 and len(h) == 0
    assert h.remove(5) is False, "both copies of 5 are gone"
    rng = random.Random(19)
    h, model = LazyHeap(), []
    for _ in range(3000):
        r = rng.random()
        x = rng.randint(0, 12)
        if r < 0.45:
            h.push(x)
            model.append(x)
        elif r < 0.7:
            assert h.remove(x) == (x in model), x
            if x in model:
                model.remove(x)
        elif model:
            if r < 0.85:
                assert h.peek() == min(model)
            else:
                assert h.pop() == min(model)
                model.remove(min(model))
        assert len(h) == len(model)
