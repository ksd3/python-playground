"""R05 - Strings

Strings are immutable: build output in a list and ''.join(parts) at the end
(s += c in a loop can go quadratic; CPython sometimes optimizes it, PyPy doesn't).
ord(c) - ord('a') maps a letter to 0-25 and chr(i + ord('a')) maps it back; a
26-slot count list turned into a tuple is a hashable anagram signature.
Strings compare by code point, one character at a time: 'Z' < 'a', '10' < '9'.
split() splits on runs of whitespace, split(' ') on every single space; strip()
removes a SET of characters; find() returns -1 where index() raises. A set of
strings iterates in a different order on each run (string hashes are randomized).

Part 1 - Predict. Each block in PREDICT is a REPL session. Replace every ???
with exactly what Python prints: expression values are echoed the way the REPL
echoes them, and a line that raises prints just the exception name (TypeError).

Part 2 - Drills. Implement every function until `python check.py 5` is green.
Don't edit the tests at the bottom; add your own test_* functions if you like.

Unlocks: anagram and palindrome problems, parsers and calculators, building
strings, and sliding windows over strings.
"""
from collections import Counter
from itertools import groupby

PREDICT = r"""
>>> 'a  b'.split()
???
>>> 'a  b'.split(' ')
???

>>> 'a,b,,c'.split(',')
???
>>> 'a,b,,c'.split(',', 1)
???

>>> 'abcba'.strip('ab')
???
>>> 'abcba'.removeprefix('ab')
???
>>> '  hi  '.lstrip() + '|'
???

>>> '10' < '9', 'Z' < 'a', 'app' < 'apple'
???

>>> sorted(['b', 'A', 'a', 'B'])
???
>>> sorted(['b', 'A', 'a', 'B'], key=str.lower)
???

>>> s = 'hello'
>>> s[0] = 'j'
???
>>> s.replace('h', 'j'), s
???

>>> ord('a'), chr(98), ord('a') - ord('A')
???
>>> chr(ord('a') + 25)
???

>>> '-5'.isdigit(), '5'.isdigit(), ''.isalpha(), 'abc1'.isalnum()
???

>>> ','.join([1, 2])
???
>>> ','.join(map(str, [1, 2]))
???

>>> 'abc'.find('z')
???
>>> 'abc'.index('z')
???

>>> s = 'racecar'
>>> s[::-1] == s, s[::2], s[-3:]
???

>>> 'abc'[5:], 'abc'[1:100]
???
>>> 'abc'[5]
???

>>> 'ab' * 3, 'ab' + 'cd' * 2
???

>>> f'{7:08b}', f'{255:x}', f'{3.14159:.2f}', f'{42:>5}|'
???

>>> x = 5
>>> f'{x=}'
???

>>> int('101', 2), int('ff', 16), bin(5), hex(255)
???

>>> 'banana'.count('ana'), 'banana'.find('ana', 2)
???

>>> sorted('banana')
???
>>> ''.join(sorted('banana'))
???

>>> 'ab' in 'cabd', '' in 'abc', 'abc'.startswith(('x', 'a'))
???
"""


# ---------------------------------------------------------------- drills

def char_counts(s):
    """Return a list of 26 counts for the lowercase letters a-z in s; every
    other character is ignored. char_counts('abca')[:3] == [2, 1, 1]"""
    raise NotImplementedError


def signature(word):
    """Return the 26 letter counts of a lowercase word as a tuple: equal for
    two words exactly when they're anagrams, and hashable.
    signature('listen') == signature('silent')"""
    raise NotImplementedError


def is_anagram(a, b):
    """Return True if b is a rearrangement of a (same characters with the same
    counts, case-sensitive), else False. is_anagram('anagram', 'nagaram') is True"""
    raise NotImplementedError


def is_palindrome(s):
    """Return True if s reads the same both ways once you keep only letters and
    digits and ignore case, else False. Use two pointers, no copies of s.
    is_palindrome('A man, a plan, a canal: Panama') is True"""
    raise NotImplementedError


def reverse_words(s):
    """Reverse the order of the words; any run of whitespace separates words,
    and the result has single spaces and nothing at either end.
    reverse_words('  the sky  is blue ') == 'blue is sky the'"""
    raise NotImplementedError


def interleave(a, b):
    """Alternate characters of a and b, then append whatever is left of the
    longer one. Build a list and join it once. interleave('abc', '12345') == 'a1b2c345'"""
    raise NotImplementedError


def rle_encode(s):
    """Run-length encode s as count followed by character for every run of
    equal characters (s has no digits). rle_encode('aaabcc') == '3a1b2c'"""
    raise NotImplementedError


def rle_decode(code):
    """Undo rle_encode. Counts can have several digits, so accumulate them with
    num = num * 10 + int(c). rle_decode('12a1b') == 'aaaaaaaaaaaab'"""
    raise NotImplementedError


def parse_ints(s):
    """Return every integer in s, scanning character by character: a run of
    digits is a number, and a '-' right before the run makes it negative.
    parse_ints('a12b-3c004') == [12, -3, 4], parse_ints('x-y') == []"""
    raise NotImplementedError


def caesar(s, k):
    """Shift every lowercase letter k places through the alphabet, wrapping
    around (k can be negative or bigger than 26); leave everything else as is.
    caesar('abz!', 2) == 'cdb!', caesar('a', -1) == 'z'"""
    raise NotImplementedError


def to_base(n, base):
    """Write integer n in base 2-36 with digits 0-9 then a-z, a '-' for
    negatives and no leading zeros, using divmod (not format or bin).
    to_base(255, 16) == 'ff', to_base(-5, 2) == '-101', to_base(0, 7) == '0'"""
    raise NotImplementedError


def common_prefix(words):
    """Return the longest string that every word starts with ('' for an empty
    list). common_prefix(['flow', 'flower', 'flight']) == 'fl'"""
    raise NotImplementedError


def format_row(name, qty, price):
    """One table row via an f-string: name left-aligned in 10 columns, qty
    right-aligned in 4, price right-aligned in 8 with 2 decimals, nothing
    between them. format_row('apple', 3, 1.5) == 'apple        3    1.50'"""
    raise NotImplementedError


def is_rotation(a, b):
    """Return True if b is a rotation of a (some suffix of a moved to the
    front), else False. is_rotation('waterbottle', 'erbottlewat') is True"""
    raise NotImplementedError


# ---------------------------------------------------------------- tests (don't edit)
import os as _os
import random as _random
import re as _re
from itertools import groupby as _groupby


def _word(rng, alphabet='abc', lo=0, hi=6):
    return ''.join(rng.choice(alphabet) for _ in range(rng.randint(lo, hi)))


def _rle(s):
    return ''.join(f'{len(list(run))}{ch}' for ch, run in _groupby(s))


def test_char_counts():
    counts = char_counts('abca')
    assert len(counts) == 26 and counts[:4] == [2, 1, 1, 0]
    assert char_counts('') == [0] * 26
    assert char_counts('zz-Z!')[25] == 2, "only lowercase a-z count"
    assert sum(char_counts('hello world')) == 10


def test_signature():
    assert signature('listen') == signature('silent')
    assert signature('abc') != signature('abd')
    sig = signature('aab')
    assert isinstance(sig, tuple) and len(sig) == 26 and sig[:2] == (2, 1)
    assert len({signature(w) for w in ['tea', 'eat', 'ate', 'tan']}) == 2


def test_is_anagram():
    assert is_anagram('anagram', 'nagaram') is True
    assert is_anagram('rat', 'car') is False
    assert is_anagram('', '') is True
    assert is_anagram('ab', 'abb') is False, "same letters, different counts"
    assert is_anagram('Ab', 'ab') is False, "the comparison is case-sensitive"
    rng = _random.Random(5)
    for _ in range(300):
        a, b = _word(rng), _word(rng)
        assert is_anagram(a, b) == (sorted(a) == sorted(b)), (a, b)


def test_is_palindrome():
    assert is_palindrome('A man, a plan, a canal: Panama') is True
    assert is_palindrome('race a car') is False
    assert is_palindrome('') is True and is_palindrome('.,') is True
    assert is_palindrome('0P') is False, "digits are characters too"
    assert is_palindrome('ab_a') is True
    rng = _random.Random(5)
    for _ in range(300):
        s = _word(rng, 'aAb1 ,', 0, 8)
        kept = [c.lower() for c in s if c.isalnum()]
        assert is_palindrome(s) == (kept == kept[::-1]), s


def test_reverse_words():
    assert reverse_words('  the sky  is blue ') == 'blue is sky the'
    assert reverse_words('one') == 'one'
    assert reverse_words('   ') == ''
    assert reverse_words('a\tb\nc') == 'c b a', "any whitespace separates words"


def test_interleave():
    assert interleave('abc', '12345') == 'a1b2c345'
    assert interleave('abcd', '12') == 'a1b2cd'
    assert interleave('', 'xy') == 'xy'
    assert interleave('', '') == ''


def test_rle_encode():
    assert rle_encode('aaabcc') == '3a1b2c'
    assert rle_encode('') == ''
    assert rle_encode('abab') == '1a1b1a1b'
    assert rle_encode('z' * 12) == '12z'


def test_rle_decode():
    assert rle_decode('3a1b2c') == 'aaabcc'
    assert rle_decode('12a1b') == 'a' * 12 + 'b', "counts can have several digits"
    assert rle_decode('') == ''
    rng = _random.Random(5)
    for _ in range(200):
        s = ''.join(rng.choice('ab') * rng.randint(1, 12) for _ in range(rng.randint(0, 5)))
        assert rle_decode(_rle(s)) == s, s


def test_parse_ints():
    assert parse_ints('a12b-3c004') == [12, -3, 4]
    assert parse_ints('x-y') == []
    assert parse_ints('') == []
    assert parse_ints('--5') == [-5]
    assert parse_ints('5-3') == [5, -3]
    assert parse_ints('-0') == [0]
    rng = _random.Random(5)
    for _ in range(300):
        s = _word(rng, 'a1-90', 0, 10)
        assert parse_ints(s) == [int(t) for t in _re.findall(r'-?\d+', s)], s


def test_caesar():
    assert caesar('abz!', 2) == 'cdb!'
    assert caesar('a', -1) == 'z'
    assert caesar('hello', 26) == 'hello' and caesar('hello', 27) == 'ifmmp'
    assert caesar('Hi there', 1) == 'Hj uifsf', "only lowercase letters move"
    rng = _random.Random(5)
    for _ in range(100):
        s, k = _word(rng, 'abxyz .A', 0, 8), rng.randint(-60, 60)
        assert caesar(caesar(s, k), -k) == s, (s, k)


def test_to_base():
    assert to_base(255, 16) == 'ff'
    assert to_base(-5, 2) == '-101'
    assert to_base(0, 7) == '0'
    assert to_base(35, 36) == 'z'
    rng = _random.Random(5)
    for _ in range(500):
        n, b = rng.randint(-10**6, 10**6), rng.randint(2, 36)
        s = to_base(n, b)
        assert int(s, b) == n, (n, b, s)
        assert s == '0' or not s.lstrip('-').startswith('0'), "no leading zeros"
        assert s == s.lower()


def test_common_prefix():
    assert common_prefix(['flow', 'flower', 'flight']) == 'fl'
    assert common_prefix(['dog', 'car']) == ''
    assert common_prefix([]) == ''
    assert common_prefix(['alone']) == 'alone'
    assert common_prefix(['ab', '']) == ''
    rng = _random.Random(5)
    for _ in range(300):
        words = [_word(rng, 'ab', 0, 4) for _ in range(rng.randint(1, 4))]
        assert common_prefix(words) == _os.path.commonprefix(words), words


def test_format_row():
    assert format_row('apple', 3, 1.5) == 'apple        3    1.50'
    assert format_row('kiwi', 120, 0.25) == 'kiwi       120    0.25'
    assert format_row('watermelons', 10, 12.5) == 'watermelons  10   12.50', "padding never truncates"


def test_is_rotation():
    assert is_rotation('waterbottle', 'erbottlewat') is True
    assert is_rotation('abc', 'acb') is False
    assert is_rotation('', '') is True
    assert is_rotation('a', 'aa') is False, "check the lengths first"
    rng = _random.Random(5)
    for _ in range(300):
        a, b = _word(rng, 'ab', 0, 5), _word(rng, 'ab', 0, 5)
        expected = len(a) == len(b) and any(a[i:] + a[:i] == b for i in range(len(a) or 1))
        assert is_rotation(a, b) == expected, (a, b)
