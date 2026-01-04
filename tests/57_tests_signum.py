from signum import sign

from testing import *
# Local names for imported entities
_SHORT_SIMPLE_TEST    = SHORT_SIMPLE_TEST
_EPS                  = EPS
_UTF8                 = UTF8
_PIRATES              = PIRATES
_numeric_finder       = numeric_finder
_file_name            = file_name
_get_passes           = get_passes
_n_extract            = n_extract
_c_prep               = c_prep
_MyNumber             = MyNumber
_ExplodingNumber      = ExplodingNumber
_NotImplementedNumber = NotImplementedNumber
_detect_version       = detect_version
_trace                = trace
_success              = success
_open_devnull         = open_devnull
_close_devnull        = close_devnull
_OutputControl        = OutputControl

from decimal import Decimal
from fractions import Fraction
from math import nan, inf
import os
import re
import sympy
import sys
import time

MAX_PASSES = _get_passes(__file__)

# Switch sys.stdout and sys.stderr to 'utf-8' encoding
outflow_saver = _OutputControl()
outflow_saver.set_utf8()

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
    (sign(_MyNumber(-5)))
    (sign(_MyNumber(-1)))
    (sign(_MyNumber(0)))
    (sign(_MyNumber(1)))
    (sign(_MyNumber(5.1)))
    try:
        (sign(_MyNumber(nan)))
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
        (sign(-1, 0, 1, 4))
    except TypeError as e:
        (e)
    try:
        (sign(-1, 0, 1, 4, 5))
    except TypeError as e:
        (e)
    try:
        (sign(5.0, code_shift=2))
    except TypeError as e:
        (e)
    try:
        (sign(_ExplodingNumber(-3.14)))
    except TypeError as e:
        (e)
    try:
        (sign(_NotImplementedNumber(-3.14)))
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

print(f'\n{_success(57, s_cnt=None, start_time=start_time, passes=MAX_PASSES)}')

# Restore stdout and stderr
outflow_saver.reset_from_utf8()
