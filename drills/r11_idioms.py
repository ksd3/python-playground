"""R11 - Pythonic idioms and assignment order

In `a, b = x, y` the whole right side is evaluated first, then the targets are
assigned LEFT TO RIGHT, so when one target's position depends on another
(nums[i] and nums[nums[i]], or curr and curr.next) the order you write them in
decides what happens. Comprehensions read like the loops they replace: the
leftmost `for` is the outer loop; a trailing `if` filters, while `a if p else b`
in front transforms. Star targets always collect into a list. `for ... else`
runs the else only when the loop didn't break. zip(..., strict=True) needs 3.10+.

Part 1 - Predict. Each block in PREDICT is a REPL session. Replace every ???
with exactly what Python prints: expression values are echoed the way the REPL
echoes them, and a line that raises prints just the exception name (TypeError).

Part 2 - Drills. The first seven are rewrite drills: the docstring shows a
C-style loop, and the tests also check that your version is a single `return`
expression. Implement everything until `python check.py 11` is green. Don't
edit the tests at the bottom; add your own test_* functions if you like.

Unlocks: shorter code with fewer index bugs, placing each value at its home
index (cyclic sort), and pointer rewiring in linked structures.
"""
import ast
import inspect
import random
import textwrap

PREDICT = r"""
>>> nums = [1, 0]
>>> i = 0
>>> nums[i], nums[nums[i]] = nums[nums[i]], nums[i]
>>> nums
???

>>> nums = [1, 0]
>>> i = 0
>>> nums[nums[i]], nums[i] = nums[i], nums[nums[i]]
>>> nums
???

>>> x = [0, 0, 0]
>>> i = 0
>>> i, x[i] = 2, 9
>>> x
???

>>> x = [0, 0, 0]
>>> i = x[i] = 2
>>> i, x
???

>>> first, *mid, last = [1, 2, 3, 4, 5]
>>> first, mid, last
???
>>> first, *mid, last = (1, 2)
>>> mid
???
>>> head, *rest = 'abc'
>>> rest
???
>>> print(*rest, sep='-')
???

>>> a, b = [1, 2, 3]
???
>>> a, *b, c = [1]
???

>>> pairs = [('a', 1), ('b', 2)]
>>> [f'{i}:{k}={v}' for i, (k, v) in enumerate(pairs, 1)]
???

>>> [(r, c) for r in range(2) for c in range(3) if c != r]
???
>>> [[r * c for c in range(3)] for r in range(2)]
???

>>> [x for x in range(6) if x % 2]
???
>>> [x if x % 2 else -x for x in range(6)]
???
>>> [x for x in range(6) if x % 2 else -x]
???

>>> {len(w): w for w in ['hi', 'yo', 'hey']}
???
>>> {v: k for k, v in {'a': 1, 'b': 2, 'c': 1}.items()}
???

>>> list(zip(*[[1, 2, 3], [4, 5, 6]]))
???
>>> nums, letters = zip(*[(1, 'a'), (2, 'b')])
>>> nums, letters
???
>>> list(zip([1, 2], 'abc', strict=True))
???

>>> words = ['pear', 'fig', 'banana', 'kiwi']
>>> min(words, key=len), max(words, key=len)
???
>>> max(['ab', 'cd'], key=len)
???
>>> max([], default=None) is None
???
>>> min([])
???

>>> nums = [30, 10, 20, 10]
>>> min(range(len(nums)), key=nums.__getitem__)
???
>>> max(enumerate(nums), key=lambda p: p[1])
???

>>> for n in [4, 6, 9]:
...     if n % 2:
...         print('odd', n)
...         break
... else:
...     print('no odd')
???
>>> for n in []:
...     break
... else:
...     print('ran')
???

>>> it = iter([3, 1, 0, 4])
>>> out = []
>>> while (x := next(it, None)) is not None and x:
...     out.append(x)
>>> out
???
>>> [y for x in range(6) if (y := x * x) % 2]
???

>>> r, R = 3, 3
>>> 0 <= r < R
???
>>> 1 < 2 > 0, 1 < 2 < 1, 3 == 3 == 3.0
???
>>> x = 5
>>> x == 1 or 2
???
>>> x in (1, 2)
???

>>> xs = [3, 1, 3, 2, 1]
>>> sorted(set(xs))
???
>>> list(dict.fromkeys(xs))
???

>>> x = 0
>>> 'zero' if x == 0 else 'pos' if x > 0 else 'neg'
???
>>> 1 + 2 if False else 10
???

>>> class N:
...     def __init__(self, v, nxt=None):
...         self.v, self.next = v, nxt
>>> prev, curr = None, N(1, N(2, N(3)))
>>> while curr:
...     prev, curr.next, curr = curr, prev, curr.next
>>> [prev.v, prev.next.v, prev.next.next.v]
???
>>> prev, curr = None, N(1, N(2))
>>> while curr:
...     curr, curr.next, prev = curr.next, prev, curr
???
"""


class ListNode:
    """A singly linked list node (given). Used by reverse_list."""

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# ---------------------------------------------------------------- drills

def squares_of_odds(nums):
    """Rewrite as a single return expression:

        out = []
        for x in nums:
            if x % 2 != 0:
                out.append(x * x)
        return out
    """
    raise NotImplementedError


def flatten_grid(grid):
    """Rewrite as a single return expression:

        out = []
        for row in grid:
            for x in row:
                out.append(x)
        return out
    """
    raise NotImplementedError


def argmax(nums):
    """Index of the first largest value, -1 for an empty list. Rewrite as a
    single return expression:

        best = -1
        for i in range(len(nums)):
            if best == -1 or nums[i] > nums[best]:
                best = i
        return best
    """
    raise NotImplementedError


def invert(d):
    """Swap keys and values (the values are unique and hashable). Rewrite as a
    single return expression:

        out = {}
        for k in d:
            out[d[k]] = k
        return out
    """
    raise NotImplementedError


def count_matches(a, b):
    """How many positions hold equal items, comparing up to the shorter length.
    Rewrite as a single return expression:

        count = 0
        for i in range(min(len(a), len(b))):
            if a[i] == b[i]:
                count += 1
        return count
    """
    raise NotImplementedError


def transpose(matrix):
    """Rows become columns (all rows have the same length; the result is a list
    of lists). Rewrite as a single return expression:

        if not matrix:
            return []
        out = []
        for c in range(len(matrix[0])):
            row = []
            for r in range(len(matrix)):
                row.append(matrix[r][c])
            out.append(row)
        return out
    """
    raise NotImplementedError


def dedupe(items):
    """Drop repeats, keeping first-seen order. Rewrite as a single return
    expression:

        seen, out = set(), []
        for x in items:
            if x not in seen:
                seen.add(x)
                out.append(x)
        return out
    """
    raise NotImplementedError


def swap_home(nums, i):
    """Swap the values at index i and index nums[i], so the value nums[i] lands
    at its home index, in ONE tuple assignment (no temporary variable). Return
    None. With nums = [3, 0, 1, 2] and i = 0, nums becomes [2, 0, 1, 3]."""
    raise NotImplementedError


def cyclic_sort(nums):
    """nums holds each of 0..n-1 exactly once. Sort it in place in O(n) by
    sending values to their home index with swaps (swap_home). Return None."""
    raise NotImplementedError


def reverse_list(head):
    """Reverse a linked list of ListNode and return the new head. Walk it once;
    each step is ONE tuple assignment that flips curr.next and moves forward
    (the target order matters)."""
    raise NotImplementedError


def parse_ints(tokens):
    """Return int(t) for every token t that int() accepts, in order, skipping
    the others: parse_ints(['4', 'x', '-2']) == [4, -2]. Ask forgiveness
    (try/except) rather than permission."""
    raise NotImplementedError


def take_until(iterable, stop):
    """Return the items before the first one equal to stop (all of them if stop
    never appears). Consume the stop item but nothing after it. Any value can
    be an item, None included. A walrus loop fits here."""
    raise NotImplementedError


def pairwise_sums(a, b):
    """Elementwise sums [a[0] + b[0], a[1] + b[1], ...]. If the lengths differ,
    raise ValueError (zip has a flag for exactly this)."""
    raise NotImplementedError


# ---------------------------------------------------------------- tests (don't edit)

def _body(fn):
    """fn's statements without its docstring, or None when the source can't be
    read (then the style checks are skipped)."""
    try:
        node = ast.parse(textwrap.dedent(inspect.getsource(fn))).body[0]
    except (OSError, TypeError, SyntaxError, IndexError):
        return None
    if not isinstance(node, ast.FunctionDef):
        return None
    body = node.body
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
        body = body[1:]
    return body


def _single_expression(fn):
    body = _body(fn)
    return body is None or (len(body) == 1 and isinstance(body[0], ast.Return) and body[0].value is not None)


def _is_tuple_assignment(stmt):
    return isinstance(stmt, ast.Assign) and isinstance(stmt.targets[0], ast.Tuple)


class _WriteLimitedList(list):
    """A list that fails the test instead of looping forever."""

    def __init__(self, values, limit):
        super().__init__(values)
        self.writes, self.limit = 0, limit

    def __setitem__(self, index, value):
        self.writes += 1
        if self.writes > self.limit:
            raise AssertionError("too many writes: is each swap really swapping? (check the target order)")
        super().__setitem__(index, value)


def _build(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def _vals(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
        if len(out) > 10_000:
            raise AssertionError("the list has a cycle: a .next pointer was rewired wrongly")
    return out


_ONE_EXPRESSION = "rewrite it as a single return expression"


def test_squares_of_odds():
    assert squares_of_odds([1, 2, 3, 4, 5]) == [1, 9, 25]
    assert squares_of_odds([]) == []
    assert squares_of_odds([-3, 0]) == [9], "-3 is odd too"
    assert _single_expression(squares_of_odds), _ONE_EXPRESSION


def test_flatten_grid():
    assert flatten_grid([[1, 2], [3], [], [4, 5]]) == [1, 2, 3, 4, 5]
    assert flatten_grid([]) == []
    assert _single_expression(flatten_grid), _ONE_EXPRESSION


def test_argmax():
    assert argmax([3, 9, 2, 9]) == 1, "return the FIRST index of the maximum"
    assert argmax([-5]) == 0
    assert argmax([]) == -1
    rng = random.Random(11)
    for _ in range(100):
        nums = [rng.randint(-5, 5) for _ in range(rng.randint(1, 8))]
        assert argmax(nums) == nums.index(max(nums)), nums
    assert _single_expression(argmax), _ONE_EXPRESSION


def test_invert():
    assert invert({'a': 1, 'b': 2}) == {1: 'a', 2: 'b'}
    assert invert({}) == {}
    assert _single_expression(invert), _ONE_EXPRESSION


def test_count_matches():
    assert count_matches('abcd', 'abxd') == 3
    assert count_matches([1, 2, 3], [1, 2]) == 2, "compare up to the shorter length"
    assert count_matches([], [1]) == 0
    assert type(count_matches('a', 'a')) is int
    assert _single_expression(count_matches), _ONE_EXPRESSION


def test_transpose():
    assert transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
    assert transpose([[1], [2]]) == [[1, 2]]
    assert transpose([]) == []
    assert all(type(row) is list for row in transpose([[1, 2]])), "rows must be lists, not tuples"
    assert _single_expression(transpose), _ONE_EXPRESSION


def test_dedupe():
    assert dedupe([3, 1, 3, 2, 1]) == [3, 1, 2]
    assert dedupe('mississippi') == ['m', 'i', 's', 'p']
    assert dedupe([]) == []
    assert _single_expression(dedupe), _ONE_EXPRESSION


def test_swap_home():
    nums = [1, 0]
    assert swap_home(nums, 0) is None
    assert nums == [0, 1], "no swap happened: assign nums[nums[i]] before nums[i]"
    nums = [2, 1, 0, 3]
    swap_home(nums, 0)
    assert nums == [0, 1, 2, 3]
    nums = [3, 0, 1, 2]
    swap_home(nums, 0)
    assert nums == [2, 0, 1, 3], "the value 3 should land at index 3"
    body = _body(swap_home)
    assert body is None or (len(body) == 1 and _is_tuple_assignment(body[0])), "do it in one tuple assignment"


def test_cyclic_sort():
    rng = random.Random(11)
    for n in [0, 1, 2, 5, 50]:
        for _ in range(20):
            values = list(range(n))
            rng.shuffle(values)
            nums = _WriteLimitedList(values, limit=4 * n + 4)
            assert cyclic_sort(nums) is None
            assert list(nums) == list(range(n)), values


def test_reverse_list():
    assert _vals(reverse_list(_build([1, 2, 3, 4]))) == [4, 3, 2, 1]
    assert reverse_list(None) is None
    assert _vals(reverse_list(_build([7]))) == [7]
    body = _body(reverse_list)
    loops = [n for stmt in body or [] for n in ast.walk(stmt) if isinstance(n, ast.While)]
    assert body is None or any(len(w.body) == 1 and _is_tuple_assignment(w.body[0]) for w in loops), \
        "make each step of the while loop a single tuple assignment"


def test_parse_ints():
    tokens = ['1', '-2', ' 7 ', '3.5', 'x', '', '+4', '0x1f', '1_000']
    assert parse_ints(tokens) == [1, -2, 7, 4, 1000], \
        "use int() inside try/except ValueError: character checks like isdigit() reject '-2' and ' 7 '"
    assert parse_ints([]) == []


def test_take_until():
    assert take_until([3, 1, 0, 4], 0) == [3, 1]
    assert take_until([3, 1], 0) == [3, 1]
    assert take_until([], 0) == []
    it = iter('abc;def')
    assert take_until(it, ';') == ['a', 'b', 'c']
    assert ''.join(it) == 'def', "consume the stop item but nothing after it"
    assert take_until([None, 1, None], 1) == [None], "None is a real item here: use a private sentinel"


def test_pairwise_sums():
    assert pairwise_sums([1, 2, 3], [10, 20, 30]) == [11, 22, 33]
    assert pairwise_sums([], []) == []
    try:
        pairwise_sums([1, 2], [1])
    except ValueError:
        pass
    else:
        raise AssertionError("the lengths differ: raise ValueError (zip(..., strict=True))")
