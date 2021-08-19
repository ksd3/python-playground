"""R28 - Dynamic programming (reference solutions)

Compare after you've made your own attempt. Run: python check.py 28 -s
"""

PREDICT = r"""
>>> @cache
... def f(xs):
...     return len(xs)
>>> f((1, 2))
2
>>> f([1, 2])
TypeError

>>> calls = 0
>>> def fib(n):
...     global calls
...     calls += 1
...     return n if n < 2 else fib(n - 1) + fib(n - 2)
>>> fib(15), calls
(610, 1973)

>>> calls = 0
>>> @cache
... def fib(n):
...     global calls
...     calls += 1
...     return n if n < 2 else fib(n - 1) + fib(n - 2)
>>> fib(15), calls
(610, 16)
>>> fib(15), calls
(610, 16)

>>> a, b = 0, 1
>>> for _ in range(10):
...     a, b = b, a + b
>>> a
55

>>> def best(weights, values, cap, downward):
...     dp = [0] * (cap + 1)
...     for w, v in zip(weights, values):
...         order = range(cap, w - 1, -1) if downward else range(w, cap + 1)
...         for c in order:
...             dp[c] = max(dp[c], dp[c - w] + v)
...     return dp[cap]
>>> best([2], [3], 6, True), best([2], [3], 6, False)
(3, 9)

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
(2, 3)

>>> dp = [[0] * 3] * 2
>>> dp[0][1] = 5
>>> dp
[[0, 5, 0], [0, 5, 0]]

>>> INF = float('inf')
>>> min(INF, 3), INF + 1 == INF, INF - INF
(3, True, nan)

>>> tails = []
>>> for x in [3, 1, 4, 1, 5, 9, 2, 6]:
...     i = bisect_left(tails, x)
...     if i == len(tails):
...         tails.append(x)
...     else:
...         tails[i] = x
>>> tails, len(tails)
([1, 2, 5, 6], 4)

>>> def lis_len(nums, strict):
...     tails = []
...     for x in nums:
...         i = (bisect_left if strict else bisect_right)(tails, x)
...         tails[i:i + 1] = [x]
...     return len(tails)
>>> lis_len([2, 2, 2], True), lis_len([2, 2, 2], False)
(1, 3)

>>> a, b = 'abc', 'ab'
>>> [list(range(len(b) + 1))] + [[i] + [0] * len(b) for i in range(1, len(a) + 1)]
[[0, 1, 2], [1, 0, 0], [2, 0, 0], [3, 0, 0]]

>>> bits = 1
>>> for x in [3, 5, 9]:
...     bits |= bits << x
>>> [s for s in range(18) if bits >> s & 1]
[0, 3, 5, 8, 9, 12, 14, 17]

>>> MOD = 10**9 + 7
>>> (MOD - 1) * 2 % MOD
1000000005

>>> memo = {}
>>> memo[(1, 2)] = 'ok'
>>> memo[[1, 2]] = 'no'
TypeError
>>> memo
{(1, 2): 'ok'}
"""

from bisect import bisect_left
import math


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def stairs(n):
    a, b = 1, 1              # ways to reach step i and step i + 1
    for _ in range(n):
        a, b = b, a + b
    return a


def max_take_skip(nums):
    take, skip = 0, 0        # best so far if the last element was taken / skipped
    for x in nums:
        take, skip = skip + x, max(take, skip)
    return max(take, skip)


def grid_paths(grid):
    if grid[0][0] == '#' or grid[-1][-1] == '#':
        return 0
    cols = len(grid[0])
    dp = [0] * cols          # dp[c]: paths reaching column c of the current row
    dp[0] = 1
    for row in grid:
        for c in range(cols):
            if row[c] == '#':
                dp[c] = 0
            elif c > 0:
                dp[c] += dp[c - 1]
    return dp[-1]


def min_coins(coins, amount):
    dp = [0] + [math.inf] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return -1 if dp[amount] == math.inf else dp[amount]


def coin_combinations(coins, amount):
    dp = [1] + [0] * amount
    for c in coins:                       # coins outside: each combination is built in one order
        for a in range(c, amount + 1):
            dp[a] += dp[a - c]
    return dp[amount]


def knapsack_01(weights, values, cap):
    dp = [0] * (cap + 1)
    for w, v in zip(weights, values):
        for c in range(cap, w - 1, -1):   # downward, so dp[c - w] still excludes this item
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[cap]


def lis_length(nums):
    tails = []               # tails[k]: smallest last value of an increasing run of length k + 1
    for x in nums:
        i = bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)


def lcs(a, b):
    prev = [0] * (len(b) + 1)
    for ch in a:
        cur = [0]
        for j, other in enumerate(b):
            cur.append(prev[j] + 1 if ch == other else max(prev[j + 1], cur[j]))
        prev = cur
    return prev[-1]


def edit_distance(a, b):
    prev = list(range(len(b) + 1))        # turning '' into b[:j] takes j inserts
    for i, ch in enumerate(a, 1):
        cur = [i]
        for j, other in enumerate(b, 1):
            if ch == other:
                cur.append(prev[j - 1])
            else:
                cur.append(1 + min(prev[j - 1], prev[j], cur[j - 1]))   # replace, delete, insert
        prev = cur
    return prev[-1]


def longest_pal_subseq(s):
    n = len(s)
    if n == 0:
        return 0
    dp = [[0] * n for _ in range(n)]      # dp[i][j]: answer for s[i..j]
    for i in range(n - 1, -1, -1):
        dp[i][i] = 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    return dp[0][n - 1]


def equal_split(nums):
    total = sum(nums)
    if total % 2:
        return False
    bits = 1                              # bit s is set when some subset sums to s
    for x in nums:
        bits |= bits << x
    return bool(bits >> (total // 2) & 1)


def shortest_route(dist):
    n = len(dist)
    if n == 1:
        return 0
    full = 1 << n
    dp = [[math.inf] * n for _ in range(full)]    # dp[mask][i]: start at 0, visit mask, stand at i
    dp[1][0] = 0
    for mask in range(1, full, 2):                # every useful mask contains city 0
        for i in range(n):
            cost = dp[mask][i]
            if cost == math.inf:
                continue
            for j in range(n):
                if not mask >> j & 1:
                    nxt = mask | 1 << j
                    if cost + dist[i][j] < dp[nxt][j]:
                        dp[nxt][j] = cost + dist[i][j]
    return min(dp[full - 1][i] + dist[i][0] for i in range(1, n))


def tree_take_skip(root):
    def best(node):                       # (best sum taking node, best sum skipping it)
        if node is None:
            return 0, 0
        lt, ls = best(node.left)
        rt, rs = best(node.right)
        return node.val + ls + rs, max(lt, ls) + max(rt, rs)

    return max(best(root))


def trade_with_cooldown(prices):
    hold, sold, rest = -math.inf, 0, 0    # holding a share / just sold / free to buy
    for p in prices:
        hold, sold, rest = max(hold, rest - p), hold + p, max(rest, sold)
    return max(sold, rest)
