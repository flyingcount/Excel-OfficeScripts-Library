# Name: impute
# Description: Fill blanks in a series (linear, ffill, mean, median, seasonal).
# Parameters: data, method='linear', period=12, headers=False

def impute(data, method="linear", period=12, headers=False):
    """Fill missing values in a series. Spills value, imputed, was_missing.

    data: value column, ref string, Series, or DataFrame (first numeric col).
    method: 'linear' (default), 'ffill', 'bfill', 'mean', 'median', or
        'seasonal' (season means; needs period).
    period: season length for method='seasonal'. Default 12.
    headers: first row is headers when data is a ref string.
    """
    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        numeric = data.select_dtypes(include="number")
        values = numeric.iloc[:, 0] if numeric.shape[1] else data.iloc[:, 0]
    else:
        values = data
    y = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce").reset_index(drop=True)
    m = str(pd.Series(method).iloc[0]).strip().lower() if not isinstance(
        method, str) else method.strip().lower()
    missing = y.isna()
    filled = y.copy()
    if m == "linear":
        filled = y.interpolate(method="linear", limit_direction="both")
    elif m == "ffill":
        filled = y.ffill().bfill()
    elif m == "bfill":
        filled = y.bfill().ffill()
    elif m == "mean":
        filled = y.fillna(float(y.mean(skipna=True)))
    elif m == "median":
        filled = y.fillna(float(y.median(skipna=True)))
    elif m == "seasonal":
        p = int(pd.Series(period).iloc[0])
        if p < 2:
            raise ValueError("period must be at least 2 for seasonal impute.")
        idx = np.arange(int(y.size)) % p
        means = y.groupby(idx).transform("mean")
        filled = y.fillna(means).fillna(float(y.mean(skipna=True)))
    else:
        raise ValueError("method must be linear, ffill, bfill, mean, median, or seasonal.")
    return pd.DataFrame({
        "value": y,
        "imputed": filled,
        "was_missing": missing.astype("float64"),
    })

"impute(data, method='linear', period=12, headers=False)"
