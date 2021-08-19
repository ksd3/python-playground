"""R08 - deque, heapq, bisect

deque: O(1) append/pop at both ends, O(n) indexing in the middle, no slicing;
maxlen=k silently drops items from the opposite end; extendleft reverses its input.
heapq keeps a min-heap in a plain list: h[0] is the smallest, the rest isn't
sorted, heapify is O(n). Max-heap = push negated values (heappush_max and friends
only arrived in 3.14). Entries compare like tuples, so push (priority, counter,
item) when items can't be compared. bisect_left(a, x) is the first index with
a[i] >= x, bisect_right the first with a[i] > x; insort is O(n); key= (3.10+) is
applied to the list's elements, not to x.

Part 1 - Predict. Each block in PREDICT is a REPL session. Replace every ???
with exactly what Python prints: expression values are echoed the way the REPL
echoes them, and a line that raises prints just the exception name (TypeError).

Part 2 - Drills. Implement every function until `python check.py 8` is green.
Don't edit the tests at the bottom; add your own test_* functions if you like.

Unlocks: BFS, sliding-window max, top-k / k-closest / merge-k problems,
scheduling, running median, Dijkstra, LIS in O(n log n), and binary search on
the answer.
"""
import heapq
from bisect import bisect_left, bisect_right, insort
from collections import Counter, deque
from heapq import heapify, heappop, heappush, heappushpop, heapreplace

PREDICT = r"""
>>> dq = deque([1])
>>> dq.extendleft([2, 3])
>>> dq
???

>>> dq = deque([1, 2, 3])
>>> dq[0:2]
???
>>> dq[1], dq[-1], 2 in dq
???

>>> dq = deque(maxlen=3)
>>> dq.extend(range(5))
>>> dq
???
>>> dq.appendleft(9)
>>> dq
???

>>> dq = deque([1, 2, 3, 4])
>>> dq.rotate(1)
>>> dq
???
>>> dq.rotate(-2)
>>> dq
???

>>> dq = deque([1, 2, 3])
>>> dq.popleft(), dq.pop(), dq
???
>>> dq.clear()
>>> dq.pop()
???

>>> h = [5, 1, 4, 2, 3]
>>> heapify(h)
>>> h, h[0]
???

>>> h = []
>>> for x in [3, 1, 2]:
...     heappush(h, -x)
>>> -h[0], [-heappop(h) for _ in range(3)]
???

>>> class Node:
...     pass
>>> h = []
>>> heappush(h, (1, Node()))
>>> heappush(h, (1, Node()))
???
>>> len(h)
???

>>> h = [(2, 'b'), (1, 'z'), (1, 'a')]
>>> heapify(h)
>>> heappop(h)
???

>>> h = [1, 5, 9]
>>> heappushpop(h, 0), h
???
>>> heapreplace(h, 0), h
???

>>> nlargest(2, [5, 1, 4, 3]), nsmallest(2, 'hello')
???
>>> nlargest(2, ['bb', 'a', 'ccc'], key=len)
???

>>> list(heapq.merge([1, 4, 7], [2, 3, 9]))
???

>>> heappop([])
???

>>> a = [1, 2, 2, 2, 5]
>>> bisect_left(a, 2), bisect_right(a, 2), bisect_left(a, 3), bisect_right(a, 0)
???
>>> bisect_right(a, 2) - bisect_left(a, 2)
???

>>> a = [1, 3, 5]
>>> insort(a, 4)
>>> insort(a, 0)
>>> a
???

>>> a = [10, 20, 30]
>>> i = bisect_right(a, 25) - 1
>>> i, a[i]
???
>>> bisect_right(a, 5) - 1
???

>>> bisect_left(range(100), True, key=lambda x: x * x >= 50)
???

>>> a = [(1, 'a'), (3, 'c')]
>>> bisect_left(a, (3,)), bisect_left(a, 3, key=lambda p: p[0])
???
"""


# ---------------------------------------------------------------- drills

def moving_average(nums, k):
    """After each new value, the average of the last k values (fewer while the
    window fills), using deque(maxlen=k) and a running sum.
    moving_average([1, 2, 3, 4], 2) == [1.0, 1.5, 2.5, 3.5]"""
    raise NotImplementedError


def josephus(n, k):
    """People 1..n stand in a circle; counting starts at person 1 and every
    k-th person leaves. Return the order they leave in, using deque.rotate.
    josephus(5, 2) == [2, 4, 1, 5, 3]"""
    raise NotImplementedError


def heapsort(items):
    """Return the items in ascending order with heapify plus repeated heappop.
    Don't modify the input. heapsort([3, 1, 2]) == [1, 2, 3]"""
    raise NotImplementedError


def k_largest(nums, k):
    """The k largest values, largest first, keeping a min-heap of at most k
    items (O(n log k)); k can be 0 or exceed len(nums).
    k_largest([3, 1, 5, 2], 2) == [5, 3]"""
    raise NotImplementedError


def merge_sorted(lists):
    """Merge sorted lists into one sorted list using a heap of (value,
    list index, position) entries; no heapq.merge, no sorting.
    merge_sorted([[1, 4], [2, 3], []]) == [1, 2, 3, 4]"""
    raise NotImplementedError


def process_in_priority(tasks):
    """tasks is a list of (priority, payload) pairs whose payloads are dicts,
    which can't be compared with <. Using a heap, return the payloads by
    priority (lowest first), equal priorities in input order."""
    raise NotImplementedError


def lazy_min(ops):
    """Run ('push', x), ('remove', x) and ('min',) operations on a multiset and
    return the answer to every ('min',), None when empty. A remove always names
    a value that's present. Use one heap plus a Counter of pending removals and
    discard stale entries only when they reach the top."""
    raise NotImplementedError


def lower_bound(a, x):
    """By hand with a while loop (no bisect): the first index i with
    a[i] >= x in sorted list a, or len(a) if there is none."""
    raise NotImplementedError


def upper_bound(a, x):
    """By hand with a while loop (no bisect): the first index i with
    a[i] > x in sorted list a, or len(a) if there is none."""
    raise NotImplementedError


def count_in_range(a, lo, hi):
    """How many values v in sorted list a satisfy lo <= v <= hi, in O(log n)
    (0 when lo > hi). count_in_range([1, 2, 2, 5, 7], 2, 5) == 3"""
    raise NotImplementedError


def floor_ceiling(a, x):
    """(largest value <= x, smallest value >= x) in sorted list a, with None for
    a side that doesn't exist. floor_ceiling([10, 20, 30], 25) == (20, 30)"""
    raise NotImplementedError


def nearest(a, x):
    """The value in non-empty sorted list a closest to x; on a tie, the
    smaller one. nearest([1, 4, 6], 5) == 4"""
    raise NotImplementedError


def count_less_before(nums):
    """For each position, how many earlier values are strictly smaller, using
    bisect on a sorted list that you insort into.
    count_less_before([3, 1, 2, 5]) == [0, 0, 1, 3]"""
    raise NotImplementedError


# ---------------------------------------------------------------- tests (don't edit)
import bisect as _bisect
import math as _math
import random as _random


def _brute_josephus(n, k):
    people, out, i = list(range(1, n + 1)), [], 0
    while people:
        i = (i + k - 1) % len(people)
        out.append(people.pop(i))
    return out


def _brute_lazy(ops):
    bag, out = [], []
    for op in ops:
        if op[0] == 'push':
            bag.append(op[1])
        elif op[0] == 'remove':
            bag.remove(op[1])
        else:
            out.append(min(bag) if bag else None)
    return out


def _sorted_list(rng, n=8, hi=9):
    return sorted(rng.randint(0, hi) for _ in range(rng.randint(0, n)))


def test_moving_average():
    assert moving_average([1, 2, 3, 4], 2) == [1.0, 1.5, 2.5, 3.5]
    assert moving_average([], 3) == []
    assert moving_average([5, 5, 5], 1) == [5.0, 5.0, 5.0]
    rng = _random.Random(8)
    for _ in range(100):
        nums = [rng.randint(-9, 9) for _ in range(rng.randint(0, 10))]
        k = rng.randint(1, 4)
        expected = [sum(nums[max(0, i - k + 1):i + 1]) / min(k, i + 1) for i in range(len(nums))]
        got = moving_average(nums, k)
        assert len(got) == len(expected), "one average per value"
        assert all(_math.isclose(g, e, abs_tol=1e-9) for g, e in zip(got, expected)), (nums, k)


def test_josephus():
    assert josephus(5, 2) == [2, 4, 1, 5, 3]
    assert josephus(1, 3) == [1]
    assert josephus(4, 1) == [1, 2, 3, 4]
    for n in range(1, 9):
        for k in range(1, 7):
            assert josephus(n, k) == _brute_josephus(n, k), (n, k)


def test_heapsort():
    items = [3, 1, 2]
    assert heapsort(items) == [1, 2, 3]
    assert items == [3, 1, 2], "heapify a copy, not the caller's list"
    assert heapsort([]) == []
    rng = _random.Random(8)
    for _ in range(100):
        xs = [rng.randint(-50, 50) for _ in range(rng.randint(0, 20))]
        assert heapsort(xs) == sorted(xs)


def test_k_largest():
    assert k_largest([3, 1, 5, 2], 2) == [5, 3]
    assert k_largest([1, 2], 5) == [2, 1]
    assert k_largest([1, 2], 0) == [], "k = 0: don't touch h[0] on an empty heap"
    assert k_largest([4, 4, 1], 2) == [4, 4]
    rng = _random.Random(8)
    for _ in range(200):
        xs = [rng.randint(-9, 9) for _ in range(rng.randint(0, 12))]
        k = rng.randint(0, 6)
        assert k_largest(xs, k) == sorted(xs, reverse=True)[:k], (xs, k)


def test_merge_sorted():
    assert merge_sorted([[1, 4], [2, 3], []]) == [1, 2, 3, 4]
    assert merge_sorted([]) == []
    assert merge_sorted([[], []]) == []
    assert merge_sorted([[1, 1], [1]]) == [1, 1, 1]
    rng = _random.Random(8)
    for _ in range(200):
        lists = [_sorted_list(rng, 5) for _ in range(rng.randint(0, 4))]
        assert merge_sorted(lists) == sorted(x for lst in lists for x in lst), lists


def test_process_in_priority():
    tasks = [(2, {'id': 'a'}), (1, {'id': 'b'}), (2, {'id': 'c'}), (1, {'id': 'd'})]
    got = process_in_priority(tasks)
    assert [p['id'] for p in got] == ['b', 'd', 'a', 'c'], "equal priorities keep input order"
    assert got[0] is tasks[1][1], "return the payload objects themselves"
    assert process_in_priority([]) == []


def test_lazy_min():
    ops = [('push', 5), ('push', 3), ('min',), ('remove', 3), ('min',), ('push', 3),
           ('push', 3), ('remove', 3), ('min',), ('remove', 3), ('remove', 5), ('min',)]
    assert lazy_min(ops) == [3, 5, 3, None]
    assert lazy_min([('min',)]) == [None]
    rng = _random.Random(8)
    for _ in range(100):
        ops, bag = [], []
        for _ in range(rng.randint(0, 25)):
            r = rng.random()
            if r < 0.45:
                x = rng.randint(0, 6)
                ops.append(('push', x))
                bag.append(x)
            elif r < 0.7 and bag:
                x = rng.choice(bag)
                ops.append(('remove', x))
                bag.remove(x)
            else:
                ops.append(('min',))
        assert lazy_min(ops) == _brute_lazy(ops), ops


def test_lower_bound():
    assert lower_bound([], 5) == 0
    assert lower_bound([1, 2, 2, 3], 2) == 1
    assert lower_bound([1, 2, 2, 3], 9) == 4
    rng = _random.Random(8)
    for _ in range(500):
        a, x = _sorted_list(rng), rng.randint(-1, 10)
        assert lower_bound(a, x) == _bisect.bisect_left(a, x), (a, x)


def test_upper_bound():
    assert upper_bound([], 5) == 0
    assert upper_bound([1, 2, 2, 3], 2) == 3
    assert upper_bound([1, 2, 2, 3], 0) == 0
    rng = _random.Random(8)
    for _ in range(500):
        a, x = _sorted_list(rng), rng.randint(-1, 10)
        assert upper_bound(a, x) == _bisect.bisect_right(a, x), (a, x)


def test_count_in_range():
    assert count_in_range([1, 2, 2, 5, 7], 2, 5) == 3
    assert count_in_range([1, 2, 3], 5, 9) == 0
    assert count_in_range([], 0, 1) == 0
    assert count_in_range([4, 4, 4], 4, 4) == 3, "both ends are included"
    rng = _random.Random(8)
    for _ in range(300):
        a = _sorted_list(rng)
        lo, hi = rng.randint(-1, 10), rng.randint(-1, 10)
        assert count_in_range(a, lo, hi) == sum(lo <= v <= hi for v in a), (a, lo, hi)


def test_floor_ceiling():
    assert floor_ceiling([10, 20, 30], 25) == (20, 30)
    assert floor_ceiling([10, 20, 30], 20) == (20, 20)
    assert floor_ceiling([10, 20, 30], 5) == (None, 10), "index -1 means no floor, not a[-1]"
    assert floor_ceiling([10, 20, 30], 35) == (30, None)
    assert floor_ceiling([], 1) == (None, None)
    rng = _random.Random(8)
    for _ in range(300):
        a, x = _sorted_list(rng), rng.randint(-1, 10)
        expected = (max((v for v in a if v <= x), default=None),
                    min((v for v in a if v >= x), default=None))
        assert floor_ceiling(a, x) == expected, (a, x)


def test_nearest():
    assert nearest([1, 4, 6], 5) == 4, "on a tie, the smaller value"
    assert nearest([1, 4, 6], 7) == 6
    assert nearest([1, 4, 6], -3) == 1
    assert nearest([2], 100) == 2
    rng = _random.Random(8)
    for _ in range(300):
        a = sorted(rng.randint(0, 20) for _ in range(rng.randint(1, 8)))
        x = rng.randint(-2, 22)
        assert nearest(a, x) == min(a, key=lambda v: (abs(v - x), v)), (a, x)


def test_count_less_before():
    assert count_less_before([3, 1, 2, 5]) == [0, 0, 1, 3]
    assert count_less_before([2, 2, 2]) == [0, 0, 0], "strictly smaller: bisect_left, not bisect_right"
    assert count_less_before([]) == []
    rng = _random.Random(8)
    for _ in range(200):
        nums = [rng.randint(0, 5) for _ in range(rng.randint(0, 10))]
        expected = [sum(y < x for y in nums[:i]) for i, x in enumerate(nums)]
        assert count_less_before(nums) == expected, nums
