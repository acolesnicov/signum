# csignum-fast
![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/release-New%20Year%20Edition-blue.svg)
![Tests](https://img.shields.io/badge/tests-92%20passed-brightgreen.svg)
![PyPI Version](https://img.shields.io/pypi/v/csignum-fast.svg)

**A versatile, high-performance C++ implementation of the universal sign function for Python.**

*Released on January 1, 2026* ❄️ *New Year Edition.*

Versions 1.1.1+ corrected links and typos in documentation, and metadata for Github, after a major internal refactor in v1.1.0.

## Key Features

1.  **Uniform Results**: Always returns only `-1`, `0`, or `1` as an `int` for valid numeric comparisons.
2.  **Correct Edge Case Handling**:
    * `sign(+0.0)` and `sign(-0.0)` return `0`.
    * `sign(inf)` returns `1`, `sign(-inf)` returns `-1`.
    * For any **NaN** (float NaN, Decimal NaN, etc.), it returns `math.nan` (float).
3.  **Comprehensive Duck Typing**: Delegates comparisons to the argument's class. Works seamlessly with:
    * Built-in `int` (including arbitrary-precision), `bool`, and `float`.
    * `fractions.Fraction` and `decimal.Decimal`.
    * Any existing and future objects that support rich comparisons with numbers.
4.  **Informative Error Handling for Easy Debugging**: Provides clear, descriptive `TypeError` messages when passed non-numeric, non-scalar, or incomparable arguments.
5.  **⚡ High Performance**: Branch-optimized C++20 core.
6.  **✅ Thoroughly Tested**: Tested on 92 cases including different types, edge cases, new custom class, and inappropriate arguments. Also tested memory leaks and benchmarking against v1.0.2.
7.  **✨ Pre-processing Engine**: Use the `preprocess` keyword argument to transform input before calculation or trigger an "Early Exit" (recursion permitted).
8.  **🛡️ Exception safety**: The `if_exc` keyword argument allows you to define a fallback value (like `None`, `math.nan`, or `-2`) instead of crashing on invalid types.

## Installation

```bash
pip install csignum-fast
```

## Standard Usage

```python
from signum import sign
from decimal import Decimal

print(sign(-10**100))       # -1
print(sign(3.14))           #  1
print(sign(Decimal("0.0"))) #  0
print(sign(float('-nan')))  # nan
```

## Advanced Usage (New features since v1.1.0)

### ☢️ Attention: Contract Programming!
For productivity reasons, keyword argument values are **not checked** by the `sign` function. It is your responsibility to:
* Pass a **`callable`** with one argument for `preprocess` (must return `None` or a `tuple`).
* Pass a **`tuple`** for `if_exc`.

*Passing incorrect types to these parameters may lead to undefined behavior or faults.*

### ⚡ Custom Pre-processing with `preprocess`
You can pass a `callable` to transform the input. The argument of `callable` is the positional argument of `sign`. The `callable` should support a special return protocol:
- Return `None`: Proceed with usual calculation.
- Return `(value,)`: Proceed with calculation using `value` as an argument. Why a `tuple`? Use `(None,)` to return `None` as a `value`.
- Return `(any, result)`: Early Exit. Immediately return `result` as the final answer. `any` is ignored.

```python
from signum import sign

from decimal import Decimal
from fractions import Fraction
from math import nan, inf
import re

# Convert str to float; uses lambda as callable
sign('5.0', preprocess=lambda a: (float(a),)) # Returns 1 (instead of exception)

# Treat small number as zero through argument replacement only
EPS = 1e-9
sign(-.187e-17, preprocess=lambda a: (0 if abs(a) < EPS else a,)) # Returns 0 (instead of -1)

# Treat small number as zero through argument or result replacement; uses variable as callable
ppf1 = lambda x: (x, 0) if abs(x) < EPS else (x,)
sign(-.187e-17, preprocess=ppf1) # Returns 0 (instead of -1)

# Extract number from string, replace only string argument; supplies function as callable
numeric_finder = re.compile(r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?")

def n_extract(s):
    if isinstance(s, str):
        match = numeric_finder.search(s)
        return (float(match.group()),) if match else None
    return None

sign("☠️ 15 men on the dead man's chest☠️", preprocess=n_extract) # Returns sign(15) == 1

# Do you want sign(complex) instead of exception?
def c_prep(z):
    if z == 0 or not isinstance(z, complex): return None
    # complex z != 0
    return (0, z/abs(z))

sign(-1+1j, preprocess=c_prep) # Returns (-0.7071067811865475+0.7071067811865475j)

# numpy flavor: float result for float or Decimal argument; uses recursive call of sign
ppf2 = lambda a: (a, float(sign(a))) if isinstance(a, (float, Decimal)) else None
sign(-5.0, preprocess=ppf2) # Returns -1.0 (instead of -1)
```

### 🛡️ Exception Safety with `if_exc`
With this keyword, you can avoid try-except blocks. If `sign()` encounters an incompatible type, it will return your fallback value instead of raising a `TypeError`. `if_exc` should be a tuple that permits you to pass `None` as the fallback value through `if_exc=(None,)`. (Default `if_exc=None` is totally different).
```python
import math
from signum import sign

# Returns -2 instead of crashing
res = sign("not a number", if_exc=(-2,))
```

### You can use both keyword arguments at once
With `preprocess`, you replace arguments (or results) in specific cases, while `if_exc` prevents exceptions for all that remains. 

## 📊 Performance & Quality Assurance

### Benchmark Results
Versions 1.1.0+ maintain near-zero overhead (+0.8% latency) despite adding logic for new arguments. See details in the "Benchmarking" section in [README for tests](https://github.com/acolesnicov/signum/tree/main/tests/README.md).

### Reliability
- **Memory Safety:** Verified with long-run leak tests (0 bytes leaked over 4M iterations).
- **Test Coverage:** 92 validation cases (up from 51 in v1.0.2).

## License
This project is licensed under the **MIT License**. See the [LICENSE](https://github.com/acolesnicov/signum/blob/main/LICENSE) file for details.

## Author
**Alexandru Colesnicov**: [GitHub Profile](https://github.com/acolesnicov)
