# Name: resid_analysis
# Description: Residual diagnostics (summary table or four-panel plot). Matches VBA Residuals analysis plus Ljung-Box and Jarque-Bera.
# Parameters: data, lags=None, plot=False, headers=False

def resid_analysis(data, lags=None, plot=False, headers=False):
    """Diagnose a residual series.

    data: residual column, stl() result (uses column resid), DataFrame, Series, or xl() result.
    lags: Ljung-Box / ACF lag count. Default min(10, n-2).
    plot: False spills a metric/value table; True returns a matplotlib Figure.
    headers: first row is headers when data is a ref string.

    Table includes n, mean, std, min, max, sum, slope/intercept/R² vs order
    (same idea as VBA ResidualsAnalysis), Ljung-Box, and Jarque-Bera.
    Chart: residuals vs order, histogram, QQ, ACF.
    Need at least 3 numeric values.
    """
    import matplotlib.pyplot as plt
    from scipy import stats
    from statsmodels.graphics.gofplots import qqplot
    from statsmodels.graphics.tsaplots import plot_acf
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
        raise ValueError("Need at least 3 residual values.")

    order = np.arange(1, n + 1, dtype=float)
    slope, intercept = np.polyfit(order, y, 1)
    fitted = intercept + slope * order
    ss_res = float(np.sum((y - fitted) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    rsq = float("nan") if ss_tot == 0 else 1.0 - ss_res / ss_tot

    max_lag = max(1, n - 2)
    lag = min(max_lag, 10 if lags is None else int(pd.Series(lags).iloc[0]))
    lag = max(1, lag)

    try:
        lb = acorr_ljungbox(y, lags=lag, return_df=True)
        lb_stat = float(lb["lb_stat"].iloc[-1])
        lb_p = float(lb["lb_pvalue"].iloc[-1])
    except (ValueError, np.linalg.LinAlgError):
        lb_stat = float("nan")
        lb_p = float("nan")

    try:
        jb_stat, jb_p = stats.jarque_bera(y)
        jb_stat, jb_p = float(jb_stat), float(jb_p)
    except ValueError:
        jb_stat = float("nan")
        jb_p = float("nan")

    if plot:
        fig, axes = plt.subplots(2, 2, figsize=(8, 8))
        axes[0, 0].scatter(order, y, marker="x", s=16, color="black")
        axes[0, 0].plot(order, fitted, color="C0", lw=1)
        axes[0, 0].axhline(0, color="gray", lw=0.8)
        axes[0, 0].set_title("Residuals vs order")
        axes[0, 0].set_xlabel("Order")
        axes[0, 0].set_ylabel("Residuals")
        axes[0, 1].hist(y, bins="auto", color="C0", edgecolor="white")
        axes[0, 1].set_title("Histogram")
        qqplot(y, line="s", ax=axes[1, 0])
        axes[1, 0].set_title("Normal QQ")
        plot_acf(y, ax=axes[1, 1], lags=lag)
        axes[1, 1].set_title("ACF")
        fig.suptitle("Residual analysis")
        fig.tight_layout()
        return fig

    return pd.DataFrame(
        {
            "metric": [
                "n",
                "mean",
                "std",
                "min",
                "max",
                "sum",
                "slope_vs_order",
                "intercept_vs_order",
                "rsq_vs_order",
                "ljung_box_lags",
                "ljung_box_stat",
                "ljung_box_pvalue",
                "jarque_bera_stat",
                "jarque_bera_pvalue",
            ],
            "value": [
                n,
                float(y.mean()),
                float(np.std(y, ddof=1)),
                float(y.min()),
                float(y.max()),
                float(y.sum()),
                float(slope),
                float(intercept),
                rsq,
                lag,
                lb_stat,
                lb_p,
                jb_stat,
                jb_p,
            ],
        }
    )

"resid_analysis(data, lags=None, plot=False, headers=False)"
