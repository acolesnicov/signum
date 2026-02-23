# My approach to the `sign` implementation

My implementation of `sign` from the very beginning (v1.0.0) and up to the upcoming release (v1.3.1), and further, was and will be based on the four principles: **Universality, Robustness, High Performance, Versatility.** These principles are shown here exactly in the order of their importance for my implementation.

### Universality
It’s my most important principle. My function should work with **any argument**, with **any type**, producing at least informative and understandable error message.

### Robustness
To provide **universality** and to guarantee absence of accidental results, and worser things like segmentation faults, my implementation relies on a **Triple Check** strategy:

1. Every input `x` is subjected to **all three** comparisons: `(x > 0)`, `(x < 0)`, and `(x == 0)`.
2. All **27** possible combinations of the three ternary outcomes (Error, False, True) are evaluated.
3. This allows the function to reliably classify **even the most insane** objects, including `NaN` of different types, `sympy` zeroes, non-scalar arguments, and types with broken comparison protocols.

Memory leak is thoroughly prevented (tested at 9 mln. `sign` calls).

### Performance
**Performance vs. safety** is **the** dilemma. From the very beginning my core logic was strictly **branchless**. It avoids `if-else` blocks, divisions, and multiplications, while mathematically the result is equivalent to the use of these beautiful but slow things (see [CORE_LOGIC](https://github.com/acolesnicov/signum/blob/main/tests/CORE_LOGIC.md) and comments in [`signum.cpp`](https://github.com/acolesnicov/signum/tree/main/signum.cpp) for detais). With maximal optimization in the C++ layer supported by the detailed compiler hints, I could take into account each processor tact and each cache bit. This ensures the CPU pipeline always remains full.

Python can’t easily detect all anomalies (and the theory can’t help), but a dedicated C++ extension can—and it does so without losing a single microsecond.

If you need even better performance, a simplified `fastsign(x)` has been available since v1.2.3. It is a straightforward implementation of the Python prototype included in the tests as [`fastsign.py`](https://github.com/acolesnicov/signum/tree/main/tests/fastsign.py). The Python version consists of 21 lines of code and 3 lines of headers. From these 17 lines of pure code, we have 4 lines of logic and 17 lines of exception handling (1:4). In C++, this proportion is **significantly worse.**

### Versatility
This implementation provides additional arguments, which help to adjust the `sign` results to user’s needs. I selected supposedly popular options that can be implemented without loss in performance. **Practice** will show if these additions became widely used.

[**Back to Main README**](README.md)
