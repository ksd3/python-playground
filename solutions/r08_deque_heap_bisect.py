"""R08 - deque, heapq, bisect (reference solutions)

Compare after you've made your own attempt. Run: python check.py 8 -s
"""
from bisect import bisect_left, bisect_right, insort
from collections import Counter, deque
from heapq import heapify, heappop, heappush, heapreplace

PREDICT = r"""
>>> dq = deque([1])
>>> dq.extendleft([2, 3])
>>> dq
deque([3, 2, 1])

>>> dq = deque([1, 2, 3])
>>> dq[0:2]
TypeError
>>> dq[1], dq[-1], 2 in dq
(2, 3, True)

>>> dq = deque(maxlen=3)
>>> dq.extend(range(5))
>>> dq
deque([2, 3, 4], maxlen=3)
>>> dq.appendleft(9)
>>> dq
deque([9, 2, 3], maxlen=3)

>>> dq = deque([1, 2, 3, 4])
>>> dq.rotate(1)
>>> dq
deque([4, 1, 2, 3])
>>> dq.rotate(-2)
>>> dq
deque([2, 3, 4, 1])

>>> dq = deque([1, 2, 3])
>>> dq.popleft(), dq.pop(), dq
(1, 3, deque([2]))
>>> dq.clear()
>>> dq.pop()
IndexError

>>> h = [5, 1, 4, 2, 3]
>>> heapify(h)
>>> h, h[0]
([1, 2, 4, 5, 3], 1)

>>> h = []
>>> for x in [3, 1, 2]:
...     heappush(h, -x)
>>> -h[0], [-heappop(h) for _ in range(3)]
(3, [3, 2, 1])

>>> class Node:
...     pass
>>> h = []
>>> heappush(h, (1, Node()))
>>> heappush(h, (1, Node()))
TypeError
>>> len(h)
2

>>> h = [(2, 'b'), (1, 'z'), (1, 'a')]
>>> heapify(h)
>>> heappop(h)
(1, 'a')

>>> h = [1, 5, 9]
>>> heappushpop(h, 0), h
(0, [1, 5, 9])
>>> heapreplace(h, 0), h
(1, [0, 5, 9])

>>> nlargest(2, [5, 1, 4, 3]), nsmallest(2, 'hello')
([5, 4], ['e', 'h'])
>>> nlargest(2, ['bb', 'a', 'ccc'], key=len)
['ccc', 'bb']

>>> list(heapq.merge([1, 4, 7], [2, 3, 9]))
[1, 2, 3, 4, 7, 9]

>>> heappop([])
IndexError

>>> a = [1, 2, 2, 2, 5]
>>> bisect_left(a, 2), bisect_right(a, 2), bisect_left(a, 3), bisect_right(a, 0)
(1, 4, 4, 0)
>>> bisect_right(a, 2) - bisect_left(a, 2)
3

>>> a = [1, 3, 5]
>>> insort(a, 4)
>>> insort(a, 0)
>>> a
[0, 1, 3, 4, 5]

>>> a = [10, 20, 30]
>>> i = bisect_right(a, 25) - 1
>>> i, a[i]
(1, 20)
>>> bisect_right(a, 5) - 1
-1

>>> bisect_left(range(100), True, key=lambda x: x * x >= 50)
8

>>> a = [(1, 'a'), (3, 'c')]
>>> bisect_left(a, (3,)), bisect_left(a, 3, key=lambda p: p[0])
(1, 1)
"""


def moving_average(nums, k):
    window, total, out = deque(maxlen=k), 0, []
    for x in nums:
        if len(window) == k:
            total -= window[0]  # maxlen is about to push this one out
        window.append(x)
        total += x
        out.append(total / len(window))
    return out


def josephus(n, k):
    circle, out = deque(range(1, n + 1)), []
    while circle:
        circle.rotate(-(k - 1))
        out.append(circle.popleft())
    return out


def heapsort(items):
    h = list(items)
    heapify(h)
    return [heappop(h) for _ in range(len(h))]


def k_largest(nums, k):
    if k <= 0:
        return []
    h = []
    for x in nums:
        if len(h) < k:
            heappush(h, x)
        elif x > h[0]:
            heapreplace(h, x)
    return sorted(h, reverse=True)


def merge_sorted(lists):
    h = [(lst[0], i, 0) for i, lst in enumerate(lists) if lst]
    heapify(h)
    out = []
    while h:
        value, i, j = heappop(h)
        out.append(value)
        if j + 1 < len(lists[i]):
            heappush(h, (lists[i][j + 1], i, j + 1))
    return out


def process_in_priority(tasks):
    # the unique index breaks ties, so two payloads are never compared
    h = [(priority, i, payload) for i, (priority, payload) in enumerate(tasks)]
    heapify(h)
    return [heappop(h)[2] for _ in range(len(h))]


def lazy_min(ops):
    h, pending, out = [], Counter(), []
    for op in ops:
        if op[0] == 'push':
            heappush(h, op[1])
        elif op[0] == 'remove':
            pending[op[1]] += 1
        else:
            while h and pending[h[0]]:
                pending[h[0]] -= 1
                heappop(h)
            out.append(h[0] if h else None)
    return out


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
    return max(0, bisect_right(a, hi) - bisect_left(a, lo))


def floor_ceiling(a, x):
    i, j = bisect_right(a, x), bisect_left(a, x)
    return (a[i - 1] if i else None, a[j] if j < len(a) else None)


def nearest(a, x):
    i = bisect_left(a, x)
    candidates = a[max(0, i - 1):i + 1]  # the last value < x and the first value >= x
    return min(candidates, key=lambda v: (abs(v - x), v))


def count_less_before(nums):
    seen, out = [], []
    for x in nums:
        out.append(bisect_left(seen, x))
        insort(seen, x)
    return out
