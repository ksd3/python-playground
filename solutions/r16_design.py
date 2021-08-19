"""R16 - Design builds (reference solutions)

Compare after you've made your own attempt. Run: python check.py 16 -s
"""
import random
from bisect import bisect_right
from collections import OrderedDict, defaultdict
from heapq import heappop, heappush

PREDICT = r"""
>>> od = OrderedDict.fromkeys('abc')
>>> od.move_to_end('a')
>>> list(od)
['b', 'c', 'a']
>>> od.popitem(last=False)
('b', None)
>>> od.move_to_end('c', last=False)
>>> list(od)
['c', 'a']

>>> d = {'a': 1, 'b': 2}
>>> d['a'] = 3
>>> list(d)
['a', 'b']
>>> del d['a']; d['a'] = 4
>>> list(d)
['b', 'a']

>>> d = {}
>>> for k in 'xyz':
...     d[k] = k.upper()
>>> d['x'] = d.pop('x')
>>> next(iter(d)), list(d)
('y', ['y', 'z', 'x'])

>>> items = ['a', 'b', 'c', 'd']
>>> i = items.index('b')
>>> items[i] = items[-1]
>>> items.pop()
'd'
>>> items
['a', 'd', 'c']

>>> items, pos = ['a', 'b'], {'a': 0, 'b': 1}
>>> i, last = pos.pop('b'), items[-1]
>>> items[i] = last; pos[last] = i
>>> items.pop()
'b'
>>> pos
{'a': 0, 'b': 1}

>>> lo = []
>>> for x in [5, 1, 9]:
...     heappush(lo, -x)
>>> -lo[0], sorted(-v for v in lo)
(9, [1, 5, 9])

>>> h = [3, 5]
>>> heappushpop(h, 1), h
(1, [3, 5])
>>> h = [3, 5]
>>> heapreplace(h, 1), h
(3, [1, 5])

>>> times, vals = [1, 4, 9], ['a', 'b', 'c']
>>> def at(t):
...     i = bisect_right(times, t)
...     return vals[i - 1] if i else ''
>>> [at(t) for t in (0, 1, 5, 9, 20)]
['', 'a', 'b', 'c', 'c']

>>> inbox, outbox = [1, 2, 3], []
>>> while inbox:
...     outbox.append(inbox.pop())
>>> outbox
[3, 2, 1]
>>> outbox, outbox.pop()
([3, 2], 1)

>>> st = []
>>> for x in [5, 3, 7, 2]:
...     st.append((x, min(x, st[-1][1]) if st else x))
>>> st
[(5, 5), (3, 3), (7, 3), (2, 2)]
>>> st.pop(); st[-1][1]
(2, 2)
3

>>> root = {}
>>> for w in ['to', 'tea']:
...     node = root
...     for ch in w:
...         node = node.setdefault(ch, {})
...     node['$'] = True
>>> root
{'t': {'o': {'$': True}, 'e': {'a': {'$': True}}}}

>>> Trie = lambda: defaultdict(Trie)
>>> t = Trie()
>>> t['a']['b']['$'] = True
>>> 'a' in t, 'b' in t, 'x' in t['a']
(True, False, False)
>>> _ = t['q']
>>> 'q' in t
True

>>> tokens = iter('1 2 # # 3 # #'.split())
>>> next(tokens), next(tokens), next(tokens)
('1', '2', '#')
>>> list(tokens)
['#', '3', '#', '#']

>>> ops = ['append', 'append', 'pop', '__len__']
>>> args = [[1], [2], [], []]
>>> s = []
>>> [getattr(s, op)(*a) for op, a in zip(ops, args)]
[None, None, 2, 1]

>>> class N:
...     def __init__(self, k):
...         self.k, self.prev, self.next = k, None, None
>>> head, tail = N('H'), N('T')
>>> head.next, tail.prev = tail, head
>>> x = N('x')
>>> x.prev, x.next = head, head.next
>>> head.next.prev = x; head.next = x
>>> [head.k, head.next.k, head.next.next.k, tail.prev.k]
['H', 'x', 'T', 'x']

>>> class N:
...     def __init__(self, k):
...         self.k, self.prev, self.next = k, None, None
>>> head, tail = N('H'), N('T')
>>> head.next, tail.prev = tail, head
>>> x = N('x')
>>> x.prev, x.next = head, head.next
>>> head.next = x; head.next.prev = x
>>> tail.prev.k, x.prev.k
('H', 'x')

>>> import random
>>> random.seed(0); a = [random.choice('abc') for _ in range(5)]
>>> random.seed(0); b = [random.choice('abc') for _ in range(5)]
>>> a == b
True
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class MinStack:
    def __init__(self):
        self._items = []            # (value, min of everything at or below it)

    def push(self, x):
        low = min(x, self._items[-1][1]) if self._items else x
        self._items.append((x, low))

    def pop(self):
        return self._items.pop()[0]

    def top(self):
        return self._items[-1][0]

    def get_min(self):
        return self._items[-1][1]

    def __len__(self):
        return len(self._items)


class TwoStackQueue:
    def __init__(self):
        self._in, self._out = [], []

    def push(self, x):
        self._in.append(x)

    def _front_ready(self):
        if not self._out:           # only refill when empty: each item moves at most once
            while self._in:
                self._out.append(self._in.pop())
        if not self._out:
            raise IndexError("queue is empty")

    def pop(self):
        self._front_ready()
        return self._out.pop()

    def peek(self):
        self._front_ready()
        return self._out[-1]

    def empty(self):
        return not (self._in or self._out)

    def __len__(self):
        return len(self._in) + len(self._out)


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self._data = OrderedDict()

    def get(self, key):
        if key not in self._data:
            return -1
        self._data.move_to_end(key)
        return self._data[key]

    def put(self, key, value):
        self._data[key] = value
        self._data.move_to_end(key)
        if len(self._data) > self.capacity:
            self._data.popitem(last=False)

    def __len__(self):
        return len(self._data)


class _Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key=None, value=None):
        self.key, self.value = key, value
        self.prev = self.next = None


class LinkedLRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self._map = {}
        # sentinels: every real node always has both neighbours, so no None checks
        self._head, self._tail = _Node(), _Node()
        self._head.next, self._tail.prev = self._tail, self._head

    def _unlink(self, node):
        node.prev.next, node.next.prev = node.next, node.prev

    def _push_front(self, node):
        node.prev, node.next = self._head, self._head.next
        self._head.next.prev = node         # before head.next changes
        self._head.next = node

    def get(self, key):
        node = self._map.get(key)
        if node is None:
            return -1
        self._unlink(node)
        self._push_front(node)
        return node.value

    def put(self, key, value):
        node = self._map.get(key)
        if node is not None:
            node.value = value
            self._unlink(node)
        else:
            node = self._map[key] = _Node(key, value)
            if len(self._map) > self.capacity:
                lru = self._tail.prev
                self._unlink(lru)
                del self._map[lru.key]
        self._push_front(node)

    def __len__(self):
        return len(self._map)


class RandomPickSet:
    def __init__(self):
        self._items = []
        self._pos = {}

    def insert(self, x):
        if x in self._pos:
            return False
        self._pos[x] = len(self._items)
        self._items.append(x)
        return True

    def remove(self, x):
        i = self._pos.pop(x, None)
        if i is None:
            return False
        last = self._items.pop()
        if i < len(self._items):            # x wasn't the last one: move the last into its slot
            self._items[i] = last
            self._pos[last] = i
        return True

    def get_random(self):
        return random.choice(self._items)

    def __len__(self):
        return len(self._items)

    def __contains__(self, x):
        return x in self._pos


class _TrieNode:
    __slots__ = ("children", "end", "count")

    def __init__(self):
        self.children = {}
        self.end = False
        self.count = 0                      # words at or below this node


class Trie:
    def __init__(self):
        self.root = _TrieNode()

    def _find(self, prefix):
        node = self.root
        for ch in prefix:
            node = node.children.get(ch)
            if node is None:
                return None
        return node

    def insert(self, word):
        if self.search(word):
            return
        node = self.root
        node.count += 1
        for ch in word:
            child = node.children.get(ch)
            if child is None:
                child = node.children[ch] = _TrieNode()
            node = child
            node.count += 1
        node.end = True

    def search(self, word):
        node = self._find(word)
        return node is not None and node.end

    def starts_with(self, prefix):
        node = self._find(prefix)
        return node is not None and node.count > 0

    def count_prefix(self, prefix):
        node = self._find(prefix)
        return node.count if node else 0

    def words_with_prefix(self, prefix):
        out = []

        def walk(node, path):
            if node.end:
                out.append(path)
            for ch, child in node.children.items():
                walk(child, path + ch)

        node = self._find(prefix)
        if node:
            walk(node, prefix)
        return sorted(out)


class DictTrie:
    END = "$"

    def __init__(self):
        self.root = {}

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node[self.END] = True

    def _walk(self, s):
        node = self.root
        for ch in s:
            node = node.get(ch)
            if node is None:
                return None
        return node

    def search(self, word):
        node = self._walk(word)
        return node is not None and self.END in node

    def starts_with(self, prefix):
        node = self._walk(prefix)
        return bool(node)                   # every node made by insert is non-empty


class VersionedStore:
    def __init__(self):
        self._times = defaultdict(list)
        self._values = defaultdict(list)

    def set(self, key, value, timestamp):
        self._times[key].append(timestamp)
        self._values[key].append(value)

    def get(self, key, timestamp):
        times = self._times.get(key)        # .get doesn't insert into a defaultdict
        if not times:
            return ""
        i = bisect_right(times, timestamp)
        return self._values[key][i - 1] if i else ""


class RunningMedian:
    def __init__(self):
        self._lo = []                       # max-heap of the lower half, negated
        self._hi = []                       # min-heap of the upper half

    def add(self, x):
        heappush(self._lo, -x)
        heappush(self._hi, -heappop(self._lo))      # largest of the low half moves up
        if len(self._hi) > len(self._lo):
            heappush(self._lo, -heappop(self._hi))  # keep len(lo) == len(hi) or one more

    def median(self):
        if not self._lo:
            raise ValueError("median of an empty stream")
        if len(self._lo) > len(self._hi):
            return -self._lo[0]
        return (-self._lo[0] + self._hi[0]) / 2


class TreeCodec:
    def serialize(self, root):
        out, stack = [], [root]
        while stack:
            node = stack.pop()
            if node is None:
                out.append("#")
            else:
                out.append(str(node.val))
                stack.append(node.right)
                stack.append(node.left)     # pushed last, so it's written first (preorder)
        return " ".join(out)

    def deserialize(self, data):
        tokens = iter(data.split())

        def build():
            tok = next(tokens)
            if tok == "#":
                return None
            node = TreeNode(int(tok))
            node.left = build()
            node.right = build()
            return node

        return build()
