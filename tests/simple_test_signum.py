from decimal import Decimal
from fractions import Fraction
from math import nan, inf
from signum import sign
import sympy

class MyNumber:
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

class ExplodingNumber:
    def __init__(self, value):
        self.value = value
    def __gt__(self, other):
        raise RuntimeError("Boom!")
    def __lt__(self, other):
        raise RuntimeError("Boom!")
    def __eq__(self, other):
        raise RuntimeError("Boom!")
    def __repr__(self):
        return f'ExplodingNumber({self.value})'

class NotImplementedNumber:
    def __init__(self, value):
        self.value = value
    def __gt__(self, other):
        return NotImplemented
    def __lt__(self, other):
        return NotImplemented
    def __eq__(self, other):
        return NotImplemented
    def __repr__(self):
        return f'NotImplementedNumber({self.value})'

print('--- int')
print("sign(-5):", sign(-5))
print("sign(-1):", sign(-1))
print("sign(0):", sign(0))
print("sign(1):", sign(1))
print("sign(5):", sign(5))

print('------ bool')
print("sign(True):", sign(True))
print("sign(False):", sign(False))

print('------ big numbers')
print('sign(10**1000):', sign(10**1000))
print('sign(-10**1000):', sign(-10**1000))
print('sign(10**1000-10**1000):', sign(10**1000-10**1000))

print('\n--- float')
print("sign(-5.0):", sign(-5.0))
print("sign(-1.0):", sign(-1.0))
print("sign(0.0):", sign(0.0))
print("sign(1.0):", sign(1.0))
print("sign(5.0):", sign(5.0))
print('------ -0.0 and +0.0')
print("sign(float('-0.0')):", sign(float('-0.0')))
print("sign(float('+0.0')):", sign(float('+0.0')))
print('------ -inf and inf')
print("sign(-inf):", sign(-inf))
print("sign(inf):", sign(inf))
print('------ -nan and nan')
print("sign(float('-nan')):", sign(float('-nan')))
print("sign(nan):", sign(nan))
print("sign(0.0*nan):", sign(0.0*nan))

print('\n--- Fraction')
print("sign(Fraction(-5, 2)):", sign(Fraction(-5, 2)))
print("sign(Fraction(-1, 2)):", sign(Fraction(-1, 2)))
print("sign(Fraction(0, 2)):", sign(Fraction(0, 2)))
print("sign(Fraction(1, 2)):", sign(Fraction(1, 2)))
print("sign(Fraction(5, 2)):", sign(Fraction(5, 2)))

print('\n--- Decimal')
print("sign(Decimal(-5.5)):", sign(Decimal(-5.5)))
print("sign(Decimal(-1.5)):", sign(Decimal(-1.5)))
print("sign(Decimal(0.0)):", sign(Decimal(0.0)))
print("sign(Decimal(1.5)):", sign(Decimal(1.5)))
print("sign(Decimal(5.5)):", sign(Decimal(5.5)))

print("------ Decimal('NaN')")
print("sign(Decimal('NaN')):", sign(Decimal('NaN')))

print('\n--- sympy (substitution and Rational)')
x_sym = sympy.Symbol('x')
expr = x_sym
val = expr.subs(x_sym, -3.14)
print(f"Type of val is {type(val)}")
print(f"Type of (val > 0) is {type(val > 0)}")
print("sign(val):", sign(val))
print("sign(sympy.Rational(3, 4)):", sign(sympy.Rational(3, 4)))

print('------ sympy.nan')
print("sign(sympy.nan):", sign(sympy.nan))

print('\n--- My Custom Class That Have >, <, == With Numbers But Nothing Else')
print("sign(MyNumber(-5)):", sign(MyNumber(-5)))
print("sign(MyNumber(-1)):", sign(MyNumber(-1)))
print("sign(MyNumber(0)):", sign(MyNumber(0)))
print("sign(MyNumber(1)):", sign(MyNumber(1)))
print("sign(MyNumber(5.1)):", sign(MyNumber(5.1)))
try:
    print("sign(MyNumber(nan)):", sign(MyNumber(nan)))
except TypeError as e:
    print(e)

print('\n--- No arguments')
try:
    print("sign():", sign())
except TypeError as e:
    print(e)

print('\n--- Three arguments')
try:
    print("sign(-1, 0, 1):", sign(-1, 0, 1))
except TypeError as e:
    print(e)

print('\n--- ExplodingNumber')
try:
    print("sign(ExplodingNumber(-3.14):", sign(ExplodingNumber(-3.14)))
except TypeError as e:
    print(e)

print('\n--- NotImplementedNumber')
try:
    print("sign(NotImplementedNumber(-3.14):", sign(NotImplementedNumber(-3.14)))
except TypeError as e:
    print(e)

print('\n--- None')
try:
    print("sign(None):", sign(None))
except TypeError as e:
    print(e)

print('\n--- str')
try:
    print("sign('5.0'):", sign('5.0'))
except TypeError as e:
    print(e)

try:
    print("sign('nan'):", sign('nan'))
except TypeError as e:
    print(e)

try:
    print("sign('number 5'):", sign('number 5'))
except TypeError as e:
    print(e)

print('\n--- list')
try:
    print("sign([-8.75]):", sign([-8.75]))
except TypeError as e:
    print(e)

print('\n--- complex')
try:
    print("sign(-1+1j):", sign(-1+1j))
except TypeError as e:
    print(e)

print('\n--- set')
try:
    print("sign({-3.14}):", sign({-3.14}))
except TypeError as e:
    print(e)
