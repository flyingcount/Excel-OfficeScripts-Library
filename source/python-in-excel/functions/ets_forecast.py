# Name: ets_forecast
# Description: Holt-Winters ETS forecast with actuals plus appended forecast rows.
# Parameters: data, h=12, trend='add', seasonal='add', period=12, headers=False

def ets_forecast(data, h=12, trend="add", seasonal="add", period=12, headers=False):
    """Holt-Winters (ETS) forecast. Spills actuals then forecast rows.

    data: value column, ref string, Series, or DataFrame (first numeric col).
    h: forecast horizon. Default 12.
    trend: 'add', 'mul', or 'none'. Default 'add'.
    seasonal: 'add', 'mul', or 'none'. Default 'add'.
    period: seasonal length when seasonal is not none. Default 12.
    headers: first row is headers when data is a ref string.

    Result columns: t, value, label ('Actual' or 'Forecast ETS').
    """
    import warnings
    from statsmodels.tsa.holtwinters import ExponentialSmoothing

    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        numeric = data.select_dtypes(include="number")
        values = numeric.iloc[:, 0] if numeric.shape[1] else data.iloc[:, 0]
    else:
        values = data
    y = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce").dropna().reset_index(drop=True)
    h = int(pd.Series(h).iloc[0])
    period = int(pd.Series(period).iloc[0])
    tr = str(pd.Series(trend).iloc[0]).strip().lower() if not isinstance(
        trend, str) else trend.strip().lower()
    se = str(pd.Series(seasonal).iloc[0]).strip().lower() if not isinstance(
        seasonal, str) else seasonal.strip().lower()
    if tr in ("none", "null", "false", ""):
        tr = None
    if se in ("none", "null", "false", ""):
        se = None
    if tr not in (None, "add", "mul"):
        raise ValueError("trend must be 'add', 'mul', or 'none'.")
    if se not in (None, "add", "mul"):
        raise ValueError("seasonal must be 'add', 'mul', or 'none'.")
    if h < 1:
        raise ValueError("h must be at least 1.")
    n = int(y.size)
    need = 2 * period if se else 3
    if n < need:
        raise ValueError("Need at least %d observations for this ETS spec." % need)
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        kw = {"trend": tr, "seasonal": se}
        if se is not None:
            kw["seasonal_periods"] = period
        fit = ExponentialSmoothing(y, **kw).fit()
        fc = np.asarray(fit.forecast(h), dtype="float64")
    actual = pd.DataFrame({
        "t": np.arange(1, n + 1, dtype="float64"),
        "value": y.to_numpy(dtype="float64"),
        "label": "Actual",
    })
    future = pd.DataFrame({
        "t": np.arange(n + 1, n + h + 1, dtype="float64"),
        "value": fc,
        "label": "Forecast ETS",
    })
    return pd.concat([actual, future], ignore_index=True)

"ets_forecast(data, h=12, trend='add', seasonal='add', period=12, headers=False)"
