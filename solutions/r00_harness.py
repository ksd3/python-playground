"""R00 - Your own test harness (reference solutions)

Compare after you've made your own attempt. Run: python check.py 0 -s
"""
import copy
from collections import deque

PREDICT = r"""
>>> 'hi'
'hi'
>>> print('hi')
hi

>>> None
>>> print(None)
None

>>> x = print('hi')
hi
>>> x is None
True

>>> print(['a', 1])
['a', 1]
>>> print('a', 1)
a 1

>>> str('a'), repr('a')
('a', "'a'")

>>> name, n = 'Ada', 3
>>> print(f'{name=} {n=}')
name='Ada' n=3
>>> f'{n + 1=}'
'n + 1=4'

>>> print(1, 2, 3, sep=', ')
1, 2, 3
>>> print('a', end=''); print('b')
ab

>>> print(*[1, 2, 3])
1 2 3
>>> print(*'abc', sep='-')
a-b-c

>>> type(True), isinstance(True, int)
(<class 'bool'>, True)
>>> type(True) is int
False

>>> assert 1 + 1 == 3, 'math broke'
AssertionError
>>> 'still here'
'still here'

>>> getattr('abc', 'upper')()
'ABC'
>>> getattr(5, 'nope', 'fallback')
'fallback'
>>> getattr(5, 'nope')
AttributeError

>>> args, kwargs = (7, 2), {}
>>> divmod(*args, **kwargs)
(3, 1)

>>> 6 * 7
42
>>> _ + 1
43
"""


def check(fn, cases):
    name = getattr(fn, "__name__", repr(fn))
    ok = True
    for args, expected in cases:
        try:
            got = fn(*args)
        except Exception as exc:
            print(f"{name}{args!r} raised {exc!r}; expected {expected!r}")
            ok = False
            continue
        if got != expected:
            print(f"{name}{args!r} returned {got!r}; expected {expected!r}")
            ok = False
    return ok


def stress(fast, brute, gen, trials=500):
    for _ in range(trials):
        args = gen()
        if fast(*copy.deepcopy(args)) != brute(*copy.deepcopy(args)):
            return args
    return None


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_list(vals):
    dummy = tail = ListNode()
    for v in vals:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def list_vals(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def build_tree(vals):
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    queue, i = deque([root]), 1
    while queue and i < len(vals):
        node = queue.popleft()
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            queue.append(node.right)
        i += 1
    return root


def tree_vals(root):
    out, queue = [], deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            out.append(None)
            continue
        out.append(node.val)
        queue.append(node.left)
        queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


def run_ops(cls, ops, args):
    obj = cls(*args[0])
    results = [None]
    for name, call_args in zip(ops[1:], args[1:]):
        results.append(getattr(obj, name)(*call_args))
    return results
