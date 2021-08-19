"""R32 - Pattern recognition (reference solutions)

Compare after you've made your own attempt. Run: python check.py 32 -s
"""
import math
from collections import Counter, deque

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
(2, 1)

>>> def prefix_count(nums, k):
...     seen, total, count = Counter({0: 1}), 0, 0
...     for x in nums:
...         total += x
...         count += seen[total - k]
...         seen[total] += 1
...     return count
>>> prefix_count([1, -1, 1, 2], 2)
2

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
{'a': 0, 'b': 1, 'c': 5, 'd': 2}
>>> dist = {v: math.inf for v in adj}
>>> dist['a'] = 0
>>> for _ in range(len(adj) - 1):
...     for u in adj:
...         for v, w in adj[u]:
...             dist[v] = min(dist[v], dist[u] + w)
>>> dist
{'a': 0, 'b': -5, 'c': 5, 'd': -4}

>>> adj = {'s': [('t', 10), ('m', 1)], 'm': [('t', 1)], 't': []}
>>> dist, q = {'s': 0}, deque(['s'])
>>> while q:
...     u = q.popleft()
...     for v, w in adj[u]:
...         if v not in dist:
...             dist[v] = dist[u] + w
...             q.append(v)
>>> dist['t']
10

>>> def greedy(coins, amount):
...     count = 0
...     for c in sorted(coins, reverse=True):
...         count += amount // c
...         amount %= c
...     return count
>>> greedy([1, 5, 6, 9], 11)
3
>>> best = [0] + [math.inf] * 11
>>> for a in range(1, 12):
...     best[a] = min(best[a - c] + 1 for c in [1, 5, 6, 9] if c <= a)
>>> best[11]
2

>>> ok = [False, True, False, True, True]
>>> lo, hi = 0, len(ok) - 1
>>> while lo < hi:
...     mid = (lo + hi) // 2
...     if ok[mid]:
...         hi = mid
...     else:
...         lo = mid + 1
>>> lo, ok.index(True)
(3, 1)

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
(False, False, True)

>>> def best_sum(nums):
...     best = cur = 0
...     for x in nums:
...         cur = max(0, cur + x)
...         best = max(best, cur)
...     return best
>>> best_sum([2, -1, 3]), best_sum([-3, -1, -2])
(4, 0)

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
(['a'], False)

>>> h = []
>>> for x in [5, 1, 9, 3, 7]:
...     heappush(h, x)
...     if len(h) > 3:
...         _ = heappop(h)
>>> h[0], sorted(h)
(5, [5, 7, 9])

>>> n = 10**5
>>> n * n, n * n.bit_length()
(10000000000, 1700000)
>>> 2 ** 20 * 20, math.factorial(11)
(20971520, 39916800)
"""

QUIZ = {
    "constraint: n <= 10": ["O(n!)", "O(n! * n)", "O(n * n!)", "factorial"],
    "constraint: n <= 20": ["O(2^n)", "O(2^n * n)", "O(n * 2^n)", "O(2^n * n^2)", "O(n^2 * 2^n)", "exponential"],
    "constraint: n <= 40": ["O(2^(n/2))", "meet in the middle", "O(2^(n/2) * n)", "O(n * 2^(n/2))"],
    "constraint: n <= 500": ["O(n^3)", "cubic"],
    "constraint: n <= 5000": ["O(n^2)", "quadratic", "O(n^2 log n)"],
    "constraint: n <= 10**6": ["O(n log n)", "O(n)", "linear", "n log n"],
    "constraint: a single number n up to 10**9": ["O(sqrt(n))", "O(sqrt n)", "O(√n)", "O(log n)", "O(1)", "logarithmic", "constant"],
    "constraint: a single number n up to 10**18": ["O(log n)", "O(1)", "logarithmic", "constant"],
    "signal: sorted array, find a pair with a target sum in O(1) extra space": ["two pointers", "two pointer", "2 pointers"],
    "signal: longest substring with at most k distinct characters": ["sliding window", "variable sliding window", "variable window"],
    "signal: count subarrays that sum to k, values can be negative": [
        "prefix sums + hashmap", "prefix sum + hashmap",
        "prefix sums and a hashmap", "prefix sums and hashmap", "prefix sum and hashmap", "prefix sums with a hashmap",
        "prefix sum hashmap", "prefix sums", "prefix sum"],
    "signal: many updates that add v to a range [l, r], then read the final array": ["difference array", "difference arrays", "diff array"],
    "signal: smallest capacity that lets the work finish within d days": [
        "binary search on the answer", "binary search on answer", "binary search the answer", "binary search"],
    "signal: for every element, the next element to its right that is greater": ["monotonic stack", "monotone stack", "stack"],
    "signal: maximum of every window of size k": ["monotonic deque", "monotone deque", "monotonic queue", "deque"],
    "signal: k-th largest element of a stream": ["heap", "min heap", "min heap of size k", "heap of size k", "priority queue"],
    "signal: running median of a stream": ["two heaps", "2 heaps", "heaps"],
    "signal: fewest moves on a grid where every move costs the same": ["bfs", "breadth first search"],
    "signal: cheapest path when edge weights are non-negative and differ": ["dijkstra", "dijkstra's", "dijkstras", "dijkstra's algorithm"],
    "signal: shortest path when every edge costs 0 or 1": ["0-1 bfs", "0/1 bfs", "zero one bfs", "deque bfs"],
    "signal: connections arrive one at a time; are a and b connected yet?": [
        "union find", "dsu", "disjoint set", "disjoint sets", "disjoint set union"],
    "signal: tasks with prerequisites, find an order that works": [
        "topological sort", "topological sorting", "topological order", "topological ordering", "topo sort",
        "kahn", "kahn's algorithm"],
    "signal: generate every subset or permutation": ["backtracking", "backtrack", "recursion", "dfs"],
    "signal: count the ways to reach a total when choices overlap": ["dp", "dynamic programming"],
    "signal: fewest single-character edits that turn one string into another": ["dp", "2d dp", "dynamic programming", "edit distance"],
    "signal: all dictionary words that start with a given prefix": ["trie", "tries", "prefix tree"],
    "signal: fewest rooms so that no two overlapping meetings share one": [
        "heap", "min heap", "sweep line", "line sweep", "sort + heap", "sort and heap", "priority queue", "events"],
    "signal: the middle node of a linked list in one pass": [
        "fast and slow pointers", "fast slow pointers", "fast/slow pointers", "slow and fast pointers",
        "tortoise and hare", "two pointers"],
    "signal: every value appears twice except one": ["xor", "bitwise xor", "bit manipulation"],
    "signal: range-sum queries mixed with point updates": [
        "fenwick tree", "fenwick", "binary indexed tree", "bit", "segment tree"],
    "signal: group the words that are anagrams of each other": [
        "hashmap", "dict", "dictionary", "canonical key", "sorted key", "hashing", "dict of lists"],
    "signal: n <= 20 items, pick the best subset where the items interact": [
        "bitmask dp", "bitmask", "bitmasks", "subset dp", "dp over subsets", "bitmask enumeration"],
    "false trigger: a shrinking sliding window breaks when the array has ...": [
        "negative numbers", "negatives", "negative values", "negative elements"],
    "false trigger: Dijkstra gives wrong answers when the graph has ...": [
        "negative edges", "negative weights", "negative edge weights", "negative edge"],
    "false trigger: plain BFS gives wrong shortest paths when edges have ...": [
        "weights", "different weights", "weighted edges", "unequal weights", "different costs", "unequal costs"],
    "false trigger: binary search on the answer needs the feasibility check to be ...": ["monotonic", "monotone"],
    "false trigger: before trusting a greedy choice, prove it with an ...": ["exchange argument", "exchange"],
    "false trigger: two pointers from both ends needs the array to be ...": ["sorted"],
    "false trigger: a topological order exists only if the graph has no ...": [
        "cycles", "cycle", "directed cycles", "directed cycle"],
    "false trigger: memoization only pays off when subproblems ...": [
        "overlap", "overlapping", "repeat", "repeat themselves", "recur", "are reused"],
    "false trigger: resetting a running sum to 0 is wrong when the chosen run must be ...": ["non-empty", "not empty"],
    "false trigger: to keep the k largest values seen so far, the size-k heap must be a ...": ["min heap"],
}


def closest_pair_gap(nums, target):
    i, j, best = 0, len(nums) - 1, math.inf
    while i < j:
        s = nums[i] + nums[j]
        best = min(best, abs(s - target))
        if s < target:
            i += 1
        elif s > target:
            j -= 1
        else:
            return 0
    return best


def shortest_reaching(nums, s):
    best, left, total = math.inf, 0, 0
    for right, x in enumerate(nums):
        total += x
        while total >= s:           # shrink while the window still reaches s
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1
    return 0 if best == math.inf else best


def count_divisible(nums, k):
    seen, total, count = Counter({0: 1}), 0, 0
    for x in nums:
        total = (total + x) % k     # Python's % is never negative for k > 0
        count += seen[total]
        seen[total] += 1
    return count


def smallest_max_split(nums, m):
    def pieces_needed(cap):
        pieces, cur = 1, 0
        for x in nums:
            if cur + x > cap:
                pieces, cur = pieces + 1, 0
            cur += x
        return pieces

    lo, hi = max(nums), sum(nums)   # feasibility flips from False to True once
    while lo < hi:
        mid = (lo + hi) // 2
        if pieces_needed(mid) <= m:
            hi = mid
        else:
            lo = mid + 1
    return lo


def steps_to_larger(nums):
    ans, stack = [0] * len(nums), []    # stack: indices still waiting for a larger value
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] < x:
            j = stack.pop()
            ans[j] = i - j
        stack.append(i)
    return ans


def fewest_moves(grid):
    rows, cols = len(grid), len(grid[0])
    if grid[0][0] == '#' or grid[-1][-1] == '#':
        return -1
    dist = [[-1] * cols for _ in range(rows)]
    dist[0][0] = 0
    q = deque([(0, 0)])
    while q:
        r, c = q.popleft()
        if (r, c) == (rows - 1, cols - 1):
            return dist[r][c]
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '.' and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                q.append((nr, nc))
    return -1


def count_groups(n, pairs):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]   # path halving, no recursion
            x = parent[x]
        return x

    groups = n
    for a, b in pairs:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            groups -= 1
    return groups


def valid_order(n, before):
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for a, b in before:
        adj[a].append(b)
        indeg[b] += 1
    order = [v for v in range(n) if indeg[v] == 0]
    for u in order:                 # the list doubles as the queue
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                order.append(v)
    return order if len(order) == n else []


def best_non_adjacent(nums):
    take = skip = 0                 # best sums ending with the last position taken / skipped
    for x in nums:
        take, skip = skip + x, max(take, skip)
    return max(take, skip)


def prefix_counts(words, prefixes):
    root = {None: 0}                # None holds how many words pass through a node
    for w in words:
        node = root
        node[None] += 1
        for ch in w:
            node = node.setdefault(ch, {None: 0})
            node[None] += 1
    out = []
    for p in prefixes:
        node = root
        for ch in p:
            node = node.get(ch)
            if node is None:
                break
        out.append(0 if node is None else node[None])
    return out
