# Name: baseline_forecast
# Description: Baseline forecast with actuals plus appended forecast rows and labels.
# Parameters: data, date_col=None, value_col=None, h=12, method='naive', period=1, headers=True

def baseline_forecast(data, date_col=None, value_col=None, h=12, method="naive",
                      period=1, headers=True):
    """Baseline forecast: naive, seasonal_naive, or drift.

    Reads a date column and value column from a table, spills actual rows then
    forecast rows appended. Each row has label 'Actual' or 'Forecast Naive',
    'Forecast Seasonal Naive', or 'Forecast Drift'.

    data: table/range with dates and values, DataFrame, or value Series/list.
    date_col: header of the date column when data is a table. Auto-detected if
        omitted.
    value_col: header of the value column. Auto-detected if omitted.
    h: forecast horizon. Default 12.
    method: 'naive' (default), 'seasonal_naive' (or 'snaive'), or 'drift'.
    period: seasonal period for seasonal_naive. Default 1.
    headers: first row is headers when data is a ref string. Default True.

    Result columns: date, value, label.
    """
    def to_frame(value):
        if isinstance(value, str):
            value = xl(value, headers=headers)
        if isinstance(value, pd.DataFrame):
            return value
        if isinstance(value, pd.Series):
            return value.to_frame()
        return pd.DataFrame(value)

    def pick_col(frame, name, kind):
        if name is not None:
            key = str(pd.Series(name).iloc[0]).strip()
            cols = {str(c).strip().lower(): c for c in frame.columns}
            if key.lower() in cols:
                return frame[cols[key.lower()]]
            if key in frame.columns:
                return frame[key]
            raise ValueError("Column '%s' not found in data." % key)
        if kind == "date":
            for col in frame.columns:
                s = frame[col]
                if pd.api.types.is_datetime64_any_dtype(s):
                    return pd.to_datetime(s)
                if pd.api.types.is_numeric_dtype(s):
                    num = pd.to_numeric(s, errors="coerce")
                    if num.notna().mean() > 0.8 and num.dropna().median() > 200:
                        return pd.to_datetime(num, unit="D", origin="1899-12-30")
                parsed = pd.to_datetime(s, errors="coerce")
                if parsed.notna().mean() > 0.8:
                    return parsed
            return None
        numeric = frame.select_dtypes(include="number")
        if numeric.shape[1]:
            return numeric.iloc[:, 0]
        return pd.to_numeric(frame.iloc[:, 0], errors="coerce")

    def as_datetime(series):
        series = pd.Series(series).reset_index(drop=True)
        if pd.api.types.is_datetime64_any_dtype(series):
            return pd.to_datetime(series)
        if pd.api.types.is_numeric_dtype(series):
            num = pd.to_numeric(series, errors="coerce")
            if num.notna().mean() > 0.8 and num.dropna().median() > 200:
                return pd.to_datetime(num, unit="D", origin="1899-12-30")
        parsed = pd.to_datetime(series, errors="coerce")
        if parsed.notna().mean() > 0.8:
            return parsed
        return None

    def forecast_dates(last_dt, prev, h):
        prev = pd.Series(prev).dropna()
        if last_dt is None or (not isinstance(last_dt, (int, float)) and not pd.notna(last_dt)):
            start = float(prev.shape[0]) if prev.shape[0] else 0.0
            return pd.Series(np.arange(start + 1, start + h + 1), dtype="float64")
        if prev.shape[0] >= 2 and pd.api.types.is_datetime64_any_dtype(prev):
            step = prev.diff().dropna().median()
            if pd.isna(step) or step <= pd.Timedelta(0):
                step = pd.Timedelta(days=1)
            return pd.Series([last_dt + step * (i + 1) for i in range(h)])
        step = float(prev.diff().dropna().median()) if prev.shape[0] >= 2 else 1.0
        if not np.isfinite(step) or step <= 0:
            step = 1.0
        base = float(last_dt)
        return pd.Series([base + step * (i + 1) for i in range(h)], dtype="float64")

    frame = to_frame(data)
    dates_raw = pick_col(frame, date_col, "date")
    values = pick_col(frame, value_col, "value")
    values = pd.to_numeric(pd.Series(values).reset_index(drop=True), errors="coerce")
    dates = None
    if dates_raw is not None:
        dates = pd.Series(dates_raw).reset_index(drop=True)
        parsed = as_datetime(dates)
        if parsed is not None:
            dates = parsed
    keep = values.notna()
    if dates is not None:
        dates = dates[keep].reset_index(drop=True)
    values = values[keep].reset_index(drop=True)
    y = values.to_numpy(dtype="float64")
    n = int(y.size)
    if n < 1:
        raise ValueError("Need at least 1 observation.")

    h = max(1, int(pd.Series(h).iloc[0]))
    m = str(pd.Series(method).iloc[0]).strip().lower() if not isinstance(
        method, str) else method.strip().lower()
    period = max(1, int(pd.Series(period).iloc[0]))
    labels = {
        "naive": "Forecast Naive",
        "seasonal_naive": "Forecast Seasonal Naive",
        "snaive": "Forecast Seasonal Naive",
        "drift": "Forecast Drift",
    }
    if m not in labels:
        raise ValueError(
            "method '%s' not supported. Use 'naive', 'seasonal_naive', or 'drift'." % m)
    fc_label = labels[m]

    fc = np.empty(h, dtype="float64")
    if m == "naive":
        fc[:] = y[-1]
    elif m in ("seasonal_naive", "snaive"):
        if n < period:
            raise ValueError(
                "Need at least %d observations for seasonal_naive with period=%d."
                % (period, period))
        tail = y[-period:]
        for i in range(h):
            fc[i] = tail[i % period]
    else:
        if n < 2:
            raise ValueError("Need at least 2 observations for drift.")
        slope = (y[-1] - y[0]) / (n - 1)
        for i in range(h):
            fc[i] = y[-1] + (i + 1) * slope

    if dates is None:
        act_dates = pd.Series(np.arange(1, n + 1), dtype="float64")
        last_dt = float(n)
        prev_dates = act_dates
    else:
        act_dates = dates
        last_dt = dates.iloc[-1]
        prev_dates = dates

    fc_dates = forecast_dates(last_dt, prev_dates, h)
    actual = pd.DataFrame({
        "date": act_dates,
        "value": y,
        "label": "Actual",
    })
    forecast = pd.DataFrame({
        "date": fc_dates.reset_index(drop=True),
        "value": fc,
        "label": fc_label,
    })
    return pd.concat([actual, forecast], ignore_index=True)

"baseline_forecast(data, date_col=None, value_col=None, h=12, method='naive', period=1, headers=True)"
