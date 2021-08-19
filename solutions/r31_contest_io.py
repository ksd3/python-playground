"""R31 - Contest I/O, deep recursion, stress testing (reference solutions)

Compare after you've made your own attempt. Run: python check.py 31 -s
"""
import copy
import io
import sys
from collections import Counter
from itertools import accumulate

PREDICT = r"""
>>> import io
>>> f = io.StringIO('3 4\nabc\n')
>>> f.readline()
'3 4\n'
>>> f.readline().strip()
'abc'
>>> f.readline()
''

>>> data = b'3\n10 -2  7\r\n'
>>> data.split()
[b'3', b'10', b'-2', b'7']
>>> list(map(int, data.split()))
[3, 10, -2, 7]

>>> int(' 42\n'), int(b'  -7 ')
(42, -7)
>>> int('4 2')
ValueError

>>> line = 'a b\n'
>>> line.split(), line.split(' ')
(['a', 'b'], ['a', 'b\n'])

>>> out = [3, 1, 4]
>>> '\n'.join(map(str, out))
'3\n1\n4'
>>> print('\n'.join(map(str, out)))
3
1
4

>>> print(*[1, 2, 3])
1 2 3
>>> print(*[1, 2, 3], sep=',')
1,2,3

>>> print('\n'.join(f'Case #{i}: {v}' for i, v in enumerate([7, 9], 1)))
Case #1: 7
Case #2: 9

>>> tokens = b'2 5 6 1 9'.split()
>>> pos = 0
>>> def nxt():
...     global pos
...     pos += 1
...     return int(tokens[pos - 1])
>>> t = nxt()
>>> [nxt() + nxt() for _ in range(t)]
[11, 10]

>>> import io
>>> sys.stdin = io.StringIO('5\n')
>>> int(input()) * 2
10
>>> sys.stdin = sys.__stdin__

>>> n = sys.stdout.write('ok\n')
ok
>>> n
3

>>> old = sys.getrecursionlimit()
>>> sys.setrecursionlimit(1000)
>>> def depth(n):
...     return 0 if n == 0 else 1 + depth(n - 1)
>>> depth(500)
500
>>> depth(5000)
RecursionError
>>> sys.setrecursionlimit(old)

>>> old = sys.getrecursionlimit()
>>> sys.setrecursionlimit(1000)
>>> @cache
... def f(n):
...     return 0 if n == 0 else f(n - 1) + 1
>>> f(5000)
RecursionError
>>> for i in range(0, 5001, 200):
...     _ = f(i)
>>> f(5000)
5000
>>> sys.setrecursionlimit(old)

>>> adj = {1: [2, 3], 2: [4], 3: [], 4: []}
>>> stack, order = [1], []
>>> while stack:
...     u = stack.pop()
...     order.append(u)
...     stack.extend(adj[u])
>>> order
[1, 3, 2, 4]
>>> stack, order = [1], []
>>> while stack:
...     u = stack.pop()
...     order.append(u)
...     stack.extend(reversed(adj[u]))
>>> order
[1, 2, 4, 3]

>>> import random
>>> rng = random.Random(7)
>>> first = [rng.randint(1, 9) for _ in range(5)]
>>> rng = random.Random(7)
>>> first == [rng.randint(1, 9) for _ in range(5)]
True
"""

MOD = 10 ** 9 + 7


def read_ints(data):
    return list(map(int, data.split()))


class TokenReader:
    def __init__(self, data):
        self.tokens = data.split()
        self.pos = 0

    def has_more(self):
        return self.pos < len(self.tokens)

    def _next(self):
        token = self.tokens[self.pos]   # IndexError past the end
        self.pos += 1
        return token

    def next_int(self):
        return int(self._next())

    def next_str(self):
        return self._next().decode()


def range_sum_queries(text):
    data = text.split()
    n, q = int(data[0]), int(data[1])
    prefix = [0, *accumulate(map(int, data[2:2 + n]))]
    out, pos = [], 2 + n
    for _ in range(q):
        l, r = int(data[pos]), int(data[pos + 1])
        pos += 2
        out.append(prefix[r] - prefix[l - 1])
    return '\n'.join(map(str, out))


def case_summaries(text):
    data = text.split()
    t, pos, out = int(data[0]), 1, []
    for _ in range(t):
        n = int(data[pos])
        counts = Counter(map(int, data[pos + 1:pos + 1 + n]))
        pos += 1 + n
        top = max(counts.values())
        out.append(f"{len(counts)} {min(v for v, c in counts.items() if c == top)}")
    return '\n'.join(out)


def parse_grid(text):
    data = text.split()                 # rows contain no spaces, so tokens are rows
    return data[2:2 + int(data[0])]


def run_main(main, text):
    real_in, real_out = sys.stdin, sys.stdout
    sys.stdin = io.TextIOWrapper(io.BytesIO(text.encode()), encoding="utf-8")
    sys.stdout = out = io.StringIO()
    try:
        main()
    finally:
        sys.stdin, sys.stdout = real_in, real_out
    return out.getvalue()


def subtree_sizes(parent):
    n = len(parent)
    children = [[] for _ in range(n)]
    root = -1
    for v, p in enumerate(parent):
        if p == -1:
            root = v
        else:
            children[p].append(v)
    order = [root]
    for v in order:                     # BFS: the list grows while we walk it
        order.extend(children[v])
    sizes = [1] * n
    for v in reversed(order):           # every child comes after its parent
        if parent[v] != -1:
            sizes[parent[v]] += sizes[v]
    return sizes


def dfs_preorder(adj, start):
    seen, order, stack = set(), [], [start]
    while stack:
        u = stack.pop()
        if u in seen:
            continue
        seen.add(u)                     # mark on pop so the order matches recursion
        order.append(u)
        stack.extend(reversed(adj[u]))  # first neighbor ends up on top
    return order


def flatten_deep(nested):
    out, stack = [], [iter(nested)]
    while stack:
        for item in stack[-1]:
            if isinstance(item, list):
                stack.append(iter(item))
                break
            out.append(item)
        else:
            stack.pop()                 # this list is used up; resume its parent
    return out


def climb_ways(n, steps):
    ways = [1] + [0] * n
    for i in range(1, n + 1):
        ways[i] = sum(ways[i - s] for s in steps if s <= i) % MOD
    return ways[n]


def find_counterexample(fast, brute, gen, trials):
    for _ in range(trials):
        args = gen()
        expected = brute(*copy.deepcopy(args))
        try:
            got = fast(*copy.deepcopy(args))
        except Exception:
            return args
        if got != expected:
            return args
    return None


def shrink_list(xs, fails):
    xs = list(xs)
    shrunk = True
    while shrunk:                       # repeat until a full pass deletes nothing
        shrunk = False
        i = 0
        while i < len(xs):
            smaller = xs[:i] + xs[i + 1:]
            if fails(smaller):
                xs, shrunk = smaller, True
            else:
                i += 1
    return xs
