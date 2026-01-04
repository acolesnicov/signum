import os
import re
import sys
import time

__all__ = [
           'SHORT_SIMPLE_TEST',
           'EPS',
           'UTF8',
           'PIRATES',
           'numeric_finder',
           'file_name',
           'get_passes',
           'n_extract',
           'c_prep',
           'MyNumber',
           'ExplodingNumber',
           'NotImplementedNumber',
           'detect_version',
           'trace',
           'success',
           'open_devnull',
           'close_devnull',
           'OutputControl',
          ]
          
### Tested entities

## Constants

# Restriction for simple_tests_signum.py
SHORT_SIMPLE_TEST = 2 # 0: pass only tests common with v1.0.2 to compare timing
                      # 1: pass only tests common with v1.1.0 (this includes v1.0.2)
                      # 2: pass all tests (current v1.2.0)

EPS = 1e-9

UTF8 = 'utf-8'

MAX_PASSES = {
    'simple_test_signum': 10000, 
    '41_tests_signum':   100000, 
    '57_tests_signum':   100000, 
    'leak_test':        1000000,
    'default':             1000,
}

PIRATES = "☠️15 men on the dead man's chest☠️"

numeric_finder = re.compile(r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?")

## Functions

# Get file name from path
def file_name(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]

# Select MAX_PASSES for a test by file name
def get_passes(file_path):
    return MAX_PASSES.get(file_name(file_path), MAX_PASSES['default'])

## Functions used to preprocess

# Number extraction from str
def n_extract(s):
    if isinstance(s, str):
        match = numeric_finder.search(s)
        return (float(match.group()),) if match else None
    return None

# sign(complex) with recursion
def c_prep(z):
    if z == 0 or not isinstance(z, complex): return None
    # complex z != 0
    return (0, z/abs(z))

## Custom comparable classes

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

### Service entities

# Detecting version
def detect_version():
    if not (signum_mod := sys.modules.get('signum')): # 'signum' not imported
        raise ImportError(
            "Module 'signum' not found in sys.modules\n"
            "Make sure you have 'from signum import sign' in your test script "
            "before calling 'success()' or 'detect_version()'"
        )
    if hasattr(signum_mod, '__version__'): # v1.2.0+
        return signum_mod.__version__
    try:
        signum_mod.sign(0, preprocess=None)
        return("1.1.0+")
    except TypeError:
        return("1.0.2")

## Tracing

def trace(pcnt, cnt, scnt, what=None):
    delta = cnt - pcnt
    suffix = 's' if delta != 1 else ''
    if what:
        # trace1: Полный отчет
        return f"{delta:2} test{suffix:1} for Sec. {scnt:2}: {what} passed, total {cnt:3} tests passed"
    # trace2: Лаконичный отчет (быстрее за счет отсутствия 'what')
    return f"   --- {delta:2} test{suffix:1} for Sec. {scnt:2} passed, total {cnt:3} tests passed"
    
def success(counter, s_cnt=None, start_time=None, passes=None):
    version = detect_version()
    sections = ''
    if s_cnt: sections = f' from {s_cnt} sections'
    seconds = ''
    if start_time: seconds = f' in {time.perf_counter() - start_time:>9.4f}s'
    reps = ''
    if passes: reps = f' (passes: {passes}; sign calls: {passes*counter})'
    return f'Success of v{version}: {counter} tests{sections} passed{seconds}{reps}.' 

## os.devnull

def open_devnull():
    return open(os.devnull, 'w', encoding=UTF8)

def close_devnull(f):
    if f:
        try:
            f.flush()
        finally:
            f.close()    

# Class to switch sys.stdout and sys.stderr and to produce devnull
class OutputControl:
    def __init__(self):
        self.original_stdout_params = {'encoding': sys.stdout.encoding, 'errors': sys.stdout.errors}
        self.original_stderr_params = {'encoding': sys.stderr.encoding, 'errors': sys.stderr.errors}
        
    def set_utf8(self):
        # Switch sys.stdout and sys.stderr to 'utf-8' encoding
        sys.stdout.flush(); sys.stdout.reconfigure(encoding=UTF8)
        sys.stderr.flush(); sys.stderr.reconfigure(encoding=UTF8)
        
    def reset_from_utf8(self):    
        # Restore stdout and stderr
        sys.stdout.flush(); sys.stdout.reconfigure(**self.original_stdout_params)
        sys.stderr.flush(); sys.stderr.reconfigure(**self.original_stderr_params)
