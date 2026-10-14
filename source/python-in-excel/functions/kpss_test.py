# Name: kpss_test
# Description: KPSS stationarity test (complement to ADF).
# Parameters: data, alpha=0.05, regression='c', headers=False

def kpss_test(data, alpha=0.05, regression="c", headers=False):
    """KPSS unit-root / stationarity test. Spills metric, value, guidance.

    H0: the series is stationary (around a level or a trend). Reject H0
    when p-value < alpha (treat as non-stationary). Opposite of ADF.

    data: value column, ref string, Series, or DataFrame (first numeric col).
    alpha: significance level. Default 0.05.
    regression: 'c' level-stationary (default) or 'ct' trend-stationary.
    headers: first row is headers when data is a ref string.
    """
    import warnings
    from statsmodels.tsa.stattools import kpss

    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        numeric = data.select_dtypes(include="number")
        values = numeric.iloc[:, 0] if numeric.shape[1] else data.iloc[:, 0]
    else:
        values = data
    y = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce").dropna()
    n = int(y.shape[0])
    if n < 8:
        raise ValueError("Need at least 8 observations.")
    alpha = float(pd.Series(alpha).iloc[0])
    reg = str(pd.Series(regression).iloc[0]).strip().lower() if not isinstance(
        regression, str) else regression.strip().lower()
    if reg not in ("c", "ct"):
        raise ValueError("regression must be 'c' or 'ct'.")
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        stat, pval, lags, crit = kpss(y, regression=reg, nlags="auto")
    stat, pval = float(stat), float(pval)
    lags = int(lags)
    c1 = float(crit.get("1%", np.nan))
    c5 = float(crit.get("5%", np.nan))
    c10 = float(crit.get("10%", np.nan))
    is_stat = 1.0 if pval >= alpha else 0.0
    if pval < alpha:
        note = "p < alpha: reject stationarity. Treat the series as non-stationary."
    else:
        note = "p >= alpha: fail to reject stationarity. Treat as stationary."
    return pd.DataFrame(
        [
            ("n", n, "Count of numeric values after dropping blanks."),
            ("kpss_stat", stat, "Larger than a critical value supports non-stationarity."),
            ("pvalue", pval, "p < alpha rejects H0 (stationary). Series is then non-stationary."),
            ("lags", lags, "Truncation lag used in the test."),
            ("crit_1", c1, "1% critical value."),
            ("crit_5", c5, "5% critical value. Usual cutoff with alpha=0.05."),
            ("crit_10", c10, "10% critical value."),
            ("alpha", alpha, "Significance level used for the stationary flag."),
            ("regression", reg, "c=level stationary, ct=trend stationary."),
            ("stationary", is_stat, "1 if pvalue >= alpha, else 0."),
            ("interpretation", note, note),
        ],
        columns=["metric", "value", "guidance"],
    )

"kpss_test(data, alpha=0.05, regression='c', headers=False)"
