"""R04 - Bit manipulation (reference solutions)

Compare after you've made your own attempt. Run: python check.py 4 -s
"""

PREDICT = r"""
>>> ~5, ~-1, -~5
(-6, 0, 6)

>>> -1 >> 1, -8 >> 1, 8 >> 1
(-1, -4, 4)

>>> bin(5), bin(-5)
('0b101', '-0b101')

>>> -5 & 0xFF, 5 & -5
(251, 1)

>>> 12 & -12, 12 & 11, 12 | 11
(4, 8, 15)

>>> (8).bit_length(), (0).bit_length(), (-8).bit_length()
(4, 0, 4)

>>> bin(255).count('1'), (255).bit_count()
(8, 8)

>>> 1 << 10, 3 << 2, 1 << 2 + 1
(1024, 12, 8)

>>> 6 & 1 == 0
True

>>> 5 ^ 3, 5 ^ 5, 5 ^ 0
(6, 0, 5)
>>> functools.reduce(operator.xor, [4, 1, 2, 1, 2])
4

>>> [i for i in range(4) if 0b1010 >> i & 1]
[1, 3]

>>> int('1011', 2), f'{11:b}', f'{11:08b}', format(11, '#x')
(11, '1011', '00001011', '0xb')

>>> [i ^ (i >> 1) for i in range(8)]
[0, 1, 3, 2, 6, 7, 5, 4]

>>> mask, sub, out = 0b101, 0b101, []
>>> while sub:
...     out.append(bin(sub))
...     sub = (sub - 1) & mask
>>> out
['0b101', '0b100', '0b1']

>>> bits = 1
>>> for x in [3, 5]:
...     bits |= bits << x
>>> bin(bits), [s for s in range(9) if bits >> s & 1]
('0b100101001', [0, 3, 5, 8])

>>> x = 0xFFFFFFFF
>>> x - (1 << 32) if x >> 31 else x
-1
>>> -3 & 0xFFFFFFFF
4294967293

>>> 1 << 64, (1 << 64) - 1 == 2**64 - 1
(18446744073709551616, True)
"""

_MASK = 0xFFFFFFFF


def get_bit(x, i):
    return x >> i & 1


def set_bit(x, i):
    return x | 1 << i


def clear_bit(x, i):
    return x & ~(1 << i)


def toggle_bit(x, i):
    return x ^ 1 << i


def lowest_set_bit(x):
    return x & -x


def is_power_of_two(x):
    return x > 0 and x & (x - 1) == 0


def popcount(x):
    count = 0
    while x:
        x &= x - 1  # drops the lowest set bit
        count += 1
    return count


def single_unpaired(nums):
    acc = 0
    for x in nums:
        acc ^= x
    return acc


def range_xor(nums, queries):
    prefix = [0]
    for x in nums:
        prefix.append(prefix[-1] ^ x)
    return [prefix[r + 1] ^ prefix[l] for l, r in queries]


def subsets(items):
    items = list(items)
    n = len(items)
    return [[items[i] for i in range(n) if mask >> i & 1] for mask in range(1 << n)]


def submasks(mask):
    out, sub = [], mask
    while sub:
        out.append(sub)
        sub = (sub - 1) & mask
    return out


def to_signed32(x):
    x &= _MASK
    return x - (1 << 32) if x >= 1 << 31 else x


def add_without_plus(a, b):
    a, b = a & _MASK, b & _MASK
    while b:
        a, b = (a ^ b) & _MASK, (a & b) << 1 & _MASK  # sum without carries, then the carries
    return a if a <= 0x7FFFFFFF else ~(a ^ _MASK)  # back to signed without subtracting


def can_make_sum(nums, target):
    if target < 0:
        return False
    bits = 1
    for x in nums:
        bits |= bits << x
    return bool(bits >> target & 1)
