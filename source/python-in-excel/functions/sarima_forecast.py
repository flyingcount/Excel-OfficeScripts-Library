# Name: sarima_forecast
# Description: SARIMA forecast with prediction interval. plot=True for a chart.
# Parameters: data, h=12, p=1, d=1, q=1, P=1, D=1, Q=1, s=12, level=0.95, plot=False, headers=False

def sarima_forecast(data, h=12, p=1, d=1, q=1, P=1, D=1, Q=1, s=12,
                    level=0.95, plot=False, headers=False):
    """SARIMA(p,d,q)(P,D,Q)s forecast with a prediction interval.

    Interval from statsmodels get_forecast at coverage `level` (default 0.95).
    plot=True returns a chart; keep that PY cell as a Python object.

    data: value column, ref string, Series, or DataFrame (first numeric col).
    Result columns: t, value, lower, upper, label (Actual / Forecast SARIMA).
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
    level = float(pd.Series(level).iloc[0])
    if h < 1:
        raise ValueError("h must be at least 1.")
    if s < 2:
        raise ValueError("s must be at least 2.")
    if not 0 < level < 1:
        raise ValueError("level must be between 0 and 1.")
    n = int(y.size)
    need = s * 2
    if n < need:
        raise ValueError("Need at least %d observations for seasonal period s." % need)
    yy = y.to_numpy(dtype="float64")
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        fit = ARIMA(y, order=(p, d, q), seasonal_order=(P, D, Q, s)).fit()
        pred = fit.get_forecast(steps=h)
        fc = np.asarray(pred.predicted_mean, dtype="float64").reshape(-1)
        ci = np.asarray(pred.conf_int(alpha=1.0 - level), dtype="float64")
    lo, hi = ci[:, 0], ci[:, 1]
    t_a = np.arange(1, n + 1, dtype="float64")
    t_f = np.arange(n + 1, n + h + 1, dtype="float64")
    if plot:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(t_a, yy, label="Actual", color="C0")
        ax.plot(t_f, fc, label="Forecast", color="C1")
        if np.isfinite(lo).all() and np.isfinite(hi).all():
            ax.fill_between(t_f, lo, hi, color="C1", alpha=0.25, label="Interval")
        last = float(yy[-1])
        if np.isfinite(last) and np.isfinite(fc[0]):
            ax.plot([n, n + 1], [last, fc[0]], color="C1", linestyle="--", linewidth=1)
        ax.axvline(n + 0.5, color="0.6", linestyle=":", linewidth=1)
        ax.set_xlabel("t")
        ax.set_ylabel("value")
        ax.set_title("SARIMA forecast")
        ax.legend(loc="best")
        fig.tight_layout()
        return fig
    nan = np.full(n, np.nan)
    actual = pd.DataFrame({
        "t": t_a, "value": yy, "lower": nan, "upper": nan, "label": "Actual",
    })
    future = pd.DataFrame({
        "t": t_f, "value": fc, "lower": lo, "upper": hi, "label": "Forecast SARIMA",
    })
    return pd.concat([actual, future], ignore_index=True)

"sarima_forecast(data, h=12, p=1, d=1, q=1, P=1, D=1, Q=1, s=12, level=0.95, plot=False, headers=False)"
