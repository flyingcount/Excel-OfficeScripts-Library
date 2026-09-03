# Name: acf_ljungbox
# Description: ACF and Ljung-Box statistic at each lag (default 20).
# Parameters: data, lags=20, alpha=0.05, headers=False

def acf_ljungbox(data, lags=20, alpha=0.05, headers=False):
    """Autocorrelation (ACF) and Ljung-Box test at lags 1..lags.

    data: value column, residual column, stl() result (uses resid), Series,
        DataFrame, or ref string.
    lags: maximum lag. Default 20, capped at n-2. Need at least 3 values.
    alpha: significance level for acf_sig and lb_sig. Default 0.05.
    headers: first row is headers when data is a ref string.

    Columns: lag, acf, acf_se, acf_sig, lb_stat, lb_pvalue, lb_sig.
    acf_se is 1/sqrt(n) (white-noise Bartlett band). acf_sig is 1 when
    |acf| > 1.96 * acf_se. lb_sig is 1 when Ljung-Box p < alpha.
    """
    from statsmodels.tsa.stattools import acf
    from statsmodels.stats.diagnostic import acorr_ljungbox

    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        cols = {str(c).strip().lower(): c for c in data.columns}
        resid_col = next((cols[n] for n in ("resid", "residual", "residuals") if n in cols), None)
        if resid_col is not None:
            series = data[resid_col]
        else:
            numeric = data.select_dtypes(include="number")
            series = numeric.iloc[:, 0] if numeric.shape[1] else data.iloc[:, 0]
    elif isinstance(data, pd.Series):
        series = data
    else:
        series = pd.Series(data)

    y = pd.to_numeric(pd.Series(series).squeeze(), errors="coerce").dropna().to_numpy(dtype=float)
    n = int(y.size)
    if n < 3:
        raise ValueError("Need at least 3 numeric values.")

    max_lag = max(1, n - 2)
    lag = min(max_lag, int(pd.Series(lags).iloc[0]))
    lag = max(1, lag)
    alpha = float(pd.Series(alpha).iloc[0])

    acf_vals = acf(y, nlags=lag, fft=False)
    se = 1.0 / np.sqrt(n)
    zcrit = 1.96
    try:
        lb = acorr_ljungbox(y, lags=lag, return_df=True)
        lb_stat = lb["lb_stat"].to_numpy(dtype=float)
        lb_p = lb["lb_pvalue"].to_numpy(dtype=float)
    except (ValueError, np.linalg.LinAlgError):
        lb_stat = np.full(lag, np.nan)
        lb_p = np.full(lag, np.nan)

    rows = []
    for k in range(1, lag + 1):
        a = float(acf_vals[k])
        stat = float(lb_stat[k - 1]) if k - 1 < len(lb_stat) else np.nan
        pval = float(lb_p[k - 1]) if k - 1 < len(lb_p) else np.nan
        rows.append((
            k,
            a,
            se,
            1.0 if abs(a) > zcrit * se else 0.0,
            stat,
            pval,
            1.0 if np.isfinite(pval) and pval < alpha else 0.0,
        ))
    return pd.DataFrame(rows, columns=["lag", "acf", "acf_se", "acf_sig",
                                       "lb_stat", "lb_pvalue", "lb_sig"])

"acf_ljungbox(data, lags=20, alpha=0.05, headers=False)"
