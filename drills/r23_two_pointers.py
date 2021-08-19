"""R23 - Two pointers

Two indices that only move forward turn an O(n^2) scan over pairs into O(n).
Opposite ends: on sorted input, each comparison rules out one end for good.
Read/write: r visits every element, w marks where the next kept one goes, and
everything left of w is final. Fast/slow: two speeds on one sequence find
middles and cycles. An in-place merge works from the back so nothing you
still need gets overwritten. Write the loop's invariant as a comment first.

Part 1 - Predict. Each block in PREDICT is a REPL session. Replace every ???
with exactly what Python prints: expression values are echoed the way the REPL
echoes them, and a line that raises prints just the exception name (TypeError).

Part 2 - Drills. Implement every function until `python check.py 23` is green.
Don't edit the tests at the bottom; add your own test_* functions if you like.

Unlocks: pair and triple sums on sorted data, in-place filtering and
deduplication, partitioning, merging, palindromes, and duplicate finding in
O(1) extra space.
"""

PREDICT = r"""
>>> s = 'racecar'
>>> i, j, steps = 0, len(s) - 1, 0
>>> while i < j:
...     i, j, steps = i + 1, j - 1, steps + 1
>>> steps, i, j
???

>>> a, target = [1, 2, 4, 7, 11], 9
>>> i, j, tried = 0, len(a) - 1, []
>>> while i < j:
...     tried.append((a[i], a[j]))
...     if a[i] + a[j] == target:
...         break
...     if a[i] + a[j] < target:
...         i += 1
...     else:
...         j -= 1
>>> tried
???

>>> nums = sorted([2, -1, 0, -2, 1, -1, 2])
>>> nums
???
>>> [i for i in range(len(nums)) if i > 0 and nums[i] == nums[i - 1]]
???

>>> nums = [0, 5, 0, 2, 9]
>>> w = 0
>>> for r in range(len(nums)):
...     if nums[r] != 0:
...         nums[w], nums[r] = nums[r], nums[w]
...         w += 1
>>> nums, w
???

>>> nums = [1, 1, 2, 3, 3]
>>> w = 1
>>> for r in range(1, len(nums)):
...     if nums[r] != nums[w - 1]:
...         nums[w] = nums[r]
...         w += 1
>>> nums[:w], nums
???

>>> def trim(nums, w):
...     nums = nums[:w]
>>> xs = [1, 2, 3, 3]
>>> trim(xs, 2); xs
???
>>> del xs[2:]; xs
???

>>> a = [1, 3, 5, 0, 0]
>>> b = [2, 4]
>>> i, j, k = 2, 1, 4
>>> while j >= 0:
...     if i >= 0 and a[i] > b[j]:
...         a[k] = a[i]
...         i -= 1
...     else:
...         a[k] = b[j]
...         j -= 1
...     k -= 1
>>> a
???

>>> a = [2, 0, 1, 2, 0]
>>> lo, i, hi = 0, 0, len(a) - 1
>>> while i <= hi:
...     if a[i] == 0:
...         a[lo], a[i] = a[i], a[lo]
...         lo += 1
...         i += 1
...     elif a[i] == 2:
...         a[i], a[hi] = a[hi], a[i]
...         hi -= 1
...     else:
...         i += 1
>>> a, lo, hi
???

>>> s = 'abc'
>>> s[0], s[2] = s[2], s[0]
???
>>> t = list(s)
>>> t[0], t[2] = t[2], t[0]
>>> ''.join(t)
???

>>> a = [1, 2, 3, 4, 5]
>>> a[1:4] = a[1:4][::-1]
>>> a
???

>>> a = [1, 2, 3, 4, 5]
>>> a[-2:] + a[:-2]
???
>>> a[-7:] + a[:-7]
???
>>> k = 7 % len(a); a[-k:] + a[:-k]
???

>>> a = [1, 2, 3, 4, 5]
>>> a.reverse(); a[:2] = a[:2][::-1]; a[2:] = a[2:][::-1]
>>> a
???

>>> def middle(xs):
...     slow = fast = 0
...     while fast + 1 < len(xs):
...         slow += 1
...         fast += 2
...     return xs[slow]
>>> middle([1, 2, 3, 4, 5]), middle([1, 2, 3, 4])
???

>>> nums = [4, 3, 1, 1, 2]
>>> i, seq = 0, []
>>> for _ in range(7):
...     seq.append(i)
...     i = nums[i]
>>> seq
???
"""


# ---------------------------------------------------------------- drills

def is_palindrome(s):
    """True if s reads the same both ways once you drop every character that
    isn't a letter or digit and ignore case. Use two pointers, not a reversed
    copy. is_palindrome('No lemon, no melon') is True"""
    raise NotImplementedError


def is_subsequence(small, big):
    """True if the characters of `small` appear in `big` in the same order (not
    necessarily next to each other). is_subsequence('ace', 'abcde') is True"""
    raise NotImplementedError


def pair_with_sum(nums, target):
    """nums is sorted ascending. Return a tuple (i, j) with i < j and
    nums[i] + nums[j] == target, or None. O(n) time, O(1) extra space.
    pair_with_sum([1, 2, 4, 7, 11], 9) == (1, 3)"""
    raise NotImplementedError


def count_pairs_below(nums, target):
    """Return how many index pairs i < j have nums[i] + nums[j] < target. nums
    is unsorted: sort a copy, then whenever the ends are small enough, count
    the whole block of partners at once. O(n log n)."""
    raise NotImplementedError


def zero_sum_triples(nums):
    """Return every distinct value triple (a, b, c) with a <= b <= c, taken
    from three different positions, where a + b + c == 0, as a sorted list of
    tuples. Sort, fix the smallest value, two-pointer the rest, skip repeats.
    zero_sum_triples([0, 0, 0, 1]) == [(0, 0, 0)]"""
    raise NotImplementedError


def max_area(heights):
    """Vertical lines of these heights stand at x = 0, 1, 2, ... Return the
    largest (j - i) * min(heights[i], heights[j]) over i < j, or 0 with fewer
    than two lines. O(n): always move the shorter line inward."""
    raise NotImplementedError


def sorted_squares(nums):
    """nums is sorted ascending and may hold negatives. Return the squares in
    ascending order in O(n): the biggest square is always at one of the ends.
    sorted_squares([-5, -2, 1, 3]) == [1, 4, 9, 25]"""
    raise NotImplementedError


def dedupe_sorted(nums):
    """nums is sorted. Rearrange it in place so its first k slots hold each
    distinct value once, in order, and return k; whatever comes after slot k
    doesn't matter. nums = [1, 1, 2]: returns 2, nums starts [1, 2, ...]."""
    raise NotImplementedError


def dedupe_keep_two(nums):
    """Like dedupe_sorted, but keep up to two copies of each value.
    nums = [5, 5, 5, 6]: returns 3, nums starts [5, 5, 6, ...]."""
    raise NotImplementedError


def move_zeros(nums):
    """Move every 0 to the end, in place, keeping the other values in order.
    Return None. [4, 0, 2] becomes [4, 2, 0]."""
    raise NotImplementedError


def merge_into(a, m, b):
    """a's first m values are sorted and are followed by len(b) spare slots; b
    is sorted. Merge b into a in place so all of a is sorted; return None.
    Fill from the back so nothing you still need gets overwritten."""
    raise NotImplementedError


def three_way_partition(nums, pivot):
    """Rearrange nums in place, in one pass, so values < pivot come first, then
    values == pivot, then values > pivot. Return (lt, gt) where nums[:lt] are
    the smaller ones, nums[lt:gt] the equal ones, nums[gt:] the bigger ones."""
    raise NotImplementedError


def rotate_right(nums, k):
    """Rotate nums right by k steps in place, with three reversals and O(1)
    extra space; k may be bigger than len(nums). Return None.
    [1, 2, 3, 4, 5] rotated by 2 becomes [4, 5, 1, 2, 3]."""
    raise NotImplementedError


def find_duplicate(nums):
    """nums holds n + 1 values, each in 1..n, and exactly one value appears
    more than once (maybe many times). Return it without modifying nums and in
    O(1) extra space: follow i -> nums[i] like a linked list and use fast/slow
    pointers to find where its cycle starts."""
    raise NotImplementedError


# ---------------------------------------------------------------- tests (don't edit)

import random
from collections import Counter
from itertools import combinations


def test_is_palindrome():
    assert is_palindrome('No lemon, no melon') is True
    assert is_palindrome('never odd or even') is True
    assert is_palindrome('not a palindrome') is False
    assert is_palindrome('') is True and is_palindrome(',.!') is True and is_palindrome('a') is True
    assert is_palindrome('Abba') is True, "ignore case"
    assert is_palindrome('a1') is False and is_palindrome('1a1') is True, "digits count too"
    rng = random.Random(23)
    for _ in range(200):
        s = ''.join(rng.choice('aAb1 ,') for _ in range(rng.randint(0, 9)))
        clean = [ch.lower() for ch in s if ch.isalnum()]
        assert is_palindrome(s) == (clean == clean[::-1]), repr(s)


def test_is_subsequence():
    assert is_subsequence('ace', 'abcde') is True
    assert is_subsequence('aec', 'abcde') is False, "order matters"
    assert is_subsequence('', 'abc') is True and is_subsequence('', '') is True
    assert is_subsequence('a', '') is False
    assert is_subsequence('aa', 'ab') is False, "each character of big can be used once"
    rng = random.Random(23)
    for _ in range(200):
        big = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 7)))
        small = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 4)))
        want = any(''.join(c) == small for c in combinations(big, len(small)))
        assert is_subsequence(small, big) == want, (small, big)


def test_pair_with_sum():
    assert pair_with_sum([1, 2, 4, 7, 11], 9) == (1, 3)
    assert pair_with_sum([1, 2, 4, 7, 11], 100) is None
    assert pair_with_sum([], 0) is None
    assert pair_with_sum([5], 10) is None, "i and j must be different positions"
    assert pair_with_sum([3, 3], 6) == (0, 1)
    rng = random.Random(23)
    for _ in range(300):
        nums = sorted(rng.randint(-10, 10) for _ in range(rng.randint(0, 10)))
        t = rng.randint(-20, 20)
        got = pair_with_sum(nums, t)
        exists = any(nums[a] + nums[b] == t for a in range(len(nums)) for b in range(a + 1, len(nums)))
        if exists:
            assert got is not None, (nums, t)
            a, b = got
            assert a < b and nums[a] + nums[b] == t, (nums, t, got)
        else:
            assert got is None, (nums, t, got)


def test_count_pairs_below():
    assert count_pairs_below([3, 1, 2, 5], 5) == 2
    assert count_pairs_below([], 1) == 0 and count_pairs_below([1], 5) == 0
    assert count_pairs_below([1, 1, 1], 3) == 3
    nums = [4, 2, 9]
    count_pairs_below(nums, 7)
    assert nums == [4, 2, 9], "sort a copy, don't reorder the caller's list"
    rng = random.Random(23)
    for _ in range(200):
        nums = [rng.randint(-10, 10) for _ in range(rng.randint(0, 10))]
        t = rng.randint(-15, 15)
        want = sum(nums[a] + nums[b] < t for a in range(len(nums)) for b in range(a + 1, len(nums)))
        assert count_pairs_below(nums, t) == want, (nums, t)


def test_zero_sum_triples():
    assert zero_sum_triples([-2, 0, 1, 1, 2, -1]) == [(-2, 0, 2), (-2, 1, 1), (-1, 0, 1)]
    assert zero_sum_triples([0, 0, 0, 0]) == [(0, 0, 0)], "skip repeated values"
    assert zero_sum_triples([0, 0]) == [] and zero_sum_triples([]) == []
    assert zero_sum_triples([1, 2, -3, 4]) == [(-3, 1, 2)]
    rng = random.Random(23)
    for _ in range(150):
        nums = [rng.randint(-5, 5) for _ in range(rng.randint(0, 9))]
        want = sorted({tuple(sorted(c)) for c in combinations(nums, 3) if sum(c) == 0})
        assert zero_sum_triples(nums) == want, nums


def test_max_area():
    assert max_area([1, 3, 2, 5, 2, 4]) == 12
    assert max_area([]) == 0 and max_area([5]) == 0
    assert max_area([2, 2]) == 2
    rng = random.Random(23)
    for _ in range(200):
        h = [rng.randint(0, 9) for _ in range(rng.randint(0, 10))]
        want = max(((j - i) * min(h[i], h[j]) for i in range(len(h)) for j in range(i + 1, len(h))), default=0)
        assert max_area(h) == want, h


def test_sorted_squares():
    assert sorted_squares([-5, -2, 1, 3]) == [1, 4, 9, 25]
    assert sorted_squares([-3, -2, -1]) == [1, 4, 9]
    assert sorted_squares([]) == [] and sorted_squares([0]) == [0]
    rng = random.Random(23)
    for _ in range(200):
        nums = sorted(rng.randint(-10, 10) for _ in range(rng.randint(0, 10)))
        assert sorted_squares(nums) == sorted(x * x for x in nums), nums


def test_dedupe_sorted():
    nums = [1, 1, 2, 3, 3, 3]
    k = dedupe_sorted(nums)
    assert k == 3 and nums[:k] == [1, 2, 3], "change the caller's list in place"
    assert dedupe_sorted([]) == 0
    nums = [7]
    assert dedupe_sorted(nums) == 1 and nums[:1] == [7]
    rng = random.Random(23)
    for _ in range(200):
        nums = sorted(rng.randint(0, 5) for _ in range(rng.randint(0, 10)))
        want = sorted(set(nums))
        k = dedupe_sorted(nums)
        assert k == len(want) and nums[:k] == want, (want, k, nums)


def test_dedupe_keep_two():
    nums = [0, 0, 0, 0, 3, 5, 5, 5]
    k = dedupe_keep_two(nums)
    assert k == 5 and nums[:k] == [0, 0, 3, 5, 5]
    assert dedupe_keep_two([]) == 0
    nums = [1, 1]
    assert dedupe_keep_two(nums) == 2 and nums[:2] == [1, 1]
    rng = random.Random(23)
    for _ in range(200):
        nums = sorted(rng.randint(0, 4) for _ in range(rng.randint(0, 12)))
        want = [x for x in sorted(set(nums)) for _ in range(min(2, nums.count(x)))]
        k = dedupe_keep_two(nums)
        assert k == len(want) and nums[:k] == want, (want, k, nums)


def test_move_zeros():
    nums = [4, 0, 0, 2, 0, 7]
    assert move_zeros(nums) is None and nums == [4, 2, 7, 0, 0, 0]
    nums = [0, 0]
    move_zeros(nums)
    assert nums == [0, 0]
    rng = random.Random(23)
    for _ in range(200):
        nums = [rng.choice([0, 0, 1, 2, 3]) for _ in range(rng.randint(0, 10))]
        want = [x for x in nums if x != 0] + [0] * nums.count(0)
        move_zeros(nums)
        assert nums == want, (want, nums)


def test_merge_into():
    a = [1, 4, 7, 0, 0, 0]
    assert merge_into(a, 3, [2, 5, 6]) is None and a == [1, 2, 4, 5, 6, 7]
    a = [0]
    merge_into(a, 0, [3])
    assert a == [3], "m == 0: everything comes from b"
    a = [2, 3]
    merge_into(a, 2, [])
    assert a == [2, 3]
    a = [4, 5, 0, 0]
    merge_into(a, 2, [1, 2])
    assert a == [1, 2, 4, 5], "when a's values run out first, copy the rest of b"
    rng = random.Random(23)
    for _ in range(200):
        x = sorted(rng.randint(-5, 5) for _ in range(rng.randint(0, 6)))
        y = sorted(rng.randint(-5, 5) for _ in range(rng.randint(0, 6)))
        a = x + [0] * len(y)
        merge_into(a, len(x), y)
        assert a == sorted(x + y), (x, y, a)


def test_three_way_partition():
    nums = [5, 1, 9, 5, 3, 7, 5]
    lt, gt = three_way_partition(nums, 5)
    assert sorted(nums) == [1, 3, 5, 5, 5, 7, 9], "values were lost or duplicated"
    assert (lt, gt) == (2, 5)
    assert all(x < 5 for x in nums[:lt]) and all(x == 5 for x in nums[lt:gt]) and all(x > 5 for x in nums[gt:])
    assert three_way_partition([], 1) == (0, 0)
    rng = random.Random(23)
    for _ in range(200):
        nums = [rng.randint(0, 4) for _ in range(rng.randint(0, 10))]
        before = Counter(nums)
        p = rng.randint(0, 4)
        lt, gt = three_way_partition(nums, p)
        assert Counter(nums) == before, "values were lost or duplicated"
        assert all(x < p for x in nums[:lt]) and all(x == p for x in nums[lt:gt]) \
            and all(x > p for x in nums[gt:]), (p, nums, lt, gt)


def test_rotate_right():
    nums = [1, 2, 3, 4, 5]
    assert rotate_right(nums, 2) is None and nums == [4, 5, 1, 2, 3]
    nums = [1, 2, 3]
    rotate_right(nums, 7)
    assert nums == [3, 1, 2], "k can be bigger than len(nums): use k % n"
    nums = [1, 2, 3]
    rotate_right(nums, 3)
    assert nums == [1, 2, 3]
    nums = []
    rotate_right(nums, 4)
    assert nums == [], "an empty list: watch out for k % 0"
    rng = random.Random(23)
    for _ in range(200):
        nums = [rng.randint(0, 9) for _ in range(rng.randint(1, 8))]
        k = rng.randint(0, 20)
        want = nums[-(k % len(nums)):] + nums[:-(k % len(nums))] if k % len(nums) else nums[:]
        rotate_right(nums, k)
        assert nums == want, (k, want, nums)


def test_find_duplicate():
    assert find_duplicate([4, 3, 1, 1, 2]) == 1
    assert find_duplicate([2, 2, 2, 2]) == 2
    assert find_duplicate([1, 1]) == 1
    nums = [3, 4, 2, 3, 1]
    assert find_duplicate(nums) == 3 and nums == [3, 4, 2, 3, 1], "don't modify nums (no sorting or marking)"
    rng = random.Random(23)
    for _ in range(200):
        n = rng.randint(1, 30)
        d = rng.randint(1, n)
        vals = list(range(1, n + 1)) + [d]
        for i in range(len(vals)):
            if vals[i] != d and rng.random() < 0.2:
                vals[i] = d
        rng.shuffle(vals)
        before = vals[:]
        assert find_duplicate(vals) == d, before
        assert vals == before, "don't modify nums"
