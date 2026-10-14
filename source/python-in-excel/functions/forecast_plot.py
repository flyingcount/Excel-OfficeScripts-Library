# Name: forecast_plot
# Description: Plot actuals, forecast, and optional prediction interval.
# Parameters: actual, forecast, lower=None, upper=None, headers=False

def forecast_plot(actual, forecast, lower=None, upper=None, headers=False):
    """Plot history, point forecast, and optional lower/upper band.

    Actual is drawn on t = 1..n. Forecast (and bands) continue on
    t = n+1..n+h. Keep the PY cell as a Python object, not Excel value.

    actual: history column, ref string, Series, list, or DataFrame.
    forecast: future point forecasts (same shapes as actual).
    lower / upper: optional interval bounds; same length as forecast.
        Both required for a shaded band. One alone is drawn as a line.
    headers: first row is headers when any argument is a ref string.
    """
    def to_series(value, name):
        if value is None:
            return None
        if isinstance(value, str):
            value = xl(value, headers=headers)
        if isinstance(value, pd.DataFrame):
            numeric = value.select_dtypes(include="number")
            col = numeric.iloc[:, 0] if numeric.shape[1] else value.iloc[:, 0]
        else:
            col = value
        s = pd.to_numeric(pd.Series(col).squeeze(), errors="coerce").reset_index(drop=True)
        if int(s.notna().sum()) < 1:
            raise ValueError("%s needs at least 1 numeric value." % name)
        return s

    ya = to_series(actual, "actual")
    yf = to_series(forecast, "forecast")
    lo = to_series(lower, "lower") if lower is not None else None
    hi = to_series(upper, "upper") if upper is not None else None
    n = int(ya.size)
    h = int(yf.size)
    t_a = np.arange(1, n + 1, dtype="float64")
    t_f = np.arange(n + 1, n + h + 1, dtype="float64")

    if lo is not None and int(lo.size) != h:
        raise ValueError("lower length must match forecast.")
    if hi is not None and int(hi.size) != h:
        raise ValueError("upper length must match forecast.")

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(t_a, ya.to_numpy(dtype="float64"), label="Actual", color="C0")
    ax.plot(t_f, yf.to_numpy(dtype="float64"), label="Forecast", color="C1")
    last = float(ya.iloc[-1]) if pd.notna(ya.iloc[-1]) else np.nan
    first = float(yf.iloc[0]) if pd.notna(yf.iloc[0]) else np.nan
    if np.isfinite(last) and np.isfinite(first):
        ax.plot([n, n + 1], [last, first], color="C1", linestyle="--", linewidth=1)
    ax.axvline(n + 0.5, color="0.6", linestyle=":", linewidth=1)

    if lo is not None and hi is not None:
        ax.fill_between(
            t_f,
            lo.to_numpy(dtype="float64"),
            hi.to_numpy(dtype="float64"),
            color="C1",
            alpha=0.25,
            label="Interval",
        )
    else:
        if lo is not None:
            ax.plot(t_f, lo.to_numpy(dtype="float64"), color="C1", linestyle=":", label="Lower")
        if hi is not None:
            ax.plot(t_f, hi.to_numpy(dtype="float64"), color="C1", linestyle=":", label="Upper")

    ax.set_xlabel("t")
    ax.set_ylabel("value")
    ax.set_title("Forecast")
    ax.legend(loc="best")
    fig.tight_layout()
    return fig

"forecast_plot(actual, forecast, lower=None, upper=None, headers=False)"
