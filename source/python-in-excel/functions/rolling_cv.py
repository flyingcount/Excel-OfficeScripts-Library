# Name: rolling_cv
# Description: Rolling-origin cross-validation with naive / seasonal naive / drift.
# Parameters: data, h=1, min_train=None, step=1, method='naive', period=12, full=False, headers=False

def rolling_cv(data, h=1, min_train=None, step=1, method="naive", period=12,
               full=False, headers=False):
    """Walk-forward CV. At each origin, forecast h steps from history only.

    method: 'naive', 'seasonal_naive' (or 'snaive'), or 'drift' - same as
    baseline_forecast, so the loop stays fast in Excel.

    data: value column, ref string, Series, or DataFrame (first numeric col).
    h: forecast horizon. Default 1.
    min_train: smallest training length. Default max(h * 2, period + 1).
    step: origin stride. Default 1.
    period: seasonal period for seasonal_naive. Default 12.
    full: False (default) spills MAE/RMSE/MAPE. True spills each origin.
    headers: first row is headers when data is a ref string.
    """
    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        numeric = data.select_dtypes(include="number")
        values = numeric.iloc[:, 0] if numeric.shape[1] else data.iloc[:, 0]
    else:
        values = data
    y = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce").dropna().to_numpy(dtype="float64")
    h = int(pd.Series(h).iloc[0])
    step = int(pd.Series(step).iloc[0])
    period = int(pd.Series(period).iloc[0])
    m = str(pd.Series(method).iloc[0]).strip().lower() if not isinstance(
        method, str) else method.strip().lower()
    if m in ("snaive", "seasonal"):
        m = "seasonal_naive"
    n = int(y.size)
    if min_train is None or min_train is False:
        min_n = max(h * 2, period + 1 if m == "seasonal_naive" else h + 1)
    else:
        min_n = int(pd.Series(min_train).iloc[0])
    if h < 1 or step < 1:
        raise ValueError("h and step must be at least 1.")
    if m not in ("naive", "seasonal_naive", "drift"):
        raise ValueError("method must be naive, seasonal_naive, or drift.")
    if n < min_n + h:
        raise ValueError("Need at least min_train + h observations.")

    def predict(hist):
        last = float(hist[-1])
        if m == "naive":
            return np.repeat(last, h)
        if m == "drift":
            k = hist.size
            slope = (last - float(hist[0])) / (k - 1) if k > 1 else 0.0
            return last + slope * np.arange(1, h + 1)
        seas = np.empty(h, dtype="float64")
        for i in range(h):
            pos = hist.size - period + (i % period)
            seas[i] = float(hist[pos]) if pos >= 0 else last
        return seas

    rows = []
    origin = min_n
    while origin + h <= n:
        hist = y[:origin]
        fc = predict(hist)
        act = y[origin:origin + h]
        err = act - fc
        rows.append(pd.DataFrame({
            "origin": origin,
            "horizon": np.arange(1, h + 1),
            "actual": act,
            "forecast": fc,
            "error": err,
        }))
        origin += step
    if not rows:
        raise ValueError("No CV windows. Increase data or lower min_train / h.")
    folds = pd.concat(rows, ignore_index=True)
    if full:
        return folds
    e = folds["error"].to_numpy(dtype="float64")
    a = folds["actual"].to_numpy(dtype="float64")
    nz = a != 0
    mape = float(np.mean(np.abs(e[nz] / a[nz])) * 100) if nz.any() else np.nan
    return pd.DataFrame(
        [
            ("n_forecasts", int(e.size), "Holdout points across all origins."),
            ("n_origins", int(folds["origin"].nunique()), "Walk-forward origins."),
            ("h", h, "Forecast horizon per origin."),
            ("method", m, "naive, seasonal_naive, or drift."),
            ("MAE", float(np.mean(np.abs(e))), "Mean absolute error."),
            ("RMSE", float(np.sqrt(np.mean(e ** 2))), "Root mean squared error."),
            ("MAPE", mape, "Mean |error|/|actual| as %. Skips zero actuals."),
        ],
        columns=["metric", "value", "guidance"],
    )

"rolling_cv(data, h=1, min_train=None, step=1, method='naive', period=12, full=False, headers=False)"
