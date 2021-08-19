"""R11 - Pythonic idioms and assignment order (reference solutions)

Compare after you've made your own attempt. Run: python check.py 11 -s
"""

PREDICT = r"""
>>> nums = [1, 0]
>>> i = 0
>>> nums[i], nums[nums[i]] = nums[nums[i]], nums[i]
>>> nums
[1, 0]

>>> nums = [1, 0]
>>> i = 0
>>> nums[nums[i]], nums[i] = nums[i], nums[nums[i]]
>>> nums
[0, 1]

>>> x = [0, 0, 0]
>>> i = 0
>>> i, x[i] = 2, 9
>>> x
[0, 0, 9]

>>> x = [0, 0, 0]
>>> i = x[i] = 2
>>> i, x
(2, [0, 0, 2])

>>> first, *mid, last = [1, 2, 3, 4, 5]
>>> first, mid, last
(1, [2, 3, 4], 5)
>>> first, *mid, last = (1, 2)
>>> mid
[]
>>> head, *rest = 'abc'
>>> rest
['b', 'c']
>>> print(*rest, sep='-')
b-c

>>> a, b = [1, 2, 3]
ValueError
>>> a, *b, c = [1]
ValueError

>>> pairs = [('a', 1), ('b', 2)]
>>> [f'{i}:{k}={v}' for i, (k, v) in enumerate(pairs, 1)]
['1:a=1', '2:b=2']

>>> [(r, c) for r in range(2) for c in range(3) if c != r]
[(0, 1), (0, 2), (1, 0), (1, 2)]
>>> [[r * c for c in range(3)] for r in range(2)]
[[0, 0, 0], [0, 1, 2]]

>>> [x for x in range(6) if x % 2]
[1, 3, 5]
>>> [x if x % 2 else -x for x in range(6)]
[0, 1, -2, 3, -4, 5]
>>> [x for x in range(6) if x % 2 else -x]
SyntaxError

>>> {len(w): w for w in ['hi', 'yo', 'hey']}
{2: 'yo', 3: 'hey'}
>>> {v: k for k, v in {'a': 1, 'b': 2, 'c': 1}.items()}
{1: 'c', 2: 'b'}

>>> list(zip(*[[1, 2, 3], [4, 5, 6]]))
[(1, 4), (2, 5), (3, 6)]
>>> nums, letters = zip(*[(1, 'a'), (2, 'b')])
>>> nums, letters
((1, 2), ('a', 'b'))
>>> list(zip([1, 2], 'abc', strict=True))
ValueError

>>> words = ['pear', 'fig', 'banana', 'kiwi']
>>> min(words, key=len), max(words, key=len)
('fig', 'banana')
>>> max(['ab', 'cd'], key=len)
'ab'
>>> max([], default=None) is None
True
>>> min([])
ValueError

>>> nums = [30, 10, 20, 10]
>>> min(range(len(nums)), key=nums.__getitem__)
1
>>> max(enumerate(nums), key=lambda p: p[1])
(0, 30)

>>> for n in [4, 6, 9]:
...     if n % 2:
...         print('odd', n)
...         break
... else:
...     print('no odd')
odd 9
>>> for n in []:
...     break
... else:
...     print('ran')
ran

>>> it = iter([3, 1, 0, 4])
>>> out = []
>>> while (x := next(it, None)) is not None and x:
...     out.append(x)
>>> out
[3, 1]
>>> [y for x in range(6) if (y := x * x) % 2]
[1, 9, 25]

>>> r, R = 3, 3
>>> 0 <= r < R
False
>>> 1 < 2 > 0, 1 < 2 < 1, 3 == 3 == 3.0
(True, False, True)
>>> x = 5
>>> x == 1 or 2
2
>>> x in (1, 2)
False

>>> xs = [3, 1, 3, 2, 1]
>>> sorted(set(xs))
[1, 2, 3]
>>> list(dict.fromkeys(xs))
[3, 1, 2]

>>> x = 0
>>> 'zero' if x == 0 else 'pos' if x > 0 else 'neg'
'zero'
>>> 1 + 2 if False else 10
10

>>> class N:
...     def __init__(self, v, nxt=None):
...         self.v, self.next = v, nxt
>>> prev, curr = None, N(1, N(2, N(3)))
>>> while curr:
...     prev, curr.next, curr = curr, prev, curr.next
>>> [prev.v, prev.next.v, prev.next.next.v]
[3, 2, 1]
>>> prev, curr = None, N(1, N(2))
>>> while curr:
...     curr, curr.next, prev = curr.next, prev, curr
AttributeError
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def squares_of_odds(nums):
    return [x * x for x in nums if x % 2]


def flatten_grid(grid):
    return [x for row in grid for x in row]


def argmax(nums):
    return max(range(len(nums)), key=nums.__getitem__, default=-1)


def invert(d):
    return {v: k for k, v in d.items()}


def count_matches(a, b):
    return sum(x == y for x, y in zip(a, b))


def transpose(matrix):
    return [list(col) for col in zip(*matrix)]


def dedupe(items):
    return list(dict.fromkeys(items))


def swap_home(nums, i):
    # nums[nums[i]] must be assigned first, while nums[i] still holds the old value
    nums[nums[i]], nums[i] = nums[i], nums[nums[i]]


def cyclic_sort(nums):
    for i in range(len(nums)):
        while nums[i] != i:
            swap_home(nums, i)


def reverse_list(head):
    prev, curr = None, head
    while curr:
        prev, curr.next, curr = curr, prev, curr.next
    return prev


def parse_ints(tokens):
    out = []
    for t in tokens:
        try:
            out.append(int(t))
        except ValueError:
            pass
    return out


def take_until(iterable, stop):
    it, done, out = iter(iterable), object(), []
    while (x := next(it, done)) is not done and x != stop:
        out.append(x)
    return out


def pairwise_sums(a, b):
    return [x + y for x, y in zip(a, b, strict=True)]
