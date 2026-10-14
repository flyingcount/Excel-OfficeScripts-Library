# Name: adf
# Description: Augmented Dickey-Fuller stationarity test. Small p-value suggests mean-reversion.
# Parameters: data, regression="c", alpha=0.05, headers=False

def adf(data, regression="c", alpha=0.05, headers=False):
    """Augmented Dickey-Fuller test for a unit root.

    H0: the series has a unit root (non-stationary). Reject H0 when
    pvalue < alpha: the series looks stationary, which is consistent
    with mean-reversion before you build a trading rule.

    data: value column, ref string, Series, or DataFrame (first numeric column).
    regression: "c" constant (default), "ct" constant+trend, "ctt" both trends, "n" none.
    alpha: p-value cutoff for the stationary flag (default 0.05).
    headers: first row is headers when data is a ref string.

    Result spills as metric / value. Need at least 8 numeric values.
    """
    import warnings
    from statsmodels.tsa.stattools import adfuller

    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        numeric = data.select_dtypes(include="number")
        values = numeric.iloc[:, 0] if numeric.shape[1] else data.iloc[:, 0]
    else:
        values = data
    y = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce").dropna()
    n = int(y.size)
    if n < 8:
        raise ValueError("Need at least 8 numeric values for the ADF test.")

    regression = str(pd.Series(regression).iloc[0])
    alpha = float(pd.Series(alpha).iloc[0])
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        stat, pvalue, usedlag, nobs, crit, icbest = adfuller(
            y, regression=regression, autolag="AIC"
        )
    return pd.DataFrame(
        {
            "metric": [
                "n",
                "adf_stat",
                "pvalue",
                "lags",
                "nobs",
                "crit_1pct",
                "crit_5pct",
                "crit_10pct",
                "icbest",
                "alpha",
                "stationary",
            ],
            "value": [
                n,
                float(stat),
                float(pvalue),
                int(usedlag),
                int(nobs),
                float(crit["1%"]),
                float(crit["5%"]),
                float(crit["10%"]),
                float(icbest),
                alpha,
                bool(pvalue < alpha),
            ],
        }
    )

"adf(data, regression='c', alpha=0.05, headers=False)"
