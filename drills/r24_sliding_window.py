"""R24 - Sliding window

A window is a contiguous stretch [left, right] that you update instead of
recomputing. Fixed size k: add what enters on the right, drop what leaves on
the left. Variable size: grow right by one, then while the window breaks the
rule, shrink from the left; record the longest answer after shrinking and the
shortest one inside the shrink loop. "Exactly k" = at_most(k) - at_most(k - 1).
Windows need growing to never repair a broken window: negative numbers break
that for sums (use prefix sums). A Counter keeps keys that drop to 0.

Part 1 - Predict. Each block in PREDICT is a REPL session. Replace every ???
with exactly what Python prints: expression values are echoed the way the REPL
echoes them, and a line that raises prints just the exception name (TypeError).

Part 2 - Drills. Implement every function until `python check.py 24` is green.
Don't edit the tests at the bottom; add your own test_* functions if you like.

Unlocks: longest/shortest substring and subarray questions, anagram and
coverage windows, counting windows, "at most k" problems, and knowing when to
switch to prefix sums.
"""

PREDICT = r"""
>>> c = Counter('aab')
>>> c['b'] -= 1
>>> c, len(c)
???
>>> del c['b']
>>> len(c)
???

>>> Counter(a=1, b=0) == Counter(a=1)
???
>>> +Counter({'a': 2, 'b': 0, 'c': -1})
???

>>> need = Counter('abc')
>>> need - Counter('cbaxa'), need - Counter('ab')
???
>>> not (need - Counter('cbaxa'))
???

>>> nums, k = [4, -2, 7, 0, 3, 1], 2
>>> s = sum(nums[:k]); sums = [s]
>>> for i in range(k, len(nums)):
...     s += nums[i] - nums[i - k]
...     sums.append(s)
>>> sums
???

>>> s, k = 'abcde', 3
>>> [s[i:i + k] for i in range(len(s) - k)]
???
>>> [s[i:i + k] for i in range(len(s) - k + 1)]
???
>>> s[3:3 + k]
???

>>> s = 'abcd'
>>> list(zip(s, s[1:], s[2:]))
???

>>> d = deque(maxlen=3)
>>> for x in [1, 2, 3, 4, 5]:
...     d.append(x)
>>> d, sum(d)
???

>>> def longest_unique(s):
...     last, left, best = {}, 0, 0
...     for right, ch in enumerate(s):
...         if ch in last:
...             left = last[ch] + 1
...         last[ch] = right
...         best = max(best, right - left + 1)
...     return best
>>> longest_unique('abcb'), longest_unique('abba')
???

>>> def longest_at_most(nums, limit, record_first):
...     left = total = best = 0
...     for right, x in enumerate(nums):
...         total += x
...         if record_first:
...             best = max(best, right - left + 1)
...         while total > limit:
...             total -= nums[left]
...             left += 1
...         if not record_first:
...             best = max(best, right - left + 1)
...     return best
>>> longest_at_most([2, 1, 5, 1, 1], 4, False), longest_at_most([2, 1, 5, 1, 1], 4, True)
???

>>> def shortest_at_least(nums, target):
...     left, total, best = 0, 0, math.inf
...     for right, x in enumerate(nums):
...         total += x
...         while total >= target:
...             best = min(best, right - left + 1)
...             total -= nums[left]
...             left += 1
...     return best
>>> shortest_at_least([1, 4, 2, 2, 5, 1], 7)
???
>>> shortest_at_least([5, -10, 6], 6)
???

>>> def counts(s):
...     c = [0] * 26
...     for ch in s:
...         c[ord(ch) - ord('a')] += 1
...     return c
>>> counts('abc') == counts('cab'), counts('abc') == counts('abd')
???
>>> counts('ab')[:3]
???
"""

import math
from collections import Counter, deque


# ---------------------------------------------------------------- drills

def window_sums(nums, k):
    """Return the sum of every window of k consecutive values, left to right,
    in O(n) total (k >= 1); a window longer than nums gives [].
    window_sums([1, 2, 3, 4], 2) == [3, 5, 7]"""
    raise NotImplementedError


def max_vowels(s, k):
    """Return the most vowels (a, e, i, o, u) found in any k-character window
    of s (k >= 1), or 0 if s is shorter than k. O(n)."""
    raise NotImplementedError


def anagram_starts(s, p):
    """Return the start index of every window of s that is a rearrangement of
    p (lowercase letters, p non-empty). Keep 26 counts for the window and
    update them as it slides. anagram_starts('baxabcab', 'ab') == [0, 3, 6]"""
    raise NotImplementedError


def has_nearby_duplicate(nums, k):
    """True if two equal values sit at most k positions apart (k >= 0). Keep a
    set of the last k values. has_nearby_duplicate([5, 6, 7, 5], 3) is True"""
    raise NotImplementedError


def longest_unique(s):
    """Return the length of the longest stretch of s with no repeated
    character. Remember where each character was last seen; when it shows up
    again inside the window, jump left just past it (left never moves back)."""
    raise NotImplementedError


def longest_k_distinct(s, k):
    """Return the length of the longest stretch of s with at most k distinct
    characters (k >= 0). longest_k_distinct('abaccc', 2) == 4"""
    raise NotImplementedError


def longest_ones_with_flips(bits, k):
    """bits is a list of 0/1. Return the length of the longest run of 1s you
    can get by flipping at most k zeros, i.e. the longest window holding at
    most k zeros."""
    raise NotImplementedError


def longest_one_letter(s, k):
    """s is uppercase letters. Return the length of the longest stretch that
    can become one repeated letter by changing at most k characters. A window
    works when its length minus the count of its most common letter is <= k."""
    raise NotImplementedError


def shortest_sum_at_least(nums, target):
    """nums are positive and target >= 1. Return the length of the shortest
    window whose sum is >= target, or 0 if there's none. Record the answer
    inside the shrink loop."""
    raise NotImplementedError


def shortest_cover(s, t):
    """Return the shortest substring of s holding every character of t with
    multiplicity (t = 'aab' needs two a's and a b), or '' if there's none; t
    is non-empty, and ties go to the leftmost. Track how many characters of t
    are still missing instead of comparing whole Counters each step."""
    raise NotImplementedError


def count_product_below(nums, k):
    """nums are positive integers. Count the non-empty windows whose product is
    < k. Each step right adds right - left + 1 new windows ending at right."""
    raise NotImplementedError


def count_exactly_k_distinct(nums, k):
    """Count the non-empty windows with exactly k distinct values (k >= 1). Write
    a helper for "at most m distinct" and return at_most(k) - at_most(k - 1)."""
    raise NotImplementedError


def shortest_sum_at_least_signed(nums, target):
    """Like shortest_sum_at_least, but nums may hold negatives, which breaks the
    plain window (growing it can lower the sum). Return the shortest length or
    0 if none. Prefix sums P plus a deque of indices with increasing P: pop the
    front while P[i] - P[front] >= target, pop the back while P[back] >= P[i]."""
    raise NotImplementedError


# ---------------------------------------------------------------- tests (don't edit)

import random


def _windows(seq):
    """Every non-empty contiguous window, as (start, stop) pairs."""
    return [(i, j) for i in range(len(seq)) for j in range(i + 1, len(seq) + 1)]


def test_window_sums():
    assert window_sums([1, 2, 3, 4], 2) == [3, 5, 7]
    assert window_sums([5], 1) == [5]
    assert window_sums([1, 2], 3) == []
    assert window_sums([4, -2, 7], 3) == [9], "the last window counts too: range(n - k + 1)"
    rng = random.Random(24)
    for _ in range(200):
        nums = [rng.randint(-9, 9) for _ in range(rng.randint(0, 12))]
        k = rng.randint(1, 6)
        assert window_sums(nums, k) == [sum(nums[i:i + k]) for i in range(len(nums) - k + 1)], (nums, k)


def test_max_vowels():
    assert max_vowels('strengths aouei', 5) == 5
    assert max_vowels('xyzab', 2) == 1
    assert max_vowels('bcd', 1) == 0
    assert max_vowels('ae', 3) == 0
    rng = random.Random(24)
    for _ in range(200):
        s = ''.join(rng.choice('abeiz') for _ in range(rng.randint(0, 12)))
        k = rng.randint(1, 5)
        want = max((sum(ch in 'aeiou' for ch in s[i:i + k]) for i in range(len(s) - k + 1)), default=0)
        assert max_vowels(s, k) == want, (s, k)


def test_anagram_starts():
    assert anagram_starts('baxabcab', 'ab') == [0, 3, 6]
    assert anagram_starts('abab', 'ab') == [0, 1, 2]
    assert anagram_starts('a', 'ab') == []
    assert anagram_starts('aaa', 'a') == [0, 1, 2]
    rng = random.Random(24)
    for _ in range(200):
        s = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 10)))
        p = ''.join(rng.choice('abc') for _ in range(rng.randint(1, 3)))
        want = [i for i in range(len(s) - len(p) + 1) if sorted(s[i:i + len(p)]) == sorted(p)]
        assert anagram_starts(s, p) == want, (s, p)


def test_has_nearby_duplicate():
    assert has_nearby_duplicate([5, 6, 7, 5], 3) is True
    assert has_nearby_duplicate([5, 6, 7, 5], 2) is False
    assert has_nearby_duplicate([], 5) is False
    assert has_nearby_duplicate([1, 1], 0) is False, "k == 0 allows no pairs at all"
    assert has_nearby_duplicate([1, 1], 1) is True
    rng = random.Random(24)
    for _ in range(200):
        nums = [rng.randint(0, 5) for _ in range(rng.randint(0, 10))]
        k = rng.randint(0, 4)
        want = any(nums[i] == nums[j] for i in range(len(nums)) for j in range(i + 1, min(len(nums), i + k + 1)))
        assert has_nearby_duplicate(nums, k) == want, (nums, k)


def test_longest_unique():
    assert longest_unique('abcb') == 3
    assert longest_unique('abba') == 2, "left moved backwards: only jump when the old position is inside the window"
    assert longest_unique('') == 0 and longest_unique('aaaa') == 1
    assert longest_unique('xyxz') == 3
    rng = random.Random(24)
    for _ in range(200):
        s = ''.join(rng.choice('abcd') for _ in range(rng.randint(0, 12)))
        want = max((j - i for i, j in _windows(s) if len(set(s[i:j])) == j - i), default=0)
        assert longest_unique(s) == want, s


def test_longest_k_distinct():
    assert longest_k_distinct('abaccc', 2) == 4
    assert longest_k_distinct('abcbbbb', 2) == 6, "a Counter keeps keys at 0: delete them or len() overcounts"
    assert longest_k_distinct('abc', 0) == 0 and longest_k_distinct('', 2) == 0
    assert longest_k_distinct('aabbcc', 1) == 2 and longest_k_distinct('abcabc', 3) == 6
    rng = random.Random(24)
    for _ in range(200):
        s = ''.join(rng.choice('abcd') for _ in range(rng.randint(0, 12)))
        k = rng.randint(0, 4)
        want = max((j - i for i, j in _windows(s) if len(set(s[i:j])) <= k), default=0)
        assert longest_k_distinct(s, k) == want, (s, k)


def test_longest_ones_with_flips():
    bits = [1, 1, 0, 1, 0, 0, 1, 1]
    assert longest_ones_with_flips(bits, 0) == 2
    assert longest_ones_with_flips(bits, 1) == 4
    assert longest_ones_with_flips(bits, 2) == 5
    assert longest_ones_with_flips([], 3) == 0 and longest_ones_with_flips([0, 0], 5) == 2
    rng = random.Random(24)
    for _ in range(200):
        bits = [rng.randint(0, 1) for _ in range(rng.randint(0, 12))]
        k = rng.randint(0, 3)
        want = max((j - i for i, j in _windows(bits) if bits[i:j].count(0) <= k), default=0)
        assert longest_ones_with_flips(bits, k) == want, (bits, k)


def test_longest_one_letter():
    assert longest_one_letter('ABBBCA', 1) == 4
    assert longest_one_letter('ABBBCA', 2) == 5
    assert longest_one_letter('', 3) == 0 and longest_one_letter('AAAA', 0) == 4
    assert longest_one_letter('ABC', 0) == 1
    assert longest_one_letter('AB', 5) == 2, "a window can't be longer than s"
    rng = random.Random(24)
    for _ in range(200):
        s = ''.join(rng.choice('ABC') for _ in range(rng.randint(0, 12)))
        k = rng.randint(0, 3)
        want = max((j - i for i, j in _windows(s) if j - i - max(Counter(s[i:j]).values()) <= k), default=0)
        assert longest_one_letter(s, k) == want, (s, k)


def test_shortest_sum_at_least():
    assert shortest_sum_at_least([1, 4, 2, 2, 5, 1], 7) == 2
    assert shortest_sum_at_least([1, 1, 1], 5) == 0
    assert shortest_sum_at_least([8], 7) == 1 and shortest_sum_at_least([3, 1, 4], 8) == 3
    rng = random.Random(24)
    for _ in range(200):
        nums = [rng.randint(1, 9) for _ in range(rng.randint(0, 12))]
        t = rng.randint(1, 30)
        want = min((j - i for i, j in _windows(nums) if sum(nums[i:j]) >= t), default=0)
        assert shortest_sum_at_least(nums, t) == want, (nums, t)


def test_shortest_cover():
    assert shortest_cover('xbyaxcbaz', 'abc') == 'cba'
    assert shortest_cover('aab', 'aab') == 'aab'
    assert shortest_cover('ab', 'aab') == '', "t = 'aab' needs two a's"
    assert shortest_cover('abcba', 'ab') == 'ab', "ties go to the leftmost window"
    assert shortest_cover('', 'a') == ''
    rng = random.Random(24)
    for _ in range(200):
        s = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 10)))
        t = ''.join(rng.choice('abc') for _ in range(rng.randint(1, 3)))
        need = Counter(t)
        fits = [(j - i, i) for i, j in _windows(s) if not need - Counter(s[i:j])]
        want = s[min(fits)[1]:sum(min(fits))] if fits else ''
        assert shortest_cover(s, t) == want, (s, t)


def test_count_product_below():
    assert count_product_below([2, 3, 7, 1], 10) == 6
    assert count_product_below([1, 1, 1], 1) == 0, "no product of positive integers is below 1"
    assert count_product_below([1, 1, 1], 2) == 6
    assert count_product_below([5], 5) == 0 and count_product_below([], 10) == 0
    rng = random.Random(24)
    for _ in range(200):
        nums = [rng.randint(1, 6) for _ in range(rng.randint(0, 10))]
        k = rng.randint(0, 60)
        want = sum(math.prod(nums[i:j]) < k for i, j in _windows(nums))
        assert count_product_below(nums, k) == want, (nums, k)


def test_count_exactly_k_distinct():
    assert count_exactly_k_distinct([1, 2, 1, 3], 2) == 4
    assert count_exactly_k_distinct([1, 1, 1], 1) == 6
    assert count_exactly_k_distinct([1, 2, 3], 4) == 0 and count_exactly_k_distinct([], 1) == 0
    rng = random.Random(24)
    for _ in range(200):
        nums = [rng.randint(1, 4) for _ in range(rng.randint(0, 10))]
        k = rng.randint(1, 4)
        want = sum(len(set(nums[i:j])) == k for i, j in _windows(nums))
        assert count_exactly_k_distinct(nums, k) == want, (nums, k)


def test_shortest_sum_at_least_signed():
    assert shortest_sum_at_least_signed([5, -10, 6], 6) == 1, "the plain window never shrinks back to just [6]"
    assert shortest_sum_at_least_signed([3, -1, 2], 4) == 3
    assert shortest_sum_at_least_signed([1, 2], 4) == 0 and shortest_sum_at_least_signed([], 1) == 0
    assert shortest_sum_at_least_signed([4, -1, 2, -3, 6], 7) == 5
    rng = random.Random(24)
    for _ in range(300):
        nums = [rng.randint(-6, 8) for _ in range(rng.randint(0, 12))]
        t = rng.randint(1, 15)
        want = min((j - i for i, j in _windows(nums) if sum(nums[i:j]) >= t), default=0)
        assert shortest_sum_at_least_signed(nums, t) == want, (nums, t)
