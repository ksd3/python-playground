"""R07 - dict, set, Counter, defaultdict, OrderedDict (reference solutions)

Compare after you've made your own attempt. Run: python check.py 7 -s
"""
from collections import Counter, OrderedDict, defaultdict

PREDICT = r"""
>>> d = {}
>>> d['x']
KeyError
>>> d.get('x'), d.get('x', 0)
(None, 0)

>>> d = {}
>>> d['x'] += 1
KeyError
>>> c = Counter()
>>> c['x'] += 1
>>> c
Counter({'x': 1})

>>> d = defaultdict(list)
>>> if d['x']:
...     pass
>>> dict(d)
{'x': []}

>>> c = Counter('aab')
>>> c['z'], 'z' in c
(0, False)

>>> c = Counter('a')
>>> c['a'] -= 1
>>> c, len(c)
(Counter({'a': 0}), 1)

>>> Counter('aab') - Counter('abb')
Counter({'a': 1})
>>> Counter('aab') & Counter('abb')
Counter({'a': 1, 'b': 1})
>>> Counter('aab') | Counter('abb')
Counter({'a': 2, 'b': 2})

>>> c = Counter('aab')
>>> c.subtract('abbb')
>>> c
Counter({'a': 1, 'b': -2})
>>> +c
Counter({'a': 1})

>>> Counter('bbaa').most_common()
[('b', 2), ('a', 2)]
>>> Counter('abcabcd').most_common(2)
[('a', 2), ('b', 2)]

>>> Counter(a=1, b=0) == Counter(a=1)
True

>>> type({}), type(set()), type({1})
(<class 'dict'>, <class 'set'>, <class 'set'>)

>>> d = dict.fromkeys('ab', [])
>>> d['a'].append(1)
>>> d
{'a': [1], 'b': [1]}

>>> d = {'a': 1, 'b': 2, 'c': 3}
>>> d.popitem()
('c', 3)
>>> d
{'a': 1, 'b': 2}

>>> d = {'b': 1, 'a': 2}
>>> list(d), sorted(d), max(d, key=d.get)
(['b', 'a'], ['a', 'b'], 'a')

>>> a = {'x': 1, 'y': 2}
>>> b = {'y': 3, 'z': 4}
>>> sorted(a.keys() & b.keys()), sorted(a.keys() - b.keys())
(['y'], ['x'])
>>> a | b
{'x': 1, 'y': 3, 'z': 4}
>>> {**b, **a}
{'y': 2, 'z': 4, 'x': 1}

>>> {[1, 2]: 'x'}
TypeError
>>> {(1, 2): 'x'}[(1, 2)]
'x'

>>> s = {1, 2}
>>> s.remove(3)
KeyError
>>> s.discard(3)
>>> len(s)
2

>>> od = OrderedDict.fromkeys('abc')
>>> od.move_to_end('a')
>>> od.popitem(last=False)
('b', None)
>>> list(od)
['c', 'a']

>>> d = {}
>>> d.setdefault('k', []).append(1)
>>> d.setdefault('k', []).append(2)
>>> d
{'k': [1, 2]}

>>> sorted({3, 1, 2} | {5}), sorted({1, 2, 3} - {2}), {1, 2} <= {1, 2, 3}
([1, 2, 3, 5], [1, 3], True)

>>> d = {1: 1}
>>> for k in d:
...     d[k + 1] = 1
RuntimeError
>>> len(d)
2
"""


def freq(items):
    counts = {}
    for x in items:
        counts[x] = counts.get(x, 0) + 1
    return counts


def pair_with_sum(nums, target):
    first = {}
    for j, x in enumerate(nums):
        if target - x in first:
            return first[target - x], j
        first.setdefault(x, j)  # keep the earliest index of each value
    return None


def group_by_signature(words):
    groups = {}
    for w in words:
        groups.setdefault(''.join(sorted(w)), []).append(w)
    return list(groups.values())


def has_duplicate_within(nums, k):
    last = {}
    for i, x in enumerate(nums):
        if x in last and i - last[x] <= k:
            return True
        last[x] = i
    return False


def first_unique(items):
    counts = Counter(items)
    return next((x for x in items if counts[x] == 1), None)


def is_bijection(pattern, words):
    if len(pattern) != len(words):
        return False
    to_word, to_letter = {}, {}
    for ch, w in zip(pattern, words):
        if to_word.setdefault(ch, w) != w or to_letter.setdefault(w, ch) != ch:
            return False
    return True


def longest_run(nums):
    values = set(nums)
    best = 0
    for v in values:
        if v - 1 not in values:  # v starts a run, so each run is walked once
            end = v
            while end + 1 in values:
                end += 1
            best = max(best, end - v + 1)
    return best


def invert(d):
    out = defaultdict(list)
    for k, v in d.items():
        out[v].append(k)
    return dict(out)


def common_elements(a, b):
    return sorted((Counter(a) & Counter(b)).elements())


def can_build(note, letters):
    return not (Counter(note) - Counter(letters))


def top_k_frequent(items, k):
    return [x for x, _ in Counter(items).most_common(k)]


def word_counts_sorted(text):
    counts = Counter(text.lower().split())
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))


def recent_unique(events, k):
    recent = OrderedDict()
    for e in events:
        recent[e] = None
        recent.move_to_end(e)
        if len(recent) > k:
            recent.popitem(last=False)
    return list(reversed(recent))
