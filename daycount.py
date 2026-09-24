"""Day count conventions.

0   actual/actual — Number of days in both a period and a year is the actual number of days. The year is the actual number of days from the first date to the same date one year later, with 29 February rolling back to 28 February.
1   30/360 SIA — Year fraction is calculated based on a 360 day year with 30-day months, after applying the following rules: If the first date and the second date are the last day of February, the second date is changed to the 30th. If the first date falls on the 31st or is the last day of February, it is changed to the 30th. If after the preceding test, the first day is the 30th and the second day is the 31st, then the second day is changed to the 30th.
2   actual/360 — Number of days in a period is equal to the actual number of days, however the number of days in a year is 360.
3   actual/365 — Number of days in a period is equal to the actual number of days, however the number of days in a year is 365 (even in a leap year).
4   30/360 PSA — Number of days in every month is set to 30 (including February). If the start date of the period is either the 31st of a month or the last day of February, the start date is set to the 30th, while if the start date is the 30th of a month and the end date is the 31st, the end date is set to the 30th. The number of days in a year is 360.
5   30/360 ISDA — Number of days in every month is set to 30, except for February where it is the actual number of days. If the start date of the period is the 31st of a month, the start date is set to the 30th while if the start date is the 30th of a month and the end date is the 31st, the end date is set to the 30th. The number of days in a year is 360.
6   30E/360 — Number of days in every month is set to 30 except for February where it is equal to the actual number of days. If the start date or the end date of the period is the 31st of a month, that date is set to the 30th. The number of days in a year is 360.
7   actual/365 Japanese — Number of days in a period is equal to the actual number of days, except for leap days (29th February) which are ignored. The number of days in a year is 365 (even in a leap year). A leap day is ignored when it falls after the first date and on or before the second date, as in QuantLib's Actual365Fixed(NoLeap).

https://www.mathworks.com/help/fininst/day-count-basis.html
"""

import pandas as pd

YEAR_DAYS = {1: 360, 2: 360, 3: 365, 4: 360, 5: 360, 6: 360, 7: 365}


def _dates(t1, t2, basis):
    t1 = pd.to_datetime(t1)
    t2 = pd.to_datetime(t2)
    if t1 > t2:
        raise ValueError("t1 is greater than t2")
    if basis not in range(8):
        raise ValueError("basis must be an integer from 0 to 7")
    return t1, t2


def day_count(t1, t2, basis):
    t1, t2 = _dates(t1, t2, basis)
    d1, d2 = t1.day, t2.day
    feb_end1 = t1.month == 2 and t1.day == t1.days_in_month
    feb_end2 = t2.month == 2 and t2.day == t2.days_in_month
    match basis:
        case 0 | 2 | 3:  # actual/actual, actual/360, actual/365
            return (t2 - t1).days
        case 7:  # actual/365 (Japanese)
            leap_days = 0
            for year in range(t1.year, t2.year + 1):
                if (year % 400 == 0) or (year % 100 != 0 and year % 4 == 0):
                    if t1 < pd.Timestamp(year, 2, 29) <= t2:
                        leap_days += 1
            return (t2 - t1).days - leap_days
        case 1:  # 30/360 (SIA)
            if feb_end1 and feb_end2:
                d2 = 30
            if d1 == 31 or feb_end1:
                d1 = 30
            if d1 == 30 and d2 == 31:
                d2 = 30
        case 4:  # 30/360 (PSA)
            if d1 == 31 or feb_end1:
                d1 = 30
            if d1 == 30 and d2 == 31:
                d2 = 30
        case 5:  # 30/360 (ISDA)
            if d1 == 31:
                d1 = 30
            if d1 == 30 and d2 == 31:
                d2 = 30
        case 6:  # 30E/360
            if d1 == 31:
                d1 = 30
            if d2 == 31:
                d2 = 30
    return 360 * (t2.year - t1.year) + 30 * (t2.month - t1.month) + d2 - d1


def year_count(t1, t2, basis):
    if basis == 0:  # actual/actual
        t1, t2 = _dates(t1, t2, basis)
        return (t2 - t1).days / (t1 + pd.DateOffset(years=1) - t1).days
    return day_count(t1, t2, basis) / YEAR_DAYS[basis]
