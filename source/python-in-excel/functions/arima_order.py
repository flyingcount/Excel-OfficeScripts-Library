# Name: arima_order
# Description: AIC grid search for ARIMA(p, d, q). Returns one row: p, d, q.
# Parameters: data, p_max=3, d_max=2, q_max=3, headers=False

def arima_order(data, p_max=3, d_max=2, q_max=3, headers=False):
    """Choose ARIMA(p, d, q) by lowest AIC over p=0..p_max, d=0..d_max, q=0..q_max.

    data: value column, ref string, Series, or DataFrame (first numeric column).
    Defaults match a p<4, d<3, q<4 search. Failed fits are skipped.
    Result spills as one row with columns p, d, q.
    """
    import warnings
    from statsmodels.tsa.arima.model import ARIMA

    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        numeric = data.select_dtypes(include="number")
        values = numeric.iloc[:, 0] if numeric.shape[1] else data.iloc[:, 0]
    else:
        values = data
    y = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce").dropna()
    p_max = int(pd.Series(p_max).iloc[0])
    d_max = int(pd.Series(d_max).iloc[0])
    q_max = int(pd.Series(q_max).iloc[0])

    best_aic = np.inf
    best_order = None
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        for d in range(d_max + 1):
            for p in range(p_max + 1):
                for q in range(q_max + 1):
                    try:
                        fit = ARIMA(y, order=(p, d, q)).fit()
                        if np.isfinite(fit.aic) and fit.aic < best_aic:
                            best_aic = fit.aic
                            best_order = (p, d, q)
                    except Exception:
                        pass

    if best_order is None:
        return pd.DataFrame(columns=["p", "d", "q"])
    return pd.DataFrame([best_order], columns=["p", "d", "q"])

"arima_order(data, p_max=3, d_max=2, q_max=3, headers=False)"