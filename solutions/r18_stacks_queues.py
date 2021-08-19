"""R18 - Stacks, queues, monotonic structures (reference solutions)

Compare after you've made your own attempt. Run: python check.py 18 -s
"""
import operator
import re
from collections import deque

PREDICT = r"""
>>> st = []
>>> st.append(1); st.append(2); st.append(3)
>>> st.pop(), st[-1], st
(3, 2, [1, 2])

>>> [].pop()
IndexError
>>> deque().popleft()
IndexError

>>> st = []
>>> st and st[-1]
[]
>>> st = [5]
>>> st and st[-1]
5

>>> d = deque([1, 2, 3])
>>> d[1], d[-1]
(2, 3)
>>> d[0:2]
TypeError

>>> d = deque([1, 2, 3, 4])
>>> d.rotate(1)
>>> d
deque([4, 1, 2, 3])
>>> d.rotate(-2)
>>> d
deque([2, 3, 4, 1])

>>> d = deque(maxlen=3)
>>> for x in range(5):
...     d.append(x)
>>> d
deque([2, 3, 4], maxlen=3)
>>> d.appendleft(9)
>>> d
deque([9, 2, 3], maxlen=3)

>>> inbox, outbox = [], []
>>> for x in (1, 2, 3):
...     inbox.append(x)
>>> if not outbox:
...     while inbox:
...         outbox.append(inbox.pop())
>>> outbox.pop(), outbox, inbox
(1, [3, 2], [])

>>> pairs = {')': '(', ']': '[', '}': '{'}
>>> st = []
>>> for ch in '([)]':
...     if ch in pairs:
...         if not st or st.pop() != pairs[ch]:
...             print('bad at', ch)
...             break
...     else:
...         st.append(ch)
bad at )

>>> st = [10, 3]
>>> st.pop() - st.pop()
-7

>>> st = []
>>> for tok in '3 4 + 2 *'.split():
...     if tok in ('+', '-', '*'):
...         b, a = st.pop(), st.pop()
...         st.append(a + b if tok == '+' else a - b if tok == '-' else a * b)
...     else:
...         st.append(int(tok))
>>> st
[14]

>>> -7 // 2, int(-7 / 2), -(7 // 2)
(-4, -3, -3)

>>> nums = [2, 1, 2, 4, 3]
>>> ans, st = [-1] * len(nums), []
>>> for i, x in enumerate(nums):
...     while st and nums[st[-1]] < x:
...         ans[st.pop()] = x
...     st.append(i)
>>> ans, st
([4, 2, 4, -1, -1], [3, 4])

>>> nums = [2, 2, 1]
>>> st, popped = [], []
>>> for i, x in enumerate(nums):
...     while st and nums[st[-1]] <= x:
...         popped.append(st.pop())
...     st.append(i)
>>> st, popped
([1, 2], [0])

>>> heights = [2, 1, 2]
>>> st, best = [], 0
>>> for i, h in enumerate(heights + [0]):
...     while st and heights[st[-1]] >= h:
...         top = st.pop()
...         left = st[-1] if st else -1
...         best = max(best, heights[top] * (i - left - 1))
...     st.append(i)
>>> best
3

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
[3, 3, 5, 5]

>>> graph = {1: [2, 3], 2: [4], 3: [], 4: []}
>>> def order(push):
...     st, out = [1], []
...     while st:
...         node = st.pop()
...         out.append(node)
...         st.extend(push(graph[node]))
...     return out
>>> order(list), order(reversed)
([1, 3, 2, 4], [1, 2, 4, 3])
"""


def is_balanced(s):
    pairs = {')': '(', ']': '[', '}': '{'}
    st = []
    for ch in s:
        if ch in pairs:
            if not st or st.pop() != pairs[ch]:
                return False
        else:
            st.append(ch)
    return not st


def longest_balanced(s):
    st, best = [-1], 0          # bottom of the stack: the index just before the current run
    for i, ch in enumerate(s):
        if ch == '(':
            st.append(i)
        else:
            st.pop()
            if st:
                best = max(best, i - st[-1])
            else:
                st.append(i)    # an unmatched ')' becomes the new floor
    return best


def _trunc_div(a, b):
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q


_OPS = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': _trunc_div}


def eval_postfix(tokens):
    st = []
    for tok in tokens:
        if tok in _OPS:
            b, a = st.pop(), st.pop()
            st.append(_OPS[tok](a, b))
        else:
            st.append(int(tok))
    return st[-1]


def eval_infix(expr):
    prec = {'+': 1, '-': 1, '*': 2, '/': 2}
    nums, ops = [], []

    def apply():
        b, a = nums.pop(), nums.pop()
        nums.append(_OPS[ops.pop()](a, b))

    for tok in re.findall(r"\d+|[-+*/()]", expr):
        if tok.isdigit():
            nums.append(int(tok))
        elif tok == '(':
            ops.append(tok)
        elif tok == ')':
            while ops[-1] != '(':
                apply()
            ops.pop()
        else:
            # >= (not >) makes operators of equal precedence left-associative
            while ops and ops[-1] != '(' and prec[ops[-1]] >= prec[tok]:
                apply()
            ops.append(tok)
    while ops:
        apply()
    return nums[-1]


class QueueFromStacks:
    def __init__(self):
        self.inbox, self.outbox = [], []

    def push(self, x):
        self.inbox.append(x)

    def _ready(self):
        if not self.outbox:          # refill only when empty: each item moves once
            while self.inbox:
                self.outbox.append(self.inbox.pop())
        if not self.outbox:
            raise IndexError("empty queue")

    def pop(self):
        self._ready()
        return self.outbox.pop()

    def peek(self):
        self._ready()
        return self.outbox[-1]

    def __len__(self):
        return len(self.inbox) + len(self.outbox)


class StackFromQueue:
    def __init__(self):
        self.q = deque()

    def push(self, x):
        self.q.append(x)
        for _ in range(len(self.q) - 1):     # rotate so the newest item sits at the front
            self.q.append(self.q.popleft())

    def pop(self):
        if not self.q:
            raise IndexError("empty stack")
        return self.q.popleft()

    def top(self):
        if not self.q:
            raise IndexError("empty stack")
        return self.q[0]

    def __len__(self):
        return len(self.q)


def next_greater(nums):
    ans, st = [-1] * len(nums), []
    for i, x in enumerate(nums):
        while st and nums[st[-1]] < x:
            ans[st.pop()] = x
        st.append(i)
    return ans


def prev_smaller_index(nums):
    ans, st = [], []                 # st: indices whose values strictly increase
    for i, x in enumerate(nums):
        while st and nums[st[-1]] >= x:
            st.pop()
        ans.append(st[-1] if st else -1)
        st.append(i)
    return ans


def wait_for_greater(nums):
    ans, st = [0] * len(nums), []
    for i, x in enumerate(nums):
        while st and nums[st[-1]] < x:
            j = st.pop()
            ans[j] = i - j
        st.append(i)
    return ans


def next_greater_circular(nums):
    n = len(nums)
    ans, st = [-1] * n, []
    for i in range(2 * n):
        x = nums[i % n]
        while st and nums[st[-1]] < x:
            ans[st.pop()] = x
        if i < n:
            st.append(i)
    return ans


def largest_rectangle(heights):
    st, best = [], 0
    for i, h in enumerate(heights + [0]):        # the 0 sentinel flushes the stack
        while st and heights[st[-1]] >= h:
            top = st.pop()
            left = st[-1] if st else -1
            best = max(best, heights[top] * (i - left - 1))
        st.append(i)
    return best


def trapped_water(heights):
    st, water = [], 0
    for i, h in enumerate(heights):
        while st and heights[st[-1]] < h:
            bottom = st.pop()
            if not st:
                break
            left = st[-1]
            water += (min(heights[left], h) - heights[bottom]) * (i - left - 1)
        st.append(i)
    return water


def window_max(nums, k):
    dq, out = deque(), []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out


def dfs_order(graph, start):
    seen, order, st = set(), [], [start]
    while st:
        node = st.pop()
        if node in seen:             # marking on pop (not push) reproduces the recursive order
            continue
        seen.add(node)
        order.append(node)
        st.extend(reversed(graph.get(node, [])))
    return order
