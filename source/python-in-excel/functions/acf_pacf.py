# Name: acf_pacf
# Description: ACF and PACF as a table or a two-panel chart.
# Parameters: data, lags=20, plot=False, headers=False

def acf_pacf(data, lags=20, plot=False, headers=False):
    """Sample ACF and PACF at lags 1..lags. plot=False spills a table; True is a chart.

    data: value column, residual column, stl() result (uses resid), Series,
        DataFrame, or ref string.
    lags: maximum lag. Default 20, capped at min(n-2, n//2 - 1) for PACF.
    plot: False (default) returns a table. True returns a two-panel matplotlib
        Figure (ACF above, PACF below). Keep that PY cell as a Python object.
    headers: first row is headers when data is a ref string.

    Table columns: lag, acf, pacf, se, acf_sig, pacf_sig.
    se is 1/sqrt(n). acf_sig / pacf_sig are 1 when |value| > 1.96 * se.
    """
    from statsmodels.tsa.stattools import acf, pacf
    from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

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
    if n < 4:
        raise ValueError("Need at least 4 numeric values.")

    max_lag = max(1, min(n - 2, n // 2 - 1))
    lag = min(max_lag, int(pd.Series(lags).iloc[0]))
    lag = max(1, lag)

    if plot:
        fig, axes = plt.subplots(2, 1, figsize=(8, 6))
        plot_acf(y, ax=axes[0], lags=lag)
        plot_pacf(y, ax=axes[1], lags=lag, method="ywm")
        axes[0].set_title("ACF")
        axes[1].set_title("PACF")
        fig.tight_layout()
        return fig

    acf_vals = acf(y, nlags=lag, fft=False)
    pacf_vals = pacf(y, nlags=lag, method="ywm")
    se = 1.0 / np.sqrt(n)
    zcrit = 1.96
    rows = []
    for k in range(1, lag + 1):
        a = float(acf_vals[k])
        p = float(pacf_vals[k])
        rows.append((
            k,
            a,
            p,
            se,
            1.0 if abs(a) > zcrit * se else 0.0,
            1.0 if abs(p) > zcrit * se else 0.0,
        ))
    return pd.DataFrame(rows, columns=["lag", "acf", "pacf", "se", "acf_sig", "pacf_sig"])

"acf_pacf(data, lags=20, plot=False, headers=False)"
