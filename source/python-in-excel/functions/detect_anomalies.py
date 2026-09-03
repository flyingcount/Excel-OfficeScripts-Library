# Name: detect_anomalies
# Description: Flag time-series anomalies via STL residuals, IQR, or z-score.
# Parameters: data, method='stl', period=12, z=3, headers=False

def detect_anomalies(data, method="stl", period=12, z=3, headers=False):
    """Flag unusual points in an ordered series.

    stl: |STL residual z-score| > z (season-aware). iqr / zscore: same
    fences as outlier_flag on the raw values.

    data: value column, ref string, Series, or DataFrame (first numeric col).
    method: 'stl' (default), 'iqr', or 'zscore'.
    period: STL seasonal length. Default 12.
    z: cutoff. STL/zscore: |z| > z (default 3). IQR: fence multiplier
        (default 3 here; pass 1.5 for Tukey).
    headers: first row is headers when data is a ref string.

    Result: t, value, residual, score, is_anomaly (1/0).
    """
    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        numeric = data.select_dtypes(include="number")
        values = numeric.iloc[:, 0] if numeric.shape[1] else data.iloc[:, 0]
    else:
        values = data
    y = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce").reset_index(drop=True)
    n = int(y.size)
    if n < 4:
        raise ValueError("Need at least 4 observations.")
    m = str(pd.Series(method).iloc[0]).strip().lower() if not isinstance(
        method, str) else method.strip().lower()
    tcut = abs(float(pd.Series(z).iloc[0]))
    period = int(pd.Series(period).iloc[0])
    resid = pd.Series(np.nan, index=y.index, dtype="float64")
    score = pd.Series(np.nan, index=y.index, dtype="float64")
    flag = pd.Series(False, index=y.index)

    if m == "stl":
        from statsmodels.tsa.seasonal import STL
        if period < 2:
            raise ValueError("period must be at least 2 for STL.")
        ok = y.notna()
        if int(ok.sum()) < period * 2:
            raise ValueError("Need at least 2 full seasons for STL.")
        fit = STL(y[ok].to_numpy(dtype="float64"), period=period, robust=True).fit()
        r = pd.Series(fit.resid, index=y.index[ok])
        resid.loc[ok] = r
        mu = float(r.mean())
        sd = float(r.std(ddof=0))
        if sd == 0 or not np.isfinite(sd):
            sc = pd.Series(0.0, index=r.index)
        else:
            sc = (r - mu) / sd
        score.loc[ok] = sc
        flag.loc[ok] = sc.abs() > tcut
    elif m == "iqr":
        q1 = float(y.quantile(0.25))
        q3 = float(y.quantile(0.75))
        iqr = q3 - q1
        lo, hi = q1 - tcut * iqr, q3 + tcut * iqr
        resid = y - float(y.median(skipna=True))
        score = y.copy()
        if iqr != 0:
            flag = (y < lo) | (y > hi)
        flag = flag.fillna(False)
    elif m == "zscore":
        mu = float(y.mean(skipna=True))
        sd = float(y.std(ddof=0, skipna=True))
        resid = y - mu
        if sd == 0 or not np.isfinite(sd):
            score = pd.Series(0.0, index=y.index)
        else:
            score = (y - mu) / sd
            flag = score.abs() > tcut
        flag = flag.fillna(False)
    else:
        raise ValueError("method must be 'stl', 'iqr', or 'zscore'.")

    out = pd.DataFrame({
        "t": np.arange(1, n + 1, dtype="float64"),
        "value": y,
        "residual": resid,
        "score": score,
        "is_anomaly": flag.astype("float64"),
    })
    blank = y.isna().to_numpy()
    if blank.any():
        out.loc[blank, ["residual", "score", "is_anomaly"]] = np.nan
    return out

"detect_anomalies(data, method='stl', period=12, z=3, headers=False)"
