# Paul Python in Excel library
#
# Paste AFTER the default imports in Formulas → Initialization, then Save.
# Do not replace the default pandas / numpy / matplotlib / seaborn imports.
#
# Requires Microsoft 365 Python in Excel. Functions use Excel's xl() helper.

def xl_df(ref, headers=True):
    """Load Excel data with xl() and drop rows that are entirely empty.

    ref: "A1:C10", "Table1[#All]", or a defined name.
    headers: first row is column names (default True).
    """
    data = xl(ref, headers=headers)
    if isinstance(data, pd.DataFrame):
        df = data
    elif isinstance(data, pd.Series):
        df = data.to_frame()
    else:
        df = pd.DataFrame(data)
    return df.dropna(how="all")

"xl_df(ref, headers=True)"


def describe(data, headers=True):
    """Summary statistics that spill back to the grid.

    data: ref string ("Table1[#All]"), DataFrame, Series, or xl() result.
    headers: used only when data is a ref string.
    """
    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        df = data
    elif isinstance(data, pd.Series):
        df = data.to_frame()
    else:
        df = pd.DataFrame(data)
    return df.dropna(how="all").describe()

"describe(data, headers=True)"


def corr(data, method="pearson", headers=True):
    """Pairwise correlation. method is pearson, kendall, or spearman.

    data: ref string, DataFrame, Series, or xl() result.
    headers: used only when data is a ref string.
    """
    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        df = data
    elif isinstance(data, pd.Series):
        df = data.to_frame()
    else:
        df = pd.DataFrame(data)
    return df.dropna(how="all").corr(method=method, numeric_only=True)

"corr(data, method='pearson', headers=True)"


def expsmooth(data, alpha=0.2, headers=False):
    """Last SES value. Seed is the first numeric observation.

    St = alpha * xt + (1 - alpha) * S(t-1), with S0 = first value.
    For 10, 12, 14 and alpha 0.2 the result is 11.12 (same as EXPSMOOTH).

    data: column range, ref string, Series, or single-column DataFrame.
    headers: used only when data is a ref string (default False for a value column).
    """
    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        numeric = data.select_dtypes(include="number")
        values = numeric.iloc[:, 0] if numeric.shape[1] else data.iloc[:, 0]
    else:
        values = data
    series = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce").dropna()
    if series.empty:
        return float("nan")
    smooth = float(series.iloc[0])
    for x in series.iloc[1:]:
        smooth = alpha * float(x) + (1 - alpha) * smooth
    return smooth

"expsmooth(data, alpha=0.2, headers=False)"


def stl_fit(data, period, dates=None, robust=False, headers=False):
    """Fit STL. Used by stl (table) and stl_plot (chart)."""
    from statsmodels.tsa.seasonal import STL

    def to_frame(value):
        if isinstance(value, str):
            value = xl(value, headers=headers)
        if isinstance(value, pd.DataFrame):
            return value.dropna(how="all")
        if isinstance(value, pd.Series):
            return value.to_frame()
        return pd.DataFrame(value)

    def first_numeric(frame):
        numeric = frame.select_dtypes(include="number")
        if numeric.shape[1]:
            return numeric.iloc[:, 0]
        return pd.to_numeric(frame.iloc[:, 0], errors="coerce")

    def as_datetime(series):
        series = pd.Series(series).reset_index(drop=True)
        if pd.api.types.is_datetime64_any_dtype(series):
            return pd.to_datetime(series)
        if pd.api.types.is_numeric_dtype(series):
            num = pd.to_numeric(series, errors="coerce")
            if num.notna().mean() > 0.8 and num.dropna().median() > 200:
                return pd.to_datetime(num, unit="D", origin="1899-12-30")
            return None
        parsed = pd.to_datetime(series, errors="coerce")
        if parsed.notna().mean() > 0.8:
            return parsed
        return None

    df = to_frame(data)
    date_out = None
    if dates is not None:
        date_out = to_frame(dates).iloc[:, 0]
        y = first_numeric(df)
        parsed = as_datetime(date_out)
        if parsed is not None:
            date_out = parsed
    else:
        date_col = None
        for col in df.columns:
            parsed = as_datetime(df[col])
            if parsed is not None and (
                pd.api.types.is_datetime64_any_dtype(df[col])
                or not pd.api.types.is_numeric_dtype(df[col])
                or df.select_dtypes(include="number").shape[1] > 1
            ):
                date_col = col
                date_out = parsed
                break
        y = first_numeric(df.drop(columns=[date_col])) if date_col is not None else first_numeric(df)

    y = pd.to_numeric(pd.Series(y).reset_index(drop=True), errors="coerce")
    period = int(pd.Series(period).iloc[0])
    if date_out is not None:
        date_out = pd.Series(date_out).reset_index(drop=True)
        n = min(len(y), len(date_out))
        y = y.iloc[:n]
        date_out = date_out.iloc[:n]
        keep = y.notna() & date_out.notna()
        y = y[keep]
        date_out = date_out[keep]
        series = pd.Series(y.to_numpy(), index=pd.Index(date_out), name="observed")
    else:
        y = y.dropna()
        series = pd.Series(y.to_numpy(), name="observed")

    return STL(series, period=period, robust=bool(robust)).fit()


def stl(data, period, dates=None, robust=False, headers=False):
    """Decompose a series with STL (LOESS). Result spills as a table.

    data: value column, or a date+value range/table.
    period: observations per season (12 monthly, 7 weekly). Required.
    dates: optional date column when it is not in data.
    robust: True down-weights outliers in the LOESS smoothers.
    headers: first row is headers when data or dates is a ref string.

    Columns: date (if dates were found), observed, trend, seasonal, resid.
    Additive identity: observed = trend + seasonal + resid.
    For the four-panel chart, use stl_plot.
    """
    fit = stl_fit(data, period, dates=dates, robust=robust, headers=headers)
    out = pd.DataFrame(
        {
            "observed": fit.observed.to_numpy(),
            "trend": fit.trend.to_numpy(),
            "seasonal": fit.seasonal.to_numpy(),
            "resid": fit.resid.to_numpy(),
        }
    )
    idx = fit.observed.index
    if not isinstance(idx, pd.RangeIndex):
        out.insert(0, "date", idx)
    return out.reset_index(drop=True)

"stl(data, period, dates=None, robust=False, headers=False)"


def stl_plot(data, period, dates=None, robust=False, weights=False, headers=False):
    """Four-panel STL chart: observed, trend, seasonal, resid.

    Same inputs as stl. Returns a matplotlib Figure (DecomposeResult.plot).
    Keep the PY cell as a Python object, not Excel value.

    weights: True adds the robust-LOESS weight panel (use with robust=True).
    """
    fit = stl_fit(data, period, dates=dates, robust=robust, headers=headers)
    return fit.plot(weights=bool(weights))

"stl_plot(data, period, dates=None, robust=False, weights=False, headers=False)"


def resid_analysis(data, lags=None, plot=False, headers=False):
    """Diagnose a residual series.

    data: residual column, stl() result (uses column resid), DataFrame, Series, or xl() result.
    lags: Ljung-Box / ACF lag count. Default min(10, n-2).
    plot: False spills a metric/value table; True returns a matplotlib Figure.
    headers: first row is headers when data is a ref string.

    Table includes n, mean, std, min, max, sum, slope/intercept/R² vs order
    (same idea as VBA ResidualsAnalysis), Ljung-Box, and Jarque-Bera.
    Chart: residuals vs order, histogram, QQ, ACF.
    Need at least 3 numeric values.
    """
    import matplotlib.pyplot as plt
    from scipy import stats
    from statsmodels.graphics.gofplots import qqplot
    from statsmodels.graphics.tsaplots import plot_acf
    from statsmodels.stats.diagnostic import acorr_ljungbox

    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        cols = {str(c).strip().lower(): c for c in data.columns}
        resid_col = next((cols[n] for n in ("resid", "residual", "residuals") if n in cols), None)
        if resid_col is not None:
            series = data[resid_col]
        else:
            numeric = data.select_dtypes(include="number")
            series = numeric.iloc[:, 0] if numeric.shape[1] else data.iloc[:, 0]
    elif isinstance(data, pd.Series):
        series = data
    else:
        series = pd.Series(data)

    y = pd.to_numeric(pd.Series(series).squeeze(), errors="coerce").dropna().to_numpy(dtype=float)
    n = int(y.size)
    if n < 3:
        raise ValueError("Need at least 3 residual values.")

    order = np.arange(1, n + 1, dtype=float)
    slope, intercept = np.polyfit(order, y, 1)
    fitted = intercept + slope * order
    ss_res = float(np.sum((y - fitted) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    rsq = float("nan") if ss_tot == 0 else 1.0 - ss_res / ss_tot

    max_lag = max(1, n - 2)
    lag = min(max_lag, 10 if lags is None else int(pd.Series(lags).iloc[0]))
    lag = max(1, lag)

    try:
        lb = acorr_ljungbox(y, lags=lag, return_df=True)
        lb_stat = float(lb["lb_stat"].iloc[-1])
        lb_p = float(lb["lb_pvalue"].iloc[-1])
    except (ValueError, np.linalg.LinAlgError):
        lb_stat = float("nan")
        lb_p = float("nan")

    try:
        jb_stat, jb_p = stats.jarque_bera(y)
        jb_stat, jb_p = float(jb_stat), float(jb_p)
    except ValueError:
        jb_stat = float("nan")
        jb_p = float("nan")

    if plot:
        fig, axes = plt.subplots(2, 2, figsize=(8, 8))
        axes[0, 0].scatter(order, y, marker="x", s=16, color="black")
        axes[0, 0].plot(order, fitted, color="C0", lw=1)
        axes[0, 0].axhline(0, color="gray", lw=0.8)
        axes[0, 0].set_title("Residuals vs order")
        axes[0, 0].set_xlabel("Order")
        axes[0, 0].set_ylabel("Residuals")
        axes[0, 1].hist(y, bins="auto", color="C0", edgecolor="white")
        axes[0, 1].set_title("Histogram")
        qqplot(y, line="s", ax=axes[1, 0])
        axes[1, 0].set_title("Normal QQ")
        plot_acf(y, ax=axes[1, 1], lags=lag)
        axes[1, 1].set_title("ACF")
        fig.suptitle("Residual analysis")
        fig.tight_layout()
        return fig

    return pd.DataFrame(
        {
            "metric": [
                "n",
                "mean",
                "std",
                "min",
                "max",
                "sum",
                "slope_vs_order",
                "intercept_vs_order",
                "rsq_vs_order",
                "ljung_box_lags",
                "ljung_box_stat",
                "ljung_box_pvalue",
                "jarque_bera_stat",
                "jarque_bera_pvalue",
            ],
            "value": [
                n,
                float(y.mean()),
                float(np.std(y, ddof=1)),
                float(y.min()),
                float(y.max()),
                float(y.sum()),
                float(slope),
                float(intercept),
                rsq,
                lag,
                lb_stat,
                lb_p,
                jb_stat,
                jb_p,
            ],
        }
    )

"resid_analysis(data, lags=None, plot=False, headers=False)"


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

