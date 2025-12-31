from signum import sign

from decimal import Decimal
from fractions import Fraction
from math import nan, inf
import os
import re
import sympy
import sys
import time

# Detecting version
def detect_version():
    try:
        sign(0, preprocess=None)
        return("1.1.0+")
    except TypeError:
        return("1.0.2")

class MyNumber: # __float__ is absent
    def __init__(self, value):
        self.value = value
    def __gt__(self, other):
        return self.value > other
    def __lt__(self, other):
        return self.value < other
    def __eq__(self, other):
        return self.value == other
    def __repr__(self):
        return f'MyNumber({self.value})'

class ExplodingNumber: # Instead of reach comprisons, raises exceptions; __float__ explodes also
    def __init__(self, value):
        self.value = value
    def __gt__(self, other):
        raise RuntimeError("Boom!")
    def __lt__(self, other):
        raise RuntimeError("Boom!")
    def __eq__(self, other):
        raise RuntimeError("Boom!")
    def __float__(self):
        raise RuntimeError("Boom!")
    def __repr__(self):
        return f'ExplodingNumber({self.value})'

class NotImplementedNumber: # Stubs for future implemetation; __float__ is implemented
    def __init__(self, value):
        self.value = value
    def __gt__(self, other):
        return NotImplemented
    def __lt__(self, other):
        return NotImplemented
    def __eq__(self, other):
        return NotImplemented
    def __float__(self):
        return float(self.value)
    def __repr__(self):
        return f'NotImplementedNumber({self.value})'

UTF8 = 'utf-8'
MAX_PASSES = 100000

original_stdout_params = {'encoding': sys.stdout.encoding, 'errors': sys.stdout.errors}
original_stderr_params = {'encoding': sys.stderr.encoding, 'errors': sys.stderr.errors}
# Switch sys.stdout and sys.stderr to 'utf-8' encoding
sys.stdout.reconfigure(encoding=UTF8)
sys.stderr.reconfigure(encoding=UTF8)

# Reserve variables
original_stdout = None
original_stderr = None

start_time = None

for _ in range(MAX_PASSES + 1):
    (sign(-5))
    (sign(-1))
    (sign(0))
    (sign(1))
    (sign(5))
    (sign(True))
    (sign(False))
    (sign(10**1000))
    (sign(-10**1000))
    (sign(10**1000-10**1000))
    (sign(-5.0))
    (sign(-1.0))
    (sign(0.0))
    (sign(1.0))
    (sign(5.0))
    (sign(float('-0.0')))
    (sign(float('+0.0')))
    (sign(-inf))
    (sign(inf))
    (sign(float('-nan')))
    (sign(nan))
    (sign(0.0*nan))
    (sign(Fraction(-5, 2)))
    (sign(Fraction(-1, 2)))
    (sign(Fraction(0, 2)))
    (sign(Fraction(1, 2)))
    (sign(Fraction(5, 2)))
    (sign(Decimal(-5.5)))
    (sign(Decimal(-1.5)))
    (sign(Decimal(0.0)))
    (sign(Decimal(1.5)))
    (sign(Decimal(5.5)))
    (sign(Decimal('NaN')))
    x_sym = sympy.Symbol('x')
    expr = x_sym
    val = expr.subs(x_sym, -3.14)
    (sign(val))
    (sign(sympy.Rational(3, 4)))
    (sign(sympy.nan))
    (sign(MyNumber(-5)))
    (sign(MyNumber(-1)))
    (sign(MyNumber(0)))
    (sign(MyNumber(1)))
    (sign(MyNumber(5.1)))
    try:
        (sign(MyNumber(nan)))
    except TypeError as e:
        (e)
    try:
        (sign())
    except TypeError as e:
        (e)
    try:
        (sign(-1, 0))
    except TypeError as e:
        (e)
    try:
        (sign(-1, 0, 1))
    except TypeError as e:
        (e)
    try:
        (sign(-1, 0, 1, 5))
    except TypeError as e:
        (e)
    try:
        (sign(ExplodingNumber(-3.14)))
    except TypeError as e:
        (e)
    try:
        (sign(NotImplementedNumber(-3.14)))
    except TypeError as e:
        (e)
    tests = [None, '5.0', 'nan', 'number 5', -1+1j, [-8.75], {-3.14},]
    for x in tests:
        try:
            (sign(x))
        except TypeError as e:
            (e)
    if start_time is None: # The very first pass to warm Python
        start_time = time.perf_counter()
        # Create devnull
        f = open(os.devnull, 'w')
        # Save and switch sys std flows
        print('', end='', file=sys.stdout, flush=True); original_stdout, sys.stdout = sys.stdout, f
        print('', end='', file=sys.stderr, flush=True); original_stderr, sys.stderr = sys.stderr, f

# Restore sys std flows
print('', end='', file=sys.stdout, flush=True); sys.stdout = original_stdout
print('', end='', file=sys.stderr, flush=True); sys.stderr = original_stderr

version = detect_version()
duration = time.perf_counter() - start_time
print(f'\nSuccess of {version}: 55 tests passed {MAX_PASSES} times in {duration:>9.4f}s.')

# Restore stdout and stderr
sys.stdout.reconfigure(**original_stdout_params)
sys.stderr.reconfigure(**original_stderr_params)
