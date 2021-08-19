"""R05 - Strings (reference solutions)

Compare after you've made your own attempt. Run: python check.py 5 -s
"""
from collections import Counter
from itertools import groupby

PREDICT = r"""
>>> 'a  b'.split()
['a', 'b']
>>> 'a  b'.split(' ')
['a', '', 'b']

>>> 'a,b,,c'.split(',')
['a', 'b', '', 'c']
>>> 'a,b,,c'.split(',', 1)
['a', 'b,,c']

>>> 'abcba'.strip('ab')
'c'
>>> 'abcba'.removeprefix('ab')
'cba'
>>> '  hi  '.lstrip() + '|'
'hi  |'

>>> '10' < '9', 'Z' < 'a', 'app' < 'apple'
(True, True, True)

>>> sorted(['b', 'A', 'a', 'B'])
['A', 'B', 'a', 'b']
>>> sorted(['b', 'A', 'a', 'B'], key=str.lower)
['A', 'a', 'b', 'B']

>>> s = 'hello'
>>> s[0] = 'j'
TypeError
>>> s.replace('h', 'j'), s
('jello', 'hello')

>>> ord('a'), chr(98), ord('a') - ord('A')
(97, 'b', 32)
>>> chr(ord('a') + 25)
'z'

>>> '-5'.isdigit(), '5'.isdigit(), ''.isalpha(), 'abc1'.isalnum()
(False, True, False, True)

>>> ','.join([1, 2])
TypeError
>>> ','.join(map(str, [1, 2]))
'1,2'

>>> 'abc'.find('z')
-1
>>> 'abc'.index('z')
ValueError

>>> s = 'racecar'
>>> s[::-1] == s, s[::2], s[-3:]
(True, 'rccr', 'car')

>>> 'abc'[5:], 'abc'[1:100]
('', 'bc')
>>> 'abc'[5]
IndexError

>>> 'ab' * 3, 'ab' + 'cd' * 2
('ababab', 'abcdcd')

>>> f'{7:08b}', f'{255:x}', f'{3.14159:.2f}', f'{42:>5}|'
('00000111', 'ff', '3.14', '   42|')

>>> x = 5
>>> f'{x=}'
'x=5'

>>> int('101', 2), int('ff', 16), bin(5), hex(255)
(5, 255, '0b101', '0xff')

>>> 'banana'.count('ana'), 'banana'.find('ana', 2)
(1, 3)

>>> sorted('banana')
['a', 'a', 'a', 'b', 'n', 'n']
>>> ''.join(sorted('banana'))
'aaabnn'

>>> 'ab' in 'cabd', '' in 'abc', 'abc'.startswith(('x', 'a'))
(True, True, True)
"""


def char_counts(s):
    counts = [0] * 26
    for c in s:
        if 'a' <= c <= 'z':
            counts[ord(c) - ord('a')] += 1
    return counts


def signature(word):
    return tuple(char_counts(word))


def is_anagram(a, b):
    return Counter(a) == Counter(b)


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


def reverse_words(s):
    return ' '.join(reversed(s.split()))


def interleave(a, b):
    parts = []
    for x, y in zip(a, b):
        parts.append(x)
        parts.append(y)
    n = min(len(a), len(b))
    parts.append(a[n:])
    parts.append(b[n:])
    return ''.join(parts)


def rle_encode(s):
    return ''.join(f'{len(list(run))}{ch}' for ch, run in groupby(s))


def rle_decode(code):
    parts, num = [], 0
    for c in code:
        if c.isdigit():
            num = num * 10 + int(c)
        else:
            parts.append(c * num)
            num = 0
    return ''.join(parts)


def parse_ints(s):
    out, i, n = [], 0, len(s)
    while i < n:
        negative = s[i] == '-' and i + 1 < n and s[i + 1].isdigit()
        if not (s[i].isdigit() or negative):
            i += 1
            continue
        if negative:
            i += 1
        num = 0
        while i < n and s[i].isdigit():
            num = num * 10 + int(s[i])
            i += 1
        out.append(-num if negative else num)
    return out


def caesar(s, k):
    a = ord('a')
    return ''.join(chr((ord(c) - a + k) % 26 + a) if 'a' <= c <= 'z' else c for c in s)


def to_base(n, base):
    digits = '0123456789abcdefghijklmnopqrstuvwxyz'
    if n == 0:
        return '0'
    sign, n = ('-', -n) if n < 0 else ('', n)
    out = []
    while n:
        n, r = divmod(n, base)
        out.append(digits[r])
    return sign + ''.join(reversed(out))


def common_prefix(words):
    if not words:
        return ''
    lo, hi = min(words), max(words)  # the lexicographic extremes share exactly the common prefix
    i = 0
    while i < len(lo) and lo[i] == hi[i]:
        i += 1
    return lo[:i]


def format_row(name, qty, price):
    return f'{name:<10}{qty:>4}{price:>8.2f}'


def is_rotation(a, b):
    return len(a) == len(b) and b in a + a
