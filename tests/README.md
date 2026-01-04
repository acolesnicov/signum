# Signum Test Suite

This directory contains validation and performance tools for the `csignum-fast` library (`*.py`), and test results (`*.txt`).

## Test Files

* `testing.py`: An auxiliary module. Contains things common for all tests, for example, the `detect_version` function.
* `simple_test_signum.py`: The prototype that prints test results for visual check; does not use assertions. 92 cases.
* `test_signum.py`: The same 92 cases with assertions and `unittest`.
* `leak_test.py`: seven million-repeating loops for memory leak detection.
* `55_test_signum.py`: 55 tests from the whole 92-tests set, which are common for version 1.0.2 and versions 1.1.0+. Repeats 100,000 times to estimate execution time. Includes tests that raise exceptions. Three results for versions 1.0.2, 1.1.0+, and 1.2.0.
* `41_test_signum.py`: **Pure Math**: 41 tests from 55 that do not raise exceptions. Repeats 100,000 times to estimate execution time. Three results for versions 1.0.2, 1.1.0+, and 1.2.0.

## Benchmarking

Results (`*.txt`) were obtained with Python 3.13.5 (AMD64) on Lenovo ThinkPad (processor 11th Gen Intel(R) Core(TM) i7-1165G7 @ 2.80GHz, RAM 32.0 GB) under Windows 11 Pro 25H2.

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

2.  Run the desired test:
```bash
python tests/test_signum.py
```

## Building from Source

To build and test the library locally:

1.  Install build tools and dependencies:
```bash
pip install build setuptools psutil sympy
```

2.  Install from the project root:
```bash
pip install .
```

3.  Run any test file from the `tests/` directory.

[**Back to Main README**](../README.md)
