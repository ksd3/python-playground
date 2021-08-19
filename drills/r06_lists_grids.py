"""R06 - Lists, tuples, 2D grids

Slices never raise ([1, 2, 3][5:] == []) and always make a copy; assigning to a
slice can change the length (a[1:3] = [9]). a[::-1] copies, a.reverse() works in
place and returns None, reversed(a) is a one-shot iterator. (1) is an int and
(1,) a tuple; tuples and lists compare element by element, which is what
multi-key sorting and heap entries rely on. Build grids with
[[0] * C for _ in range(R)]; zip(*g) transposes, [list(r) for r in zip(*g[::-1])]
rotates clockwise; r - c is constant along a down-right diagonal and r + c along
a down-left one; cell (r, c) is index r * C + c, and divmod(i, C) maps back.

Part 1 - Predict. Each block in PREDICT is a REPL session. Replace every ???
with exactly what Python prints: expression values are echoed the way the REPL
echoes them, and a line that raises prints just the exception name (TypeError).

Part 2 - Drills. Implement every function until `python check.py 6` is green.
Don't edit the tests at the bottom; add your own test_* functions if you like.

Unlocks: matrix problems (rotate, spiral, set-zeroes, search), grid traversal,
in-place array problems, and partitioning.
"""

PREDICT = r"""
>>> l = [[]] * 3
>>> l[0].append(1)
>>> l
???

>>> lst = [1, 2, 2, 3]
>>> for x in lst:
...     if x == 2:
...         lst.remove(x)
>>> lst
???

>>> a = [1, 2, 3]
>>> a[5:], a[-10:2], a[::-1], a[::2]
???
>>> a[5]
???

>>> a = [1, 2, 3, 4, 5]
>>> a[1:3] = [9]
>>> a
???
>>> del a[::2]
>>> a
???

>>> a = [3, 1, 2]
>>> print(a.reverse())
???
>>> a
???

>>> r = reversed([1, 2, 3])
>>> list(r), list(r)
???

>>> a = [1, 2, 3]
>>> a[::-1] is a, a[:] == a, a[:] is a
???

>>> type((1)), type((1,)), (1, 2) + (3,)
???

>>> (1, 2) < (1, 3), (1, 2) < (1, 2, 0), [2] > [1, 9, 9]
???

>>> t = (1, [2])
>>> t[1].append(3)
>>> t
???
>>> t[0] = 5
???

>>> list(range(5, 0, -2)), list(range(0)), len(range(3, 10, 3))
???

>>> g = [[1, 2, 3], [4, 5, 6]]
>>> list(zip(*g))
???
>>> [list(r) for r in zip(*g[::-1])]
???

>>> C = 3
>>> divmod(7, C), 2 * C + 1
???

>>> [x for row in [[1, 2], [3]] for x in row]
???

>>> a = [1, 2, 3]
>>> b = a * 2
>>> a.append(4)
>>> b
???

>>> a = [1, 2]
>>> a.append([3, 4])
>>> a.extend([5, 6])
>>> a.extend('ab')
>>> a
???

>>> a = [1, 2, 3]
>>> a.insert(100, 9)
>>> a.insert(-100, 0)
>>> a
???

>>> [1, 2, 2].index(2)
???
>>> [1, 2].remove(3)
???

>>> max([], default=0), min([[1, 2], [1]]), max([(1, 'b'), (1, 'a')])
???

>>> sorted((3, 1, 2)), sorted('cab'), sorted({'b': 1, 'a': 2})
???
"""


# ---------------------------------------------------------------- drills

def reverse_range(a, i, j):
    """Reverse a[i..j] (both ends included) in place with two pointers and
    return None. a = [1, 2, 3, 4, 5]; reverse_range(a, 1, 3) -> [1, 4, 3, 2, 5]"""
    raise NotImplementedError


def rotate_right(a, k):
    """Rotate a to the right by k steps in place (k may exceed len(a)) and
    return None, using three reversals and O(1) extra space.
    a = [1, 2, 3, 4, 5]; rotate_right(a, 2) -> [4, 5, 1, 2, 3]"""
    raise NotImplementedError


def remove_value(a, val):
    """Remove every val from a in place, keeping the order of the rest, and
    return the new length: move kept values down with a write pointer, then
    trim the tail. a = [3, 2, 2, 3]; remove_value(a, 3) == 2 and a == [2, 2]"""
    raise NotImplementedError


def three_way_partition(a, pivot):
    """Rearrange a in place, in one pass, into values < pivot, then == pivot,
    then > pivot, and return (i, j) where a[:i] < pivot, a[i:j] == pivot and
    a[j:] > pivot. Order inside each group doesn't matter."""
    raise NotImplementedError


def neighbors(R, C, r, c, eight=False):
    """In-bounds neighbors of (r, c) in an R x C grid as (row, col) tuples.
    4-way order: up, down, left, right. eight=True: all 8 surrounding cells in
    row-major order. neighbors(2, 2, 0, 0) == [(1, 0), (0, 1)]"""
    raise NotImplementedError


def transpose(grid):
    """Return the transpose as a list of lists (rows become columns).
    transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]"""
    raise NotImplementedError


def rotate_cw(grid):
    """Return a new grid rotated 90 degrees clockwise, as a list of lists.
    rotate_cw([[1, 2, 3], [4, 5, 6]]) == [[4, 1], [5, 2], [6, 3]]"""
    raise NotImplementedError


def rotate_ccw(grid):
    """Return a new grid rotated 90 degrees counter-clockwise, as a list of
    lists. rotate_ccw([[1, 2, 3], [4, 5, 6]]) == [[3, 6], [2, 5], [1, 4]]"""
    raise NotImplementedError


def spiral(grid):
    """Return the values in clockwise spiral order from the top-left corner.
    spiral([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [1, 2, 3, 6, 9, 8, 7, 4, 5]"""
    raise NotImplementedError


def anti_diagonals(grid):
    """Group the values by r + c, from the top-left corner to the bottom-right;
    inside a group, upper rows first.
    anti_diagonals([[1, 2, 3], [4, 5, 6]]) == [[1], [2, 4], [3, 5], [6]]"""
    raise NotImplementedError


def reshape(grid, rows, cols):
    """Lay the values of grid out row by row in a new rows x cols grid, or
    return None if the sizes don't match. Don't modify grid.
    reshape([[1, 2], [3, 4]], 1, 4) == [[1, 2, 3, 4]]"""
    raise NotImplementedError


def pad(grid, fill):
    """Return a new grid with a one-cell border of `fill`: an R x C grid becomes
    (R + 2) x (C + 2), every row its own list.
    pad([[1]], 0) == [[0, 0, 0], [0, 1, 0], [0, 0, 0]]"""
    raise NotImplementedError


def zero_rows_cols(grid):
    """In place: wherever a cell is 0, set its entire row and column to 0, and
    return None. Find every original zero before changing anything."""
    raise NotImplementedError


def latest_version(versions):
    """Return the highest version string, comparing the dot-separated parts as
    a tuple of ints (so '1.10' > '1.9' and '1.0' > '1'); on a tie, the first.
    latest_version(['1.9.9', '1.10.0', '1.2']) == '1.10.0'"""
    raise NotImplementedError


# ---------------------------------------------------------------- tests (don't edit)
import random as _random


def _rotate_cw(g):
    return [list(r) for r in zip(*g[::-1])]


def _spiral(g):
    R, C = len(g), len(g[0])
    seen, out, r, c, d = set(), [], 0, 0, 0
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for _ in range(R * C):
        out.append(g[r][c])
        seen.add((r, c))
        nr, nc = r + dirs[d][0], c + dirs[d][1]
        if not (0 <= nr < R and 0 <= nc < C) or (nr, nc) in seen:
            d = (d + 1) % 4
            nr, nc = r + dirs[d][0], c + dirs[d][1]
        r, c = nr, nc
    return out


def _grid(rng, R, C, lo=0, hi=9):
    return [[rng.randint(lo, hi) for _ in range(C)] for _ in range(R)]


def test_reverse_range():
    a = [1, 2, 3, 4, 5]
    alias = a
    assert reverse_range(a, 1, 3) is None
    assert alias == [1, 4, 3, 2, 5] and alias is a
    rng = _random.Random(6)
    for _ in range(200):
        n = rng.randint(1, 8)
        a = [rng.randint(0, 9) for _ in range(n)]
        i = rng.randrange(n)
        j = rng.randrange(i, n)
        expected = a[:i] + a[i:j + 1][::-1] + a[j + 1:]
        reverse_range(a, i, j)
        assert a == expected, (i, j)


def test_rotate_right():
    a = [1, 2, 3, 4, 5]
    alias = a
    assert rotate_right(a, 2) is None
    assert alias == [4, 5, 1, 2, 3] and alias is a
    empty = []
    rotate_right(empty, 3)
    assert empty == [], "an empty list must not crash (k % 0)"
    rng = _random.Random(6)
    for _ in range(200):
        n, k = rng.randint(1, 8), rng.randint(0, 20)
        a = list(range(n))
        expected = a[n - k % n:] + a[:n - k % n]
        rotate_right(a, k)
        assert a == expected, (n, k)


def test_remove_value():
    a = [3, 2, 2, 3]
    alias = a
    assert remove_value(a, 3) == 2
    assert alias == [2, 2] and alias is a, "trim the list in place (del a[k:])"
    rng = _random.Random(6)
    for _ in range(200):
        a = [rng.randint(0, 3) for _ in range(rng.randint(0, 10))]
        val = rng.randint(0, 3)
        expected = [x for x in a if x != val]
        assert remove_value(a, val) == len(expected)
        assert a == expected


def test_three_way_partition():
    rng = _random.Random(6)
    for _ in range(300):
        a = [rng.randint(0, 5) for _ in range(rng.randint(0, 12))]
        before, alias, pivot = sorted(a), a, rng.randint(0, 5)
        i, j = three_way_partition(a, pivot)
        assert alias is a and sorted(a) == before, "rearrange the list itself"
        assert all(x < pivot for x in a[:i]), (a, pivot, i, j)
        assert all(x == pivot for x in a[i:j]), (a, pivot, i, j)
        assert all(x > pivot for x in a[j:]), (a, pivot, i, j)


def test_neighbors():
    assert neighbors(2, 2, 0, 0) == [(1, 0), (0, 1)]
    assert neighbors(3, 3, 1, 1) == [(0, 1), (2, 1), (1, 0), (1, 2)]
    assert neighbors(1, 1, 0, 0) == []
    assert neighbors(3, 3, 1, 1, eight=True) == [
        (0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]
    assert neighbors(2, 3, 0, 2, eight=True) == [(0, 1), (1, 1), (1, 2)]


def test_transpose():
    assert transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
    assert transpose([[1], [2]]) == [[1, 2]]
    assert transpose([]) == []
    assert all(type(row) is list for row in transpose([[1, 2]])), "rows must be lists, not tuples"


def test_rotate_cw():
    g = [[1, 2, 3], [4, 5, 6]]
    assert rotate_cw(g) == [[4, 1], [5, 2], [6, 3]]
    assert g == [[1, 2, 3], [4, 5, 6]], "don't modify the input"
    assert all(type(row) is list for row in rotate_cw(g)), "rows must be lists, not tuples"
    sq = [[1, 2], [3, 4]]
    assert rotate_cw(rotate_cw(rotate_cw(rotate_cw(sq)))) == sq


def test_rotate_ccw():
    g = [[1, 2, 3], [4, 5, 6]]
    assert rotate_ccw(g) == [[3, 6], [2, 5], [1, 4]]
    assert all(type(row) is list for row in rotate_ccw(g)), "rows must be lists, not tuples"
    rng = _random.Random(6)
    for _ in range(50):
        g = _grid(rng, rng.randint(1, 4), rng.randint(1, 4))
        assert rotate_ccw(_rotate_cw(g)) == g


def test_spiral():
    assert spiral([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [1, 2, 3, 6, 9, 8, 7, 4, 5]
    assert spiral([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]) == [
        1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
    assert spiral([[1], [2], [3]]) == [1, 2, 3], "a single column must not double back"
    assert spiral([[1, 2, 3]]) == [1, 2, 3], "a single row must not double back"
    assert spiral([]) == []
    rng = _random.Random(6)
    for _ in range(100):
        R, C = rng.randint(1, 5), rng.randint(1, 5)
        g = [[r * C + c for c in range(C)] for r in range(R)]
        assert spiral(g) == _spiral(g), (R, C)


def test_anti_diagonals():
    assert anti_diagonals([[1, 2, 3], [4, 5, 6]]) == [[1], [2, 4], [3, 5], [6]]
    assert anti_diagonals([[1], [2]]) == [[1], [2]]
    assert anti_diagonals([]) == []
    rng = _random.Random(6)
    for _ in range(50):
        R, C = rng.randint(1, 5), rng.randint(1, 5)
        g = _grid(rng, R, C)
        expected = [[g[r][s - r] for r in range(R) if 0 <= s - r < C] for s in range(R + C - 1)]
        assert anti_diagonals(g) == expected


def test_reshape():
    g = [[1, 2], [3, 4]]
    assert reshape(g, 1, 4) == [[1, 2, 3, 4]]
    assert reshape(g, 4, 1) == [[1], [2], [3], [4]]
    assert reshape(g, 3, 2) is None
    assert g == [[1, 2], [3, 4]], "don't modify the input"
    assert reshape([[1, 2, 3], [4, 5, 6]], 3, 2) == [[1, 2], [3, 4], [5, 6]]


def test_pad():
    assert pad([[1]], 0) == [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    p = pad([[1, 2]], '.')
    assert p == [['.'] * 4, ['.', 1, 2, '.'], ['.'] * 4]
    p[0][0] = 'x'
    assert p[2][0] == '.', "the top and bottom border rows must be separate lists"
    assert pad([], 0) == [[0, 0], [0, 0]]


def test_zero_rows_cols():
    g = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    alias = g
    assert zero_rows_cols(g) is None
    assert alias == [[1, 0, 1], [0, 0, 0], [1, 0, 1]] and alias is g
    g = [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]
    zero_rows_cols(g)
    assert g == [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]], "zeros you write must not spread further"
    rng = _random.Random(6)
    for _ in range(100):
        R, C = rng.randint(1, 4), rng.randint(1, 4)
        g = _grid(rng, R, C, 0, 3)
        rows = {r for r in range(R) if 0 in g[r]}
        cols = {c for c in range(C) if any(g[r][c] == 0 for r in range(R))}
        expected = [[0 if r in rows or c in cols else g[r][c] for c in range(C)] for r in range(R)]
        zero_rows_cols(g)
        assert g == expected


def test_latest_version():
    assert latest_version(['1.9.9', '1.10.0', '1.2']) == '1.10.0', "compare numbers, not strings"
    assert latest_version(['2', '1.99']) == '2'
    assert latest_version(['1', '1.0']) == '1.0'
    assert latest_version(['3.1', '3.01']) == '3.1', "on a tie, the first one wins"
