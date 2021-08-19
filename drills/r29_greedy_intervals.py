"""R29 - Greedy, intervals, sweep line

A greedy algorithm makes the locally best choice and never revisits it. It's
only correct when an exchange argument holds: swapping an optimal solution's
choice for the greedy one never makes things worse. Write that argument in 2-3
sentences, then stress-test against a brute force; wrong greedy ideas die there.
Intervals: sort first. By start to merge, by end to keep the most disjoint ones.
Sweep line: turn intervals into (time, delta) events and sort them; at equal
times the tuple order decides whether touching intervals count as overlapping.

Part 1 - Predict. Each block in PREDICT is a REPL session. Replace every ???
with exactly what Python prints: expression values are echoed the way the REPL
echoes them, and a line that raises prints just the exception name (TypeError).

Part 2 - Drills. Implement every function until `python check.py 29` is green.
Don't edit the tests at the bottom; add your own test_* functions if you like.

Unlocks: merging and inserting ranges, room/resource allocation, max disjoint
intervals, reach scanning, circular-route balances, cooldown scheduling,
deadline scheduling, and "sort by requirement, pick from a heap by reward".
"""
import math
import random
from collections import Counter, deque
from fractions import Fraction
from heapq import heappop, heappush, heapreplace
from itertools import combinations

PREDICT = r"""
>>> sorted([[3, 4], [1, 5], [1, 2]])
???

>>> sorted([(1, 5), (2, 3), (4, 6)], key=lambda iv: iv[1])
???

>>> sorted([(5, 1), (5, -1), (2, 1)])
???

>>> out = [[1, 3]]
>>> s, e = [2, 6]
>>> if s <= out[-1][1]:
...     out[-1][1] = max(out[-1][1], e)
>>> out
???

>>> out = [(1, 3)]
>>> out[-1][1] = 6
???
>>> out[-1] = (out[-1][0], 6)
>>> out
???

>>> def overlaps(a, b):
...     return a[0] < b[1] and b[0] < a[1]
>>> overlaps((1, 2), (2, 3)), overlaps((1, 3), (2, 4))
???

>>> a, b = (1, 5), (3, 8)
>>> lo, hi = max(a[0], b[0]), min(a[1], b[1])
>>> (lo, hi) if lo <= hi else None
???

>>> rooms = []
>>> for s, e in sorted([(0, 30), (5, 10), (15, 20)]):
...     if rooms and rooms[0] <= s:
...         _ = heapreplace(rooms, e)
...     else:
...         heappush(rooms, e)
>>> len(rooms), sorted(rooms)
???

>>> h = [5, 7]
>>> heappushpop(h, 1), h
???
>>> h = [5, 7]
>>> heapreplace(h, 1), h
???

>>> events = sorted([(1, 1), (4, -1), (2, 1), (3, -1), (3, 1), (5, -1)])
>>> running = list(accumulate(d for _, d in events))
>>> running, max(running)
???

>>> reach = 0
>>> for i, step in enumerate([2, 0, 1, 0, 4]):
...     if i > reach:
...         print('stuck at', i)
...         break
...     reach = max(reach, i + step)
... else:
...     print('made it')
???

>>> best = cur = 0
>>> for x in [3, -5, 2, 4, -1, 2, -9, 1]:
...     cur = max(0, cur + x)
...     best = max(best, cur)
>>> best
???

>>> pairs = [(1, 'x'), (2, 'y'), (1, 'z')]
>>> sorted(pairs, key=lambda p: p[0], reverse=True)
???
>>> sorted(pairs, key=lambda p: p[0])[::-1]
???

>>> heap = [(-n, ch) for ch, n in Counter('aaabbc').items()]
>>> heapify(heap)
>>> [heappop(heap) for _ in range(3)]
???

>>> def greedy_coins(coins, amount):
...     used = 0
...     for c in sorted(coins, reverse=True):
...         used += amount // c
...         amount %= c
...     return used
>>> greedy_coins([1, 3, 4], 6)
???
>>> min(len(c) for r in range(1, 4) for c in product([1, 3, 4], repeat=r) if sum(c) == 6)
???

>>> from fractions import Fraction
>>> (10**17 + 1) / 10**17 == 1.0
???
>>> Fraction(10**17 + 1, 10**17) > 1
???
"""


# ---------------------------------------------------------------- drills

def merge_intervals(intervals):
    """Merge overlapping closed intervals [s, e] (touching ones merge too:
    [1, 3] + [3, 5] -> [1, 5]). Return a new list of [s, e] lists sorted by
    start; don't modify the input. O(n log n).
    merge_intervals([[1, 3], [8, 10], [2, 6]]) == [[1, 6], [8, 10]]"""
    raise NotImplementedError


def insert_interval(intervals, new):
    """`intervals` is sorted by start and has no overlaps. Insert the closed
    interval `new`, merging whatever it overlaps or touches, and return the
    result as a new list of [s, e] lists. O(n), no sorting needed.
    insert_interval([[1, 3], [6, 9]], [2, 5]) == [[1, 5], [6, 9]]"""
    raise NotImplementedError


def intersect_lists(a, b):
    """a and b are each sorted lists of disjoint closed intervals. Return the
    list of their intersections, in order, as [s, e] lists. Two pointers, O(n + m).
    intersect_lists([[0, 2], [5, 10]], [[1, 5]]) == [[1, 2], [5, 5]]"""
    raise NotImplementedError


def max_non_overlapping(intervals):
    """Half-open intervals [s, e) (so [1, 2) and [2, 3) don't overlap). Return
    the largest number of them you can keep with no two overlapping.
    max_non_overlapping([[1, 2], [2, 3], [3, 4], [1, 3]]) == 3"""
    raise NotImplementedError


def min_points_to_stab(intervals):
    """Closed intervals [s, e]. Return the fewest points such that every
    interval contains at least one of them.
    min_points_to_stab([[10, 16], [2, 8], [1, 6], [7, 12]]) == 2"""
    raise NotImplementedError


def min_rooms(meetings):
    """Half-open meetings [s, e). Return the fewest rooms so no two meetings in
    the same room overlap (a meeting ending at 5 frees its room for one
    starting at 5). min_rooms([[0, 30], [5, 10], [15, 20]]) == 2"""
    raise NotImplementedError


def max_coverage(intervals):
    """Closed intervals [s, e]. Return the largest number of intervals that
    contain one common point (0 for no intervals). Sweep over sorted events.
    max_coverage([[1, 2], [2, 3]]) == 2"""
    raise NotImplementedError


def can_reach_end(steps):
    """Start at index 0 of a non-empty list; from index i you may move forward
    by 0..steps[i] positions. Return True if the last index is reachable, else
    False. O(n). can_reach_end([2, 3, 1, 1, 4]) is True"""
    raise NotImplementedError


def min_jumps(steps):
    """Same moves as can_reach_end. Return the fewest moves to reach the last
    index, or -1 if it can't be reached. O(n), no BFS queue needed.
    min_jumps([2, 3, 1, 1, 4]) == 2"""
    raise NotImplementedError


def loop_start(gas, cost):
    """Stations 0..n-1 sit on a loop. At station i you pick up gas[i]; driving
    from i to i+1 (and from n-1 to 0) burns cost[i]. Starting with an empty
    tank, return the smallest start index that lets you drive the whole loop
    without the tank going negative, or -1. O(n).
    loop_start([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]) == 3"""
    raise NotImplementedError


def schedule_length(tasks, gap):
    """`tasks` is a string of task labels, one slot each, in any order you like.
    Two runs of the same label need at least `gap` other slots (busy or idle)
    between them. Return the fewest slots to run every task.
    schedule_length('AAABBB', 2) == 8   # A B _ A B _ A B"""
    raise NotImplementedError


def max_capital(k, capital, profits, needs):
    """You start with `capital` and may complete at most k distinct projects,
    one at a time. Project i can only start while your capital is >= needs[i],
    and finishing it adds profits[i] (>= 0) to your capital; nothing is spent.
    Return the largest capital you can end with. O(n log n).
    max_capital(2, 0, [1, 2, 3], [0, 1, 1]) == 4"""
    raise NotImplementedError


def max_on_time(tasks):
    """tasks: (duration, deadline) pairs. Run chosen tasks one after another
    starting at time 0; a task is on time if it finishes at or before its
    deadline. Return the largest number of tasks that can all be on time.
    O(n log n). max_on_time([(100, 200), (200, 1300), (1000, 1250), (2000, 3200)]) == 3"""
    raise NotImplementedError


def fractional_best(items, capacity):
    """items: (value, weight) pairs, weight > 0. You may take any fraction of
    each item, using at most `capacity` total weight. Return the largest total
    value as an exact fractions.Fraction.
    fractional_best([(60, 10), (100, 20), (120, 30)], 50) == 240"""
    raise NotImplementedError


# ---------------------------------------------------------------- tests (don't edit)

def _rand_intervals(rng, n, lo=0, hi=20, max_len=6):
    out = []
    for _ in range(n):
        s = rng.randint(lo, hi)
        out.append([s, s + rng.randint(0, max_len)])
    return out


def _rand_half_open(rng, n):
    return [[s, s + rng.randint(1, 5)] for s in (rng.randint(0, 15) for _ in range(n))]


def _rand_disjoint(rng):
    pts = sorted(rng.sample(range(30), 2 * rng.randint(0, 4)))
    return [[pts[i], pts[i + 1]] for i in range(0, len(pts), 2)]


def _brute_merge(ivs):
    ivs = [list(iv) for iv in ivs]
    merged = True
    while merged:
        merged = False
        for i, j in combinations(range(len(ivs)), 2):
            a, b = ivs[i], ivs[j]
            if a[0] <= b[1] and b[0] <= a[1]:
                ivs[i] = [min(a[0], b[0]), max(a[1], b[1])]
                del ivs[j]
                merged = True
                break
    return sorted(ivs)


def _brute_disjoint(ivs):
    for r in range(len(ivs), 0, -1):
        for combo in combinations(ivs, r):
            if all(a[1] <= b[0] or b[1] <= a[0] for a, b in combinations(combo, 2)):
                return r
    return 0


def _brute_stab(ivs):
    ends = sorted({e for _, e in ivs})
    for r in range(1, len(ends) + 1):
        for pts in combinations(ends, r):
            if all(any(s <= p <= e for p in pts) for s, e in ivs):
                return r
    return 0


def _bfs_jumps(steps):
    n = len(steps)
    dist = [-1] * n
    dist[0] = 0
    q = deque([0])
    while q:
        i = q.popleft()
        for j in range(i + 1, min(n, i + steps[i] + 1)):
            if dist[j] == -1:
                dist[j] = dist[i] + 1
                q.append(j)
    return dist[-1]


def _loop_ok(gas, cost, start):
    tank, n = 0, len(gas)
    for k in range(n):
        i = (start + k) % n
        tank += gas[i] - cost[i]
        if tank < 0:
            return False
    return True


def _brute_schedule(tasks, gap):
    labels = sorted(set(tasks))
    start = tuple((tasks.count(lab), 0) for lab in labels)
    frontier, seen, slots = {start}, {start}, 0
    while frontier:
        if any(all(c == 0 for c, _ in state) for state in frontier):
            return slots
        nxt = set()
        for state in frontier:
            cooled = [(c, max(0, wait - 1)) for c, wait in state]
            nxt.add(tuple(cooled))
            for k, (c, wait) in enumerate(state):
                if c and wait == 0:
                    ran = list(cooled)
                    ran[k] = (c - 1, gap)
                    nxt.add(tuple(ran))
        frontier = nxt - seen
        seen |= frontier
        slots += 1


def _brute_capital(k, capital, profits, needs):
    best = capital

    def go(cap, left, used):
        nonlocal best
        best = max(best, cap)
        if left:
            for i in range(len(profits)):
                if i not in used and needs[i] <= cap:
                    go(cap + profits[i], left - 1, used | {i})

    go(capital, k, frozenset())
    return best


def _brute_on_time(tasks):
    for r in range(len(tasks), 0, -1):
        for combo in combinations(tasks, r):
            t = 0
            for dur, deadline in sorted(combo, key=lambda x: x[1]):
                t += dur
                if t > deadline:
                    break
            else:
                return r
    return 0


def test_merge_intervals():
    assert merge_intervals([[1, 3], [8, 10], [2, 6], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
    assert merge_intervals([[1, 4], [4, 5]]) == [[1, 5]], "touching closed intervals merge"
    assert merge_intervals([[1, 10], [2, 3]]) == [[1, 10]], "keep the max end, not the latest end"
    assert merge_intervals([]) == []
    data = [(5, 6), (1, 2)]
    assert merge_intervals(data) == [[1, 2], [5, 6]]
    assert data == [(5, 6), (1, 2)], "don't sort the caller's list in place"
    rng = random.Random(29)
    for _ in range(200):
        ivs = _rand_intervals(rng, rng.randint(0, 7))
        assert merge_intervals(ivs) == _brute_merge(ivs), ivs


def test_insert_interval():
    assert insert_interval([[1, 3], [6, 9]], [2, 5]) == [[1, 5], [6, 9]]
    assert insert_interval([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]) == [[1, 2], [3, 10], [12, 16]]
    assert insert_interval([], [5, 7]) == [[5, 7]]
    assert insert_interval([[1, 5]], [6, 8]) == [[1, 5], [6, 8]]
    assert insert_interval([[3, 5]], [1, 2]) == [[1, 2], [3, 5]]
    assert insert_interval([[1, 2], [5, 6]], [2, 5]) == [[1, 6]], "touching closed intervals merge"
    rng = random.Random(29)
    for _ in range(200):
        base = _brute_merge(_rand_intervals(rng, rng.randint(0, 6)))
        s = rng.randint(0, 25)
        new = [s, s + rng.randint(0, 6)]
        assert insert_interval(base, new) == _brute_merge(base + [new]), (base, new)


def test_intersect_lists():
    a = [[0, 2], [5, 10], [13, 23], [24, 25]]
    b = [[1, 5], [8, 12], [15, 24], [25, 26]]
    assert intersect_lists(a, b) == [[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]]
    assert intersect_lists([], [[1, 2]]) == []
    assert intersect_lists([[1, 7]], [[3, 10]]) == [[3, 7]]
    rng = random.Random(29)
    for _ in range(200):
        a, b = _rand_disjoint(rng), _rand_disjoint(rng)
        want = sorted([max(x[0], y[0]), min(x[1], y[1])] for x in a for y in b
                      if max(x[0], y[0]) <= min(x[1], y[1]))
        assert intersect_lists(a, b) == want, (a, b)


def test_max_non_overlapping():
    assert max_non_overlapping([[1, 2], [2, 3], [3, 4], [1, 3]]) == 3, "half-open: [1, 2) and [2, 3) don't overlap"
    assert max_non_overlapping([[1, 10], [2, 3], [4, 5]]) == 2, "sort by END, not by start"
    assert max_non_overlapping([]) == 0
    rng = random.Random(29)
    for _ in range(150):
        ivs = _rand_half_open(rng, rng.randint(0, 8))
        assert max_non_overlapping(ivs) == _brute_disjoint(ivs), ivs


def test_min_points_to_stab():
    assert min_points_to_stab([[10, 16], [2, 8], [1, 6], [7, 12]]) == 2
    assert min_points_to_stab([[1, 2], [2, 3]]) == 1, "closed intervals: the point 2 hits both"
    assert min_points_to_stab([[1, 2], [3, 4]]) == 2
    assert min_points_to_stab([[1, 10], [2, 3], [4, 5]]) == 2, "sort by END, not by start"
    assert min_points_to_stab([]) == 0
    rng = random.Random(29)
    for _ in range(150):
        ivs = _rand_intervals(rng, rng.randint(1, 7))
        assert min_points_to_stab(ivs) == _brute_stab(ivs), ivs


def test_min_rooms():
    assert min_rooms([[0, 30], [5, 10], [15, 20]]) == 2
    assert min_rooms([[7, 10], [2, 4]]) == 1
    assert min_rooms([[1, 5], [5, 10]]) == 1, "a meeting ending at 5 frees its room for one starting at 5"
    assert min_rooms([]) == 0
    rng = random.Random(29)
    for _ in range(200):
        ivs = _rand_half_open(rng, rng.randint(0, 9))
        want = max((sum(s <= t < e for s, e in ivs) for t, _ in ivs), default=0)
        assert min_rooms(ivs) == want, ivs


def test_max_coverage():
    assert max_coverage([[1, 2], [2, 3]]) == 2, "closed intervals touching at 2 both cover it: count starts before ends"
    assert max_coverage([[1, 3], [4, 6]]) == 1
    assert max_coverage([[1, 10], [2, 3], [3, 4], [3, 3]]) == 4
    assert max_coverage([]) == 0
    rng = random.Random(29)
    for _ in range(200):
        ivs = _rand_intervals(rng, rng.randint(0, 9))
        want = max((sum(s <= t <= e for s, e in ivs) for t, _ in ivs), default=0)
        assert max_coverage(ivs) == want, ivs


def test_can_reach_end():
    assert can_reach_end([2, 3, 1, 1, 4]) is True
    assert can_reach_end([3, 2, 1, 0, 4]) is False
    assert can_reach_end([0]) is True
    assert can_reach_end([1, 0, 1]) is False
    rng = random.Random(29)
    for _ in range(300):
        steps = [rng.randint(0, 3) for _ in range(rng.randint(1, 9))]
        assert can_reach_end(steps) is (_bfs_jumps(steps) != -1), steps


def test_min_jumps():
    assert min_jumps([2, 3, 1, 1, 4]) == 2
    assert min_jumps([2, 3, 0, 1, 4]) == 2
    assert min_jumps([0]) == 0
    assert min_jumps([1, 0, 2]) == -1
    assert min_jumps([1, 1, 1, 1]) == 3
    rng = random.Random(29)
    for _ in range(300):
        steps = [rng.randint(0, 3) for _ in range(rng.randint(1, 9))]
        assert min_jumps(steps) == _bfs_jumps(steps), steps


def test_loop_start():
    assert loop_start([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]) == 3
    assert loop_start([2, 3, 4], [3, 4, 3]) == -1
    assert loop_start([5], [5]) == 0
    assert loop_start([1, 1, 1], [1, 1, 1]) == 0, "return the smallest valid start"
    rng = random.Random(29)
    for _ in range(300):
        n = rng.randint(1, 7)
        gas = [rng.randint(0, 5) for _ in range(n)]
        cost = [rng.randint(0, 5) for _ in range(n)]
        want = next((s for s in range(n) if _loop_ok(gas, cost, s)), -1)
        assert loop_start(gas, cost) == want, (gas, cost)


def test_schedule_length():
    assert schedule_length('AAABBB', 2) == 8
    assert schedule_length('AAABBB', 0) == 6
    assert schedule_length('AAAAAABCDEFG', 2) == 16
    assert schedule_length('', 3) == 0
    assert schedule_length('ABC', 5) == 3, "different labels never wait for each other"
    assert schedule_length('AABBCCDD', 1) == 8, "enough variety fills every gap: the answer is at least len(tasks)"
    rng = random.Random(29)
    for _ in range(120):
        tasks = ''.join(rng.choice('ABC') for _ in range(rng.randint(0, 6)))
        gap = rng.randint(0, 3)
        assert schedule_length(tasks, gap) == _brute_schedule(tasks, gap), (tasks, gap)


def test_max_capital():
    assert max_capital(2, 0, [1, 2, 3], [0, 1, 1]) == 4
    assert max_capital(3, 0, [1, 2, 3], [0, 1, 2]) == 6
    assert max_capital(1, 0, [5], [1]) == 0, "can't afford anything: capital stays"
    assert max_capital(0, 7, [5], [0]) == 7
    rng = random.Random(29)
    for _ in range(200):
        n = rng.randint(0, 6)
        profits = [rng.randint(0, 6) for _ in range(n)]
        needs = [rng.randint(0, 8) for _ in range(n)]
        k, start = rng.randint(0, 3), rng.randint(0, 4)
        want = _brute_capital(k, start, profits, needs)
        assert max_capital(k, start, profits, needs) == want, (k, start, profits, needs)


def test_max_on_time():
    assert max_on_time([(100, 200), (200, 1300), (1000, 1250), (2000, 3200)]) == 3
    assert max_on_time([(1, 2)]) == 1
    assert max_on_time([(3, 2), (4, 3)]) == 0
    assert max_on_time([]) == 0
    assert max_on_time([(5, 5), (4, 6), (2, 6)]) == 2, "when you're past a deadline, drop the LONGEST task so far"
    rng = random.Random(29)
    for _ in range(200):
        tasks = [(rng.randint(1, 5), rng.randint(1, 12)) for _ in range(rng.randint(0, 7))]
        assert max_on_time(tasks) == _brute_on_time(tasks), tasks


def test_fractional_best():
    assert fractional_best([(60, 10), (100, 20), (120, 30)], 50) == 240
    assert fractional_best([(1, 3), (2, 3)], 4) == Fraction(7, 3)
    assert fractional_best([(5, 1)], 0) == 0
    assert fractional_best([], 10) == 0
    assert fractional_best([(10, 2)], 100) == 10, "you can't take more than the whole item"
    assert isinstance(fractional_best([(1, 3)], 1), Fraction), "return a Fraction"
    big = 10 ** 17
    assert fractional_best([(1, 1), (big + 1, big)], big) == big + 1, \
        "sort by the exact ratio (Fraction or cross-multiplying), not float division"
