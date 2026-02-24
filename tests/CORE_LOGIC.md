## The Triple Check strategy: Core Logic of the Signum Implementation

1. **Argument analysis.** As always in programming, "no step without errors": invalid number of arguments and keyword misspelling are quite possible.
2. **Obtain** `gt = (x > 0) + 1`**,** `lt = (x < 0) + 1`**, and** `eq = (x == 0) + 1`, in this order. (In the implementation, variables `gt`, `lt`, and `eq` don’t exist, and I don’t add 1 for performance. The result is the same.)
    * With **Rich Comparisons**, these results may be 0 (-1+1, Error), 1 (0+1, `False`), and 2 (1+1, `True`).
    * If I get an error, I immediately go to error processing (step 7).
    * After obtaining `lt`, I immediately calculate the **potential** result `sign = gt - lt`.
3. **Calculate** `stat_idx = (gt * lt * eq) % 4`. (It is implemented **branchlessly**, **without** multiplication or division.)
    * The product `gt * lt * eq` may be 1, 2, 4, or 8.
    * The product can’t be 0, because I immediately jump to error processing (step 7) if I get 0 (Error) as a multiplier.
    * `stat_idx` may be 0 (obtained from 4 or 8 by `mod 4`), 1, or 2.
4. `stat_idx == 0` **means strange combinations:** two `True` and one `False` (4 == 2\*2\*1 == 2\*1\*2 == 1\*2\*2), or three `True` (8 == 2\*2\*2). Jump to error processing (step 7).
5. `stat_idx == 1` **means three** `False` (1 == 1\*1\*1). This behavior usually corresponds to the `float('nan')`, or to the pair of`sympy` zeroes (`sympy.Number(0)` compared with `sympy.Float(0.0)`). Jump to error processing (step 7).
6. `stat_idx == 2` **means two** `False` **and one** `True` (2 == 2\*1\*1 == 1\*2\*1 == 1\*1\*2). **It’s a normal number**, and `sign` is returned.
7. **Error processing**.

    7.1. **Check for NaN:** if `stat_idx == 0` and `x != x`, `x` is `NaN`. If `stat_idx != 0`, or the comparions issues `true` or fails, I try to use `nb_float` slot: `x` is converted to Python `float`, then to C++ `double`. C++ `isnan()` is just one processor command. If there is no `nb_float`, jump to step 7.3. (Note for the future: The strange case of `sympy` zeroes should also be analyzed after conversion to C++ `double`.)

    7.2. **If** `x` **is** `NaN`, `float('nan')` is returned. I noted for the future that returning `x` would keep the type of `NaN`. (If `x == 0` and its type implements IEEE 754, returning `x` would keep the type and sign of zero.)

    7.3. **If** `x` **is not** `NaN`, an error is raised.

[**Back to Main README**](../README.md)
