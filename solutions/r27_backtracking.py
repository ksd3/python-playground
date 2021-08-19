"""R27 - Recursion and backtracking (reference solutions)

Compare after you've made your own attempt. Run: python check.py 27 -s
"""

PREDICT = r"""
>>> res, path = [], []
>>> def dfs(i):
...     if i == 2:
...         res.append(path)
...         return
...     for c in 'ab':
...         path.append(c)
...         dfs(i + 1)
...         path.pop()
>>> dfs(0)
>>> res
[[], [], [], []]

>>> res, path = [], []
>>> def dfs(i):
...     if i == 2:
...         res.append(path[:])
...         return
...     for c in 'ab':
...         path.append(c)
...         dfs(i + 1)
...         path.pop()
>>> dfs(0)
>>> res
[['a', 'a'], ['a', 'b'], ['b', 'a'], ['b', 'b']]

>>> out = []
>>> def gen(s, n):
...     if len(s) == n:
...         out.append(s)
...         return
...     for c in '01':
...         gen(s + c, n)
>>> gen('', 2)
>>> out
['00', '01', '10', '11']

>>> def depth(n):
...     return 0 if n == 0 else 1 + depth(n - 1)
>>> old = sys.getrecursionlimit()
>>> sys.setrecursionlimit(1000)
>>> depth(500)
500
>>> depth(5000)
RecursionError
>>> sys.setrecursionlimit(old)

>>> def subsets(items):
...     if not items:
...         yield []
...         return
...     for rest in subsets(items[1:]):
...         yield rest
...         yield [items[0]] + rest
>>> list(subsets('ab'))
[[], ['a'], ['b'], ['a', 'b']]

>>> len(list(permutations(range(4)))), len(list(combinations(range(6), 3))), 2 ** 5
(24, 20, 32)

>>> list(combinations('abc', 2))
[('a', 'b'), ('a', 'c'), ('b', 'c')]

>>> len(list(permutations('aab'))), len(set(permutations('aab')))
(6, 3)

>>> nums = sorted([2, 1, 2])
>>> res = []
>>> def dfs(start, path):
...     res.append(path[:])
...     for i in range(start, len(nums)):
...         if i > start and nums[i] == nums[i - 1]:
...             continue
...         path.append(nums[i])
...         dfs(i + 1, path)
...         path.pop()
>>> dfs(0, [])
>>> res
[[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]

>>> res = []
>>> def dfs(start, remaining, path):
...     if remaining == 0:
...         res.append(path[:])
...         return
...     for i in range(start, len(cands)):
...         if cands[i] > remaining:
...             break
...         path.append(cands[i])
...         dfs(i, remaining - cands[i], path)
...         path.pop()
>>> cands = [1, 2]
>>> dfs(0, 4, [])
>>> res
[[1, 1, 1, 1], [1, 1, 2], [2, 2]]

>>> cells = [(0, 0), (1, 1), (2, 0), (1, 3)]
>>> [r - c for r, c in cells], [r + c for r, c in cells]
([0, 0, 2, -2], [0, 2, 2, 4])

>>> def collect(n, acc=[]):
...     if n == 0:
...         return acc
...     acc.append(n)
...     return collect(n - 1, acc)
>>> collect(2)
[2, 1]
>>> collect(2)
[2, 1, 2, 1]

>>> a = [1, 2, 3]
>>> out = []
>>> def permute(i):
...     if i == len(a):
...         out.append(a[:])
...         return
...     for j in range(i, len(a)):
...         a[i], a[j] = a[j], a[i]
...         permute(i + 1)
...         a[i], a[j] = a[j], a[i]
>>> permute(0)
>>> out
[[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 2, 1], [3, 1, 2]]

>>> list(product('01', repeat=2))
[('0', '0'), ('0', '1'), ('1', '0'), ('1', '1')]
"""


def subsets(nums):
    res, path = [], []

    def dfs(i):
        if i == len(nums):
            res.append(path[:])
            return
        path.append(nums[i])     # take nums[i]
        dfs(i + 1)
        path.pop()               # skip nums[i]
        dfs(i + 1)

    dfs(0)
    return res


def subsets_with_dups(nums):
    nums = sorted(nums)
    res, path = [], []

    def dfs(start):
        res.append(path[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue          # an equal sibling already started this branch
            path.append(nums[i])
            dfs(i + 1)
            path.pop()

    dfs(0)
    return res


def permute(nums):
    res, path, used = [], [], [False] * len(nums)

    def dfs():
        if len(path) == len(nums):
            res.append(path[:])
            return
        for i, x in enumerate(nums):
            if not used[i]:
                used[i] = True
                path.append(x)
                dfs()
                path.pop()
                used[i] = False

    dfs()
    return res


def unique_permutations(nums):
    nums = sorted(nums)
    res, path, used = [], [], [False] * len(nums)

    def dfs():
        if len(path) == len(nums):
            res.append(path[:])
            return
        for i, x in enumerate(nums):
            # among equal values, always place the leftmost unused copy first
            if used[i] or (i > 0 and nums[i] == nums[i - 1] and not used[i - 1]):
                continue
            used[i] = True
            path.append(x)
            dfs()
            path.pop()
            used[i] = False

    dfs()
    return res


def combinations_k(n, k):
    res, path = [], []

    def dfs(start):
        if len(path) == k:
            res.append(path[:])
            return
        need = k - len(path)
        for x in range(start, n - need + 2):    # stop once fewer than `need` numbers remain
            path.append(x)
            dfs(x + 1)
            path.pop()

    dfs(1)
    return res


def sums_with_reuse(cands, target):
    cands = sorted(cands)
    res, path = [], []

    def dfs(start, remaining):
        if remaining == 0:
            res.append(path[:])
            return
        for i in range(start, len(cands)):
            if cands[i] > remaining:
                break                         # sorted: every later candidate is too big too
            path.append(cands[i])
            dfs(i, remaining - cands[i])      # i, not i + 1: the same candidate can repeat
            path.pop()

    dfs(0, target)
    return res


def sums_without_reuse(cands, target):
    cands = sorted(cands)
    res, path = [], []

    def dfs(start, remaining):
        if remaining == 0:
            res.append(path[:])
            return
        for i in range(start, len(cands)):
            if cands[i] > remaining:
                break
            if i > start and cands[i] == cands[i - 1]:
                continue
            path.append(cands[i])
            dfs(i + 1, remaining - cands[i])
            path.pop()

    dfs(0, target)
    return res


def balanced_parens(n):
    res = []

    def dfs(s, opened, closed):
        if len(s) == 2 * n:
            res.append(s)
            return
        if opened < n:
            dfs(s + '(', opened + 1, closed)
        if closed < opened:
            dfs(s + ')', opened, closed + 1)

    dfs('', 0, 0)
    return res


def word_in_grid(board, word):
    rows, cols = len(board), len(board[0])

    def dfs(r, c, i):
        if i == len(word):
            return True
        if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != word[i]:
            return False
        saved, board[r][c] = board[r][c], None          # mark: used on this path
        found = any(dfs(r + dr, c + dc, i + 1) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        board[r][c] = saved                             # un-choose
        return found

    return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))


def n_queens(n):
    cols, diag, anti = set(), set(), set()

    def place(r):
        if r == n:
            return 1
        count = 0
        for c in range(n):
            if c in cols or r - c in diag or r + c in anti:
                continue
            cols.add(c)
            diag.add(r - c)
            anti.add(r + c)
            count += place(r + 1)
            cols.remove(c)
            diag.remove(r - c)
            anti.remove(r + c)
        return count

    return place(0)


def palindrome_splits(s):
    res, path = [], []

    def dfs(start):
        if start == len(s):
            res.append(path[:])
            return
        for end in range(start + 1, len(s) + 1):
            piece = s[start:end]
            if piece == piece[::-1]:
                path.append(piece)
                dfs(end)
                path.pop()

    dfs(0)
    return res


def cartesian(choices):
    res = []

    def dfs(i, prefix):
        if i == len(choices):
            res.append(prefix)
            return
        for ch in choices[i]:
            dfs(i + 1, prefix + ch)

    dfs(0, '')
    return res


def iter_subsets(nums):
    nums = tuple(nums)
    if not nums:
        yield ()
        return
    for rest in iter_subsets(nums[1:]):
        yield rest
        yield (nums[0],) + rest
