"""R32 - Pattern recognition

Read the constraints before the story: they set the target complexity (n <= 20
allows exponential, n <= 10**5 needs O(n log n) or better, a lone number up to
10**18 needs O(log n)). Then match signals in the statement to patterns, and
check the template's false triggers before you commit: a shrinking window breaks
on negatives, Dijkstra on negative edges, BFS on weighted edges, binary search
on a non-monotone check, greedy without an exchange argument. Keep your own
signal -> pattern table in work/triggers.md and grow it after every problem.

Part 1 - Predict. Each block in PREDICT is a REPL session. Replace every ???
with exactly what Python prints: expression values are echoed the way the REPL
echoes them, and a line that raises prints just the exception name (TypeError).

Part 2 - Quiz. Replace every ??? in QUIZ: complexities like O(n log n), and
short pattern names like "sliding window" or "union find".

Part 3 - Mixed review. Each problem below needs a different pattern, and the
docstrings don't say which: name it before you code it. The timed tests use the
sizes stated in each docstring, so brute force won't pass. Implement them until
`python check.py 32` is green; don't edit the tests at the bottom.

Unlocks: the first step of every new problem, which is seeing which template it is.
"""
import math
import random
import sys
import time
from collections import Counter, deque
from itertools import combinations

PREDICT = r"""
>>> def window_count(nums, k):
...     left = total = count = 0
...     for right, x in enumerate(nums):
...         total += x
...         while total > k and left <= right:
...             total -= nums[left]
...             left += 1
...         count += total == k
...     return count
>>> window_count([1, 2, 3], 3), window_count([1, -1, 1, 2], 2)
???

>>> def prefix_count(nums, k):
...     seen, total, count = Counter({0: 1}), 0, 0
...     for x in nums:
...         total += x
...         count += seen[total - k]
...         seen[total] += 1
...     return count
>>> prefix_count([1, -1, 1, 2], 2)
???

>>> def dijkstra(adj, src):
...     dist, done, pq = {src: 0}, set(), [(0, src)]
...     while pq:
...         d, u = heappop(pq)
...         if u in done:
...             continue
...         done.add(u)
...         for v, w in adj[u]:
...             if v not in done and d + w < dist.get(v, math.inf):
...                 dist[v] = d + w
...                 heappush(pq, (d + w, v))
...     return dist
>>> adj = {'a': [('b', 1), ('c', 5)], 'b': [('d', 1)], 'c': [('b', -10)], 'd': []}
>>> dijkstra(adj, 'a')
???
>>> dist = {v: math.inf for v in adj}
>>> dist['a'] = 0
>>> for _ in range(len(adj) - 1):
...     for u in adj:
...         for v, w in adj[u]:
...             dist[v] = min(dist[v], dist[u] + w)
>>> dist
???

>>> adj = {'s': [('t', 10), ('m', 1)], 'm': [('t', 1)], 't': []}
>>> dist, q = {'s': 0}, deque(['s'])
>>> while q:
...     u = q.popleft()
...     for v, w in adj[u]:
...         if v not in dist:
...             dist[v] = dist[u] + w
...             q.append(v)
>>> dist['t']
???

>>> def greedy(coins, amount):
...     count = 0
...     for c in sorted(coins, reverse=True):
...         count += amount // c
...         amount %= c
...     return count
>>> greedy([1, 5, 6, 9], 11)
???
>>> best = [0] + [math.inf] * 11
>>> for a in range(1, 12):
...     best[a] = min(best[a - c] + 1 for c in [1, 5, 6, 9] if c <= a)
>>> best[11]
???

>>> ok = [False, True, False, True, True]
>>> lo, hi = 0, len(ok) - 1
>>> while lo < hi:
...     mid = (lo + hi) // 2
...     if ok[mid]:
...         hi = mid
...     else:
...         lo = mid + 1
>>> lo, ok.index(True)
???

>>> def pair_sum(nums, target):
...     i, j = 0, len(nums) - 1
...     while i < j:
...         s = nums[i] + nums[j]
...         if s == target:
...             return True
...         if s < target:
...             i += 1
...         else:
...             j -= 1
...     return False
>>> pair_sum([1, 4, 2, 3], 5), pair_sum([5, 1, 9, 2], 14), pair_sum(sorted([5, 1, 9, 2]), 14)
???

>>> def best_sum(nums):
...     best = cur = 0
...     for x in nums:
...         cur = max(0, cur + x)
...         best = max(best, cur)
...     return best
>>> best_sum([2, -1, 3]), best_sum([-3, -1, -2])
???

>>> adj = {'a': ['b'], 'b': ['c'], 'c': ['b']}
>>> indeg = Counter(v for vs in adj.values() for v in vs)
>>> q = deque(u for u in adj if indeg[u] == 0)
>>> order = []
>>> while q:
...     u = q.popleft()
...     order.append(u)
...     for v in adj[u]:
...         indeg[v] -= 1
...         if indeg[v] == 0:
...             q.append(v)
>>> order, len(order) == len(adj)
???

>>> h = []
>>> for x in [5, 1, 9, 3, 7]:
...     heappush(h, x)
...     if len(h) > 3:
...         _ = heappop(h)
>>> h[0], sorted(h)
???

>>> n = 10**5
>>> n * n, n * n.bit_length()
???
>>> 2 ** 20 * 20, math.factorial(11)
???
"""

QUIZ = {
    "constraint: n <= 10": "???",
    "constraint: n <= 20": "???",
    "constraint: n <= 40": "???",
    "constraint: n <= 500": "???",
    "constraint: n <= 5000": "???",
    "constraint: n <= 10**6": "???",
    "constraint: a single number n up to 10**9": "???",
    "constraint: a single number n up to 10**18": "???",
    "signal: sorted array, find a pair with a target sum in O(1) extra space": "???",
    "signal: longest substring with at most k distinct characters": "???",
    "signal: count subarrays that sum to k, values can be negative": "???",
    "signal: many updates that add v to a range [l, r], then read the final array": "???",
    "signal: smallest capacity that lets the work finish within d days": "???",
    "signal: for every element, the next element to its right that is greater": "???",
    "signal: maximum of every window of size k": "???",
    "signal: k-th largest element of a stream": "???",
    "signal: running median of a stream": "???",
    "signal: fewest moves on a grid where every move costs the same": "???",
    "signal: cheapest path when edge weights are non-negative and differ": "???",
    "signal: shortest path when every edge costs 0 or 1": "???",
    "signal: connections arrive one at a time; are a and b connected yet?": "???",
    "signal: tasks with prerequisites, find an order that works": "???",
    "signal: generate every subset or permutation": "???",
    "signal: count the ways to reach a total when choices overlap": "???",
    "signal: fewest single-character edits that turn one string into another": "???",
    "signal: all dictionary words that start with a given prefix": "???",
    "signal: fewest rooms so that no two overlapping meetings share one": "???",
    "signal: the middle node of a linked list in one pass": "???",
    "signal: every value appears twice except one": "???",
    "signal: range-sum queries mixed with point updates": "???",
    "signal: group the words that are anagrams of each other": "???",
    "signal: n <= 20 items, pick the best subset where the items interact": "???",
    "false trigger: a shrinking sliding window breaks when the array has ...": "???",
    "false trigger: Dijkstra gives wrong answers when the graph has ...": "???",
    "false trigger: plain BFS gives wrong shortest paths when edges have ...": "???",
    "false trigger: binary search on the answer needs the feasibility check to be ...": "???",
    "false trigger: before trusting a greedy choice, prove it with an ...": "???",
    "false trigger: two pointers from both ends needs the array to be ...": "???",
    "false trigger: a topological order exists only if the graph has no ...": "???",
    "false trigger: memoization only pays off when subproblems ...": "???",
    "false trigger: resetting a running sum to 0 is wrong when the chosen run must be ...": "???",
    "false trigger: to keep the k largest values seen so far, the size-k heap must be a ...": "???",
}


# ---------------------------------------------------------------- mixed review

def closest_pair_gap(nums, target):
    """nums is sorted ascending (len >= 2). Return the smallest
    |nums[i] + nums[j] - target| over index pairs i < j.
    closest_pair_gap([1, 3, 4, 7, 10], 15) == 1     # 4 + 10
    n up to 10**5; timed at 10,000."""
    raise NotImplementedError


def shortest_reaching(nums, s):
    """nums holds positive integers and s >= 1. Return the length of the
    shortest contiguous run whose sum is at least s, or 0 if there's none.
    shortest_reaching([2, 3, 1, 2, 4, 3], 7) == 2    # [4, 3]
    n up to 10**5; timed at 30,000."""
    raise NotImplementedError


def count_divisible(nums, k):
    """Count the non-empty contiguous runs whose sum is divisible by k (k >= 1;
    values can be negative). count_divisible([4, 5, 0, -2, -3, 1], 5) == 7
    n up to 10**5; timed at 15,000."""
    raise NotImplementedError


def smallest_max_split(nums, m):
    """Cut nums (non-empty, non-negative) into at most m contiguous non-empty
    pieces so that the largest piece sum is as small as possible; return it.
    smallest_max_split([7, 2, 5, 10, 8], 2) == 18    # [7, 2, 5] + [10, 8]
    n up to 10**5; timed at 2,000 numbers with m = 20."""
    raise NotImplementedError


def steps_to_larger(nums):
    """For each position, return how many steps to the right you must go to
    reach a strictly larger value (0 if there's none).
    steps_to_larger([3, 4, 5, 1, 0, 2, 6, 3]) == [1, 1, 4, 2, 1, 1, 0, 0]
    n up to 10**5; timed at 25,000."""
    raise NotImplementedError


def fewest_moves(grid):
    """grid is a list of equal-length strings of '.' (open) and '#' (wall).
    Moving up, down, left or right between open cells, return the fewest moves
    from the top-left cell to the bottom-right cell, or -1 if you can't get
    there (including when either end is a wall).
    fewest_moves(['..#', '#..', '...']) == 4
    Grids up to 1000 x 1000; timed at 301 x 301."""
    raise NotImplementedError


def count_groups(n, pairs):
    """People 0..n-1. Each pair (a, b) says a and b are in the same group, and
    "same group" is transitive. Return the number of groups.
    count_groups(5, [(0, 1), (1, 2), (3, 4)]) == 2
    n and len(pairs) up to 10**5; timed at 50,000 people, one group a long chain."""
    raise NotImplementedError


def valid_order(n, before):
    """Tasks 0..n-1 (n >= 1). Each pair (a, b) in `before` says a must happen
    before b. Return all n tasks in an order that satisfies every pair (any such
    order), or [] if none exists. valid_order(3, [(0, 1), (0, 2), (1, 2)]) == [0, 1, 2]
    n up to 10**5; timed at 30,000 tasks with 60,000 pairs, including a long chain."""
    raise NotImplementedError


def best_non_adjacent(nums):
    """Pick any set of positions with no two next to each other (picking none is
    allowed) and return the largest possible sum of the picked values.
    best_non_adjacent([2, 7, 9, 3, 1]) == 12    # 2 + 9 + 1
    n up to 10**5; timed at 100,000."""
    raise NotImplementedError


def prefix_counts(words, prefixes):
    """For each string in `prefixes`, count how many of `words` start with it
    (duplicate words count separately).
    prefix_counts(['apple', 'app', 'bat'], ['ap', 'b', 'c', 'apple']) == [2, 1, 0, 1]
    Up to 10**5 words and prefixes; timed at 10,000 of each."""
    raise NotImplementedError


# ---------------------------------------------------------------- tests (don't edit)

_BUDGET = 0.5   # seconds; reasonable solutions take a few milliseconds


def _timed(fn, *args):
    start = time.perf_counter()
    result = fn(*args)
    return result, time.perf_counter() - start


def _assert_fast(secs, hint):
    assert secs < _BUDGET, f"{secs:.2f}s against a {_BUDGET}s budget: {hint}"


def _deep(fn, *args):
    """Call fn at the default recursion limit; turn RecursionError into a clear failure."""
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(1000)
    try:
        return fn(*args)
    except RecursionError:
        raise AssertionError("RecursionError at the default limit: rewrite it with a loop or an explicit stack") from None
    finally:
        sys.setrecursionlimit(old)


def _brute_split(nums, m):
    n, best = len(nums), sum(nums)
    for pieces in range(1, min(m, n) + 1):
        for cuts in combinations(range(1, n), pieces - 1):
            bounds = (0, *cuts, n)
            best = min(best, max(sum(nums[a:b]) for a, b in zip(bounds, bounds[1:])))
    return best


def _brute_moves(grid):
    R, C = len(grid), len(grid[0])
    dist = {(r, c): math.inf for r in range(R) for c in range(C) if grid[r][c] == '.'}
    if (0, 0) not in dist or (R - 1, C - 1) not in dist:
        return -1
    dist[(0, 0)] = 0
    for _ in range(len(dist)):
        for (r, c), d in list(dist.items()):
            for nb in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if nb in dist and d + 1 < dist[nb]:
                    dist[nb] = d + 1
    d = dist[(R - 1, C - 1)]
    return -1 if d == math.inf else d


def _brute_groups(n, pairs):
    groups = [{i} for i in range(n)]
    for a, b in pairs:
        ga = next(g for g in groups if a in g)
        gb = next(g for g in groups if b in g)
        if ga is not gb:
            groups.remove(gb)
            ga |= gb
    return len(groups)


def _check_order(n, before, order):
    if sorted(order) != list(range(n)):
        return False
    pos = {v: i for i, v in enumerate(order)}
    return all(pos[a] < pos[b] for a, b in before)


def _has_cycle(n, before):
    reach = [[False] * n for _ in range(n)]
    for a, b in before:
        reach[a][b] = True
    for k in range(n):
        for i in range(n):
            if reach[i][k]:
                for j in range(n):
                    if reach[k][j]:
                        reach[i][j] = True
    return any(reach[i][i] for i in range(n))


def test_closest_pair_gap():
    assert closest_pair_gap([1, 3, 4, 7, 10], 15) == 1
    assert closest_pair_gap([1, 2], 3) == 0
    assert closest_pair_gap([-5, 0, 5], 100) == 95
    assert closest_pair_gap([2, 2, 2], 4) == 0
    rng = random.Random(32)
    for _ in range(200):
        nums = sorted(rng.randint(-20, 20) for _ in range(rng.randint(2, 9)))
        t = rng.randint(-45, 45)
        want = min(abs(a + b - t) for a, b in combinations(nums, 2))
        assert closest_pair_gap(nums, t) == want, (nums, t)
    big = sorted(rng.choices(range(10 ** 9), k=10_000))
    _, secs = _timed(closest_pair_gap, big, 10 ** 9 + 7)
    _assert_fast(secs, "10,000 sorted numbers: checking every pair is too slow; aim for O(n)")


def test_shortest_reaching():
    assert shortest_reaching([2, 3, 1, 2, 4, 3], 7) == 2
    assert shortest_reaching([1, 4, 4], 4) == 1
    assert shortest_reaching([1, 1, 1], 5) == 0
    assert shortest_reaching([5], 5) == 1
    rng = random.Random(32)
    for _ in range(200):
        nums = [rng.randint(1, 9) for _ in range(rng.randint(1, 10))]
        s = rng.randint(1, 40)
        lengths = [j - i for i in range(len(nums)) for j in range(i + 1, len(nums) + 1) if sum(nums[i:j]) >= s]
        assert shortest_reaching(nums, s) == min(lengths, default=0), (nums, s)
    big = rng.choices(range(1, 100), k=30_000)
    _, secs = _timed(shortest_reaching, big, sum(big) // 3)
    _assert_fast(secs, "30,000 values: trying every start is too slow; aim for O(n)")


def test_count_divisible():
    assert count_divisible([4, 5, 0, -2, -3, 1], 5) == 7
    assert count_divisible([5], 9) == 0
    assert count_divisible([-1, 2, 9], 2) == 2, "negative sums can be divisible too"
    assert count_divisible([0, 0], 3) == 3
    rng = random.Random(32)
    for _ in range(200):
        nums = [rng.randint(-9, 9) for _ in range(rng.randint(1, 10))]
        k = rng.randint(1, 6)
        want = sum(sum(nums[i:j]) % k == 0 for i in range(len(nums)) for j in range(i + 1, len(nums) + 1))
        assert count_divisible(nums, k) == want, (nums, k)
    big = rng.choices(range(-100, 100), k=15_000)
    _, secs = _timed(count_divisible, big, 7)
    _assert_fast(secs, "15,000 values: checking every run is O(n^2); aim for O(n)")


def test_smallest_max_split():
    assert smallest_max_split([7, 2, 5, 10, 8], 2) == 18
    assert smallest_max_split([1, 2, 3, 4, 5], 2) == 9
    assert smallest_max_split([1, 4, 4], 3) == 4
    assert smallest_max_split([5, 1], 5) == 5, "more pieces allowed than numbers: every number alone"
    assert smallest_max_split([0, 0, 0], 1) == 0
    rng = random.Random(32)
    for _ in range(150):
        nums = [rng.randint(0, 9) for _ in range(rng.randint(1, 8))]
        m = rng.randint(1, 4)
        assert smallest_max_split(nums, m) == _brute_split(nums, m), (nums, m)
    big = rng.choices(range(10 ** 4), k=2_000)
    _, secs = _timed(smallest_max_split, big, 20)
    _assert_fast(secs, "2,000 numbers in 20 pieces: an O(m * n^2) table is too slow; aim for about O(n log n)")


def test_steps_to_larger():
    assert steps_to_larger([3, 4, 5, 1, 0, 2, 6, 3]) == [1, 1, 4, 2, 1, 1, 0, 0]
    assert steps_to_larger([]) == []
    assert steps_to_larger([2, 2, 2]) == [0, 0, 0], "equal isn't larger"
    rng = random.Random(32)
    for _ in range(200):
        nums = [rng.randint(0, 5) for _ in range(rng.randint(0, 10))]
        want = [next((j - i for j in range(i + 1, len(nums)) if nums[j] > x), 0) for i, x in enumerate(nums)]
        assert steps_to_larger(nums) == want, nums
    big = list(range(25_000, 0, -1))
    _, secs = _timed(steps_to_larger, big)
    _assert_fast(secs, "25,000 values: scanning right from every position is O(n^2); aim for O(n)")


def test_fewest_moves():
    assert fewest_moves(['..#', '#..', '...']) == 4
    assert fewest_moves(['.']) == 0
    assert fewest_moves(['.#', '#.']) == -1
    assert fewest_moves(['#.', '..']) == -1, "a wall at the start means there's no path"
    assert fewest_moves(['....', '###.', '....', '.###', '....']) == 13
    assert fewest_moves(['..', '#.', '..', '..', '..']) == 5, \
        "that's a path but not the shortest: expand cells in order of their distance"
    rng = random.Random(32)
    for _ in range(150):
        rows, cols = rng.randint(1, 6), rng.randint(1, 6)
        grid = [''.join(rng.choice('...#') for _ in range(cols)) for _ in range(rows)]
        assert fewest_moves(grid) == _brute_moves(grid), grid
    n = 301
    grid = []
    for r in range(n):          # a snake: every other row is a wall with one gap, alternating sides
        if r % 4 == 1:
            grid.append('#' * (n - 1) + '.')
        elif r % 4 == 3:
            grid.append('.' + '#' * (n - 1))
        else:
            grid.append('.' * n)
    moves, secs = _timed(fewest_moves, grid)
    assert moves == 45_600, moves
    _assert_fast(secs, "a 301 x 301 grid: aim for O(rows * cols)")


def test_count_groups():
    assert count_groups(5, [(0, 1), (1, 2), (3, 4)]) == 2
    assert count_groups(3, []) == 3
    assert count_groups(1, [(0, 0)]) == 1
    assert count_groups(4, [(0, 1), (2, 3), (1, 2), (0, 3)]) == 1
    rng = random.Random(32)
    for _ in range(150):
        n = rng.randint(1, 10)
        pairs = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 8))]
        assert count_groups(n, pairs) == _brute_groups(n, pairs), (n, pairs)
    n = 50_000
    people = list(range(n))
    rng.shuffle(people)
    chain, rest = people[:20_000], people[20_000:]
    pairs = list(zip(chain, chain[1:]))                    # one group is a 20,000-long chain
    for i in range(0, len(rest), 3):                       # the other 30,000 form groups of three
        a, b, c = rest[i:i + 3]
        pairs += [(a, b), (c, b)]
    rng.shuffle(pairs)
    groups, secs = _timed(_deep, count_groups, n, pairs)
    assert groups == 10_001, groups
    _assert_fast(secs, "50,000 people: aim for about O(n + pairs)")


def test_valid_order():
    assert valid_order(3, [(0, 1), (0, 2), (1, 2)]) == [0, 1, 2]
    assert valid_order(2, [(0, 1), (1, 0)]) == []
    assert valid_order(1, [(0, 0)]) == [], "a task can't come before itself"
    order = valid_order(4, [(3, 1), (2, 1)])
    assert _check_order(4, [(3, 1), (2, 1)], order), order
    rng = random.Random(32)
    for _ in range(200):
        n = rng.randint(1, 7)
        before = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 8))]
        order = valid_order(n, before)
        if _has_cycle(n, before):
            assert order == [], (n, before)
        else:
            assert _check_order(n, before, order), (n, before, order)
    n = 30_000
    before = [(i, i + 1) for i in range(14_999)]                     # tasks 0..14,999 form one long chain
    rest = list(range(15_000, n))
    rng.shuffle(rest)                                                 # the rest: random pairs in a hidden order
    before += [(rest[i], rest[j]) for i, j in (sorted(rng.sample(range(len(rest)), 2)) for _ in range(45_000))]
    rng.shuffle(before)
    order, secs = _timed(_deep, valid_order, n, before)
    assert _check_order(n, before, order), "not a valid order"
    _assert_fast(secs, "30,000 tasks: aim for O(n + pairs)")


def test_best_non_adjacent():
    assert best_non_adjacent([2, 7, 9, 3, 1]) == 12
    assert best_non_adjacent([]) == 0
    assert best_non_adjacent([-3, -1]) == 0, "picking nothing is allowed"
    assert best_non_adjacent([5, 1, 1, 5]) == 10
    rng = random.Random(32)
    for _ in range(200):
        nums = [rng.randint(-5, 9) for _ in range(rng.randint(0, 9))]
        n = len(nums)
        want = max(sum(nums[i] for i in range(n) if mask >> i & 1)
                   for mask in range(1 << n) if not mask & (mask >> 1))
        assert best_non_adjacent(nums) == want, nums
    best, secs = _timed(_deep, best_non_adjacent, [1, 3] * 50_000)
    assert best == 150_000, best
    _assert_fast(secs, "100,000 values: aim for O(n)")


def test_prefix_counts():
    assert prefix_counts(['apple', 'app', 'bat'], ['ap', 'b', 'c', 'apple']) == [2, 1, 0, 1]
    assert prefix_counts([], ['a']) == [0]
    assert prefix_counts(['a', 'a'], ['a', 'aa']) == [2, 0], "duplicate words count separately"
    assert prefix_counts(['abc'], ['']) == [1], "every word starts with the empty string"
    rng = random.Random(32)
    for _ in range(150):
        words = [''.join(rng.choices('ab', k=rng.randint(0, 4))) for _ in range(rng.randint(0, 8))]
        prefixes = [''.join(rng.choices('ab', k=rng.randint(0, 3))) for _ in range(5)]
        want = [sum(w.startswith(p) for w in words) for p in prefixes]
        assert prefix_counts(words, prefixes) == want, (words, prefixes)
    words = [''.join(rng.choices('abcd', k=rng.randint(1, 8))) for _ in range(10_000)]
    prefixes = [''.join(rng.choices('abcd', k=rng.randint(1, 4))) for _ in range(10_000)]
    got, secs = _timed(prefix_counts, words, prefixes)
    assert got[:50] == [sum(w.startswith(p) for w in words) for p in prefixes[:50]]
    _assert_fast(secs, "10,000 words x 10,000 prefixes: comparing every pair is too slow")
