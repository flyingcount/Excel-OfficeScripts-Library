# Name: ets_forecast
# Description: Holt-Winters ETS forecast with prediction interval. plot=True for a chart.
# Parameters: data, h=12, trend='add', seasonal='add', period=12, level=0.95, plot=False, headers=False

def ets_forecast(data, h=12, trend="add", seasonal="add", period=12,
                 level=0.95, plot=False, headers=False):
    """Holt-Winters ETS forecast with a prediction interval.

    Point forecast from statsmodels ExponentialSmoothing. Interval is
    z * sigma * sqrt(v_h) with Hyndman additive-error weights
    c_j = alpha + j*beta + gamma * 1_{j mod m = 0}. plot=True returns
    a chart; keep that PY cell as a Python object.

    Multiplicative trend/seasonal need values > 0. Zeros, negatives, and
    blanks are linearly interpolated for the fit (Excel blanks often arrive
    as 0). If the series still is not strictly positive, use add or impute.

    data: value column, ref string, Series, or DataFrame (first numeric col).
    Result columns: t, value, lower, upper, label (Actual / Forecast ETS).
    """
    import warnings
    from scipy.stats import norm
    from statsmodels.tsa.holtwinters import ExponentialSmoothing

    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        numeric = data.select_dtypes(include="number")
        values = numeric.iloc[:, 0] if numeric.shape[1] else data.iloc[:, 0]
    else:
        values = data
    raw = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce").reset_index(drop=True)
    h = int(pd.Series(h).iloc[0])
    period = int(pd.Series(period).iloc[0])
    level = float(pd.Series(level).iloc[0])
    alias = {"additive": "add", "multiplicative": "mul", "mult": "mul"}
    tr = str(pd.Series(trend).iloc[0]).strip().lower() if not isinstance(
        trend, str) else trend.strip().lower()
    se = str(pd.Series(seasonal).iloc[0]).strip().lower() if not isinstance(
        seasonal, str) else seasonal.strip().lower()
    if tr in ("none", "null", "false", ""):
        tr = None
    else:
        tr = alias.get(tr, tr)
    if se in ("none", "null", "false", ""):
        se = None
    else:
        se = alias.get(se, se)
    if tr not in (None, "add", "mul"):
        raise ValueError("trend must be 'add', 'mul', or 'none'.")
    if se not in (None, "add", "mul"):
        raise ValueError("seasonal must be 'add', 'mul', or 'none'.")
    if h < 1:
        raise ValueError("h must be at least 1.")
    if not 0 < level < 1:
        raise ValueError("level must be between 0 and 1.")
    mul = tr == "mul" or se == "mul"
    if mul:
        y = raw.mask(raw <= 0)
        y = y.interpolate(method="linear", limit_direction="both").bfill().ffill()
        yy = y.to_numpy(dtype="float64")
        if yy.size == 0 or not np.isfinite(yy).all() or bool((yy <= 0).any()):
            raise ValueError(
                "Multiplicative trend/seasonal need all values > 0. "
                "Fill zeros/negatives or use trend='add' and seasonal='add'."
            )
        y_act = raw.to_numpy(dtype="float64")
    else:
        y = raw.dropna().reset_index(drop=True)
        yy = y.to_numpy(dtype="float64")
        y_act = yy
    n = int(yy.size)
    need = 2 * period if se else 3
    if n < need:
        raise ValueError("Need at least %d observations for this ETS spec." % need)
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        kw = {"trend": tr, "seasonal": se}
        if se is not None:
            kw["seasonal_periods"] = period
        fit = ExponentialSmoothing(yy, **kw).fit()
        fc = np.asarray(fit.forecast(h), dtype="float64")
        p = fit.params
        if isinstance(p, pd.Series):
            p = p.to_dict()
        a = p.get("smoothing_level", np.nan) if isinstance(p, dict) else np.nan
        b = p.get("smoothing_trend", p.get("smoothing_slope", np.nan)) if isinstance(
            p, dict) else np.nan
        g = p.get("smoothing_seasonal", np.nan) if isinstance(p, dict) else np.nan
        a, b, g = [0.0 if not np.isfinite(float(x)) else float(x) for x in (a, b, g)]
        if not tr:
            b = 0.0
        if not se:
            g = 0.0
        m = period if se else 0
        v = np.empty(h, dtype="float64")
        for k in range(1, h + 1):
            s = 0.0
            for j in range(1, k):
                d = 1.0 if (g and m and j % m == 0) else 0.0
                s += (a + j * b + g * d) ** 2
            v[k - 1] = 1.0 + s
        resid = np.asarray(fit.resid, dtype="float64")
        resid = resid[np.isfinite(resid)]
        sigma = float(np.sqrt(np.mean(resid ** 2))) if resid.size else np.nan
    z = float(norm.ppf(0.5 + level / 2.0))
    se_h = sigma * np.sqrt(v)
    lo = fc - z * se_h
    hi = fc + z * se_h
    t_a = np.arange(1, n + 1, dtype="float64")
    t_f = np.arange(n + 1, n + h + 1, dtype="float64")
    if plot:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(t_a, y_act, label="Actual", color="C0")
        ax.plot(t_f, fc, label="Forecast", color="C1")
        if np.isfinite(lo).all() and np.isfinite(hi).all():
            ax.fill_between(t_f, lo, hi, color="C1", alpha=0.25, label="Interval")
        last = float(y_act[-1]) if np.isfinite(y_act[-1]) else np.nan
        if np.isfinite(last) and np.isfinite(fc[0]):
            ax.plot([n, n + 1], [last, fc[0]], color="C1", linestyle="--", linewidth=1)
        ax.axvline(n + 0.5, color="0.6", linestyle=":", linewidth=1)
        ax.set_xlabel("t")
        ax.set_ylabel("value")
        ax.set_title("ETS forecast")
        ax.legend(loc="best")
        fig.tight_layout()
        return fig
    nan = np.full(n, np.nan)
    actual = pd.DataFrame({
        "t": t_a, "value": y_act, "lower": nan, "upper": nan, "label": "Actual",
    })
    future = pd.DataFrame({
        "t": t_f, "value": fc, "lower": lo, "upper": hi, "label": "Forecast ETS",
    })
    return pd.concat([actual, future], ignore_index=True)

"ets_forecast(data, h=12, trend='add', seasonal='add', period=12, level=0.95, plot=False, headers=False)"
