# Name: sarima_forecast
# Description: Seasonal ARIMA forecast with actuals plus appended forecast rows.
# Parameters: data, h=12, p=1, d=1, q=1, P=1, D=1, Q=1, s=12, headers=False

def sarima_forecast(data, h=12, p=1, d=1, q=1, P=1, D=1, Q=1, s=12, headers=False):
    """SARIMA(p,d,q)(P,D,Q)s forecast. Spills actuals then forecast rows.

    data: value column, ref string, Series, or DataFrame (first numeric col).
    h: forecast horizon. Default 12.
    p, d, q: non-seasonal ARIMA orders. Default 1, 1, 1.
    P, D, Q, s: seasonal orders and period. Default 1, 1, 1, 12.
    headers: first row is headers when data is a ref string.

    Result columns: t, value, label ('Actual' or 'Forecast SARIMA').
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
    y = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce").dropna().reset_index(drop=True)
    h = int(pd.Series(h).iloc[0])
    p = int(pd.Series(p).iloc[0])
    d = int(pd.Series(d).iloc[0])
    q = int(pd.Series(q).iloc[0])
    P = int(pd.Series(P).iloc[0])
    D = int(pd.Series(D).iloc[0])
    Q = int(pd.Series(Q).iloc[0])
    s = int(pd.Series(s).iloc[0])
    if h < 1:
        raise ValueError("h must be at least 1.")
    if s < 2:
        raise ValueError("s must be at least 2.")
    n = int(y.size)
    need = s * 2
    if n < need:
        raise ValueError("Need at least %d observations for seasonal period s." % need)
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        fit = ARIMA(y, order=(p, d, q), seasonal_order=(P, D, Q, s)).fit()
        fc = np.asarray(fit.forecast(h), dtype="float64")
    actual = pd.DataFrame({
        "t": np.arange(1, n + 1, dtype="float64"),
        "value": y.to_numpy(dtype="float64"),
        "label": "Actual",
    })
    future = pd.DataFrame({
        "t": np.arange(n + 1, n + h + 1, dtype="float64"),
        "value": fc,
        "label": "Forecast SARIMA",
    })
    return pd.concat([actual, future], ignore_index=True)

"sarima_forecast(data, h=12, p=1, d=1, q=1, P=1, D=1, Q=1, s=12, headers=False)"
