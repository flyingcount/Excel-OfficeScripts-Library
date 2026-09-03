# Name: date_features
# Description: Expand a date column into calendar parts, cyclical encodings, and a holiday flag.
# Parameters: data, cyclical=True, calendar=True, fourier=1, country_holiday='UK', headers=False

def date_features(data, cyclical=True, calendar=True, fourier=1, country_holiday="UK", headers=False):
    """Calendar parts, sine/cosine cycle encodings, and a public-holiday flag.

    Cyclical pairs wrap at the end of each cycle, so December sits next to
    January and Sunday next to Monday. Angle is 2 * pi * k * position / period
    with position 0 at the start of the cycle (January, day 1, Monday).

    data: date column, a range/table containing dates, Series, or list.
    cyclical: add sin/cos pairs for month, day, dayofweek, dayofyear.
    calendar: add integer parts (year, quarter, month, week, day, dayofweek,
        dayofyear, days_in_month, is_weekend, is_month_end, is_quarter_end).
    fourier: harmonics per cycle. 1 gives month_sin / month_cos; 2 also gives
        month_sin_2 / month_cos_2 for a second, faster wave.
    country_holiday: two-letter country code for the is_holiday column.
        'UK' (default) or 'US'. None or False disables the column.
    headers: first row is headers when data is a ref string.

    Excel serial numbers are read with the 1899-12-30 origin. Blank or
    unparseable dates keep their row and spill blank features. Result spills
    as a table with a date column plus the requested features.
    """
    from datetime import date, timedelta

    def _easter(year):
        a = year % 19
        b, c = divmod(year, 100)
        d, e = divmod(b, 4)
        f = (b + 8) // 25
        g = (b - f + 1) // 3
        h = (19 * a + b - d - g + 15) % 30
        i, k = divmod(c, 4)
        el = (32 + 2 * e + 2 * i - h - k) % 7
        m = (a + 11 * h + 22 * el) // 451
        month, day = divmod(h + el - 7 * m + 114, 31)
        return date(year, month, day + 1)

    def _sub_uk(d):
        wd = d.weekday()
        return d + timedelta(days=2) if wd == 5 else d + timedelta(days=1) if wd == 6 else d

    def _sub_us(d):
        wd = d.weekday()
        return d - timedelta(days=1) if wd == 5 else d + timedelta(days=1) if wd == 6 else d

    def _nth_weekday(year, month, weekday, n):
        d = date(year, month, 1)
        while d.weekday() != weekday:
            d += timedelta(days=1)
        return d + timedelta(weeks=n - 1)

    def _last_mon(year, month):
        d = date(year, month + 1, 1) - timedelta(days=1) if month < 12 else date(year, 12, 31)
        while d.weekday() != 0:
            d -= timedelta(days=1)
        return d

    def _uk_holidays(year):
        hols = set()
        hols.add(_sub_uk(date(year, 1, 1)))
        es = _easter(year)
        hols.add(es - timedelta(days=2))
        hols.add(es + timedelta(days=1))
        hols.add(_nth_weekday(year, 5, 0, 1))
        hols.add(_last_mon(year, 5))
        hols.add(_last_mon(year, 8))
        xmas = _sub_uk(date(year, 12, 25))
        boxing = _sub_uk(date(year, 12, 26))
        hols.add(xmas)
        hols.add(boxing)
        if xmas == boxing:
            boxing = xmas + timedelta(days=1)
            hols.add(boxing)
        return hols

    def _us_holidays(year):
        hols = set()
        hols.add(_sub_us(date(year, 1, 1)))
        hols.add(_nth_weekday(year, 1, 0, 3))
        hols.add(_nth_weekday(year, 2, 0, 3))
        hols.add(_last_mon(year, 5))
        hols.add(_sub_us(date(year, 6, 19)))
        hols.add(_sub_us(date(year, 7, 4)))
        hols.add(_nth_weekday(year, 9, 0, 1))
        hols.add(_nth_weekday(year, 10, 0, 2))
        hols.add(_sub_us(date(year, 11, 11)))
        hols.add(_nth_weekday(year, 11, 3, 4))
        hols.add(_sub_us(date(year, 12, 25)))
        return hols

    def _holidays_for(country, years):
        fn = {"UK": _uk_holidays, "US": _us_holidays}.get(
            str(country).strip().upper())
        if fn is None:
            raise ValueError(
                "country_holiday '%s' not supported. Use 'UK' or 'US'." % country)
        hols = set()
        for y in years:
            hols |= fn(int(y))
        return hols

    def to_frame(value):
        if isinstance(value, str):
            value = xl(value, headers=headers)
        if isinstance(value, pd.DataFrame):
            return value
        if isinstance(value, pd.Series):
            return value.to_frame()
        return pd.DataFrame(value)

    def as_datetime(series, min_valid=0.8):
        series = pd.Series(series).reset_index(drop=True)
        if pd.api.types.is_datetime64_any_dtype(series):
            return pd.to_datetime(series)
        if pd.api.types.is_numeric_dtype(series):
            num = pd.to_numeric(series, errors="coerce")
            if num.notna().mean() > min_valid and num.dropna().median() > 200:
                return pd.to_datetime(num, unit="D", origin="1899-12-30")
            return None
        parsed = pd.to_datetime(series, errors="coerce")
        if parsed.notna().mean() > min_valid:
            return parsed
        return None

    frame = to_frame(data)
    dates = None
    for col in frame.columns:
        dates = as_datetime(frame[col])
        if dates is not None:
            break
    if dates is None:
        dates = as_datetime(frame.iloc[:, 0], min_valid=0.0)
    if dates is None or not dates.notna().any():
        raise ValueError("No date column found in data.")

    dates = pd.Series(dates).reset_index(drop=True)
    harmonics = max(1, int(pd.Series(fourier).iloc[0]))
    dt = dates.dt
    out = pd.DataFrame({"date": dates})

    if calendar:
        out["year"] = dt.year
        out["quarter"] = dt.quarter
        out["month"] = dt.month
        out["week"] = pd.to_numeric(dt.isocalendar()["week"], errors="coerce").astype("float64")
        out["day"] = dt.day
        out["dayofweek"] = dt.dayofweek
        out["dayofyear"] = dt.dayofyear
        out["days_in_month"] = dt.days_in_month
        out["is_weekend"] = (dt.dayofweek >= 5).astype("float64")
        out["is_month_end"] = dt.is_month_end.astype("float64")
        out["is_quarter_end"] = dt.is_quarter_end.astype("float64")

    if cyclical:
        days_in_year = np.where(dt.is_leap_year.to_numpy(), 366.0, 365.0)
        cycles = (
            ("month", dt.month.to_numpy(dtype="float64") - 1.0, 12.0),
            ("day", dt.day.to_numpy(dtype="float64") - 1.0, dt.days_in_month.to_numpy(dtype="float64")),
            ("dayofweek", dt.dayofweek.to_numpy(dtype="float64"), 7.0),
            ("dayofyear", dt.dayofyear.to_numpy(dtype="float64") - 1.0, days_in_year),
        )
        for name, position, period in cycles:
            fraction = position / period
            for k in range(1, harmonics + 1):
                angle = 2.0 * np.pi * k * fraction
                suffix = "" if k == 1 else "_%d" % k
                out[name + "_sin" + suffix] = np.sin(angle)
                out[name + "_cos" + suffix] = np.cos(angle)

    if country_holiday and country_holiday is not True:
        ch = str(pd.Series(country_holiday).iloc[0]).strip().upper() if not isinstance(
            country_holiday, str) else country_holiday.strip().upper()
        valid = dates.dropna()
        if not valid.empty:
            yrs = valid.dt.year.unique()
            hset = _holidays_for(ch, yrs)
            out["is_holiday"] = dates.apply(
                lambda x: 1.0 if pd.notna(x) and x.date() in hset else 0.0)
        else:
            out["is_holiday"] = np.nan

    blank = dates.isna().to_numpy()
    if blank.any():
        for col in out.columns:
            if col != "date":
                out.loc[blank, col] = np.nan
    return out

"date_features(data, cyclical=True, calendar=True, fourier=1, country_holiday='UK', headers=False)"
