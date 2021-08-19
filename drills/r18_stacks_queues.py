"""R18 - Stacks, queues, monotonic structures

A stack is a list (append, pop, [-1]); a queue is a deque (append, popleft).
list.pop(0) shifts every element, so it's O(n). A monotonic stack keeps indices
whose values only rise (or only fall) from bottom to top; each index is pushed
and popped once, so a whole pass is O(n). Store indices, not values: widths and
distances come from index differences. A sentinel value at the end flushes
whatever is left on the stack. A monotonic deque does the same for a sliding
window, and an explicit stack turns any recursive DFS into a loop.

Part 1 - Predict. Each block in PREDICT is a REPL session. Replace every ???
with exactly what Python prints: expression values are echoed the way the REPL
echoes them, and a line that raises prints just the exception name (TypeError).

Part 2 - Drills. Implement every function until `python check.py 18` is green.
Don't edit the tests at the bottom; add your own test_* functions if you like.

Unlocks: bracket matching, expression evaluation, next-greater and span-style
problems, histogram areas, trapped water, and sliding-window extremes.
"""

PREDICT = r"""
>>> st = []
>>> st.append(1); st.append(2); st.append(3)
>>> st.pop(), st[-1], st
???

>>> [].pop()
???
>>> deque().popleft()
???

>>> st = []
>>> st and st[-1]
???
>>> st = [5]
>>> st and st[-1]
???

>>> d = deque([1, 2, 3])
>>> d[1], d[-1]
???
>>> d[0:2]
???

>>> d = deque([1, 2, 3, 4])
>>> d.rotate(1)
>>> d
???
>>> d.rotate(-2)
>>> d
???

>>> d = deque(maxlen=3)
>>> for x in range(5):
...     d.append(x)
>>> d
???
>>> d.appendleft(9)
>>> d
???

>>> inbox, outbox = [], []
>>> for x in (1, 2, 3):
...     inbox.append(x)
>>> if not outbox:
...     while inbox:
...         outbox.append(inbox.pop())
>>> outbox.pop(), outbox, inbox
???

>>> pairs = {')': '(', ']': '[', '}': '{'}
>>> st = []
>>> for ch in '([)]':
...     if ch in pairs:
...         if not st or st.pop() != pairs[ch]:
...             print('bad at', ch)
...             break
...     else:
...         st.append(ch)
???

>>> st = [10, 3]
>>> st.pop() - st.pop()
???

>>> st = []
>>> for tok in '3 4 + 2 *'.split():
...     if tok in ('+', '-', '*'):
...         b, a = st.pop(), st.pop()
...         st.append(a + b if tok == '+' else a - b if tok == '-' else a * b)
...     else:
...         st.append(int(tok))
>>> st
???

>>> -7 // 2, int(-7 / 2), -(7 // 2)
???

>>> nums = [2, 1, 2, 4, 3]
>>> ans, st = [-1] * len(nums), []
>>> for i, x in enumerate(nums):
...     while st and nums[st[-1]] < x:
...         ans[st.pop()] = x
...     st.append(i)
>>> ans, st
???

>>> nums = [2, 2, 1]
>>> st, popped = [], []
>>> for i, x in enumerate(nums):
...     while st and nums[st[-1]] <= x:
...         popped.append(st.pop())
...     st.append(i)
>>> st, popped
???

>>> heights = [2, 1, 2]
>>> st, best = [], 0
>>> for i, h in enumerate(heights + [0]):
...     while st and heights[st[-1]] >= h:
...         top = st.pop()
...         left = st[-1] if st else -1
...         best = max(best, heights[top] * (i - left - 1))
...     st.append(i)
>>> best
???

>>> def window_max(nums, k):
...     dq, out = deque(), []
...     for i, x in enumerate(nums):
...         while dq and nums[dq[-1]] <= x:
...             dq.pop()
...         dq.append(i)
...         if dq[0] <= i - k:
...             dq.popleft()
...         if i >= k - 1:
...             out.append(nums[dq[0]])
...     return out
>>> window_max([1, 3, -1, -3, 5, 3], 3)
???

>>> graph = {1: [2, 3], 2: [4], 3: [], 4: []}
>>> def order(push):
...     st, out = [1], []
...     while st:
...         node = st.pop()
...         out.append(node)
...         st.extend(push(graph[node]))
...     return out
>>> order(list), order(reversed)
???
"""


# ---------------------------------------------------------------- drills

def is_balanced(s):
    """Return True if every bracket in s (only the characters ()[]{}) is closed by
    the matching bracket in the right order. '([]{})' -> True, '([)]' -> False."""
    raise NotImplementedError


def longest_balanced(s):
    """Length of the longest contiguous substring of s (only '(' and ')') whose
    parentheses are balanced. longest_balanced(')()())') == 4. O(n): keep a stack
    of indices with the index just before the current run at the bottom."""
    raise NotImplementedError


def eval_postfix(tokens):
    """Evaluate a postfix expression given as a list of tokens: integers (possibly
    negative, like '-3') and the operators + - * /. Division truncates toward zero.
    eval_postfix(['2', '1', '+', '3', '*']) == 9."""
    raise NotImplementedError


def eval_infix(expr):
    """Evaluate a string of non-negative integers, + - * /, parentheses and spaces
    with normal precedence (* and / before + and -, equal precedence left to
    right). Division truncates toward zero. No unary minus.
    eval_infix('2 * (3 + 4) - 5') == 9."""
    raise NotImplementedError


class QueueFromStacks:
    """FIFO queue built from two lists used only as stacks (append, pop, [-1], len);
    no deque. push(x); pop() and peek() return the oldest item and raise IndexError
    when empty; len(q). Amortized O(1) per operation."""

    def __init__(self):
        raise NotImplementedError

    def push(self, x):
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError

    def peek(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError


class StackFromQueue:
    """LIFO stack built from ONE deque used only as a queue (append, popleft, [0],
    len); no lists. push(x); pop() and top() return the newest item and raise
    IndexError when empty; len(s). push may cost O(n)."""

    def __init__(self):
        raise NotImplementedError

    def push(self, x):
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError

    def top(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError


def next_greater(nums):
    """For each element, the first value to its right that is strictly greater,
    or -1. next_greater([2, 1, 2, 4, 3]) == [4, 2, 4, -1, -1]. O(n)."""
    raise NotImplementedError


def prev_smaller_index(nums):
    """For each i, the index of the nearest j < i with nums[j] < nums[i], or -1.
    prev_smaller_index([3, 1, 4, 1, 5]) == [-1, -1, 1, -1, 3]. O(n)."""
    raise NotImplementedError


def wait_for_greater(nums):
    """For each i, how many steps to the right you must go to reach a strictly
    greater value, or 0 if there's none. wait_for_greater([3, 1, 2, 5]) == [3, 1, 1, 0].
    O(n)."""
    raise NotImplementedError


def next_greater_circular(nums):
    """Like next_greater, but the array wraps around: after the last element the
    search continues from the start. next_greater_circular([1, 2, 1]) == [2, -1, 2].
    O(n): walk the indices twice."""
    raise NotImplementedError


def largest_rectangle(heights):
    """Area of the largest rectangle that fits under a bar chart of unit-width bars
    with these heights (a list). largest_rectangle([2, 1, 5, 6, 2, 3]) == 10.
    O(n) with a monotonic stack and a 0-height sentinel at the end."""
    raise NotImplementedError


def trapped_water(heights):
    """Units of water held between bars of these heights after rain.
    trapped_water([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6. O(n)."""
    raise NotImplementedError


def window_max(nums, k):
    """Maximum of every contiguous window of size k (1 <= k <= len(nums)), left to
    right. window_max([1, 3, -1, -3, 5, 3], 3) == [3, 3, 5, 5]. O(n) with a deque
    of indices whose values decrease."""
    raise NotImplementedError


def dfs_order(graph, start):
    """Preorder DFS from start over graph (a dict: node -> list of neighbors; a
    node with no entry has no neighbors), visiting neighbors in listed order and
    each node once: exactly the order the recursive version produces. Iterative,
    because the graph can be a 5000-node chain."""
    raise NotImplementedError


# ---------------------------------------------------------------- tests (don't edit)

import random
from collections import deque


def _bf_balanced(s):
    prev = None
    while prev != s:
        prev, s = s, s.replace('()', '').replace('[]', '').replace('{}', '')
    return s == ''


def _balanced_parens(s):
    depth = 0
    for ch in s:
        depth += 1 if ch == '(' else -1
        if depth < 0:
            return False
    return depth == 0


def _trunc(a, b):
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q


def _random_tree(rng, depth):
    """A random expression tree: an int, or (op, left, right)."""
    if depth == 0 or rng.random() < 0.3:
        return rng.randint(-9, 9)
    return (rng.choice('+-*/'), _random_tree(rng, depth - 1), _random_tree(rng, depth - 1))


def _value(t):
    if isinstance(t, int):
        return t
    op, a, b = t[0], _value(t[1]), _value(t[2])
    if op == '/':
        if b == 0:
            raise ZeroDivisionError
        return _trunc(a, b)
    return a + b if op == '+' else a - b if op == '-' else a * b


def _postfix(t):
    return [str(t)] if isinstance(t, int) else _postfix(t[1]) + _postfix(t[2]) + [t[0]]


def _random_infix(rng, depth):
    if depth == 0 or rng.random() < 0.3:
        return str(rng.randint(0, 20))
    left, right = _random_infix(rng, depth - 1), _random_infix(rng, depth - 1)
    text = f"{left} {rng.choice('+-*')} {right}"
    return f"({text})" if rng.random() < 0.5 else text


def test_is_balanced():
    for s, want in [('', True), ('()', True), ('([]{})', True), ('{[()()]}', True),
                    ('([)]', False), ('(', False), (')', False), ('(()', False), ('][', False)]:
        assert is_balanced(s) is want, s
    rng = random.Random(18)
    for _ in range(500):
        s = ''.join(rng.choice('()[]{}') for _ in range(rng.randint(0, 8)))
        assert is_balanced(s) == _bf_balanced(s), s


def test_longest_balanced():
    for s, want in [(')()())', 4), ('(()', 2), ('', 0), ('()(()', 2), ('()(())', 6), ('))((', 0)]:
        assert longest_balanced(s) == want, s
    rng = random.Random(18)
    for _ in range(400):
        s = ''.join(rng.choice('()') for _ in range(rng.randint(0, 12)))
        want = max((j - i for i in range(len(s)) for j in range(i, len(s) + 1) if _balanced_parens(s[i:j])), default=0)
        assert longest_balanced(s) == want, s


def test_eval_postfix():
    assert eval_postfix(['2', '1', '+', '3', '*']) == 9
    assert eval_postfix(['4', '13', '5', '/', '+']) == 6
    assert eval_postfix(['5', '3', '-']) == 2, "the second pop is the LEFT operand"
    assert eval_postfix(['7', '-2', '/']) == -3, "division truncates toward zero (7 // -2 is -4)"
    assert eval_postfix(['-7', '2', '/']) == -3, "division truncates toward zero"
    assert eval_postfix(['-3']) == -3, "'-3' is a number, not an operator"
    rng = random.Random(18)
    done = 0
    while done < 300:
        t = _random_tree(rng, 4)
        try:
            want = _value(t)
        except ZeroDivisionError:
            continue
        assert eval_postfix(_postfix(t)) == want, _postfix(t)
        done += 1


def test_eval_infix():
    for expr, want in [('1 + 2', 3), ('2 * (3 + 4) - 5', 9), ('42', 42), ('((2))', 2),
                       ('100 / (2 * (3 + 2))', 10), (' 3+5 / 2 ', 5)]:
        assert eval_infix(expr) == want, expr
    assert eval_infix('14 / 3 * 2') == 8, "equal precedence goes left to right: (14 / 3) * 2"
    assert eval_infix('2 - 3 - 4') == -5, "minus is left-associative: (2 - 3) - 4"
    assert eval_infix('7 - 10 / 3') == 4
    assert eval_infix('(1 - 8) / 2') == -3, "division truncates toward zero"
    rng = random.Random(18)
    for _ in range(300):
        expr = _random_infix(rng, 4)
        assert eval_infix(expr) == eval(expr), expr


def test_queue_from_stacks():
    q = QueueFromStacks()
    assert len(q) == 0
    for method in (q.pop, q.peek):
        try:
            method()
        except IndexError:
            pass
        else:
            raise AssertionError("pop()/peek() on an empty queue should raise IndexError")
    assert not any(isinstance(v, deque) for v in vars(q).values()), "build it from two lists, not a deque"
    rng = random.Random(18)
    model = deque()
    for step in range(1000):
        if model and rng.random() < 0.45:
            if rng.random() < 0.5:
                assert q.peek() == model[0]
            else:
                assert q.pop() == model.popleft()
        else:
            q.push(step)
            model.append(step)
        assert len(q) == len(model)


def test_stack_from_queue():
    s = StackFromQueue()
    assert len(s) == 0
    for method in (s.pop, s.top):
        try:
            method()
        except IndexError:
            pass
        else:
            raise AssertionError("pop()/top() on an empty stack should raise IndexError")
    assert not any(isinstance(v, list) for v in vars(s).values()), "build it from one deque, not a list"
    rng = random.Random(18)
    model = []
    for step in range(600):
        if model and rng.random() < 0.45:
            if rng.random() < 0.5:
                assert s.top() == model[-1]
            else:
                assert s.pop() == model.pop()
        else:
            s.push(step)
            model.append(step)
        assert len(s) == len(model)


def test_next_greater():
    assert next_greater([]) == []
    assert next_greater([2, 1, 2, 4, 3]) == [4, 2, 4, -1, -1]
    rng = random.Random(18)
    for _ in range(300):
        nums = [rng.randint(0, 6) for _ in range(rng.randint(0, 10))]
        want = [next((y for y in nums[i + 1:] if y > x), -1) for i, x in enumerate(nums)]
        assert next_greater(nums) == want, nums


def test_prev_smaller_index():
    assert prev_smaller_index([]) == []
    assert prev_smaller_index([3, 1, 4, 1, 5]) == [-1, -1, 1, -1, 3], "strictly smaller: equal values don't count"
    rng = random.Random(18)
    for _ in range(300):
        nums = [rng.randint(0, 6) for _ in range(rng.randint(0, 10))]
        want = [next((j for j in range(i - 1, -1, -1) if nums[j] < nums[i]), -1) for i in range(len(nums))]
        assert prev_smaller_index(nums) == want, nums


def test_wait_for_greater():
    assert wait_for_greater([3, 1, 2, 5]) == [3, 1, 1, 0]
    assert wait_for_greater([5, 5, 5]) == [0, 0, 0], "strictly greater"
    rng = random.Random(18)
    for _ in range(300):
        nums = [rng.randint(0, 6) for _ in range(rng.randint(0, 10))]
        want = [next((j - i for j in range(i + 1, len(nums)) if nums[j] > nums[i]), 0) for i in range(len(nums))]
        assert wait_for_greater(nums) == want, nums


def test_next_greater_circular():
    assert next_greater_circular([]) == []
    assert next_greater_circular([1, 2, 1]) == [2, -1, 2]
    rng = random.Random(18)
    for _ in range(300):
        nums = [rng.randint(0, 6) for _ in range(rng.randint(0, 10))]
        n = len(nums)
        want = [next((nums[(i + d) % n] for d in range(1, n) if nums[(i + d) % n] > nums[i]), -1) for i in range(n)]
        assert next_greater_circular(nums) == want, nums


def test_largest_rectangle():
    assert largest_rectangle([]) == 0
    assert largest_rectangle([2, 1, 5, 6, 2, 3]) == 10
    assert largest_rectangle([2, 4]) == 4
    assert largest_rectangle([3, 3, 3]) == 9, "equal heights extend the same rectangle"
    rng = random.Random(18)
    for _ in range(300):
        hs = [rng.randint(0, 6) for _ in range(rng.randint(0, 10))]
        want = max((min(hs[i:j + 1]) * (j - i + 1) for i in range(len(hs)) for j in range(i, len(hs))), default=0)
        assert largest_rectangle(hs) == want, hs


def test_trapped_water():
    assert trapped_water([]) == 0
    assert trapped_water([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
    assert trapped_water([4, 2, 0, 3, 2, 5]) == 9
    rng = random.Random(18)
    for _ in range(300):
        hs = [rng.randint(0, 6) for _ in range(rng.randint(0, 10))]
        want = sum(max(0, min(max(hs[:i + 1]), max(hs[i:])) - h) for i, h in enumerate(hs))
        assert trapped_water(hs) == want, hs


def test_window_max():
    assert window_max([1, 3, -1, -3, 5, 3], 3) == [3, 3, 5, 5]
    assert window_max([4], 1) == [4]
    rng = random.Random(18)
    for _ in range(300):
        nums = [rng.randint(-5, 5) for _ in range(rng.randint(1, 10))]
        k = rng.randint(1, len(nums))
        assert window_max(nums, k) == [max(nums[i:i + k]) for i in range(len(nums) - k + 1)], (nums, k)


def _bf_dfs(graph, start):
    seen, order = set(), []

    def visit(u):
        seen.add(u)
        order.append(u)
        for v in graph.get(u, []):
            if v not in seen:
                visit(v)

    visit(start)
    return order


def test_dfs_order():
    assert dfs_order({}, 7) == [7]
    assert dfs_order({1: [2, 3], 2: [4], 3: [], 4: []}, 1) == [1, 2, 4, 3]
    assert dfs_order({1: [2, 3], 2: [3, 4]}, 1) == [1, 2, 3, 4], "mark nodes when you pop them, not when you push them"
    rng = random.Random(18)
    for _ in range(300):
        nodes = range(8)
        graph = {u: [rng.choice(nodes) for _ in range(rng.randint(0, 3))] for u in nodes if rng.random() < 0.8}
        start = rng.choice(nodes)
        assert dfs_order(graph, start) == _bf_dfs(graph, start), (graph, start)
    chain = {i: [i + 1] for i in range(5000)}
    try:
        got = dfs_order(chain, 0)
    except RecursionError:
        raise AssertionError("a 5000-node chain is too deep for recursion: use an explicit stack")
    assert got == list(range(5001))
