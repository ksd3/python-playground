"""R01 - Names, objects, mutability, identity (reference solutions)

Compare after you've made your own attempt. Run: python check.py 1 -s
"""

PREDICT = r"""
>>> grid = [[0] * 3] * 3
>>> grid[0][0] = 1
>>> grid
[[1, 0, 0], [1, 0, 0], [1, 0, 0]]

>>> grid = [[0] * 3 for _ in range(3)]
>>> grid[0][0] = 1
>>> grid
[[1, 0, 0], [0, 0, 0], [0, 0, 0]]

>>> def f(x, acc=[]):
...     acc.append(x)
...     return acc
>>> f(1)
[1]
>>> f(2)
[1, 2]

>>> a = [1, 2]
>>> b = a
>>> a += [3]
>>> b
[1, 2, 3]
>>> a = a + [4]
>>> b, a
([1, 2, 3], [1, 2, 3, 4])

>>> t = ([1],)
>>> t[0] += [2]
TypeError
>>> t
([1, 2],)

>>> res, path = [], [1]
>>> res.append(path)
>>> path.pop()
1
>>> res
[[]]

>>> def bad(nums):
...     nums = sorted(nums)
>>> def good(nums):
...     nums[:] = sorted(nums)
>>> xs = [3, 1, 2]
>>> bad(xs); xs
[3, 1, 2]
>>> good(xs); xs
[1, 2, 3]

>>> x = [3, 1, 2].sort()
>>> print(x)
None

>>> a = [1, 2]
>>> b = [1, 2]
>>> a == b, a is b
(True, False)
>>> c = a
>>> c is a
True

>>> {1: 'a', True: 'b', 1.0: 'c'}
{1: 'c'}

>>> all([]), any([])
(True, False)

>>> g = [[1, 2], [3, 4]]
>>> h = g[:]
>>> h[0].append(9)
>>> h.append([5])
>>> g
[[1, 2, 9], [3, 4]]

>>> g = [[1, 2], [3, 4]]
>>> d = copy.deepcopy(g)
>>> d[0].append(9)
>>> g, d[0] is g[0]
([[1, 2], [3, 4]], False)

>>> hash((1, 2)) == hash((1, 2))
True
>>> hash((1, [2]))
TypeError

>>> [bool(v) for v in (0, 0.0, '', [], {}, set(), (), None, '0', [0], ' ')]
[False, False, False, False, False, False, False, False, True, True, True]

>>> None == False, 0 == False, '' == False
(False, True, False)

>>> a = b = []
>>> a.append(1)
>>> b
[1]
"""


def make_grid(rows, cols, fill=0):
    return [[fill] * cols for _ in range(rows)]


def copy_grid(grid):
    return [row[:] for row in grid]


def append_to(x, acc=None):
    if acc is None:
        acc = []
    acc.append(x)
    return acc


def sort_in_place(nums):
    nums.sort()


def replace_contents(nums, new_items):
    nums[:] = new_items


def all_prefixes(items):
    res, path = [[]], []
    for x in items:
        path.append(x)
        res.append(path[:])
    return res


def first_present(values):
    return next((v for v in values if v is not None), None)


def shares_rows(g1, g2):
    ids = {id(row) for row in g2}
    return any(id(row) in ids for row in g1)


def unique_by_identity(objs):
    seen, out = set(), []
    for obj in objs:
        if id(obj) not in seen:
            seen.add(id(obj))
            out.append(obj)
    return out


def freeze(obj):
    if isinstance(obj, (list, tuple)):
        return tuple(freeze(x) for x in obj)
    if isinstance(obj, (set, frozenset)):
        return frozenset(freeze(x) for x in obj)
    if isinstance(obj, dict):
        return frozenset((k, freeze(v)) for k, v in obj.items())
    return obj
