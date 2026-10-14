# Name: forecast_metrics
# Description: Accuracy metrics from actual and forecast columns.
# Parameters: data, actual_col, forecast_col, headers=True

def forecast_metrics(data, actual_col, forecast_col, headers=True):
    """Forecast accuracy from a table with actual and forecast columns.

    Error is actual minus forecast. Rows with a blank in either column
    are dropped. MAPE skips zero actuals; sMAPE skips |a|+|f|=0.

    data: table/range, DataFrame, or ref string.
    actual_col: header of the actual values.
    forecast_col: header of the forecast values.
    headers: first row is headers when data is a ref string. Default True.

    Result: metric, value, guidance. Metrics: n, ME, MAE, MSE, RMSE,
    MAPE, sMAPE, MdAPE, MASE, R2.
    """
    def to_frame(value):
        if isinstance(value, str):
            value = xl(value, headers=headers)
        if isinstance(value, pd.DataFrame):
            return value
        if isinstance(value, pd.Series):
            return value.to_frame()
        return pd.DataFrame(value)

    def pick_col(frame, name):
        key = str(pd.Series(name).iloc[0]).strip()
        cols = {str(c).strip().lower(): c for c in frame.columns}
        if key.lower() in cols:
            return frame[cols[key.lower()]]
        if key in frame.columns:
            return frame[key]
        raise ValueError("Column '%s' not found in data." % key)

    frame = to_frame(data)
    a = pd.to_numeric(pick_col(frame, actual_col), errors="coerce")
    f = pd.to_numeric(pick_col(frame, forecast_col), errors="coerce")
    keep = a.notna() & f.notna()
    a = a[keep].to_numpy(dtype=float)
    f = f[keep].to_numpy(dtype=float)
    n = int(a.size)
    if n < 1:
        raise ValueError("Need at least 1 row with both actual and forecast.")

    err = a - f
    abs_e = np.abs(err)
    me = float(err.mean())
    mae = float(abs_e.mean())
    mse = float((err ** 2).mean())
    rmse = float(np.sqrt(mse))

    nz = a != 0
    mape = float(np.mean(np.abs(err[nz] / a[nz])) * 100) if nz.any() else np.nan
    den = np.abs(a) + np.abs(f)
    ok = den > 0
    smape = float(np.mean(2.0 * abs_e[ok] / den[ok]) * 100) if ok.any() else np.nan
    mdape = float(np.median(np.abs(err[nz] / a[nz])) * 100) if nz.any() else np.nan

    if n >= 2:
        naive_mae = float(np.mean(np.abs(np.diff(a))))
        mase = mae / naive_mae if naive_mae > 0 else np.nan
    else:
        mase = np.nan

    ss_tot = float(np.sum((a - a.mean()) ** 2))
    rsq = np.nan if ss_tot == 0 else 1.0 - float(np.sum(err ** 2)) / ss_tot

    return pd.DataFrame(
        [
            ("n", n, "Pairs with both actual and forecast after dropping blanks."),
            ("ME", me, "Mean error (actual - forecast). Positive: under-forecast."),
            ("MAE", mae, "Mean absolute error. Same units as the series."),
            ("MSE", mse, "Mean squared error. Penalises large misses."),
            ("RMSE", rmse, "Root mean squared error. Same units as the series."),
            ("MAPE", mape, "Mean |error|/|actual| as %. Skips zero actuals. Blank if none."),
            ("sMAPE", smape, "Symmetric MAPE %. Uses |a|+|f| in the denominator."),
            ("MdAPE", mdape, "Median |error|/|actual| as %. Less sensitive than MAPE."),
            ("MASE", mase, "MAE / mean |actual change|. <1 beats a naive walk. Need n>=2."),
            ("R2", rsq, "1 - SS_error/SS_actual. 1 is a perfect fit; near 0 is weak."),
        ],
        columns=["metric", "value", "guidance"],
    )

"forecast_metrics(data, actual_col, forecast_col, headers=True)"
