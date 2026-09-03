# Name: arima_estimate
# Description: Estimate ARIMA(p,d,q) using ADF-based differencing and AIC/BIC grid search.
# Parameters: data, p_max=3, q_max=3, d_max=2, criterion='aic', alpha=0.05, full=False, headers=False

def arima_estimate(data, p_max=3, q_max=3, d_max=2, criterion="aic",
                   alpha=0.05, full=False, headers=False):
    """Estimate ARIMA order: ADF test sets d, then grid search minimises AIC or BIC.

    1. Differencing order d is chosen by repeated ADF tests: difference the
       series until the ADF p-value < alpha or d reaches d_max.
    2. For the chosen d, fit ARIMA(p, d, q) for every p in 0..p_max and
       q in 0..q_max. The model with the lowest criterion wins.

    data: value column, ref string, Series, or DataFrame (first numeric col).
    p_max: maximum AR order to search. Default 3.
    q_max: maximum MA order to search. Default 3.
    d_max: maximum differencing order for ADF. Default 2.
    criterion: 'aic' (default) or 'bic'.
    alpha: ADF significance level for stationarity. Default 0.05.
    full: False (default) returns one best-order row. True returns the full
        grid sorted by the chosen criterion.
    headers: first row is headers when data is a ref string.

    Result columns: p, d, q, aic, bic.  full=True adds all fitted models.
    The adf_pvalue and adf_d columns show the test result for the chosen d.
    """
    import warnings
    from statsmodels.tsa.arima.model import ARIMA
    from statsmodels.tsa.stattools import adfuller

    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        numeric = data.select_dtypes(include="number")
        values = numeric.iloc[:, 0] if numeric.shape[1] else data.iloc[:, 0]
    else:
        values = data
    y = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce").dropna()
    if y.shape[0] < 4:
        raise ValueError("Need at least 4 observations.")

    p_max = int(pd.Series(p_max).iloc[0])
    q_max = int(pd.Series(q_max).iloc[0])
    d_max = int(pd.Series(d_max).iloc[0])
    alpha = float(pd.Series(alpha).iloc[0])
    crit = str(pd.Series(criterion).iloc[0]).strip().lower() if not isinstance(
        criterion, str) else criterion.strip().lower()
    if crit not in ("aic", "bic"):
        raise ValueError("criterion must be 'aic' or 'bic', got '%s'." % crit)

    d = 0
    adf_p = np.nan
    series = y.copy()
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        for _ in range(d_max + 1):
            if series.shape[0] < 4:
                break
            try:
                result = adfuller(series, autolag="AIC")
                adf_p = float(result[1])
            except Exception:
                break
            if adf_p < alpha:
                break
            if d < d_max:
                d += 1
                series = series.diff().dropna()
            else:
                break

    rows = []
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        for p in range(p_max + 1):
            for q in range(q_max + 1):
                try:
                    fit = ARIMA(y, order=(p, d, q)).fit()
                    a = float(fit.aic)
                    b = float(fit.bic)
                    if np.isfinite(a) and np.isfinite(b):
                        rows.append((p, d, q, a, b))
                except Exception:
                    pass

    if not rows:
        out = pd.DataFrame(columns=["p", "d", "q", "aic", "bic",
                                     "adf_pvalue", "adf_d"])
        return out

    grid = pd.DataFrame(rows, columns=["p", "d", "q", "aic", "bic"])
    grid = grid.sort_values(crit).reset_index(drop=True)
    grid["adf_pvalue"] = adf_p
    grid["adf_d"] = d

    if full:
        return grid
    return grid.iloc[:1].reset_index(drop=True)

"arima_estimate(data, p_max=3, q_max=3, d_max=2, criterion='aic', alpha=0.05, full=False, headers=False)"
