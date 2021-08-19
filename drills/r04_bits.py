"""R04 - Bit manipulation

Python ints behave like two's complement with infinitely many sign bits, so
nothing overflows or wraps at 32 bits: ~x == -x - 1, -1 >> 1 == -1, and
bin(-5) is '-0b101'. x & -x isolates the lowest set bit; x & (x - 1) clears it.
Precedence: + and - bind tighter than << and >> (1 << 2 + 1 == 8), and & | ^
bind tighter than == (unlike C). Mask with & 0xFFFFFFFF to emulate 32 bits; a
carry loop on negative numbers never ends without that mask. int.bit_count()
is 3.10+; bin(x).count('1') works everywhere.

Part 1 - Predict. Each block in PREDICT is a REPL session. Replace every ???
with exactly what Python prints: expression values are echoed the way the REPL
echoes them, and a line that raises prints just the exception name (TypeError).

Part 2 - Drills. Implement every function until `python check.py 4` is green.
Don't edit the tests at the bottom; add your own test_* functions if you like.

Unlocks: the "everything appears twice but one" family, trying every subset
when n <= 20, bitmask DP and visited-state compression, 32-bit bit puzzles,
and fast subset-sum checks.
"""
import functools
import itertools
import operator
import random

PREDICT = r"""
>>> ~5, ~-1, -~5
???

>>> -1 >> 1, -8 >> 1, 8 >> 1
???

>>> bin(5), bin(-5)
???

>>> -5 & 0xFF, 5 & -5
???

>>> 12 & -12, 12 & 11, 12 | 11
???

>>> (8).bit_length(), (0).bit_length(), (-8).bit_length()
???

>>> bin(255).count('1'), (255).bit_count()
???

>>> 1 << 10, 3 << 2, 1 << 2 + 1
???

>>> 6 & 1 == 0
???

>>> 5 ^ 3, 5 ^ 5, 5 ^ 0
???
>>> functools.reduce(operator.xor, [4, 1, 2, 1, 2])
???

>>> [i for i in range(4) if 0b1010 >> i & 1]
???

>>> int('1011', 2), f'{11:b}', f'{11:08b}', format(11, '#x')
???

>>> [i ^ (i >> 1) for i in range(8)]
???

>>> mask, sub, out = 0b101, 0b101, []
>>> while sub:
...     out.append(bin(sub))
...     sub = (sub - 1) & mask
>>> out
???

>>> bits = 1
>>> for x in [3, 5]:
...     bits |= bits << x
>>> bin(bits), [s for s in range(9) if bits >> s & 1]
???

>>> x = 0xFFFFFFFF
>>> x - (1 << 32) if x >> 31 else x
???
>>> -3 & 0xFFFFFFFF
???

>>> 1 << 64, (1 << 64) - 1 == 2**64 - 1
???
"""


# ---------------------------------------------------------------- drills

def get_bit(x, i):
    """Return bit i of x >= 0 (0 or 1); bit 0 is the least significant.
    get_bit(0b1010, 1) == 1"""
    raise NotImplementedError


def set_bit(x, i):
    """Return x with bit i set to 1. set_bit(0b1000, 1) == 0b1010"""
    raise NotImplementedError


def clear_bit(x, i):
    """Return x with bit i set to 0. clear_bit(0b1010, 1) == 0b1000"""
    raise NotImplementedError


def toggle_bit(x, i):
    """Return x with bit i flipped. toggle_bit(0b1010, 0) == 0b1011"""
    raise NotImplementedError


def lowest_set_bit(x):
    """Return the value of the lowest set bit of x >= 0 (0 when x is 0), in
    O(1). lowest_set_bit(12) == 4"""
    raise NotImplementedError


def is_power_of_two(x):
    """True if x is a power of two (1, 2, 4, ...), in O(1). Zero and negative
    numbers are not."""
    raise NotImplementedError


def popcount(x):
    """Number of set bits in x >= 0 using the x & (x - 1) trick: one loop
    iteration per set bit, no bin() or bit_count()."""
    raise NotImplementedError


def single_unpaired(nums):
    """Every value appears exactly twice except one; return that one in O(n)
    time and O(1) extra space. single_unpaired([4, 1, 2, 1, 2]) == 4"""
    raise NotImplementedError


def range_xor(nums, queries):
    """For each (l, r) in queries return nums[l] ^ ... ^ nums[r] (inclusive),
    in O(len(nums) + len(queries)) total, using a prefix-XOR array."""
    raise NotImplementedError


def subsets(items):
    """All subsets of items by bitmask: mask m picks items[i] whenever bit i of
    m is set. Return them as lists, in mask order 0, 1, ..., 2**n - 1:
    subsets('ab') == [[], ['a'], ['b'], ['a', 'b']]"""
    raise NotImplementedError


def submasks(mask):
    """All non-empty submasks of mask, largest first, using
    sub = (sub - 1) & mask. submasks(0b101) == [0b101, 0b100, 0b001]"""
    raise NotImplementedError


def to_signed32(x):
    """Interpret the low 32 bits of x as a signed 32-bit integer:
    to_signed32(0xFFFFFFFF) == -1, to_signed32(2**31) == -2**31."""
    raise NotImplementedError


def add_without_plus(a, b):
    """Add two signed 32-bit ints using only bit operations (no + or -) and
    return the wrapped signed 32-bit result, like C int addition:
    add_without_plus(2**31 - 1, 1) == -2**31."""
    raise NotImplementedError


def can_make_sum(nums, target):
    """True if some subset of the non-negative ints nums sums to target. Use a
    big int as a bitset: bit s set means sum s is reachable."""
    raise NotImplementedError


# ---------------------------------------------------------------- tests (don't edit)

def _wrap32(v):
    return (v + 2**31) % 2**32 - 2**31


def test_get_bit():
    assert get_bit(0b1010, 1) == 1 and get_bit(0b1010, 0) == 0 and get_bit(0b1010, 9) == 0
    rng = random.Random(4)
    for _ in range(300):
        x, i = rng.randint(0, 2**40), rng.randint(0, 45)
        assert get_bit(x, i) == (x // 2**i) % 2, f"get_bit({x}, {i})"


def test_set_bit():
    assert set_bit(0b1000, 1) == 0b1010 and set_bit(0, 5) == 32
    assert set_bit(0b1010, 1) == 0b1010, "setting a set bit changes nothing: use |, not ^ or +"
    rng = random.Random(4)
    for _ in range(300):
        x, i = rng.randint(0, 2**40), rng.randint(0, 45)
        assert set_bit(x, i) == (x if (x // 2**i) % 2 else x + 2**i), f"set_bit({x}, {i})"


def test_clear_bit():
    assert clear_bit(0b1010, 1) == 0b1000 and clear_bit(0b1111, 0) == 0b1110
    assert clear_bit(0b1000, 1) == 0b1000, "clearing a clear bit changes nothing: use & ~(1 << i), not ^"
    rng = random.Random(4)
    for _ in range(300):
        x, i = rng.randint(0, 2**40), rng.randint(0, 45)
        assert clear_bit(x, i) == (x - 2**i if (x // 2**i) % 2 else x), f"clear_bit({x}, {i})"


def test_toggle_bit():
    assert toggle_bit(0b1010, 0) == 0b1011 and toggle_bit(0b1010, 1) == 0b1000
    rng = random.Random(4)
    for _ in range(300):
        x, i = rng.randint(0, 2**30), rng.randint(0, 35)
        assert toggle_bit(x, i) != x and toggle_bit(toggle_bit(x, i), i) == x, f"toggle_bit({x}, {i})"


def test_lowest_set_bit():
    assert lowest_set_bit(12) == 4 and lowest_set_bit(1) == 1 and lowest_set_bit(0) == 0
    assert lowest_set_bit(2**100) == 2**100 and lowest_set_bit(2**100 + 2**7) == 2**7
    for x in range(1, 3000):
        assert lowest_set_bit(x) == next(1 << i for i in range(20) if x >> i & 1), f"lowest_set_bit({x})"


def test_is_power_of_two():
    assert [x for x in range(-8, 70) if is_power_of_two(x)] == [1, 2, 4, 8, 16, 32, 64], \
        "0 & (0 - 1) == 0 too: rule out zero and negatives"
    assert is_power_of_two(2**100) and not is_power_of_two(2**100 + 2**50)


def test_popcount():
    assert popcount(0) == 0 and popcount(1) == 1 and popcount(255) == 8
    assert popcount(2**200 - 1) == 200
    rng = random.Random(4)
    for _ in range(500):
        x = rng.randint(0, 2**64)
        assert popcount(x) == bin(x).count('1'), f"popcount({x})"


def test_single_unpaired():
    assert single_unpaired([4, 1, 2, 1, 2]) == 4 and single_unpaired([7]) == 7
    assert single_unpaired([-3, 5, 5]) == -3 and single_unpaired([0, 9, 9]) == 0
    rng = random.Random(4)
    for _ in range(50):
        pool = rng.sample(range(-1000, 1000), 30)
        nums = pool[1:] * 2 + [pool[0]]
        rng.shuffle(nums)
        assert single_unpaired(nums) == pool[0]


def test_range_xor():
    assert range_xor([3, 8, 2, 6], [(0, 0), (0, 3), (1, 2), (3, 3)]) == [3, 15, 10, 6]
    assert range_xor([5], []) == []
    rng = random.Random(4)
    nums = [rng.randint(0, 10**6) for _ in range(200)]
    queries = [tuple(sorted((rng.randrange(200), rng.randrange(200)))) for _ in range(500)]
    want = [functools.reduce(operator.xor, nums[l:r + 1]) for l, r in queries]
    assert range_xor(nums, queries) == want


def test_subsets():
    assert subsets('ab') == [[], ['a'], ['b'], ['a', 'b']]
    assert subsets('abc') == [[], ['a'], ['b'], ['a', 'b'], ['c'], ['a', 'c'], ['b', 'c'], ['a', 'b', 'c']]
    assert subsets([]) == [[]]
    out = subsets(list(range(10)))
    assert len(out) == 1024 and out[5] == [0, 2] and out[1023] == list(range(10))


def test_submasks():
    assert submasks(0b101) == [0b101, 0b100, 0b001]
    assert submasks(0) == [] and submasks(1) == [1]
    for mask in (0b11111, 0b101010, 0b1000001):
        assert submasks(mask) == [s for s in range(mask, 0, -1) if s & ~mask == 0], f"submasks({bin(mask)})"


def test_to_signed32():
    assert to_signed32(0xFFFFFFFF) == -1 and to_signed32(2**31) == -2**31
    assert to_signed32(2**31 - 1) == 2**31 - 1 and to_signed32(5) == 5 and to_signed32(0) == 0
    assert to_signed32(2**32 + 7) == 7, "only the low 32 bits count"
    assert to_signed32(-1) == -1 and to_signed32(-2**31 - 1) == 2**31 - 1


def test_add_without_plus():
    for a, b in ((1, 2), (-1, 1), (-5, -7), (0, 0), (2**31 - 1, 1), (-2**31, -1)):
        assert add_without_plus(a, b) == _wrap32(a + b), f"add_without_plus({a}, {b})"
    rng = random.Random(4)
    for _ in range(300):
        a, b = rng.randint(-2**31, 2**31 - 1), rng.randint(-2**31, 2**31 - 1)
        assert add_without_plus(a, b) == _wrap32(a + b), f"add_without_plus({a}, {b})"


def test_can_make_sum():
    assert can_make_sum([3, 5, 9], 14) and not can_make_sum([3, 5, 9], 13)
    assert can_make_sum([3, 5, 9], 0) and can_make_sum([], 0) and not can_make_sum([], 1)
    assert not can_make_sum([2, 4], -2), "a negative target is unreachable (and >> by a negative count raises)"
    rng = random.Random(4)
    for _ in range(200):
        nums = [rng.randint(0, 12) for _ in range(rng.randint(0, 7))]
        target = rng.randint(0, 40)
        want = any(sum(c) == target for r in range(len(nums) + 1) for c in itertools.combinations(nums, r))
        assert can_make_sum(nums, target) == want, f"can_make_sum({nums}, {target})"
    assert can_make_sum([1000] * 100 + [1], 50001)
