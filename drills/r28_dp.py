"""R28 - Dynamic programming

Ritual for every DP: (1) the state in words, (2) the recurrence, (3) base cases,
(4) evaluation order, (5) where the answer lives, (6) complexity = states x
transitions. Write each drill three ways: @cache top-down, a bottom-up table,
then a rolling version that keeps only the rows it needs. 0/1 knapsack loops
capacity DOWNWARD (each item once); unbounded loops upward. Counting coin
combinations puts the coin loop outside the amount loop. LIS in O(n log n)
keeps `tails` with bisect_left. Two-string DPs use an (n + 1) x (m + 1) table
with an empty-prefix row and column. Python specifics: @cache needs hashable
arguments and recursion deeper than ~1000 frames raises RecursionError, so
finish deep DPs bottom-up; start min-DPs at math.inf; apply % MOD every step.

Part 1 - Predict. Each block in PREDICT is a REPL session. Replace every ???
with exactly what Python prints: expression values are echoed the way the REPL
echoes them, and a line that raises prints just the exception name (TypeError).

Part 2 - Drills. Implement every function until `python check.py 28` is green.
Don't edit the tests at the bottom; add your own test_* functions if you like.

Unlocks: counting ways, min cost / max value with overlapping choices, take-or-
skip, knapsack, increasing runs, two-string alignment, intervals, bitmask tours,
tree choices, and buy/sell state machines.
"""

PREDICT = r"""
>>> @cache
... def f(xs):
...     return len(xs)
>>> f((1, 2))
???
>>> f([1, 2])
???

>>> calls = 0
>>> def fib(n):
...     global calls
...     calls += 1
...     return n if n < 2 else fib(n - 1) + fib(n - 2)
>>> fib(15), calls
???

>>> calls = 0
>>> @cache
... def fib(n):
...     global calls
...     calls += 1
...     return n if n < 2 else fib(n - 1) + fib(n - 2)
>>> fib(15), calls
???
>>> fib(15), calls
???

>>> a, b = 0, 1
>>> for _ in range(10):
...     a, b = b, a + b
>>> a
???

>>> def best(weights, values, cap, downward):
...     dp = [0] * (cap + 1)
...     for w, v in zip(weights, values):
...         order = range(cap, w - 1, -1) if downward else range(w, cap + 1)
...         for c in order:
...             dp[c] = max(dp[c], dp[c - w] + v)
...     return dp[cap]
>>> best([2], [3], 6, True), best([2], [3], 6, False)
???

>>> def ways(coins, amount, coins_outside):
...     dp = [1] + [0] * amount
...     if coins_outside:
...         for c in coins:
...             for a in range(c, amount + 1):
...                 dp[a] += dp[a - c]
...     else:
...         for a in range(1, amount + 1):
...             for c in coins:
...                 if c <= a:
...                     dp[a] += dp[a - c]
...     return dp[amount]
>>> ways([1, 2], 3, True), ways([1, 2], 3, False)
???

>>> dp = [[0] * 3] * 2
>>> dp[0][1] = 5
>>> dp
???

>>> INF = float('inf')
>>> min(INF, 3), INF + 1 == INF, INF - INF
???

>>> tails = []
>>> for x in [3, 1, 4, 1, 5, 9, 2, 6]:
...     i = bisect_left(tails, x)
...     if i == len(tails):
...         tails.append(x)
...     else:
...         tails[i] = x
>>> tails, len(tails)
???

>>> def lis_len(nums, strict):
...     tails = []
...     for x in nums:
...         i = (bisect_left if strict else bisect_right)(tails, x)
...         tails[i:i + 1] = [x]
...     return len(tails)
>>> lis_len([2, 2, 2], True), lis_len([2, 2, 2], False)
???

>>> a, b = 'abc', 'ab'
>>> [list(range(len(b) + 1))] + [[i] + [0] * len(b) for i in range(1, len(a) + 1)]
???

>>> bits = 1
>>> for x in [3, 5, 9]:
...     bits |= bits << x
>>> [s for s in range(18) if bits >> s & 1]
???

>>> MOD = 10**9 + 7
>>> (MOD - 1) * 2 % MOD
???

>>> memo = {}
>>> memo[(1, 2)] = 'ok'
>>> memo[[1, 2]] = 'no'
???
>>> memo
???
"""

from bisect import bisect_left
from functools import cache
import math


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ---------------------------------------------------------------- drills

def stairs(n):
    """Ways to climb n steps (n >= 0) taking 1 or 2 steps at a time;
    stairs(0) == 1. Must handle n = 3000, where top-down recursion hits the
    recursion limit, so finish with rolling variables. stairs(4) == 5."""
    raise NotImplementedError


def max_take_skip(nums):
    """Take-or-skip: the largest sum of elements with no two taken elements
    adjacent. Taking nothing is allowed (sum 0). O(n), O(1) extra space.
    max_take_skip([2, 7, 9, 3, 1]) == 12."""
    raise NotImplementedError


def grid_paths(grid):
    """grid is a list of strings of '.' (open) and '#' (blocked). Count the
    paths from the top-left to the bottom-right cell moving only right or down
    through open cells (0 if either corner is blocked).
    grid_paths(['...', '.#.', '...']) == 2."""
    raise NotImplementedError


def min_coins(coins, amount):
    """Fewest coins (each denomination unlimited) that sum to amount, or -1 if
    impossible. min_coins([1, 2, 5], 11) == 3; min_coins([2], 3) == -1."""
    raise NotImplementedError


def coin_combinations(coins, amount):
    """How many combinations (order doesn't matter) of unlimited coins sum to
    amount? coin_combinations([1, 2], 3) == 2: {1,1,1} and {1,2}."""
    raise NotImplementedError


def knapsack_01(weights, values, cap):
    """0/1 knapsack: each item at most once; the best total value with total
    weight <= cap. One 1D table. knapsack_01([1, 3, 4, 5], [1, 4, 5, 7], 7) == 9."""
    raise NotImplementedError


def lis_length(nums):
    """Length of the longest strictly increasing subsequence, in O(n log n).
    lis_length([10, 9, 2, 5, 3, 7, 101, 18]) == 4."""
    raise NotImplementedError


def lcs(a, b):
    """Length of the longest common subsequence of strings a and b. Must
    handle 700-character strings, so finish bottom-up.
    lcs('abcde', 'ace') == 3."""
    raise NotImplementedError


def edit_distance(a, b):
    """Fewest single-character inserts, deletes, or replacements turning a
    into b. edit_distance('horse', 'ros') == 3."""
    raise NotImplementedError


def longest_pal_subseq(s):
    """Length of the longest subsequence of s that reads the same backwards.
    Interval DP over (i, j). longest_pal_subseq('bbbab') == 4."""
    raise NotImplementedError


def equal_split(nums):
    """Can nums (non-negative ints, possibly empty) be split into two groups,
    every number in exactly one, with equal sums? Must handle 40 numbers, so
    trying every subset won't finish. equal_split([1, 5, 11, 5]) is True."""
    raise NotImplementedError


def shortest_route(dist):
    """dist is an n x n matrix (1 <= n <= 10) of non-negative travel costs,
    possibly asymmetric. Return the cheapest cost to start at city 0, visit
    every other city exactly once, and return to 0. Bitmask DP dp[mask][i].
    shortest_route([[0, 1], [1, 0]]) == 2; shortest_route([[0]]) == 0."""
    raise NotImplementedError


def tree_take_skip(root):
    """Values are non-negative. Pick nodes with no picked node directly below
    another picked node; return the largest possible sum (0 for an empty
    tree). Recurse returning (best with node, best without node)."""
    raise NotImplementedError


def trade_with_cooldown(prices):
    """prices[i] is the price on day i. Hold at most one share; buy and sell
    as often as you like, but after a sale you must skip the next day before
    buying again. Return the best total profit, using hold/sold/rest states.
    trade_with_cooldown([1, 2, 3, 0, 2]) == 3."""
    raise NotImplementedError


# ---------------------------------------------------------------- tests (don't edit)

import functools as _functools
import itertools as _itertools
import random as _random
import time as _time


def _fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def _ways(n):
    if n < 0:
        return 0
    return 1 if n == 0 else _ways(n - 1) + _ways(n - 2)


def test_stairs():
    assert [stairs(n) for n in range(8)] == [1, 1, 2, 3, 5, 8, 13, 21]
    for n in range(20):
        assert stairs(n) == _ways(n), n
    try:
        big = stairs(3000)
    except RecursionError:
        raise AssertionError("RecursionError at n = 3000: finish with the bottom-up / rolling version") from None
    assert big == _fib(3001)


def test_max_take_skip():
    assert max_take_skip([2, 7, 9, 3, 1]) == 12
    assert max_take_skip([1, 2, 3, 1]) == 4
    assert max_take_skip([]) == 0
    assert max_take_skip([-5, -1]) == 0, "taking nothing is allowed"
    assert max_take_skip([5]) == 5
    rng = _random.Random(28)
    for _ in range(200):
        nums = [rng.randint(-5, 9) for _ in range(rng.randint(0, 10))]
        n = len(nums)
        want = max(sum(nums[i] for i in range(n) if m >> i & 1)
                   for m in range(1 << n) if not m & (m >> 1))
        assert max_take_skip(nums) == want, nums


def _count_paths(grid):
    rows, cols = len(grid), len(grid[0])

    def go(r, c):
        if r >= rows or c >= cols or grid[r][c] == '#':
            return 0
        if (r, c) == (rows - 1, cols - 1):
            return 1
        return go(r + 1, c) + go(r, c + 1)

    return go(0, 0)


def test_grid_paths():
    assert grid_paths(['...', '...', '...']) == 6
    assert grid_paths(['...', '.#.', '...']) == 2
    assert grid_paths(['#.']) == 0
    assert grid_paths(['.#']) == 0
    assert grid_paths(['.']) == 1
    assert grid_paths(['..', '##', '..']) == 0
    rng = _random.Random(28)
    for _ in range(100):
        rows, cols = rng.randint(1, 5), rng.randint(1, 5)
        grid = [''.join(rng.choice('...#') for _ in range(cols)) for _ in range(rows)]
        assert grid_paths(grid) == _count_paths(grid), grid
    assert grid_paths(['.' * 17] * 17) == 601080390


def _brute_coins(coins, amount):
    best = {0: 0}
    for a in range(1, amount + 1):
        options = [best[a - c] + 1 for c in coins if c <= a and best.get(a - c) is not None]
        best[a] = min(options) if options else None
    return -1 if best[amount] is None else best[amount]


def test_min_coins():
    assert min_coins([1, 2, 5], 11) == 3
    assert min_coins([2], 3) == -1
    assert min_coins([1], 0) == 0
    assert min_coins([3, 7], 1) == -1
    assert min_coins([1, 3, 4], 6) == 2, "biggest-coin-first greedy isn't optimal: 3 + 3 beats 4 + 1 + 1"
    rng = _random.Random(28)
    for _ in range(100):
        coins = rng.sample(range(1, 12), rng.randint(1, 4))
        amount = rng.randint(0, 40)
        assert min_coins(coins, amount) == _brute_coins(coins, amount), (coins, amount)


def _brute_combos(coins, amount):
    @_functools.lru_cache(maxsize=None)
    def go(i, left):
        if left == 0:
            return 1
        if i == len(coins):
            return 0
        return sum(go(i + 1, left - k * coins[i]) for k in range(left // coins[i] + 1))

    return go(0, amount)


def test_coin_combinations():
    assert coin_combinations([1, 2], 3) == 2, "you counted orderings: loop over coins OUTSIDE the amounts"
    assert coin_combinations([1, 2, 5], 5) == 4
    assert coin_combinations([2], 3) == 0
    assert coin_combinations([7], 0) == 1
    rng = _random.Random(28)
    for _ in range(100):
        coins = tuple(rng.sample(range(1, 10), rng.randint(1, 4)))
        amount = rng.randint(0, 30)
        assert coin_combinations(list(coins), amount) == _brute_combos(coins, amount), (coins, amount)


def test_knapsack_01():
    assert knapsack_01([1, 3, 4, 5], [1, 4, 5, 7], 7) == 9
    assert knapsack_01([2], [3], 6) == 3, "an item was used more than once: loop capacity downward"
    assert knapsack_01([], [], 5) == 0
    assert knapsack_01([5], [10], 4) == 0
    rng = _random.Random(28)
    for _ in range(100):
        n = rng.randint(0, 8)
        weights = [rng.randint(1, 8) for _ in range(n)]
        values = [rng.randint(0, 20) for _ in range(n)]
        cap = rng.randint(0, 20)
        want = max(sum(values[i] for i in range(n) if m >> i & 1)
                   for m in range(1 << n) if sum(weights[i] for i in range(n) if m >> i & 1) <= cap)
        assert knapsack_01(weights, values, cap) == want, (weights, values, cap)


def test_lis_length():
    assert lis_length([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert lis_length([0, 1, 0, 3, 2, 3]) == 4
    assert lis_length([7, 7, 7]) == 1, "strictly increasing: equal values don't extend a run (bisect_left)"
    assert lis_length([]) == 0
    rng = _random.Random(28)
    for _ in range(200):
        nums = [rng.randint(0, 9) for _ in range(rng.randint(0, 12))]
        best = [1] * len(nums)
        for j in range(len(nums)):
            for i in range(j):
                if nums[i] < nums[j]:
                    best[j] = max(best[j], best[i] + 1)
        assert lis_length(nums) == max(best, default=0), nums
    nums = [(i * 7919) % 20011 for i in range(20000)]
    start = _time.perf_counter()
    got = lis_length(nums)
    assert _time.perf_counter() - start < 0.5, "too slow for n = 20000: keep tails and use bisect_left (O(n log n))"
    assert got == 145


def _brute_lcs(a, b):
    @_functools.lru_cache(maxsize=None)
    def go(i, j):
        if i == len(a) or j == len(b):
            return 0
        if a[i] == b[j]:
            return 1 + go(i + 1, j + 1)
        return max(go(i + 1, j), go(i, j + 1))

    return go(0, 0)


def test_lcs():
    assert lcs('abcde', 'ace') == 3
    assert lcs('abc', 'abc') == 3
    assert lcs('abc', 'def') == 0
    assert lcs('', 'abc') == 0
    rng = _random.Random(28)
    for _ in range(100):
        a = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 8)))
        b = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 8)))
        assert lcs(a, b) == _brute_lcs(a, b), (a, b)
    try:
        deep = lcs('ab' * 350, 'ba' * 350), lcs('a' * 700, 'b' * 700)
    except RecursionError:
        raise AssertionError("RecursionError on 700-character strings: build the table bottom-up") from None
    assert deep == (699, 0)


def _brute_edit(a, b):
    @_functools.lru_cache(maxsize=None)
    def go(i, j):
        if i == len(a):
            return len(b) - j
        if j == len(b):
            return len(a) - i
        if a[i] == b[j]:
            return go(i + 1, j + 1)
        return 1 + min(go(i + 1, j + 1), go(i + 1, j), go(i, j + 1))

    return go(0, 0)


def test_edit_distance():
    assert edit_distance('horse', 'ros') == 3
    assert edit_distance('intention', 'execution') == 5
    assert edit_distance('', 'abc') == 3, "the empty-prefix row/column: turning '' into b takes len(b) inserts"
    assert edit_distance('abc', '') == 3
    assert edit_distance('same', 'same') == 0
    rng = _random.Random(28)
    for _ in range(100):
        a = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 7)))
        b = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 7)))
        assert edit_distance(a, b) == _brute_edit(a, b), (a, b)


def test_longest_pal_subseq():
    assert longest_pal_subseq('bbbab') == 4
    assert longest_pal_subseq('cbbd') == 2
    assert longest_pal_subseq('') == 0
    assert longest_pal_subseq('a') == 1
    rng = _random.Random(28)
    for _ in range(100):
        s = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 10)))
        want = max(len(c) for r in range(len(s) + 1) for c in _itertools.combinations(s, r) if c == c[::-1])
        assert longest_pal_subseq(s) == want, s


def test_equal_split():
    assert equal_split([1, 5, 11, 5]) is True
    assert equal_split([1, 2, 3, 5]) is False
    assert equal_split([]) is True
    assert equal_split([0]) is True
    assert equal_split([2]) is False
    rng = _random.Random(28)
    for _ in range(100):
        nums = [rng.randint(0, 12) for _ in range(rng.randint(0, 10))]
        total = sum(nums)
        want = total % 2 == 0 and any(sum(c) == total // 2 for r in range(len(nums) + 1)
                                      for c in _itertools.combinations(nums, r))
        assert equal_split(nums) is want, nums
    big = [rng.randint(1, 50) for _ in range(40)]
    big[-1] += sum(big) % 2
    assert equal_split(big) is True
    assert equal_split(big + [2 * sum(big)]) is False


def test_shortest_route():
    assert shortest_route([[0]]) == 0
    assert shortest_route([[0, 1], [1, 0]]) == 2
    assert shortest_route([[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]]) == 80
    assert shortest_route([[0, 1, 9], [9, 0, 1], [1, 9, 0]]) == 3, "costs can be asymmetric: dist[i][j] != dist[j][i]"
    rng = _random.Random(28)
    for _ in range(40):
        n = rng.randint(1, 7)
        dist = [[0 if i == j else rng.randint(1, 20) for j in range(n)] for i in range(n)]
        want = min((sum(dist[a][b] for a, b in zip((0, *p), (*p, 0))) for p in _itertools.permutations(range(1, n))), default=0)
        assert shortest_route(dist) == want, dist
    line = [[abs(i - j) for j in range(10)] for i in range(10)]
    assert shortest_route(line) == 18


def _tree(vals):
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    queue, i = [root], 1
    for node in queue:
        if i >= len(vals):
            break
        if vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            queue.append(node.right)
        i += 1
    return root


def _brute_tree(root):
    nodes, parent = [], []

    def walk(node, p):
        if node:
            nodes.append(node)
            parent.append(p)
            me = len(nodes) - 1
            walk(node.left, me)
            walk(node.right, me)

    walk(root, -1)
    best = 0
    for m in range(1 << len(nodes)):
        if all(not (m >> i & 1 and p >= 0 and m >> p & 1) for i, p in enumerate(parent)):
            best = max(best, sum(nodes[i].val for i in range(len(nodes)) if m >> i & 1))
    return best


def test_tree_take_skip():
    assert tree_take_skip(_tree([3, 2, 3, None, 3, None, 1])) == 7
    assert tree_take_skip(_tree([3, 4, 5, 1, 3, None, 1])) == 9
    assert tree_take_skip(None) == 0
    assert tree_take_skip(_tree([5])) == 5
    rng = _random.Random(28)
    for _ in range(40):
        nodes = [TreeNode(rng.randint(0, 9))]
        for _ in range(rng.randint(0, 9)):
            while True:
                p = rng.choice(nodes)
                side = rng.choice(('left', 'right'))
                if getattr(p, side) is None:
                    child = TreeNode(rng.randint(0, 9))
                    setattr(p, side, child)
                    nodes.append(child)
                    break
        assert tree_take_skip(nodes[0]) == _brute_tree(nodes[0])


def _brute_trade(prices):
    @_functools.lru_cache(maxsize=None)
    def go(i, holding, cooling):
        if i == len(prices):
            return 0
        best = go(i + 1, holding, False)
        if holding:
            best = max(best, prices[i] + go(i + 1, False, True))
        elif not cooling:
            best = max(best, -prices[i] + go(i + 1, True, False))
        return best

    return go(0, False, False)


def test_trade_with_cooldown():
    assert trade_with_cooldown([1, 2, 3, 0, 2]) == 3, "after a sale you must skip a day before buying again"
    assert trade_with_cooldown([1]) == 0
    assert trade_with_cooldown([]) == 0
    assert trade_with_cooldown([5, 4, 3]) == 0
    assert trade_with_cooldown([1, 4, 2]) == 3
    assert trade_with_cooldown([1, 3, 1, 3]) == 2, "after a sale you must skip a day before buying again"
    rng = _random.Random(28)
    for _ in range(150):
        prices = [rng.randint(0, 9) for _ in range(rng.randint(0, 10))]
        assert trade_with_cooldown(prices) == _brute_trade(tuple(prices)), prices
