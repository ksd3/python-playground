"""R25 - Prefix sums and difference arrays

Prefix sums with a leading zero: P[i] is the sum of the first i items, so
sum(a[l..r]) == P[r + 1] - P[l] with no special case for l == 0. In 2D,
inclusion-exclusion gives any rectangle in O(1). Prefix sums + a hashmap count
or measure subarrays with a target sum, and they work with negative numbers,
where a sliding window breaks. The same trick works for XOR and remainders
(Python's % is never negative for a positive modulus). A difference array turns
"add v to a[l..r]" into two writes: d[l] += v, d[r + 1] -= v, then accumulate.

Part 1 - Predict. Each block in PREDICT is a REPL session. Replace every ???
with exactly what Python prints: expression values are echoed the way the REPL
echoes them, and a line that raises prints just the exception name (TypeError).

Part 2 - Drills. Implement every function until `python check.py 25` is green.
Don't edit the tests at the bottom; add your own test_* functions if you like.

Unlocks: range-sum queries, "count/longest subarray with sum k" (negatives
included), divisible-sum and balanced-count subarrays, batched range updates.
"""

PREDICT = r"""
>>> list(accumulate([3, 1, 4, 1, 5]))
???
>>> list(accumulate([3, 1, 4], initial=0))
???

>>> a = [3, 1, 4, 1, 5]
>>> P = [0, *accumulate(a)]
>>> P
???
>>> P[4] - P[1]
???

>>> a = [3, 1, 4, 1, 5]
>>> S = list(accumulate(a))
>>> l, r = 0, 3
>>> S[r] - S[l - 1]
???

>>> list(accumulate([2, 5, 1, 7, 3], max))
???

>>> a = [1, 2, 3, 4]
>>> list(accumulate(reversed(a)))[::-1]
???

>>> def count_k(nums, k, seed):
...     seen, total, ans = Counter(seed), 0, 0
...     for x in nums:
...         total += x
...         ans += seen[total - k]
...         seen[total] += 1
...     return ans
>>> count_k([1, 2, 3], 3, {}), count_k([1, 2, 3], 3, {0: 1})
???

>>> def longest_k(nums, k, keep_first):
...     first, total, best = {0: -1}, 0, 0
...     for i, x in enumerate(nums):
...         total += x
...         if total - k in first:
...             best = max(best, i - first[total - k])
...         if keep_first:
...             first.setdefault(total, i)
...         else:
...             first[total] = i
...     return best
>>> longest_k([1, -1, 5, -2, 3], 3, True), longest_k([1, -1, 5, -2, 3], 3, False)
???

>>> [p % 3 for p in accumulate([2, -7, 4])]
???

>>> bits = [0, 1, 1, 0, 1]
>>> list(accumulate(1 if b else -1 for b in bits))
???

>>> a = [5, 3, 6, 2]
>>> X = [0, *accumulate(a, operator.xor)]
>>> X
???
>>> X[3] ^ X[1]
???

>>> a = [2, 3, 4]
>>> left = list(accumulate([1] + a[:-1], operator.mul))
>>> right = list(accumulate([1] + a[:0:-1], operator.mul))[::-1]
>>> left, right, [x * y for x, y in zip(left, right)]
???

>>> n = 5
>>> d = [0] * (n + 1)
>>> for l, r, v in [(1, 3, 2), (0, 1, 5)]:
...     d[l] += v
...     d[r + 1] -= v
>>> list(accumulate(d))[:n]
???

>>> n = 3
>>> d = [0] * n
>>> l, r, v = 1, 2, 4
>>> d[l] += v
>>> d[r + 1] -= v
???

>>> R, C = 2, 2
>>> P = [[0] * (C + 1)] * (R + 1)
>>> P[1][1] = 7
>>> P
???

>>> g = [[1, 2], [3, 4]]
>>> P = [[0] * 3 for _ in range(3)]
>>> for r in range(2):
...     for c in range(2):
...         P[r + 1][c + 1] = g[r][c] + P[r][c + 1] + P[r + 1][c] - P[r][c]
>>> P
???
>>> P[2][2] - P[0][2] - P[2][1] + P[0][1]
???
"""

from collections import Counter
from itertools import accumulate
import operator


# ---------------------------------------------------------------- drills

def prefix_sums(nums):
    """Return P with a leading zero: len(P) == len(nums) + 1 and P[i] is the
    sum of nums[:i]. prefix_sums([3, 1, 4]) == [0, 3, 4, 8]."""
    raise NotImplementedError


class RangeSum:
    """Precompute once, then answer sum(nums[l..r]) (inclusive) in O(1).

    rs = RangeSum([3, 1, 4, 1, 5]); rs.query(1, 3) == 6; rs.query(0, 4) == 14
    """

    def __init__(self, nums):
        raise NotImplementedError

    def query(self, l, r):
        raise NotImplementedError


class MatrixSum:
    """Precompute a 2D prefix table, then return the sum of the rectangle with
    corners (r1, c1) and (r2, c2), both inclusive, in O(1).

    ms = MatrixSum([[1, 2], [3, 4]]); ms.query(0, 1, 1, 1) == 6
    """

    def __init__(self, grid):
        raise NotImplementedError

    def query(self, r1, c1, r2, c2):
        raise NotImplementedError


def count_subarrays_sum_k(nums, k):
    """Count the non-empty contiguous subarrays whose sum is k. nums may hold
    negatives. O(n). count_subarrays_sum_k([1, 1, 1], 2) == 2."""
    raise NotImplementedError


def longest_subarray_sum_k(nums, k):
    """Length of the longest contiguous subarray whose sum is k, or 0 if there
    is none. Negatives allowed. O(n).
    longest_subarray_sum_k([1, -1, 5, -2, 3], 3) == 4."""
    raise NotImplementedError


def count_subarrays_divisible(nums, k):
    """Count the non-empty contiguous subarrays whose sum is divisible by k
    (k > 0). Negatives allowed. O(n).
    count_subarrays_divisible([4, 5, 0, -2, -3, 1], 5) == 7."""
    raise NotImplementedError


def longest_balanced(bits):
    """bits holds only 0s and 1s. Return the length of the longest contiguous
    stretch with as many 0s as 1s (0 if none). O(n).
    longest_balanced([0, 1, 0]) == 2."""
    raise NotImplementedError


def product_of_others(nums):
    """Return out where out[i] is the product of every element except nums[i].
    No division (zeros must work). O(n).
    product_of_others([1, 2, 3, 4]) == [24, 12, 8, 6]."""
    raise NotImplementedError


def xor_ranges(nums, queries):
    """For each (l, r) in queries, the XOR of nums[l..r] inclusive, in a list.
    O(n + len(queries)). xor_ranges([1, 3, 4, 8], [(0, 1), (1, 2)]) == [2, 7]."""
    raise NotImplementedError


def apply_range_updates(n, updates):
    """Start from n zeros. Each update (l, r, v) adds v to positions l..r
    inclusive. Return the final list in O(n + len(updates)).
    apply_range_updates(5, [(1, 3, 2), (0, 1, 5)]) == [5, 7, 2, 2, 0]."""
    raise NotImplementedError


def apply_2d_updates(rows, cols, updates):
    """Start from a rows x cols grid of zeros. Each update (r1, c1, r2, c2, v)
    adds v to every cell of that inclusive rectangle. Return the final grid in
    O(rows * cols + len(updates)).
    apply_2d_updates(2, 2, [(0, 0, 0, 1, 3)]) == [[3, 3], [0, 0]]."""
    raise NotImplementedError


def balance_index(nums):
    """The leftmost index i where sum(nums[:i]) == sum(nums[i + 1:]), or -1.
    O(n). balance_index([1, 7, 3, 6, 5, 6]) == 3."""
    raise NotImplementedError


def max_subarray_sum(nums):
    """nums is non-empty. Return the largest sum of a non-empty contiguous
    subarray, in O(n), using the smallest prefix sum seen so far.
    max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6."""
    raise NotImplementedError


# ---------------------------------------------------------------- tests (don't edit)

import random as _random


def _rand_list(rng, lo=-9, hi=9, max_len=12, min_len=0):
    return [rng.randint(lo, hi) for _ in range(rng.randint(min_len, max_len))]


def _brute_count(nums, k):
    n = len(nums)
    return sum(sum(nums[i:j]) == k for i in range(n) for j in range(i + 1, n + 1))


def _brute_longest(nums, k):
    n = len(nums)
    return max((j - i for i in range(n) for j in range(i + 1, n + 1) if sum(nums[i:j]) == k), default=0)


def test_prefix_sums():
    assert prefix_sums([3, 1, 4]) == [0, 3, 4, 8]
    assert prefix_sums([]) == [0], "keep the leading zero even for an empty list"
    assert prefix_sums([2, -5, 7]) == [0, 2, -3, 4]


def test_range_sum():
    rs = RangeSum([3, 1, 4, 1, 5])
    assert rs.query(1, 3) == 6
    assert rs.query(2, 2) == 4
    assert rs.query(0, 4) == 14, "query(0, r) is wrong: did P[l - 1] wrap around to the end?"
    rng = _random.Random(25)
    for _ in range(60):
        nums = _rand_list(rng, min_len=1)
        rs = RangeSum(nums)
        for _ in range(10):
            l = rng.randrange(len(nums))
            r = rng.randrange(l, len(nums))
            assert rs.query(l, r) == sum(nums[l:r + 1]), (nums, l, r)


def test_matrix_sum():
    ms = MatrixSum([[1, 2], [3, 4]])
    assert ms.query(0, 0, 1, 1) == 10
    assert ms.query(1, 1, 1, 1) == 4
    assert ms.query(0, 1, 1, 1) == 6
    rng = _random.Random(25)
    for _ in range(30):
        R, C = rng.randint(1, 5), rng.randint(1, 5)
        grid = [[rng.randint(-5, 9) for _ in range(C)] for _ in range(R)]
        ms = MatrixSum(grid)
        for _ in range(10):
            r1, r2 = sorted(rng.randrange(R) for _ in range(2))
            c1, c2 = sorted(rng.randrange(C) for _ in range(2))
            want = sum(grid[r][c] for r in range(r1, r2 + 1) for c in range(c1, c2 + 1))
            assert ms.query(r1, c1, r2, c2) == want, (grid, r1, c1, r2, c2)


def test_count_subarrays_sum_k():
    seed_hint = "seed the counter with {0: 1}: subarrays can start at index 0"
    assert count_subarrays_sum_k([1, 2, 3], 3) == 2, seed_hint
    assert count_subarrays_sum_k([1, 1, 1], 2) == 2, seed_hint
    assert count_subarrays_sum_k([1, -1, 0], 0) == 3
    assert count_subarrays_sum_k([], 0) == 0
    rng = _random.Random(25)
    for _ in range(200):
        nums, k = _rand_list(rng, -3, 3), rng.randint(-4, 4)
        assert count_subarrays_sum_k(nums, k) == _brute_count(nums, k), (nums, k)


def test_longest_subarray_sum_k():
    assert longest_subarray_sum_k([1, -1, 5, -2, 3], 3) == 4, "store only the FIRST index of each prefix sum"
    assert longest_subarray_sum_k([-2, -1, 2, 1], 1) == 2
    assert longest_subarray_sum_k([1, 2, 3], 7) == 0
    assert longest_subarray_sum_k([], 0) == 0
    rng = _random.Random(25)
    for _ in range(200):
        nums, k = _rand_list(rng, -3, 3), rng.randint(-4, 4)
        assert longest_subarray_sum_k(nums, k) == _brute_longest(nums, k), (nums, k)


def test_count_subarrays_divisible():
    assert count_subarrays_divisible([4, 5, 0, -2, -3, 1], 5) == 7
    assert count_subarrays_divisible([5], 9) == 0
    assert count_subarrays_divisible([-1, 1], 2) == 1, "negative running sums: Python's % is already non-negative"
    rng = _random.Random(25)
    for _ in range(200):
        nums, k = _rand_list(rng), rng.randint(1, 6)
        n = len(nums)
        want = sum(sum(nums[i:j]) % k == 0 for i in range(n) for j in range(i + 1, n + 1))
        assert count_subarrays_divisible(nums, k) == want, (nums, k)


def test_longest_balanced():
    assert longest_balanced([0, 1]) == 2
    assert longest_balanced([0, 1, 0]) == 2
    assert longest_balanced([0, 0, 1, 0, 0, 0, 1, 1]) == 6
    assert longest_balanced([1, 1, 1]) == 0
    assert longest_balanced([]) == 0
    rng = _random.Random(25)
    for _ in range(200):
        bits = [rng.randint(0, 1) for _ in range(rng.randint(0, 12))]
        mapped = [1 if b else -1 for b in bits]
        assert longest_balanced(bits) == _brute_longest(mapped, 0), bits


def test_product_of_others():
    assert product_of_others([1, 2, 3, 4]) == [24, 12, 8, 6]
    assert product_of_others([0, 1, 2]) == [2, 0, 0], "a zero breaks 'total // nums[i]': use left and right products"
    assert product_of_others([0, 2, 0]) == [0, 0, 0]
    assert product_of_others([5]) == [1]
    assert product_of_others([]) == []
    rng = _random.Random(25)
    for _ in range(100):
        nums = _rand_list(rng, -4, 4, max_len=8)
        want = []
        for i in range(len(nums)):
            p = 1
            for j, x in enumerate(nums):
                if j != i:
                    p *= x
            want.append(p)
        assert product_of_others(nums) == want, nums


def test_xor_ranges():
    assert xor_ranges([1, 3, 4, 8], [(0, 1), (1, 2), (0, 3), (3, 3)]) == [2, 7, 14, 8]
    assert xor_ranges([7], []) == []
    rng = _random.Random(25)
    for _ in range(60):
        nums = _rand_list(rng, 0, 63, min_len=1)
        queries = []
        for _ in range(8):
            l = rng.randrange(len(nums))
            queries.append((l, rng.randrange(l, len(nums))))
        want = []
        for l, r in queries:
            x = 0
            for v in nums[l:r + 1]:
                x ^= v
            want.append(x)
        assert xor_ranges(nums, queries) == want, (nums, queries)


def test_apply_range_updates():
    assert apply_range_updates(5, [(1, 3, 2), (0, 1, 5)]) == [5, 7, 2, 2, 0]
    assert apply_range_updates(3, [(0, 2, 1)]) == [1, 1, 1], "an update ending at n - 1 writes d[n]: give d length n + 1"
    assert apply_range_updates(0, []) == []
    assert apply_range_updates(2, []) == [0, 0]
    rng = _random.Random(25)
    for _ in range(100):
        n = rng.randint(1, 10)
        updates = []
        for _ in range(rng.randint(0, 6)):
            l = rng.randrange(n)
            updates.append((l, rng.randrange(l, n), rng.randint(-5, 5)))
        want = [0] * n
        for l, r, v in updates:
            for i in range(l, r + 1):
                want[i] += v
        assert apply_range_updates(n, updates) == want, (n, updates)


def test_apply_2d_updates():
    assert apply_2d_updates(2, 2, [(0, 0, 0, 1, 3)]) == [[3, 3], [0, 0]]
    assert apply_2d_updates(2, 3, [(0, 0, 1, 1, 1), (1, 1, 1, 2, 10)]) == [[1, 1, 0], [1, 11, 10]]
    assert apply_2d_updates(1, 1, []) == [[0]]
    rng = _random.Random(25)
    for _ in range(60):
        R, C = rng.randint(1, 5), rng.randint(1, 5)
        updates = []
        for _ in range(rng.randint(0, 5)):
            r1, r2 = sorted(rng.randrange(R) for _ in range(2))
            c1, c2 = sorted(rng.randrange(C) for _ in range(2))
            updates.append((r1, c1, r2, c2, rng.randint(-5, 5)))
        want = [[0] * C for _ in range(R)]
        for r1, c1, r2, c2, v in updates:
            for r in range(r1, r2 + 1):
                for c in range(c1, c2 + 1):
                    want[r][c] += v
        assert apply_2d_updates(R, C, updates) == want, (R, C, updates)


def test_balance_index():
    assert balance_index([1, 7, 3, 6, 5, 6]) == 3
    assert balance_index([1, 2, 3]) == -1
    assert balance_index([2, 1, -1]) == 0, "index 0 has an empty left side (sum 0)"
    assert balance_index([0]) == 0
    assert balance_index([]) == -1
    rng = _random.Random(25)
    for _ in range(200):
        nums = _rand_list(rng, -2, 2)
        want = next((i for i in range(len(nums)) if sum(nums[:i]) == sum(nums[i + 1:])), -1)
        assert balance_index(nums) == want, nums


def test_max_subarray_sum():
    assert max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert max_subarray_sum([-3, -1, -2]) == -1, "the subarray must be non-empty, even when everything is negative"
    assert max_subarray_sum([5]) == 5
    rng = _random.Random(25)
    for _ in range(200):
        nums = _rand_list(rng, min_len=1)
        n = len(nums)
        want = max(sum(nums[i:j]) for i in range(n) for j in range(i + 1, n + 1))
        assert max_subarray_sum(nums) == want, nums
