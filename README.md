# Day Count Conventions

A lightweight Python implementation of eight financial day count conventions, an alternative to QuantLib for counting the days and the year fraction between two dates. Each rule follows the MathWorks day count basis definitions, stated in the docstring of `daycount.py`, and pandas is the only dependency.

## Usage

Python 3.13 with pandas.

```python
import pandas as pd
from daycount import day_count, year_count

t1 = pd.to_datetime("2025-09-10")
t2 = pd.to_datetime("2027-12-15")
days = day_count(t1, t2, basis=0)    # 826
years = year_count(t1, t2, basis=0)  # 2.263014
```

Both functions take dates with `t1` on or before `t2` and an integer `basis` from 0 to 7, and raise `ValueError` otherwise.

## Bases

| `basis` | Convention |
|---|---|
| 0 | actual/actual |
| 1 | 30/360 (SIA) |
| 2 | actual/360 |
| 3 | actual/365 |
| 4 | 30/360 (PSA) |
| 5 | 30/360 (ISDA) |
| 6 | 30E/360 (European) |
| 7 | actual/365 (Japanese) |

## Reference

MathWorks, [Day count basis](https://www.mathworks.com/help/fininst/day-count-basis.html).
