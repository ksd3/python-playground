"""R26 - Binary search

One template covers almost everything: find the smallest x in [lo, hi] where a
monotone predicate flips from False to True. The mirror ("last True") must round
mid UP, or `lo = mid` loops forever once hi == lo + 1. bisect_left(a, x) is the
first index with a[i] >= x; bisect_right(a, x) is the first with a[i] > x. Search
on the answer: when "can it be done with capacity c?" is monotone in c, binary
search c. Variants: rotated arrays, peaks (search the slope), real numbers (fixed
iteration count), a 2D matrix read as one flattened index. bisect's key= needs
Python 3.10+ and is applied to the elements, never to x.

Part 1 - Predict. Each block in PREDICT is a REPL session. Replace every ???
with exactly what Python prints: expression values are echoed the way the REPL
echoes them, and a line that raises prints just the exception name (TypeError).

Part 2 - Drills. Implement every function until `python check.py 26` is green.
Don't edit the tests at the bottom; add your own test_* functions if you like.
The O(log n) drills get a read-only sequence that counts element reads: use only
len(a) and a[i] on it.

Unlocks: sorted/rotated lookups, counting in ranges, floor/ceiling queries,
"minimize the maximum" and "smallest rate that works" style problems.
"""

PREDICT = r"""
>>> a = [1, 2, 2, 2, 5]
>>> bisect_left(a, 2), bisect_right(a, 2)
???
>>> bisect_left(a, 3), bisect_right(a, 3)
???
>>> bisect_left(a, 0), bisect_left(a, 9)
???

>>> a = [1, 2, 2, 2, 5]
>>> bisect_right(a, 2) - bisect_left(a, 2)
???

>>> a = [10, 20, 30]
>>> i = bisect_right(a, 25) - 1
>>> i, a[i]
???
>>> j = bisect_right(a, 5) - 1
>>> j, a[j]
???

>>> a = [10, 20, 30]
>>> a[bisect_left(a, 25)]
???
>>> a[bisect_left(a, 35)]
???

>>> a = [1, 3, 5]
>>> insort(a, 4)
>>> a
???

>>> bisect_left([1, 2, 3, 4, 5], 1, lo=2)
???

>>> bisect_left([5, 1, 4], 5)
???

>>> people = [('ann', 25), ('bob', 31), ('cy', 40)]
>>> bisect_left(people, 31, key=lambda p: p[1])
???
>>> bisect_left(people, ('x', 31), key=lambda p: p[1])
???

>>> bisect_left(range(100), True, key=lambda x: x * x >= 50)
???

>>> lo, hi = 4, 5
>>> (lo + hi) // 2, (lo + hi + 1) // 2
???

>>> lo, hi = -3, -2
>>> (lo + hi) // 2, int((lo + hi) / 2)
???

>>> bisect_left(['apple', 'banana', 'cherry'], 'b')
???

>>> lo, hi = 0.0, 2.0
>>> for _ in range(100):
...     mid = (lo + hi) / 2
...     if mid * mid < 2:
...         lo = mid
...     else:
...         hi = mid
>>> round(lo, 6)
???

>>> rows, cols = 3, 4
>>> divmod(7, cols)
???
"""

from bisect import bisect_left, bisect_right


# ---------------------------------------------------------------- drills

def lower_bound(a, x):
    """First index i with a[i] >= x in sorted a (len(a) if there is none).
    Write the loop yourself. O(log n). lower_bound([1, 2, 2, 5], 2) == 1."""
    raise NotImplementedError


def upper_bound(a, x):
    """First index i with a[i] > x in sorted a (len(a) if there is none).
    Write the loop yourself. O(log n). upper_bound([1, 2, 2, 5], 2) == 3."""
    raise NotImplementedError


def count_in_range(a, lo, hi):
    """How many values v in sorted a satisfy lo <= v <= hi (lo <= hi). O(log n).
    count_in_range([1, 3, 3, 5, 8], 3, 5) == 3."""
    raise NotImplementedError


def first_true(lo, hi, ok):
    """ok is monotone on [lo, hi]: False...False True...True. Return the
    smallest x in [lo, hi] with ok(x) True; if nothing below hi is True, return
    hi (without needing to call ok(hi)). Call ok O(log(hi - lo)) times.
    first_true(0, 100, lambda x: x * x >= 50) == 8."""
    raise NotImplementedError


def last_true(lo, hi, ok):
    """ok is monotone on [lo, hi]: True...True False...False. Return the
    largest x in [lo, hi] with ok(x) True; if nothing above lo is True, return
    lo. Call ok O(log(hi - lo)) times. last_true(0, 100, lambda x: x * x <= 50) == 7."""
    raise NotImplementedError


def search_rotated(a, target):
    """a is a sorted list of distinct values rotated by some k (e.g.
    [4, 5, 6, 7, 0, 1, 2]). Return the index of target, or -1. O(log n).
    search_rotated([4, 5, 6, 7, 0, 1, 2], 0) == 4."""
    raise NotImplementedError


def rotation_min(a):
    """The minimum of a non-empty rotated sorted list of distinct values.
    O(log n). rotation_min([4, 5, 6, 7, 0, 1, 2]) == 0."""
    raise NotImplementedError


def peak_index(a):
    """a is non-empty and no two neighbors are equal. Return an index i with
    a[i] greater than both neighbors (outside the list counts as -infinity).
    Any peak will do. O(log n). peak_index([1, 3, 2]) == 1."""
    raise NotImplementedError


def min_largest_group_sum(nums, k):
    """Split nums (non-negative, non-empty), in order, into at most k contiguous
    groups (1 <= k <= len(nums)). Return the smallest possible largest group sum.
    Binary search the answer. min_largest_group_sum([7, 2, 5, 10, 8], 2) == 18."""
    raise NotImplementedError


def min_speed(piles, hours):
    """Working through each pile p at speed s takes ceil(p / s) hours, one pile
    at a time. Return the smallest integer s >= 1 that finishes all piles
    (positive ints) within hours (hours >= len(piles)). Binary search the
    answer. min_speed([3, 6, 7, 11], 8) == 4."""
    raise NotImplementedError


def int_sqrt(n):
    """floor(sqrt(n)) for any int n >= 0, exact even for huge n: binary search
    on integers, no floats. int_sqrt(99) == 9; int_sqrt(10**30) == 10**15."""
    raise NotImplementedError


def bisect_root(f, lo, hi):
    """f is continuous and increasing on [lo, hi] with f(lo) < 0 <= f(hi).
    Return x with f(x) == 0 to within 1e-9, by bisecting a fixed number of
    times. bisect_root(lambda x: x * x - 2, 0, 2) is about 1.41421356."""
    raise NotImplementedError


def matrix_contains(matrix, target):
    """Every row of matrix is sorted and each row starts above the previous
    row's last value. Return True if target is present, else False, in
    O(log(rows * cols)) by treating the matrix as one flattened sorted list."""
    raise NotImplementedError


# ---------------------------------------------------------------- tests (don't edit)

import itertools as _itertools
import math as _math
import random as _random
from bisect import bisect_left as _bl, bisect_right as _br


class _Probe:
    """A read-only sequence that counts element reads."""

    def __init__(self, data):
        self._data = list(data)
        self.reads = 0

    def __len__(self):
        return len(self._data)

    def __getitem__(self, i):
        if isinstance(i, slice):
            part = self._data[i]
            self.reads += len(part)
            return part
        self.reads += 1
        return self._data[i]


class _Counted:
    """Wraps a predicate and fails fast instead of looping forever."""

    def __init__(self, fn, limit=200):
        self.fn, self.calls, self.limit = fn, 0, limit

    def __call__(self, x):
        self.calls += 1
        assert self.calls <= self.limit, "predicate called 200+ times: infinite loop? (with lo = mid, round mid up)"
        return self.fn(x)


def _sorted_list(rng):
    return sorted(rng.randint(0, 9) for _ in range(rng.randint(0, 10)))


def _rotations(n):
    base = list(range(0, 2 * n, 2))
    return [base[k:] + base[:k] for k in range(n)]


def test_lower_bound():
    assert lower_bound([1, 2, 2, 2, 5], 2) == 1
    assert lower_bound([1, 2, 2, 2, 5], 3) == 4
    assert lower_bound([1, 2, 2, 2, 5], 9) == 5
    assert lower_bound([], 1) == 0
    rng = _random.Random(26)
    for _ in range(300):
        a, x = _sorted_list(rng), rng.randint(-1, 10)
        assert lower_bound(a, x) == _bl(a, x), (a, x)
    probe = _Probe(range(0, 2 * 65536, 2))
    assert lower_bound(probe, 12345) == 6173
    assert probe.reads <= 40, f"{probe.reads} reads for 65536 items: that's not O(log n)"


def test_upper_bound():
    assert upper_bound([1, 2, 2, 2, 5], 2) == 4
    assert upper_bound([1, 2, 2, 2, 5], 0) == 0
    assert upper_bound([1, 2, 2, 2, 5], 5) == 5
    assert upper_bound([], 1) == 0
    rng = _random.Random(26)
    for _ in range(300):
        a, x = _sorted_list(rng), rng.randint(-1, 10)
        assert upper_bound(a, x) == _br(a, x), (a, x)
    probe = _Probe(range(65536))
    assert upper_bound(probe, 40000) == 40001
    assert probe.reads <= 40, f"{probe.reads} reads for 65536 items: that's not O(log n)"


def test_count_in_range():
    assert count_in_range([1, 3, 3, 5, 8], 3, 5) == 3
    assert count_in_range([1, 3, 3, 5, 8], 4, 4) == 0
    assert count_in_range([1, 3, 3, 5, 8], 0, 100) == 5
    assert count_in_range([], 0, 1) == 0
    rng = _random.Random(26)
    for _ in range(300):
        a = _sorted_list(rng)
        lo = rng.randint(-1, 10)
        hi = rng.randint(lo, 11)
        assert count_in_range(a, lo, hi) == sum(lo <= v <= hi for v in a), (a, lo, hi)
    probe = _Probe(sorted(i // 3 for i in range(65536)))
    assert count_in_range(probe, 100, 199) == 300
    assert probe.reads <= 80, f"{probe.reads} reads for 65536 items: that's not O(log n)"


def test_first_true():
    for t in range(21):
        assert first_true(0, 20, _Counted(lambda x, t=t: x >= t)) == t, t
    ok = _Counted(lambda x: x >= 10**6 - 3)
    assert first_true(0, 10**6, ok) == 10**6 - 3
    assert ok.calls <= 25, f"{ok.calls} predicate calls: should be about log2 of the range"
    assert first_true(5, 5, _Counted(lambda x: True)) == 5
    assert first_true(0, 7, _Counted(lambda x: False)) == 7, "nothing below hi is True: return hi"
    assert first_true(-50, 50, _Counted(lambda x: x >= -17)) == -17


def test_last_true():
    for t in range(21):
        assert last_true(0, 20, _Counted(lambda x, t=t: x <= t)) == t, t
    assert last_true(4, 5, _Counted(lambda x: x <= 4)) == 4
    assert last_true(4, 5, _Counted(lambda x: x <= 5)) == 5
    ok = _Counted(lambda x: x <= 777)
    assert last_true(0, 10**6, ok) == 777
    assert ok.calls <= 25, f"{ok.calls} predicate calls: should be about log2 of the range"
    assert last_true(3, 9, _Counted(lambda x: False)) == 3, "nothing above lo is True: return lo"
    assert last_true(-50, 50, _Counted(lambda x: x <= -17)) == -17


def test_search_rotated():
    assert search_rotated([4, 5, 6, 7, 0, 1, 2], 0) == 4
    assert search_rotated([4, 5, 6, 7, 0, 1, 2], 3) == -1
    assert search_rotated([], 1) == -1
    assert search_rotated([1], 1) == 0
    for n in range(1, 9):
        for a in _rotations(n):
            for i, v in enumerate(a):
                assert search_rotated(a, v) == i, (a, v)
            for v in (-1, 1, 2 * n + 1):
                assert search_rotated(a, v) == -1, (a, v)
    big = list(range(100000))
    probe = _Probe(big[31337:] + big[:31337])
    assert search_rotated(probe, 99) == 100000 - 31337 + 99
    assert probe.reads <= 150, f"{probe.reads} reads for 100000 items: that's not O(log n)"


def test_rotation_min():
    assert rotation_min([4, 5, 6, 7, 0, 1, 2]) == 0
    assert rotation_min([1]) == 1
    assert rotation_min([2, 1]) == 1
    assert rotation_min([1, 2, 3]) == 1, "an unrotated list works too"
    for n in range(1, 10):
        for a in _rotations(n):
            assert rotation_min(a) == 0, a
    big = list(range(5, 100005))
    probe = _Probe(big[70001:] + big[:70001])
    assert rotation_min(probe) == 5
    assert probe.reads <= 100, f"{probe.reads} reads for 100000 items: that's not O(log n)"


def _is_peak(a, i):
    left = a[i - 1] if i > 0 else -_math.inf
    right = a[i + 1] if i + 1 < len(a) else -_math.inf
    return left < a[i] > right


def test_peak_index():
    assert peak_index([1, 3, 2]) == 1
    assert peak_index([5]) == 0
    assert peak_index([1, 2, 3]) == 2, "the last element can be the peak"
    assert peak_index([3, 2, 1]) == 0
    rng = _random.Random(26)
    for _ in range(300):
        a = [rng.randint(0, 5)]
        for _ in range(rng.randint(0, 10)):
            a.append(rng.choice([v for v in range(6) if v != a[-1]]))
        i = peak_index(a)
        assert 0 <= i < len(a) and _is_peak(a, i), (a, i)
    probe = _Probe(list(range(60000)) + list(range(40000, 0, -1)))
    i = peak_index(probe)
    assert i == 59999
    assert probe.reads <= 80, f"{probe.reads} reads for 100000 items: that's not O(log n)"


def _brute_groups(nums, k):
    best = sum(nums)
    n = len(nums)
    for groups in range(1, k + 1):
        for cuts in _itertools.combinations(range(1, n), groups - 1):
            bounds = (0, *cuts, n)
            best = min(best, max(sum(nums[a:b]) for a, b in zip(bounds, bounds[1:])))
    return best


def test_min_largest_group_sum():
    assert min_largest_group_sum([7, 2, 5, 10, 8], 2) == 18
    assert min_largest_group_sum([1, 2, 3, 4, 5], 2) == 9
    assert min_largest_group_sum([1, 4, 4], 3) == 4
    assert min_largest_group_sum([5], 1) == 5
    assert min_largest_group_sum([0, 0, 0], 2) == 0
    rng = _random.Random(26)
    for _ in range(150):
        nums = [rng.randint(0, 9) for _ in range(rng.randint(1, 8))]
        k = rng.randint(1, len(nums))
        assert min_largest_group_sum(nums, k) == _brute_groups(nums, k), (nums, k)
    big = list(range(1, 20001))
    assert min_largest_group_sum(big, 7) == 28579635


def test_min_speed():
    assert min_speed([3, 6, 7, 11], 8) == 4, "hours per pile is ceil(p / s): -(-p // s)"
    assert min_speed([30, 11, 23, 4, 20], 5) == 30
    assert min_speed([30, 11, 23, 4, 20], 6) == 23
    assert min_speed([1], 10) == 1
    assert min_speed([10**6], 2) == 5 * 10**5, "hours per pile is ceil(p / s): -(-p // s)"
    rng = _random.Random(26)
    for _ in range(150):
        piles = [rng.randint(1, 20) for _ in range(rng.randint(1, 6))]
        hours = rng.randint(len(piles), 3 * len(piles) + 5)
        want = next(s for s in range(1, 21) if sum(-(-p // s) for p in piles) <= hours)
        assert min_speed(piles, hours) == want, (piles, hours)


def test_int_sqrt():
    for n in range(300):
        assert int_sqrt(n) == _math.isqrt(n), n
    assert int_sqrt(10**16 - 1) == 99999999, "float sqrt rounds 10**16 - 1 up to 10**8: stay in integers"
    for n in (10**30, 10**30 - 1, (10**20 + 7) ** 2, (10**20 + 7) ** 2 - 1, 2**200 + 12345):
        assert int_sqrt(n) == _math.isqrt(n), n


def test_bisect_root():
    assert abs(bisect_root(lambda x: x ** 3 - 2, 0, 2) - 2 ** (1 / 3)) < 1e-9
    assert abs(bisect_root(lambda x: x - 0.3, 0, 1) - 0.3) < 1e-9
    assert abs(bisect_root(lambda x: _math.exp(x) - 5, 0, 3) - _math.log(5)) < 1e-9
    assert abs(bisect_root(lambda x: x, -1, 1)) < 1e-9


def test_matrix_contains():
    m = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
    for v in (1, 3, 7, 10, 20, 23, 60):
        assert matrix_contains(m, v) is True, v
    for v in (0, 2, 13, 61):
        assert matrix_contains(m, v) is False, v
    assert matrix_contains([], 1) is False
    assert matrix_contains([[]], 1) is False
    assert matrix_contains([[5]], 5) is True
    rng = _random.Random(26)
    for _ in range(100):
        rows, cols = rng.randint(1, 4), rng.randint(1, 4)
        flat = sorted(rng.sample(range(40), rows * cols))
        mat = [flat[r * cols:(r + 1) * cols] for r in range(rows)]
        for v in range(-1, 41):
            assert matrix_contains(mat, v) is (v in flat), (mat, v)
