# Signum Test Suite

This directory contains validation and benchmarking tools for the `csignum-fast` library (`*.py`), and test results (`*.txt`).

## Test Files

* `testing.py`: An auxiliary module. Contains items common for all tests, for example, the `detect_version()` function.
* `simple_test_signum.py`: The prototype that prints test results for visual check; does not use assertions. 210 cases. Works for all versions: for older versions, passes only the corresponding subset of tests.
* `test_signum.py`: The same 210 cases plus 53 cases testing equivalence of `sign` and `fastsign` (total 263) with assertions and `unittest`. Current version only.
* `leak_test.py`: nine million-repeating loops for memory leak detection. Current version only.
* `57_tests_signum.py`: 57 tests from the whole 210-tests set, which are common for all versions. Repeats 100,000 times to estimate execution time. Includes tests that raise exceptions.
* `fastsign_57_tests.py`: The same 57 tests for `fastsign`.
* `41_tests_signum.py` (**Pure Math**): 41 tests from 57 that do not raise exceptions. Repeats 100,000 times to estimate execution time.
* `fastsign_41_tests.py`: The same 41 tests for `fastsign`.
* `fastsign.py`: The Python prototype of the function `signum.fastsign(x)`.
* `CORE_LOGIC.md`: The description of internal sign logic.
* `*.txt`: Test results.

## Benchmarking

Results (`*.txt`) were obtained with **Python 3.13.5 (AMD64)** on a **Lenovo ThinkPad** (processor 11th Gen Intel® Core™ i7-1165G7 @ 2.80GHz, RAM 32.0 GB) running **Windows 11 Pro 25H2** under the **“Best performance”** power plan.

For consistent results, all benchmarking scripts (except `test_signum.py`) automatically set **High Process Priority** via `psutil`.

Benchmarks were conducted using the **Best-of-N** method with the `41_tests_signum.py` **Pure Math** suite. This eliminates jitter from background OS activities (antivirus, network tasks, system updates, notifications, etc.), capturing the true peak performance of the extension.

| Version | 4.1M calls (s) | Speedup vs v1.0.2 (%) | Edition | Features | Status |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 1.0.2 | 6.6877 | - | Christmas | Base `sign(x)` | Legacy, 7.1% slower  |
| 1.1.0+ | 7.2759 | -8.8% | New Year | preprocess=, if_exc= | Intermediate, 15.9% slower |
| 1.2.2 | 6.2133 | +7.1% | Gold | codeshift=, max optimization | **The Recommended Champion** |

**Efficiency Note 1:** The transition from v1.1.0+ to v1.2.0 resolved previous performance regressions, resulting in a 15.9% internal throughput improvement because of refined optimizations in C++ code.

**Efficiency Note 2:** For `int` and `float`, `fastsign` is up to 1.5 times faster than `sign`. The causes: it has only one argument and skips argument processing found in `sign`; it doesn't perform all three comparisons (`x > 0`, `x < 0`, `x == 0`) but returns after the first success.

## How to run tests

1.  Ensure the library and dependencies are installed:
```bash
pip install csignum-fast psutil sympy
```

2.  Run the desired test under Linux/macOS:
```bash
python tests/test_signum.py
python tests/test_signum.py >> tests/test_signum.txt 2>&1
```
or under Windows:
```bash
python tests\test_signum.py
python tests\test_signum.py >> tests\test_signum.txt 2>&1
```
**Note:** The `test_signum.py` script outputs to both `stdout` (headers and traces) and `stderr` (`unittest` results). To capture the complete log into a single file, use `2>&1`.

## Building from Source

To build and test the library locally:

1.  Install build tools and dependencies:
```bash
pip install build setuptools psutil sympy
```

2.  Build from the project root:
```bash
python -m build
```

3.  Install from the project root:
```bash
pip install .
```

4.  Run any test file from the `tests` directory as shown above.

[**Back to Main README**](../README.md)
