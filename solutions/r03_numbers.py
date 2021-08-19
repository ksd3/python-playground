"""R03 - Integers, floats, math (reference solutions)

Compare after you've made your own attempt. Run: python check.py 3 -s
"""
import math
import string

PREDICT = r"""
>>> -7 // 2, -7 % 2
(-4, 1)
>>> 7 // -2, 7 % -2
(-4, -1)

>>> int(-7 / 2), divmod(-7, 2)
(-3, (-4, 1))
>>> int(3.9), int(-3.9)
(3, -3)

>>> -(-7 // 2), (7 + 2 - 1) // 2
(4, 4)

>>> (3 - 5) % 7, -7 % 3, abs(-7) % 3
(5, 2, 1)

>>> 10 / 2, 10 // 2
(5.0, 5)
>>> 7.0 / 0
ZeroDivisionError

>>> round(0.5), round(1.5), round(2.5), round(3.5)
(0, 2, 2, 4)
>>> round(2.675, 2)
2.67

>>> 0.1 + 0.2
0.30000000000000004
>>> 0.1 + 0.2 == 0.3, math.isclose(0.1 + 0.2, 0.3)
(False, True)

>>> total = 0.0
>>> for _ in range(10):
...     total += 0.1
>>> total, math.fsum([0.1] * 10)
(0.9999999999999999, 1.0)

>>> float(2**53 + 1) == float(2**53)
True
>>> 2**64
18446744073709551616

>>> int(math.sqrt(10**16 - 1)), math.isqrt(10**16 - 1)
(100000000, 99999999)

>>> pow(2, 10, 1000), pow(3, -1, 7)
(24, 5)

>>> float('inf') > 10**100, math.inf - math.inf
(True, nan)
>>> float('nan') == float('nan')
False

>>> int('ff', 16), int('101', 2), int(' 42 ')
(255, 5, 42)
>>> int('3.0')
ValueError

>>> format(10, 'b'), f'{5:08b}', bin(10), hex(255)
('1010', '00000101', '0b1010', '0xff')

>>> math.gcd(12, 18), math.lcm(4, 6), math.gcd(0, 5)
(6, 12, 5)
>>> math.comb(5, 2), math.perm(5, 2), math.factorial(5)
(10, 20, 120)

>>> from fractions import Fraction
>>> Fraction(1, 3) + Fraction(1, 6)
Fraction(1, 2)
>>> Fraction(6, -4)
Fraction(-3, 2)
"""

_DIGITS = string.digits + string.ascii_lowercase


def trunc_div(a, b):
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q


def ceil_div(a, b):
    return -(-a // b)


def fast_pow(a, b, m):
    result, a = 1 % m, a % m
    while b:
        if b & 1:
            result = result * a % m
        a = a * a % m
        b >>= 1
    return result


class Combinatorics:
    def __init__(self, limit, mod=10**9 + 7):
        self.mod = mod
        self.fact = [1] * (limit + 1)
        for i in range(1, limit + 1):
            self.fact[i] = self.fact[i - 1] * i % mod
        self.inv = [1] * (limit + 1)
        self.inv[limit] = pow(self.fact[limit], mod - 2, mod)  # Fermat, since mod is prime
        for i in range(limit, 0, -1):
            self.inv[i - 1] = self.inv[i] * i % mod

    def comb(self, n, r):
        if r < 0 or r > n:
            return 0
        return self.fact[n] * self.inv[r] % self.mod * self.inv[n - r] % self.mod

    def perm(self, n, r):
        if r < 0 or r > n:
            return 0
        return self.fact[n] * self.inv[n - r] % self.mod


def gcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    if a == 0 or b == 0:
        return 0
    return abs(a) // gcd(a, b) * abs(b)


def is_prime(n):
    if n < 2:
        return False
    for d in range(2, math.isqrt(n) + 1):
        if n % d == 0:
            return False
    return True


def primes_up_to(n):
    if n < 2:
        return []
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, math.isqrt(n) + 1):
        if sieve[i]:
            sieve[i * i::i] = [False] * len(range(i * i, n + 1, i))
    return [i for i, is_p in enumerate(sieve) if is_p]


def factorize(n):
    out, p = [], 2
    while p * p <= n:
        if n % p == 0:
            e = 0
            while n % p == 0:
                n //= p
                e += 1
            out.append((p, e))
        p += 1
    if n > 1:
        out.append((n, 1))
    return out


def same_ratio(a, b, c, d):
    return a * d == b * c


def slope_key(p, q):
    dy, dx = q[1] - p[1], q[0] - p[0]
    if dx == 0:
        return (1, 0)
    if dy == 0:
        return (0, 1)
    g = math.gcd(dy, dx)
    dy, dx = dy // g, dx // g
    if dx < 0:
        dy, dx = -dy, -dx
    return (dy, dx)


def digits(n):
    out = [n % 10]
    n //= 10
    while n:
        out.append(n % 10)
        n //= 10
    return out[::-1]


def to_base(n, base):
    if n == 0:
        return '0'
    sign, n = ('-', -n) if n < 0 else ('', n)
    out = []
    while n:
        n, r = divmod(n, base)
        out.append(_DIGITS[r])
    return sign + ''.join(reversed(out))
