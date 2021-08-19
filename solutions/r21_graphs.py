"""R21 - Graphs (reference solutions)

Compare after you've made your own attempt. Run: python check.py 21 -s
"""

PREDICT = r"""
>>> adj = [[]] * 3
>>> adj[0].append(1)
>>> adj
[[1], [1], [1]]

>>> g = defaultdict(list)
>>> for u, v in [(0, 1), (1, 2)]:
...     g[u].append(v)
...     g[v].append(u)
>>> sorted(g.items())
[(0, [1]), (1, [0, 2]), (2, [1])]
>>> len(g), g[5], len(g)
(3, [], 4)

>>> adj = {0: [1, 2], 1: [3], 2: [3], 3: []}
>>> seen, q, order = {0}, deque([0]), []
>>> while q:
...     u = q.popleft()
...     order.append(u)
...     for v in adj[u]:
...         if v not in seen:
...             seen.add(v)
...             q.append(v)
>>> order
[0, 1, 2, 3]

>>> adj = {0: [1, 2], 1: [3], 2: [], 3: []}
>>> def dfs_order(start, rev):
...     stack, seen, order = [start], set(), []
...     while stack:
...         u = stack.pop()
...         if u not in seen:
...             seen.add(u)
...             order.append(u)
...             stack.extend(reversed(adj[u]) if rev else adj[u])
...     return order
>>> dfs_order(0, False)
[0, 2, 1, 3]
>>> dfs_order(0, True)
[0, 1, 3, 2]

>>> adj = {0: [1, 2], 1: [3], 2: [3], 3: []}
>>> q, seen, pushes = deque([0]), set(), 0
>>> while q:
...     u = q.popleft()
...     if u in seen:
...         continue
...     seen.add(u)
...     for v in adj[u]:
...         q.append(v)
...         pushes += 1
>>> pushes, len(seen)
(4, 4)

>>> pq = []
>>> heappush(pq, (5, 'b')); heappush(pq, (2, 'b')); heappush(pq, (3, 'c'))
>>> [heappop(pq) for _ in range(3)]
[(2, 'b'), (3, 'c'), (5, 'b')]

>>> dist = [math.inf] * 3
>>> dist[0] = 0
>>> dist, [d if d < math.inf else -1 for d in dist]
([0, inf, inf], [0, -1, -1])

>>> from graphlib import TopologicalSorter
>>> list(TopologicalSorter({'b': {'a'}, 'c': {'b'}}).static_order())
['a', 'b', 'c']
>>> list(TopologicalSorter({'a': {'b'}, 'b': {'a'}}).static_order())
CycleError

>>> edges = [(0, 1), (1, 2), (2, 0)]
>>> indeg = [0] * 3
>>> for u, v in edges:
...     indeg[v] += 1
>>> [u for u in range(3) if indeg[u] == 0]
[]

>>> grid = ['ab', 'cd']
>>> r, c = 0, 0
>>> grid[r - 1][c], grid[r][c - 1]
('c', 'b')

>>> seen = {(0, 1)}
>>> (0, 1) in seen
True
>>> [0, 1] in seen
TypeError

>>> grid = [[1, 0, 0], [0, 0, 0], [0, 0, 1]]
>>> dist = [[0 if x else -1 for x in row] for row in grid]
>>> q = deque((r, c) for r in range(3) for c in range(3) if grid[r][c])
>>> while q:
...     r, c = q.popleft()
...     for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
...         if 0 <= nr < 3 and 0 <= nc < 3 and dist[nr][nc] == -1:
...             dist[nr][nc] = dist[r][c] + 1
...             q.append((nr, nc))
>>> dist
[[0, 1, 2], [1, 2, 1], [2, 1, 0]]

>>> w = 'cat'
>>> [w[:i] + '*' + w[i + 1:] for i in range(len(w))]
['*at', 'c*t', 'ca*']

>>> mask = 0b001
>>> mask | 1 << 2, 1 << 3 - 1, (1 << 3) - 1
(5, 4, 7)
"""

import heapq
import math
from collections import defaultdict, deque

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def build_adj(n, edges, directed=False):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        if not directed:
            adj[v].append(u)
    return adj


def bfs_dist(adj, src):
    dist = [-1] * len(adj)
    dist[src] = 0
    q = deque([src])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


def shortest_path(adj, src, dst):
    parent = {src: None}
    q = deque([src])
    while q and dst not in parent:
        u = q.popleft()
        for v in adj[u]:
            if v not in parent:
                parent[v] = u
                q.append(v)
    if dst not in parent:
        return []
    path = [dst]
    while parent[path[-1]] is not None:     # `is not None`: node 0 is falsy
        path.append(parent[path[-1]])
    return path[::-1]


def count_islands(grid):
    R = len(grid)
    C = len(grid[0]) if R else 0
    seen = set()
    islands = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] != '#' or (r, c) in seen:
                continue
            islands += 1
            seen.add((r, c))
            stack = [(r, c)]
            while stack:
                cr, cc = stack.pop()
                for dr, dc in DIRS:
                    nr, nc = cr + dr, cc + dc
                    if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == '#' and (nr, nc) not in seen:
                        seen.add((nr, nc))
                        stack.append((nr, nc))
    return islands


def grid_steps(grid, start, goal):
    R, C = len(grid), len(grid[0])
    dist = {start: 0}
    q = deque([start])
    while q:
        r, c = q.popleft()
        if (r, c) == goal:
            return dist[r, c]
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] != '#' and (nr, nc) not in dist:
                dist[nr, nc] = dist[r, c] + 1
                q.append((nr, nc))
    return -1


def nearest_source(grid):
    R, C = len(grid), len(grid[0])
    dist = [[0 if x else -1 for x in row] for row in grid]
    q = deque((r, c) for r in range(R) for c in range(C) if grid[r][c])
    while q:
        r, c = q.popleft()
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                q.append((nr, nc))
    return dist


def has_cycle_directed(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n
    for root in range(n):
        if color[root] != WHITE:
            continue
        color[root] = GRAY
        stack = [(root, iter(adj[root]))]      # (node, its remaining neighbors)
        while stack:
            u, rest = stack[-1]
            for v in rest:
                if color[v] == GRAY:
                    return True
                if color[v] == WHITE:
                    color[v] = GRAY
                    stack.append((v, iter(adj[v])))
                    break
            else:                               # no neighbors left: u is finished
                color[u] = BLACK
                stack.pop()
    return False


def topo_order(n, edges):
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1
    q = deque(u for u in range(n) if indeg[u] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == n else None


def is_bipartite(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    color = [-1] * n
    for root in range(n):
        if color[root] != -1:
            continue
        color[root] = 0
        q = deque([root])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if color[v] == -1:
                    color[v] = color[u] ^ 1
                    q.append(v)
                elif color[v] == color[u]:
                    return False
    return True


def dijkstra(n, edges, src):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [math.inf] * n
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue                    # stale: u was already reached more cheaply
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(pq, (d + w, v))
    return dist


def zero_one_bfs(n, edges, src):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [math.inf] * n
    dist[src] = 0
    dq = deque([src])
    while dq:
        u = dq.popleft()
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                if w == 0:
                    dq.appendleft(v)
                else:
                    dq.append(v)
    return dist


def cheapest_within_k(n, edges, src, dst, k):
    best = [math.inf] * n
    best[src] = 0
    for _ in range(k):
        nxt = best[:]                   # read last round, write this round
        for u, v, price in edges:
            if best[u] + price < nxt[v]:
                nxt[v] = best[u] + price
        best = nxt
    return -1 if best[dst] == math.inf else best[dst]


def word_steps(start, goal, words):
    if start == goal:
        return 0
    words = set(words)
    if goal not in words:
        return -1
    buckets = defaultdict(list)
    for w in words:
        for i in range(len(w)):
            buckets[w[:i] + '*' + w[i + 1:]].append(w)
    seen = {start}
    q = deque([(start, 0)])
    while q:
        w, d = q.popleft()
        for i in range(len(w)):
            for x in buckets.pop(w[:i] + '*' + w[i + 1:], ()):   # each bucket only needs one scan
                if x == goal:
                    return d + 1
                if x not in seen:
                    seen.add(x)
                    q.append((x, d + 1))
    return -1


def min_steps_with_breaks(grid, k):
    R, C = len(grid), len(grid[0])
    seen = {(0, 0, 0)}
    q = deque([(0, 0, 0, 0)])           # row, col, walls used, steps
    while q:
        r, c, used, steps = q.popleft()
        if (r, c) == (R - 1, C - 1):
            return steps
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C:
                nu = used + (grid[nr][nc] == '#')
                if nu <= k and (nr, nc, nu) not in seen:
                    seen.add((nr, nc, nu))
                    q.append((nr, nc, nu, steps + 1))
    return -1
