"""R30 - Complexity lab

Big-O describes growth; the clock describes your machine. Learn both. Know the
cost of every built-in you call, because the expensive ones hide inside loops:
x in list, pop(0), insert(0, x), slices, list(x), a == b, s + t. CPython runs
on the order of 10**7 simple loop iterations per second, so an O(n^2) loop is
fine at n = 10**3 and hopeless at n = 10**5. Passing xs[1:] into every
recursive call costs O(n^2) in total; pass an index instead. (CPython sometimes
optimizes s += t in place. Don't rely on it; PyPy doesn't.)

Part 1 - Predict. Each block in PREDICT is a REPL session. Replace every ???
with exactly what Python prints: expression values are echoed the way the REPL
echoes them, and a line that raises prints just the exception name (TypeError).

Part 2 - Quiz. Replace every ??? in QUIZ with the cost, written like O(1),
O(n), O(log n), O(n log n) or O(n^2).

Part 3 - Drills. Implement every function until `python check.py 30` is green.
The timed tests give the efficient approach a generous budget; the naive one
blows through it. Don't edit the tests at the bottom.

Unlocks: choosing data structures by cost, reading constraints, and spotting
the hidden O(n) that turns an O(n) plan into O(n^2).
"""
import random
import time
from bisect import bisect_left, bisect_right
from collections import Counter, deque
from heapq import heappop, heappush
from itertools import accumulate, combinations

PREDICT = r"""
>>> count = 0
>>> for i in range(100):
...     for j in range(i):
...         count += 1
>>> count
???

>>> n, steps = 10**6, 0
>>> while n > 1:
...     n //= 2
...     steps += 1
>>> steps
???

>>> (10**9).bit_length(), 2**30 > 10**9
???

>>> math.comb(10**5, 2)
???

>>> 2 ** 20, math.factorial(10), math.factorial(12)
???

>>> sum(1 for _ in permutations(range(8)))
???

>>> copied = 0
>>> def total(xs):
...     global copied
...     if not xs:
...         return 0
...     copied += len(xs) - 1
...     return xs[0] + total(xs[1:])
>>> total(list(range(100))), copied
???

>>> cap, size, copies = 1, 0, 0
>>> for _ in range(1000):
...     if size == cap:
...         copies += size
...         cap *= 2
...     size += 1
>>> cap, copies
???

>>> r = range(0, 10**12, 3)
>>> len(r), 999999999999 in r, r[-1]
???

>>> def insertion_sort_moves(a):
...     a, moves = a[:], 0
...     for i in range(1, len(a)):
...         j = i
...         while j and a[j - 1] > a[j]:
...             a[j - 1], a[j] = a[j], a[j - 1]
...             j -= 1
...             moves += 1
...     return moves
>>> insertion_sort_moves(list(range(100))), insertion_sort_moves(list(range(100, 0, -1)))
???

>>> next(x for x in itertools.count() if x * x > 50)
???

>>> calls = 0
>>> def size_of(xs):
...     global calls
...     calls += 1
...     return len(xs)
>>> xs = list(range(10))
>>> for i in range(size_of(xs)):
...     pass
>>> calls
???
>>> i = 0
>>> while i < size_of(xs):
...     i += 1
>>> calls
???

>>> class Probe:
...     seen = 0
...     def __eq__(self, other):
...         Probe.seen += 1
...         return False
>>> p = Probe()
>>> p in list(range(1000)), Probe.seen
???
>>> p in set(range(1000))
???
"""

QUIZ = {
    "list: a[i] or a[i] = x": "???",
    "list: a.append(x)": "???",
    "list: a.pop()": "???",
    "list: a.pop(0)": "???",
    "list: a.insert(0, x)": "???",
    "list: x in a": "???",
    "list: a.index(x), a.remove(x)": "???",
    "list: len(a)": "???",
    "list: min(a), max(a), sum(a)": "???",
    "list: a[i:j] (k = j - i)": "???",
    "list: a == b": "???",
    "list: a.sort() or sorted(a)": "???",
    "dict/set: d[k], k in d, d[k] = v, del d[k] (average)": "???",
    "dict/set: the same operations in the worst case": "???",
    "set: s & t": "???",
    "deque: append, appendleft, pop, popleft": "???",
    "deque: dq[i] for i in the middle": "???",
    "heapq: heappush, heappop": "???",
    "heapq: heapify(a)": "???",
    "heapq: h[0]": "???",
    "bisect: bisect_left(a, x)": "???",
    "bisect: insort(a, x)": "???",
    "str: s + t": "???",
    "str: ''.join(parts) (L = total length)": "???",
    "range: x in range(n) for an int x": "???",
    "recursion: f(xs) calls f(xs[1:]) until xs is empty": "???",
    "loops: for i in range(n): for j in range(i): ...": "???",
    "loops: while n > 1: n //= 2": "???",
}


# ---------------------------------------------------------------- drills

def loops_per_second():
    """Time a plain Python loop of at least 10**6 iterations (doing
    total += i) with time.perf_counter, and return iterations per second as a
    float. Expect something between 10**7 and 10**8 on a modern machine."""
    raise NotImplementedError


def pair_count(nums, target):
    """Count index pairs i < j with nums[i] + nums[j] == target.
    pair_count([1, 5, 7, -1, 5], 6) == 3. Timed at n = 16,000."""
    raise NotImplementedError


def shared_values(a, b):
    """Count the elements of b (repeats included) whose value appears anywhere
    in a. shared_values([1, 2, 3], [3, 3, 4]) == 2. Timed at
    len(a) == len(b) == 30,000."""
    raise NotImplementedError


def dedupe(items):
    """Return a new list without repeats, keeping each value's first
    occurrence in order. dedupe([3, 1, 3, 2, 1]) == [3, 1, 2].
    Timed at 40,000 items."""
    raise NotImplementedError


def round_robin(jobs):
    """jobs: (name, units) pairs with units >= 1, in queue order. Repeatedly
    take the job at the front, do one unit of it, and send it to the back if
    units remain. Return the names in the order the jobs finish. Don't modify
    the input list. round_robin([('a', 2), ('b', 1), ('c', 3)]) == ['b', 'a', 'c'].
    Timed at 200,000 jobs."""
    raise NotImplementedError


def range_sums(nums, queries):
    """queries: (l, r) index pairs with 0 <= l <= r < len(nums). Return
    sum(nums[l..r]) (inclusive) for each query, in order.
    range_sums([1, 2, 3, 4], [(0, 1), (1, 3)]) == [3, 9].
    Timed at len(nums) == 100,000 with 20,000 queries."""
    raise NotImplementedError


def count_between(sorted_nums, queries):
    """sorted_nums is sorted ascending; queries are (lo, hi) value pairs. For
    each query, return how many x in sorted_nums satisfy lo <= x <= hi.
    count_between([1, 3, 3, 7], [(2, 3), (4, 6)]) == [2, 0].
    Timed at 100,000 numbers with 4,000 queries."""
    raise NotImplementedError


def kth_largest_so_far(nums, k):
    """Return a list whose entry i is the k-th largest value among
    nums[:i + 1], or None while fewer than k values have been seen.
    kth_largest_so_far([5, 1, 9, 3], 2) == [None, 1, 5, 5].
    Timed at n = 10,000 with k = 10."""
    raise NotImplementedError


def apply_range_adds(n, updates):
    """Start from [0] * n. Each update (l, r, delta) adds delta to every index
    l..r inclusive. Return the final list.
    apply_range_adds(5, [(1, 3, 2), (0, 1, -1)]) == [-1, 1, 2, 2, 0].
    Timed at n = 20,000 with 40,000 updates."""
    raise NotImplementedError


# ---------------------------------------------------------------- tests (don't edit)

_BUDGET = 0.5   # seconds; the efficient versions take a few milliseconds


def _timed(fn, *args):
    start = time.perf_counter()
    result = fn(*args)
    return result, time.perf_counter() - start


def _assert_fast(secs, hint):
    assert secs < _BUDGET, f"{secs:.2f}s against a {_BUDGET}s budget: {hint}"


def _random_ranges(rng, n, count):
    out = []
    for _ in range(count):
        lo = rng.randrange(n)
        out.append((lo, rng.randrange(lo, n)))
    return out


def test_loops_per_second():
    start = time.perf_counter()
    rate = loops_per_second()
    secs = time.perf_counter() - start
    assert isinstance(rate, (int, float)), "return a number"
    assert 1e6 <= rate <= 1e10, f"{rate:.3g} loops/s doesn't look right: time at least 10**6 iterations"
    assert secs < 2, "keep the measurement short (one loop of about 10**6 iterations)"


def test_pair_count():
    assert pair_count([1, 5, 7, -1, 5], 6) == 3
    assert pair_count([1, 1, 1, 1], 2) == 6
    assert pair_count([3], 6) == 0, "a pair needs two different indices"
    assert pair_count([], 0) == 0
    rng = random.Random(30)
    for _ in range(100):
        nums = [rng.randint(-5, 5) for _ in range(rng.randint(0, 12))]
        t = rng.randint(-6, 6)
        want = sum(a + b == t for a, b in combinations(nums, 2))
        assert pair_count(nums, t) == want, (nums, t)
    big = rng.choices(range(10 ** 6), k=16_000)
    _, secs = _timed(pair_count, big, 10 ** 6)
    _assert_fast(secs, "a double loop is O(n^2); count complements with a Counter in one pass")


def test_shared_values():
    assert shared_values([1, 2, 3], [3, 3, 4]) == 2
    assert shared_values([], [1, 2]) == 0
    assert shared_values([5, 5], []) == 0
    rng = random.Random(30)
    for _ in range(100):
        a = [rng.randint(0, 9) for _ in range(rng.randint(0, 8))]
        b = [rng.randint(0, 9) for _ in range(rng.randint(0, 8))]
        want = sum(x in a for x in b)
        assert shared_values(a, b) == want, (a, b)
    a = rng.choices(range(10 ** 9), k=30_000)
    b = rng.choices(range(10 ** 9), k=30_000)
    _, secs = _timed(shared_values, a, b)
    _assert_fast(secs, "`x in list` scans the whole list; build a set once")


def test_dedupe():
    assert dedupe([3, 1, 3, 2, 1]) == [3, 1, 2]
    assert dedupe([]) == []
    assert dedupe(['b', 'a', 'b']) == ['b', 'a']
    data = [2, 2, 1]
    dedupe(data)
    assert data == [2, 2, 1], "return a new list; leave the input alone"
    rng = random.Random(30)
    for _ in range(100):
        items = [rng.randint(0, 6) for _ in range(rng.randint(0, 10))]
        want = [x for i, x in enumerate(items) if x not in items[:i]]
        assert dedupe(items) == want, items
    big = rng.sample(range(10 ** 9), 40_000)
    _, secs = _timed(dedupe, big)
    _assert_fast(secs, "`x not in out` scans the output list; remember seen values in a set (or use dict.fromkeys)")


def test_round_robin():
    assert round_robin([('a', 2), ('b', 1), ('c', 3)]) == ['b', 'a', 'c']
    assert round_robin([]) == []
    assert round_robin([('x', 1)]) == ['x']
    rng = random.Random(30)
    for _ in range(100):
        jobs = [(i, rng.randint(1, 4)) for i in range(rng.randint(0, 8))]
        want = [name for _, _, name in sorted((u, i, name) for i, (name, u) in enumerate(jobs))]
        given = list(jobs)
        assert round_robin(given) == want, jobs
        assert given == jobs, "don't modify the input list"
    jobs = list(zip(range(200_000), rng.choices((1, 2, 3), k=200_000)))
    _, secs = _timed(round_robin, jobs)
    _assert_fast(secs, "list.pop(0) shifts every remaining element; use collections.deque")


def test_range_sums():
    assert range_sums([1, 2, 3, 4], [(0, 1), (1, 3)]) == [3, 9]
    assert range_sums([5], [(0, 0), (0, 0)]) == [5, 5]
    assert range_sums([1, 2], []) == []
    rng = random.Random(30)
    for _ in range(100):
        nums = [rng.randint(-9, 9) for _ in range(rng.randint(1, 10))]
        qs = _random_ranges(rng, len(nums), rng.randint(0, 5))
        want = [sum(nums[l:r + 1]) for l, r in qs]
        assert range_sums(nums, qs) == want, (nums, qs)
    nums = rng.choices(range(-1000, 1000), k=100_000)
    qs = _random_ranges(rng, len(nums), 20_000)
    _, secs = _timed(range_sums, nums, qs)
    _assert_fast(secs, "sum(nums[l:r + 1]) costs O(r - l) per query; build prefix sums once")


def test_count_between():
    assert count_between([1, 3, 3, 7], [(2, 3), (4, 6)]) == [2, 0]
    assert count_between([], [(0, 5)]) == [0]
    assert count_between([2, 2, 2], [(2, 2), (3, 1)]) == [3, 0], "an empty range (lo > hi) counts nothing"
    rng = random.Random(30)
    for _ in range(100):
        nums = sorted(rng.randint(0, 9) for _ in range(rng.randint(0, 10)))
        qs = [(rng.randint(-1, 10), rng.randint(-1, 10)) for _ in range(4)]
        want = [sum(lo <= x <= hi for x in nums) for lo, hi in qs]
        assert count_between(nums, qs) == want, (nums, qs)
    nums = sorted(rng.choices(range(10 ** 6), k=100_000))
    qs = []
    for _ in range(4_000):
        lo = rng.randrange(10 ** 6)
        qs.append((lo, lo + rng.randrange(10 ** 5)))
    _, secs = _timed(count_between, nums, qs)
    _assert_fast(secs, "scanning is O(n) per query; the list is sorted, so use bisect")


def test_kth_largest_so_far():
    assert kth_largest_so_far([5, 1, 9, 3], 2) == [None, 1, 5, 5]
    assert kth_largest_so_far([4, 4, 4], 1) == [4, 4, 4]
    assert kth_largest_so_far([], 3) == []
    assert kth_largest_so_far([7, 2], 3) == [None, None]
    rng = random.Random(30)
    for _ in range(100):
        nums = [rng.randint(0, 9) for _ in range(rng.randint(0, 10))]
        k = rng.randint(1, 4)
        want = [sorted(nums[:i + 1])[-k] if i + 1 >= k else None for i in range(len(nums))]
        assert kth_largest_so_far(nums, k) == want, (nums, k)
    big = rng.choices(range(10 ** 6), k=10_000)
    _, secs = _timed(kth_largest_so_far, big, 10)
    _assert_fast(secs, "re-sorting every prefix is O(n^2 log n); keep a min-heap of the k largest")


def test_apply_range_adds():
    assert apply_range_adds(5, [(1, 3, 2), (0, 1, -1)]) == [-1, 1, 2, 2, 0]
    assert apply_range_adds(3, []) == [0, 0, 0]
    assert apply_range_adds(1, [(0, 0, 5), (0, 0, 5)]) == [10]
    assert apply_range_adds(4, [(0, 3, 1)]) == [1, 1, 1, 1], "a range that ends at the last index"
    rng = random.Random(30)
    for _ in range(100):
        n = rng.randint(1, 10)
        ups = [(lo, hi, rng.randint(-3, 3)) for lo, hi in _random_ranges(rng, n, rng.randint(0, 6))]
        want = [sum(d for lo, hi, d in ups if lo <= i <= hi) for i in range(n)]
        assert apply_range_adds(n, ups) == want, (n, ups)
    n = 20_000
    ups = [(lo, hi, rng.randint(-5, 5)) for lo, hi in _random_ranges(rng, n, 40_000)]
    _, secs = _timed(apply_range_adds, n, ups)
    _assert_fast(secs, "touching every index of every range is O(n * updates); use a difference array")
