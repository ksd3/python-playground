"""R31 - Contest I/O, deep recursion, stress testing

Judges send input on stdin and read your stdout. Read everything at once with
data = sys.stdin.buffer.read().split() and walk the tokens with an index, or
use input = sys.stdin.readline and strip the newline it keeps. Collect output
strings in a list and write them once, joined by newlines. Put the code in
main(). Recursion: the default limit is 1000 frames and raising it isn't always
enough, so know the explicit-stack rewrite. Stress testing: brute force +
random tiny inputs + compare + shrink the failing case. (PyPy runs loops much
faster than CPython but handles deep recursion worse.)

Part 1 - Predict. Each block in PREDICT is a REPL session. Replace every ???
with exactly what Python prints: expression values are echoed the way the REPL
echoes them, and a line that raises prints just the exception name (TypeError).

Part 2 - Drills. Implement every function until `python check.py 31` is green.
The deep-recursion tests run at the default recursion limit of 1000. Don't edit
the tests at the bottom; add your own test_* functions if you like.

Unlocks: stdin/stdout judges, multi-case input formats, tree and graph code on
10**5-node inputs, and finding the input that breaks a fast solution.
"""
import copy
import io
import random
import sys
import time
from collections import Counter
from itertools import accumulate

PREDICT = r"""
>>> import io
>>> f = io.StringIO('3 4\nabc\n')
>>> f.readline()
???
>>> f.readline().strip()
???
>>> f.readline()
???

>>> data = b'3\n10 -2  7\r\n'
>>> data.split()
???
>>> list(map(int, data.split()))
???

>>> int(' 42\n'), int(b'  -7 ')
???
>>> int('4 2')
???

>>> line = 'a b\n'
>>> line.split(), line.split(' ')
???

>>> out = [3, 1, 4]
>>> '\n'.join(map(str, out))
???
>>> print('\n'.join(map(str, out)))
???

>>> print(*[1, 2, 3])
???
>>> print(*[1, 2, 3], sep=',')
???

>>> print('\n'.join(f'Case #{i}: {v}' for i, v in enumerate([7, 9], 1)))
???

>>> tokens = b'2 5 6 1 9'.split()
>>> pos = 0
>>> def nxt():
...     global pos
...     pos += 1
...     return int(tokens[pos - 1])
>>> t = nxt()
>>> [nxt() + nxt() for _ in range(t)]
???

>>> import io
>>> sys.stdin = io.StringIO('5\n')
>>> int(input()) * 2
???
>>> sys.stdin = sys.__stdin__

>>> n = sys.stdout.write('ok\n')
???
>>> n
???

>>> old = sys.getrecursionlimit()
>>> sys.setrecursionlimit(1000)
>>> def depth(n):
...     return 0 if n == 0 else 1 + depth(n - 1)
>>> depth(500)
???
>>> depth(5000)
???
>>> sys.setrecursionlimit(old)

>>> old = sys.getrecursionlimit()
>>> sys.setrecursionlimit(1000)
>>> @cache
... def f(n):
...     return 0 if n == 0 else f(n - 1) + 1
>>> f(5000)
???
>>> for i in range(0, 5001, 200):
...     _ = f(i)
>>> f(5000)
???
>>> sys.setrecursionlimit(old)

>>> adj = {1: [2, 3], 2: [4], 3: [], 4: []}
>>> stack, order = [1], []
>>> while stack:
...     u = stack.pop()
...     order.append(u)
...     stack.extend(adj[u])
>>> order
???
>>> stack, order = [1], []
>>> while stack:
...     u = stack.pop()
...     order.append(u)
...     stack.extend(reversed(adj[u]))
>>> order
???

>>> import random
>>> rng = random.Random(7)
>>> first = [rng.randint(1, 9) for _ in range(5)]
>>> rng = random.Random(7)
>>> first == [rng.randint(1, 9) for _ in range(5)]
???
"""


# ---------------------------------------------------------------- drills

def read_ints(data):
    """Parse every whitespace-separated integer in `data` (bytes, as returned
    by sys.stdin.buffer.read()) and return them as a list of ints.
    read_ints(b'3\n1 2 -3\n') == [3, 1, 2, -3]"""
    raise NotImplementedError


class TokenReader:
    """Walks the whitespace-separated tokens of a bytes input with an index.
    r = TokenReader(b'2\nab 5'); r.next_int() == 2; r.next_str() == 'ab'"""

    def __init__(self, data):
        """Split `data` (bytes) into tokens once."""
        raise NotImplementedError

    def has_more(self):
        """Return True if any tokens are left, else False."""
        raise NotImplementedError

    def next_int(self):
        """Return the next token as an int; raise IndexError past the end."""
        raise NotImplementedError

    def next_str(self):
        """Return the next token as a str (not bytes); raise IndexError past the end."""
        raise NotImplementedError


def range_sum_queries(text):
    """Input: "n q", then n integers, then q lines "l r" (1-indexed, inclusive).
    Return the q range sums, one per line (a trailing newline is fine).
    range_sum_queries('3 2\n1 2 3\n1 2\n2 3\n') == '3\n5'
    Timed at n = q = 100,000."""
    raise NotImplementedError


def case_summaries(text):
    """Input: t, then t test cases, each "n" followed by n integers. Tokens may
    be split across lines in any way, so read tokens, not lines. For each case
    output "d v": d is the number of distinct values and v the most frequent
    value (the smallest one on ties). Return the lines joined by newlines.
    case_summaries('2\n3\n5 1 5\n1\n-7\n') == '2 5\n1 -7'"""
    raise NotImplementedError


def parse_grid(text):
    """Input: "R C" on the first line, then R rows of C characters ('.' or
    '#'). Lines may end in \n or \r\n, and the last may have no newline.
    Return the rows as a list of R strings with no line-ending characters.
    parse_grid('2 3\n.#.\n###\n') == ['.#.', '###']"""
    raise NotImplementedError


def run_main(main, text):
    """Run main() (which reads sys.stdin and writes sys.stdout) with `text` as
    its stdin and return everything it printed, as a str. Support programs that
    read with input(), sys.stdin.readline() or sys.stdin.buffer.read(). Always
    restore the real sys.stdin and sys.stdout, even when main raises, and let
    the exception propagate."""
    raise NotImplementedError


def subtree_sizes(parent):
    """parent[i] is the parent of node i in a rooted tree (-1 for the root,
    which isn't always node 0). Return a list where entry i is the number of
    nodes in i's subtree, i included. No recursion: it must handle a path of
    100,000 nodes. subtree_sizes([-1, 0, 0, 1, 1]) == [5, 3, 1, 1, 1]"""
    raise NotImplementedError


def dfs_preorder(adj, start):
    """adj[u] lists u's out-neighbors. Return the nodes in the order a recursive
    DFS from `start` first visits them (neighbors tried in list order, visited
    ones skipped), but use an explicit stack: it must handle a 100,000-node path.
    dfs_preorder([[1, 2], [3], [3], []], 0) == [0, 1, 3, 2]"""
    raise NotImplementedError


def flatten_deep(nested):
    """Flatten a list whose items are values or lists (nested to any depth) into
    one flat list, left to right. Only lists nest; strings and tuples are values.
    No recursion: nesting can be 100,000 levels deep.
    flatten_deep([1, [2, [3, [4]], 5], [], [[6]]]) == [1, 2, 3, 4, 5, 6]"""
    raise NotImplementedError


def climb_ways(n, steps):
    """Count the ordered ways to climb exactly n stairs when each move climbs
    one of the sizes in `steps` (distinct positive ints), modulo 10**9 + 7.
    climb_ways(4, [1, 2]) == 5. Must handle n = 100,000 at the default
    recursion limit, so fill the table bottom-up."""
    raise NotImplementedError


def find_counterexample(fast, brute, gen, trials):
    """Stress-test `fast` against the trusted `brute`. Call gen() up to `trials`
    times; each call returns a tuple of positional arguments. Give each function
    its own copy.deepcopy of the arguments (either might mutate them). Return the
    first arguments tuple, exactly as generated, where the results differ or
    `fast` raises an exception; return None if every trial agrees."""
    raise NotImplementedError


def shrink_list(xs, fails):
    """fails(xs) is True. Return a smaller failing input: keep deleting single
    elements while the result still fails, until deleting any one element would
    make it pass. Keep the remaining elements in their original order and don't
    modify xs. shrink_list([4, 9, 1], lambda l: sum(l) > 8) == [9]"""
    raise NotImplementedError


# ---------------------------------------------------------------- tests (don't edit)

def _deep(fn, *args):
    """Call fn at the default recursion limit; turn RecursionError into a clear failure."""
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(1000)
    try:
        return fn(*args)
    except RecursionError:
        raise AssertionError("RecursionError at the default limit: rewrite it with an explicit stack or a loop") from None
    finally:
        sys.setrecursionlimit(old)


def _sum_main():
    n = int(input())
    nums = list(map(int, input().split()))
    print(n, sum(nums))


def _readline_main():
    readline = sys.stdin.readline
    for _ in range(int(readline())):
        a, b = map(int, readline().split())
        print(a * b)


def _buffer_main():
    words = sys.stdin.buffer.read().split()
    sys.stdout.write(' '.join(w.decode()[::-1] for w in words) + '\n')


def _crash_main():
    input()
    raise ZeroDivisionError("boom")


def _summary(vals):
    counts = Counter(vals)
    top = max(counts.values())
    return f"{len(counts)} {min(v for v, c in counts.items() if c == top)}"


def _brute_sizes(parent):
    sizes = [0] * len(parent)
    for v in range(len(parent)):
        while v != -1:
            sizes[v] += 1
            v = parent[v]
    return sizes


def _rec_preorder(adj, start):
    seen, order = set(), []

    def go(u):
        seen.add(u)
        order.append(u)
        for v in adj[u]:
            if v not in seen:
                go(v)

    go(start)
    return order


def _brute_climb(n, steps):
    if n == 0:
        return 1
    return sum(_brute_climb(n - s, steps) for s in steps if s <= n)


def _is_subsequence(small, big):
    it = iter(big)
    return all(x in it for x in small)


def test_read_ints():
    assert read_ints(b'3\n1 2 -3\n') == [3, 1, 2, -3]
    assert read_ints(b'  7\r\n\t8   9  ') == [7, 8, 9], "split() with no argument handles \\r\\n, tabs and runs of spaces"
    assert read_ints(b'') == []
    big = b' '.join(str(i).encode() for i in range(200_000))
    start = time.perf_counter()
    got = read_ints(big)
    secs = time.perf_counter() - start
    assert got == list(range(200_000))
    assert secs < 1.0, f"{secs:.2f}s for 200,000 numbers: split once, then map int over the tokens"


def test_token_reader():
    r = TokenReader(b'2\nab 5\n-3 xyz')
    assert r.has_more() is True
    assert r.next_int() == 2
    assert r.next_str() == 'ab', "next_str should return a str: decode the bytes token"
    assert r.next_int() == 5 and r.next_int() == -3
    assert r.next_str() == 'xyz'
    assert r.has_more() is False
    try:
        r.next_int()
    except IndexError:
        pass
    else:
        raise AssertionError("reading past the end should raise IndexError")
    assert TokenReader(b'  \n').has_more() is False


def test_range_sum_queries():
    assert range_sum_queries('5 3\n1 2 3 4 5\n1 5\n2 3\n4 4\n').rstrip('\n') == '15\n5\n4'
    assert range_sum_queries('1 1\n-7\n1 1').rstrip('\n') == '-7', "the last line may have no newline"
    rng = random.Random(31)
    n = q = 100_000
    nums = rng.choices(range(-10 ** 9, 10 ** 9), k=n)
    queries = []
    for _ in range(q):
        lo = rng.randint(1, n)
        queries.append((lo, rng.randint(lo, n)))
    text = f"{n} {q}\n{' '.join(map(str, nums))}\n" + '\n'.join(f'{l} {r}' for l, r in queries) + '\n'
    start = time.perf_counter()
    out = range_sum_queries(text)
    secs = time.perf_counter() - start
    lines = out.rstrip('\n').split('\n')
    assert len(lines) == q, f"expected {q} lines, got {len(lines)}"
    for (l, r), line in list(zip(queries, lines))[:200]:
        assert int(line) == sum(nums[l - 1:r]), (l, r)
    assert secs < 2.0, f"{secs:.2f}s: read all tokens at once, use prefix sums, join the output once"


def test_case_summaries():
    assert case_summaries('2\n3\n5 1 5\n1\n-7\n').rstrip('\n') == '2 5\n1 -7'
    assert case_summaries('1\n5\n3 3 1 1 2\n').rstrip('\n') == '3 1', "on ties print the smallest value"
    assert case_summaries('2\n3 1\n2 3\n2\n4\n4').rstrip('\n') == '3 1\n1 4', \
        "tokens can be split across lines: read tokens, not lines"
    rng = random.Random(31)
    cases = [[rng.randint(-5, 5) for _ in range(rng.randint(1, 30))] for _ in range(10_000)]
    parts = [str(len(cases))]
    for vals in cases:
        parts.append(str(len(vals)))
        parts.append(' '.join(map(str, vals)))
    text = '\n'.join(parts) + '\n'
    start = time.perf_counter()
    out = case_summaries(text)
    secs = time.perf_counter() - start
    assert out.rstrip('\n').split('\n') == [_summary(v) for v in cases]
    assert secs < 2.0, f"{secs:.2f}s for 10,000 cases: read every token once and join the output once"


def test_parse_grid():
    assert parse_grid('2 3\n.#.\n###\n') == ['.#.', '###']
    assert parse_grid('2 2\r\n.#\r\n#.\r\n') == ['.#', '#.'], "strip the line endings, \\r\\n included"
    assert parse_grid('1 4\n....') == ['....'], "the last line may have no newline"
    rows = parse_grid('3 1\n#\n.\n#\n')
    assert rows == ['#', '.', '#'] and all(isinstance(row, str) for row in rows)


def test_run_main():
    real_in, real_out = sys.stdin, sys.stdout
    try:
        got = run_main(_sum_main, '3\n1 2 3\n')
        assert sys.stdin is real_in and sys.stdout is real_out, "put the real sys.stdin and sys.stdout back"
        assert got.rstrip('\n') == '3 6'
        assert run_main(_readline_main, '2\n2 3\n4 5\n').rstrip('\n') == '6\n20'
        assert run_main(_buffer_main, 'ab cd\nef\n').rstrip('\n') == 'ba dc fe', \
            "support sys.stdin.buffer: wrap the bytes in io.BytesIO inside an io.TextIOWrapper"
        try:
            run_main(_crash_main, 'x\n')
        except ZeroDivisionError:
            pass
        else:
            raise AssertionError("let exceptions from main propagate")
        restored = sys.stdin is real_in and sys.stdout is real_out
    finally:
        sys.stdin, sys.stdout = real_in, real_out
    assert restored, "restore sys.stdin and sys.stdout even when main raises (try/finally)"


def test_subtree_sizes():
    assert subtree_sizes([-1, 0, 0, 1, 1]) == [5, 3, 1, 1, 1]
    assert subtree_sizes([-1]) == [1]
    assert subtree_sizes([2, 2, -1]) == [1, 1, 3], "the root isn't always node 0"
    rng = random.Random(31)
    for _ in range(100):
        n = rng.randint(1, 25)
        order = list(range(n))
        rng.shuffle(order)                     # order[0] is the root; later nodes hang off earlier ones
        parent = [0] * n
        parent[order[0]] = -1
        for i in range(1, n):
            parent[order[i]] = order[rng.randrange(i)]
        assert subtree_sizes(parent) == _brute_sizes(parent), parent
    n = 100_000
    sizes = _deep(subtree_sizes, [-1] + list(range(n - 1)))    # 0 <- 1 <- 2 <- ... one long path
    assert sizes[0] == n and sizes[-1] == 1 and sizes[n // 2] == n - n // 2
    sizes = _deep(subtree_sizes, list(range(1, n)) + [-1])     # the same path rooted at the last node
    assert sizes[-1] == n and sizes[0] == 1, "children can have smaller numbers than their parents"


def test_dfs_preorder():
    assert dfs_preorder([[1, 2], [3], [3], []], 0) == [0, 1, 3, 2]
    assert dfs_preorder([[1], [0]], 1) == [1, 0]
    assert dfs_preorder([[1, 2], [2, 3], [], []], 0) == [0, 1, 2, 3], \
        "mark a node visited when you pop it, not when you push it"
    rng = random.Random(31)
    for _ in range(200):
        n = rng.randint(1, 9)
        adj = [rng.sample(range(n), rng.randint(0, min(3, n))) for _ in range(n)]
        s = rng.randrange(n)
        assert dfs_preorder(adj, s) == _rec_preorder(adj, s), (adj, s)
    n = 100_000
    line = [[i + 1] for i in range(n - 1)] + [[]]
    assert _deep(dfs_preorder, line, 0) == list(range(n))


def test_flatten_deep():
    assert flatten_deep([1, [2, [3, [4]], 5], [], [[6]]]) == [1, 2, 3, 4, 5, 6]
    assert flatten_deep([]) == []
    assert flatten_deep([[[]]]) == []
    assert flatten_deep(['ab', ('c', 'd')]) == ['ab', ('c', 'd')], "only lists nest; strings and tuples are values"
    nested = cur = []
    for i in range(100_000):
        nxt = [i]
        cur.append(nxt)
        cur = nxt
    assert _deep(flatten_deep, nested) == list(range(100_000))


def test_climb_ways():
    assert climb_ways(4, [1, 2]) == 5
    assert climb_ways(0, [1, 2]) == 1, "there's exactly one way to climb 0 stairs: do nothing"
    assert climb_ways(3, [2]) == 0
    rng = random.Random(31)
    for _ in range(60):
        n = rng.randint(0, 14)
        steps = rng.sample(range(1, 6), rng.randint(1, 3))
        assert climb_ways(n, steps) == _brute_climb(n, steps), (n, steps)
    assert _deep(climb_ways, 100_000, [1, 2, 3]) == 111787461


def test_find_counterexample():
    rng = random.Random(31)

    def gen():
        return ([rng.randint(0, 9) for _ in range(rng.randint(1, 5))],)

    def buggy_max(xs):                      # ignores the last element
        return max(xs[:-1]) if len(xs) > 1 else xs[0]

    found = find_counterexample(buggy_max, max, gen, 500)
    assert found is not None, "this bug shows up often; 500 trials should find it"
    assert isinstance(found, tuple) and buggy_max(*found) != max(*found)
    assert find_counterexample(max, max, gen, 200) is None, "return None when every trial agrees"

    def sorts_first(xs):                    # mutates its input
        xs.sort()
        return xs[0]

    def first(xs):
        return xs[0]

    found = find_counterexample(sorts_first, first, gen, 500)
    assert found is not None, "give each function its own copy.deepcopy: one of them mutates its input"
    (xs,) = found
    assert xs[0] != min(xs), "return the arguments as generated, before any function mutated them"

    def pop_last(xs):                       # mutates its input
        return xs.pop()

    assert find_counterexample(pop_last, pop_last, gen, 200) is None, \
        "a function compared with itself must always agree: each call needs its own copy of the arguments"

    def gen_maybe_empty():
        return ([rng.randint(0, 9) for _ in range(rng.randint(0, 3))],)

    def fragile(xs):
        return xs[0]

    def safe(xs):
        return xs[0] if xs else None

    assert find_counterexample(fragile, safe, gen_maybe_empty, 500) == ([],), "an exception in fast counts as a failure"


def test_shrink_list():
    assert shrink_list([4, 9, 1], lambda l: sum(l) > 8) == [9]
    data = [1, 7, 2, 3, 7, 5]
    small = shrink_list(data, lambda l: 7 in l and 3 in l)
    assert data == [1, 7, 2, 3, 7, 5], "don't modify the input"
    assert sorted(small) == [3, 7]
    assert shrink_list([1, 2, 3], lambda l: l in ([1, 2, 3], [1, 3], [3])) == [3], \
        "after a deletion, earlier positions may become deletable: repeat until a full pass deletes nothing"
    rng = random.Random(31)
    for _ in range(100):
        xs = [rng.randint(0, 9) for _ in range(rng.randint(1, 12))]
        limit = rng.randint(0, 20)
        fails = lambda l, limit=limit: sum(l) > limit
        if not fails(xs):
            continue
        small = shrink_list(xs, fails)
        assert fails(small), "the shrunk input must still fail"
        assert all(not fails(small[:i] + small[i + 1:]) for i in range(len(small))), \
            "keep shrinking until deleting any single element makes it pass"
        assert _is_subsequence(small, xs), "keep the remaining elements in their original order"

