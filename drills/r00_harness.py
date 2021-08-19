"""R00 - Your own test harness

Every later routine leans on four habits: running code in the REPL to see what
it really does, checking a function against expected outputs, stress-testing a
fast version against a brute force, and building linked lists and trees from
plain Python lists. Here you write those tools yourself.
REPL habits: `python -i file.py` opens the REPL with your definitions loaded;
help(obj) and dir(obj) say what something can do; f"{x=}" prints a name with
its value; breakpoint() pauses a running script; in the REPL, _ is the last
echoed value.

Part 1 - Predict. Each block in PREDICT is a REPL session. Replace every ???
with exactly what Python prints: expression values are echoed the way the REPL
echoes them, and a line that raises prints just the exception name (TypeError).

Part 2 - Drills. Implement every function until `python check.py 0` is green.
Don't edit the tests at the bottom; add your own test_* functions if you like.

Unlocks: everything after this. Stress-testing a fast solution against a brute
force is the single most valuable habit in this repo.
"""
import collections
import contextlib
import copy
import io
import random

PREDICT = r"""
>>> 'hi'
???
>>> print('hi')
???

>>> None
>>> print(None)
???

>>> x = print('hi')
???
>>> x is None
???

>>> print(['a', 1])
???
>>> print('a', 1)
???

>>> str('a'), repr('a')
???

>>> name, n = 'Ada', 3
>>> print(f'{name=} {n=}')
???
>>> f'{n + 1=}'
???

>>> print(1, 2, 3, sep=', ')
???
>>> print('a', end=''); print('b')
???

>>> print(*[1, 2, 3])
???
>>> print(*'abc', sep='-')
???

>>> type(True), isinstance(True, int)
???
>>> type(True) is int
???

>>> assert 1 + 1 == 3, 'math broke'
???
>>> 'still here'
???

>>> getattr('abc', 'upper')()
???
>>> getattr(5, 'nope', 'fallback')
???
>>> getattr(5, 'nope')
???

>>> args, kwargs = (7, 2), {}
>>> divmod(*args, **kwargs)
???

>>> 6 * 7
???
>>> _ + 1
???
"""


# ---------------------------------------------------------------- drills

def check(fn, cases):
    """Run fn(*args) for every (args, expected) pair in cases and return True
    if every result matches. For each mismatch print the args, the expected
    value and what fn returned, all with repr(). A case that raises counts as
    a mismatch (print the exception with repr()) and checking carries on.
    Print nothing when every case passes.
    check(len, [(('ab',), 2), (([],), 0)]) -> True"""
    raise NotImplementedError


def stress(fast, brute, gen, trials=500):
    """Call gen() up to `trials` times; each call returns a tuple of args. Run
    fast(*args) and brute(*args), each on its own copy.deepcopy of the args,
    and return the first args tuple (unmodified) where the two results differ,
    or None if they always agree."""
    raise NotImplementedError


class ListNode:
    """A singly linked list node: ListNode(val=0, next=None) stores both as
    attributes. ListNode(1, ListNode(2)) is the list 1 -> 2."""

    def __init__(self, val=0, next=None):
        raise NotImplementedError


class TreeNode:
    """A binary tree node: TreeNode(val=0, left=None, right=None) stores all
    three as attributes."""

    def __init__(self, val=0, left=None, right=None):
        raise NotImplementedError


def build_list(vals):
    """Return the head ListNode of a linked list holding vals in order, or
    None when vals is empty. Must handle 10**5 values (no recursion)."""
    raise NotImplementedError


def list_vals(head):
    """Return the values of the linked list starting at head as a Python list
    ([] for None). Must handle 10**5 nodes (no recursion)."""
    raise NotImplementedError


def build_tree(vals):
    """Build a binary tree from level order with None for missing children
    and return the root (None when vals is empty or vals[0] is None).
    Children are listed only for nodes that exist: [1, None, 2, 3] is 1 with
    right child 2, and 2 has left child 3. Must handle very deep trees, so no
    recursion."""
    raise NotImplementedError


def tree_vals(root):
    """The inverse of build_tree: level order with None for missing children,
    trailing Nones dropped. tree_vals(build_tree([1, None, 2, 3])) ==
    [1, None, 2, 3]. Must handle very deep trees, so no recursion."""
    raise NotImplementedError


def run_ops(cls, ops, args):
    """Replay a recorded call sequence: ops[0] names the class and args[0]
    holds the constructor args; every later ops[i] is a method name, called
    with *args[i] on that one instance. Return all the results, with None for
    the constructor. Use getattr.
    run_ops(list, ['list', 'append', 'pop'], [[[]], [7], []]) == [None, None, 7]"""
    raise NotImplementedError


# ---------------------------------------------------------------- tests (don't edit)

def _captured(fn, *args, **kwargs):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        result = fn(*args, **kwargs)
    return result, out.getvalue()


class _N:
    def __init__(self, val, next=None):
        self.val, self.next = val, next


class _T:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right


def _build_list(vals):
    head = None
    for v in reversed(vals):
        head = _N(v, head)
    return head


def _list_vals(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def _build_tree(vals):
    if not vals or vals[0] is None:
        return None
    root = _T(vals[0])
    queue, i = collections.deque([root]), 1
    while queue and i < len(vals):
        node = queue.popleft()
        for side in ('left', 'right'):
            if i < len(vals) and vals[i] is not None:
                child = _T(vals[i])
                setattr(node, side, child)
                queue.append(child)
            i += 1
    return root


def _tree_vals(root):
    out, queue = [], collections.deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


class _Box:
    def __init__(self, start):
        self.total = start

    def put(self, x):
        self.total += x

    def get(self):
        return self.total


def test_check():
    ok, printed = _captured(check, lambda a, b: a + b, [((1, 2), 3), ((2, 2), 4)])
    assert ok is True
    assert printed == '', "print nothing when every case passes"
    ok, printed = _captured(check, str.upper, [(('a',), 'A'), (('b',), 'b')])
    assert ok is False
    assert "'B'" in printed, "show what fn returned, with repr()"
    calls = []

    def risky(x):
        calls.append(x)
        return 10 // x

    ok, printed = _captured(check, risky, [((0,), 0), ((5,), 2)])
    assert ok is False and 'ZeroDivisionError' in printed, "print the exception with repr()"
    assert calls == [0, 5], "keep checking after a case that raises"


def test_stress():
    rng = random.Random(0)
    assert stress(sorted, lambda xs: sorted(xs), lambda: ([rng.randint(0, 9) for _ in range(5)],)) is None

    def gen():
        return ([rng.randint(0, 9) for _ in range(rng.randint(0, 3))],)

    found = stress(lambda xs: max(xs) if xs else 0, lambda xs: max(xs, default=-1), gen)
    assert found == ([],), "return the args where fast and brute disagree"
    shared = stress(lambda xs: xs.pop(), lambda xs: xs.pop(), lambda: ([1, 2, 3],))
    assert shared is None, "give fast and brute separate copy.deepcopy(args)"
    found = stress(lambda xs: xs.clear(), lambda xs: len(xs), lambda: ([1, 2, 3],))
    assert found == ([1, 2, 3],), "return the args as gen made them, before any mutation"
    calls = []

    def counting_gen():
        calls.append(1)
        return (len(calls),)

    assert stress(abs, abs, counting_gen, trials=37) is None and len(calls) == 37
    calls.clear()
    assert stress(lambda i: -1 if i == 5 else i, lambda i: i, counting_gen) == (5,)
    assert len(calls) == 5, "stop at the first failure"


def test_ListNode():
    n = ListNode()
    assert n.val == 0 and n.next is None
    m = ListNode(5, n)
    assert m.val == 5 and m.next is n
    assert ListNode(val=3).val == 3 and ListNode(next=n).next is n


def test_TreeNode():
    t = TreeNode()
    assert t.val == 0 and t.left is None and t.right is None
    a, b = TreeNode(2), TreeNode(3)
    root = TreeNode(1, a, b)
    assert root.val == 1 and root.left is a and root.right is b
    only_right = TreeNode(right=b)
    assert only_right.right is b and only_right.left is None


def test_build_list():
    head = build_list([1, 2, 3])
    assert head.val == 1 and head.next.val == 2 and head.next.next.val == 3
    assert head.next.next.next is None
    assert build_list([]) is None
    assert _list_vals(build_list(['x'])) == ['x']
    big = list(range(10**5))
    assert _list_vals(build_list(big)) == big


def test_list_vals():
    assert list_vals(None) == []
    assert list_vals(_build_list([4, 5, 6])) == [4, 5, 6]
    big = list(range(10**5))
    assert list_vals(_build_list(big)) == big


def test_build_tree():
    root = build_tree([1, None, 2, 3])
    assert root.val == 1 and root.left is None
    assert root.right.val == 2 and root.right.left.val == 3 and root.right.right is None
    assert build_tree([]) is None and build_tree([None]) is None
    full = build_tree([1, 2, 3, 4, 5, 6, 7])
    assert full.left.right.val == 5 and full.right.left.val == 6
    for vals in ([1], [1, 2], [0, None, 0, None, 0],
                 [5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1]):
        assert _tree_vals(build_tree(vals)) == vals, "children are listed only for nodes that exist"
    chain = [0] + [x for i in range(1, 5000) for x in (i, None)]
    node, depth = build_tree(chain), 0
    while node:
        node, depth = node.left, depth + 1
    assert depth == 5000


def test_tree_vals():
    assert tree_vals(None) == []
    assert tree_vals(_T(1)) == [1]
    assert tree_vals(_T(1, _T(2))) == [1, 2], "drop trailing Nones"
    for vals in ([1, None, 2, 3], [1, 2, 3, 4, 5, 6, 7],
                 [5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1]):
        assert tree_vals(_build_tree(vals)) == vals
    chain = [0] + [x for i in range(1, 5000) for x in (None, i)]
    assert tree_vals(_build_tree(chain)) == chain


def test_run_ops():
    assert run_ops(_Box, ['_Box', 'put', 'put', 'get'], [[5], [3], [2], []]) == [None, None, None, 10]
    assert run_ops(_Box, ['_Box', 'get'], [[0], []]) == [None, 0]
    out = run_ops(list, ['list', 'append', 'append', 'pop', '__len__'], [[[]], [1], [2], [], []])
    assert out == [None, None, None, 2, 1]
