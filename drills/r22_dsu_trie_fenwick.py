"""R22 - Union-Find, Trie, Fenwick tree

Union-Find keeps one parent pointer per element and find walks up to the
root; path compression plus union by size make both operations nearly O(1).
When union finds the two already share a root, that edge closes a cycle. A
trie stores strings one character per level: a node is a dict of children
plus an end flag. A Fenwick tree keeps partial sums at indices whose lowest
set bit says how far back each one reaches: updates climb with i += i & -i,
queries descend with i -= i & -i, and indices start at 1, not 0.

Part 1 - Predict. Each block in PREDICT is a REPL session. Replace every ???
with exactly what Python prints: expression values are echoed the way the REPL
echoes them, and a line that raises prints just the exception name (TypeError).

Part 2 - Drills. Implement every function until `python check.py 22` is green.
Don't edit the tests at the bottom; add your own test_* functions if you like.

Unlocks: connectivity and grouping, cheapest networks, cycle-closing edges,
prefix searches over word lists, and running counts and sums over ranges.
"""

PREDICT = r"""
>>> [i & -i for i in range(1, 9)]
???

>>> 0 & -0, 6 & -6, 12 & -12
???

>>> i, path = 5, []
>>> while i <= 16:
...     path.append(i)
...     i += i & -i
>>> path
???

>>> i, path = 7, []
>>> while i > 0:
...     path.append(i)
...     i -= i & -i
>>> path
???

>>> parent = list(range(5))
>>> def find(x):
...     while parent[x] != x:
...         x = parent[x]
...     return x
>>> parent[0] = 1; parent[1] = 2; parent[3] = 4
>>> [find(x) for x in range(5)]
???

>>> parent = list(range(4))
>>> def find(x):
...     while parent[x] != x:
...         x = parent[x]
...     return x
>>> def bad_union(a, b):
...     parent[a] = b
>>> bad_union(0, 1); bad_union(0, 2)
>>> find(1) == find(2), parent
???

>>> parent = [1, 2, 3, 3]
>>> def find(x):
...     if parent[x] != x:
...         parent[x] = find(parent[x])
...     return parent[x]
>>> find(0), parent
???

>>> parent = [1, 2, 3, 4, 4]
>>> def find(x):
...     while parent[x] != x:
...         parent[x] = parent[parent[x]]
...         x = parent[x]
...     return x
>>> find(0), parent
???

>>> parent = {}
>>> def find(x):
...     parent.setdefault(x, x)
...     while parent[x] != x:
...         x = parent[x]
...     return x
>>> find('b'), find('a')
???
>>> parent['b'] = 'a'
>>> find('b'), parent
???
>>> parent['c'] = 'd'
>>> find('c')
???

>>> edges = [(0, 2, 3), (1, 2, 1), (0, 1, 3)]
>>> sorted(edges)
???
>>> sorted(edges, key=lambda e: e[2])
???

>>> root = {}
>>> for word in ['to', 'tea']:
...     node = root
...     for ch in word:
...         node = node.setdefault(ch, {})
...     node['$'] = True
>>> root
???

>>> Trie = lambda: defaultdict(Trie)
>>> t = Trie()
>>> t['c']['a']['t']['$'] = True
>>> 'd' in t, len(t['d']['o']), 'd' in t
???

>>> words = sorted(['cat', 'car', 'dog', 'cart'])
>>> lo = bisect_left(words, 'car')
>>> hi = bisect_left(words, 'car￿')
>>> words, words[lo:hi]
???

>>> xs = [40, 10, 40, 1000000, 10]
>>> rank = {v: i for i, v in enumerate(sorted(set(xs)), 1)}
>>> rank, [rank[x] for x in xs]
???
"""

import math


# ---------------------------------------------------------------- drills

class DSU:
    """Union-Find over the elements 0..n-1.

    DSU(n)            n groups of one; self.count == n
    find(x)           the root of x's group (a loop, not recursion)
    union(a, b)       merge the two groups: True if they were separate,
                      False if a and b were already connected
    connected(a, b)   True if a and b are in the same group
    size_of(x)        how many elements are in x's group
    self.count        the number of groups right now

    Use path compression (or halving) and union by size."""

    def __init__(self, n):
        raise NotImplementedError

    def find(self, x):
        raise NotImplementedError

    def union(self, a, b):
        raise NotImplementedError

    def connected(self, a, b):
        raise NotImplementedError

    def size_of(self, x):
        raise NotImplementedError


def count_groups(n, edges):
    """Return how many connected groups the undirected graph on 0..n-1 has.
    count_groups(5, [(0, 1), (1, 2), (3, 4)]) == 2"""
    raise NotImplementedError


def first_cycle_edge(edges):
    """edges join hashable labels (strings, tuples...) and arrive one at a time.
    Return the first edge whose two ends were already connected, or None. Use
    a dict-based Union-Find (parent.setdefault(x, x) adds new labels).
    first_cycle_edge([('a', 'b'), ('b', 'c'), ('c', 'a')]) == ('c', 'a')"""
    raise NotImplementedError


def mst_weight(n, edges):
    """edges are undirected (u, v, w) on nodes 0..n-1. Return the total weight
    of a minimum spanning tree, or None if the graph isn't connected (n <= 1
    gives 0). Kruskal: sort the edges by weight and keep every edge that joins
    two different groups."""
    raise NotImplementedError


def compress(values):
    """Replace each value by its rank among the distinct values, starting at 1;
    equal values share a rank. compress([40, 10, 40, 10**6]) == [2, 1, 2, 3]"""
    raise NotImplementedError


class Fenwick:
    """Fenwick (binary indexed) tree over indices 1..n.

    Fenwick(n)                n zeros
    Fenwick.from_list(vals)   vals[0] goes to index 1; build it in O(n)
    add(i, delta)             the value at index i grows by delta, O(log n)
    prefix_sum(i)             sum of indices 1..i (prefix_sum(0) == 0), O(log n)
    range_sum(lo, hi)         sum of indices lo..hi inclusive"""

    def __init__(self, n):
        raise NotImplementedError

    @classmethod
    def from_list(cls, values):
        raise NotImplementedError

    def add(self, i, delta):
        raise NotImplementedError

    def prefix_sum(self, i):
        raise NotImplementedError

    def range_sum(self, lo, hi):
        raise NotImplementedError


def count_smaller_after(nums):
    """Return out where out[i] counts the j > i with nums[j] < nums[i].
    O(n log n): walk from the right, compress the values to ranks, and ask a
    Fenwick tree how many smaller ranks you've already seen.
    count_smaller_after([3, 1, 4, 1, 5]) == [2, 0, 1, 0, 0]"""
    raise NotImplementedError


class Trie:
    """A set of lowercase words stored one character per level.

    insert(word)                add word (adding it again changes nothing)
    contains(word)              True if word was inserted
    starts_with(prefix)         True if some inserted word starts with prefix
    count_prefix(prefix)        how many inserted words start with prefix
    words_with_prefix(prefix)   those words, sorted
    match(pattern)              True if some word matches; '.' is any letter
    remove(word)                remove it: True if it was there, else False"""

    def __init__(self):
        raise NotImplementedError

    def insert(self, word):
        raise NotImplementedError

    def contains(self, word):
        raise NotImplementedError

    def starts_with(self, prefix):
        raise NotImplementedError

    def count_prefix(self, prefix):
        raise NotImplementedError

    def words_with_prefix(self, prefix):
        raise NotImplementedError

    def match(self, pattern):
        raise NotImplementedError

    def remove(self, word):
        raise NotImplementedError


class RangeMin:
    """Segment tree for range minimums over a list of numbers (0-indexed).

    RangeMin(values)   build in O(n)
    update(i, value)   set position i to value, O(log n)
    query(lo, hi)      min of positions lo..hi inclusive, O(log n)

    Iterative layout: the leaves live at tree[n:], and node i covers its
    children 2i and 2i + 1."""

    def __init__(self, values):
        raise NotImplementedError

    def update(self, i, value):
        raise NotImplementedError

    def query(self, lo, hi):
        raise NotImplementedError


# ---------------------------------------------------------------- tests (don't edit)

import random
from bisect import bisect_left, insort


def _groups_ref(n, edges):
    label = list(range(n))
    changed = True
    while changed:
        changed = False
        for u, v in edges:
            low = min(label[u], label[v])
            if label[u] != low or label[v] != low:
                label[u] = label[v] = low
                changed = True
    return len(set(label))


def _first_cycle_ref(edges):
    for i, (a, b) in enumerate(edges):
        seen, stack = {a}, [a]
        while stack:
            u = stack.pop()
            for x, y in edges[:i]:
                for p, q in ((x, y), (y, x)):
                    if p == u and q not in seen:
                        seen.add(q)
                        stack.append(q)
        if b in seen:
            return (a, b)
    return None


def _mst_ref(n, edges):
    """Prim's algorithm on a dict of cheapest edges."""
    if n <= 1:
        return 0
    best = {}
    for u, v, w in edges:
        if u != v:
            for a, b in ((u, v), (v, u)):
                best[a, b] = min(best.get((a, b), math.inf), w)
    inside, total = {0}, 0
    while len(inside) < n:
        options = [(w, b) for (a, b), w in best.items() if a in inside and b not in inside]
        if not options:
            return None
        w, b = min(options)
        inside.add(b)
        total += w
    return total


def _smaller_ref(nums):
    seen, out = [], []
    for x in reversed(nums):
        out.append(bisect_left(seen, x))
        insort(seen, x)
    return out[::-1]


def test_dsu():
    d = DSU(5)
    assert d.count == 5 and d.size_of(3) == 1
    assert d.union(0, 1) is True and d.union(1, 2) is True
    assert d.union(0, 2) is False, "0 and 2 were already connected"
    assert d.connected(0, 2) and not d.connected(0, 3)
    assert d.count == 3 and d.size_of(2) == 3 and d.size_of(4) == 1
    assert d.find(0) == d.find(1) == d.find(2) != d.find(3)
    rng = random.Random(22)
    for _ in range(50):
        n = rng.randint(1, 12)
        d, group = DSU(n), list(range(n))
        for _ in range(15):
            a, b = rng.randrange(n), rng.randrange(n)
            ga, gb = group[a], group[b]
            assert d.union(a, b) == (ga != gb)
            group = [ga if g == gb else g for g in group]
            x = rng.randrange(n)
            assert d.size_of(x) == group.count(group[x])
        assert d.count == len(set(group))
        for a in range(n):
            for b in range(n):
                assert d.connected(a, b) == (group[a] == group[b])
    d = DSU(20000)
    try:
        for i in range(19999):
            d.union(i, i + 1)
        assert d.count == 1 and d.size_of(0) == 20000
        assert all(d.find(i) == d.find(0) for i in range(0, 20000, 97))
    except RecursionError:
        raise AssertionError("find recursed too deep: union by size keeps trees shallow, or loop instead") from None


def test_count_groups():
    assert count_groups(5, [(0, 1), (1, 2), (3, 4)]) == 2
    assert count_groups(3, []) == 3
    assert count_groups(0, []) == 0
    assert count_groups(4, [(0, 1), (1, 0), (2, 2)]) == 3, "repeated edges and self-loops change nothing"
    rng = random.Random(22)
    for _ in range(100):
        n = rng.randint(1, 10)
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 10))]
        assert count_groups(n, edges) == _groups_ref(n, edges), (n, edges)


def test_first_cycle_edge():
    assert first_cycle_edge([('a', 'b'), ('b', 'c'), ('c', 'a')]) == ('c', 'a')
    assert first_cycle_edge([('a', 'b'), ('c', 'd')]) is None
    assert first_cycle_edge([]) is None
    assert first_cycle_edge([('x', 'x')]) == ('x', 'x'), "a self-loop closes a cycle at once"
    assert first_cycle_edge([((0, 0), (0, 1)), ((0, 1), (0, 0))]) == ((0, 1), (0, 0))
    edges = [('a', 'b'), ('c', 'd'), ('b', 'd'), ('a', 'c'), ('a', 'd')]
    assert first_cycle_edge(edges) == ('a', 'c')
    rng = random.Random(22)
    for _ in range(100):
        labels = 'abcdefg'[:rng.randint(1, 7)]
        edges = [(rng.choice(labels), rng.choice(labels)) for _ in range(rng.randint(0, 8))]
        assert first_cycle_edge(edges) == _first_cycle_ref(edges), edges


def test_mst_weight():
    edges = [(0, 1, 4), (0, 2, 1), (1, 2, 2), (1, 3, 5), (2, 3, 8)]
    assert mst_weight(4, edges) == 8
    assert mst_weight(3, [(0, 1, 1)]) is None, "node 2 can't be reached"
    assert mst_weight(1, []) == 0 and mst_weight(0, []) == 0
    assert mst_weight(2, [(0, 1, 5), (0, 1, 2), (1, 1, 0)]) == 2
    rng = random.Random(22)
    for _ in range(100):
        n = rng.randint(1, 7)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 9)) for _ in range(rng.randint(0, 12))]
        assert mst_weight(n, edges) == _mst_ref(n, edges), (n, edges)


def test_compress():
    assert compress([40, 10, 40, 10**6]) == [2, 1, 2, 3]
    assert compress([]) == []
    assert compress([-5, -5]) == [1, 1]
    assert compress(['b', 'a', 'c']) == [2, 1, 3]
    rng = random.Random(22)
    for _ in range(100):
        xs = [rng.randint(-10**9, 10**9) if rng.random() < 0.5 else rng.randint(0, 5)
              for _ in range(rng.randint(0, 12))]
        ranks = compress(xs)
        assert len(ranks) == len(xs)
        for i in range(len(xs)):
            for j in range(len(xs)):
                assert (xs[i] < xs[j]) == (ranks[i] < ranks[j]), (xs, ranks)
        assert sorted(set(ranks)) == list(range(1, len(set(xs)) + 1)), "ranks should be 1..m with no gaps"


def test_fenwick():
    f = Fenwick(8)
    f.add(3, 5)
    f.add(5, 2)
    assert f.prefix_sum(0) == 0 and f.prefix_sum(2) == 0 and f.prefix_sum(3) == 5
    assert f.prefix_sum(8) == 7, "updates must climb all the way to index n: loop while i <= n"
    assert f.range_sum(4, 5) == 2 and f.range_sum(3, 3) == 5
    f.add(8, -1)
    assert f.prefix_sum(8) == 6
    rng = random.Random(22)
    for _ in range(30):
        n = rng.randint(1, 40)
        f, vals = Fenwick(n), [0] * n
        for _ in range(60):
            if rng.random() < 0.5:
                i, delta = rng.randint(1, n), rng.randint(-9, 9)
                f.add(i, delta)
                vals[i - 1] += delta
            else:
                lo = rng.randint(1, n)
                hi = rng.randint(lo, n)
                assert f.range_sum(lo, hi) == sum(vals[lo - 1:hi]), (vals, lo, hi)
                assert f.prefix_sum(hi) == sum(vals[:hi])


def test_fenwick_from_list():
    vals = [3, -1, 4, 1, -5, 9, 2]
    f = Fenwick.from_list(vals)
    assert vals == [3, -1, 4, 1, -5, 9, 2], "don't modify the input list"
    assert [f.prefix_sum(i) for i in range(8)] == [0, 3, 2, 6, 7, 2, 11, 13]
    f.add(2, 10)
    assert f.range_sum(2, 3) == 13
    assert Fenwick.from_list([]).prefix_sum(0) == 0
    rng = random.Random(22)
    for _ in range(30):
        vals = [rng.randint(-50, 50) for _ in range(rng.randint(1, 60))]
        f = Fenwick.from_list(vals)
        assert [f.prefix_sum(i) for i in range(len(vals) + 1)] == [sum(vals[:i]) for i in range(len(vals) + 1)]


def test_count_smaller_after():
    assert count_smaller_after([3, 1, 4, 1, 5]) == [2, 0, 1, 0, 0]
    assert count_smaller_after([]) == []
    assert count_smaller_after([2, 2, 2]) == [0, 0, 0], "equal values aren't smaller"
    assert count_smaller_after([-1, -10**9, 10**9]) == [1, 0, 0]
    rng = random.Random(22)
    for _ in range(60):
        nums = [rng.randint(-5, 5) for _ in range(rng.randint(0, 15))]
        want = [sum(nums[j] < nums[i] for j in range(i + 1, len(nums))) for i in range(len(nums))]
        assert count_smaller_after(nums) == want, nums
    nums = [rng.randint(-10**9, 10**9) for _ in range(3000)]
    assert count_smaller_after(nums) == _smaller_ref(nums)


def test_trie():
    t = Trie()
    for w in ['car', 'cart', 'cat', 'dog']:
        t.insert(w)
    assert t.contains('car') and t.contains('cart') and t.contains('dog')
    assert not t.contains('ca'), "a prefix isn't a word unless it was inserted"
    assert not t.contains('carts') and not t.contains('')
    assert t.starts_with('ca') and t.starts_with('cart') and t.starts_with('')
    assert not t.starts_with('co') and not t.starts_with('carts')


def test_trie_count_prefix():
    t = Trie()
    for w in ['car', 'cart', 'cat', 'dog', 'car']:
        t.insert(w)
    assert t.count_prefix('ca') == 3, "inserting 'car' twice must count once"
    assert t.count_prefix('car') == 2 and t.count_prefix('d') == 1 and t.count_prefix('x') == 0
    assert t.count_prefix('') == 4


def test_trie_words_with_prefix():
    t = Trie()
    for w in ['car', 'cart', 'cat', 'dog', 'carbon']:
        t.insert(w)
    assert t.words_with_prefix('car') == ['car', 'carbon', 'cart']
    assert t.words_with_prefix('') == ['car', 'carbon', 'cart', 'cat', 'dog']
    assert t.words_with_prefix('cab') == [] and t.words_with_prefix('dogs') == []


def test_trie_match():
    t = Trie()
    for w in ['bad', 'dad', 'mad']:
        t.insert(w)
    assert t.match('bad') and t.match('.ad') and t.match('b..') and t.match('...')
    assert not t.match('pad') and not t.match('..') and not t.match('....') and not t.match('b.')
    rng = random.Random(22)
    for _ in range(40):
        words = {''.join(rng.choice('ab') for _ in range(rng.randint(1, 4))) for _ in range(rng.randint(0, 6))}
        t = Trie()
        for w in words:
            t.insert(w)
        for _ in range(10):
            p = ''.join(rng.choice('ab.') for _ in range(rng.randint(1, 4)))
            want = any(len(w) == len(p) and all(c in ('.', x) for c, x in zip(p, w)) for w in words)
            assert t.match(p) == want, (sorted(words), p)


def test_trie_remove():
    t = Trie()
    for w in ['car', 'cart', 'cat']:
        t.insert(w)
    assert t.remove('car') is True
    assert not t.contains('car') and t.contains('cart'), "removing a word must keep longer words on its path"
    assert t.remove('car') is False and t.remove('ca') is False and t.remove('dog') is False
    assert t.remove('cart') is True
    assert not t.starts_with('car') and t.starts_with('ca'), "prune or count, so dead branches stop matching"
    t.insert('car')
    assert t.contains('car') and t.count_prefix('car') == 1
    rng = random.Random(22)
    t, model = Trie(), set()
    for _ in range(400):
        w = ''.join(rng.choice('ab') for _ in range(rng.randint(1, 4)))
        roll = rng.random()
        if roll < 0.4:
            t.insert(w)
            model.add(w)
        elif roll < 0.7:
            assert t.remove(w) == (w in model), (sorted(model), w)
            model.discard(w)
        else:
            assert t.contains(w) == (w in model), (sorted(model), w)
            assert t.starts_with(w) == any(x.startswith(w) for x in model), (sorted(model), w)
            assert t.count_prefix(w) == sum(x.startswith(w) for x in model), (sorted(model), w)


def test_range_min():
    rm = RangeMin([5, 3, 8, 6, 1, 7])
    assert rm.query(0, 5) == 1 and rm.query(0, 2) == 3 and rm.query(2, 3) == 6 and rm.query(5, 5) == 7
    rm.update(4, 9)
    assert rm.query(0, 5) == 3 and rm.query(3, 5) == 6
    assert RangeMin([4]).query(0, 0) == 4
    rng = random.Random(22)
    for _ in range(30):
        n = rng.randint(1, 30)
        vals = [rng.randint(-50, 50) for _ in range(n)]
        rm = RangeMin(vals)
        for _ in range(40):
            if rng.random() < 0.4:
                i, v = rng.randrange(n), rng.randint(-50, 50)
                rm.update(i, v)
                vals[i] = v
            else:
                lo = rng.randrange(n)
                hi = rng.randint(lo, n - 1)
                assert rm.query(lo, hi) == min(vals[lo:hi + 1]), (vals, lo, hi)
