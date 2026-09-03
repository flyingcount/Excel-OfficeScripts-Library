# Name: outlier_flag
# Description: Flag outliers using IQR, MAD, or z-score methods.
# Parameters: data, method='iqr', threshold=1.5, headers=False

def outlier_flag(data, method="iqr", threshold=1.5, headers=False):
    """Flag outlier rows by IQR, MAD, or z-score. Returns the original values
    plus is_outlier (1/0), score, lower_bound, and upper_bound columns.

    data: value column, ref string, DataFrame, Series, or list.
    method: 'iqr' (default), 'mad', or 'zscore'.
    threshold: sensitivity. IQR multiplier (default 1.5; 3 for far outliers),
        MAD multiplier (default 1.5; ~2 is common), or z-score cutoff
        (pass 3 for z-score). Meaning depends on method.
    headers: first row is headers when data is a ref string.

    Methods:
      iqr     — outlier when value < Q1 - t*IQR or > Q3 + t*IQR.
      mad     — outlier when |value - median| / MAD > t  (MAD scaled by
                1.4826 to approximate std for normal data).
      zscore  — outlier when |value - mean| / std > t  (population std,
                ddof=0, same convention as zscore_replace).

    A constant column (spread = 0) flags nothing. Blanks stay blank.
    Result is a DataFrame with columns value, is_outlier, score,
    lower_bound, upper_bound.
    """
    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        numeric = data.select_dtypes(include="number")
        values = numeric.iloc[:, 0] if numeric.shape[1] else data.iloc[:, 0]
    elif isinstance(data, pd.Series):
        values = data
    else:
        values = pd.Series(data)

    y = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce").astype("float64")
    y = y.reset_index(drop=True)
    t = abs(float(pd.Series(threshold).iloc[0]))
    m = str(pd.Series(method).iloc[0]).strip().lower() if not isinstance(
        method, str) else method.strip().lower()

    n = y.dropna().shape[0]
    score = pd.Series(np.nan, index=y.index, dtype="float64")
    lo = np.nan
    hi = np.nan

    if m == "iqr":
        q1 = float(y.quantile(0.25))
        q3 = float(y.quantile(0.75))
        iqr = q3 - q1
        lo = q1 - t * iqr
        hi = q3 + t * iqr
        if iqr == 0:
            outliers = pd.Series(False, index=y.index)
        else:
            outliers = (y < lo) | (y > hi)
            outliers = outliers.fillna(False)
        score = y.copy()
    elif m == "mad":
        med = float(y.median(skipna=True))
        abs_dev = (y - med).abs()
        mad_raw = float(abs_dev.median(skipna=True))
        mad_scaled = mad_raw * 1.4826
        if mad_scaled == 0 or not np.isfinite(mad_scaled):
            outliers = pd.Series(False, index=y.index)
        else:
            score = abs_dev / mad_scaled
            outliers = score > t
            outliers = outliers.fillna(False)
            lo = med - t * mad_scaled
            hi = med + t * mad_scaled
    elif m == "zscore":
        mu = float(y.mean(skipna=True))
        sigma = float(y.std(ddof=0, skipna=True))
        if sigma == 0 or not np.isfinite(sigma):
            outliers = pd.Series(False, index=y.index)
        else:
            score = ((y - mu) / sigma).abs()
            outliers = score > t
            outliers = outliers.fillna(False)
            lo = mu - t * sigma
            hi = mu + t * sigma
    else:
        raise ValueError(
            "method '%s' not supported. Use 'iqr', 'mad', or 'zscore'." % m)

    out = pd.DataFrame({
        "value": y,
        "is_outlier": outliers.astype("float64"),
        "score": score,
        "lower_bound": lo,
        "upper_bound": hi,
    })
    blank = y.isna().to_numpy()
    if blank.any():
        out.loc[blank, ["is_outlier", "score", "lower_bound", "upper_bound"]] = np.nan
    return out

"outlier_flag(data, method='iqr', threshold=1.5, headers=False)"
