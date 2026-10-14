# date_features

Expand a date column into calendar parts, **cyclical sine/cosine encodings**, and a **public-holiday flag** for regression, ARIMA with exogenous terms, or clustering.

Formula: `source/python-in-excel/functions/date_features.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/TimeSeries.py` (time series functions only) or the whole `init/PaulPythonLibrary.py`.

In a PY cell (output **Excel value**):

```python
date_features("A2:A400")
date_features("A2:A400", calendar=False)
date_features("A2:A400", fourier=2)
date_features("A2:A400", country_holiday="US")
date_features("A2:A400", country_holiday=None)
date_features("Table1[Date]")
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Date column, or a range/table containing dates. Ref string, DataFrame, Series, or list. The first column that parses as dates is used. |
| `cyclical` | No | Add the sin/cos pairs. Default `True`. |
| `calendar` | No | Add the plain calendar parts. Default `True`. |
| `fourier` | No | Harmonics per cycle. Default `1`. |
| `country_holiday` | No | Two-letter country code for the `is_holiday` column. `'UK'` (default, England & Wales) or `'US'` (federal). `None` or `False` disables the column. |
| `headers` | No | First row is headers when `data` is a ref string. Default `False`. |

Excel serial numbers are read with the `1899-12-30` origin, so a raw date column works whether Excel hands over real dates or serials. Blank or unparseable dates keep their row and spill blank features.

## Why sine and cosine

Month `12` and month `1` are one step apart in time but eleven apart as numbers, so a model reads December and January as opposites. Encoding the position on a circle removes that jump:

```text
angle = 2 * pi * k * pos / period
sin   = SIN(angle)
cos   = COS(angle)
```

`pos` is 0 at the start of the cycle (January, day 1, Monday) and `k` is the harmonic. February and December end up with the same `month_cos` (`0.866025`) and opposite `month_sin` (`+0.5` and `-0.5`) — equally far from January in either direction. Use both columns together; either one alone is ambiguous.

`fourier=2` adds a second wave at double frequency (`month_sin_2`, `month_cos_2`), which lets a model fit a seasonal shape that is not a plain single peak per year.

## Cycles

| Prefix | Period | Position |
|--------|--------|----------|
| `month_sin` / `month_cos` | 12 months | `month - 1` |
| `day_sin` / `day_cos` | days in that month (28–31) | `day - 1` |
| `dayofweek_sin` / `dayofweek_cos` | 7 days | `dayofweek` (Monday = 0) |
| `dayofyear_sin` / `dayofyear_cos` | 365, or 366 in a leap year | `dayofyear - 1` |

Day-of-month and day-of-year use the true length of the month or year, so the encoding stays continuous across short months and leap years.

## Result

A DataFrame with one row per input date. Set the PY cell to **Excel value** to spill it.

| Column | Notes |
|--------|-------|
| `date` | Parsed date, always present. |
| `year`, `quarter`, `month`, `week`, `day`, `dayofweek`, `dayofyear`, `days_in_month` | `calendar=True`. `week` is the ISO week; `dayofweek` is Monday `0` to Sunday `6`. |
| `is_weekend`, `is_month_end`, `is_quarter_end` | `calendar=True`. `1` or `0`. |
| `month_sin` … `dayofyear_cos` | `cyclical=True`. Two columns per cycle per harmonic. |
| `is_holiday` | `country_holiday` is set. `1` on a public holiday, `0` otherwise. |

Default `date_features` spills 21 columns. `calendar=False` gives 10 (date plus encodings plus holiday); `country_holiday=None` drops `is_holiday`.

## Holiday calendars

Holidays are computed algorithmically — no external `holidays` package is needed (it is not available in Python in Excel). Easter uses the anonymous Gregorian algorithm (Meeus/Jones/Butcher). Fixed dates that fall on a weekend are moved to the next Monday (Saturday → Monday, Sunday → Monday).

| Country | Code | Holidays |
|---------|------|----------|
| UK (England & Wales) | `'UK'` | New Year's Day, Good Friday, Easter Monday, Early May bank holiday (1st Mon in May), Spring bank holiday (last Mon in May), Summer bank holiday (last Mon in Aug), Christmas Day, Boxing Day. |
| US (federal) | `'US'` | New Year's Day, MLK Day (3rd Mon in Jan), Presidents' Day (3rd Mon in Feb), Memorial Day (last Mon in May), Juneteenth, Independence Day, Labor Day (1st Mon in Sep), Columbus Day (2nd Mon in Oct), Veterans Day, Thanksgiving (4th Thu in Nov), Christmas Day. |

## Example

```python
date_features(["2020-01-01", "2020-02-01", "2020-12-01"], calendar=False)
```

| date | month_sin | month_cos |
|------|-----------|-----------|
| 2020-01-01 | 0.000000 | 1.000000 |
| 2020-02-01 | 0.500000 | 0.866025 |
| 2020-12-01 | -0.500000 | 0.866025 |

Feed the sin/cos columns to a regression as predictors, or pass them as the exogenous block alongside an order from [arima_order](arima_order.md).
