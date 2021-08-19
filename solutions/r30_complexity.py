"""R30 - Complexity lab (reference solutions)

Compare after you've made your own attempt. Run: python check.py 30 -s
"""
import time
from bisect import bisect_left, bisect_right
from collections import Counter, deque
from heapq import heappop, heappush
from itertools import accumulate

PREDICT = r"""
>>> count = 0
>>> for i in range(100):
...     for j in range(i):
...         count += 1
>>> count
4950

>>> n, steps = 10**6, 0
>>> while n > 1:
...     n //= 2
...     steps += 1
>>> steps
19

>>> (10**9).bit_length(), 2**30 > 10**9
(30, True)

>>> math.comb(10**5, 2)
4999950000

>>> 2 ** 20, math.factorial(10), math.factorial(12)
(1048576, 3628800, 479001600)

>>> sum(1 for _ in permutations(range(8)))
40320

>>> copied = 0
>>> def total(xs):
...     global copied
...     if not xs:
...         return 0
...     copied += len(xs) - 1
...     return xs[0] + total(xs[1:])
>>> total(list(range(100))), copied
(4950, 4950)

>>> cap, size, copies = 1, 0, 0
>>> for _ in range(1000):
...     if size == cap:
...         copies += size
...         cap *= 2
...     size += 1
>>> cap, copies
(1024, 1023)

>>> r = range(0, 10**12, 3)
>>> len(r), 999999999999 in r, r[-1]
(333333333334, True, 999999999999)

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
(0, 4950)

>>> next(x for x in itertools.count() if x * x > 50)
8

>>> calls = 0
>>> def size_of(xs):
...     global calls
...     calls += 1
...     return len(xs)
>>> xs = list(range(10))
>>> for i in range(size_of(xs)):
...     pass
>>> calls
1
>>> i = 0
>>> while i < size_of(xs):
...     i += 1
>>> calls
12

>>> class Probe:
...     seen = 0
...     def __eq__(self, other):
...         Probe.seen += 1
...         return False
>>> p = Probe()
>>> p in list(range(1000)), Probe.seen
(False, 1000)
>>> p in set(range(1000))
TypeError
"""

QUIZ = {
    "list: a[i] or a[i] = x": ["O(1)", "constant"],
    "list: a.append(x)": ["O(1) amortized", "amortized O(1)", "O(1)", "constant", "amortized constant"],
    "list: a.pop()": ["O(1)", "constant"],
    "list: a.pop(0)": ["O(n)", "linear"],
    "list: a.insert(0, x)": ["O(n)", "linear"],
    "list: x in a": ["O(n)", "linear"],
    "list: a.index(x), a.remove(x)": ["O(n)", "linear"],
    "list: len(a)": ["O(1)", "constant"],
    "list: min(a), max(a), sum(a)": ["O(n)", "linear"],
    "list: a[i:j] (k = j - i)": ["O(k)", "O(j - i)", "linear in k"],
    "list: a == b": ["O(n)", "linear", "O(min(n, m))"],
    "list: a.sort() or sorted(a)": ["O(n log n)", "n log n", "linearithmic"],
    "dict/set: d[k], k in d, d[k] = v, del d[k] (average)": ["O(1)", "O(1) average", "average O(1)", "constant"],
    "dict/set: the same operations in the worst case": ["O(n)", "linear"],
    "set: s & t": ["O(min(len(s), len(t)))", "O(min(n, m))", "O(min(m, n))"],
    "deque: append, appendleft, pop, popleft": ["O(1)", "constant"],
    "deque: dq[i] for i in the middle": ["O(n)", "linear"],
    "heapq: heappush, heappop": ["O(log n)", "logarithmic"],
    "heapq: heapify(a)": ["O(n)", "linear"],
    "heapq: h[0]": ["O(1)", "constant"],
    "bisect: bisect_left(a, x)": ["O(log n)", "logarithmic"],
    "bisect: insort(a, x)": ["O(n)", "linear"],
    "str: s + t": ["O(len(s) + len(t))", "O(n + m)", "O(m + n)", "linear"],
    "str: ''.join(parts) (L = total length)": ["O(L)", "O(n)", "linear"],
    "range: x in range(n) for an int x": ["O(1)", "constant"],
    "recursion: f(xs) calls f(xs[1:]) until xs is empty": ["O(n^2)", "quadratic"],
    "loops: for i in range(n): for j in range(i): ...": ["O(n^2)", "quadratic"],
    "loops: while n > 1: n //= 2": ["O(log n)", "logarithmic"],
}


def loops_per_second():
    n = 10 ** 6
    start = time.perf_counter()
    total = 0
    for i in range(n):
        total += i
    return n / (time.perf_counter() - start)


def pair_count(nums, target):
    seen, pairs = Counter(), 0
    for x in nums:
        pairs += seen[target - x]   # every earlier complement makes a pair with x
        seen[x] += 1
    return pairs


def shared_values(a, b):
    present = set(a)
    return sum(x in present for x in b)


def dedupe(items):
    return list(dict.fromkeys(items))


def round_robin(jobs):
    queue = deque(jobs)
    done = []
    while queue:
        name, units = queue.popleft()
        if units > 1:
            queue.append((name, units - 1))
        else:
            done.append(name)
    return done


def range_sums(nums, queries):
    prefix = [0, *accumulate(nums)]
    return [prefix[r + 1] - prefix[l] for l, r in queries]


def count_between(sorted_nums, queries):
    return [max(0, bisect_right(sorted_nums, hi) - bisect_left(sorted_nums, lo))
            for lo, hi in queries]


def kth_largest_so_far(nums, k):
    heap, out = [], []              # min-heap of the k largest seen so far
    for x in nums:
        heappush(heap, x)
        if len(heap) > k:
            heappop(heap)
        out.append(heap[0] if len(heap) == k else None)
    return out


def apply_range_adds(n, updates):
    diff = [0] * (n + 1)
    for lo, hi, delta in updates:
        diff[lo] += delta
        diff[hi + 1] -= delta
    return list(accumulate(diff[:n]))
