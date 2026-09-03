# Name: outlier_flag
# Description: Flag outliers using IQR, MAD, z-score, STL residuals, or Isolation Forest.
# Parameters: data, method='iqr', threshold=1.5, headers=False, period=12

def outlier_flag(data, method="iqr", threshold=1.5, headers=False, period=12):
    """Flag outlier rows. Spills value, is_outlier, score, lower_bound, upper_bound.

    data: value column, ref string, DataFrame, Series, or list.
    method: iqr (default), mad, zscore, stl, or iforest.
    threshold: IQR/MAD fence (default 1.5); |z| cutoff for zscore/stl (use 3);
        iforest contamination in (0, 0.5), else 'auto'.
    period: STL seasonal length. Default 12. Need 2 full seasons.
    headers: first row is headers when data is a ref string.

    stl: |residual z| after robust STL; bounds are trend+seasonal +/- t*sd.
    iforest: sklearn IsolationForest; score is -score_samples (higher = more
        anomalous); bounds are blank. random_state=42.
    Constant spread flags nothing. Blanks stay blank.
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
    m = str(pd.Series(method).iloc[0]).strip().lower().replace("_", "-")
    period = int(pd.Series(period).iloc[0])
    score = pd.Series(np.nan, index=y.index, dtype="float64")
    lo = pd.Series(np.nan, index=y.index, dtype="float64")
    hi = lo.copy()
    outliers = pd.Series(False, index=y.index)

    if m == "iqr":
        q1, q3 = float(y.quantile(0.25)), float(y.quantile(0.75))
        iqr = q3 - q1
        lo[:], hi[:] = q1 - t * iqr, q3 + t * iqr
        score = y.copy()
        if iqr != 0:
            outliers = ((y < lo) | (y > hi)).fillna(False)
    elif m == "mad":
        med = float(y.median(skipna=True))
        abs_dev = (y - med).abs()
        mad_s = float(abs_dev.median(skipna=True)) * 1.4826
        if mad_s != 0 and np.isfinite(mad_s):
            score = abs_dev / mad_s
            outliers = (score > t).fillna(False)
            lo[:], hi[:] = med - t * mad_s, med + t * mad_s
    elif m == "zscore":
        mu = float(y.mean(skipna=True))
        sigma = float(y.std(ddof=0, skipna=True))
        if sigma != 0 and np.isfinite(sigma):
            score = ((y - mu) / sigma).abs()
            outliers = (score > t).fillna(False)
            lo[:], hi[:] = mu - t * sigma, mu + t * sigma
    elif m in ("stl", "stl-resid"):
        from statsmodels.tsa.seasonal import STL
        if period < 2:
            raise ValueError("period must be at least 2 for STL.")
        ok = y.notna()
        if int(ok.sum()) < period * 2:
            raise ValueError("Need at least 2 full seasons for STL.")
        fit = STL(y[ok].to_numpy(dtype="float64"), period=period, robust=True).fit()
        r = pd.Series(fit.resid, index=y.index[ok])
        mu, sd = float(r.mean()), float(r.std(ddof=0))
        exp = y[ok] - r
        lo.loc[ok], hi.loc[ok] = exp, exp
        if sd != 0 and np.isfinite(sd):
            z = (r - mu) / sd
            score.loc[ok] = z.abs()
            outliers.loc[ok] = z.abs() > t
            lo.loc[ok], hi.loc[ok] = exp - t * sd, exp + t * sd
        else:
            score.loc[ok] = 0.0
    elif m in ("iforest", "isolation-forest", "iso"):
        from sklearn.ensemble import IsolationForest
        ok = y.notna()
        X = y[ok].to_numpy(dtype="float64").reshape(-1, 1)
        if X.shape[0] < 2:
            raise ValueError("Need at least 2 observations for Isolation Forest.")
        contam = t if 0 < t < 0.5 else "auto"
        clf = IsolationForest(contamination=contam, random_state=42)
        clf.fit(X)
        score.loc[ok] = -clf.score_samples(X)
        outliers.loc[ok] = clf.predict(X) == -1
    else:
        raise ValueError(
            "method '%s' not supported. Use 'iqr', 'mad', 'zscore', 'stl', or 'iforest'." % m)

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

"outlier_flag(data, method='iqr', threshold=1.5, headers=False, period=12)"
