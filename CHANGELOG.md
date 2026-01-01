# Changelog

All notable changes to this project will be documented in this file.

## [1.1.5] - 2026-01-01 (New Year Edition)
- Fixed usage of `import` in examples.

## [1.1.4] - 2026-01-01 (New Year Edition)
- Fixed metadata for Github Actions in release.yml.

## [1.1.3] - 2026-01-01 (New Year Edition)
- Fixed metadata for Github Actions in pyproject.toml.

## [1.1.2] - 2026-01-01 (New Year Edition)
- Fixed broken relative links in README on PyPI (switched to absolute GitHub URLs).

## [1.1.1] - 2026-01-01 (New Year Edition)
- Corrected links and typos in documentation.

## [1.1.0] - 2025-12-31 (New Year Edition)
- **Refactored core logic**:
    - Replaced the 27-state switch with optimized conditional branching.
    - Improved execution speed for valid numeric types.
- **Added new keyword parameters**:
    - `preprocess`: supports custom argument transformation or early return of a pre-calculated result.
    - `if_exc`: provides exception safety by returning a fallback value instead of raising errors.
- **Expanded test suite**:
    - Increased validation cases from 51 to 92.
    - Added comparative benchmarking against v1.0.2, and memory leak test.

## [1.0.2] - 2025-12-25 (Christmas Edition)
- The prototype block deleted from `test-signum.py`.

## [1.0.1] - 2025-12-25 (Christmas Edition)
- Initial public release on PyPI as `csignum-fast`.
- Added project URLs and metadata for GitHub integration.

## [1.0.0] - 2025-12-25 (Christmas Edition)
### Added
- Initial stable release of the `signum` C++ extension.
- High-performance universal `sign()` function; returns `-1` for negative arguments, `0` for zeroes, `1` for positives.
- Support for all numeric types via duck typing (int, float, Decimal, Fraction, etc.).
- Robust handling of edge cases: signed zeros (returns `0`), infinities (returns `-1` or `1`), and NaNs (returns float `nan`).
- Branchless ternary logic implementation for maximum execution speed.
- Informative `TypeError` diagnostics for incompatible (non-numeric, non-scalar) types.
- Test suite with 51 test cases covering various scenarios.
