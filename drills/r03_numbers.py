"""R03 - Integers, floats, math

// and % floor toward negative infinity: -7 // 2 == -4 and -7 % 2 == 1, and with
a positive modulus % is never negative. int(a / b) truncates instead, but it
goes through a float, so it's wrong for huge ints. Ints never overflow; floats
carry 53 bits, so compare them with math.isclose, cross-multiply fractions,
and use math.isqrt rather than int(math.sqrt(n)). pow(a, b, m) is fast modular
power and pow(a, -1, m) a modular inverse (3.8+); round() sends halves to even.
Since 3.12, sum() of floats compensates for rounding; a += loop never does.

Part 1 - Predict. Each block in PREDICT is a REPL session. Replace every ???
with exactly what Python prints: expression values are echoed the way the REPL
echoes them, and a line that raises prints just the exception name (TypeError).

Part 2 - Drills. Implement every function until `python check.py 3` is green.
Don't edit the tests at the bottom; add your own test_* functions if you like.

Unlocks: "answer modulo 10**9 + 7", counting and combinatorics, geometry and
slope hashing, digit manipulation, and division in expression evaluators.
"""
import math
import random
from fractions import Fraction

PREDICT = r"""
>>> -7 // 2, -7 % 2
???
>>> 7 // -2, 7 % -2
???

>>> int(-7 / 2), divmod(-7, 2)
???
>>> int(3.9), int(-3.9)
???

>>> -(-7 // 2), (7 + 2 - 1) // 2
???

>>> (3 - 5) % 7, -7 % 3, abs(-7) % 3
???

>>> 10 / 2, 10 // 2
???
>>> 7.0 / 0
???

>>> round(0.5), round(1.5), round(2.5), round(3.5)
???
>>> round(2.675, 2)
???

>>> 0.1 + 0.2
???
>>> 0.1 + 0.2 == 0.3, math.isclose(0.1 + 0.2, 0.3)
???

>>> total = 0.0
>>> for _ in range(10):
...     total += 0.1
>>> total, math.fsum([0.1] * 10)
???

>>> float(2**53 + 1) == float(2**53)
???
>>> 2**64
???

>>> int(math.sqrt(10**16 - 1)), math.isqrt(10**16 - 1)
???

>>> pow(2, 10, 1000), pow(3, -1, 7)
???

>>> float('inf') > 10**100, math.inf - math.inf
???
>>> float('nan') == float('nan')
???

>>> int('ff', 16), int('101', 2), int(' 42 ')
???
>>> int('3.0')
???

>>> format(10, 'b'), f'{5:08b}', bin(10), hex(255)
???

>>> math.gcd(12, 18), math.lcm(4, 6), math.gcd(0, 5)
???
>>> math.comb(5, 2), math.perm(5, 2), math.factorial(5)
???

>>> from fractions import Fraction
>>> Fraction(1, 3) + Fraction(1, 6)
???
>>> Fraction(6, -4)
???
"""


# ---------------------------------------------------------------- drills

def trunc_div(a, b):
    """Integer division rounding toward zero (like C), exact even for huge
    ints, so no floats: trunc_div(-7, 2) == -3, trunc_div(7, 2) == 3."""
    raise NotImplementedError


def ceil_div(a, b):
    """Integer division rounding up (toward +infinity), exact for any signs:
    ceil_div(7, 2) == 4, ceil_div(-7, 2) == -3."""
    raise NotImplementedError


def fast_pow(a, b, m):
    """Return a**b % m for b >= 0 and m >= 1 by binary exponentiation, in
    O(log b) multiplications and without pow() or **. Same results as
    pow(a, b, m), including fast_pow(7, 0, 1) == 0."""
    raise NotImplementedError


class Combinatorics:
    """Precompute factorials and inverse factorials modulo the prime `mod` up
    to `limit` in O(limit). Then comb(n, r) and perm(n, r), both mod `mod`,
    take O(1) for 0 <= n <= limit. An r outside 0..n gives 0."""

    def __init__(self, limit, mod=10**9 + 7):
        raise NotImplementedError

    def comb(self, n, r):
        raise NotImplementedError

    def perm(self, n, r):
        raise NotImplementedError


def gcd(a, b):
    """Greatest common divisor by Euclid's algorithm (not math.gcd). The
    result is never negative, and gcd(0, 0) == 0."""
    raise NotImplementedError


def lcm(a, b):
    """Least common multiple via gcd, never negative; 0 if either is 0
    (including lcm(0, 0)). Divide before multiplying."""
    raise NotImplementedError


def is_prime(n):
    """Trial division by d = 2 .. isqrt(n). Anything below 2 is not prime."""
    raise NotImplementedError


def primes_up_to(n):
    """All primes <= n in increasing order, by the Sieve of Eratosthenes.
    primes_up_to(10) == [2, 3, 5, 7]"""
    raise NotImplementedError


def factorize(n):
    """Prime factorization of n >= 1 by trial division, as sorted
    (prime, exponent) pairs: factorize(360) == [(2, 3), (3, 2), (5, 1)],
    factorize(1) == []."""
    raise NotImplementedError


def same_ratio(a, b, c, d):
    """True if a/b == c/d exactly (b and d are non-zero ints). Integers only:
    floats can't tell (10**18 + 1)/10**18 from 1/1."""
    raise NotImplementedError


def slope_key(p, q):
    """A hashable key (dy, dx) for the slope of the line through two distinct
    integer points, reduced by gcd and normalized so equal slopes give equal
    keys: dx > 0, vertical lines give (1, 0), horizontal lines give (0, 1).
    slope_key((0, 0), (2, 4)) == slope_key((1, 1), (0, -1)) == (2, 1)"""
    raise NotImplementedError


def digits(n):
    """Decimal digits of n >= 0, most significant first, using % and //
    (not str): digits(1203) == [1, 2, 0, 3], digits(0) == [0]."""
    raise NotImplementedError


def to_base(n, base):
    """n written in base 2..36 with digits 0-9 then a-z, no leading zeros, and
    a leading '-' for negatives: to_base(255, 16) == 'ff', to_base(0, 7) == '0',
    to_base(-5, 2) == '-101'."""
    raise NotImplementedError


# ---------------------------------------------------------------- tests (don't edit)

def _primes(limit):
    return [n for n in range(2, limit + 1) if all(n % d for d in range(2, math.isqrt(n) + 1))]


def _slope(p, q):
    dx, dy = q[0] - p[0], q[1] - p[1]
    return 'vertical' if dx == 0 else Fraction(dy, dx)


def test_trunc_div():
    for a, b, want in ((7, 2, 3), (-7, 2, -3), (7, -2, -3), (-7, -2, 3), (6, 3, 2), (0, 5, 0)):
        assert trunc_div(a, b) == want, f"trunc_div({a}, {b}) should be {want}"
    assert trunc_div(10**30 + 7, 3) == 333333333333333333333333333335, \
        "int(a / b) goes through a float and loses precision for huge ints"
    assert trunc_div(-(10**30) - 7, 3) == -333333333333333333333333333335
    rng = random.Random(3)
    for _ in range(500):
        a, b = rng.randint(-10**6, 10**6), rng.choice((-1, 1)) * rng.randint(1, 1000)
        assert trunc_div(a, b) == math.trunc(Fraction(a, b)), f"trunc_div({a}, {b})"


def test_ceil_div():
    for a, b, want in ((7, 2, 4), (-7, 2, -3), (7, -2, -3), (-7, -2, 4), (6, 3, 2), (0, 5, 0)):
        assert ceil_div(a, b) == want, f"ceil_div({a}, {b}) should be {want}"
    assert ceil_div(10**30 + 7, 3) == 333333333333333333333333333336
    rng = random.Random(3)
    for _ in range(500):
        a, b = rng.randint(-10**6, 10**6), rng.choice((-1, 1)) * rng.randint(1, 1000)
        assert ceil_div(a, b) == math.ceil(Fraction(a, b)), f"ceil_div({a}, {b})"


def test_fast_pow():
    assert fast_pow(2, 10, 1000) == 24 and fast_pow(3, 0, 7) == 1
    assert fast_pow(7, 0, 1) == 0, "1 % 1 == 0: reduce the starting 1 too"
    rng = random.Random(3)
    for _ in range(300):
        a, b, m = rng.randint(0, 10**9), rng.randint(0, 10**18), rng.randint(1, 10**9 + 7)
        assert fast_pow(a, b, m) == pow(a, b, m), f"fast_pow({a}, {b}, {m})"


def test_Combinatorics():
    mod = 10**9 + 7
    c = Combinatorics(1000)
    assert c.comb(5, 2) == 10 and c.comb(5, 0) == 1 and c.comb(5, 5) == 1 and c.comb(0, 0) == 1
    assert c.comb(5, 6) == 0 and c.comb(5, -1) == 0, "an r outside 0..n gives 0"
    assert c.perm(5, 2) == 20 and c.perm(5, 0) == 1 and c.perm(5, 6) == 0
    rng = random.Random(3)
    for _ in range(300):
        n = rng.randint(0, 1000)
        r = rng.randint(-2, n + 2)
        want = math.comb(n, r) % mod if 0 <= r <= n else 0
        assert c.comb(n, r) == want, f"comb({n}, {r})"
    big = Combinatorics(10**5, 998244353)
    assert big.comb(10**5, 5 * 10**4) == math.comb(10**5, 5 * 10**4) % 998244353
    assert big.perm(10**5, 3) == 10**5 * (10**5 - 1) * (10**5 - 2) % 998244353


def test_gcd():
    assert gcd(12, 18) == 6 and gcd(18, 12) == 6 and gcd(7, 0) == 7 and gcd(0, 0) == 0
    assert gcd(-12, 18) == 6 and gcd(12, -18) == 6, "the result should never be negative"
    rng = random.Random(3)
    for _ in range(500):
        a, b = rng.randint(-10**12, 10**12), rng.randint(-10**12, 10**12)
        assert gcd(a, b) == math.gcd(a, b), f"gcd({a}, {b})"


def test_lcm():
    assert lcm(4, 6) == 12 and lcm(3, 5) == 15 and lcm(-4, 6) == 12
    assert lcm(0, 5) == 0 and lcm(0, 0) == 0, "gcd(0, 0) is 0: don't divide by it"
    rng = random.Random(3)
    for _ in range(300):
        a, b = rng.randint(1, 10**9), rng.randint(1, 10**9)
        assert lcm(a, b) == a * b // math.gcd(a, b), f"lcm({a}, {b})"


def test_is_prime():
    assert [n for n in range(-5, 3000) if is_prime(n)] == _primes(2999)
    for square in (4, 9, 49, 121, 10007**2):
        assert not is_prime(square), f"{square}: check divisors up to AND including isqrt(n)"
    assert is_prime(10**9 + 7) and is_prime(2**31 - 1) and not is_prime(10**9 + 1)


def test_primes_up_to():
    assert primes_up_to(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    assert primes_up_to(1) == [] and primes_up_to(0) == [] and primes_up_to(2) == [2]
    assert primes_up_to(3000) == _primes(3000)
    ps = primes_up_to(10**6)
    assert len(ps) == 78498 and ps[-1] == 999983


def test_factorize():
    assert factorize(360) == [(2, 3), (3, 2), (5, 1)]
    assert factorize(1) == [] and factorize(2) == [(2, 1)] and factorize(97) == [(97, 1)]
    assert factorize(600851475143) == [(71, 1), (839, 1), (1471, 1), (6857, 1)]
    assert factorize(2**40 * 3) == [(2, 40), (3, 1)]
    assert factorize(2 * 999983) == [(2, 1), (999983, 1)], "a leftover n > 1 after the loop is prime"
    primes = set(_primes(3000))
    for n in range(2, 3000):
        fs = factorize(n)
        assert math.prod(p**e for p, e in fs) == n, f"factorize({n})"
        assert all(p in primes for p, _ in fs) and [p for p, _ in fs] == sorted({p for p, _ in fs})


def test_same_ratio():
    assert same_ratio(1, 3, 2, 6) and not same_ratio(1, 3, 1, 4)
    assert same_ratio(-1, 2, 1, -2) and same_ratio(0, 5, 0, -3)
    assert not same_ratio(10**18 + 1, 10**18, 1, 1), "floats can't tell these apart: cross-multiply"
    rng = random.Random(3)
    for _ in range(500):
        a, b, c, d = (rng.randint(-20, 20) for _ in range(4))
        if b and d:
            assert same_ratio(a, b, c, d) == (Fraction(a, b) == Fraction(c, d)), \
                f"same_ratio({a}, {b}, {c}, {d})"


def test_slope_key():
    assert slope_key((0, 0), (2, 4)) == slope_key((1, 1), (0, -1)) == (2, 1)
    assert slope_key((0, 0), (0, 5)) == slope_key((3, 3), (3, -1)) == (1, 0), "vertical lines"
    assert slope_key((0, 0), (5, 0)) == slope_key((2, 7), (-1, 7)) == (0, 1), "horizontal lines"
    assert slope_key((0, 0), (1, -1)) == slope_key((0, 0), (-1, 1)) == (-1, 1), "normalize the sign"
    hash(slope_key((0, 0), (1, 2)))
    rng = random.Random(3)
    pts = [(rng.randint(-6, 6), rng.randint(-6, 6)) for _ in range(25)]
    pairs = [(p, q) for p in pts for q in pts if p != q]
    rng.shuffle(pairs)
    for p, q in pairs[:60]:
        for r, s in pairs[60:160]:
            same = slope_key(p, q) == slope_key(r, s)
            assert same == (_slope(p, q) == _slope(r, s)), f"slope_key({p}, {q}) vs ({r}, {s})"


def test_digits():
    assert digits(0) == [0] and digits(7) == [7] and digits(1203) == [1, 2, 0, 3]
    assert digits(10**20) == [1] + [0] * 20
    for n in range(0, 5000, 7):
        assert digits(n) == [int(ch) for ch in str(n)], f"digits({n})"


def test_to_base():
    assert to_base(255, 16) == 'ff' and to_base(5, 2) == '101' and to_base(0, 7) == '0'
    assert to_base(-5, 2) == '-101' and to_base(35, 36) == 'z' and to_base(16, 16) == '10'
    rng = random.Random(3)
    for _ in range(500):
        n, base = rng.randint(-10**12, 10**12), rng.randint(2, 36)
        s = to_base(n, base)
        assert int(s, base) == n, f"to_base({n}, {base}) gave {s!r}"
        assert s == '0' or s.lstrip('-')[0] != '0', f"to_base({n}, {base}) has a leading zero"
