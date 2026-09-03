# Name: expsmooth
# Description: SES forecast with prediction interval (default alpha 0.2, h=12). plot=True for a chart.
# Parameters: data, alpha=0.2, h=12, level=0.95, plot=False, headers=False

def expsmooth(data, alpha=0.2, h=12, level=0.95, plot=False, headers=False):
    """SES forecast with a prediction interval. Seed is the first observation.

    St = alpha * xt + (1 - alpha) * S(t-1), with S0 = first value.
    Point forecast is the last St (flat). Interval width is
    z * sigma * sqrt(1 + alpha^2 * (h-1)), with sigma from one-step errors.
    Default h=12, alpha=0.2, level=0.95. plot=True returns a chart; keep
    that PY cell as a Python object.

    data: column range, ref string, Series, or DataFrame (first numeric col).
    Result columns: t, value, lower, upper, label (Actual / Forecast SES).
    """
    from scipy.stats import norm

    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        numeric = data.select_dtypes(include="number")
        values = numeric.iloc[:, 0] if numeric.shape[1] else data.iloc[:, 0]
    else:
        values = data
    series = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce").dropna()
    if series.empty:
        raise ValueError("Need at least 1 observation.")
    alpha = float(pd.Series(alpha).iloc[0])
    h = int(pd.Series(h).iloc[0])
    level = float(pd.Series(level).iloc[0])
    if h < 1:
        raise ValueError("h must be at least 1.")
    if not 0 < level < 1:
        raise ValueError("level must be between 0 and 1.")
    y = series.to_numpy(dtype="float64")
    n = int(y.size)
    smooth = float(y[0])
    err = []
    for x in y[1:]:
        err.append(float(x) - smooth)
        smooth = alpha * float(x) + (1 - alpha) * smooth
    fc = np.full(h, smooth, dtype="float64")
    z = float(norm.ppf(0.5 + level / 2.0))
    if err:
        sigma = float(np.sqrt(np.mean(np.square(err))))
        se = sigma * np.sqrt(1.0 + (alpha ** 2) * np.arange(h, dtype="float64"))
    else:
        se = np.full(h, np.nan)
    lo = fc - z * se
    hi = fc + z * se
    t_a = np.arange(1, n + 1, dtype="float64")
    t_f = np.arange(n + 1, n + h + 1, dtype="float64")
    if plot:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(t_a, y, label="Actual", color="C0")
        ax.plot(t_f, fc, label="Forecast", color="C1")
        if np.isfinite(lo).all() and np.isfinite(hi).all():
            ax.fill_between(t_f, lo, hi, color="C1", alpha=0.25, label="Interval")
        last = float(y[-1])
        if np.isfinite(last) and np.isfinite(fc[0]):
            ax.plot([n, n + 1], [last, fc[0]], color="C1", linestyle="--", linewidth=1)
        ax.axvline(n + 0.5, color="0.6", linestyle=":", linewidth=1)
        ax.set_xlabel("t")
        ax.set_ylabel("value")
        ax.set_title("SES forecast")
        ax.legend(loc="best")
        fig.tight_layout()
        return fig
    nan = np.full(n, np.nan)
    actual = pd.DataFrame({
        "t": t_a, "value": y, "lower": nan, "upper": nan, "label": "Actual",
    })
    future = pd.DataFrame({
        "t": t_f, "value": fc, "lower": lo, "upper": hi, "label": "Forecast SES",
    })
    return pd.concat([actual, future], ignore_index=True)

"expsmooth(data, alpha=0.2, h=12, level=0.95, plot=False, headers=False)"
