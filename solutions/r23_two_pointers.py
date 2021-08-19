"""R23 - Two pointers (reference solutions)

Compare after you've made your own attempt. Run: python check.py 23 -s
"""

PREDICT = r"""
>>> s = 'racecar'
>>> i, j, steps = 0, len(s) - 1, 0
>>> while i < j:
...     i, j, steps = i + 1, j - 1, steps + 1
>>> steps, i, j
(3, 3, 3)

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
[(1, 11), (1, 7), (2, 7)]

>>> nums = sorted([2, -1, 0, -2, 1, -1, 2])
>>> nums
[-2, -1, -1, 0, 1, 2, 2]
>>> [i for i in range(len(nums)) if i > 0 and nums[i] == nums[i - 1]]
[2, 6]

>>> nums = [0, 5, 0, 2, 9]
>>> w = 0
>>> for r in range(len(nums)):
...     if nums[r] != 0:
...         nums[w], nums[r] = nums[r], nums[w]
...         w += 1
>>> nums, w
([5, 2, 9, 0, 0], 3)

>>> nums = [1, 1, 2, 3, 3]
>>> w = 1
>>> for r in range(1, len(nums)):
...     if nums[r] != nums[w - 1]:
...         nums[w] = nums[r]
...         w += 1
>>> nums[:w], nums
([1, 2, 3], [1, 2, 3, 3, 3])

>>> def trim(nums, w):
...     nums = nums[:w]
>>> xs = [1, 2, 3, 3]
>>> trim(xs, 2); xs
[1, 2, 3, 3]
>>> del xs[2:]; xs
[1, 2]

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
[1, 2, 3, 4, 5]

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
([0, 0, 1, 2, 2], 2, 2)

>>> s = 'abc'
>>> s[0], s[2] = s[2], s[0]
TypeError
>>> t = list(s)
>>> t[0], t[2] = t[2], t[0]
>>> ''.join(t)
'cba'

>>> a = [1, 2, 3, 4, 5]
>>> a[1:4] = a[1:4][::-1]
>>> a
[1, 4, 3, 2, 5]

>>> a = [1, 2, 3, 4, 5]
>>> a[-2:] + a[:-2]
[4, 5, 1, 2, 3]
>>> a[-7:] + a[:-7]
[1, 2, 3, 4, 5]
>>> k = 7 % len(a); a[-k:] + a[:-k]
[4, 5, 1, 2, 3]

>>> a = [1, 2, 3, 4, 5]
>>> a.reverse(); a[:2] = a[:2][::-1]; a[2:] = a[2:][::-1]
>>> a
[4, 5, 1, 2, 3]

>>> def middle(xs):
...     slow = fast = 0
...     while fast + 1 < len(xs):
...         slow += 1
...         fast += 2
...     return xs[slow]
>>> middle([1, 2, 3, 4, 5]), middle([1, 2, 3, 4])
(3, 3)

>>> nums = [4, 3, 1, 1, 2]
>>> i, seq = 0, []
>>> for _ in range(7):
...     seq.append(i)
...     i = nums[i]
>>> seq
[0, 4, 2, 1, 3, 1, 3]
"""


def is_palindrome(s):
    i, j = 0, len(s) - 1
    while i < j:
        if not s[i].isalnum():
            i += 1
        elif not s[j].isalnum():
            j -= 1
        elif s[i].lower() != s[j].lower():
            return False
        else:
            i, j = i + 1, j - 1
    return True


def is_subsequence(small, big):
    i = 0
    for ch in big:
        if i < len(small) and small[i] == ch:
            i += 1
    return i == len(small)


def pair_with_sum(nums, target):
    i, j = 0, len(nums) - 1
    while i < j:
        total = nums[i] + nums[j]
        if total == target:
            return (i, j)
        if total < target:
            i += 1          # nums[i] is too small even with the biggest partner left
        else:
            j -= 1          # nums[j] is too big even with the smallest partner left
    return None


def count_pairs_below(nums, target):
    a = sorted(nums)
    i, j, count = 0, len(a) - 1, 0
    while i < j:
        if a[i] + a[j] < target:
            count += j - i  # a[i] works with every partner in (i, j]
            i += 1
        else:
            j -= 1
    return count


def zero_sum_triples(nums):
    a = sorted(nums)
    out = []
    for i in range(len(a) - 2):
        if i > 0 and a[i] == a[i - 1]:
            continue
        lo, hi = i + 1, len(a) - 1
        while lo < hi:
            total = a[i] + a[lo] + a[hi]
            if total < 0:
                lo += 1
            elif total > 0:
                hi -= 1
            else:
                out.append((a[i], a[lo], a[hi]))
                lo += 1
                while lo < hi and a[lo] == a[lo - 1]:
                    lo += 1
                hi -= 1
    return out


def max_area(heights):
    i, j, best = 0, len(heights) - 1, 0
    while i < j:
        best = max(best, (j - i) * min(heights[i], heights[j]))
        if heights[i] < heights[j]:
            i += 1          # the shorter line can't do better with any closer partner
        else:
            j -= 1
    return best


def sorted_squares(nums):
    out = [0] * len(nums)
    i, j = 0, len(nums) - 1
    for k in range(len(nums) - 1, -1, -1):
        if abs(nums[i]) > abs(nums[j]):
            out[k] = nums[i] * nums[i]
            i += 1
        else:
            out[k] = nums[j] * nums[j]
            j -= 1
    return out


def dedupe_sorted(nums):
    if not nums:
        return 0
    w = 1                   # nums[:w] is final
    for r in range(1, len(nums)):
        if nums[r] != nums[w - 1]:
            nums[w] = nums[r]
            w += 1
    return w


def dedupe_keep_two(nums):
    w = 0
    for x in nums:
        if w < 2 or x != nums[w - 2]:   # a third copy would equal the value two slots back
            nums[w] = x
            w += 1
    return w


def move_zeros(nums):
    w = 0
    for r in range(len(nums)):
        if nums[r] != 0:
            nums[w], nums[r] = nums[r], nums[w]
            w += 1


def merge_into(a, m, b):
    i, j, k = m - 1, len(b) - 1, m + len(b) - 1
    while j >= 0:           # once b is used up, a's leftovers are already in place
        if i >= 0 and a[i] > b[j]:
            a[k] = a[i]
            i -= 1
        else:
            a[k] = b[j]
            j -= 1
        k -= 1


def three_way_partition(nums, pivot):
    lt, i, gt = 0, 0, len(nums)        # [0, lt) < pivot, [lt, i) == pivot, [gt, n) > pivot
    while i < gt:
        if nums[i] < pivot:
            nums[lt], nums[i] = nums[i], nums[lt]
            lt += 1
            i += 1
        elif nums[i] > pivot:
            gt -= 1
            nums[i], nums[gt] = nums[gt], nums[i]   # the swapped-in value is unchecked: don't move i
        else:
            i += 1
    return lt, gt


def rotate_right(nums, k):
    n = len(nums)
    if n == 0:
        return
    k %= n

    def reverse(lo, hi):
        while lo < hi:
            nums[lo], nums[hi] = nums[hi], nums[lo]
            lo, hi = lo + 1, hi - 1

    reverse(0, n - 1)
    reverse(0, k - 1)
    reverse(k, n - 1)


def find_duplicate(nums):
    slow = fast = 0
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    slow = 0                # restart one pointer: they meet where the cycle begins
    while slow != fast:
        slow, fast = nums[slow], nums[fast]
    return slow
