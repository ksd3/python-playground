"""R27 - Recursion and backtracking

The template: choose, explore, un-choose. Grow one `path`, recurse, then undo
the change, and collect copies (path[:]) because the path keeps changing.
Subsets: take/skip each item, or loop from a start index. Permutations: a used[]
array or swapping. Combinations: a start index, pruned when too few items remain.
Reuse allowed: recurse on i, not i + 1. Duplicates: sort, then skip equal
siblings (i > start and nums[i] == nums[i - 1]). Grid search: mark a cell,
recurse, unmark it. N queens: sets for columns and both diagonals (r - c, r + c).
Know the sizes before you start: 2**n subsets, n! permutations. Python stops
recursing at sys.getrecursionlimit() frames (1000 by default).

Part 1 - Predict. Each block in PREDICT is a REPL session. Replace every ???
with exactly what Python prints: expression values are echoed the way the REPL
echoes them, and a line that raises prints just the exception name (TypeError).

Part 2 - Drills. Implement every function until `python check.py 27` is green.
Don't edit the tests at the bottom; add your own test_* functions if you like.
"Any order" means the tests sort your answer before comparing.

Unlocks: "generate all subsets/orderings/combinations", sums built from
candidates, word paths in a grid, placement puzzles, partitioning a string.
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
???

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
???

>>> out = []
>>> def gen(s, n):
...     if len(s) == n:
...         out.append(s)
...         return
...     for c in '01':
...         gen(s + c, n)
>>> gen('', 2)
>>> out
???

>>> def depth(n):
...     return 0 if n == 0 else 1 + depth(n - 1)
>>> old = sys.getrecursionlimit()
>>> sys.setrecursionlimit(1000)
>>> depth(500)
???
>>> depth(5000)
???
>>> sys.setrecursionlimit(old)

>>> def subsets(items):
...     if not items:
...         yield []
...         return
...     for rest in subsets(items[1:]):
...         yield rest
...         yield [items[0]] + rest
>>> list(subsets('ab'))
???

>>> len(list(permutations(range(4)))), len(list(combinations(range(6), 3))), 2 ** 5
???

>>> list(combinations('abc', 2))
???

>>> len(list(permutations('aab'))), len(set(permutations('aab')))
???

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
???

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
???

>>> cells = [(0, 0), (1, 1), (2, 0), (1, 3)]
>>> [r - c for r, c in cells], [r + c for r, c in cells]
???

>>> def collect(n, acc=[]):
...     if n == 0:
...         return acc
...     acc.append(n)
...     return collect(n - 1, acc)
>>> collect(2)
???
>>> collect(2)
???

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
???

>>> list(product('01', repeat=2))
???
"""


# ---------------------------------------------------------------- drills

def subsets(nums):
    """All subsets of nums (distinct values), as lists. Each subset keeps the
    input order; the subsets themselves can come in any order.
    subsets([1, 2]) -> [[], [1], [2], [1, 2]] in some order."""
    raise NotImplementedError


def subsets_with_dups(nums):
    """nums may repeat values. Return every distinct subset exactly once, each
    as a sorted list, in any order.
    subsets_with_dups([2, 1, 2]) -> [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]."""
    raise NotImplementedError


def permute(nums):
    """All orderings of nums (distinct values), as lists, in any order.
    permute([1, 2]) -> [[1, 2], [2, 1]]."""
    raise NotImplementedError


def unique_permutations(nums):
    """nums may repeat values. Return every distinct ordering exactly once, as
    lists, in any order. unique_permutations([1, 1, 2]) has 3 orderings."""
    raise NotImplementedError


def combinations_k(n, k):
    """All k-element combinations of 1..n, each as an ascending list, in any
    order. Prune branches that can't reach k items.
    combinations_k(4, 2) has 6 combinations, from [1, 2] to [3, 4]."""
    raise NotImplementedError


def sums_with_reuse(cands, target):
    """cands are distinct positive ints, each usable any number of times.
    Return every combination summing to target (a positive int) once, each as
    a non-decreasing list, in any order.
    sums_with_reuse([2, 3, 6, 7], 7) -> [[2, 2, 3], [7]]."""
    raise NotImplementedError


def sums_without_reuse(cands, target):
    """cands are positive ints that may repeat; each element is used at most
    once. Return every distinct combination summing to target once, each as a
    non-decreasing list, in any order.
    sums_without_reuse([10, 1, 2, 7, 6, 1, 5], 8) -> [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]."""
    raise NotImplementedError


def balanced_parens(n):
    """Every string of n pairs of correctly nested parentheses, in any order.
    balanced_parens(2) -> ['(())', '()()']; balanced_parens(0) -> ['']."""
    raise NotImplementedError


def word_in_grid(board, word):
    """board is a list of lists of single characters. Return True if word
    (non-empty) can be traced through horizontally or vertically adjacent
    cells, using no cell twice; else False. Leave board exactly as you found it."""
    raise NotImplementedError


def n_queens(n):
    """How many ways can n queens be placed on an n x n board with no two
    sharing a row, column, or diagonal? (n >= 1) n_queens(4) == 2."""
    raise NotImplementedError


def palindrome_splits(s):
    """Every way to cut s into pieces that are all palindromes, each way as a
    list of pieces in order, in any order.
    palindrome_splits('aab') -> [['a', 'a', 'b'], ['aa', 'b']]; palindrome_splits('') -> [[]]."""
    raise NotImplementedError


def cartesian(choices):
    """choices is a list of strings. Return every string made by picking one
    character from each, in order, sorted the way nested loops produce them.
    cartesian(['ab', 'cd']) == ['ac', 'ad', 'bc', 'bd']; cartesian([]) == ['']."""
    raise NotImplementedError


def iter_subsets(nums):
    """A generator function: lazily yield every subset of nums (distinct
    values) as a tuple in input order, in any order, using yield / yield from.
    sorted(iter_subsets([1, 2])) == [(), (1,), (1, 2), (2,)]."""
    raise NotImplementedError


# ---------------------------------------------------------------- tests (don't edit)

import itertools as _itertools
import random as _random
import types as _types


def _canon(lists):
    return sorted(tuple(x) for x in lists)


def _all_subsets(nums):
    return [list(c) for r in range(len(nums) + 1) for c in _itertools.combinations(nums, r)]


def test_subsets():
    out = subsets([1, 2, 3])
    assert len(out) == 8
    assert _canon(out) == _canon(_all_subsets([1, 2, 3])), "wrong subsets: did you append path instead of path[:]?"
    assert subsets([]) == [[]]
    assert all(isinstance(s, list) for s in out)
    assert len({id(s) for s in out}) == len(out), "every subset must be its own list"
    rng = _random.Random(27)
    for _ in range(30):
        nums = rng.sample(range(50), rng.randint(0, 7))
        assert _canon(subsets(nums)) == _canon(_all_subsets(nums)), nums


def test_subsets_with_dups():
    out = subsets_with_dups([2, 1, 2])
    assert _canon(out) == [(), (1,), (1, 2), (1, 2, 2), (2,), (2, 2)]
    assert len(out) == len(set(map(tuple, out))), "duplicate subsets: sort first, then skip equal siblings"
    assert subsets_with_dups([]) == [[]]
    rng = _random.Random(27)
    for _ in range(60):
        nums = [rng.randint(0, 3) for _ in range(rng.randint(0, 8))]
        want = sorted({tuple(sorted(c)) for r in range(len(nums) + 1) for c in _itertools.combinations(nums, r)})
        got = subsets_with_dups(nums)
        assert sorted(tuple(x) for x in got) == want, nums


def test_permute():
    assert _canon(permute([1, 2, 3])) == sorted(_itertools.permutations([1, 2, 3]))
    assert permute([]) == [[]]
    assert permute([5]) == [[5]]
    rng = _random.Random(27)
    for _ in range(20):
        nums = rng.sample(range(20), rng.randint(0, 6))
        assert _canon(permute(nums)) == sorted(_itertools.permutations(nums)), nums


def test_unique_permutations():
    out = unique_permutations([1, 1, 2])
    assert _canon(out) == [(1, 1, 2), (1, 2, 1), (2, 1, 1)], "repeated orderings: skip equal values you've already placed at this position"
    assert unique_permutations([]) == [[]]
    rng = _random.Random(27)
    for _ in range(40):
        nums = [rng.randint(0, 2) for _ in range(rng.randint(0, 7))]
        assert _canon(unique_permutations(nums)) == sorted(set(_itertools.permutations(nums))), nums


def test_combinations_k():
    assert _canon(combinations_k(4, 2)) == [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
    assert combinations_k(5, 0) == [[]]
    assert combinations_k(3, 4) == []
    assert combinations_k(3, 3) == [[1, 2, 3]]
    for n in range(0, 9):
        for k in range(0, n + 1):
            got = combinations_k(n, k)
            assert _canon(got) == sorted(_itertools.combinations(range(1, n + 1), k)), (n, k)
    assert len(combinations_k(20, 18)) == 190


def test_sums_with_reuse():
    assert _canon(sums_with_reuse([2, 3, 6, 7], 7)) == [(2, 2, 3), (7,)]
    assert _canon(sums_with_reuse([2, 3, 5], 8)) == [(2, 2, 2, 2), (2, 3, 3), (3, 5)]
    assert sums_with_reuse([2], 1) == []
    assert _canon(sums_with_reuse([7, 3, 2], 7)) == [(2, 2, 3), (7,)], "unsorted candidates: sort them, and keep each answer non-decreasing"
    rng = _random.Random(27)
    for _ in range(60):
        cands = rng.sample(range(1, 9), rng.randint(1, 4))
        target = rng.randint(1, 12)
        want = sorted({c for r in range(1, target // min(cands) + 1)
                       for c in _itertools.combinations_with_replacement(sorted(cands), r) if sum(c) == target})
        assert _canon(sums_with_reuse(cands, target)) == want, (cands, target)


def test_sums_without_reuse():
    assert _canon(sums_without_reuse([10, 1, 2, 7, 6, 1, 5], 8)) == [(1, 1, 6), (1, 2, 5), (1, 7), (2, 6)]
    assert _canon(sums_without_reuse([2, 5, 2, 1, 2], 5)) == [(1, 2, 2), (5,)], "duplicate combinations: sort, then skip equal siblings"
    assert sums_without_reuse([3], 2) == []
    rng = _random.Random(27)
    for _ in range(60):
        cands = [rng.randint(1, 6) for _ in range(rng.randint(1, 8))]
        target = rng.randint(1, 12)
        want = sorted({tuple(sorted(c)) for r in range(1, len(cands) + 1)
                       for c in _itertools.combinations(cands, r) if sum(c) == target})
        assert _canon(sums_without_reuse(cands, target)) == want, (cands, target)


def _balanced(s):
    depth = 0
    for ch in s:
        depth += 1 if ch == '(' else -1
        if depth < 0:
            return False
    return depth == 0


def test_balanced_parens():
    assert sorted(balanced_parens(3)) == ['((()))', '(()())', '(())()', '()(())', '()()()']
    assert balanced_parens(0) == ['']
    assert balanced_parens(1) == ['()']
    for n, count in enumerate([1, 1, 2, 5, 14, 42, 132, 429, 1430]):
        out = balanced_parens(n)
        assert len(out) == count, f"n = {n}: expected {count} strings, got {len(out)}"
        assert len(set(out)) == count and all(len(s) == 2 * n and _balanced(s) for s in out), n


def test_word_in_grid():
    board = [list('ABCE'), list('SFCS'), list('ADEE')]
    snapshot = [row[:] for row in board]
    assert word_in_grid(board, 'ABCCED') is True
    assert board == snapshot, "restore every cell you mark (un-choose)"
    assert word_in_grid(board, 'SEE') is True
    assert word_in_grid(board, 'ABCB') is False, "a cell can't be used twice in one word"
    assert board == snapshot, "restore every cell you mark (un-choose)"
    assert word_in_grid([['a']], 'a') is True
    assert word_in_grid([['a']], 'aa') is False
    assert word_in_grid([list('ab'), list('cd')], 'abdc') is True
    assert word_in_grid([list('ab'), list('cd')], 'ad') is False, "no diagonal moves"
    assert word_in_grid([list('ab'), list('ba')], 'abab') is True
    assert word_in_grid([list('ab'), list('ba')], 'ababa') is False
    assert word_in_grid([list('aaa'), list('aaa')], 'aaaaaaa') is False


def test_n_queens():
    got = [n_queens(n) for n in range(1, 9)]
    assert got == [1, 0, 0, 2, 10, 4, 40, 92], f"{got}: check both diagonals (r - c and r + c)"


def _brute_splits(s):
    n, out = len(s), []
    for mask in range(1 << max(n - 1, 0)):
        pieces, start = [], 0
        for i in range(1, n):
            if mask >> (i - 1) & 1:
                pieces.append(s[start:i])
                start = i
        pieces.append(s[start:])
        if all(p == p[::-1] for p in pieces):
            out.append(pieces)
    return out if s else [[]]


def test_palindrome_splits():
    assert _canon(palindrome_splits('aab')) == [('a', 'a', 'b'), ('aa', 'b')]
    assert palindrome_splits('a') == [['a']]
    assert palindrome_splits('') == [[]]
    rng = _random.Random(27)
    for _ in range(60):
        s = ''.join(rng.choice('ab') for _ in range(rng.randint(1, 8)))
        assert _canon(palindrome_splits(s)) == _canon(_brute_splits(s)), s


def test_cartesian():
    assert cartesian(['ab', 'cd']) == ['ac', 'ad', 'bc', 'bd']
    assert cartesian([]) == ['']
    assert cartesian(['ab', '']) == []
    assert cartesian(['xyz']) == ['x', 'y', 'z']
    rng = _random.Random(27)
    for _ in range(40):
        choices = [''.join(rng.sample('abcdef', rng.randint(1, 3))) for _ in range(rng.randint(0, 4))]
        assert cartesian(choices) == [''.join(p) for p in _itertools.product(*choices)], choices


def test_iter_subsets():
    gen = iter_subsets([1, 2, 3])
    assert isinstance(gen, _types.GeneratorType), "write it as a generator function: use yield"
    out = list(gen)
    assert sorted(out) == sorted(c for r in range(4) for c in _itertools.combinations([1, 2, 3], r))
    assert list(iter_subsets([])) == [()]
    first = next(iter_subsets(range(20)))
    assert isinstance(first, tuple)
    rng = _random.Random(27)
    for _ in range(20):
        nums = rng.sample(range(30), rng.randint(0, 6))
        want = sorted(c for r in range(len(nums) + 1) for c in _itertools.combinations(nums, r))
        assert sorted(iter_subsets(nums)) == want, nums
