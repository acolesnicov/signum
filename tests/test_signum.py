from signum import sign, fastsign

from testing import EPS, PIRATES, n_extract, c_prep, \
                    MyNumber, ExplodingNumber, NotImplementedNumber, trace, success, OutputUTF8

from decimal import Decimal
from fractions import Fraction
from math import nan, isnan, inf
import sympy
import unittest

class TestSignum(unittest.TestCase):

    def test_sign(self):
        self.buffer = []
        s_cnt = 0
        counter = 0
        # --- int
        s_cnt += 1; prev_counter = counter
        self.assertEqual(sign(-5), -1); counter += 1
        self.assertEqual(sign(-1), -1); counter += 1
        self.assertEqual(sign(0), 0); counter += 1
        self.assertEqual(sign(1), 1); counter += 1
        self.assertEqual(sign(5), 1); counter += 1
        self.buffer.append(trace(prev_counter, counter, s_cnt, what="'int'"))

        # ------ bool
        s_cnt += 1; prev_counter = counter
        self.assertEqual(sign(True), 1); counter += 1
        self.assertEqual(sign(False), 0); counter += 1
        self.buffer.append(trace(prev_counter, counter, s_cnt, what="'bool'"))

        # ------ big numbers
        s_cnt += 1; prev_counter = counter
        self.assertEqual(sign(10**1000), 1); counter += 1
        self.assertEqual(sign(-10**1000), -1); counter += 1
        self.assertEqual(sign(10**1000-10**1000), 0); counter += 1
        self.buffer.append(trace(prev_counter, counter, s_cnt, what="big 'int'"))

        # --- float
        s_cnt += 1; prev_counter = counter
        self.assertEqual(sign(-5.0), -1); counter += 1
        self.assertEqual(sign(-1.0), -1); counter += 1
        self.assertEqual(sign(0.0), 0); counter += 1
        self.assertEqual(sign(1.0), 1); counter += 1
        self.assertEqual(sign(5.0), 1); counter += 1
        self.buffer.append(trace(prev_counter, counter, s_cnt, what="'float'"))

        # ------ -0.0 and +0.0
        s_cnt += 1; prev_counter = counter
        self.assertEqual(sign(float('-0.0')), 0); counter += 1
        self.assertEqual(sign(float('+0.0')), 0); counter += 1
        self.buffer.append(trace(prev_counter, counter, s_cnt, what="±0.0"))

        # ------ -inf and inf
        s_cnt += 1; prev_counter = counter
        self.assertEqual(sign(-inf), -1); counter += 1
        self.assertEqual(sign(inf), 1); counter += 1
        self.buffer.append(trace(prev_counter, counter, s_cnt, what="infinity"))

        # ------ -nan (the same as nan), nan
        s_cnt += 1; prev_counter = counter
        self.assertTrue(isnan(sign(float('-nan')))); counter += 1
        self.assertTrue(isnan(sign(nan))); counter += 1
        self.assertTrue(isnan(sign(0.0*nan))); counter += 1
        self.buffer.append(trace(prev_counter, counter, s_cnt, what="NaN"))

        # --- Fraction
        s_cnt += 1; prev_counter = counter
        self.assertEqual(sign(Fraction(-5, 2)), -1); counter += 1
        self.assertEqual(sign(Fraction(-1, 2)), -1); counter += 1
        self.assertEqual(sign(Fraction(0, 2)), 0); counter += 1
        self.assertEqual(sign(Fraction(1, 2)), 1); counter += 1
        self.assertEqual(sign(Fraction(5, 2)), 1); counter += 1
        self.buffer.append(trace(prev_counter, counter, s_cnt, what="'Fraction'"))

        # --- Tests with a very small argument kindly provided by Tim Peters
        s_cnt += 1; prev_counter = counter
        self.assertEqual(sign(Fraction(1, 1 << 2000)), 1); counter += 1
        self.assertEqual(sign(float(Fraction(1, 1 << 2000))), 0); counter += 1
        self.buffer.append(trace(prev_counter, counter, s_cnt, what="Very small argument (kindly provided by Tim Peters)"))

        # --- Decimal
        s_cnt += 1; prev_counter = counter
        self.assertEqual(sign(Decimal(-5.5)), -1); counter += 1
        self.assertEqual(sign(Decimal(-1.5)), -1); counter += 1
        self.assertEqual(sign(Decimal(0.0)), 0); counter += 1
        self.assertEqual(sign(Decimal(1.5)), 1); counter += 1
        self.assertEqual(sign(Decimal(5.5)), 1); counter += 1
        self.buffer.append(trace(prev_counter, counter, s_cnt, what="'Decimal'"))

        # ------ Decimal NaN
        s_cnt += 1; prev_counter = counter
        self.assertTrue(isnan(sign(Decimal('NaN')))); counter += 1
        self.buffer.append(trace(prev_counter, counter, s_cnt, what="Decimal NaN"))

        # --- sympy
        x_sym = sympy.Symbol('x')
        expr = x_sym
        val = expr.subs(x_sym, -3.14)
        s_cnt += 1; prev_counter = counter
        self.assertEqual(sign(val), -1); counter += 1
        self.assertEqual(sign(sympy.Rational(3, 4)), 1); counter += 1
        self.buffer.append(trace(prev_counter, counter, s_cnt, what="sympy"))

        # ------ sympy.nan
        s_cnt += 1; prev_counter = counter
        self.assertTrue(isnan(sign(sympy.nan))); counter += 1
        self.buffer.append(trace(prev_counter, counter, s_cnt, what="sympy.nan"))

        # --- New custom class (testing possible future extentions)
        #     This class has no __float__ that tests one subtle branch in the C++ code
        s_cnt += 1; prev_counter = counter
        self.assertEqual(sign(MyNumber(-5)), -1); counter += 1
        self.assertEqual(sign(MyNumber(-1)), -1); counter += 1
        self.assertEqual(sign(MyNumber(0)), 0); counter += 1
        self.assertEqual(sign(MyNumber(1)), 1); counter += 1
        self.assertEqual(sign(MyNumber(5)), 1); counter += 1
        with self.assertRaisesRegex(TypeError, r'signum\.sign: invalid argument `MyNumber\(nan\)`'):
            sign(MyNumber(nan))
        counter += 1
        self.buffer.append(trace(prev_counter, counter, s_cnt, what="new custom class"))

        # Testing inappropriate arguments and types (non-scalar, non-comparable, etc.)

        # --- Invalid number of positional arguments (0, 0 with keys, 2, 3, 4, 5); invalid keyword
        s_cnt += 1; prev_counter = counter
        with self.assertRaisesRegex(TypeError, r"signum\.sign\(\) takes 1 or 2 positional arguments, got 0"):
            sign()
        counter += 1
        with self.assertRaisesRegex(TypeError, r"signum\.sign\(\) takes 1 or 2 positional arguments, got 0"):
            sign(preprocess=lambda a: (float(a),), if_exc=None)
        counter += 1
        with self.assertRaisesRegex(TypeError, r'signum\.sign\(\) takes 1 or 2 positional arguments, got 3'):
            sign(-1, 0, 1)
        counter += 1
        with self.assertRaisesRegex(TypeError, r'signum\.sign\(\) takes 1 or 2 positional arguments, got 4'):
            sign(-1, 0, 1, 4)
        counter += 1
        with self.assertRaisesRegex(TypeError, r'signum\.sign\(\) takes 1 or 2 positional arguments, got 5'):
            sign(-1, 0, 1, 4, 5)
        counter += 1
        with self.assertRaisesRegex(TypeError, r"signum.sign\(\) got an unexpected keyword argument 'code_shift'"):
            sign(5.0, code_shift=2)
        counter += 1
        self.buffer.append(trace(prev_counter, counter, s_cnt, what="invalid number of arguments"))

        # --- ExplodingNumber, NotImplementedNumber
        s_cnt += 1; prev_counter = counter
        with self.assertRaisesRegex(TypeError, r'signum.sign: invalid argument `ExplodingNumber\(-3\.14\)`'):
            sign(ExplodingNumber(-3.14))
        counter += 1
        with self.assertRaisesRegex(TypeError, r'signum.sign: invalid argument `NotImplementedNumber\(-3\.14\)`'):
            sign(NotImplementedNumber(-3.14))
        counter += 1
        self.buffer.append(trace(prev_counter, counter, s_cnt, what="Exploding and Not Implemented numbers"))

        # --- None, str, complex, list, set
        tests = [(r"`None`", None), (r"`'5\.0'`", '5.0'), (r"`'nan'`", 'nan'),
                 (r"`'number 5'`", 'number 5'), (r"`\(-1\+1j\)`", -1+1j), (r"`\[-8\.75\]`", [-8.75]),
                 (r"`\{-3\.14\}`", {-3.14}),
                ]

        s_cnt += 1; prev_counter = counter
        for msg, obj in tests:
            with self.subTest(obj=obj):
                with self.assertRaisesRegex(TypeError,
                                            r'signum\.sign: invalid argument ' + msg):
                    sign(obj)
                counter += 1
        self.buffer.append(trace(prev_counter, counter, s_cnt, what="inappropriate types"))

        ## Testing additional key arguments (preprocess=, is_exc=, both, codeshift=, combinations)

        # --- preprocess key, simple argument replacement, string conversion
        s_cnt += 1; prev_counter = counter
        self.assertEqual(sign('5.0', preprocess=lambda a: (float(a),)), 1); counter += 1
        self.assertTrue(isnan(sign('nan', preprocess=lambda a: (float(a),)))); counter += 1
        self.assertEqual(sign(-18, preprocess=lambda a: (float(a),)), -1); counter += 1
        self.buffer.append(trace(prev_counter, counter, s_cnt, what="preprocess with simple str replacement"))

        # --- preprocess key, argument replacement, treat small number as zero
        s_cnt += 1; prev_counter = counter
        tests = [(-1, -1), (0, 0), (-.187e-17, 0), (5.0, 1)]
        for x, y in tests:
            self.assertEqual(sign(x, preprocess=lambda a: (0 if abs(a) < EPS else a,)), y);  counter += 1
        self.buffer.append(trace(prev_counter, counter, s_cnt, what="preprocess treating small number as zero"))

        # --- preprocess key, replace only string argument, extract number from string
        s_cnt += 1; prev_counter = counter
        self.assertEqual(sign(PIRATES, preprocess=n_extract), 1); counter += 1
        self.assertEqual(sign('Temperature is -.12e+02 °C', preprocess=n_extract), -1); counter += 1
        with self.assertRaisesRegex(TypeError, r"signum.sign: invalid argument `'error'` \(type 'str'\)"):
            sign('error', preprocess=n_extract)
        counter += 1
        self.assertEqual(sign(123, preprocess=n_extract), 1); counter += 1
        self.buffer.append(trace(prev_counter, counter, s_cnt, what="preprocess extracting numbers from str"))

        # --- preprocess key, replace result, permits complex arguments
        s_cnt += 1; prev_counter = counter
        tests = [(-1+1j, '(-0.7071067811865475+0.7071067811865475j)'), (-18.4, '-1')]
        for x, y in tests:
            self.assertEqual(str(sign(x, preprocess=c_prep)), y); counter += 1
        self.buffer.append(trace(prev_counter, counter, s_cnt, what="preprocess permitting complex arguments"))

        # --- preprocess key, replace result, float result for 'float' and 'Decimal', sign recursion
        s_cnt += 1; prev_counter = counter
        tests = [(-5, -1, int), (-5.0, -1.0, float), (Decimal(-5.5), -1.0, float)]
        for x, y, t in tests:
            self.assertEqual((s := sign(x, preprocess=lambda a: (a, float(sign(a))) if isinstance(a, (float, Decimal)) else None)), y)
            self.assertIsInstance(s, t); counter += 1
        self.buffer.append(trace(prev_counter, counter, s_cnt, what="preprocess with float result and sign recursion"))

        # --- preprocess key, replace result or argument, treat small number as zero differently
        s_cnt += 1; prev_counter = counter
        tests = [(-1, -1), (0, 0), (-.187e-17, 0), (5.0, 1)]
        ppl = lambda x: (x, 0) if abs(x) < EPS else (x,)
        for x, y in tests:
            self.assertEqual(sign(x, preprocess=ppl), y); counter += 1
        self.buffer.append(trace(prev_counter, counter, s_cnt, what="preprocess replacing result or argument"))

        # --- if_exc key (exception safety)
        s_cnt += 1; prev_counter = counter
        tests = [(None, 'None'), ('5.0', '-2'), ('nan', 'nan'), ('number 5', 'None'),
                 (-1+1j, 'None'), ([-8.75], '-2'), ({-3.14}, 'nan'), # blocking exceptions
                 (-1, '-1'), (31.4, '1'), (nan, 'nan'), (Fraction(-99, 19), '-1'), (Decimal('101.78'), '1'),]                                              # valid nuneric types
        flag = 0
        repl = [None, -2, nan, None,]
        nrepl = len(repl)
        for x, y in tests:
            self.assertEqual(repr(sign(x, if_exc=(repl[flag],))), y); counter += 1
            flag = (flag + 1) % nrepl
        self.buffer.append(trace(prev_counter, counter, s_cnt, what="if_exc key"))

        # --- both preprocess and if_exc key
        s_cnt += 1; prev_counter = counter
        tests = [(-5, '-1', int), (-5.0, '-1.0', float),
                 (Decimal(-5.5), '-1.0', float), ('error', 'None', type(None))]
        for x, y, t in tests:
            self.assertEqual(str(s := sign(x, preprocess=lambda a: (a, float(sign(a))) if isinstance(a, (float, Decimal)) else None, if_exc=(None,))), y)
            self.assertIsInstance(s, t); counter += 1
        self.buffer.append(trace(prev_counter, counter, s_cnt, what="both preprocess and if_exc"))

        # codeshift and combinations
        s_cnt += 1; prev_counter = counter
        self.assertEqual(sign('error', codeshift=2), 0); counter += 1
        self.assertEqual(sign(-5, codeshift=2), 1); counter += 1
        self.assertEqual(sign(0, codeshift=2), 2); counter += 1
        self.assertEqual(sign(5, codeshift=2), 3); counter += 1
        self.assertEqual(sign(nan, codeshift=2), 4); counter += 1
        self.assertEqual(sign('error', if_exc=(-7,), codeshift=2), -7); counter += 1
        self.assertEqual(sign(-5, if_exc=(-7,), codeshift=2), 1); counter += 1
        self.assertEqual(sign(0, if_exc=(-7,), codeshift=2), 2); counter += 1
        self.assertEqual(sign(5, if_exc=(-7,), codeshift=2), 3); counter += 1
        self.assertEqual(sign(nan, if_exc=(-7,), codeshift=2), 4); counter += 1
        self.assertEqual(sign('error', preprocess=lambda a: (0 if abs(a) < EPS else a,), codeshift=2), 0); counter += 1
        self.assertEqual(sign(-1, preprocess=lambda a: (0 if abs(a) < EPS else a,), codeshift=2), 1); counter += 1
        self.assertEqual(sign(0, preprocess=lambda a: (0 if abs(a) < EPS else a,), codeshift=2), 2); counter += 1
        self.assertEqual(sign(-1.87e-18, preprocess=lambda a: (0 if abs(a) < EPS else a,), codeshift=2), 2); counter += 1
        self.assertEqual(sign(5.0, preprocess=lambda a: (0 if abs(a) < EPS else a,), codeshift=2), 3); counter += 1
        self.assertEqual(sign('error', preprocess=lambda a: (a, float(sign(a))) if isinstance(a, float) else None, codeshift=1), -1); counter += 1
        self.assertEqual((s := sign(-5.0, preprocess=lambda a: (a, float(sign(a))) if isinstance(a, float) else None, codeshift=1)), -1.0)
        self.assertIsInstance(s, float); counter += 1
        self.assertEqual((s := sign(0.0, preprocess=lambda a: (a, float(sign(a))) if isinstance(a, float) else None, codeshift=1)), 0.0)
        self.assertIsInstance(s, float); counter += 1
        self.assertEqual(sign(0, preprocess=lambda a: (a, float(sign(a))) if isinstance(a, float) else None, codeshift=1), 1); counter += 1
        self.assertEqual(sign(5, preprocess=lambda a: (a, float(sign(a))) if isinstance(a, float) else None, codeshift=1), 2); counter += 1
        self.assertTrue(isnan(sign(nan, preprocess=lambda a: (a, float(sign(a))) if isinstance(a, float) else None, codeshift=1))); counter += 1
        self.assertEqual(sign('error', preprocess=lambda a: (a, float(sign(a))) if isinstance(a, float) else None, if_exc=(-7,), codeshift=1), -7); counter += 1
        self.assertEqual((s := sign(-5.0, preprocess=lambda a: (a, float(sign(a))) if isinstance(a, float) else None, if_exc=(-7,), codeshift=1)), -1.0)
        self.assertIsInstance(s, float); counter += 1
        self.assertEqual((s := sign(0.0, preprocess=lambda a: (a, float(sign(a))) if isinstance(a, float) else None, if_exc=(-7,), codeshift=1)), 0.0)
        self.assertIsInstance(s, float); counter += 1
        self.assertEqual(sign(0, preprocess=lambda a: (a, float(sign(a))) if isinstance(a, float) else None, if_exc=(-7,), codeshift=1), 1); counter += 1
        self.assertEqual(sign(5, preprocess=lambda a: (a, float(sign(a))) if isinstance(a, float) else None, if_exc=(-7,), codeshift=1), 2); counter += 1
        self.assertTrue(isnan(sign(nan, preprocess=lambda a: (a, float(sign(a))) if isinstance(a, float) else None, if_exc=(-7,), codeshift=1))); counter += 1
        self.buffer.append(trace(prev_counter, counter, s_cnt, what="codeshift and key combinations"))

        # v1.2.3: positional codeshift
        s_cnt += 1; prev_counter = counter
        with self.assertRaisesRegex(TypeError, r"signum\.sign\(\): the 2nd positional argument used; "
                                               r"'codeshift=' is not permitted"):
            sign(-77, None, codeshift=2)
        counter += 1
        self.assertEqual(sign('error', 2), 0); counter += 1
        self.assertEqual(sign(-5, 2), 1); counter += 1
        self.assertEqual(sign(0, 2), 2); counter += 1
        self.assertEqual(sign(5, 2), 3); counter += 1
        self.assertEqual(sign(nan, 2), 4); counter += 1
        self.assertEqual(sign('error', 2, if_exc=(-7,)), -7); counter += 1
        self.assertEqual(sign(-5, 2, if_exc=(-7,)), 1); counter += 1
        self.assertEqual(sign(0, 2, if_exc=(-7,)), 2); counter += 1
        self.assertEqual(sign(5, 2, if_exc=(-7,)), 3); counter += 1
        self.assertEqual(sign(nan, 2, if_exc=(-7,)), 4); counter += 1
        self.assertEqual(sign('error', 2, preprocess=lambda a: (0 if abs(a) < EPS else a,)), 0); counter += 1
        self.assertEqual(sign(-1, 2, preprocess=lambda a: (0 if abs(a) < EPS else a,)), 1); counter += 1
        self.assertEqual(sign(0, 2, preprocess=lambda a: (0 if abs(a) < EPS else a,)), 2); counter += 1
        self.assertEqual(sign(-1.87e-18, 2, preprocess=lambda a: (0 if abs(a) < EPS else a,)), 2); counter += 1
        self.assertEqual(sign(5.0, 2, preprocess=lambda a: (0 if abs(a) < EPS else a,)), 3); counter += 1
        self.assertEqual(sign('error', 1, preprocess=lambda a: (a, float(sign(a))) if isinstance(a, float) else None), -1); counter += 1
        self.assertEqual(s := sign(-5.0, 1, preprocess=lambda a: (a, float(sign(a))) if isinstance(a, float) else None), -1.0);
        self.assertIsInstance(s, float); counter += 1
        self.assertEqual(s := sign(0.0, 1, preprocess=lambda a: (a, float(sign(a))) if isinstance(a, float) else None), 0.0);
        self.assertIsInstance(s, float); counter += 1
        self.assertEqual(sign(0, 1, preprocess=lambda a: (a, float(sign(a))) if isinstance(a, float) else None), 1); counter += 1
        self.assertEqual(sign(5, 1, preprocess=lambda a: (a, float(sign(a))) if isinstance(a, float) else None), 2); counter += 1
        self.assertTrue(isnan(sign(nan, 1, preprocess=lambda a: (a, float(sign(a))) if isinstance(a, float) else None))); counter += 1
        self.assertEqual(sign(nan, 1, preprocess=lambda a: (a, float(sign(a))) if isinstance(a, float) and not isnan(a) else None), 3); counter += 1
        self.assertEqual(sign('error', 1, preprocess=lambda a: (a, float(sign(a))) if isinstance(a, float) else None, if_exc=(-7,)), -7); counter += 1
        self.assertEqual(s := sign(-5.0, 1, preprocess=lambda a: (a, float(sign(a))) if isinstance(a, float) else None, if_exc=(-7,)), -1.0);
        self.assertIsInstance(s, float); counter += 1
        self.assertEqual(s := sign(0.0, 1, preprocess=lambda a: (a, float(sign(a))) if isinstance(a, float) else None, if_exc=(-7,)), 0.0);
        self.assertIsInstance(s, float); counter += 1
        self.assertEqual(sign(0, 1, preprocess=lambda a: (a, float(sign(a))) if isinstance(a, float) else None, if_exc=(-7,)), 1); counter += 1
        self.assertEqual(sign(5, 1, preprocess=lambda a: (a, float(sign(a))) if isinstance(a, float) else None, if_exc=(-7,)), 2); counter += 1
        self.assertTrue(isnan(sign(nan, 1, preprocess=lambda a: (a, float(sign(a))) if isinstance(a, float) else None, if_exc=(-7,)))); counter += 1
        self.assertEqual(sign(nan, 1, preprocess=lambda a: (a, float(sign(a))) if isinstance(a, float) and not isnan(a) else None, if_exc=(-7,)), 3); counter += 1
        self.buffer.append(trace(prev_counter, counter, s_cnt, what="positional codeshift"))

        # v1.2.3: fastsign
        s_cnt += 1; prev_counter = counter
        self.assertEqual(fastsign(-5), -1); counter += 1
        self.assertEqual(fastsign(-1), -1); counter += 1
        self.assertEqual(fastsign(0), 0); counter += 1
        self.assertEqual(fastsign(1), 1); counter += 1
        self.assertEqual(fastsign(5), 1); counter += 1
        self.assertEqual(fastsign(True), 1); counter += 1
        self.assertEqual(fastsign(False), 0); counter += 1
        self.assertEqual(fastsign(10**1000), 1); counter += 1
        self.assertEqual(fastsign(-10**1000), -1); counter += 1
        self.assertEqual(fastsign(10**1000-10**1000), 0); counter += 1
        self.assertEqual(fastsign(-5.0), -1); counter += 1
        self.assertEqual(fastsign(-1.0), -1); counter += 1
        self.assertEqual(fastsign(0.0), 0); counter += 1
        self.assertEqual(fastsign(1.0), 1); counter += 1
        self.assertEqual(fastsign(5.0), 1); counter += 1
        self.assertEqual(fastsign(float('-0.0')), 0); counter += 1
        self.assertEqual(fastsign(float('+0.0')), 0); counter += 1
        self.assertEqual(fastsign(-inf), -1); counter += 1
        self.assertEqual(fastsign(inf), 1); counter += 1
        self.assertTrue(isnan(fastsign(float('-nan')))); counter += 1
        self.assertTrue(isnan(fastsign(nan))); counter += 1
        self.assertTrue(isnan(fastsign(0.0*nan))); counter += 1
        self.assertEqual(fastsign(Fraction(-5, 2)), -1); counter += 1
        self.assertEqual(fastsign(Fraction(-1, 2)), -1); counter += 1
        self.assertEqual(fastsign(Fraction(0, 2)), 0); counter += 1
        self.assertEqual(fastsign(Fraction(1, 2)), 1); counter += 1
        self.assertEqual(fastsign(Fraction(5, 2)), 1); counter += 1
        self.assertEqual(fastsign(Fraction(1, 1 << 2000)), 1); counter += 1
        self.assertEqual(fastsign(float(Fraction(1, 1 << 2000))), 0); counter += 1
        self.assertEqual(fastsign(Decimal(-5.5)), -1); counter += 1
        self.assertEqual(fastsign(Decimal(-1.5)), -1); counter += 1
        self.assertEqual(fastsign(Decimal(0.0)), 0); counter += 1
        self.assertEqual(fastsign(Decimal(1.5)), 1); counter += 1
        self.assertEqual(fastsign(Decimal(5.5)), 1); counter += 1
        self.assertTrue(isnan(fastsign(Decimal('NaN')))); counter += 1
        x_sym = sympy.Symbol('x')
        expr = x_sym
        val = expr.subs(x_sym, -3.14)
        self.assertEqual(fastsign(val), -1); counter += 1
        self.assertEqual(fastsign(sympy.Rational(3, 4)), 1); counter += 1
        self.assertTrue(isnan(fastsign(sympy.nan))); counter += 1
        self.assertEqual(fastsign(MyNumber(-5)), -1); counter += 1
        self.assertEqual(fastsign(MyNumber(-1)), -1); counter += 1
        self.assertEqual(fastsign(MyNumber(0)), 0); counter += 1
        self.assertEqual(fastsign(MyNumber(1)), 1); counter += 1
        self.assertEqual(fastsign(MyNumber(5.1)), 1); counter += 1
        with self.assertRaisesRegex(TypeError, r"must be real number, not MyNumber"):
            fastsign(MyNumber(nan))
        counter += 1
        with self.assertRaisesRegex(TypeError, r"signum\.fastsign\(\) takes exactly one argument \(0 given\)"):
            fastsign()
        counter += 1
        with self.assertRaisesRegex(TypeError, r"signum\.fastsign\(\) takes no keyword arguments"):
            fastsign(if_exc=None)
        counter += 1
        with self.assertRaisesRegex(TypeError, r"signum\.fastsign\(\) takes exactly one argument \(2 given\)"):
            fastsign(-1, 0)
        counter += 1
        with self.assertRaisesRegex(TypeError, r"signum\.fastsign\(\) takes exactly one argument \(3 given\)"):
            fastsign(-1, 0, 1)
        counter += 1
        with self.assertRaisesRegex(TypeError, r"signum\.fastsign\(\) takes no keyword arguments"):
            fastsign(5.0, code_shift=2)
        counter += 1
        with self.assertRaisesRegex(RuntimeError, r"Boom!"):
            fastsign(ExplodingNumber(-3.14))
        counter += 1
        self.assertEqual(fastsign(NotImplementedNumber(-3.14)), -1); counter += 1
        with self.assertRaisesRegex(TypeError, r"must be real number, not NoneType"):
            fastsign(None)
        counter += 1
        with self.assertRaisesRegex(TypeError, r"signum\.fastsign\(\): cannot compare or check for NaN\. Cause: comparison with 'int' not implemented for type 'str'"):
            fastsign('5.0')
        counter += 1
        with self.assertRaisesRegex(TypeError, r"signum\.fastsign\(\): cannot compare or check for NaN\. Cause: comparison with 'int' not implemented for type 'str'"):
            fastsign('nan')
        counter += 1
        with self.assertRaisesRegex(TypeError, r"signum\.fastsign\(\): cannot compare or check for NaN\. Cause: comparison with 'int' not implemented for type 'str'"):
            fastsign('number 5')
        counter += 1
        with self.assertRaisesRegex(TypeError, r"must be real number, not complex"):
            fastsign(-1+1j)
        counter += 1
        with self.assertRaisesRegex(TypeError, r"must be real number, not list"):
            fastsign([-8.75,])
        counter += 1
        with self.assertRaisesRegex(TypeError, r"must be real number, not set"):
            fastsign({-3.14,})
        counter += 1
        self.buffer.append(trace(prev_counter, counter, s_cnt, what="fastsign"))

        # fastsign vs sign: same results
        s_cnt += 1; prev_counter = counter
        x_sym = sympy.Symbol('x')
        expr = x_sym
        val = expr.subs(x_sym, -3.14)
        args = [
            -5,
            -1,
            0,
            1,
            5,
            True,
            False,
            10**1000,
            -10**1000,
            10**1000-10**1000,
            -5.0,
            -1.0,
            0.0,
            1.0,
            5.0,
            float('-0.0'),
            float('+0.0'),
            -inf,
            inf,
            Fraction(-5, 2),
            Fraction(-1, 2),
            Fraction(0, 2),
            Fraction(1, 2),
            Fraction(5, 2),
            Fraction(1, 1 << 2000),
            float(Fraction(1, 1 << 2000)),
            Decimal(-5.5),
            Decimal(-1.5),
            Decimal(0.0),
            Decimal(1.5),
            Decimal(5.5),
            val,
            sympy.Rational(3, 4),
            MyNumber(-5),
            MyNumber(-1),
            MyNumber(0),
            MyNumber(1),
            MyNumber(5.1),
        ]
        for x in args:
            self.assertEqual(fastsign(x), sign(x)); counter += 1
        self.buffer.append(trace(prev_counter, counter, s_cnt, what="fastsign vs sign: same results"))

        # fastsign vs sign: same NaNs
        s_cnt += 1; prev_counter = counter
        args = [
            float('-nan'),
            nan,
            0.0*nan,
            Decimal('NaN'),
            sympy.nan,
        ]
        for x in args:
            self.assertTrue(isnan(fastsign(x)) and isnan(sign(x))); counter += 1
        self.buffer.append(trace(prev_counter, counter, s_cnt, what="fastsign vs sign: same NaNs"))

        # fastsign vs sign: same error cases
        s_cnt += 1; prev_counter = counter
        args = [
            (TypeError, MyNumber(nan),),
            (RuntimeError, ExplodingNumber(-3.14),),
            (TypeError, None,),
            (TypeError, '5.0',),
            (TypeError, 'nan',),
            (TypeError, 'number 5',),
            (TypeError, -1+1j,),
            (TypeError, [-8.75,],),
            (TypeError, {-3.14,},),
        ]
        for t, x in args:
            with self.assertRaises(t):
              fastsign(x)
            self.assertEqual(sign(x, 2), 0)
            counter += 1
        self.buffer.append(trace(prev_counter, counter, s_cnt, what="fastsign vs sign: same error cases"))

        # fastsign vs sign: different behavior
        s_cnt += 1; prev_counter = counter
        x = NotImplementedNumber(-3.14)
        self.assertEqual(fastsign(x), -1)
        self.assertEqual(sign(x, 2), 0)
        counter += 1
        self.buffer.append(trace(prev_counter, counter, s_cnt, what="fastsign vs sign: different behavior"))

        self.buffer.append(f'\n{success(counter, s_cnt=s_cnt)}\n')
        print('\n'.join(self.buffer), flush=True)

if __name__ == '__main__':
    # Switch sys.stdout and sys.stderr to 'utf-8' encoding
    outflows = OutputUTF8()
    outflows.set_utf8()

    print(f'***** Test: {__file__}\n', flush=True)
    unittest.main()

    # Restore stdout and stderr
    outflows.reset_from_utf8()
