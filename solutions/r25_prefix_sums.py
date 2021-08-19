"""R25 - Prefix sums and difference arrays (reference solutions)

Compare after you've made your own attempt. Run: python check.py 25 -s
"""

PREDICT = r"""
>>> list(accumulate([3, 1, 4, 1, 5]))
[3, 4, 8, 9, 14]
>>> list(accumulate([3, 1, 4], initial=0))
[0, 3, 4, 8]

>>> a = [3, 1, 4, 1, 5]
>>> P = [0, *accumulate(a)]
>>> P
[0, 3, 4, 8, 9, 14]
>>> P[4] - P[1]
6

>>> a = [3, 1, 4, 1, 5]
>>> S = list(accumulate(a))
>>> l, r = 0, 3
>>> S[r] - S[l - 1]
-5

>>> list(accumulate([2, 5, 1, 7, 3], max))
[2, 5, 5, 7, 7]

>>> a = [1, 2, 3, 4]
>>> list(accumulate(reversed(a)))[::-1]
[10, 9, 7, 4]

>>> def count_k(nums, k, seed):
...     seen, total, ans = Counter(seed), 0, 0
...     for x in nums:
...         total += x
...         ans += seen[total - k]
...         seen[total] += 1
...     return ans
>>> count_k([1, 2, 3], 3, {}), count_k([1, 2, 3], 3, {0: 1})
(1, 2)

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
(4, 2)

>>> [p % 3 for p in accumulate([2, -7, 4])]
[2, 1, 2]

>>> bits = [0, 1, 1, 0, 1]
>>> list(accumulate(1 if b else -1 for b in bits))
[-1, 0, 1, 0, 1]

>>> a = [5, 3, 6, 2]
>>> X = [0, *accumulate(a, operator.xor)]
>>> X
[0, 5, 6, 0, 2]
>>> X[3] ^ X[1]
5

>>> a = [2, 3, 4]
>>> left = list(accumulate([1] + a[:-1], operator.mul))
>>> right = list(accumulate([1] + a[:0:-1], operator.mul))[::-1]
>>> left, right, [x * y for x, y in zip(left, right)]
([1, 2, 6], [12, 4, 1], [12, 8, 6])

>>> n = 5
>>> d = [0] * (n + 1)
>>> for l, r, v in [(1, 3, 2), (0, 1, 5)]:
...     d[l] += v
...     d[r + 1] -= v
>>> list(accumulate(d))[:n]
[5, 7, 2, 2, 0]

>>> n = 3
>>> d = [0] * n
>>> l, r, v = 1, 2, 4
>>> d[l] += v
>>> d[r + 1] -= v
IndexError

>>> R, C = 2, 2
>>> P = [[0] * (C + 1)] * (R + 1)
>>> P[1][1] = 7
>>> P
[[0, 7, 0], [0, 7, 0], [0, 7, 0]]

>>> g = [[1, 2], [3, 4]]
>>> P = [[0] * 3 for _ in range(3)]
>>> for r in range(2):
...     for c in range(2):
...         P[r + 1][c + 1] = g[r][c] + P[r][c + 1] + P[r + 1][c] - P[r][c]
>>> P
[[0, 0, 0], [0, 1, 3], [0, 4, 10]]
>>> P[2][2] - P[0][2] - P[2][1] + P[0][1]
6
"""

from collections import Counter
from itertools import accumulate
import operator


def prefix_sums(nums):
    return [0, *accumulate(nums)]


class RangeSum:
    def __init__(self, nums):
        self.P = [0, *accumulate(nums)]

    def query(self, l, r):
        return self.P[r + 1] - self.P[l]


class MatrixSum:
    def __init__(self, grid):
        rows, cols = len(grid), len(grid[0])
        P = [[0] * (cols + 1) for _ in range(rows + 1)]
        for r in range(rows):
            for c in range(cols):
                P[r + 1][c + 1] = grid[r][c] + P[r][c + 1] + P[r + 1][c] - P[r][c]
        self.P = P

    def query(self, r1, c1, r2, c2):
        P = self.P
        return P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1]


def count_subarrays_sum_k(nums, k):
    seen, total, count = Counter({0: 1}), 0, 0
    for x in nums:
        total += x
        count += seen[total - k]
        seen[total] += 1
    return count


def longest_subarray_sum_k(nums, k):
    first, total, best = {0: -1}, 0, 0
    for i, x in enumerate(nums):
        total += x
        if total - k in first:
            best = max(best, i - first[total - k])
        first.setdefault(total, i)   # keep the earliest index: it gives the longest span
    return best


def count_subarrays_divisible(nums, k):
    seen, total, count = Counter({0: 1}), 0, 0
    for x in nums:
        total = (total + x) % k      # already in 0..k-1, even when the sum is negative
        count += seen[total]
        seen[total] += 1
    return count


def longest_balanced(bits):
    return longest_subarray_sum_k([1 if b else -1 for b in bits], 0)


def product_of_others(nums):
    out = [1] * len(nums)
    left = 1
    for i, x in enumerate(nums):
        out[i] = left
        left *= x
    right = 1
    for i in range(len(nums) - 1, -1, -1):
        out[i] *= right
        right *= nums[i]
    return out


def xor_ranges(nums, queries):
    X = [0, *accumulate(nums, operator.xor)]
    return [X[r + 1] ^ X[l] for l, r in queries]


def apply_range_updates(n, updates):
    d = [0] * (n + 1)
    for l, r, v in updates:
        d[l] += v
        d[r + 1] -= v
    return list(accumulate(d))[:n]


def apply_2d_updates(rows, cols, updates):
    d = [[0] * (cols + 1) for _ in range(rows + 1)]
    for r1, c1, r2, c2, v in updates:
        d[r1][c1] += v
        d[r1][c2 + 1] -= v
        d[r2 + 1][c1] -= v
        d[r2 + 1][c2 + 1] += v
    for row in d:                       # accumulate along each row...
        for c in range(1, cols + 1):
            row[c] += row[c - 1]
    for r in range(1, rows + 1):        # ...then down each column
        for c in range(cols + 1):
            d[r][c] += d[r - 1][c]
    return [row[:cols] for row in d[:rows]]


def balance_index(nums):
    total, left = sum(nums), 0
    for i, x in enumerate(nums):
        if left == total - left - x:
            return i
        left += x
    return -1


def max_subarray_sum(nums):
    best, total, lowest = nums[0], 0, 0
    for x in nums:
        total += x
        best = max(best, total - lowest)
        lowest = min(lowest, total)
    return best
