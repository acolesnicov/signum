from signum import fastsign as fastsign
from testing import get_passes, MyNumber as _MyNumber, set_high_priority, success, OutputUTF8

from decimal import Decimal
from fractions import Fraction
from math import nan, inf
import sympy
import time

MAX_PASSES = get_passes(__file__)

# Switch sys.stdout and sys.stderr to 'utf-8' encoding
outflows = OutputUTF8()
outflows.set_utf8()

start_time = None

print(f'***** Test: {__file__}')
print(f'MAX_PASSES: {MAX_PASSES}')
print(f'*** {set_high_priority()} ***\n')
for _ in range(MAX_PASSES + 1):
    (fastsign(-5))
    (fastsign(-1))
    (fastsign(0))
    (fastsign(1))
    (fastsign(5))
    (fastsign(True))
    (fastsign(False))
    (fastsign(10**1000))
    (fastsign(-10**1000))
    (fastsign(10**1000-10**1000))
    (fastsign(-5.0))
    (fastsign(-1.0))
    (fastsign(0.0))
    (fastsign(1.0))
    (fastsign(5.0))
    (fastsign(float('-0.0')))
    (fastsign(float('+0.0')))
    (fastsign(-inf))
    (fastsign(inf))
    (fastsign(float('-nan')))
    (fastsign(nan))
    (fastsign(0.0*nan))
    (fastsign(Fraction(-5, 2)))
    (fastsign(Fraction(-1, 2)))
    (fastsign(Fraction(0, 2)))
    (fastsign(Fraction(1, 2)))
    (fastsign(Fraction(5, 2)))
    (fastsign(Decimal(-5.5)))
    (fastsign(Decimal(-1.5)))
    (fastsign(Decimal(0.0)))
    (fastsign(Decimal(1.5)))
    (fastsign(Decimal(5.5)))
    (fastsign(Decimal('NaN')))
    x_sym = sympy.Symbol('x')
    expr = x_sym
    val = expr.subs(x_sym, -3.14)
    (fastsign(val))
    (fastsign(sympy.Rational(3, 4)))
    (fastsign(sympy.nan))
    (fastsign(_MyNumber(-5)))
    (fastsign(_MyNumber(-1)))
    (fastsign(_MyNumber(0)))
    (fastsign(_MyNumber(1)))
    (fastsign(_MyNumber(5.1)))

    if start_time is None: # The very first pass to warm Python
        start_time = time.perf_counter()

print(f'{success(41, s_cnt=None, start_time=start_time, passes=MAX_PASSES)}\n')

# Restore stdout and stderr
outflows.reset_from_utf8()
