# Name: adf_test
# Description: Augmented Dickey-Fuller test for stationarity.
# Parameters: data, alpha=0.05, regression='c', headers=False

def adf_test(data, alpha=0.05, regression="c", headers=False):
    """Augmented Dickey-Fuller unit-root test. Spills metric, value, guidance.

    H0: the series has a unit root (non-stationary). Reject H0 when
    p-value < alpha (or adf_stat is more negative than the 5% critical value).

    data: value column, ref string, Series, or DataFrame (first numeric col).
    alpha: significance level. Default 0.05.
    regression: 'c' constant (default), 'ct' constant+trend, 'n' none,
        'ctt' constant+trend+quadratic.
    headers: first row is headers when data is a ref string.

    Need at least 4 numeric values. Lag length is chosen by AIC (autolag).
    """
    from statsmodels.tsa.stattools import adfuller

    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        numeric = data.select_dtypes(include="number")
        values = numeric.iloc[:, 0] if numeric.shape[1] else data.iloc[:, 0]
    else:
        values = data
    y = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce").dropna()
    n = int(y.shape[0])
    if n < 4:
        raise ValueError("Need at least 4 observations.")

    alpha = float(pd.Series(alpha).iloc[0])
    reg = str(pd.Series(regression).iloc[0]).strip().lower() if not isinstance(
        regression, str) else regression.strip().lower()
    if reg not in ("c", "ct", "n", "ctt"):
        raise ValueError("regression must be 'c', 'ct', 'n', or 'ctt'.")

    stat, pval, usedlag, nobs, crit, _ = adfuller(y, regression=reg, autolag="AIC")
    stat, pval = float(stat), float(pval)
    usedlag, nobs = int(usedlag), int(nobs)
    c1, c5, c10 = float(crit["1%"]), float(crit["5%"]), float(crit["10%"])
    is_stat = 1.0 if pval < alpha else 0.0
    if pval < alpha:
        note = "p < alpha: reject unit root. Treat the series as stationary."
    else:
        note = "p >= alpha: fail to reject unit root. Treat as non-stationary."

    return pd.DataFrame(
        [
            ("n", n, "Count of numeric values after dropping blanks."),
            ("adf_stat", stat, "More negative than a critical value supports stationarity."),
            ("pvalue", pval, "p < alpha rejects H0 (unit root). Series is then stationary."),
            ("usedlag", usedlag, "ADF lag length chosen by AIC."),
            ("nobs", nobs, "Observations used in the regression after lags."),
            ("crit_1", c1, "1% critical value. adf_stat below this is strong evidence."),
            ("crit_5", c5, "5% critical value. Usual cutoff with alpha=0.05."),
            ("crit_10", c10, "10% critical value. Weaker evidence of stationarity."),
            ("alpha", alpha, "Significance level used for the stationary flag."),
            ("regression", reg, "c=constant, ct=constant+trend, n=none, ctt=quadratic."),
            ("stationary", is_stat, "1 if pvalue < alpha, else 0."),
            ("interpretation", note, note),
        ],
        columns=["metric", "value", "guidance"],
    )

"adf_test(data, alpha=0.05, regression='c', headers=False)"
