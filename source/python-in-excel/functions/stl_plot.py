# Name: stl_plot
# Description: STL decomposition as a four-panel matplotlib chart (DecomposeResult.plot).
# Parameters: data, period, dates=None, robust=False, weights=False, headers=False

def stl_fit(data, period, dates=None, robust=False, headers=False):
    """Fit STL. Used by stl (table) and stl_plot (chart)."""
    from statsmodels.tsa.seasonal import STL

    def to_frame(value):
        if isinstance(value, str):
            value = xl(value, headers=headers)
        if isinstance(value, pd.DataFrame):
            return value.dropna(how="all")
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

    y = pd.to_numeric(pd.Series(y).reset_index(drop=True), errors="coerce")
    period = int(pd.Series(period).iloc[0])
    if date_out is not None:
        date_out = pd.Series(date_out).reset_index(drop=True)
        n = min(len(y), len(date_out))
        y = y.iloc[:n]
        date_out = date_out.iloc[:n]
        keep = y.notna() & date_out.notna()
        y = y[keep]
        date_out = date_out[keep]
        series = pd.Series(y.to_numpy(), index=pd.Index(date_out), name="observed")
    else:
        y = y.dropna()
        series = pd.Series(y.to_numpy(), name="observed")

    return STL(series, period=period, robust=bool(robust)).fit()


def stl_plot(data, period, dates=None, robust=False, weights=False, headers=False):
    """Four-panel STL chart: observed, trend, seasonal, resid.

    Same inputs as stl. Returns a matplotlib Figure (DecomposeResult.plot).
    Keep the PY cell as a Python object, not Excel value.

    weights: True adds the robust-LOESS weight panel (use with robust=True).
    """
    fit = stl_fit(data, period, dates=dates, robust=robust, headers=headers)
    return fit.plot(weights=bool(weights))
