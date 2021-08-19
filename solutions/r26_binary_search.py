"""R26 - Binary search (reference solutions)

Compare after you've made your own attempt. Run: python check.py 26 -s
"""

PREDICT = r"""
>>> a = [1, 2, 2, 2, 5]
>>> bisect_left(a, 2), bisect_right(a, 2)
(1, 4)
>>> bisect_left(a, 3), bisect_right(a, 3)
(4, 4)
>>> bisect_left(a, 0), bisect_left(a, 9)
(0, 5)

>>> a = [1, 2, 2, 2, 5]
>>> bisect_right(a, 2) - bisect_left(a, 2)
3

>>> a = [10, 20, 30]
>>> i = bisect_right(a, 25) - 1
>>> i, a[i]
(1, 20)
>>> j = bisect_right(a, 5) - 1
>>> j, a[j]
(-1, 30)

>>> a = [10, 20, 30]
>>> a[bisect_left(a, 25)]
30
>>> a[bisect_left(a, 35)]
IndexError

>>> a = [1, 3, 5]
>>> insort(a, 4)
>>> a
[1, 3, 4, 5]

>>> bisect_left([1, 2, 3, 4, 5], 1, lo=2)
2

>>> bisect_left([5, 1, 4], 5)
3

>>> people = [('ann', 25), ('bob', 31), ('cy', 40)]
>>> bisect_left(people, 31, key=lambda p: p[1])
1
>>> bisect_left(people, ('x', 31), key=lambda p: p[1])
TypeError

>>> bisect_left(range(100), True, key=lambda x: x * x >= 50)
8

>>> lo, hi = 4, 5
>>> (lo + hi) // 2, (lo + hi + 1) // 2
(4, 5)

>>> lo, hi = -3, -2
>>> (lo + hi) // 2, int((lo + hi) / 2)
(-3, -2)

>>> bisect_left(['apple', 'banana', 'cherry'], 'b')
1

>>> lo, hi = 0.0, 2.0
>>> for _ in range(100):
...     mid = (lo + hi) / 2
...     if mid * mid < 2:
...         lo = mid
...     else:
...         hi = mid
>>> round(lo, 6)
1.414214

>>> rows, cols = 3, 4
>>> divmod(7, cols)
(1, 3)
"""

from bisect import bisect_left, bisect_right


def lower_bound(a, x):
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo


def upper_bound(a, x):
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] <= x:
            lo = mid + 1
        else:
            hi = mid
    return lo


def count_in_range(a, lo, hi):
    return bisect_right(a, hi) - bisect_left(a, lo)


def first_true(lo, hi, ok):
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def last_true(lo, hi, ok):
    while lo < hi:
        mid = (lo + hi + 1) // 2      # round up, or `lo = mid` never moves when hi == lo + 1
        if ok(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo


def search_rotated(a, target):
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == target:
            return mid
        if a[lo] <= a[mid]:                  # the left half is sorted
            if a[lo] <= target < a[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                                # the right half is sorted
            if a[mid] < target <= a[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1


def rotation_min(a):
    lo, hi = 0, len(a) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] > a[hi]:     # the drop is to the right of mid
            lo = mid + 1
        else:
            hi = mid
    return a[lo]


def peak_index(a):
    lo, hi = 0, len(a) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < a[mid + 1]:    # walking uphill to the right: a peak lies past mid
            lo = mid + 1
        else:
            hi = mid
    return lo


def min_largest_group_sum(nums, k):
    def fits(cap):
        groups, current = 1, 0
        for x in nums:
            if current + x > cap:
                groups += 1
                current = 0
            current += x
        return groups <= k

    return first_true(max(nums), sum(nums), fits)


def min_speed(piles, hours):
    return first_true(1, max(piles), lambda s: sum(-(-p // s) for p in piles) <= hours)


def int_sqrt(n):
    return last_true(0, n, lambda x: x * x <= n)


def bisect_root(f, lo, hi):
    for _ in range(100):
        mid = (lo + hi) / 2
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def matrix_contains(matrix, target):
    if not matrix or not matrix[0]:
        return False
    rows, cols = len(matrix), len(matrix[0])
    lo, hi = 0, rows * cols
    while lo < hi:
        mid = (lo + hi) // 2
        r, c = divmod(mid, cols)
        if matrix[r][c] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo < rows * cols and matrix[lo // cols][lo % cols] == target
