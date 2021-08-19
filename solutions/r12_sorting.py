"""R12 - Sorting (reference solutions)

Compare after you've made your own attempt. Run: python check.py 12 -s
"""
import operator
import random
from collections import Counter
from functools import cmp_to_key

PREDICT = r"""
>>> nums = [3, 1, 2]
>>> print(nums.sort())
None
>>> nums
[1, 2, 3]
>>> sorted('bca')
['a', 'b', 'c']
>>> ''.join(sorted('bca'))
'abc'

>>> d = {'b': 1, 'a': 3, 'c': 2}
>>> sorted(d)
['a', 'b', 'c']
>>> sorted(d, key=d.get)
['b', 'c', 'a']
>>> sorted(d.items(), key=lambda kv: kv[1], reverse=True)
[('a', 3), ('c', 2), ('b', 1)]

>>> sorted(['b', 'A', 'a', 'B'])
['A', 'B', 'a', 'b']
>>> sorted(['b', 'A', 'a', 'B'], key=str.lower)
['A', 'a', 'b', 'B']

>>> sorted(['10', '9', '100'])
['10', '100', '9']
>>> sorted(['10', '9', '100'], key=int)
['9', '10', '100']

>>> words = ['bb', 'a', 'ccc', 'aa']
>>> sorted(words, key=lambda w: (-len(w), w))
['ccc', 'aa', 'bb', 'a']
>>> sorted(['a', 'b'], key=lambda s: -s)
TypeError

>>> pairs = [('x', 2), ('y', 1), ('z', 2)]
>>> sorted(pairs, key=lambda p: p[1], reverse=True)
[('x', 2), ('z', 2), ('y', 1)]

>>> people = [('bo', 30), ('al', 25), ('bo', 20), ('al', 35)]
>>> by_age = sorted(people, key=lambda p: p[1])
>>> sorted(by_age, key=lambda p: p[0], reverse=True)
[('bo', 20), ('bo', 30), ('al', 25), ('al', 35)]

>>> sorted([-3, 2, -1, 3], key=abs)
[-1, 2, -3, 3]

>>> sorted([3, 'a', 1])
TypeError
>>> sorted([3, 1.5, True])
[True, 1.5, 3]

>>> sorted([(2, 'b'), (1, 'z'), (2, 'a')])
[(1, 'z'), (2, 'a'), (2, 'b')]
>>> sorted([[1, 2], [1], [0, 9]])
[[0, 9], [1], [1, 2]]

>>> nums = [30, 10, 20]
>>> order = sorted(range(len(nums)), key=nums.__getitem__)
>>> order, [nums[i] for i in order]
([1, 2, 0], [10, 20, 30])

>>> def by_len_desc(a, b):
...     return len(b) - len(a)
>>> sorted(['a', 'ccc', 'bb'], key=cmp_to_key(by_len_desc))
['ccc', 'bb', 'a']

>>> class P:
...     def __init__(self, x):
...         self.x = x
>>> sorted([P(2), P(1)])
TypeError
>>> [p.x for p in sorted([P(2), P(1)], key=operator.attrgetter('x'))]
[1, 2]

>>> class Q:
...     def __init__(self, x):
...         self.x = x
...     def __lt__(self, other):
...         return self.x < other.x
>>> [q.x for q in sorted([Q(3), Q(1), Q(2)])]
[1, 2, 3]
>>> Q(1) > Q(0)
True
>>> Q(1) <= Q(2)
TypeError

>>> @dataclass(order=True)
... class Card:
...     rank: int
...     suit: str
>>> sorted([Card(2, 'h'), Card(1, 's'), Card(2, 'c')])
[Card(rank=1, suit='s'), Card(rank=2, suit='c'), Card(rank=2, suit='h')]

>>> calls = []
>>> def key(x):
...     calls.append(x)
...     return -x
>>> sorted([3, 1, 2], key=key)
[3, 2, 1]
>>> len(calls)
3
"""


def by_length_then_alpha(words):
    return sorted(words, key=lambda w: (len(w), w))


def by_freq_desc(words):
    counts = Counter(words)
    return sorted(counts, key=lambda w: (-counts[w], w))


def sort_people(people):
    by_age = sorted(people, key=operator.itemgetter(1))
    return sorted(by_age, key=operator.itemgetter(0), reverse=True)   # stable: equal names keep age order


def argsort(nums):
    return sorted(range(len(nums)), key=nums.__getitem__)


def sort_fractions(pairs):
    def compare(p, q):
        left, right = p[0] * q[1], q[0] * p[1]    # exact, and safe because denominators are positive
        return (left > right) - (left < right)

    return sorted(pairs, key=cmp_to_key(compare))


class Version:
    def __init__(self, text):
        self.text = text
        parts = [int(p) for p in text.split('.')]
        while parts and parts[-1] == 0:     # '1.0.0' and '1' compare equal
            parts.pop()
        self.parts = tuple(parts)

    def __eq__(self, other):
        return self.parts == other.parts

    def __lt__(self, other):
        return self.parts < other.parts

    def __repr__(self):
        return f"Version({self.text!r})"


def insertion_sort(nums):
    for i in range(1, len(nums)):
        x, j = nums[i], i - 1
        while j >= 0 and x < nums[j]:       # strict <: equal items never jump each other
            nums[j + 1] = nums[j]
            j -= 1
        nums[j + 1] = x


def _merge(left, right):
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if right[j] < left[i]:              # take from the right only when strictly smaller
            out.append(right[j])
            j += 1
        else:
            out.append(left[i])
            i += 1
    return out + left[i:] + right[j:]


def merge_sort(nums):
    if len(nums) <= 1:
        return list(nums)
    mid = len(nums) // 2
    return _merge(merge_sort(nums[:mid]), merge_sort(nums[mid:]))


def count_inversions(nums):
    def sort_count(a):
        if len(a) <= 1:
            return a, 0
        mid = len(a) // 2
        left, x = sort_count(a[:mid])
        right, y = sort_count(a[mid:])
        merged, i, j, count = [], 0, 0, x + y
        while i < len(left) and j < len(right):
            if right[j] < left[i]:
                merged.append(right[j])
                j += 1
                count += len(left) - i      # right[j] jumps ahead of everything left in `left`
            else:
                merged.append(left[i])
                i += 1
        return merged + left[i:] + right[j:], count

    return sort_count(list(nums))[1]


def quicksort(nums):
    def sort(lo, hi):                       # sorts nums[lo..hi], inclusive
        while lo < hi:
            pivot = nums[random.randint(lo, hi)]
            lt, i, gt = lo, lo, hi          # [lo, lt) < pivot, [lt, i) == pivot, (gt, hi] > pivot
            while i <= gt:
                if nums[i] < pivot:
                    nums[lt], nums[i] = nums[i], nums[lt]
                    lt += 1
                    i += 1
                elif pivot < nums[i]:
                    nums[gt], nums[i] = nums[i], nums[gt]
                    gt -= 1
                else:
                    i += 1
            # recurse into the smaller side and loop on the larger: O(log n) stack
            if lt - lo < hi - gt:
                sort(lo, lt - 1)
                lo = gt + 1
            else:
                sort(gt + 1, hi)
                hi = lt - 1

    sort(0, len(nums) - 1)


def kth_smallest(nums, k):
    items = list(nums)
    while True:
        pivot = random.choice(items)
        smaller = [x for x in items if x < pivot]
        if k <= len(smaller):
            items = smaller
            continue
        equal = sum(1 for x in items if x == pivot)
        if k <= len(smaller) + equal:
            return pivot
        k -= len(smaller) + equal
        items = [x for x in items if pivot < x]


def counting_sort(nums):
    if not nums:
        return []
    lo = min(nums)
    counts = [0] * (max(nums) - lo + 1)
    for x in nums:
        counts[x - lo] += 1
    out = []
    for offset, c in enumerate(counts):
        out.extend([lo + offset] * c)
    return out


def sort_by_frequency(nums):
    buckets = [[] for _ in range(len(nums) + 1)]
    for value, c in Counter(nums).items():
        buckets[c].append(value)
    out = []
    for c in range(len(nums), 0, -1):
        for value in sorted(buckets[c]):
            out.extend([value] * c)
    return out
