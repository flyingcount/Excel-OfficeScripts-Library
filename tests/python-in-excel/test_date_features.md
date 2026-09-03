# Test: date_features

## Setup

1. Formulas → **Initialization** → paste `date_features` from `source/python-in-excel/functions/date_features.py` after the default imports → Save. Or paste `init/TimeSeries.py`.
2. Put dates `2020-01-01`, `2020-02-01`, `2020-04-01`, `2020-07-01`, `2020-12-01` in `A1:A5`.
3. Optional: put `2020-01-05` (Sunday) and `2020-01-06` (Monday) in `B1:B2`.

Reference points: `2020-01-01` is a Wednesday (`dayofweek` 2) in the leap year 2020. Cycle position is 0 at January, day 1, and Monday, so those get `sin` 0 and `cos` 1.

## Cases

In a PY cell, set output to **Excel value**.

### Shape and columns

| Python | Expected |
|--------|----------|
| `date_features("A1:A5").shape` | `(5, 21)` |
| `date_features("A1:A5", calendar=False).shape` | `(5, 10)` |
| `date_features("A1:A5", fourier=2).shape` | `(5, 29)` |
| `list(date_features("A1:A5", calendar=False).columns)` | `['date', 'month_sin', 'month_cos', 'day_sin', 'day_cos', 'dayofweek_sin', 'dayofweek_cos', 'dayofyear_sin', 'dayofyear_cos', 'is_holiday']` |
| `date_features("A1:A5", cyclical=False).shape` | `(5, 13)` |
| `date_features("A1:A5", country_holiday=None).shape` | `(5, 20)` |
| `date_features("A1:A5", country_holiday=False).shape` | `(5, 20)` |

### Cyclical encodings

| Python | Expected |
|--------|----------|
| `round(date_features("A1:A5").loc[0, "month_sin"], 6)` | `0.0` |
| `round(date_features("A1:A5").loc[0, "month_cos"], 6)` | `1.0` |
| `round(date_features("A1:A5").loc[1, "month_sin"], 6)` | `0.5` |
| `round(date_features("A1:A5").loc[1, "month_cos"], 6)` | `0.866025` |
| `round(date_features("A1:A5").loc[2, "month_sin"], 6)` | `1.0` |
| `round(date_features("A1:A5").loc[3, "month_cos"], 6)` | `-1.0` |
| `round(date_features("A1:A5").loc[4, "month_sin"], 6)` | `-0.5` |
| `round(date_features("A1:A5").loc[4, "month_cos"], 6)` | `0.866025` |
| `round(date_features(["2020-04-01"], fourier=2).loc[0, "month_cos_2"], 6)` | `-1.0` |
| `round(date_features(["2020-01-01"]).loc[0, "dayofweek_sin"], 6)` | `0.974928` |
| `round(date_features(["2020-01-01"]).loc[0, "dayofweek_cos"], 6)` | `-0.222521` |
| `round(date_features(["2020-01-06"]).loc[0, "dayofweek_sin"], 6)` | `0.0` |
| `round(date_features(["2020-01-06"]).loc[0, "dayofweek_cos"], 6)` | `1.0` |
| `round(date_features(["2020-01-05"]).loc[0, "dayofweek_sin"], 6)` | `-0.781831` |
| `round(date_features(["2020-01-05"]).loc[0, "dayofweek_cos"], 6)` | `0.62349` |
| `round(date_features(["2020-01-01"]).loc[0, "day_cos"], 6)` | `1.0` |
| `round(date_features(["2020-01-01"]).loc[0, "dayofyear_cos"], 6)` | `1.0` |

February and December sit the same distance from January: `month_cos` is `0.866025` for both, `month_sin` is `+0.5` and `-0.5`.

Every pair is on the unit circle. This should be `1.0` for any date and any column prefix:

| Python | Expected |
|--------|----------|
| `round(date_features("A1:A5")["month_sin"] ** 2 + date_features("A1:A5")["month_cos"] ** 2, 6).tolist()` | `[1.0, 1.0, 1.0, 1.0, 1.0]` |

### Calendar parts

| Python | Expected |
|--------|----------|
| `int(date_features(["2020-01-01"]).loc[0, "year"])` | `2020` |
| `int(date_features(["2020-01-01"]).loc[0, "quarter"])` | `1` |
| `int(date_features(["2020-01-01"]).loc[0, "week"])` | `1` |
| `int(date_features(["2020-01-01"]).loc[0, "dayofweek"])` | `2` |
| `int(date_features(["2020-01-01"]).loc[0, "days_in_month"])` | `31` |
| `int(date_features(["2020-02-01"]).loc[0, "days_in_month"])` | `29` |
| `int(date_features(["2020-01-05"]).loc[0, "is_weekend"])` | `1` |
| `int(date_features(["2020-01-06"]).loc[0, "is_weekend"])` | `0` |
| `int(date_features(["2020-06-30"]).loc[0, "is_month_end"])` | `1` |
| `int(date_features(["2020-06-30"]).loc[0, "is_quarter_end"])` | `1` |
| `int(date_features(["2020-12-01"]).loc[0, "is_month_end"])` | `0` |
| `int(date_features(["2020-12-31"]).loc[0, "dayofyear"])` | `366` |

### Holiday flag (UK default)

2020 UK bank holidays: 1 Jan (Wed), 10 Apr (Good Friday), 13 Apr (Easter Monday), 4 May (early May), 25 May (spring), 31 Aug (summer), 25 Dec (Fri), 28 Dec (substitute Boxing Day — 26 Dec is Sat).

| Python | Expected |
|--------|----------|
| `int(date_features(["2020-01-01"]).loc[0, "is_holiday"])` | `1` |
| `int(date_features(["2020-01-02"]).loc[0, "is_holiday"])` | `0` |
| `int(date_features(["2020-04-10"]).loc[0, "is_holiday"])` | `1` |
| `int(date_features(["2020-04-13"]).loc[0, "is_holiday"])` | `1` |
| `int(date_features(["2020-05-04"]).loc[0, "is_holiday"])` | `1` |
| `int(date_features(["2020-05-25"]).loc[0, "is_holiday"])` | `1` |
| `int(date_features(["2020-08-31"]).loc[0, "is_holiday"])` | `1` |
| `int(date_features(["2020-12-25"]).loc[0, "is_holiday"])` | `1` |
| `int(date_features(["2020-12-28"]).loc[0, "is_holiday"])` | `1` |
| `int(date_features(["2020-12-26"]).loc[0, "is_holiday"])` | `0` |

### Holiday flag (US)

2020 US federal holidays: 1 Jan (Wed), 20 Jan (MLK), 17 Feb (Presidents'), 25 May (Memorial), 19 Jun (Fri Juneteenth), 3 Jul (observed Independence Day — 4 Jul is Sat), 7 Sep (Labor), 12 Oct (Columbus), 11 Nov (Veterans), 26 Nov (Thanksgiving), 25 Dec (Fri).

| Python | Expected |
|--------|----------|
| `int(date_features(["2020-01-20"], country_holiday="US").loc[0, "is_holiday"])` | `1` |
| `int(date_features(["2020-07-03"], country_holiday="US").loc[0, "is_holiday"])` | `1` |
| `int(date_features(["2020-07-04"], country_holiday="US").loc[0, "is_holiday"])` | `0` |
| `int(date_features(["2020-11-26"], country_holiday="US").loc[0, "is_holiday"])` | `1` |
| `int(date_features(["2020-12-25"], country_holiday="US").loc[0, "is_holiday"])` | `1` |
| `date_features(["2020-01-01"], country_holiday="FR")` | `#PYTHON!` — `country_holiday 'FR' not supported` |

### Inputs

| Python | Expected |
|--------|----------|
| `str(date_features([43831]).loc[0, "date"].date())` | `2020-01-01` |
| `date_features(pd.Series(pd.to_datetime(["2020-01-01"]))).shape` | `(1, 21)` |
| `date_features(["2020-01-01", None]).loc[1, "month_sin"]` | blank (`NaN`) |
| `str(date_features(["2020-01-01", None]).loc[0, "date"].date())` | `2020-01-01` |
| `date_features(["x", "y"])` | `#PYTHON!` — `No date column found in data.` |

`43831` is the Excel serial for `2020-01-01`, so a column of raw serials gives the same result as a column of real dates.
