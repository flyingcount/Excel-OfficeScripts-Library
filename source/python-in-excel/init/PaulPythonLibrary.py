# Paul Python in Excel library
#
# Formulas → Initialization → replace the editor contents with this file → Save.
# This file is a complete Initialization: Excel defaults, then the library functions.
#
# Restore defaults only: paste init/DefaultInitialization.py instead.
# Sampling functions only: paste init/Sampling.py instead.
# Time series functions only: paste init/TimeSeries.py instead.
# Add functions to an existing default Initialization: paste from the first def onward.
#
# Requires Microsoft 365 Python in Excel. Functions use Excel's xl() helper.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels as sm
import excel
import warnings

warnings.simplefilter('ignore')

excel.set_xl_scalar_conversion(excel.convert_to_scalar)
excel.set_xl_array_conversion(excel.convert_to_dataframe)


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
    """Diagnose a residual series. plot=False spills metric/value/guidance; True is a 4-panel chart.

    data: residual column, stl() result (uses resid), DataFrame, Series, or xl() result.
    lags: Ljung-Box / ACF lags. Default min(10, n-2). headers: first row is headers for a ref string.
    Need at least 3 numeric values. Z-scored series is result.std_resid.
    """
    from scipy import stats
    from statsmodels.graphics.gofplots import qqplot
    from statsmodels.graphics.tsaplots import plot_acf
    from statsmodels.stats.diagnostic import acorr_ljungbox
    from statsmodels.stats.stattools import durbin_watson

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

    try:
        dw_stat = float(durbin_watson(y))
    except (ValueError, ZeroDivisionError):
        dw_stat = float("nan")
    if not np.isfinite(dw_stat):
        dw_stat = float("nan")

    try:
        sh_stat, sh_p = stats.shapiro(y)
        sh_stat, sh_p = float(sh_stat), float(sh_p)
    except ValueError:
        sh_stat, sh_p = float("nan"), float("nan")

    try:
        std_resid = np.asarray(stats.zscore(y), dtype=float)
    except ValueError:
        std_resid = np.full(n, np.nan)
    finite_z = np.isfinite(std_resid)
    if finite_z.any():
        std_resid_max_abs = float(np.max(np.abs(std_resid[finite_z])))
        n_std_resid_gt_2 = int(np.sum(np.abs(std_resid[finite_z]) > 2.0))
    else:
        std_resid_max_abs = float("nan")
        n_std_resid_gt_2 = 0
    std_resid_series = pd.Series(std_resid)

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
        fig.std_resid = std_resid_series
        return fig

    out = pd.DataFrame(
        [
            ("n", n, "Count of residual values after dropping blanks."),
            (
                "mean",
                float(y.mean()),
                "Ideal residuals center near 0. A large |mean| suggests systematic bias.",
            ),
            (
                "std",
                float(np.std(y, ddof=1)),
                "Sample standard deviation (n-1). Larger values mean noisier residuals.",
            ),
            (
                "min",
                float(y.min()),
                "Smallest residual. A large negative value can be an outlier.",
            ),
            (
                "max",
                float(y.max()),
                "Largest residual. A large positive value can be an outlier.",
            ),
            (
                "sum",
                float(y.sum()),
                "Sum of residuals. Near 0 when the mean is near 0.",
            ),
            (
                "slope_vs_order",
                float(slope),
                "Linear drift vs observation order. Near 0 means no trend in the residuals.",
            ),
            (
                "intercept_vs_order",
                float(intercept),
                "Fitted residual at order 1 of that trend line.",
            ),
            (
                "rsq_vs_order",
                rsq,
                "Share of residual variation explained by a straight line vs order. Near 0 is better.",
            ),
            (
                "ljung_box_lags",
                lag,
                "Lag count used for Ljung-Box and the ACF plot.",
            ),
            (
                "ljung_box_stat",
                lb_stat,
                "Ljung-Box Q statistic. Larger values suggest leftover autocorrelation.",
            ),
            (
                "ljung_box_pvalue",
                lb_p,
                "p < 0.05 suggests leftover autocorrelation at the chosen lag.",
            ),
            (
                "jarque_bera_stat",
                jb_stat,
                "Jarque-Bera statistic. Larger values suggest residuals are not normal.",
            ),
            (
                "jarque_bera_pvalue",
                jb_p,
                "p < 0.05 suggests residuals are not normal.",
            ),
            (
                "durbin_watson",
                dw_stat,
                "Near 2: little lag-1 autocorrelation. Toward 0: positive. Toward 4: negative.",
            ),
            (
                "shapiro_stat",
                sh_stat,
                "Shapiro-Wilk W. Values near 1 support normality.",
            ),
            (
                "shapiro_pvalue",
                sh_p,
                "p > 0.05: normality can be assumed. p < 0.05: residuals are not normal.",
            ),
            (
                "std_resid_max_abs",
                std_resid_max_abs,
                "Largest |z-score|. |z| > 2 is unusual; |z| > 3 is extreme. Blank if constant.",
            ),
            (
                "n_std_resid_gt_2",
                n_std_resid_gt_2,
                "How many points have |z-score| > 2. Zero is typical; many suggest outliers.",
            ),
        ],
        columns=["metric", "value", "guidance"],
    )
    object.__setattr__(out, "std_resid", std_resid_series)
    return out


"resid_analysis(data, lags=None, plot=False, headers=False)"


def _norm_values(data, headers=False):
    """First numeric column as float. Drops blanks. Need at least 3 values."""
    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        numeric = data.select_dtypes(include="number")
        values = numeric.iloc[:, 0] if numeric.shape[1] else data.iloc[:, 0]
    else:
        values = data
    y = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce").dropna().to_numpy(dtype=float)
    if y.size < 3:
        raise ValueError("Need at least 3 numeric values.")
    return y


def _norm_df(rows, notes):
    return pd.DataFrame({"metric": list(rows), "value": list(rows.values()), "interpretation": notes})


def shapiro(data, metric=None, headers=False):
    """Shapiro-Wilk W and p. metric 'pvalue' or 'stat' for a float; omit for the table."""
    from scipy import stats

    y = _norm_values(data, headers)
    try:
        sh_stat, sh_p = (float(x) for x in stats.shapiro(y))
    except ValueError:
        sh_stat, sh_p = float("nan"), float("nan")
    rows = {"shapiro_stat": sh_stat, "shapiro_pvalue": sh_p}
    if metric is not None:
        key = str(pd.Series(metric).iloc[0]).strip().lower()
        aliases = {"stat": "shapiro_stat", "w": "shapiro_stat", "pvalue": "shapiro_pvalue", "p": "shapiro_pvalue", "p_value": "shapiro_pvalue"}
        aliases.update({k: k for k in rows})
        if key not in aliases:
            raise ValueError("metric must be 'stat', 'pvalue', or omitted for the table.")
        return float(rows[aliases[key]])
    if not np.isfinite(sh_p):
        p_note = "Test did not run."
    elif sh_p > 0.05:
        p_note = "p > 0.05: a normal distribution in the data can be assumed."
    else:
        p_note = "p <= 0.05: data are not consistent with a normal distribution."
    return _norm_df(rows, ["Shapiro-Wilk W. Values near 1 support normality.", p_note])


def anderson(data, metric=None, headers=False):
    """Anderson-Darling A^2. metric 'stat' or 'critical_5' for a float; omit for the table."""
    from scipy import stats

    y = _norm_values(data, headers)
    rows = {"anderson_stat": float("nan")}
    aliases = {"stat": "anderson_stat", "a2": "anderson_stat", "anderson_stat": "anderson_stat"}
    try:
        ad = stats.anderson(y, dist="norm")
        rows["anderson_stat"] = float(ad.statistic)
        for sig, val in zip(np.asarray(ad.significance_level, dtype=float), np.asarray(ad.critical_values, dtype=float)):
            tag = "2_5" if abs(sig - 2.5) < 1e-9 else str(int(sig)) if abs(sig - int(sig)) < 1e-9 else str(sig).replace(".", "_")
            name, short = f"anderson_critical_{tag}", f"critical_{tag}"
            rows[name] = float(val)
            aliases[short] = aliases[name] = name
            aliases[str(int(sig)) if abs(sig - int(sig)) < 1e-9 else str(sig)] = name
    except ValueError:
        pass
    if metric is not None:
        key = str(pd.Series(metric).iloc[0]).strip().lower()
        if key not in aliases:
            raise ValueError("metric must be 'stat', 'critical_5', or omitted for the table.")
        return float(rows[aliases[key]])
    ad_stat, crit_5 = rows["anderson_stat"], rows.get("anderson_critical_5", float("nan"))
    if not np.isfinite(ad_stat) or not np.isfinite(crit_5):
        ad_note = "If A^2 is less than the 5% critical value, the data is normal. If not, it is not normal."
    elif ad_stat > crit_5:
        ad_note = "A^2 is not less than the 5% critical value, so the data is not normal."
    else:
        ad_note = "A^2 is less than the 5% critical value, so the data is normal."
    crit_note = "If A^2 is less than this value, the data is normal. If not, it is not normal."
    notes = [ad_note if n == "anderson_stat" else crit_note if n.startswith("anderson_critical_") else "" for n in rows]
    return _norm_df(rows, notes)


def normality_check(data, plot=True, headers=False):
    """Q-Q plot with Shapiro-Wilk and Anderson-Darling. plot=False spills a table."""
    from scipy import stats

    y = _norm_values(data, headers)
    sh, ad = shapiro(y), anderson(y)
    table = pd.concat(
        [
            pd.DataFrame({"metric": ["n"], "value": [int(y.size)], "interpretation": ["Count after dropping blanks."]}),
            sh,
            ad.loc[ad["metric"].isin(["anderson_stat", "anderson_critical_5"])],
        ],
        ignore_index=True,
    )
    if not plot:
        return table
    idx = table.set_index("metric")["value"]
    sh_stat, sh_p = float(idx["shapiro_stat"]), float(idx["shapiro_pvalue"])
    ad_stat, crit_5 = float(idx["anderson_stat"]), float(idx["anderson_critical_5"])
    fig, ax = plt.subplots(figsize=(6, 5))
    stats.probplot(y, dist="norm", plot=ax)
    ax.set_title("Q-Q plot")
    ax.text(
        0.02,
        0.98,
        f"Shapiro-Wilk  W = {sh_stat:.3f}  p = {sh_p:.3f}\n"
        f"(If p > 0.05, normal distribution in the data can be assumed)\n"
        f"Anderson-Darling  A^2 = {ad_stat:.3f}  (5% crit. {crit_5:.3f})",
        transform=ax.transAxes,
        va="top",
        ha="left",
        fontsize=9,
        bbox={"boxstyle": "round", "facecolor": "white", "alpha": 0.85},
    )
    fig.tight_layout()
    fig.shapiro_stat = sh_stat
    fig.shapiro_pvalue = sh_p
    fig.anderson_stat = ad_stat
    fig.anderson_critical_5 = crit_5
    fig.results = table
    return fig

qq_norm = normality_check

"""normality_check(data, plot=True, headers=False)
 qq_norm(data, plot=True, headers=False)
 shapiro(data, metric=None, headers=False)
 anderson(data, metric=None, headers=False)"""



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


def arima_estimate(data, p_max=3, q_max=3, d_max=2, criterion="aic",
                   alpha=0.05, full=False, headers=False):
    """Estimate ARIMA order: ADF test sets d, then grid search minimises AIC or BIC.

    1. Differencing order d is chosen by repeated ADF tests: difference the
       series until the ADF p-value < alpha or d reaches d_max.
    2. For the chosen d, fit ARIMA(p, d, q) for every p in 0..p_max and
       q in 0..q_max. The model with the lowest criterion wins.

    data: value column, ref string, Series, or DataFrame (first numeric col).
    p_max: maximum AR order to search. Default 3.
    q_max: maximum MA order to search. Default 3.
    d_max: maximum differencing order for ADF. Default 2.
    criterion: 'aic' (default) or 'bic'.
    alpha: ADF significance level for stationarity. Default 0.05.
    full: False (default) returns one best-order row. True returns the full
        grid sorted by the chosen criterion.
    headers: first row is headers when data is a ref string.

    Result columns: p, d, q, aic, bic.  full=True adds all fitted models.
    The adf_pvalue and adf_d columns show the test result for the chosen d.
    """
    import warnings
    from statsmodels.tsa.arima.model import ARIMA
    from statsmodels.tsa.stattools import adfuller

    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        numeric = data.select_dtypes(include="number")
        values = numeric.iloc[:, 0] if numeric.shape[1] else data.iloc[:, 0]
    else:
        values = data
    y = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce").dropna()
    if y.shape[0] < 4:
        raise ValueError("Need at least 4 observations.")

    p_max = int(pd.Series(p_max).iloc[0])
    q_max = int(pd.Series(q_max).iloc[0])
    d_max = int(pd.Series(d_max).iloc[0])
    alpha = float(pd.Series(alpha).iloc[0])
    crit = str(pd.Series(criterion).iloc[0]).strip().lower() if not isinstance(
        criterion, str) else criterion.strip().lower()
    if crit not in ("aic", "bic"):
        raise ValueError("criterion must be 'aic' or 'bic', got '%s'." % crit)

    d = 0
    adf_p = np.nan
    series = y.copy()
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        for _ in range(d_max + 1):
            if series.shape[0] < 4:
                break
            try:
                result = adfuller(series, autolag="AIC")
                adf_p = float(result[1])
            except Exception:
                break
            if adf_p < alpha:
                break
            if d < d_max:
                d += 1
                series = series.diff().dropna()
            else:
                break

    rows = []
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        for p in range(p_max + 1):
            for q in range(q_max + 1):
                try:
                    fit = ARIMA(y, order=(p, d, q)).fit()
                    a = float(fit.aic)
                    b = float(fit.bic)
                    if np.isfinite(a) and np.isfinite(b):
                        rows.append((p, d, q, a, b))
                except Exception:
                    pass

    if not rows:
        out = pd.DataFrame(columns=["p", "d", "q", "aic", "bic",
                                     "adf_pvalue", "adf_d"])
        return out

    grid = pd.DataFrame(rows, columns=["p", "d", "q", "aic", "bic"])
    grid = grid.sort_values(crit).reset_index(drop=True)
    grid["adf_pvalue"] = adf_p
    grid["adf_d"] = d

    if full:
        return grid
    return grid.iloc[:1].reset_index(drop=True)

"arima_estimate(data, p_max=3, q_max=3, d_max=2, criterion='aic', alpha=0.05, full=False, headers=False)"


def baseline_forecast(data, date_col=None, value_col=None, h=12, method="naive",
                      period=1, headers=True):
    """Baseline forecast: naive, seasonal_naive, or drift.

    Reads a date column and value column from a table, spills actual rows then
    forecast rows appended. Each row has label 'Actual' or 'Forecast Naive',
    'Forecast Seasonal Naive', or 'Forecast Drift'.

    data: table/range with dates and values, DataFrame, or value Series/list.
    date_col: header of the date column when data is a table. Auto-detected if
        omitted.
    value_col: header of the value column. Auto-detected if omitted.
    h: forecast horizon. Default 12.
    method: 'naive' (default), 'seasonal_naive' (or 'snaive'), or 'drift'.
    period: seasonal period for seasonal_naive. Default 1.
    headers: first row is headers when data is a ref string. Default True.

    Result columns: date, value, label.
    """
    def to_frame(value):
        if isinstance(value, str):
            value = xl(value, headers=headers)
        if isinstance(value, pd.DataFrame):
            return value
        if isinstance(value, pd.Series):
            return value.to_frame()
        return pd.DataFrame(value)

    def pick_col(frame, name, kind):
        if name is not None:
            key = str(pd.Series(name).iloc[0]).strip()
            cols = {str(c).strip().lower(): c for c in frame.columns}
            if key.lower() in cols:
                return frame[cols[key.lower()]]
            if key in frame.columns:
                return frame[key]
            raise ValueError("Column '%s' not found in data." % key)
        if kind == "date":
            for col in frame.columns:
                s = frame[col]
                if pd.api.types.is_datetime64_any_dtype(s):
                    return pd.to_datetime(s)
                if pd.api.types.is_numeric_dtype(s):
                    num = pd.to_numeric(s, errors="coerce")
                    if num.notna().mean() > 0.8 and num.dropna().median() > 200:
                        return pd.to_datetime(num, unit="D", origin="1899-12-30")
                parsed = pd.to_datetime(s, errors="coerce")
                if parsed.notna().mean() > 0.8:
                    return parsed
            return None
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
        parsed = pd.to_datetime(series, errors="coerce")
        if parsed.notna().mean() > 0.8:
            return parsed
        return None

    def forecast_dates(last_dt, prev, h):
        prev = pd.Series(prev).dropna()
        if last_dt is None or (not isinstance(last_dt, (int, float)) and not pd.notna(last_dt)):
            start = float(prev.shape[0]) if prev.shape[0] else 0.0
            return pd.Series(np.arange(start + 1, start + h + 1), dtype="float64")
        if prev.shape[0] >= 2 and pd.api.types.is_datetime64_any_dtype(prev):
            step = prev.diff().dropna().median()
            if pd.isna(step) or step <= pd.Timedelta(0):
                step = pd.Timedelta(days=1)
            return pd.Series([last_dt + step * (i + 1) for i in range(h)])
        step = float(prev.diff().dropna().median()) if prev.shape[0] >= 2 else 1.0
        if not np.isfinite(step) or step <= 0:
            step = 1.0
        base = float(last_dt)
        return pd.Series([base + step * (i + 1) for i in range(h)], dtype="float64")

    frame = to_frame(data)
    dates_raw = pick_col(frame, date_col, "date")
    values = pick_col(frame, value_col, "value")
    values = pd.to_numeric(pd.Series(values).reset_index(drop=True), errors="coerce")
    dates = None
    if dates_raw is not None:
        dates = pd.Series(dates_raw).reset_index(drop=True)
        parsed = as_datetime(dates)
        if parsed is not None:
            dates = parsed
    keep = values.notna()
    if dates is not None:
        dates = dates[keep].reset_index(drop=True)
    values = values[keep].reset_index(drop=True)
    y = values.to_numpy(dtype="float64")
    n = int(y.size)
    if n < 1:
        raise ValueError("Need at least 1 observation.")

    h = max(1, int(pd.Series(h).iloc[0]))
    m = str(pd.Series(method).iloc[0]).strip().lower() if not isinstance(
        method, str) else method.strip().lower()
    period = max(1, int(pd.Series(period).iloc[0]))
    labels = {
        "naive": "Forecast Naive",
        "seasonal_naive": "Forecast Seasonal Naive",
        "snaive": "Forecast Seasonal Naive",
        "drift": "Forecast Drift",
    }
    if m not in labels:
        raise ValueError(
            "method '%s' not supported. Use 'naive', 'seasonal_naive', or 'drift'." % m)
    fc_label = labels[m]

    fc = np.empty(h, dtype="float64")
    if m == "naive":
        fc[:] = y[-1]
    elif m in ("seasonal_naive", "snaive"):
        if n < period:
            raise ValueError(
                "Need at least %d observations for seasonal_naive with period=%d."
                % (period, period))
        tail = y[-period:]
        for i in range(h):
            fc[i] = tail[i % period]
    else:
        if n < 2:
            raise ValueError("Need at least 2 observations for drift.")
        slope = (y[-1] - y[0]) / (n - 1)
        for i in range(h):
            fc[i] = y[-1] + (i + 1) * slope

    if dates is None:
        act_dates = pd.Series(np.arange(1, n + 1), dtype="float64")
        last_dt = float(n)
        prev_dates = act_dates
    else:
        act_dates = dates
        last_dt = dates.iloc[-1]
        prev_dates = dates

    fc_dates = forecast_dates(last_dt, prev_dates, h)
    actual = pd.DataFrame({
        "date": act_dates,
        "value": y,
        "label": "Actual",
    })
    forecast = pd.DataFrame({
        "date": fc_dates.reset_index(drop=True),
        "value": fc,
        "label": fc_label,
    })
    return pd.concat([actual, forecast], ignore_index=True)

"baseline_forecast(data, date_col=None, value_col=None, h=12, method='naive', period=1, headers=True)"


def zscore_replace(data, z=3, dates=None, headers=False):
    """Replace points with |z-score| > z by interpolating neighboring values.

    z-scores use the series mean and population standard deviation (ddof=0).
    Interior outliers are filled with linear interpolation (time-based when
    dates are available). Leading or trailing outliers use the nearest
    remaining value. Original blanks stay blank.

    data: value column, date+value range/table, Series, or list.
    z: absolute z-score cutoff (default 3).
    dates: optional date column when it is not in data.
    headers: first row is headers when data or dates is a ref string.

    Result is a Series named value, same length as the input values.
    """

    def to_frame(value):
        if isinstance(value, str):
            value = xl(value, headers=headers)
        if isinstance(value, pd.DataFrame):
            return value
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

    y = pd.to_numeric(pd.Series(y).reset_index(drop=True), errors="coerce").astype("float64")
    z = abs(float(pd.Series(z).iloc[0]))
    if date_out is not None:
        date_out = pd.Series(date_out).reset_index(drop=True)
        n = min(len(y), len(date_out))
        y = y.iloc[:n].reset_index(drop=True)
        date_out = date_out.iloc[:n]
        date_idx = pd.Index(date_out)
        use_time = (
            isinstance(date_idx, pd.DatetimeIndex)
            and date_idx.notna().all()
            and date_idx.is_monotonic_increasing
            and date_idx.is_unique
        )
    else:
        use_time = False

    sigma = float(y.std(ddof=0, skipna=True))
    if not np.isfinite(sigma) or sigma == 0:
        outliers = pd.Series(False, index=y.index)
    else:
        outliers = ((y - y.mean(skipna=True)) / sigma).abs() > z
        outliers = outliers.fillna(False)

    masked = y.where(~outliers)
    if use_time:
        filled = pd.Series(masked.to_numpy(), index=date_idx)
        filled = filled.interpolate(method="time", limit_direction="both")
        filled = pd.Series(filled.bfill().ffill().to_numpy(), index=y.index)
    else:
        filled = masked.interpolate(method="linear", limit_direction="both")
        filled = filled.bfill().ffill()

    cleaned = y.where(~outliers, filled)
    return pd.Series(cleaned.to_numpy(), name="value")

"zscore_replace(data, z=3, dates=None, headers=False)"


def date_features(data, cyclical=True, calendar=True, fourier=1, country_holiday="UK", headers=False):
    """Calendar parts, sine/cosine cycle encodings, and a public-holiday flag.

    Cyclical pairs wrap at the end of each cycle, so December sits next to
    January and Sunday next to Monday. Angle is 2 * pi * k * position / period
    with position 0 at the start of the cycle (January, day 1, Monday).

    data: date column, a range/table containing dates, Series, or list.
    cyclical: add sin/cos pairs for month, day, dayofweek, dayofyear.
    calendar: add integer parts (year, quarter, month, week, day, dayofweek,
        dayofyear, days_in_month, is_weekend, is_month_end, is_quarter_end).
    fourier: harmonics per cycle. 1 gives month_sin / month_cos; 2 also gives
        month_sin_2 / month_cos_2 for a second, faster wave.
    country_holiday: two-letter country code for the is_holiday column.
        'UK' (default) or 'US'. None or False disables the column.
    headers: first row is headers when data is a ref string.

    Excel serial numbers are read with the 1899-12-30 origin. Blank or
    unparseable dates keep their row and spill blank features. Result spills
    as a table with a date column plus the requested features.
    """
    from datetime import date, timedelta

    def _easter(year):
        a = year % 19
        b, c = divmod(year, 100)
        d, e = divmod(b, 4)
        f = (b + 8) // 25
        g = (b - f + 1) // 3
        h = (19 * a + b - d - g + 15) % 30
        i, k = divmod(c, 4)
        el = (32 + 2 * e + 2 * i - h - k) % 7
        m = (a + 11 * h + 22 * el) // 451
        month, day = divmod(h + el - 7 * m + 114, 31)
        return date(year, month, day + 1)

    def _sub_uk(d):
        wd = d.weekday()
        return d + timedelta(days=2) if wd == 5 else d + timedelta(days=1) if wd == 6 else d

    def _sub_us(d):
        wd = d.weekday()
        return d - timedelta(days=1) if wd == 5 else d + timedelta(days=1) if wd == 6 else d

    def _nth_weekday(year, month, weekday, n):
        d = date(year, month, 1)
        while d.weekday() != weekday:
            d += timedelta(days=1)
        return d + timedelta(weeks=n - 1)

    def _last_mon(year, month):
        d = date(year, month + 1, 1) - timedelta(days=1) if month < 12 else date(year, 12, 31)
        while d.weekday() != 0:
            d -= timedelta(days=1)
        return d

    def _uk_holidays(year):
        hols = set()
        hols.add(_sub_uk(date(year, 1, 1)))
        es = _easter(year)
        hols.add(es - timedelta(days=2))
        hols.add(es + timedelta(days=1))
        hols.add(_nth_weekday(year, 5, 0, 1))
        hols.add(_last_mon(year, 5))
        hols.add(_last_mon(year, 8))
        xmas = _sub_uk(date(year, 12, 25))
        boxing = _sub_uk(date(year, 12, 26))
        hols.add(xmas)
        hols.add(boxing)
        if xmas == boxing:
            boxing = xmas + timedelta(days=1)
            hols.add(boxing)
        return hols

    def _us_holidays(year):
        hols = set()
        hols.add(_sub_us(date(year, 1, 1)))
        hols.add(_nth_weekday(year, 1, 0, 3))
        hols.add(_nth_weekday(year, 2, 0, 3))
        hols.add(_last_mon(year, 5))
        hols.add(_sub_us(date(year, 6, 19)))
        hols.add(_sub_us(date(year, 7, 4)))
        hols.add(_nth_weekday(year, 9, 0, 1))
        hols.add(_nth_weekday(year, 10, 0, 2))
        hols.add(_sub_us(date(year, 11, 11)))
        hols.add(_nth_weekday(year, 11, 3, 4))
        hols.add(_sub_us(date(year, 12, 25)))
        return hols

    def _holidays_for(country, years):
        fn = {"UK": _uk_holidays, "US": _us_holidays}.get(
            str(country).strip().upper())
        if fn is None:
            raise ValueError(
                "country_holiday '%s' not supported. Use 'UK' or 'US'." % country)
        hols = set()
        for y in years:
            hols |= fn(int(y))
        return hols

    def to_frame(value):
        if isinstance(value, str):
            value = xl(value, headers=headers)
        if isinstance(value, pd.DataFrame):
            return value
        if isinstance(value, pd.Series):
            return value.to_frame()
        return pd.DataFrame(value)

    def as_datetime(series, min_valid=0.8):
        series = pd.Series(series).reset_index(drop=True)
        if pd.api.types.is_datetime64_any_dtype(series):
            return pd.to_datetime(series)
        if pd.api.types.is_numeric_dtype(series):
            num = pd.to_numeric(series, errors="coerce")
            if num.notna().mean() > min_valid and num.dropna().median() > 200:
                return pd.to_datetime(num, unit="D", origin="1899-12-30")
            return None
        parsed = pd.to_datetime(series, errors="coerce")
        if parsed.notna().mean() > min_valid:
            return parsed
        return None

    frame = to_frame(data)
    dates = None
    for col in frame.columns:
        dates = as_datetime(frame[col])
        if dates is not None:
            break
    if dates is None:
        dates = as_datetime(frame.iloc[:, 0], min_valid=0.0)
    if dates is None or not dates.notna().any():
        raise ValueError("No date column found in data.")

    dates = pd.Series(dates).reset_index(drop=True)
    harmonics = max(1, int(pd.Series(fourier).iloc[0]))
    dt = dates.dt
    out = pd.DataFrame({"date": dates})

    if calendar:
        out["year"] = dt.year
        out["quarter"] = dt.quarter
        out["month"] = dt.month
        out["week"] = pd.to_numeric(dt.isocalendar()["week"], errors="coerce").astype("float64")
        out["day"] = dt.day
        out["dayofweek"] = dt.dayofweek
        out["dayofyear"] = dt.dayofyear
        out["days_in_month"] = dt.days_in_month
        out["is_weekend"] = (dt.dayofweek >= 5).astype("float64")
        out["is_month_end"] = dt.is_month_end.astype("float64")
        out["is_quarter_end"] = dt.is_quarter_end.astype("float64")

    if cyclical:
        days_in_year = np.where(dt.is_leap_year.to_numpy(), 366.0, 365.0)
        cycles = (
            ("month", dt.month.to_numpy(dtype="float64") - 1.0, 12.0),
            ("day", dt.day.to_numpy(dtype="float64") - 1.0, dt.days_in_month.to_numpy(dtype="float64")),
            ("dayofweek", dt.dayofweek.to_numpy(dtype="float64"), 7.0),
            ("dayofyear", dt.dayofyear.to_numpy(dtype="float64") - 1.0, days_in_year),
        )
        for name, position, period in cycles:
            fraction = position / period
            for k in range(1, harmonics + 1):
                angle = 2.0 * np.pi * k * fraction
                suffix = "" if k == 1 else "_%d" % k
                out[name + "_sin" + suffix] = np.sin(angle)
                out[name + "_cos" + suffix] = np.cos(angle)

    if country_holiday and country_holiday is not True:
        ch = str(pd.Series(country_holiday).iloc[0]).strip().upper() if not isinstance(
            country_holiday, str) else country_holiday.strip().upper()
        valid = dates.dropna()
        if not valid.empty:
            yrs = valid.dt.year.unique()
            hset = _holidays_for(ch, yrs)
            out["is_holiday"] = dates.apply(
                lambda x: 1.0 if pd.notna(x) and x.date() in hset else 0.0)
        else:
            out["is_holiday"] = np.nan

    blank = dates.isna().to_numpy()
    if blank.any():
        for col in out.columns:
            if col != "date":
                out.loc[blank, col] = np.nan
    return out

"date_features(data, cyclical=True, calendar=True, fourier=1, country_holiday='UK', headers=False)"


def cluster_prep(data, headers=True):
    """Standard-scale numbers and one-hot encode categories for clustering.

    Auto-detects column types so any mixed table works. Drops empty rows and
    columns, then rows with remaining blanks. Datetimes become numeric days,
    bools become 0/1, and object columns that are mostly numbers are treated
    as numeric. Constant or all-unique text columns (IDs) are skipped.

    data: ref string, DataFrame, Series, or xl() result.
    headers: used only when data is a ref string.
    """
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import OneHotEncoder, StandardScaler

    def as_days(s):
        parsed = pd.to_datetime(s, utc=True, errors="coerce")
        return (parsed.astype("int64") / 8.64e13).where(parsed.notna())

    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        df = data
    elif isinstance(data, pd.Series):
        df = data.to_frame()
    else:
        df = pd.DataFrame(data)
    df = df.dropna(how="all").dropna(axis=1, how="all").replace("", np.nan).copy()
    if df.empty:
        raise ValueError("No data after dropping empty rows and columns.")

    num_cols, cat_cols = [], []
    for c in list(df.columns):
        s = df[c]
        if pd.api.types.is_bool_dtype(s):
            df[c] = s.astype("float64")
            num_cols.append(c)
            continue
        if pd.api.types.is_timedelta64_dtype(s):
            df[c] = s.dt.total_seconds()
            num_cols.append(c)
            continue
        if pd.api.types.is_datetime64_any_dtype(s):
            df[c] = as_days(s)
            num_cols.append(c)
            continue
        if pd.api.types.is_numeric_dtype(s):
            num_cols.append(c)
            continue
        conv = pd.to_numeric(s, errors="coerce")
        if s.notna().any() and float(conv.notna().mean()) >= 0.8:
            df[c] = conv
            num_cols.append(c)
            continue
        parsed = pd.to_datetime(s, utc=True, errors="coerce")
        if s.notna().any() and float(parsed.notna().mean()) >= 0.8:
            df[c] = as_days(s)
            num_cols.append(c)
            continue
        n_ok = int(s.notna().sum())
        n_unq = int(s.nunique(dropna=True))
        if n_unq <= 1 or n_unq >= n_ok:
            continue
        cat_cols.append(c)

    use = num_cols + cat_cols
    if not use:
        raise ValueError("No numeric or categorical columns to encode.")
    df = df.loc[:, use].dropna()
    if df.empty:
        raise ValueError("No rows left after dropping blanks.")
    if cat_cols:
        df[cat_cols] = df[cat_cols].astype(str)

    try:
        ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        ohe = OneHotEncoder(handle_unknown="ignore", sparse=False)
    steps = []
    if num_cols:
        steps.append(("num", StandardScaler(), num_cols))
    if cat_cols:
        steps.append(("cat", ohe, cat_cols))
    pre = ColumnTransformer(steps)
    arr = pre.fit_transform(df)
    if hasattr(arr, "toarray"):
        arr = arr.toarray()
    names = list(num_cols)
    if cat_cols:
        enc = pre.named_transformers_["cat"]
        try:
            names = names + list(enc.get_feature_names_out(cat_cols))
        except AttributeError:
            names = names + list(enc.get_feature_names(cat_cols))
    return pd.DataFrame(np.asarray(arr), columns=names)

"cluster_prep(data, headers=True)"


def outlier_flag(data, method="iqr", threshold=1.5, headers=False):
    """Flag outlier rows by IQR, MAD, or z-score. Returns the original values
    plus is_outlier (1/0), score, lower_bound, and upper_bound columns.

    data: value column, ref string, DataFrame, Series, or list.
    method: 'iqr' (default), 'mad', or 'zscore'.
    threshold: sensitivity. IQR multiplier (default 1.5; 3 for far outliers),
        MAD multiplier (default 1.5; ~2 is common), or z-score cutoff
        (pass 3 for z-score). Meaning depends on method.
    headers: first row is headers when data is a ref string.

    Methods:
      iqr     — outlier when value < Q1 - t*IQR or > Q3 + t*IQR.
      mad     — outlier when |value - median| / MAD > t  (MAD scaled by
                1.4826 to approximate std for normal data).
      zscore  — outlier when |value - mean| / std > t  (population std,
                ddof=0, same convention as zscore_replace).

    A constant column (spread = 0) flags nothing. Blanks stay blank.
    Result is a DataFrame with columns value, is_outlier, score,
    lower_bound, upper_bound.
    """
    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        numeric = data.select_dtypes(include="number")
        values = numeric.iloc[:, 0] if numeric.shape[1] else data.iloc[:, 0]
    elif isinstance(data, pd.Series):
        values = data
    else:
        values = pd.Series(data)

    y = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce").astype("float64")
    y = y.reset_index(drop=True)
    t = abs(float(pd.Series(threshold).iloc[0]))
    m = str(pd.Series(method).iloc[0]).strip().lower() if not isinstance(
        method, str) else method.strip().lower()

    n = y.dropna().shape[0]
    score = pd.Series(np.nan, index=y.index, dtype="float64")
    lo = np.nan
    hi = np.nan

    if m == "iqr":
        q1 = float(y.quantile(0.25))
        q3 = float(y.quantile(0.75))
        iqr = q3 - q1
        lo = q1 - t * iqr
        hi = q3 + t * iqr
        if iqr == 0:
            outliers = pd.Series(False, index=y.index)
        else:
            outliers = (y < lo) | (y > hi)
            outliers = outliers.fillna(False)
        score = y.copy()
    elif m == "mad":
        med = float(y.median(skipna=True))
        abs_dev = (y - med).abs()
        mad_raw = float(abs_dev.median(skipna=True))
        mad_scaled = mad_raw * 1.4826
        if mad_scaled == 0 or not np.isfinite(mad_scaled):
            outliers = pd.Series(False, index=y.index)
        else:
            score = abs_dev / mad_scaled
            outliers = score > t
            outliers = outliers.fillna(False)
            lo = med - t * mad_scaled
            hi = med + t * mad_scaled
    elif m == "zscore":
        mu = float(y.mean(skipna=True))
        sigma = float(y.std(ddof=0, skipna=True))
        if sigma == 0 or not np.isfinite(sigma):
            outliers = pd.Series(False, index=y.index)
        else:
            score = ((y - mu) / sigma).abs()
            outliers = score > t
            outliers = outliers.fillna(False)
            lo = mu - t * sigma
            hi = mu + t * sigma
    else:
        raise ValueError(
            "method '%s' not supported. Use 'iqr', 'mad', or 'zscore'." % m)

    out = pd.DataFrame({
        "value": y,
        "is_outlier": outliers.astype("float64"),
        "score": score,
        "lower_bound": lo,
        "upper_bound": hi,
    })
    blank = y.isna().to_numpy()
    if blank.any():
        out.loc[blank, ["is_outlier", "score", "lower_bound", "upper_bound"]] = np.nan
    return out

"outlier_flag(data, method='iqr', threshold=1.5, headers=False)"


def stratified_sample(data, strata_col, total_n, random_state=42, headers=True):
    """Draw a proportional stratified sample.

    Each stratum gets round(total_n * its share of the population) rows,
    at least 1 when the stratum is non-empty, capped at the stratum size.

    data: ref string, DataFrame, Series, or xl() result.
    strata_col: column name that defines the strata.
    total_n: target sample size across all strata.
    random_state: seed for reproducibility (default 42).
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
    df = df.dropna(how="all")
    if df.empty:
        raise ValueError("No data after dropping empty rows.")

    strata_col = str(pd.Series(strata_col).iloc[0]).strip()
    if strata_col not in df.columns:
        lookup = {str(c).strip().lower(): c for c in df.columns}
        key = strata_col.lower()
        if key not in lookup:
            raise ValueError("strata_col not found.")
        strata_col = lookup[key]

    total_n = int(pd.Series(total_n).iloc[0])
    random_state = int(pd.Series(random_state).iloc[0])
    if total_n < 1:
        raise ValueError("total_n must be at least 1.")

    df = df.copy()
    df[strata_col] = df[strata_col].replace("", np.nan)
    df = df.dropna(subset=[strata_col])
    if df.empty:
        raise ValueError("No rows with a stratum value.")

    pop = len(df)
    sampled = []
    for _, group in df.groupby(strata_col, dropna=True):
        n = max(1, int(round(total_n * len(group) / pop)))
        n = min(n, len(group))
        sampled.append(group.sample(n=n, random_state=random_state))
    return pd.concat(sampled).reset_index(drop=True)

"stratified_sample(data, strata_col, total_n, random_state=42, headers=True)"


def systematic_sample(data, sample_size, random_state=42, headers=True):
    """Draw a systematic sample of rows.

    Interval k = N // sample_size. Start is random in 0..k-1. Then every
    kth row: start, start+k, start+2k, ... trimmed to sample_size.

    data: ref string, DataFrame, Series, list, or xl() result.
    sample_size: number of rows to return. Must be 1..N.
    random_state: seed for the start position (default 42).
    headers: used only when data is a ref string.
    """
    import random

    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        df = data
    elif isinstance(data, pd.Series):
        df = data.to_frame()
    else:
        df = pd.DataFrame(data)
    df = df.dropna(how="all")
    if df.empty:
        raise ValueError("No data after dropping empty rows.")

    sample_size = int(pd.Series(sample_size).iloc[0])
    random_state = int(pd.Series(random_state).iloc[0])
    n = len(df)
    if sample_size < 1:
        raise ValueError("sample_size must be at least 1.")
    if sample_size > n:
        raise ValueError("sample_size cannot exceed population size.")

    k = n // sample_size
    start = random.Random(random_state).randint(0, k - 1)
    idx = list(range(start, n, k))[:sample_size]
    return df.iloc[idx].reset_index(drop=True)

"systematic_sample(data, sample_size, random_state=42, headers=True)"


def two_stage_cluster_sample(
    data, cluster_col, n_clusters, sample_per_cluster, random_state=42, headers=True
):
    """Two-stage cluster sample.

    Stage 1: randomly select n_clusters from all clusters. Stage 2: within
    each selected cluster, randomly sample sample_per_cluster rows (or the
    whole cluster if it is smaller).

    data: ref string, DataFrame, Series, or xl() result.
    cluster_col: column that identifies cluster membership.
    n_clusters: how many clusters to select in stage 1.
    sample_per_cluster: how many rows to sample per selected cluster.
    random_state: seed for reproducibility (default 42).
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
    df = df.dropna(how="all")
    if df.empty:
        raise ValueError("No data after dropping empty rows.")

    cluster_col = str(pd.Series(cluster_col).iloc[0]).strip()
    if cluster_col not in df.columns:
        lookup = {str(c).strip().lower(): c for c in df.columns}
        key = cluster_col.lower()
        if key not in lookup:
            raise ValueError("cluster_col not found.")
        cluster_col = lookup[key]

    n_clusters = int(pd.Series(n_clusters).iloc[0])
    sample_per_cluster = int(pd.Series(sample_per_cluster).iloc[0])
    random_state = int(pd.Series(random_state).iloc[0])
    if n_clusters < 1:
        raise ValueError("n_clusters must be at least 1.")
    if sample_per_cluster < 1:
        raise ValueError("sample_per_cluster must be at least 1.")

    df = df.copy()
    df[cluster_col] = df[cluster_col].replace("", np.nan)
    df = df.dropna(subset=[cluster_col])
    if df.empty:
        raise ValueError("No rows with a cluster value.")

    all_clusters = df[cluster_col].unique()
    n_all = len(all_clusters)
    if n_clusters > n_all:
        raise ValueError("n_clusters cannot exceed the number of clusters.")

    rng = np.random.default_rng(random_state)
    selected = rng.choice(all_clusters, size=n_clusters, replace=False)
    sampled = []
    for cluster_id in selected:
        cluster_data = df[df[cluster_col] == cluster_id]
        n = min(sample_per_cluster, len(cluster_data))
        sampled.append(cluster_data.sample(n=n, random_state=random_state))
    return pd.concat(sampled).reset_index(drop=True)

"two_stage_cluster_sample(data, cluster_col, n_clusters, sample_per_cluster, random_state=42, headers=True)"


def reservoir_sample(data, k, random_state=42, headers=True):
    """Uniform sample of k rows (Algorithm R). Uses O(k) index memory.

    Fills a reservoir with the first k rows, then each later row i replaces
    a random reservoir slot with probability k / (i + 1). If there are fewer
    than k rows, all of them are returned.

    data: ref string, DataFrame, Series, list, or xl() result.
    k: desired sample size (at least 1).
    random_state: seed for reproducibility (default 42).
    headers: used only when data is a ref string.
    """
    import random

    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        df = data
    elif isinstance(data, pd.Series):
        df = data.to_frame()
    else:
        df = pd.DataFrame(data)
    df = df.dropna(how="all")
    if df.empty:
        raise ValueError("No data after dropping empty rows.")

    k = int(pd.Series(k).iloc[0])
    random_state = int(pd.Series(random_state).iloc[0])
    if k < 1:
        raise ValueError("k must be at least 1.")

    rng = random.Random(random_state)
    pos = []
    for i in range(len(df)):
        if i < k:
            pos.append(i)
        else:
            j = rng.randint(0, i)
            if j < k:
                pos[j] = i
    return df.iloc[pos].reset_index(drop=True)

"reservoir_sample(data, k, random_state=42, headers=True)"

