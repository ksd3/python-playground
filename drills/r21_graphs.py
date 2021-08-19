"""R21 - Graphs

Most graph work starts by turning an edge list into an adjacency list;
undirected edges go in both directions. BFS finds fewest-edge paths, and a
node is marked visited when it enters the queue, not when it leaves. Dijkstra
is BFS with a heap for non-negative weights (skip popped entries that are out
of date); with 0/1 weights a deque is enough. Directed cycles: three colors,
or Kahn's algorithm. Grids, word changes and puzzle states are graphs too:
generate neighbors on the fly and put everything that matters in the state.

Part 1 - Predict. Each block in PREDICT is a REPL session. Replace every ???
with exactly what Python prints: expression values are echoed the way the REPL
echoes them, and a line that raises prints just the exception name (TypeError).

Part 2 - Drills. Implement every function until `python check.py 21` is green.
Don't edit the tests at the bottom; add your own test_* functions if you like.

Unlocks: islands and flood fill, dependency ordering, network delays, word
transformations, spreading from many sources at once, two-coloring, and grid
searches that carry extra state.
"""

PREDICT = r"""
>>> adj = [[]] * 3
>>> adj[0].append(1)
>>> adj
???

>>> g = defaultdict(list)
>>> for u, v in [(0, 1), (1, 2)]:
...     g[u].append(v)
...     g[v].append(u)
>>> sorted(g.items())
???
>>> len(g), g[5], len(g)
???

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
???

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
???
>>> dfs_order(0, True)
???

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
???

>>> pq = []
>>> heappush(pq, (5, 'b')); heappush(pq, (2, 'b')); heappush(pq, (3, 'c'))
>>> [heappop(pq) for _ in range(3)]
???

>>> dist = [math.inf] * 3
>>> dist[0] = 0
>>> dist, [d if d < math.inf else -1 for d in dist]
???

>>> from graphlib import TopologicalSorter
>>> list(TopologicalSorter({'b': {'a'}, 'c': {'b'}}).static_order())
???
>>> list(TopologicalSorter({'a': {'b'}, 'b': {'a'}}).static_order())
???

>>> edges = [(0, 1), (1, 2), (2, 0)]
>>> indeg = [0] * 3
>>> for u, v in edges:
...     indeg[v] += 1
>>> [u for u in range(3) if indeg[u] == 0]
???

>>> grid = ['ab', 'cd']
>>> r, c = 0, 0
>>> grid[r - 1][c], grid[r][c - 1]
???

>>> seen = {(0, 1)}
>>> (0, 1) in seen
???
>>> [0, 1] in seen
???

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
???

>>> w = 'cat'
>>> [w[:i] + '*' + w[i + 1:] for i in range(len(w))]
???

>>> mask = 0b001
>>> mask | 1 << 2, 1 << 3 - 1, (1 << 3) - 1
???
"""

import heapq
import math
from collections import defaultdict, deque

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


# ---------------------------------------------------------------- drills

def build_adj(n, edges, directed=False):
    """Return an adjacency list for nodes 0..n-1 (a list of n lists). Each edge
    (u, v) appends v to adj[u]; an undirected graph also appends u to adj[v].
    Neighbors keep the order of the edge list.
    build_adj(3, [(0, 1), (1, 2)]) == [[1], [0, 2], [1]]"""
    raise NotImplementedError


def bfs_dist(adj, src):
    """Return dist where dist[v] is the fewest edges on a path from src to v,
    or -1 if v can't be reached. bfs_dist([[1], [2], []], 0) == [0, 1, 2]"""
    raise NotImplementedError


def shortest_path(adj, src, dst):
    """Return one fewest-edge path from src to dst as a list of nodes (both
    ends included), or [] if dst can't be reached; the path from x to x is [x].
    Record each node's parent when you first reach it, then walk back."""
    raise NotImplementedError


def count_islands(grid):
    """grid is a list of equal-length strings: '#' is land, '.' is water.
    Return the number of islands (land cells joined up/down/left/right, not
    diagonally). Islands can be thousands of cells long, so a DFS that
    recurses once per cell will hit the recursion limit."""
    raise NotImplementedError


def grid_steps(grid, start, goal):
    """grid is a list of equal-length strings where '#' is a wall. Return the
    fewest up/down/left/right moves from start to goal ((row, col) tuples,
    never walls), or -1 if goal can't be reached. Moves can't leave the grid.
    grid_steps(['..', '#.'], (0, 0), (1, 1)) == 2"""
    raise NotImplementedError


def nearest_source(grid):
    """grid is a list of lists of 0/1 and every cell is walkable. Return a new
    grid of the same shape holding the fewest up/down/left/right moves from
    each cell to the nearest 1 (so 1-cells hold 0); with no 1 anywhere, every
    cell is -1. Use one BFS that starts from all the 1s at once."""
    raise NotImplementedError


def has_cycle_directed(n, edges):
    """Return True if the directed graph on 0..n-1 with edges (u, v) has a
    cycle (a self-loop counts), else False. Three colors: unvisited, on the
    current path, finished; an edge into a node still on the current path
    closes a cycle. (Kahn's algorithm works too.)"""
    raise NotImplementedError


def topo_order(n, edges):
    """Return an ordering of 0..n-1 where every edge (u, v) puts u before v,
    or None if there's a cycle. Any valid order is accepted. Kahn: start from
    the nodes with no incoming edges and remove them one at a time."""
    raise NotImplementedError


def is_bipartite(n, edges):
    """Return True if the undirected graph on 0..n-1 can be two-colored so
    every edge joins different colors, else False. It may be disconnected."""
    raise NotImplementedError


def dijkstra(n, edges, src):
    """edges are directed (u, v, w) with w >= 0. Return dist where dist[v] is
    the cheapest total weight from src to v, or math.inf if unreachable. Use a
    heap of (distance, node) and skip popped entries that are out of date."""
    raise NotImplementedError


def zero_one_bfs(n, edges, src):
    """Same contract as dijkstra, but every weight is 0 or 1. Use a deque: the
    far end of a 0-edge goes to the front, the far end of a 1-edge to the back."""
    raise NotImplementedError


def cheapest_within_k(n, edges, src, dst, k):
    """edges are directed (u, v, price) with price >= 0. Return the cheapest
    total price from src to dst using at most k edges, or -1 if there's no
    such route (src == dst costs 0). Bellman-Ford for k rounds, where each
    round relaxes from a copy of the previous round's prices."""
    raise NotImplementedError


def word_steps(start, goal, words):
    """All words have the same length. One step changes exactly one letter, and
    every word after start must be in `words`. Return the fewest steps from
    start to goal (0 if they're equal), or -1 if it can't be done. Bucket the
    words by patterns like 'c*t' instead of comparing every pair."""
    raise NotImplementedError


def min_steps_with_breaks(grid, k):
    """grid is a list of equal-length strings, '#' is a wall; the top-left and
    bottom-right cells are never walls. Return the fewest up/down/left/right
    moves from top-left to bottom-right when you may step onto at most k wall
    cells, or -1. The BFS state is (row, col, walls_used), not (row, col)."""
    raise NotImplementedError


# ---------------------------------------------------------------- tests (don't edit)

import random


def _adj(n, edges, directed=True):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        if not directed:
            adj[v].append(u)
    return adj


def _relax(n, wedges, src):
    """Bellman-Ford: slow, but obviously correct."""
    dist = [math.inf] * n
    dist[src] = 0
    for _ in range(n):
        for u, v, w in wedges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return dist


def _islands_ref(grid):
    cells = {(r, c) for r, row in enumerate(grid) for c, ch in enumerate(row) if ch == '#'}
    parent = {cell: cell for cell in cells}

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    for r, c in cells:
        for nb in ((r + 1, c), (r, c + 1)):
            if nb in cells:
                parent[find(nb)] = find((r, c))
    return len({find(cell) for cell in cells})


def _snake(rows, cols):
    """One island, one cell wide, winding back and forth (rows must be odd)."""
    out = []
    for r in range(rows):
        if r % 2 == 0:
            out.append('#' * cols)
        elif r % 4 == 1:
            out.append('.' * (cols - 1) + '#')
        else:
            out.append('#' + '.' * (cols - 1))
    return out


def _grid_ref(grid, start, goal):
    R, C = len(grid), len(grid[0])
    dist = {start: 0}
    changed = True
    while changed:
        changed = False
        for (r, c), d in list(dist.items()):
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] != '#' \
                        and dist.get((nr, nc), math.inf) > d + 1:
                    dist[(nr, nc)] = d + 1
                    changed = True
    return dist.get(goal, -1)


def _has_cycle_ref(n, edges):
    reach = [[False] * n for _ in range(n)]
    for u, v in edges:
        reach[u][v] = True
    for k in range(n):
        for i in range(n):
            if reach[i][k]:
                for j in range(n):
                    if reach[k][j]:
                        reach[i][j] = True
    return any(reach[i][i] for i in range(n))


def _check_topo(n, edges, order):
    assert order is not None, f"got None, but {edges} has no cycle"
    assert sorted(order) == list(range(n)), f"not an ordering of 0..{n - 1}: {order}"
    pos = {v: i for i, v in enumerate(order)}
    for u, v in edges:
        assert pos[u] < pos[v], f"edge {u}->{v}, but {v} comes first in {order}"


def _bipartite_ref(n, edges):
    return any(all((mask >> u & 1) != (mask >> v & 1) for u, v in edges) for mask in range(1 << n))


def _cheapest_ref(n, edges, src, dst, k):
    best = math.inf

    def walk(u, cost, left):
        nonlocal best
        if u == dst:
            best = min(best, cost)
        if left:
            for a, b, p in edges:
                if a == u:
                    walk(b, cost + p, left - 1)

    walk(src, 0, k)
    return -1 if best == math.inf else best


def _word_ref(start, goal, words):
    if start == goal:
        return 0
    words, seen, frontier, steps = set(words), {start}, [start], 0
    while frontier:
        steps += 1
        nxt = []
        for w in frontier:
            for x in words:
                if x not in seen and sum(a != b for a, b in zip(w, x)) == 1:
                    if x == goal:
                        return steps
                    seen.add(x)
                    nxt.append(x)
        frontier = nxt
    return -1


def _breaks_ref(grid, k):
    """Try every simple path (fine for tiny grids)."""
    R, C = len(grid), len(grid[0])
    best, seen = math.inf, {(0, 0)}

    def walk(r, c, steps, used):
        nonlocal best
        if (r, c) == (R - 1, C - 1):
            best = min(best, steps)
            return
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and (nr, nc) not in seen:
                cost = used + (grid[nr][nc] == '#')
                if cost <= k:
                    seen.add((nr, nc))
                    walk(nr, nc, steps + 1, cost)
                    seen.remove((nr, nc))

    walk(0, 0, 0, 0)
    return -1 if best == math.inf else best


def test_build_adj():
    assert build_adj(3, [(0, 1), (1, 2)]) == [[1], [0, 2], [1]], \
        "every node needs its own list ([[]] * n makes them all share one)"
    assert build_adj(3, [(0, 1), (1, 2)], directed=True) == [[1], [2], []]
    assert build_adj(4, [(2, 0), (2, 3)]) == [[2], [], [0, 3], [2]], "isolated nodes get []"
    assert build_adj(0, []) == []
    adj = build_adj(3, [])
    adj[0].append(9)
    assert adj == [[9], [], []], "every node needs its own list"


def test_bfs_dist():
    adj = [[1, 2], [3], [3], [], []]
    assert bfs_dist(adj, 0) == [0, 1, 1, 2, -1]
    assert bfs_dist(adj, 4) == [-1, -1, -1, -1, 0]
    assert bfs_dist([[]], 0) == [0]
    rng = random.Random(21)
    for _ in range(200):
        n = rng.randint(1, 9)
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 14))]
        src = rng.randrange(n)
        want = [-1 if d == math.inf else d for d in _relax(n, [(u, v, 1) for u, v in edges], src)]
        assert bfs_dist(_adj(n, edges), src) == want, (n, edges, src)


def test_shortest_path():
    adj = [[1, 2], [3], [3], [4], []]
    assert shortest_path(adj, 0, 4) in ([0, 1, 3, 4], [0, 2, 3, 4])
    assert shortest_path(adj, 4, 0) == []
    assert shortest_path(adj, 2, 2) == [2]
    assert shortest_path([[1], [0]], 1, 0) == [1, 0], "node 0 is falsy: compare parents with `is None`"
    rng = random.Random(21)
    for _ in range(200):
        n = rng.randint(1, 9)
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 14))]
        adj = _adj(n, edges)
        src, dst = rng.randrange(n), rng.randrange(n)
        d = _relax(n, [(u, v, 1) for u, v in edges], src)[dst]
        path = shortest_path(adj, src, dst)
        if d == math.inf:
            assert path == [], (adj, src, dst, path)
        else:
            assert len(path) == d + 1 and path[0] == src and path[-1] == dst, (adj, src, dst, path)
            assert all(b in adj[a] for a, b in zip(path, path[1:])), f"{path} uses a missing edge"


def test_count_islands():
    assert count_islands(['##..', '#..#', '..##']) == 2
    assert count_islands(['#.#', '.#.', '#.#']) == 5, "diagonal cells aren't connected"
    assert count_islands([]) == 0
    assert count_islands(['....']) == 0
    rng = random.Random(21)
    for _ in range(150):
        R, C = rng.randint(1, 6), rng.randint(1, 6)
        g = [''.join(rng.choice('#.') for _ in range(C)) for _ in range(R)]
        assert count_islands(g) == _islands_ref(g), g
    try:
        got = count_islands(_snake(41, 61))
    except RecursionError:
        raise AssertionError("recursion went one level per cell: use an explicit stack or a queue") from None
    assert got == 1


def test_grid_steps():
    assert grid_steps(['..', '#.'], (0, 0), (1, 1)) == 2
    assert grid_steps(['...', '.#.', '...'], (0, 0), (2, 2)) == 4
    assert grid_steps(['.'], (0, 0), (0, 0)) == 0
    assert grid_steps(['.#.'], (0, 0), (0, 2)) == -1, \
        "check bounds before indexing: grid[r][c - 1] with c == 0 wraps to the last column"
    assert grid_steps(['.', '#', '.'], (0, 0), (2, 0)) == -1, "row -1 is the last row: check bounds"
    rng = random.Random(21)
    for _ in range(150):
        R, C = rng.randint(1, 6), rng.randint(1, 6)
        g = [''.join(rng.choice('..#') for _ in range(C)) for _ in range(R)]
        cells = [(r, c) for r in range(R) for c in range(C) if g[r][c] == '.']
        if cells:
            s, t = rng.choice(cells), rng.choice(cells)
            assert grid_steps(g, s, t) == _grid_ref(g, s, t), (g, s, t)


def test_nearest_source():
    grid = [[1, 0, 0], [0, 0, 0], [0, 0, 1]]
    assert nearest_source(grid) == [[0, 1, 2], [1, 2, 1], [2, 1, 0]]
    assert grid == [[1, 0, 0], [0, 0, 0], [0, 0, 1]], "don't modify the input grid"
    assert nearest_source([[0, 0], [0, 0]]) == [[-1, -1], [-1, -1]]
    assert nearest_source([[1]]) == [[0]]
    rng = random.Random(21)
    for _ in range(100):
        R, C = rng.randint(1, 7), rng.randint(1, 7)
        g = [[int(rng.random() < 0.15) for _ in range(C)] for _ in range(R)]
        srcs = [(r, c) for r in range(R) for c in range(C) if g[r][c]]
        want = [[min((abs(r - a) + abs(c - b) for a, b in srcs), default=-1) for c in range(C)]
                for r in range(R)]
        assert nearest_source(g) == want, g


def test_has_cycle_directed():
    assert has_cycle_directed(3, [(0, 1), (1, 2)]) is False
    assert has_cycle_directed(3, [(0, 1), (1, 2), (2, 0)]) is True
    assert has_cycle_directed(1, [(0, 0)]) is True, "a self-loop is a cycle"
    assert has_cycle_directed(4, [(0, 1), (0, 2), (1, 3), (2, 3)]) is False, \
        "reaching a node twice isn't a cycle unless it's still on the current path"
    assert has_cycle_directed(4, [(0, 1), (2, 3), (3, 2)]) is True, "check every component"
    assert has_cycle_directed(0, []) is False
    rng = random.Random(21)
    for _ in range(200):
        n = rng.randint(1, 7)
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 10))]
        assert has_cycle_directed(n, edges) == _has_cycle_ref(n, edges), (n, edges)
    try:
        got = has_cycle_directed(3000, [(i, i + 1) for i in range(2999)])
    except RecursionError:
        raise AssertionError("recursion went one level per node: use an explicit stack or Kahn's algorithm") from None
    assert got is False


def test_topo_order():
    edges = [(0, 1), (0, 2), (1, 3), (2, 3)]
    _check_topo(4, edges, topo_order(4, edges))
    assert topo_order(3, [(0, 1), (1, 2), (2, 0)]) is None
    assert topo_order(2, [(1, 1)]) is None, "a self-loop is a cycle"
    _check_topo(4, [(3, 1)], topo_order(4, [(3, 1)]))
    assert topo_order(0, []) == []
    rng = random.Random(21)
    for _ in range(200):
        n = rng.randint(1, 8)
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 12))]
        order = topo_order(n, edges)
        if _has_cycle_ref(n, edges):
            assert order is None, (n, edges, order)
        else:
            _check_topo(n, edges, order)
    try:
        order = topo_order(3000, [(i, i + 1) for i in range(2999)])
    except RecursionError:
        raise AssertionError("recursion went one level per node: Kahn's algorithm needs none") from None
    assert order == list(range(3000))


def test_is_bipartite():
    assert is_bipartite(4, [(0, 1), (1, 2), (2, 3), (3, 0)]) is True
    assert is_bipartite(3, [(0, 1), (1, 2), (2, 0)]) is False
    assert is_bipartite(5, [(0, 1), (2, 3), (3, 4), (4, 2)]) is False, \
        "color every component, not just the one containing node 0"
    assert is_bipartite(3, []) is True and is_bipartite(0, []) is True
    rng = random.Random(21)
    for _ in range(200):
        n = rng.randint(1, 8)
        pairs = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 10))]
        edges = [(u, v) for u, v in pairs if u != v]
        assert is_bipartite(n, edges) == _bipartite_ref(n, edges), (n, edges)


def test_dijkstra():
    edges = [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5)]
    assert dijkstra(4, edges, 0) == [0, 3, 1, 4]
    assert dijkstra(3, [(0, 1, 0), (1, 2, 0)], 0) == [0, 0, 0]
    assert dijkstra(3, [(1, 2, 7)], 0) == [0, math.inf, math.inf], "unreachable nodes stay math.inf"
    assert dijkstra(2, [(0, 1, 5), (0, 1, 2)], 0) == [0, 2], "parallel edges: the cheaper one wins"
    rng = random.Random(21)
    for _ in range(200):
        n = rng.randint(1, 8)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 9)) for _ in range(rng.randint(0, 16))]
        src = rng.randrange(n)
        assert dijkstra(n, edges, src) == _relax(n, edges, src), (n, edges, src)


def test_zero_one_bfs():
    edges = [(0, 1, 1), (0, 2, 0), (2, 1, 0), (1, 3, 1)]
    assert zero_one_bfs(4, edges, 0) == [0, 0, 0, 1]
    assert zero_one_bfs(2, [], 1) == [math.inf, 0]
    rng = random.Random(21)
    for _ in range(200):
        n = rng.randint(1, 8)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 1)) for _ in range(rng.randint(0, 16))]
        src = rng.randrange(n)
        assert zero_one_bfs(n, edges, src) == _relax(n, edges, src), (n, edges, src)


def test_cheapest_within_k():
    edges = [(0, 1, 1), (1, 2, 1), (0, 2, 5)]
    assert cheapest_within_k(3, edges, 0, 2, 2) == 2
    assert cheapest_within_k(3, edges, 0, 2, 1) == 5, \
        "one round chained two edges: relax from a copy of the previous round's prices"
    assert cheapest_within_k(3, edges, 0, 2, 0) == -1
    assert cheapest_within_k(3, edges, 1, 1, 0) == 0
    assert cheapest_within_k(2, [(1, 0, 1)], 0, 1, 5) == -1
    rng = random.Random(21)
    for _ in range(200):
        n = rng.randint(1, 6)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 9)) for _ in range(rng.randint(0, 7))]
        src, dst, k = rng.randrange(n), rng.randrange(n), rng.randint(0, 3)
        assert cheapest_within_k(n, edges, src, dst, k) == _cheapest_ref(n, edges, src, dst, k), \
            (n, edges, src, dst, k)


def test_word_steps():
    words = ['cord', 'card', 'ward', 'warm', 'worm', 'word']
    assert word_steps('cold', 'warm', words) == 4
    assert word_steps('cold', 'cold', []) == 0
    assert word_steps('cold', 'warm', ['cord', 'card', 'ward']) == -1, "the goal must be in words"
    assert word_steps('ab', 'cd', ['cb', 'cd', 'ad']) == 2
    rng = random.Random(21)
    for _ in range(200):
        L = rng.randint(1, 3)
        pool = [''.join(rng.choice('abc') for _ in range(L)) for _ in range(rng.randint(0, 12))]
        start = ''.join(rng.choice('abc') for _ in range(L))
        goal = ''.join(rng.choice('abc') for _ in range(L))
        assert word_steps(start, goal, pool) == _word_ref(start, goal, pool), (start, goal, pool)


def test_min_steps_with_breaks():
    assert min_steps_with_breaks(['...', '.#.', '...'], 0) == 4
    assert min_steps_with_breaks(['.#.', '###', '.#.'], 0) == -1
    assert min_steps_with_breaks(['.#.', '###', '.#.'], 1) == -1
    assert min_steps_with_breaks(['.#.', '###', '.#.'], 2) == 4
    assert min_steps_with_breaks(['.'], 0) == 0
    assert min_steps_with_breaks(['..###', '#..#.'], 1) == 5, \
        "a cell reached first with more walls used blocked a better route: visited must include walls_used"
    rng = random.Random(21)
    for _ in range(150):
        R, C = rng.choice([(2, 2), (2, 3), (3, 3), (2, 5), (3, 4)])
        g = [''.join(rng.choice('..#') for _ in range(C)) for _ in range(R)]
        g[0] = '.' + g[0][1:]
        g[-1] = g[-1][:-1] + '.'
        k = rng.randint(0, 2)
        assert min_steps_with_breaks(g, k) == _breaks_ref(g, k), (g, k)
