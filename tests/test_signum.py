try:
    from signum import sign

    from math import nan, isnan, inf
    import re
    import sys
    import unittest
except ImportError as e:
    print(e)
    print("To pass these signum tests, you should have 'csignum-fast' module installed")
    print("Terminated: no tests passed")
    exit(1)

UTF8 = 'utf-8'

class TestSignum(unittest.TestCase):

    EPS = 1e-9

    def trace(self, pcnt, cnt, scnt, what):
        delta = cnt - pcnt
        pl = 's' if delta > 1 else ' '
        self.buffer.append(f"{delta:2} test{pl} for Sec. {scnt:2}: {what} passed, total {cnt:3} tests passed")

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
        self.trace(prev_counter, counter, s_cnt, "'int'")

        # ------ bool
        s_cnt += 1; prev_counter = counter
        self.assertEqual(sign(True), 1); counter += 1
        self.assertEqual(sign(False), 0); counter += 1
        self.trace(prev_counter, counter, s_cnt, "'bool'")

        # ------ big numbers
        s_cnt += 1; prev_counter = counter
        self.assertEqual(sign(10**1000), 1); counter += 1
        self.assertEqual(sign(-10**1000), -1); counter += 1
        self.assertEqual(sign(10**1000-10**1000), 0); counter += 1
        self.trace(prev_counter, counter, s_cnt, "big 'int'")

        # --- float
        s_cnt += 1; prev_counter = counter
        self.assertEqual(sign(-5.0), -1); counter += 1
        self.assertEqual(sign(-1.0), -1); counter += 1
        self.assertEqual(sign(0.0), 0); counter += 1
        self.assertEqual(sign(1.0), 1); counter += 1
        self.assertEqual(sign(5.0), 1); counter += 1
        self.trace(prev_counter, counter, s_cnt, "'float'")

        # ------ -0.0 and +0.0
        s_cnt += 1; prev_counter = counter
        self.assertEqual(sign(float('-0.0')), 0); counter += 1
        self.assertEqual(sign(float('+0.0')), 0); counter += 1
        self.trace(prev_counter, counter, s_cnt, "±0.0")

        # ------ -inf and inf
        s_cnt += 1; prev_counter = counter
        self.assertEqual(sign(-inf), -1); counter += 1
        self.assertEqual(sign(inf), 1); counter += 1
        self.trace(prev_counter, counter, s_cnt, "infinity")

        # ------ -nan (the same as nan), nan
        s_cnt += 1; prev_counter = counter
        self.assertTrue(isnan(sign(float('-nan')))); counter += 1
        self.assertTrue(isnan(sign(nan))); counter += 1
        self.assertTrue(isnan(sign(0.0*nan))); counter += 1
        self.trace(prev_counter, counter, s_cnt, "NaN")

        # --- Fraction
        try:
            from fractions import Fraction
            have_fractions = True
        except ImportError as e:
            have_fractions = False
            self.buffer.append(e)
            self.buffer.append("No 'fractions' module found in your installation. Tests for 'Fraction' are skipped")
        if have_fractions:
            s_cnt += 1; prev_counter = counter
            self.assertEqual(sign(Fraction(-5, 2)), -1); counter += 1
            self.assertEqual(sign(Fraction(-1, 2)), -1); counter += 1
            self.assertEqual(sign(Fraction(0, 2)), 0); counter += 1
            self.assertEqual(sign(Fraction(1, 2)), 1); counter += 1
            self.assertEqual(sign(Fraction(5, 2)), 1); counter += 1
            self.trace(prev_counter, counter, s_cnt, "'Fraction'")

        # --- Decimal
        try:
            from decimal import Decimal
            have_decimal = True
        except ImportError as e:
            have_decimal = False
            self.buffer.append(e)
            self.buffer.append("No 'decimal' module found in your installation. Tests for 'Decimal' are skipped")
        if have_decimal:
            s_cnt += 1; prev_counter = counter
            self.assertEqual(sign(Decimal(-5.5)), -1); counter += 1
            self.assertEqual(sign(Decimal(-1.5)), -1); counter += 1
            self.assertEqual(sign(Decimal(0.0)), 0); counter += 1
            self.assertEqual(sign(Decimal(1.5)), 1); counter += 1
            self.assertEqual(sign(Decimal(5.5)), 1); counter += 1
            self.trace(prev_counter, counter, s_cnt, "'Decimal'")

            # ------ Decimal NaN
            s_cnt += 1; prev_counter = counter
            self.assertTrue(isnan(sign(Decimal('NaN')))); counter += 1
            self.trace(prev_counter, counter, s_cnt, "Decimal NaN")

        # --- sympy
        try:
            import sympy
            have_sympy = True
        except ImportError as e:
            have_sympy = False
            self.buffer.append(e)
            self.buffer.append("No 'sympy' module found in your installation. Tests for 'sympy' are skipped")
        if have_sympy:
            x_sym = sympy.Symbol('x')
            expr = x_sym
            val = expr.subs(x_sym, -3.14)
            s_cnt += 1; prev_counter = counter
            self.assertEqual(sign(val), -1); counter += 1
            self.assertEqual(sign(sympy.Rational(3, 4)), 1); counter += 1
            self.trace(prev_counter, counter, s_cnt, "sympy")

            # ------ sympy.nan
            s_cnt += 1; prev_counter = counter
            self.assertTrue(isnan(sign(sympy.nan))); counter += 1
            self.trace(prev_counter, counter, s_cnt, "sympy.nan")

        # --- New custom class (testing possible future extentions)
        #     This class has no __float__ that tests one subtle branch in the C++ code
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

        s_cnt += 1; prev_counter = counter
        self.assertEqual(sign(MyNumber(-5)), -1); counter += 1
        self.assertEqual(sign(MyNumber(-1)), -1); counter += 1
        self.assertEqual(sign(MyNumber(0)), 0); counter += 1
        self.assertEqual(sign(MyNumber(1)), 1); counter += 1
        self.assertEqual(sign(MyNumber(5)), 1); counter += 1
        with self.assertRaisesRegex(TypeError, r'signum\.sign: invalid argument `MyNumber\(nan\)`'):
            sign(MyNumber(nan))
        counter += 1
        self.trace(prev_counter, counter, s_cnt, "new custom class")

        # Testing inappropriate arguments and types (non-scalar, non-comparable, etc.)

        # --- Invalid number of positional arguments (0, 0 with keys, 2, 3, 4)
        s_cnt += 1; prev_counter = counter
        with self.assertRaisesRegex(TypeError, r"function missing required argument 'x' \(pos 1\)"):
            sign()
        counter += 1
        with self.assertRaisesRegex(TypeError, r"function missing required argument 'x' \(pos 1\)"):
            sign(preprocess=lambda a: (float(a),), if_exc=None)
        counter += 1
        with self.assertRaisesRegex(TypeError, r'function takes at most 1 positional argument \(2 given\)'):
            sign(-1, 0)
        counter += 1
        with self.assertRaisesRegex(TypeError, r'function takes at most 1 positional argument \(3 given\)'):
            sign(-1, 0, 1)
        counter += 1
        with self.assertRaisesRegex(TypeError, r'function takes at most 3 arguments \(4 given\)'):
            sign(-1, 0, 1, 5)
        counter += 1
        self.trace(prev_counter, counter, s_cnt, "invalid number of arguments")

        # --- ExplodingNumber, NotImplementedNumber
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

        s_cnt += 1; prev_counter = counter
        with self.assertRaisesRegex(TypeError, r'signum.sign: invalid argument `ExplodingNumber\(-3\.14\)`'):
            sign(ExplodingNumber(-3.14))
        counter += 1
        with self.assertRaisesRegex(TypeError, r'signum.sign: invalid argument `NotImplementedNumber\(-3\.14\)`'):
            sign(NotImplementedNumber(-3.14))
        counter += 1
        self.trace(prev_counter, counter, s_cnt, "Exploding and Not Implemented numbers")

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
        self.trace(prev_counter, counter, s_cnt, "inappropriate types")

        # Testing additional key arguments (preprocess=, is_exc=, both)

        # --- preprocess key, simple argument replacement, string conversion
        s_cnt += 1; prev_counter = counter
        self.assertEqual(sign('5.0', preprocess=lambda a: (float(a),)), 1); counter += 1
        self.assertTrue(isnan(sign('nan', preprocess=lambda a: (float(a),)))); counter += 1
        self.assertEqual(sign(-18, preprocess=lambda a: (float(a),)), -1); counter += 1
        self.trace(prev_counter, counter, s_cnt, "preprocess with simple str replacement")

        # --- preprocess key, argument replacement, treat small number as zero
        s_cnt += 1; prev_counter = counter
        tests = [(-1, -1), (0, 0), (-.187e-17, 0), (5.0, 1)]
        for x, y in tests:
            self.assertEqual(sign(x, preprocess=lambda a: (0 if abs(a) < self.EPS else a,)), y);  counter += 1
        self.trace(prev_counter, counter, s_cnt, "preprocess treating small number as zero")

        # --- preprocess key, replace only string argument, extract number from string
        s_cnt += 1; prev_counter = counter
        numeric_finder = re.compile(r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?")

        def n_extract(s):
            if isinstance(s, str):
                match = numeric_finder.search(s)
                return (float(match.group()),) if match else None
            return None

        self.assertEqual(sign("15 men on the dead man's chest", preprocess=n_extract), 1); counter += 1
        self.assertEqual(sign('Temperature is -.12e+02 °C', preprocess=n_extract), -1); counter += 1
        with self.assertRaisesRegex(TypeError, r"signum.sign: invalid argument `'error'` \(type 'str'\)"):
            sign('error', preprocess=n_extract)
        counter += 1
        self.assertEqual(sign(123, preprocess=n_extract), 1); counter += 1
        self.trace(prev_counter, counter, s_cnt, "preprocess extracting numbers from str")

        # --- preprocess key, replace result, permits complex arguments
        s_cnt += 1; prev_counter = counter
        tests = [(-1+1j, '(-0.7071067811865475+0.7071067811865475j)'), (-18.4, '-1')]

        def c_prep(z):
            if z == 0 or not isinstance(z, complex): return None
            # complex z != 0
            return (0, z/abs(z))

        for x, y in tests:
            self.assertEqual(str(sign(x, preprocess=c_prep)), y); counter += 1
        self.trace(prev_counter, counter, s_cnt, "preprocess permitting complex arguments")

        # --- preprocess key, replace result, float result for 'float' and 'Decimal', sign recursion
        s_cnt += 1; prev_counter = counter
        tests = [(-5, -1, int), (-5.0, -1.0, float), (Decimal(-5.5), -1.0, float)]
        for x, y, t in tests:
            self.assertEqual((s := sign(x, preprocess=lambda a: (a, float(sign(a))) if isinstance(a, (float, Decimal)) else None)), y)
            self.assertIsInstance(s, t); counter += 1
        self.trace(prev_counter, counter, s_cnt, "preprocess with float result and sign recursion")

        # --- preprocess key, replace result or argument, treat small number as zero differently
        s_cnt += 1; prev_counter = counter
        tests = [(-1, -1), (0, 0), (-.187e-17, 0), (5.0, 1)]
        ppl = lambda x: (x, 0) if abs(x) < self.EPS else (x,)
        for x, y in tests:
            self.assertEqual(sign(x, preprocess=ppl), y); counter += 1
        self.trace(prev_counter, counter, s_cnt, "preprocess replacing result or argument")

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
        self.trace(prev_counter, counter, s_cnt, "if_exc key")

        # --- both preprocess and if_exc key
        s_cnt += 1; prev_counter = counter
        tests = [(-5, '-1', int), (-5.0, '-1.0', float),
                 (Decimal(-5.5), '-1.0', float), ('error', 'None', type(None))]
        for x, y, t in tests:
            self.assertEqual(str(s := sign(x, preprocess=lambda a: (a, float(sign(a))) if isinstance(a, (float, Decimal)) else None, if_exc=(None,))), y)
            self.assertIsInstance(s, t); counter += 1
        self.trace(prev_counter, counter, s_cnt, "both preprocess and if_exc")

        self.buffer.append(f'\nSuccess: {counter} tests passed in {s_cnt} sections.\n')
        print('\n'.join(self.buffer), flush=True)

if __name__ == '__main__':
    original_stdout_params = {'encoding': sys.stdout.encoding, 'errors': sys.stdout.errors}
    original_stderr_params = {'encoding': sys.stderr.encoding, 'errors': sys.stderr.errors}
    # Switch sys.stdout and sys.stderr to 'utf-8' encoding
    sys.stdout.reconfigure(encoding=UTF8)
    sys.stderr.reconfigure(encoding=UTF8)

    unittest.main()

    # Restore stdout and stderr
    sys.stdout.reconfigure(**original_stdout_params)
    sys.stderr.reconfigure(**original_stderr_params)
