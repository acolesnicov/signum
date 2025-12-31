from signum import sign

from decimal import Decimal
from fractions import Fraction
from math import nan, inf
import os
import re
import sympy
import sys
import time

def trace(pcnt, cnt, scnt):
    delta = cnt - pcnt
    pl = 's' if delta != 1 else ' '
    print(f"   --- {delta:2} test{pl} for Sec. {scnt:2} passed, total {cnt:3} tests passed")

# Functions used to preprocess
def n_extract(s):
    if isinstance(s, str):
        match = numeric_finder.search(s)
        return (float(match.group()),) if match else None
    return None

def c_prep(z):
    if z == 0 or not isinstance(z, complex): return None
    # complex z != 0
    return (0, z/abs(z))

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
EPS = 1e-9
MAX_PASSES = 10000

original_stdout_params = {'encoding': sys.stdout.encoding, 'errors': sys.stdout.errors}
original_stderr_params = {'encoding': sys.stderr.encoding, 'errors': sys.stderr.errors}
# Switch sys.stdout and sys.stderr to 'utf-8' encoding
sys.stdout.reconfigure(encoding=UTF8)
sys.stderr.reconfigure(encoding=UTF8)

# Reserve variables
original_stdout = None
original_stderr = None

# Detecting version
version = detect_version()
# Uncomment to pass restricted test set for comparison
# version = "1.0.2"

start_time = None

for _ in range(MAX_PASSES + 1):
    s_cnt = 0
    counter = 0

    s_cnt += 1; prev_counter = counter
    print(f'{s_cnt:2} --- int')
    print("sign(-5):", sign(-5)); counter += 1
    print("sign(-1):", sign(-1)); counter += 1
    print("sign(0):", sign(0)); counter += 1
    print("sign(1):", sign(1)); counter += 1
    print("sign(5):", sign(5)); counter += 1

    trace(prev_counter, counter, s_cnt)

    s_cnt += 1; prev_counter = counter
    print(f'\n{s_cnt:2} --- bool')
    print("sign(True):", sign(True)); counter += 1
    print("sign(False):", sign(False)); counter += 1

    trace(prev_counter, counter, s_cnt)

    s_cnt += 1; prev_counter = counter
    print(f'\n{s_cnt:2} --- big numbers')
    print('sign(10**1000):', sign(10**1000)); counter += 1
    print('sign(-10**1000):', sign(-10**1000)); counter += 1
    print('sign(10**1000-10**1000):', sign(10**1000-10**1000)); counter += 1

    trace(prev_counter, counter, s_cnt)

    s_cnt += 1; prev_counter = counter
    print(f'\n{s_cnt:2} --- float')
    print("sign(-5.0):", sign(-5.0)); counter += 1
    print("sign(-1.0):", sign(-1.0)); counter += 1
    print("sign(0.0):", sign(0.0)); counter += 1
    print("sign(1.0):", sign(1.0)); counter += 1
    print("sign(5.0):", sign(5.0)); counter += 1

    trace(prev_counter, counter, s_cnt)

    s_cnt += 1; prev_counter = counter
    print(f'\n{s_cnt:2} --- -0.0 and +0.0')
    print("sign(float('-0.0')):", sign(float('-0.0'))); counter += 1
    print("sign(float('+0.0')):", sign(float('+0.0'))); counter += 1

    trace(prev_counter, counter, s_cnt)

    s_cnt += 1; prev_counter = counter
    print(f'\n{s_cnt:2} --- -inf and inf')
    print("sign(-inf):", sign(-inf)); counter += 1
    print("sign(inf):", sign(inf)); counter += 1

    trace(prev_counter, counter, s_cnt)

    s_cnt += 1; prev_counter = counter
    print(f'\n{s_cnt:2} --- -nan and nan')
    print("sign(float('-nan')):", sign(float('-nan'))); counter += 1
    print("sign(nan):", sign(nan)); counter += 1
    print("sign(0.0*nan):", sign(0.0*nan)); counter += 1

    trace(prev_counter, counter, s_cnt)

    s_cnt += 1; prev_counter = counter
    print(f'\n{s_cnt:2} --- Fraction')
    print("sign(Fraction(-5, 2)):", sign(Fraction(-5, 2))); counter += 1
    print("sign(Fraction(-1, 2)):", sign(Fraction(-1, 2))); counter += 1
    print("sign(Fraction(0, 2)):", sign(Fraction(0, 2))); counter += 1
    print("sign(Fraction(1, 2)):", sign(Fraction(1, 2))); counter += 1
    print("sign(Fraction(5, 2)):", sign(Fraction(5, 2))); counter += 1

    trace(prev_counter, counter, s_cnt)

    s_cnt += 1; prev_counter = counter
    print(f'\n{s_cnt:2} --- Decimal')
    print("sign(Decimal(-5.5)):", sign(Decimal(-5.5))); counter += 1
    print("sign(Decimal(-1.5)):", sign(Decimal(-1.5))); counter += 1
    print("sign(Decimal(0.0)):", sign(Decimal(0.0))); counter += 1
    print("sign(Decimal(1.5)):", sign(Decimal(1.5))); counter += 1
    print("sign(Decimal(5.5)):", sign(Decimal(5.5))); counter += 1

    trace(prev_counter, counter, s_cnt)

    s_cnt += 1; prev_counter = counter
    print(f"\n{s_cnt:2} --- Decimal('NaN')")
    print("sign(Decimal('NaN')):", sign(Decimal('NaN'))); counter += 1

    trace(prev_counter, counter, s_cnt)

    s_cnt += 1; prev_counter = counter
    print(f'\n{s_cnt:2} --- sympy (substitution and Rational)')
    x_sym = sympy.Symbol('x')
    expr = x_sym
    val = expr.subs(x_sym, -3.14)
    print(f"val: {repr(val)}; type(val): {type(val)}")
    print(f"type(val > 0): {type(val > 0)}")
    print("sign(val):", sign(val)); counter += 1
    print("sign(sympy.Rational(3, 4)):", sign(sympy.Rational(3, 4))); counter += 1

    trace(prev_counter, counter, s_cnt)

    s_cnt += 1; prev_counter = counter
    print(f'\n{s_cnt:2} --- sympy.nan')
    print("sign(sympy.nan):", sign(sympy.nan)); counter += 1

    trace(prev_counter, counter, s_cnt)

    s_cnt += 1; prev_counter = counter
    print(f'\n{s_cnt:2} --- My Custom Class That Have >, <, == With Numbers But Nothing Else')
    print("sign(MyNumber(-5)):", sign(MyNumber(-5))); counter += 1
    print("sign(MyNumber(-1)):", sign(MyNumber(-1))); counter += 1
    print("sign(MyNumber(0)):", sign(MyNumber(0))); counter += 1
    print("sign(MyNumber(1)):", sign(MyNumber(1))); counter += 1
    print("sign(MyNumber(5.1)):", sign(MyNumber(5.1))); counter += 1
    try:
        print("sign(MyNumber(nan)):", sign(MyNumber(nan)))
    except TypeError as e:
        print(f"- {e}")
    finally:
        counter += 1

    trace(prev_counter, counter, s_cnt)

    s_cnt += 1; prev_counter = counter
    new_test = '0 with keys, ' if version != '1.0.2' else ''
    print(f"\n{s_cnt:2} --- invalid number of positional arguments (0, {new_test}2, 3, 4)")
    try:
        print("sign():", sign())
    except TypeError as e:
        print(f"- {e}")
    finally:
        counter += 1

    if version != '1.0.2': # Test for newer versions
        try:
            print("sign(preprocess=lambda a: (float(a),), if_exc=None):",
                  sign(preprocess=lambda a: (float(a),), if_exc=None))
        except TypeError as e:
            print(f"- {e}")
        finally:
            counter += 1

    try:
        print("sign(-1, 0):", sign(-1, 0))
    except TypeError as e:
        print(f"- {e}")
    finally:
        counter += 1

    try:
        print("sign(-1, 0, 1):", sign(-1, 0, 1))
    except TypeError as e:
        print(f"- {e}")
    finally:
        counter += 1

    try:
        print("sign(-1, 0, 1, 5):", sign(-1, 0, 1, 5))
    except TypeError as e:
        print(f"- {e}")
    finally:
        counter += 1

    trace(prev_counter, counter, s_cnt)

    s_cnt += 1; prev_counter = counter
    print(f'\n{s_cnt:2} --- ExplodingNumber, NotImplementedNumber')
    try:
        print("sign(ExplodingNumber(-3.14):", sign(ExplodingNumber(-3.14)))
    except TypeError as e:
        print(f"- {e}")
    finally:
        counter += 1

    try:
        print("sign(NotImplementedNumber(-3.14):", sign(NotImplementedNumber(-3.14)))
    except TypeError as e:
        print(f"- {e}")
    finally:
        counter += 1

    trace(prev_counter, counter, s_cnt)

    s_cnt += 1; prev_counter = counter
    print(f"\n{s_cnt:2} --- inappropriate argument types (None, str, complex, list, set)")
    tests = [None, '5.0', 'nan', 'number 5', -1+1j, [-8.75], {-3.14},]
    for x in tests:
        try:
            print("sign({repr(x)}):", sign(x))
        except TypeError as e:
            print(f"- {e}")
        finally:
            counter += 1

    trace(prev_counter, counter, s_cnt)

    # New options since version 1.1.0; skip these tests for v1.0.2

    if version != '1.0.2': # v1.1.0+
        s_cnt += 1; prev_counter = counter
        print(f'\n{s_cnt:2} --- preprocess key, simple argument replacement, string conversion')
        tests = ['5.0', 'nan', -18]
        for x in tests:
            try:
                print(f"sign({repr(x)}, "
                      f"preprocess=lambda a: (float(a),)):", sign(x, preprocess=lambda a: (float(a),)))
            except TypeError as e:
                print(f"- {e}")
            finally:
                counter += 1

        trace(prev_counter, counter, s_cnt)

        s_cnt += 1; prev_counter = counter
        print(f'\n{s_cnt:2} --- preprocess key, argument replacement, treat small number as zero')
        tests = [-1, 0, -.187e-17, 5.0]
        for x in tests:
            print(f"sign({x}, "
                  f"preprocess=lambda a: (0 if abs(a) < EPS else a,)):",
                  sign(x, preprocess=lambda a: (0 if abs(a) < EPS else a,))); counter += 1

        trace(prev_counter, counter, s_cnt)

        s_cnt += 1; prev_counter = counter
        print(f'\n{s_cnt:2} --- preprocess key, replace only string argument, extract number from string')
        numeric_finder = re.compile(r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?")

        tests = ["15 men on the dead man's chest", 'Temperature is -.12e+02 °C', 'error', 123]
        for x in tests:
            try:
                print(f"sign({repr(x)}, "
                      f"preprocess=n_extract):", sign(x, preprocess=n_extract))
            except TypeError as e:
                print(f"- {e}")
            finally:
                counter += 1

        trace(prev_counter, counter, s_cnt)

        s_cnt += 1; prev_counter = counter
        print(f'\n{s_cnt:2} --- preprocess key, replace result, permits complex arguments')
        tests = [-1+1j, -18.4]

        for x in tests:
            try:
                print(f"sign({repr(x)}, "
                      f"preprocess=c_prep):", sign(x, preprocess=c_prep))
            except TypeError as e:
                print(f"- {e}")
            finally:
                counter += 1

        trace(prev_counter, counter, s_cnt)

        s_cnt += 1; prev_counter = counter
        print(f"\n{s_cnt:2} --- preprocess key, replace result, float result for 'float' and 'Decimal', sign recursion")
        tests = [-5, -5.0, Decimal(-5.5)]
        for x in tests:
            try:
                print(f"sign({repr(x)}, "
                      f"preprocess=lambda a: (a, float(sign(a))) if isinstance(a, (float, Decimal)) else None):",
                      sign(x, preprocess=lambda a: (a, float(sign(a))) if isinstance(a, (float, Decimal)) else None))
            except TypeError as e:
                print(f"- {e}")
            finally:
                counter += 1

        trace(prev_counter, counter, s_cnt)

        s_cnt += 1; prev_counter = counter
        print(f'\n{s_cnt:2} --- preprocess key, replace result or argument, treat small number as zero differently')
        tests = [-1, 0, -.187e-17, 5.0]
        ppl = lambda x: (x, 0) if abs(x) < EPS else (x,)
        for x in tests:
            print(f"sign({x}, preprocess=ppl):", sign(x, preprocess=ppl)); counter += 1

        trace(prev_counter, counter, s_cnt)

        s_cnt += 1; prev_counter = counter
        print(f'\n{s_cnt:2} --- if_exc key (exception safety)')
        tests = [(None, '?'), ('5.0', '?'), ('nan', '?'), ('number 5', '?'),
                 (-1+1j, '?'), ([-8.75], '?'), ({-3.14}, '?'), # blocking exception, marked '?'
                 (-1, '!'), (31.4, '!'), (nan, '!'), (Fraction(-99, 19), '!'), (Decimal('101.78'), '!'),]                                              # valid nuneric types, marked '!'
        flag = 0
        repl = [None, -2, nan, None,]
        nrepl = len(repl)
        sp = ' '; quo = "'"
        for x, mark in tests:
            try:
                print(f"Type: {quo + type(x).__name__ + quo:10} {mark} "
                      f"sign({repr(x)}, "
                      f"if_exc=({repl[flag]},)):",
                      sign(x, if_exc=(repl[flag],)))
            except TypeError as e:
                print(f"- {e}")
            finally:
                counter += 1
            flag = (flag + 1) % nrepl

        trace(prev_counter, counter, s_cnt)

        s_cnt += 1; prev_counter = counter
        print(f"\n{s_cnt:2} --- both preprocess and if_exc key")
        tests = [-5, -5.0, Decimal(-5.5), 'error']
        for x in tests:
            try:
                print(f"sign({repr(x)}, "
                      f"preprocess=lambda a: (a, float(sign(a))) if isinstance(a, (float, Decimal)) else None, "
                      f"if_exc=(None,)):",
                      sign(x, preprocess=lambda a: (a, float(sign(a))) if isinstance(a, (float, Decimal)) else None, if_exc=(None,)))
            except TypeError as e:
                print(f"- {e}")
            finally:
                counter += 1

        trace(prev_counter, counter, s_cnt)

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

# Detecting version anew
version = detect_version()

duration = time.perf_counter() - start_time
print(f'\nSuccess of {version}: {counter} tests in {s_cnt} sections passed {MAX_PASSES} times in {duration:>9.4f}s.')

# Restore stdout and stderr
sys.stdout.reconfigure(**original_stdout_params)
sys.stderr.reconfigure(**original_stderr_params)
