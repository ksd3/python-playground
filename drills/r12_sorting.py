"""R12 - Sorting

sorted() returns a new list; list.sort() sorts in place and returns None. Both
are stable: equal keys keep their input order, even with reverse=True. That is
what makes two-pass sorts work (sort by the secondary key, then the primary).
key= is called once per item; a tuple key sorts by several fields, and negating
a number flips one field (you can't negate a string). cmp_to_key wraps a
two-argument comparator for orders defined pairwise. Sorting objects needs only
__lt__. Timsort is O(n log n) and close to O(n) on nearly sorted input.

Part 1 - Predict. Each block in PREDICT is a REPL session. Replace every ???
with exactly what Python prints: expression values are echoed the way the REPL
echoes them, and a line that raises prints just the exception name (TypeError).

Part 2 - Drills. Implement every function and class until `python check.py 12`
is green. Write the hand-made sorts without sorted() or list.sort(). Don't edit
the tests at the bottom; add your own test_* functions if you like.

Unlocks: sort-first greedy strategies, interval problems, k-th element
selection, custom orderings, inversion counting, and divide and conquer.
"""
import bisect
import functools
import operator
import random
from collections import Counter
from fractions import Fraction
from functools import cmp_to_key

PREDICT = r"""
>>> nums = [3, 1, 2]
>>> print(nums.sort())
???
>>> nums
???
>>> sorted('bca')
???
>>> ''.join(sorted('bca'))
???

>>> d = {'b': 1, 'a': 3, 'c': 2}
>>> sorted(d)
???
>>> sorted(d, key=d.get)
???
>>> sorted(d.items(), key=lambda kv: kv[1], reverse=True)
???

>>> sorted(['b', 'A', 'a', 'B'])
???
>>> sorted(['b', 'A', 'a', 'B'], key=str.lower)
???

>>> sorted(['10', '9', '100'])
???
>>> sorted(['10', '9', '100'], key=int)
???

>>> words = ['bb', 'a', 'ccc', 'aa']
>>> sorted(words, key=lambda w: (-len(w), w))
???
>>> sorted(['a', 'b'], key=lambda s: -s)
???

>>> pairs = [('x', 2), ('y', 1), ('z', 2)]
>>> sorted(pairs, key=lambda p: p[1], reverse=True)
???

>>> people = [('bo', 30), ('al', 25), ('bo', 20), ('al', 35)]
>>> by_age = sorted(people, key=lambda p: p[1])
>>> sorted(by_age, key=lambda p: p[0], reverse=True)
???

>>> sorted([-3, 2, -1, 3], key=abs)
???

>>> sorted([3, 'a', 1])
???
>>> sorted([3, 1.5, True])
???

>>> sorted([(2, 'b'), (1, 'z'), (2, 'a')])
???
>>> sorted([[1, 2], [1], [0, 9]])
???

>>> nums = [30, 10, 20]
>>> order = sorted(range(len(nums)), key=nums.__getitem__)
>>> order, [nums[i] for i in order]
???

>>> def by_len_desc(a, b):
...     return len(b) - len(a)
>>> sorted(['a', 'ccc', 'bb'], key=cmp_to_key(by_len_desc))
???

>>> class P:
...     def __init__(self, x):
...         self.x = x
>>> sorted([P(2), P(1)])
???
>>> [p.x for p in sorted([P(2), P(1)], key=operator.attrgetter('x'))]
???

>>> class Q:
...     def __init__(self, x):
...         self.x = x
...     def __lt__(self, other):
...         return self.x < other.x
>>> [q.x for q in sorted([Q(3), Q(1), Q(2)])]
???
>>> Q(1) > Q(0)
???
>>> Q(1) <= Q(2)
???

>>> @dataclass(order=True)
... class Card:
...     rank: int
...     suit: str
>>> sorted([Card(2, 'h'), Card(1, 's'), Card(2, 'c')])
???

>>> calls = []
>>> def key(x):
...     calls.append(x)
...     return -x
>>> sorted([3, 1, 2], key=key)
???
>>> len(calls)
???
"""


# ---------------------------------------------------------------- drills

def by_length_then_alpha(words):
    """Return a new list: shorter words first, equal lengths alphabetical.
    ['pear', 'fig', 'kiwi'] -> ['fig', 'kiwi', 'pear']"""
    raise NotImplementedError


def by_freq_desc(words):
    """Return the distinct words, most frequent first, ties alphabetical.
    ['b', 'a', 'c', 'b', 'a', 'b'] -> ['b', 'a', 'c']"""
    raise NotImplementedError


def sort_people(people):
    """people is a list of (name, age). Return them by name DESCENDING, and by
    age ascending among equal names. (You can't negate a string: lean on
    stability and sort twice.)"""
    raise NotImplementedError


def argsort(nums):
    """The indexes that would sort nums, ties in index order:
    argsort([30, 10, 20, 10]) == [1, 3, 2, 0]"""
    raise NotImplementedError


def sort_fractions(pairs):
    """pairs holds (numerator, denominator) with denominator > 0. Return them
    ordered by exact value (no floats: compare by cross-multiplying inside a
    cmp_to_key comparator); equal values keep their input order.
    [(1, 2), (1, 3), (2, 4)] -> [(1, 3), (1, 2), (2, 4)]"""
    raise NotImplementedError


class Version:
    """A dotted version like Version('1.10.0'). Compare numerically part by
    part, treating missing parts as 0: Version('1.2') < Version('1.10') and
    Version('1.0') == Version('1'). Needs __lt__ and __eq__ (that's enough for
    sorted, min and max) and __repr__ giving "Version('1.10.0')"."""

    def __init__(self, text):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    def __lt__(self, other):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError


def insertion_sort(nums):
    """Sort the list in place (stable) and return None. Compare items with <
    only."""
    raise NotImplementedError


def merge_sort(nums):
    """Return a new sorted list (stable) and leave nums untouched. O(n log n).
    Compare items with < only."""
    raise NotImplementedError


def count_inversions(nums):
    """Count pairs i < j with nums[i] > nums[j], in O(n log n): count them while
    merge sorting. count_inversions([2, 4, 1, 3, 5]) == 3"""
    raise NotImplementedError


def quicksort(nums):
    """Sort the list in place and return None. Pick a random pivot, and make it
    hold up on sorted input and on lots of duplicates (all-equal input must not
    blow the recursion limit)."""
    raise NotImplementedError


def kth_smallest(nums, k):
    """The k-th smallest value (k is 1-based) by quickselect: average O(n), no
    full sort. Don't reorder the caller's list. Lots of duplicates must stay
    fast. kth_smallest([7, 2, 9, 4], 2) == 4"""
    raise NotImplementedError


def counting_sort(nums):
    """Return a new sorted list of ints (negatives allowed) in
    O(n + (max - min)) by counting occurrences."""
    raise NotImplementedError


def sort_by_frequency(nums):
    """More frequent values first, each repeated as often as it occurs; equal
    frequencies put the smaller value first. Bucket the values by count.
    [4, 1, 1, 2, 2, 2, 3] -> [2, 2, 2, 1, 1, 3, 4]"""
    raise NotImplementedError


# ---------------------------------------------------------------- tests (don't edit)

@functools.total_ordering
class _Card:
    """Compares by rank only, so equal ranks reveal whether a sort is stable."""

    def __init__(self, rank, tag):
        self.rank, self.tag = rank, tag

    def __eq__(self, other):
        return self.rank == other.rank

    def __lt__(self, other):
        return self.rank < other.rank


def _cards(ranks):
    return [_Card(r, i) for i, r in enumerate(ranks)]


class _Counted:
    """Wraps a value and counts every comparison. Once the budget runs out it
    fails the test, so a quadratic algorithm stops in milliseconds instead of
    grinding on, on any machine."""
    used = budget = 0
    message = ''

    def __init__(self, v):
        self.v = v

    def _tick(self, other):
        _Counted.used += 1
        if _Counted.used > _Counted.budget:
            raise AssertionError(_Counted.message)
        return getattr(other, 'v', other)

    def __lt__(self, other):
        return self.v < self._tick(other)

    def __le__(self, other):
        return self.v <= self._tick(other)

    def __gt__(self, other):
        return self.v > self._tick(other)

    def __ge__(self, other):
        return self.v >= self._tick(other)

    def __eq__(self, other):
        return self.v == self._tick(other)

    def __ne__(self, other):
        return self.v != self._tick(other)

    def __hash__(self):
        return hash(self.v)


def _counted(values, budget, message):
    _Counted.used, _Counted.budget, _Counted.message = 0, budget, message
    return [_Counted(v) for v in values]


def _fast_inversions(values):
    seen, count = [], 0
    for v in values:
        count += len(seen) - bisect.bisect_right(seen, v)
        bisect.insort(seen, v)
    return count


def _people_order(p, q):
    if p[0] != q[0]:
        return -1 if p[0] > q[0] else 1
    return (p[1] > q[1]) - (p[1] < q[1])


def _brute_inversions(nums):
    return sum(nums[i] > nums[j] for i in range(len(nums)) for j in range(i + 1, len(nums)))


def test_by_length_then_alpha():
    words = ['pear', 'fig', 'apple', 'kiwi', 'date']
    assert by_length_then_alpha(words) == ['fig', 'date', 'kiwi', 'pear', 'apple']
    assert words == ['pear', 'fig', 'apple', 'kiwi', 'date'], "return a new list; don't sort the input"
    assert by_length_then_alpha([]) == []


def test_by_freq_desc():
    assert by_freq_desc(['b', 'a', 'c', 'b', 'a', 'b']) == ['b', 'a', 'c']
    assert by_freq_desc(['z', 'y', 'x']) == ['x', 'y', 'z'], "ties go alphabetical"
    assert by_freq_desc([]) == []


def test_sort_people():
    people = [('bo', 30), ('al', 25), ('bo', 20), ('al', 35), ('cy', 1)]
    assert sort_people(people) == [('cy', 1), ('bo', 20), ('bo', 30), ('al', 25), ('al', 35)]
    rng = random.Random(12)
    for _ in range(100):
        ps = [(rng.choice(['ann', 'bob', 'cat']), rng.randint(1, 5)) for _ in range(rng.randint(0, 8))]
        assert sort_people(ps) == sorted(ps, key=cmp_to_key(_people_order)), ps


def test_argsort():
    assert argsort([30, 10, 20, 10]) == [1, 3, 2, 0], "ties keep index order"
    assert argsort([]) == []
    rng = random.Random(12)
    for _ in range(100):
        nums = [rng.randint(0, 5) for _ in range(rng.randint(0, 10))]
        assert argsort(nums) == sorted(range(len(nums)), key=lambda i: (nums[i], i)), nums


def test_sort_fractions():
    assert sort_fractions([(1, 2), (1, 3), (2, 4), (3, 1)]) == [(1, 3), (1, 2), (2, 4), (3, 1)], \
        "equal values keep their input order"
    big = 10 ** 17
    assert sort_fractions([(big + 1, big), (1, 1)]) == [(1, 1), (big + 1, big)], \
        "floats can't tell these two apart: cross-multiply instead"
    rng = random.Random(12)
    for _ in range(100):
        ps = [(rng.randint(-9, 9), rng.randint(1, 9)) for _ in range(rng.randint(0, 8))]
        assert sort_fractions(ps) == sorted(ps, key=lambda p: Fraction(*p)), ps


def test_version():
    vs = [Version(s) for s in ['1.10', '1.2', '1.2.1', '1', '0.9']]
    assert [repr(v) for v in sorted(vs)] == \
        ["Version('0.9')", "Version('1')", "Version('1.2')", "Version('1.2.1')", "Version('1.10')"], \
        "compare the parts as numbers, not strings"
    assert Version('1.0') == Version('1') and Version('1.0.0') == Version('1'), "missing parts count as 0"
    assert Version('2') < Version('10')
    assert not Version('1.0') < Version('1')
    assert Version('1') < Version('1.0.1')
    assert max(vs) == Version('1.10') and min(vs) == Version('0.9')


def test_insertion_sort():
    rng = random.Random(12)
    for _ in range(100):
        nums = [rng.randint(-5, 5) for _ in range(rng.randint(0, 12))]
        expected = sorted(nums)
        assert insertion_sort(nums) is None
        assert nums == expected
    cards = _cards([3, 1, 3, 2, 1])
    insertion_sort(cards)
    assert [(c.rank, c.tag) for c in cards] == [(1, 1), (1, 4), (2, 3), (3, 0), (3, 2)], \
        "not stable: equal items changed order (shift only items that are strictly bigger)"


def test_merge_sort():
    rng = random.Random(12)
    for _ in range(100):
        nums = [rng.randint(-5, 5) for _ in range(rng.randint(0, 20))]
        before = nums[:]
        assert merge_sort(nums) == sorted(before)
        assert nums == before, "return a new list; leave the input alone"
    out = merge_sort(_cards([3, 1, 3, 2, 1, 2, 3]))
    assert [(c.rank, c.tag) for c in out] == [(1, 1), (1, 4), (2, 3), (2, 5), (3, 0), (3, 2), (3, 6)], \
        "not stable: on ties take from the left half"


def test_count_inversions():
    assert count_inversions([2, 4, 1, 3, 5]) == 3
    assert count_inversions([]) == 0 and count_inversions([1, 2, 3]) == 0
    assert count_inversions([5, 4, 3, 2, 1]) == 10
    assert count_inversions([2, 2, 1]) == 2, "equal values aren't an inversion"
    rng = random.Random(12)
    for _ in range(100):
        nums = [rng.randint(0, 6) for _ in range(rng.randint(0, 12))]
        assert count_inversions(nums) == _brute_inversions(nums), nums
    values = [rng.randint(0, 10 ** 6) for _ in range(2000)]
    nums = _counted(values, 3 * 2000 * 11, "too many comparisons for n = 2000: count while merge sorting, O(n log n)")
    assert count_inversions(nums) == _fast_inversions(values)


def test_quicksort():
    rng = random.Random(12)
    for _ in range(100):
        nums = [rng.randint(-5, 5) for _ in range(rng.randint(0, 30))]
        expected = sorted(nums)
        assert quicksort(nums) is None
        assert nums == expected, expected
    cases = [('all-equal', [7] * 3000), ('sorted', list(range(3000))), ('reversed', list(range(3000, 0, -1))),
             ('duplicate-heavy', [rng.randint(0, 99) for _ in range(3000)])]
    for name, values in cases:
        nums = _counted(values, 20 * 3000 * 12, f"too many comparisons on {name} input: pick a random pivot and "
                                                "split equal values evenly (three-way or Hoare partition)")
        try:
            quicksort(nums)
        except RecursionError:
            raise AssertionError(f"{name} input blew the recursion limit: pick a random pivot and split equal "
                                 "values evenly (three-way or Hoare partition)")
        assert [x.v for x in nums] == sorted(values), name


def test_kth_smallest():
    nums = [7, 2, 9, 4, 2]
    assert [kth_smallest(nums, k) for k in range(1, 6)] == [2, 2, 4, 7, 9]
    assert nums == [7, 2, 9, 4, 2], "don't reorder the caller's list"
    rng = random.Random(12)
    for _ in range(100):
        xs = [rng.randint(0, 9) for _ in range(rng.randint(1, 15))]
        k = rng.randint(1, len(xs))
        assert kth_smallest(xs, k) == sorted(xs)[k - 1], (xs, k)
    same = _counted([5] * 3000, 60 * 3000, "duplicates made the partition quadratic: split three ways "
                                           "(less / equal / greater)")
    try:
        assert kth_smallest(same, 1500).v == 5
    except RecursionError:
        raise AssertionError("duplicates blew the recursion limit: split three ways (less / equal / greater)")
    values = [rng.randint(0, 10 ** 9) for _ in range(3000)]
    nums = _counted(values, 60 * 3000, "too many comparisons for n = 3000: quickselect should be about O(n)")
    assert kth_smallest(nums, 1500).v == sorted(values)[1499]


def test_counting_sort():
    assert counting_sort([3, -1, 2, -1, 0]) == [-1, -1, 0, 2, 3]
    assert counting_sort([]) == []
    assert counting_sort([5]) == [5]
    rng = random.Random(12)
    for _ in range(100):
        nums = [rng.randint(-20, 20) for _ in range(rng.randint(0, 30))]
        before = nums[:]
        assert counting_sort(nums) == sorted(before), before
        assert nums == before, "return a new list; leave the input alone"


def test_sort_by_frequency():
    assert sort_by_frequency([4, 1, 1, 2, 2, 2, 3]) == [2, 2, 2, 1, 1, 3, 4]
    assert sort_by_frequency([]) == []
    rng = random.Random(12)
    for _ in range(100):
        nums = [rng.randint(0, 6) for _ in range(rng.randint(0, 15))]
        counts = Counter(nums)
        assert sort_by_frequency(nums) == sorted(nums, key=lambda x: (-counts[x], x)), nums
