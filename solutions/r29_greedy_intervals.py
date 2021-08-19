"""R29 - Greedy, intervals, sweep line (reference solutions)

Compare after you've made your own attempt. Run: python check.py 29 -s
"""
import math
from collections import Counter
from fractions import Fraction
from heapq import heappop, heappush, heapreplace

PREDICT = r"""
>>> sorted([[3, 4], [1, 5], [1, 2]])
[[1, 2], [1, 5], [3, 4]]

>>> sorted([(1, 5), (2, 3), (4, 6)], key=lambda iv: iv[1])
[(2, 3), (1, 5), (4, 6)]

>>> sorted([(5, 1), (5, -1), (2, 1)])
[(2, 1), (5, -1), (5, 1)]

>>> out = [[1, 3]]
>>> s, e = [2, 6]
>>> if s <= out[-1][1]:
...     out[-1][1] = max(out[-1][1], e)
>>> out
[[1, 6]]

>>> out = [(1, 3)]
>>> out[-1][1] = 6
TypeError
>>> out[-1] = (out[-1][0], 6)
>>> out
[(1, 6)]

>>> def overlaps(a, b):
...     return a[0] < b[1] and b[0] < a[1]
>>> overlaps((1, 2), (2, 3)), overlaps((1, 3), (2, 4))
(False, True)

>>> a, b = (1, 5), (3, 8)
>>> lo, hi = max(a[0], b[0]), min(a[1], b[1])
>>> (lo, hi) if lo <= hi else None
(3, 5)

>>> rooms = []
>>> for s, e in sorted([(0, 30), (5, 10), (15, 20)]):
...     if rooms and rooms[0] <= s:
...         _ = heapreplace(rooms, e)
...     else:
...         heappush(rooms, e)
>>> len(rooms), sorted(rooms)
(2, [20, 30])

>>> h = [5, 7]
>>> heappushpop(h, 1), h
(1, [5, 7])
>>> h = [5, 7]
>>> heapreplace(h, 1), h
(5, [1, 7])

>>> events = sorted([(1, 1), (4, -1), (2, 1), (3, -1), (3, 1), (5, -1)])
>>> running = list(accumulate(d for _, d in events))
>>> running, max(running)
([1, 2, 1, 2, 1, 0], 2)

>>> reach = 0
>>> for i, step in enumerate([2, 0, 1, 0, 4]):
...     if i > reach:
...         print('stuck at', i)
...         break
...     reach = max(reach, i + step)
... else:
...     print('made it')
stuck at 4

>>> best = cur = 0
>>> for x in [3, -5, 2, 4, -1, 2, -9, 1]:
...     cur = max(0, cur + x)
...     best = max(best, cur)
>>> best
7

>>> pairs = [(1, 'x'), (2, 'y'), (1, 'z')]
>>> sorted(pairs, key=lambda p: p[0], reverse=True)
[(2, 'y'), (1, 'x'), (1, 'z')]
>>> sorted(pairs, key=lambda p: p[0])[::-1]
[(2, 'y'), (1, 'z'), (1, 'x')]

>>> heap = [(-n, ch) for ch, n in Counter('aaabbc').items()]
>>> heapify(heap)
>>> [heappop(heap) for _ in range(3)]
[(-3, 'a'), (-2, 'b'), (-1, 'c')]

>>> def greedy_coins(coins, amount):
...     used = 0
...     for c in sorted(coins, reverse=True):
...         used += amount // c
...         amount %= c
...     return used
>>> greedy_coins([1, 3, 4], 6)
3
>>> min(len(c) for r in range(1, 4) for c in product([1, 3, 4], repeat=r) if sum(c) == 6)
2

>>> from fractions import Fraction
>>> (10**17 + 1) / 10**17 == 1.0
True
>>> Fraction(10**17 + 1, 10**17) > 1
True
"""


def merge_intervals(intervals):
    out = []
    for s, e in sorted(intervals):
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out


def insert_interval(intervals, new):
    s, e = new
    out, i, n = [], 0, len(intervals)
    while i < n and intervals[i][1] < s:
        out.append(list(intervals[i]))
        i += 1
    while i < n and intervals[i][0] <= e:
        s, e = min(s, intervals[i][0]), max(e, intervals[i][1])
        i += 1
    out.append([s, e])
    out.extend(list(iv) for iv in intervals[i:])
    return out


def intersect_lists(a, b):
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        lo, hi = max(a[i][0], b[j][0]), min(a[i][1], b[j][1])
        if lo <= hi:
            out.append([lo, hi])
        if a[i][1] < b[j][1]:   # the interval that ends first can't meet anything else
            i += 1
        else:
            j += 1
    return out


def max_non_overlapping(intervals):
    count, end = 0, -math.inf
    for s, e in sorted(intervals, key=lambda iv: iv[1]):
        if s >= end:
            count += 1
            end = e
    return count


def min_points_to_stab(intervals):
    points, last = 0, -math.inf
    for s, e in sorted(intervals, key=lambda iv: iv[1]):
        if s > last:            # the last point placed misses this interval
            points += 1
            last = e
    return points


def min_rooms(meetings):
    ends = []                   # min-heap of end times, one per room in use
    for s, e in sorted(meetings):
        if ends and ends[0] <= s:
            heapreplace(ends, e)
        else:
            heappush(ends, e)
    return len(ends)


def max_coverage(intervals):
    events = [(s, 0) for s, _ in intervals] + [(e, 1) for _, e in intervals]
    best = cur = 0
    for _, kind in sorted(events):  # at equal times 0 (start) sorts before 1 (end)
        cur += 1 if kind == 0 else -1
        best = max(best, cur)
    return best


def can_reach_end(steps):
    reach = 0
    for i, step in enumerate(steps):
        if i > reach:
            return False
        reach = max(reach, i + step)
    return True


def min_jumps(steps):
    jumps = end = farthest = 0
    for i in range(len(steps) - 1):
        farthest = max(farthest, i + steps[i])
        if i == end:            # the current jump's range is used up
            if farthest <= i:
                return -1
            jumps += 1
            end = farthest
    return jumps


def loop_start(gas, cost):
    if sum(gas) < sum(cost):
        return -1
    start = tank = 0
    for i, (g, c) in enumerate(zip(gas, cost)):
        tank += g - c
        if tank < 0:            # no station in start..i can be the start
            start, tank = i + 1, 0
    return start


def schedule_length(tasks, gap):
    if not tasks:
        return 0
    counts = Counter(tasks).values()
    top = max(counts)
    ties = sum(1 for c in counts if c == top)
    return max(len(tasks), (top - 1) * (gap + 1) + ties)


def max_capital(k, capital, profits, needs):
    projects = sorted(zip(needs, profits))
    best, i = [], 0             # max-heap (negated) of affordable profits
    for _ in range(k):
        while i < len(projects) and projects[i][0] <= capital:
            heappush(best, -projects[i][1])
            i += 1
        if not best:
            break
        capital -= heappop(best)
    return capital


def max_on_time(tasks):
    taken, t = [], 0            # max-heap (negated) of durations taken
    for dur, deadline in sorted(tasks, key=lambda x: x[1]):
        heappush(taken, -dur)
        t += dur
        if t > deadline:
            t += heappop(taken)  # drop the longest task so far
    return len(taken)


def fractional_best(items, capacity):
    total = Fraction(0)
    for value, weight in sorted(items, key=lambda it: Fraction(it[0], it[1]), reverse=True):
        if capacity <= 0:
            break
        take = min(weight, capacity)
        total += Fraction(value * take, weight)
        capacity -= take
    return total
