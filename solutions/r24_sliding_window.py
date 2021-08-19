"""R24 - Sliding window (reference solutions)

Compare after you've made your own attempt. Run: python check.py 24 -s
"""

PREDICT = r"""
>>> c = Counter('aab')
>>> c['b'] -= 1
>>> c, len(c)
(Counter({'a': 2, 'b': 0}), 2)
>>> del c['b']
>>> len(c)
1

>>> Counter(a=1, b=0) == Counter(a=1)
True
>>> +Counter({'a': 2, 'b': 0, 'c': -1})
Counter({'a': 2})

>>> need = Counter('abc')
>>> need - Counter('cbaxa'), need - Counter('ab')
(Counter(), Counter({'c': 1}))
>>> not (need - Counter('cbaxa'))
True

>>> nums, k = [4, -2, 7, 0, 3, 1], 2
>>> s = sum(nums[:k]); sums = [s]
>>> for i in range(k, len(nums)):
...     s += nums[i] - nums[i - k]
...     sums.append(s)
>>> sums
[2, 5, 7, 3, 4]

>>> s, k = 'abcde', 3
>>> [s[i:i + k] for i in range(len(s) - k)]
['abc', 'bcd']
>>> [s[i:i + k] for i in range(len(s) - k + 1)]
['abc', 'bcd', 'cde']
>>> s[3:3 + k]
'de'

>>> s = 'abcd'
>>> list(zip(s, s[1:], s[2:]))
[('a', 'b', 'c'), ('b', 'c', 'd')]

>>> d = deque(maxlen=3)
>>> for x in [1, 2, 3, 4, 5]:
...     d.append(x)
>>> d, sum(d)
(deque([3, 4, 5], maxlen=3), 12)

>>> def longest_unique(s):
...     last, left, best = {}, 0, 0
...     for right, ch in enumerate(s):
...         if ch in last:
...             left = last[ch] + 1
...         last[ch] = right
...         best = max(best, right - left + 1)
...     return best
>>> longest_unique('abcb'), longest_unique('abba')
(3, 3)

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
(2, 3)

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
2
>>> shortest_at_least([5, -10, 6], 6)
inf

>>> def counts(s):
...     c = [0] * 26
...     for ch in s:
...         c[ord(ch) - ord('a')] += 1
...     return c
>>> counts('abc') == counts('cab'), counts('abc') == counts('abd')
(True, False)
>>> counts('ab')[:3]
[1, 1, 0]
"""

import math
from collections import Counter, deque


def window_sums(nums, k):
    if k > len(nums):
        return []
    total = sum(nums[:k])
    out = [total]
    for i in range(k, len(nums)):
        total += nums[i] - nums[i - k]      # one value enters, one leaves
        out.append(total)
    return out


def max_vowels(s, k):
    if len(s) < k:
        return 0
    vowels = set('aeiou')
    count = sum(ch in vowels for ch in s[:k])
    best = count
    for i in range(k, len(s)):
        count += (s[i] in vowels) - (s[i - k] in vowels)
        best = max(best, count)
    return best


def anagram_starts(s, p):
    k = len(p)
    need, have = [0] * 26, [0] * 26
    for ch in p:
        need[ord(ch) - ord('a')] += 1
    out = []
    for i, ch in enumerate(s):
        have[ord(ch) - ord('a')] += 1
        if i >= k:
            have[ord(s[i - k]) - ord('a')] -= 1
        if i >= k - 1 and have == need:
            out.append(i - k + 1)
    return out


def has_nearby_duplicate(nums, k):
    window = set()                      # the last k values
    for i, x in enumerate(nums):
        if x in window:
            return True
        window.add(x)
        if len(window) > k:
            window.remove(nums[i - k])
    return False


def longest_unique(s):
    last, left, best = {}, 0, 0
    for right, ch in enumerate(s):
        if last.get(ch, -1) >= left:    # only a repeat inside the window matters
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best


def longest_k_distinct(s, k):
    count, left, best = Counter(), 0, 0
    for right, ch in enumerate(s):
        count[ch] += 1
        while len(count) > k:
            count[s[left]] -= 1
            if count[s[left]] == 0:
                del count[s[left]]
            left += 1
        best = max(best, right - left + 1)
    return best


def longest_ones_with_flips(bits, k):
    left = zeros = best = 0
    for right, b in enumerate(bits):
        zeros += b == 0
        while zeros > k:
            zeros -= bits[left] == 0
            left += 1
        best = max(best, right - left + 1)
    return best


def longest_one_letter(s, k):
    count, left, top, best = Counter(), 0, 0, 0
    for right, ch in enumerate(s):
        count[ch] += 1
        top = max(top, count[ch])
        # top can go stale (too high) after shrinking; that only stops the
        # window from growing, and the answer only improves when top grows.
        while right - left + 1 - top > k:
            count[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best


def shortest_sum_at_least(nums, target):
    left = total = 0
    best = math.inf
    for right, x in enumerate(nums):
        total += x
        while total >= target:
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1
    return 0 if best == math.inf else best


def shortest_cover(s, t):
    need = Counter(t)
    missing = len(t)
    left = 0
    best_len, best_start = math.inf, 0
    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1                   # negative means the window has extras
        while missing == 0:
            if right - left + 1 < best_len:
                best_len, best_start = right - left + 1, left
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1
            left += 1
    return '' if best_len == math.inf else s[best_start:best_start + best_len]


def count_product_below(nums, k):
    left, product, count = 0, 1, 0
    for right, x in enumerate(nums):
        product *= x
        while product >= k and left <= right:
            product //= nums[left]
            left += 1
        count += right - left + 1       # windows ending at right
    return count


def count_exactly_k_distinct(nums, k):
    def at_most(m):
        count, left, total = Counter(), 0, 0
        for right, x in enumerate(nums):
            count[x] += 1
            while len(count) > m:
                count[nums[left]] -= 1
                if count[nums[left]] == 0:
                    del count[nums[left]]
                left += 1
            total += right - left + 1
        return total

    return at_most(k) - at_most(k - 1)


def shortest_sum_at_least_signed(nums, target):
    prefix = [0]
    for x in nums:
        prefix.append(prefix[-1] + x)
    best = math.inf
    starts = deque()                    # indices whose prefix sums increase
    for i, p in enumerate(prefix):
        while starts and p - prefix[starts[0]] >= target:
            best = min(best, i - starts.popleft())
        while starts and prefix[starts[-1]] >= p:
            starts.pop()                # a later, smaller prefix is a better start
        starts.append(i)
    return 0 if best == math.inf else best
