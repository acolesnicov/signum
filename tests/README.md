# Signum Test Suite

This directory contains validation and benchmarking tools for the `csignum-fast` library (`*.py`), and test results (`*.txt`).

## Test Files

* `testing.py`: An auxiliary module. Contains things common for all tests, for example, the `detect_version` function.
* `simple_test_signum.py`: The prototype that prints test results for visual check; does not use assertions. 121 cases. Works for all versions: for older versions, passes only the corresponding subset of tests.
* `test_signum.py`: The same 121 cases with assertions and `unittest`. Current version only.
* `leak_test.py`: seven million-repeating loops for memory leak detection. Current version only.
* `57_test_signum.py`: 57 tests from the whole 121-tests set, which are common for all versions. Repeats 100,000 times to estimate execution time. Includes tests that raise exceptions.
* `41_test_signum.py` (**Pure Math**): 41 tests from 57 that do not raise exceptions. Repeats 100,000 times to estimate execution time. Results `41_test_signum.txt` are accumulated for all versions (by >>).

## Benchmarking

Results (`*.txt`) were obtained with Python 3.13.5 (AMD64) on Lenovo ThinkPad (processor 11th Gen Intel(R) Core(TM) i7-1165G7 @ 2.80GHz, RAM 32.0 GB) under Windows 11 Pro 25H2, with **"Best performance"** power plan setting. 

**For more consistent benchmarking results, all tests except `test_signum.py` internally attempt to set high process priority via psutil.**

The 0.8% overhead mentioned in the [main documentation](../README.md) was measured by running 100,000 iterations of 41 **Pure Math** tests (total 4,100,000 `sign` calls), and comparing [v1.0.2](41_tests_signum_v1.0.2.txt) vs [v1.1.0+](41_tests_signum_v1.1.0.txt). The resuls are collected in the table:
| Version | Timing (s) | Overhead (s) | Overhead (%) | Per call (μs) |
| :---: | :---: | :---: | :---: | :---: |
| 1.0.2 | 7.00 | - | - | 1.71 |
| 1.1.0+ | 7.06 | 0.06 | 0.8% | 1.72 | 

## How to run

1.  Ensure the library and dependencies are installed:
```bash
pip install csignum-fast psutil sympy
```

2.  Run the desired test under Linux:
```bash
python tests/test_signum.py
python tests/test_signum.py >> tests/test_signum.txt 2>&1
```
or under Windows:
```bash
python tests\test_signum.py
python tests\test_signum.py >> tests\test_signum.txt 2>&1
```
`test_signum.py` is unique: the result is printed both through `sys.stdout` (test header and section trace) and `sys.stderr` (the `unittest` module), so you need `2>&1` to catch all that in a file.

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
