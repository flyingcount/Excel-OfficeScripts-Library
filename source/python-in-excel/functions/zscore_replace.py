# Name: zscore_replace
# Description: Replace time-series points outside a z-score threshold using interpolation.
# Parameters: data, z=3, dates=None, headers=False

def zscore_replace(data, z=3, dates=None, headers=False):
    """Replace points with |z-score| > z by interpolating neighboring values.

    z-scores use the series mean and population standard deviation (ddof=0).
    Interior outliers are filled with linear interpolation (time-based when
    dates are available). Leading or trailing outliers use the nearest
    remaining value. Original blanks stay blank.

    data: value column, date+value range/table, Series, or list.
    z: absolute z-score cutoff (default 3).
    dates: optional date column when it is not in data.
    headers: first row is headers when data or dates is a ref string.

    Result is a Series named value, same length as the input values.
    """

    def to_frame(value):
        if isinstance(value, str):
            value = xl(value, headers=headers)
        if isinstance(value, pd.DataFrame):
            return value
        if isinstance(value, pd.Series):
            return value.to_frame()
        return pd.DataFrame(value)

    def first_numeric(frame):
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
            return None
        parsed = pd.to_datetime(series, errors="coerce")
        if parsed.notna().mean() > 0.8:
            return parsed
        return None

    df = to_frame(data)
    date_out = None
    if dates is not None:
        date_out = to_frame(dates).iloc[:, 0]
        y = first_numeric(df)
        parsed = as_datetime(date_out)
        if parsed is not None:
            date_out = parsed
    else:
        date_col = None
        for col in df.columns:
            parsed = as_datetime(df[col])
            if parsed is not None and (
                pd.api.types.is_datetime64_any_dtype(df[col])
                or not pd.api.types.is_numeric_dtype(df[col])
                or df.select_dtypes(include="number").shape[1] > 1
            ):
                date_col = col
                date_out = parsed
                break
        y = first_numeric(df.drop(columns=[date_col])) if date_col is not None else first_numeric(df)

    y = pd.to_numeric(pd.Series(y).reset_index(drop=True), errors="coerce").astype("float64")
    z = abs(float(pd.Series(z).iloc[0]))
    if date_out is not None:
        date_out = pd.Series(date_out).reset_index(drop=True)
        n = min(len(y), len(date_out))
        y = y.iloc[:n].reset_index(drop=True)
        date_out = date_out.iloc[:n]
        date_idx = pd.Index(date_out)
        use_time = (
            isinstance(date_idx, pd.DatetimeIndex)
            and date_idx.notna().all()
            and date_idx.is_monotonic_increasing
            and date_idx.is_unique
        )
    else:
        use_time = False

    sigma = float(y.std(ddof=0, skipna=True))
    if not np.isfinite(sigma) or sigma == 0:
        outliers = pd.Series(False, index=y.index)
    else:
        outliers = ((y - y.mean(skipna=True)) / sigma).abs() > z
        outliers = outliers.fillna(False)

    masked = y.where(~outliers)
    if use_time:
        filled = pd.Series(masked.to_numpy(), index=date_idx)
        filled = filled.interpolate(method="time", limit_direction="both")
        filled = pd.Series(filled.bfill().ffill().to_numpy(), index=y.index)
    else:
        filled = masked.interpolate(method="linear", limit_direction="both")
        filled = filled.bfill().ffill()

    cleaned = y.where(~outliers, filled)
    return pd.Series(cleaned.to_numpy(), name="value")

"zscore_replace(data, z=3, dates=None, headers=False)"
