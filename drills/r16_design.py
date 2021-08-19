"""R16 - Design builds

A design build is a class whose methods get called in some sequence, each
with a complexity promise. Pick the representation first: which built-in
gives O(1) for each operation (list ends, dict lookups, heaps, OrderedDict
recency), and which extra structure pays for the rest (a stack of
(value, min) pairs, a value -> index map, two heaps, sentinel nodes in a
doubly linked list). Then write each method against that representation and
state its cost. The tests replay call sequences against simple models.

Part 1 - Predict. Each block in PREDICT is a REPL session. Replace every ???
with exactly what Python prints: expression values are echoed the way the REPL
echoes them, and a line that raises prints just the exception name (TypeError).

Part 2 - Drills. Implement every class until `python check.py 16` is green.
Don't edit the tests at the bottom; add your own test_* functions if you like.

Unlocks: stack/queue/cache/set designs with complexity guarantees, prefix
trees, versioned lookups, streaming medians, and tree serialization.
"""
import random
import statistics
from bisect import bisect_left, bisect_right
from collections import Counter, OrderedDict, defaultdict, deque
from heapq import heappop, heappush

PREDICT = r"""
>>> od = OrderedDict.fromkeys('abc')
>>> od.move_to_end('a')
>>> list(od)
???
>>> od.popitem(last=False)
???
>>> od.move_to_end('c', last=False)
>>> list(od)
???

>>> d = {'a': 1, 'b': 2}
>>> d['a'] = 3
>>> list(d)
???
>>> del d['a']; d['a'] = 4
>>> list(d)
???

>>> d = {}
>>> for k in 'xyz':
...     d[k] = k.upper()
>>> d['x'] = d.pop('x')
>>> next(iter(d)), list(d)
???

>>> items = ['a', 'b', 'c', 'd']
>>> i = items.index('b')
>>> items[i] = items[-1]
>>> items.pop()
???
>>> items
???

>>> items, pos = ['a', 'b'], {'a': 0, 'b': 1}
>>> i, last = pos.pop('b'), items[-1]
>>> items[i] = last; pos[last] = i
>>> items.pop()
???
>>> pos
???

>>> lo = []
>>> for x in [5, 1, 9]:
...     heappush(lo, -x)
>>> -lo[0], sorted(-v for v in lo)
???

>>> h = [3, 5]
>>> heappushpop(h, 1), h
???
>>> h = [3, 5]
>>> heapreplace(h, 1), h
???

>>> times, vals = [1, 4, 9], ['a', 'b', 'c']
>>> def at(t):
...     i = bisect_right(times, t)
...     return vals[i - 1] if i else ''
>>> [at(t) for t in (0, 1, 5, 9, 20)]
???

>>> inbox, outbox = [1, 2, 3], []
>>> while inbox:
...     outbox.append(inbox.pop())
>>> outbox
???
>>> outbox, outbox.pop()
???

>>> st = []
>>> for x in [5, 3, 7, 2]:
...     st.append((x, min(x, st[-1][1]) if st else x))
>>> st
???
>>> st.pop(); st[-1][1]
???

>>> root = {}
>>> for w in ['to', 'tea']:
...     node = root
...     for ch in w:
...         node = node.setdefault(ch, {})
...     node['$'] = True
>>> root
???

>>> Trie = lambda: defaultdict(Trie)
>>> t = Trie()
>>> t['a']['b']['$'] = True
>>> 'a' in t, 'b' in t, 'x' in t['a']
???
>>> _ = t['q']
>>> 'q' in t
???

>>> tokens = iter('1 2 # # 3 # #'.split())
>>> next(tokens), next(tokens), next(tokens)
???
>>> list(tokens)
???

>>> ops = ['append', 'append', 'pop', '__len__']
>>> args = [[1], [2], [], []]
>>> s = []
>>> [getattr(s, op)(*a) for op, a in zip(ops, args)]
???

>>> class N:
...     def __init__(self, k):
...         self.k, self.prev, self.next = k, None, None
>>> head, tail = N('H'), N('T')
>>> head.next, tail.prev = tail, head
>>> x = N('x')
>>> x.prev, x.next = head, head.next
>>> head.next.prev = x; head.next = x
>>> [head.k, head.next.k, head.next.next.k, tail.prev.k]
???

>>> class N:
...     def __init__(self, k):
...         self.k, self.prev, self.next = k, None, None
>>> head, tail = N('H'), N('T')
>>> head.next, tail.prev = tail, head
>>> x = N('x')
>>> x.prev, x.next = head, head.next
>>> head.next = x; head.next.prev = x
>>> tail.prev.k, x.prev.k
???

>>> import random
>>> random.seed(0); a = [random.choice('abc') for _ in range(5)]
>>> random.seed(0); b = [random.choice('abc') for _ in range(5)]
>>> a == b
???
"""


class TreeNode:
    """Given: a binary tree node."""

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ---------------------------------------------------------------- drills

class MinStack:
    """A stack that also reports its minimum, every operation O(1):
    push(x) -> None; pop() -> removes and returns the top; top() -> the top;
    get_min() -> the smallest item currently on the stack; len(stack).
    pop, top and get_min on an empty stack raise IndexError.
    Trick: store (value, min_so_far) pairs."""

    def __init__(self):
        raise NotImplementedError

    def push(self, x):
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError

    def top(self):
        raise NotImplementedError

    def get_min(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError


class TwoStackQueue:
    """A FIFO queue built from two lists used only as stacks (append and pop
    at the end; no deque, no pop(0), no slicing):
    push(x) -> None adds at the back; pop() -> removes and returns the front;
    peek() -> the front; empty() -> True/False; len(q).
    pop and peek on an empty queue raise IndexError.
    Amortized O(1): refill the out-stack only when it's empty."""

    def __init__(self):
        raise NotImplementedError

    def push(self, x):
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError

    def peek(self):
        raise NotImplementedError

    def empty(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError


class LRUCache:
    """A least-recently-used cache built on collections.OrderedDict.
    LRUCache(capacity) with capacity >= 1:
    - get(key) -> the value, or -1 if absent; a hit makes key the most recent
    - put(key, value) -> None; inserts or updates (an update also makes key the
      most recent); when over capacity, evict the least recently used key
    - len(cache) is the number of stored keys
    Every operation O(1)."""

    def __init__(self, capacity):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def put(self, key, value):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError


class LinkedLRUCache:
    """The same contract as LRUCache, built from a plain dict (key -> node)
    and your own doubly linked list with sentinel head and tail nodes: most
    recent next to the head, least recent next to the tail. Every operation
    O(1): unlink a node by rewiring its two neighbours; never walk the list.
    (No OrderedDict here.)"""

    def __init__(self, capacity):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def put(self, key, value):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError


class RandomPickSet:
    """A set with O(1) insert, remove and uniform random pick:
    - insert(x) -> True if x was added, False if it was already there
    - remove(x) -> True if x was removed, False if it wasn't there
    - get_random() -> a uniformly random member (use the random module)
    - len(s) and `x in s`
    Keep a list of members plus a dict member -> index. To remove, move the
    LAST member into the removed slot, then pop the end."""

    def __init__(self):
        raise NotImplementedError

    def insert(self, x):
        raise NotImplementedError

    def remove(self, x):
        raise NotImplementedError

    def get_random(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def __contains__(self, x):
        raise NotImplementedError


class Trie:
    """A prefix tree of words built from node objects (a small node class with
    a children dict and an end flag; __slots__ optional).
    - insert(word) -> None; inserting a word twice changes nothing
    - search(word) -> True if word was inserted
    - starts_with(prefix) -> True if some inserted word starts with prefix
      (the empty prefix matches only when the trie has a word)
    - count_prefix(prefix) -> how many distinct inserted words start with
      prefix, in O(len(prefix)): keep a word count on every node
    - words_with_prefix(prefix) -> those words, sorted"""

    def __init__(self):
        raise NotImplementedError

    def insert(self, word):
        raise NotImplementedError

    def search(self, word):
        raise NotImplementedError

    def starts_with(self, prefix):
        raise NotImplementedError

    def count_prefix(self, prefix):
        raise NotImplementedError

    def words_with_prefix(self, prefix):
        raise NotImplementedError


class DictTrie:
    """The same idea with no node class: self.root is a dict of dicts, one
    level per character, and the key '$' (value True) marks the end of a
    word. After insert('ab'): root == {'a': {'b': {'$': True}}}.
    insert(word) -> None; search(word) -> bool; starts_with(prefix) -> bool
    (True if some inserted word starts with prefix). Words are lowercase."""

    def __init__(self):
        raise NotImplementedError

    def insert(self, word):
        raise NotImplementedError

    def search(self, word):
        raise NotImplementedError

    def starts_with(self, prefix):
        raise NotImplementedError


class VersionedStore:
    """A key-value store that remembers every version.
    - set(key, value, timestamp) -> None; timestamps for one key arrive
      strictly increasing
    - get(key, timestamp) -> the value set for key at the latest timestamp
      <= timestamp, or '' if there is none
    O(log n) per get: keep, per key, a list of timestamps and a list of
    values, and bisect."""

    def __init__(self):
        raise NotImplementedError

    def set(self, key, value, timestamp):
        raise NotImplementedError

    def get(self, key, timestamp):
        raise NotImplementedError


class RunningMedian:
    """The median of a growing stream, from two heaps: a max-heap of the lower
    half (store negated values) and a min-heap of the upper half.
    - add(x) -> None in O(log n)
    - median() in O(1): the middle value for an odd count, the mean of the two
      middle values (a float) for an even count, exactly like
      statistics.median; on an empty stream it raises ValueError."""

    def __init__(self):
        raise NotImplementedError

    def add(self, x):
        raise NotImplementedError

    def median(self):
        raise NotImplementedError


class TreeCodec:
    """Turn a binary tree of TreeNode into a string and back.
    - serialize(root) -> str
    - deserialize(data) -> root (None for an empty tree)
    deserialize(serialize(t)) must rebuild the same shape and values for any
    tree, including negative values and missing children. Any format works;
    preorder with a marker for missing children is the classic one."""

    def serialize(self, root):
        raise NotImplementedError

    def deserialize(self, data):
        raise NotImplementedError


# ---------------------------------------------------------------- tests (don't edit)

def _replay(cls, ops, args):
    """Run a call sequence: ops[0]/args[0] construct, the rest are method calls."""
    obj = cls(*args[0])
    return [None] + [getattr(obj, op)(*a) for op, a in zip(ops[1:], args[1:])]


def _raises(exc, fn):
    try:
        fn()
    except exc:
        return True
    return False


class _ModelLRU:
    """Slow but obviously correct: (key, value) pairs, oldest first."""

    def __init__(self, capacity):
        self.capacity, self.items = capacity, []

    def get(self, key):
        for i, (k, v) in enumerate(self.items):
            if k == key:
                self.items.append(self.items.pop(i))
                return v
        return -1

    def put(self, key, value):
        self.items = [kv for kv in self.items if kv[0] != key] + [(key, value)]
        if len(self.items) > self.capacity:
            self.items.pop(0)


def _check_lru(cls):
    ops = ['LRU', 'put', 'put', 'get', 'put', 'get', 'put', 'get', 'get', 'get']
    args = [[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
    assert _replay(cls, ops, args) == [None, None, None, 1, None, -1, None, -1, 3, 4], \
        "a get() hit must make the key the most recent"
    c = cls(2)
    c.put('a', 1)
    c.put('b', 2)
    c.put('a', 10)
    c.put('c', 3)
    assert c.get('b') == -1 and c.get('a') == 10 and len(c) == 2, "updating a key must refresh it"
    rng = random.Random(16)
    for capacity in (1, 2, 5):
        real, model = cls(capacity), _ModelLRU(capacity)
        for _ in range(2000):
            key = rng.randrange(8)
            if rng.random() < 0.5:
                assert real.get(key) == model.get(key), f"get({key}) with capacity {capacity}"
            else:
                value = rng.randrange(100)
                real.put(key, value)
                model.put(key, value)
            assert len(real) == len(model.items)


def _tree_shape(node):
    return None if node is None else (node.val, _tree_shape(node.left), _tree_shape(node.right))


def _random_tree(rng, n):
    if n == 0:
        return None
    left = rng.randint(0, n - 1)
    return TreeNode(rng.randint(-1000, 1000), _random_tree(rng, left), _random_tree(rng, n - 1 - left))


def test_min_stack():
    ops = ['MinStack', 'push', 'push', 'push', 'get_min', 'pop', 'top', 'get_min', '__len__']
    args = [[], [-2], [0], [-3], [], [], [], [], []]
    assert _replay(MinStack, ops, args) == [None, None, None, None, -3, -3, 0, -2, 2]
    s = MinStack()
    assert len(s) == 0 and _raises(IndexError, s.pop) and _raises(IndexError, s.get_min)
    rng = random.Random(16)
    model = []
    for _ in range(3000):
        if model and rng.random() < 0.4:
            assert s.pop() == model.pop()
        else:
            x = rng.randint(-50, 50)
            s.push(x)
            model.append(x)
        if model:
            assert s.top() == model[-1] and s.get_min() == min(model), "the min must survive pops"
        assert len(s) == len(model)


def test_two_stack_queue():
    ops = ['TwoStackQueue', 'push', 'push', 'peek', 'pop', 'empty', 'pop', 'empty']
    args = [[], [1], [2], [], [], [], [], []]
    assert _replay(TwoStackQueue, ops, args) == [None, None, None, 1, 1, False, 2, True]
    q = TwoStackQueue()
    assert _raises(IndexError, q.pop) and _raises(IndexError, q.peek) and len(q) == 0
    rng = random.Random(16)
    model = deque()
    for _ in range(3000):
        if model and rng.random() < 0.45:
            assert q.pop() == model.popleft(), "the front of the queue is the oldest item"
        else:
            x = rng.randint(0, 999)
            q.push(x)
            model.append(x)
        assert len(q) == len(model) and q.empty() == (not model)
        if model:
            assert q.peek() == model[0]


def test_lru_cache():
    _check_lru(LRUCache)


def test_linked_lru_cache():
    _check_lru(LinkedLRUCache)
    c = LinkedLRUCache(3)
    c.put(1, 1)
    assert not any(isinstance(v, OrderedDict) for v in vars(c).values()), \
        "build this one from a plain dict and your own linked nodes"


def test_random_pick_set():
    s = RandomPickSet()
    assert s.insert(1) is True and s.insert(1) is False and s.insert(2) is True
    assert s.remove(3) is False and s.remove(1) is True and s.remove(1) is False
    assert len(s) == 1 and 2 in s and 1 not in s and s.get_random() == 2
    rng = random.Random(16)
    model = {2}
    for _ in range(3000):
        x = rng.randrange(30)
        if rng.random() < 0.5:
            assert s.insert(x) == (x not in model)
            model.add(x)
        else:
            assert s.remove(x) == (x in model)
            model.discard(x)
        assert len(s) == len(model) and all((y in s) == (y in model) for y in range(30)), \
            "remove: move the last member into the freed slot, update its index, then pop"
        if model:
            assert s.get_random() in model, "get_random returned something that isn't a member"
    random.seed(16)
    s = RandomPickSet()
    for x in 'abcde':
        s.insert(x)
    s.remove('b')
    picks = Counter(s.get_random() for _ in range(2000))
    assert set(picks) == set('acde'), "every member should come up, and only members"
    assert min(picks.values()) > 350, "picks should be roughly uniform"


def test_trie():
    t = Trie()
    for w in ['apple', 'app', 'apt', 'bat', 'app']:
        t.insert(w)
    assert t.search('app') and t.search('apple') and not t.search('ap') and not t.search('apples')
    assert t.starts_with('ap') and t.starts_with('') and not t.starts_with('c')
    assert t.count_prefix('ap') == 3 and t.count_prefix('app') == 2 and t.count_prefix('') == 4, \
        "inserting a word twice must not count it twice"
    assert t.count_prefix('z') == 0
    assert t.words_with_prefix('ap') == ['app', 'apple', 'apt'] and t.words_with_prefix('x') == []
    assert Trie().starts_with('') is False and Trie().count_prefix('') == 0
    rng = random.Random(16)
    words = {''.join(rng.choice('abc') for _ in range(rng.randint(1, 5))) for _ in range(150)}
    big = Trie()
    for w in sorted(words):
        big.insert(w)
    for p in ['', 'a', 'ab', 'cab', 'bbb', 'q']:
        want = sorted(w for w in words if w.startswith(p))
        assert big.words_with_prefix(p) == want and big.count_prefix(p) == len(want), f"prefix {p!r}"
        assert big.starts_with(p) == bool(want)


def test_dict_trie():
    t = DictTrie()
    t.insert('ab')
    assert t.root == {'a': {'b': {'$': True}}}, "one dict level per character, '$' marks a word end"
    t.insert('a')
    t.insert('abc')
    assert t.root == {'a': {'$': True, 'b': {'$': True, 'c': {'$': True}}}}
    assert t.search('a') and t.search('ab') and t.search('abc')
    assert not t.search('abcd') and not t.search('b')
    assert t.starts_with('ab') and t.starts_with('') and not t.starts_with('b')
    assert DictTrie().starts_with('') is False and type(t.root) is dict


def test_versioned_store():
    ops = ['VersionedStore', 'set', 'get', 'get', 'set', 'get', 'get', 'get']
    args = [[], ['k', 'v1', 1], ['k', 1], ['k', 3], ['k', 'v2', 4], ['k', 4], ['k', 5], ['k', 0]]
    assert _replay(VersionedStore, ops, args) == [None, None, 'v1', 'v1', None, 'v2', 'v2', '']
    s = VersionedStore()
    assert s.get('missing', 10) == ''
    rng = random.Random(16)
    history = defaultdict(list)
    t = 0
    for _ in range(500):
        key = rng.choice('xyz')
        t += rng.randint(1, 3)
        s.set(key, f'{key}{t}', t)
        history[key].append((t, f'{key}{t}'))
    for _ in range(500):
        key, q = rng.choice('xyzw'), rng.randint(-1, t + 2)
        want = ''
        for ts, val in history[key]:
            if ts <= q:
                want = val
        assert s.get(key, q) == want, f"get({key!r}, {q})"


def test_running_median():
    m = RunningMedian()
    assert _raises(ValueError, m.median), "median() of an empty stream must raise ValueError"
    out = []
    for x in [5, 15, 1, 3]:
        m.add(x)
        out.append(m.median())
    assert out == [5, 10.0, 5, 4.0]
    rng = random.Random(16)
    m, seen = RunningMedian(), []
    for _ in range(1500):
        x = rng.randint(-100, 100)
        m.add(x)
        seen.append(x)
        assert m.median() == statistics.median(seen), f"after {len(seen)} values"


def test_tree_codec():
    codec = TreeCodec()
    t = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(-4), None))
    data = codec.serialize(t)
    assert isinstance(data, str), "serialize must return a str"
    assert _tree_shape(codec.deserialize(data)) == (1, (2, None, None), (3, (-4, None, None), None)), \
        "the round trip must rebuild the same shape: record where children are missing"
    assert codec.deserialize(codec.serialize(None)) is None
    twin = TreeNode(1, TreeNode(1))
    assert _tree_shape(codec.deserialize(codec.serialize(twin))) == (1, (1, None, None), None), \
        "left and right must survive: mark the missing children"
    chain = None
    for v in range(200):
        chain = TreeNode(v, chain, None)
    assert _tree_shape(codec.deserialize(codec.serialize(chain))) == _tree_shape(chain)
    rng = random.Random(16)
    for _ in range(100):
        tree = _random_tree(rng, rng.randint(0, 40))
        assert _tree_shape(codec.deserialize(codec.serialize(tree))) == _tree_shape(tree)
