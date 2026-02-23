from math import nan as nan, isnan as isnan

def fastsign(x):
    err = None;
    try:
        if x >  0:   return  1
        if x <  0:   return -1
        if x == 0:   return  0
        if isnan(x): return nan
        raise TypeError(f"Unusual results with type {type(x)}")
    except (TypeError, ValueError, NotImplementedError) as e:
        err = e
        if not isinstance(x, str):
            try:
                d = float(x)
                if isnan(d): return nan
                if d == 0.0: return  0
                if d >  0.0: return  1
                if d <  0.0: return -1
            except (TypeError, ValueError) as e:
               err = e

    raise TypeError(
              f"Python fastsign({repr(x)}) for type {type(x)}: cannot compare or check for NaN"
          ) from err

__all__ = [fastsign,]
