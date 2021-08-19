"""R22 - Union-Find, Trie, Fenwick tree (reference solutions)

Compare after you've made your own attempt. Run: python check.py 22 -s
"""

PREDICT = r"""
>>> [i & -i for i in range(1, 9)]
[1, 2, 1, 4, 1, 2, 1, 8]

>>> 0 & -0, 6 & -6, 12 & -12
(0, 2, 4)

>>> i, path = 5, []
>>> while i <= 16:
...     path.append(i)
...     i += i & -i
>>> path
[5, 6, 8, 16]

>>> i, path = 7, []
>>> while i > 0:
...     path.append(i)
...     i -= i & -i
>>> path
[7, 6, 4]

>>> parent = list(range(5))
>>> def find(x):
...     while parent[x] != x:
...         x = parent[x]
...     return x
>>> parent[0] = 1; parent[1] = 2; parent[3] = 4
>>> [find(x) for x in range(5)]
[2, 2, 2, 4, 4]

>>> parent = list(range(4))
>>> def find(x):
...     while parent[x] != x:
...         x = parent[x]
...     return x
>>> def bad_union(a, b):
...     parent[a] = b
>>> bad_union(0, 1); bad_union(0, 2)
>>> find(1) == find(2), parent
(False, [2, 1, 2, 3])

>>> parent = [1, 2, 3, 3]
>>> def find(x):
...     if parent[x] != x:
...         parent[x] = find(parent[x])
...     return parent[x]
>>> find(0), parent
(3, [3, 3, 3, 3])

>>> parent = [1, 2, 3, 4, 4]
>>> def find(x):
...     while parent[x] != x:
...         parent[x] = parent[parent[x]]
...         x = parent[x]
...     return x
>>> find(0), parent
(4, [2, 2, 4, 4, 4])

>>> parent = {}
>>> def find(x):
...     parent.setdefault(x, x)
...     while parent[x] != x:
...         x = parent[x]
...     return x
>>> find('b'), find('a')
('b', 'a')
>>> parent['b'] = 'a'
>>> find('b'), parent
('a', {'b': 'a', 'a': 'a'})
>>> parent['c'] = 'd'
>>> find('c')
KeyError

>>> edges = [(0, 2, 3), (1, 2, 1), (0, 1, 3)]
>>> sorted(edges)
[(0, 1, 3), (0, 2, 3), (1, 2, 1)]
>>> sorted(edges, key=lambda e: e[2])
[(1, 2, 1), (0, 2, 3), (0, 1, 3)]

>>> root = {}
>>> for word in ['to', 'tea']:
...     node = root
...     for ch in word:
...         node = node.setdefault(ch, {})
...     node['$'] = True
>>> root
{'t': {'o': {'$': True}, 'e': {'a': {'$': True}}}}

>>> Trie = lambda: defaultdict(Trie)
>>> t = Trie()
>>> t['c']['a']['t']['$'] = True
>>> 'd' in t, len(t['d']['o']), 'd' in t
(False, 0, True)

>>> words = sorted(['cat', 'car', 'dog', 'cart'])
>>> lo = bisect_left(words, 'car')
>>> hi = bisect_left(words, 'car￿')
>>> words, words[lo:hi]
(['car', 'cart', 'cat', 'dog'], ['car', 'cart'])

>>> xs = [40, 10, 40, 1000000, 10]
>>> rank = {v: i for i, v in enumerate(sorted(set(xs)), 1)}
>>> rank, [rank[x] for x in xs]
({10: 1, 40: 2, 1000000: 3}, [2, 1, 2, 3, 1])
"""

import math


class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.count = n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]   # path halving
            x = self.parent[x]
        return x

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a                                 # smaller tree goes under the bigger
        self.size[a] += self.size[b]
        self.count -= 1
        return True

    def connected(self, a, b):
        return self.find(a) == self.find(b)

    def size_of(self, x):
        return self.size[self.find(x)]


def count_groups(n, edges):
    dsu = DSU(n)
    for u, v in edges:
        dsu.union(u, v)
    return dsu.count


def first_cycle_edge(edges):
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            return (a, b)
        parent[ra] = rb
    return None


def mst_weight(n, edges):
    dsu = DSU(n)
    total = 0
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        if dsu.union(u, v):
            total += w
    return total if dsu.count <= 1 else None


def compress(values):
    rank = {v: i for i, v in enumerate(sorted(set(values)), 1)}
    return [rank[v] for v in values]


class Fenwick:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)

    @classmethod
    def from_list(cls, values):
        fw = cls(len(values))
        tree = fw.tree
        for i, v in enumerate(values, 1):
            tree[i] += v                 # children (smaller i) already pushed into tree[i]
            parent = i + (i & -i)
            if parent <= fw.n:
                tree[parent] += tree[i]
        return fw

    def add(self, i, delta):
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i

    def prefix_sum(self, i):
        total = 0
        while i > 0:
            total += self.tree[i]
            i -= i & -i
        return total

    def range_sum(self, lo, hi):
        return self.prefix_sum(hi) - self.prefix_sum(lo - 1)


def count_smaller_after(nums):
    ranks = compress(nums)
    fw = Fenwick(len(set(nums)))
    out = []
    for r in reversed(ranks):
        out.append(fw.prefix_sum(r - 1))
        fw.add(r, 1)
    return out[::-1]


class _Node:
    __slots__ = ('children', 'end', 'count')

    def __init__(self):
        self.children = {}
        self.end = False
        self.count = 0                   # words that pass through this node


class Trie:
    def __init__(self):
        self.root = _Node()

    def _walk(self, s):
        node = self.root
        for ch in s:
            node = node.children.get(ch)
            if node is None:
                return None
        return node

    def insert(self, word):
        if self.contains(word):
            return
        node = self.root
        node.count += 1
        for ch in word:
            node = node.children.setdefault(ch, _Node())
            node.count += 1
        node.end = True

    def contains(self, word):
        node = self._walk(word)
        return node is not None and node.end

    def starts_with(self, prefix):
        node = self._walk(prefix)
        return node is not None and node.count > 0

    def count_prefix(self, prefix):
        node = self._walk(prefix)
        return node.count if node else 0

    def words_with_prefix(self, prefix):
        start = self._walk(prefix)
        if start is None:
            return []
        out, stack = [], [(start, prefix)]
        while stack:
            node, word = stack.pop()
            if node.end:
                out.append(word)
            for ch, child in node.children.items():
                stack.append((child, word + ch))
        return sorted(out)

    def match(self, pattern):
        frontier = [self.root]           # every node the pattern so far can reach
        for ch in pattern:
            if ch == '.':
                frontier = [c for node in frontier for c in node.children.values()]
            else:
                frontier = [node.children[ch] for node in frontier if ch in node.children]
            if not frontier:
                return False
        return any(node.end for node in frontier)

    def remove(self, word):
        if not self.contains(word):
            return False
        node = self.root
        node.count -= 1
        for ch in word:
            child = node.children[ch]
            child.count -= 1
            if child.count == 0:
                del node.children[ch]    # nothing else uses this branch: prune it
                return True
            node = child
        node.end = False
        return True


class RangeMin:
    def __init__(self, values):
        self.n = n = len(values)
        self.tree = [math.inf] * n + list(values)
        for i in range(n - 1, 0, -1):
            self.tree[i] = min(self.tree[2 * i], self.tree[2 * i + 1])

    def update(self, i, value):
        i += self.n
        self.tree[i] = value
        while i > 1:
            i //= 2
            self.tree[i] = min(self.tree[2 * i], self.tree[2 * i + 1])

    def query(self, lo, hi):
        res = math.inf
        lo, hi = lo + self.n, hi + self.n + 1      # half-open [lo, hi) over the leaves
        while lo < hi:
            if lo & 1:
                res = min(res, self.tree[lo])
                lo += 1
            if hi & 1:
                hi -= 1
                res = min(res, self.tree[hi])
            lo //= 2
            hi //= 2
        return res
