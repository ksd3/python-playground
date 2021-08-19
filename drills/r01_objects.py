"""R01 - Names, objects, mutability, identity

A variable is a name bound to an object. Assignment never copies anything.
Mutating an object is visible through every name bound to it.

Part 1 - Predict. Each block in PREDICT is a REPL session. Replace every ???
with exactly what Python prints: expression values are echoed the way the REPL
echoes them, and a line that raises prints just the exception name (TypeError).

Part 2 - Drills. Implement every function until `python check.py 1` is green.
Don't edit the tests at the bottom; add your own test_* functions if you like.

Unlocks: collecting results in backtracking, in-place array problems, DP table
setup, and every "why did my whole grid change" bug.
"""

PREDICT = r"""
>>> grid = [[0] * 3] * 3
>>> grid[0][0] = 1
>>> grid
???

>>> grid = [[0] * 3 for _ in range(3)]
>>> grid[0][0] = 1
>>> grid
???

>>> def f(x, acc=[]):
...     acc.append(x)
...     return acc
>>> f(1)
???
>>> f(2)
???

>>> a = [1, 2]
>>> b = a
>>> a += [3]
>>> b
???
>>> a = a + [4]
>>> b, a
???

>>> t = ([1],)
>>> t[0] += [2]
???
>>> t
???

>>> res, path = [], [1]
>>> res.append(path)
>>> path.pop()
???
>>> res
???

>>> def bad(nums):
...     nums = sorted(nums)
>>> def good(nums):
...     nums[:] = sorted(nums)
>>> xs = [3, 1, 2]
>>> bad(xs); xs
???
>>> good(xs); xs
???

>>> x = [3, 1, 2].sort()
>>> print(x)
???

>>> a = [1, 2]
>>> b = [1, 2]
>>> a == b, a is b
???
>>> c = a
>>> c is a
???

>>> {1: 'a', True: 'b', 1.0: 'c'}
???

>>> all([]), any([])
???

>>> g = [[1, 2], [3, 4]]
>>> h = g[:]
>>> h[0].append(9)
>>> h.append([5])
>>> g
???

>>> g = [[1, 2], [3, 4]]
>>> d = copy.deepcopy(g)
>>> d[0].append(9)
>>> g, d[0] is g[0]
???

>>> hash((1, 2)) == hash((1, 2))
???
>>> hash((1, [2]))
???

>>> [bool(v) for v in (0, 0.0, '', [], {}, set(), (), None, '0', [0], ' ')]
???

>>> None == False, 0 == False, '' == False
???

>>> a = b = []
>>> a.append(1)
>>> b
???
"""


# ---------------------------------------------------------------- drills

def make_grid(rows, cols, fill=0):
    """Return a rows x cols grid (a list of lists) filled with `fill`, where
    every row is its own list. make_grid(2, 3) == [[0, 0, 0], [0, 0, 0]]."""
    raise NotImplementedError


def copy_grid(grid):
    """Return a copy of a 2D grid whose rows can be changed (cells reassigned,
    rows appended to) without touching the original."""
    raise NotImplementedError


def append_to(x, acc=None):
    """Append x to acc and return acc. When acc isn't given, start a NEW list
    on every call: append_to(1) == [1], then append_to(2) == [2]."""
    raise NotImplementedError


def sort_in_place(nums):
    """Sort the caller's list in place and return None. The caller must see
    the change, and it must still be the same list object."""
    raise NotImplementedError


def replace_contents(nums, new_items):
    """Make the caller's list `nums` hold exactly `new_items` (same object,
    new contents) and return None."""
    raise NotImplementedError


def all_prefixes(items):
    """Return every prefix of items, shortest first, built by growing ONE
    running list: all_prefixes('ab') == [[], ['a'], ['a', 'b']]."""
    raise NotImplementedError


def first_present(values):
    """Return the first value that is not None, or None if there isn't one.
    0, '' and [] all count as present: first_present([None, 0, 5]) == 0."""
    raise NotImplementedError


def shares_rows(g1, g2):
    """Return True if some row of g1 is the very same list object as a row of
    g2 (identity, not equality), else False."""
    raise NotImplementedError


def unique_by_identity(objs):
    """Drop repeated references to the same object, keeping first-seen order.
    Equal-but-distinct objects are all kept."""
    raise NotImplementedError


def freeze(obj):
    """Make a nested structure hashable: lists and tuples become tuples, sets
    become frozensets, dicts become frozensets of (key, frozen value) pairs.
    freeze([1, [2, 3], {4}]) == (1, (2, 3), frozenset({4}))"""
    raise NotImplementedError


# ---------------------------------------------------------------- tests (don't edit)

def test_make_grid():
    g = make_grid(3, 2)
    assert g == [[0, 0], [0, 0], [0, 0]]
    g[0][0] = 1
    assert g == [[1, 0], [0, 0], [0, 0]], "rows must be independent lists"
    assert make_grid(2, 2, '.') == [['.', '.'], ['.', '.']]
    assert make_grid(0, 5) == []


def test_copy_grid():
    g = [[1, 2], [3, 4]]
    c = copy_grid(g)
    assert c == g and c is not g
    c[0][0] = 99
    c[1].append(5)
    assert g == [[1, 2], [3, 4]], "changing the copy changed the original"


def test_append_to():
    assert append_to(1) == [1]
    assert append_to(2) == [2], "the default list is shared between calls"
    mine = [0]
    assert append_to(1, mine) is mine and mine == [0, 1]


def test_sort_in_place():
    nums = [3, 1, 2]
    alias = nums
    assert sort_in_place(nums) is None
    assert alias == [1, 2, 3] and alias is nums


def test_replace_contents():
    nums = [1, 2, 3]
    alias = nums
    assert replace_contents(nums, [9, 8]) is None
    assert alias == [9, 8] and alias is nums, "rebinding the parameter doesn't reach the caller"


def test_all_prefixes():
    assert all_prefixes('ab') == [[], ['a'], ['a', 'b']]
    assert all_prefixes([]) == [[]]
    out = all_prefixes([1, 2, 3])
    assert out == [[], [1], [1, 2], [1, 2, 3]], "did you store the running list instead of copies?"
    assert len({id(p) for p in out}) == 4, "every prefix must be its own list"


def test_first_present():
    assert first_present([None, 0, 5]) == 0
    assert first_present([None, '', 'x']) == ''
    assert first_present([None, None]) is None
    assert first_present([]) is None
    assert first_present([[], 1]) == []


def test_shares_rows():
    a, b = [1], [2]
    assert shares_rows([a, b], [[1], b]) is True
    assert shares_rows([a], [[1]]) is False, "equal rows aren't the same row"
    g = [[0] * 2] * 2
    assert shares_rows(g, [g[1]]) is True


def test_unique_by_identity():
    x, y = [1], [1]
    out = unique_by_identity([x, x, y, x])
    assert len(out) == 2 and out[0] is x and out[1] is y
    assert unique_by_identity([]) == []


def test_freeze():
    assert freeze([1, [2, 3], {4}]) == (1, (2, 3), frozenset({4}))
    f = freeze({'a': [1, 2], 'b': {'c': [3]}})
    assert f == frozenset({('a', (1, 2)), ('b', frozenset({('c', (3,))}))})
    hash(f)
    seen = {freeze([[1], [2]]): 'ok'}
    assert seen[freeze([[1], [2]])] == 'ok'
