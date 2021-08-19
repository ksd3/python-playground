"""R06 - Lists, tuples, 2D grids (reference solutions)

Compare after you've made your own attempt. Run: python check.py 6 -s
"""

PREDICT = r"""
>>> l = [[]] * 3
>>> l[0].append(1)
>>> l
[[1], [1], [1]]

>>> lst = [1, 2, 2, 3]
>>> for x in lst:
...     if x == 2:
...         lst.remove(x)
>>> lst
[1, 2, 3]

>>> a = [1, 2, 3]
>>> a[5:], a[-10:2], a[::-1], a[::2]
([], [1, 2], [3, 2, 1], [1, 3])
>>> a[5]
IndexError

>>> a = [1, 2, 3, 4, 5]
>>> a[1:3] = [9]
>>> a
[1, 9, 4, 5]
>>> del a[::2]
>>> a
[9, 5]

>>> a = [3, 1, 2]
>>> print(a.reverse())
None
>>> a
[2, 1, 3]

>>> r = reversed([1, 2, 3])
>>> list(r), list(r)
([3, 2, 1], [])

>>> a = [1, 2, 3]
>>> a[::-1] is a, a[:] == a, a[:] is a
(False, True, False)

>>> type((1)), type((1,)), (1, 2) + (3,)
(<class 'int'>, <class 'tuple'>, (1, 2, 3))

>>> (1, 2) < (1, 3), (1, 2) < (1, 2, 0), [2] > [1, 9, 9]
(True, True, True)

>>> t = (1, [2])
>>> t[1].append(3)
>>> t
(1, [2, 3])
>>> t[0] = 5
TypeError

>>> list(range(5, 0, -2)), list(range(0)), len(range(3, 10, 3))
([5, 3, 1], [], 3)

>>> g = [[1, 2, 3], [4, 5, 6]]
>>> list(zip(*g))
[(1, 4), (2, 5), (3, 6)]
>>> [list(r) for r in zip(*g[::-1])]
[[4, 1], [5, 2], [6, 3]]

>>> C = 3
>>> divmod(7, C), 2 * C + 1
((2, 1), 7)

>>> [x for row in [[1, 2], [3]] for x in row]
[1, 2, 3]

>>> a = [1, 2, 3]
>>> b = a * 2
>>> a.append(4)
>>> b
[1, 2, 3, 1, 2, 3]

>>> a = [1, 2]
>>> a.append([3, 4])
>>> a.extend([5, 6])
>>> a.extend('ab')
>>> a
[1, 2, [3, 4], 5, 6, 'a', 'b']

>>> a = [1, 2, 3]
>>> a.insert(100, 9)
>>> a.insert(-100, 0)
>>> a
[0, 1, 2, 3, 9]

>>> [1, 2, 2].index(2)
1
>>> [1, 2].remove(3)
ValueError

>>> max([], default=0), min([[1, 2], [1]]), max([(1, 'b'), (1, 'a')])
(0, [1], (1, 'b'))

>>> sorted((3, 1, 2)), sorted('cab'), sorted({'b': 1, 'a': 2})
([1, 2, 3], ['a', 'b', 'c'], ['a', 'b'])
"""


def reverse_range(a, i, j):
    while i < j:
        a[i], a[j] = a[j], a[i]
        i, j = i + 1, j - 1


def rotate_right(a, k):
    n = len(a)
    if n == 0:
        return
    k %= n
    reverse_range(a, 0, n - 1)
    reverse_range(a, 0, k - 1)
    reverse_range(a, k, n - 1)


def remove_value(a, val):
    w = 0
    for x in a:
        if x != val:
            a[w] = x  # w never passes the read position, so nothing unread is overwritten
            w += 1
    del a[w:]
    return w


def three_way_partition(a, pivot):
    lt, i, gt = 0, 0, len(a)
    while i < gt:
        if a[i] < pivot:
            a[lt], a[i] = a[i], a[lt]
            lt += 1
            i += 1
        elif a[i] > pivot:
            gt -= 1
            a[gt], a[i] = a[i], a[gt]  # don't advance i: the swapped-in value is unread
        else:
            i += 1
    return lt, gt


def neighbors(R, C, r, c, eight=False):
    if eight:
        steps = [(dr, dc) for dr in (-1, 0, 1) for dc in (-1, 0, 1) if dr or dc]
    else:
        steps = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    return [(r + dr, c + dc) for dr, dc in steps if 0 <= r + dr < R and 0 <= c + dc < C]


def transpose(grid):
    return [list(col) for col in zip(*grid)]


def rotate_cw(grid):
    return [list(row) for row in zip(*grid[::-1])]


def rotate_ccw(grid):
    return [list(row) for row in zip(*grid)][::-1]


def spiral(grid):
    out = []
    if not grid:
        return out
    top, bottom, left, right = 0, len(grid) - 1, 0, len(grid[0]) - 1
    while top <= bottom and left <= right:
        out.extend(grid[top][c] for c in range(left, right + 1))
        out.extend(grid[r][right] for r in range(top + 1, bottom + 1))
        if top < bottom and left < right:  # a lone row or column has no way back
            out.extend(grid[bottom][c] for c in range(right - 1, left - 1, -1))
            out.extend(grid[r][left] for r in range(bottom - 1, top, -1))
        top, bottom, left, right = top + 1, bottom - 1, left + 1, right - 1
    return out


def anti_diagonals(grid):
    if not grid:
        return []
    R, C = len(grid), len(grid[0])
    groups = [[] for _ in range(R + C - 1)]
    for r in range(R):
        for c in range(C):
            groups[r + c].append(grid[r][c])
    return groups


def reshape(grid, rows, cols):
    flat = [x for row in grid for x in row]
    if rows * cols != len(flat):
        return None
    return [flat[r * cols:(r + 1) * cols] for r in range(rows)]


def pad(grid, fill):
    C = len(grid[0]) if grid else 0
    border = [fill] * (C + 2)
    return [border[:]] + [[fill, *row, fill] for row in grid] + [border[:]]


def zero_rows_cols(grid):
    rows = {r for r, row in enumerate(grid) if 0 in row}
    cols = {c for row in grid for c, v in enumerate(row) if v == 0}
    for r, row in enumerate(grid):
        for c in range(len(row)):
            if r in rows or c in cols:
                row[c] = 0


def latest_version(versions):
    return max(versions, key=lambda v: tuple(map(int, v.split('.'))))
