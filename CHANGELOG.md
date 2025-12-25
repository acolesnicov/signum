# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2025-12-25 (Christmas Edition)
### Added
- Initial stable release of the `signum` C++ extension.
- High-performance universal `sign()` function; returns `-1` for negative arguments, `0` for zeroes, `1` for positives.
- Support for all numeric types via duck typing (int, float, Decimal, Fraction, etc.).
- Robust handling of edge cases: signed zeros (returns `0`), infinities (returns `-1` or `1`), and NaNs (returns float `nan`).
- Branchless ternary logic implementation for maximum execution speed.
- Informative `TypeError` diagnostics for incompatible (non-numeric, non-scalar) types.
- Test suite with 51 test cases covering various scenarios.
