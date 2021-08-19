"""R07 - dict, set, Counter, defaultdict, OrderedDict

Dicts keep insertion order (3.7+); sets don't. d[k] raises KeyError where
d.get(k, default) doesn't; d.setdefault(k, []).append(v) groups; d.popitem()
removes the LAST item. defaultdict inserts a key just because you read it, while
Counter[missing] returns 0 without inserting, and a count decremented to 0 stays
in the Counter. Counter arithmetic (+ - & |) drops counts <= 0, subtract() keeps
them, most_common() breaks ties by first appearance, total() is 3.10+. Keys must
be hashable: lists become tuples, sets become frozensets. {} is a dict, not a set.

Part 1 - Predict. Each block in PREDICT is a REPL session. Replace every ???
with exactly what Python prints: expression values are echoed the way the REPL
echoes them, and a line that raises prints just the exception name (TypeError).

Part 2 - Drills. Implement every function until `python check.py 7` is green.
Don't edit the tests at the bottom; add your own test_* functions if you like.

Unlocks: the hashing family (pair-sum lookups, grouping anagrams, one-to-one
mappings, longest consecutive run), frequency windows, and LRU caches.
"""
from collections import Counter, OrderedDict, defaultdict

PREDICT = r"""
>>> d = {}
>>> d['x']
???
>>> d.get('x'), d.get('x', 0)
???

>>> d = {}
>>> d['x'] += 1
???
>>> c = Counter()
>>> c['x'] += 1
>>> c
???

>>> d = defaultdict(list)
>>> if d['x']:
...     pass
>>> dict(d)
???

>>> c = Counter('aab')
>>> c['z'], 'z' in c
???

>>> c = Counter('a')
>>> c['a'] -= 1
>>> c, len(c)
???

>>> Counter('aab') - Counter('abb')
???
>>> Counter('aab') & Counter('abb')
???
>>> Counter('aab') | Counter('abb')
???

>>> c = Counter('aab')
>>> c.subtract('abbb')
>>> c
???
>>> +c
???

>>> Counter('bbaa').most_common()
???
>>> Counter('abcabcd').most_common(2)
???

>>> Counter(a=1, b=0) == Counter(a=1)
???

>>> type({}), type(set()), type({1})
???

>>> d = dict.fromkeys('ab', [])
>>> d['a'].append(1)
>>> d
???

>>> d = {'a': 1, 'b': 2, 'c': 3}
>>> d.popitem()
???
>>> d
???

>>> d = {'b': 1, 'a': 2}
>>> list(d), sorted(d), max(d, key=d.get)
???

>>> a = {'x': 1, 'y': 2}
>>> b = {'y': 3, 'z': 4}
>>> sorted(a.keys() & b.keys()), sorted(a.keys() - b.keys())
???
>>> a | b
???
>>> {**b, **a}
???

>>> {[1, 2]: 'x'}
???
>>> {(1, 2): 'x'}[(1, 2)]
???

>>> s = {1, 2}
>>> s.remove(3)
???
>>> s.discard(3)
>>> len(s)
???

>>> od = OrderedDict.fromkeys('abc')
>>> od.move_to_end('a')
>>> od.popitem(last=False)
???
>>> list(od)
???

>>> d = {}
>>> d.setdefault('k', []).append(1)
>>> d.setdefault('k', []).append(2)
>>> d
???

>>> sorted({3, 1, 2} | {5}), sorted({1, 2, 3} - {2}), {1, 2} <= {1, 2, 3}
???

>>> d = {1: 1}
>>> for k in d:
...     d[k + 1] = 1
???
>>> len(d)
???
"""


# ---------------------------------------------------------------- drills

def freq(items):
    """Count how often each item appears using a plain dict and .get (no
    Counter, no defaultdict). freq('abca') == {'a': 2, 'b': 1, 'c': 1}"""
    raise NotImplementedError


def pair_with_sum(nums, target):
    """In one pass with a value -> index dict, return (i, j), i < j, with
    nums[i] + nums[j] == target: the pair with the smallest j, and for that j
    the smallest i. None if there's none. pair_with_sum([3, 2, 4], 6) == (1, 2)"""
    raise NotImplementedError


def group_by_signature(words):
    """Group words that are anagrams of each other. Groups come in order of
    their first word; inside a group, input order.
    group_by_signature(['eat', 'tea', 'tan', 'ate']) == [['eat', 'tea', 'ate'], ['tan']]"""
    raise NotImplementedError


def has_duplicate_within(nums, k):
    """Return True if two equal values sit at most k positions apart, else
    False, in O(n) with a value -> last index dict.
    has_duplicate_within([1, 2, 3, 1], 3) is True"""
    raise NotImplementedError


def first_unique(items):
    """Return the first item that appears exactly once, or None. Count first,
    then make a second pass. first_unique('swiss') == 'w'"""
    raise NotImplementedError


def is_bijection(pattern, words):
    """Return True if letters of pattern and words pair up one-to-one (same
    letter <-> same word, in both directions), else False.
    is_bijection('abba', ['dog', 'cat', 'cat', 'dog']) is True"""
    raise NotImplementedError


def longest_run(nums):
    """Length of the longest run of consecutive integers v, v + 1, ... that all
    appear in nums (in any order), in O(n) with a set: only start counting at a
    value whose predecessor is missing. longest_run([100, 4, 200, 1, 3, 2]) == 4"""
    raise NotImplementedError


def invert(d):
    """Map each value of d to the list of keys that had it, keys in d's order.
    invert({'a': 1, 'b': 2, 'c': 1}) == {1: ['a', 'c'], 2: ['b']}"""
    raise NotImplementedError


def common_elements(a, b):
    """Multiset intersection as a sorted list: every value appears
    min(count in a, count in b) times.
    common_elements([1, 2, 2, 3], [2, 2, 2, 4]) == [2, 2]"""
    raise NotImplementedError


def can_build(note, letters):
    """Return True if note can be spelled using each character of letters at
    most once, else False. can_build('aab', 'baa') is True"""
    raise NotImplementedError


def top_k_frequent(items, k):
    """The k most common items, most common first; ties go to whichever was
    seen first. top_k_frequent('aabbbc', 2) == ['b', 'a']"""
    raise NotImplementedError


def word_counts_sorted(text):
    """Lowercase the whitespace-separated words of text and return (word, count)
    pairs sorted by count (highest first), then alphabetically.
    word_counts_sorted('b a B c a') == [('a', 2), ('b', 2), ('c', 1)]"""
    raise NotImplementedError


def recent_unique(events, k):
    """The k most recently seen distinct events, most recent first, holding at
    most k entries at any time (OrderedDict: move_to_end, popitem(last=False)).
    recent_unique('abcab', 2) == ['b', 'a']"""
    raise NotImplementedError


# ---------------------------------------------------------------- tests (don't edit)
import random as _random


def _brute_pair(nums, target):
    for j in range(len(nums)):
        for i in range(j):
            if nums[i] + nums[j] == target:
                return (i, j)
    return None


def _brute_run(nums):
    best, run, prev = 0, 0, None
    for v in sorted(set(nums)):
        run = run + 1 if prev is not None and v == prev + 1 else 1
        best, prev = max(best, run), v
    return best


def test_freq():
    assert freq('abca') == {'a': 2, 'b': 1, 'c': 1}
    assert freq([]) == {}
    out = freq([1, 1, 2])
    assert type(out) is dict and out == {1: 2, 2: 1}, "return a plain dict"
    assert list(freq('cab')) == ['c', 'a', 'b'], "keys in first-seen order"


def test_pair_with_sum():
    assert pair_with_sum([3, 2, 4], 6) == (1, 2)
    assert pair_with_sum([3, 3], 6) == (0, 1), "look up before you insert, or 3 pairs with itself"
    assert pair_with_sum([1, 2], 7) is None
    assert pair_with_sum([], 0) is None
    rng = _random.Random(7)
    for _ in range(300):
        nums = [rng.randint(-5, 5) for _ in range(rng.randint(0, 8))]
        t = rng.randint(-6, 6)
        assert pair_with_sum(nums, t) == _brute_pair(nums, t), (nums, t)


def test_group_by_signature():
    assert group_by_signature(['eat', 'tea', 'tan', 'ate', 'nat', 'bat']) == [
        ['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
    assert group_by_signature([]) == []
    assert group_by_signature(['', 'a', '']) == [['', ''], ['a']]
    assert group_by_signature(['ab', 'ba', 'abb']) == [['ab', 'ba'], ['abb']], "same letters, different counts"


def test_has_duplicate_within():
    assert has_duplicate_within([1, 2, 3, 1], 3) is True
    assert has_duplicate_within([1, 2, 3, 1], 2) is False
    assert has_duplicate_within([1, 0, 1, 1], 1) is True, "remember the LAST index of each value"
    assert has_duplicate_within([], 5) is False
    rng = _random.Random(7)
    for _ in range(300):
        nums = [rng.randint(0, 4) for _ in range(rng.randint(0, 9))]
        k = rng.randint(0, 4)
        expected = any(nums[i] == nums[j] for i in range(len(nums))
                       for j in range(i + 1, min(len(nums), i + k + 1)))
        assert has_duplicate_within(nums, k) == expected, (nums, k)


def test_first_unique():
    assert first_unique('swiss') == 'w'
    assert first_unique('aabb') is None
    assert first_unique([]) is None
    assert first_unique([0, 1, 1]) == 0
    assert first_unique([2, 2, 0]) == 0


def test_is_bijection():
    assert is_bijection('abba', ['dog', 'cat', 'cat', 'dog']) is True
    assert is_bijection('abba', ['dog', 'cat', 'cat', 'fish']) is False
    assert is_bijection('abba', ['dog', 'dog', 'dog', 'dog']) is False, "check both directions"
    assert is_bijection('aaaa', ['dog', 'cat', 'cat', 'dog']) is False
    assert is_bijection('ab', ['x']) is False, "lengths must match"
    assert is_bijection('', []) is True


def test_longest_run():
    assert longest_run([100, 4, 200, 1, 3, 2]) == 4
    assert longest_run([]) == 0
    assert longest_run([5, 5, 5]) == 1, "duplicates don't extend a run"
    assert longest_run([-1, 0, 1, 3]) == 3
    rng = _random.Random(7)
    for _ in range(300):
        nums = [rng.randint(-6, 6) for _ in range(rng.randint(0, 10))]
        assert longest_run(nums) == _brute_run(nums), nums


def test_invert():
    assert invert({'a': 1, 'b': 2, 'c': 1}) == {1: ['a', 'c'], 2: ['b']}
    assert invert({}) == {}
    out = invert({'x': 0, 'y': 0})
    assert out == {0: ['x', 'y']} and list(out) == [0]


def test_common_elements():
    assert common_elements([1, 2, 2, 3], [2, 2, 2, 4]) == [2, 2]
    assert common_elements([], [1]) == []
    assert common_elements([3, 1, 3], [3, 3, 1]) == [1, 3, 3]
    rng = _random.Random(7)
    for _ in range(200):
        a = [rng.randint(0, 4) for _ in range(rng.randint(0, 8))]
        b = [rng.randint(0, 4) for _ in range(rng.randint(0, 8))]
        expected = sorted(v for v in set(a) for _ in range(min(a.count(v), b.count(v))))
        assert common_elements(a, b) == expected, (a, b)


def test_can_build():
    assert can_build('aab', 'baa') is True
    assert can_build('aa', 'ab') is False
    assert can_build('', 'xyz') is True
    assert can_build('abc', '') is False
    rng = _random.Random(7)
    for _ in range(200):
        note = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 5)))
        letters = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 7)))
        expected = all(note.count(ch) <= letters.count(ch) for ch in set(note))
        assert can_build(note, letters) == expected, (note, letters)


def test_top_k_frequent():
    assert top_k_frequent('aabbbc', 2) == ['b', 'a']
    assert top_k_frequent('abc', 2) == ['a', 'b'], "ties go to the item seen first"
    assert top_k_frequent([3, 1, 1, 3, 2], 5) == [3, 1, 2]
    assert top_k_frequent([], 3) == []


def test_word_counts_sorted():
    assert word_counts_sorted('b a B c a') == [('a', 2), ('b', 2), ('c', 1)]
    assert word_counts_sorted('') == []
    assert word_counts_sorted('the cat\tthe  Dog\nTHE') == [('the', 3), ('cat', 1), ('dog', 1)]


def test_recent_unique():
    assert recent_unique('abcab', 2) == ['b', 'a']
    assert recent_unique('aaaa', 3) == ['a']
    assert recent_unique('', 2) == []
    rng = _random.Random(7)
    for _ in range(200):
        events = [rng.randint(0, 5) for _ in range(rng.randint(0, 12))]
        k = rng.randint(1, 4)
        expected = list(dict.fromkeys(reversed(events)))[:k]
        assert recent_unique(events, k) == expected, (events, k)
