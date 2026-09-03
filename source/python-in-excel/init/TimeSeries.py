# Python in Excel time series library
#
# Formulas â†’ Initialization â†’ replace the editor contents with this file â†’ Save.
# This file is a complete Initialization: Excel defaults, then time series functions only.
# After Save, call contents() in a PY cell for the public function list.
#
# General (non-series) functions: paste init/PaulPythonLibrary.py instead.
# Sampling functions only: paste init/Sampling.py instead.
# Restore defaults only: paste init/DefaultInitialization.py instead.
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


def contents():
    """List time series functions in this Initialization.

    Result spills as function / description / call. A readable description is
    enough when it already says what the function does. call matches the
    quoted signature after each def.
    """
    return pd.DataFrame(
        [
            ("contents", "List library functions", "contents()"),
            ("expsmooth", "SES forecast with interval", "expsmooth(data, alpha=0.2, h=12, level=0.95, plot=False, headers=False)"),
            ("stl", "STL decomposition table", "stl(data, period, dates=None, robust=False, headers=False)"),
            ("stl_plot", "Four-panel STL chart", "stl_plot(data, period, dates=None, robust=False, weights=False, headers=False)"),
            ("resid_analysis", "Residual diagnostics", "resid_analysis(data, lags=None, plot=False, headers=False)"),
            ("acf_ljungbox", "ACF and Ljung-Box Q", "acf_ljungbox(data, lags=20, alpha=0.05, headers=False)"),
            ("acf_pacf", "ACF and PACF", "acf_pacf(data, lags=20, plot=False, headers=False)"),
            ("adf_test", "Augmented Dickey-Fuller", "adf_test(data, alpha=0.05, regression='c', headers=False)"),
            ("fft_spectrum", "FFT periodogram", "fft_spectrum(data, dt=1, plot=False, headers=False)"),
            ("arima_order", "ARIMA(p, d, q) by AIC", "arima_order(data, p_max=3, d_max=2, q_max=3, headers=False)"),
            ("arima_estimate", "ARIMA via ADF and AIC/BIC", "arima_estimate(data, p_max=3, q_max=3, d_max=2, criterion='aic', alpha=0.05, full=False, headers=False)"),
            ("baseline_forecast", "Naive, seasonal naive, or drift", "baseline_forecast(data, date_col=None, value_col=None, h=12, method='naive', period=1, headers=True)"),
            ("forecast_metrics", "MAE, RMSE, MAPE, MASE", "forecast_metrics(data, actual_col, forecast_col, headers=True)"),
            ("zscore_replace", "Replace |z| outliers by interpolation", "zscore_replace(data, z=3, dates=None, headers=False)"),
            ("date_features", "Calendar parts, cycles, holidays", "date_features(data, cyclical=True, calendar=True, fourier=1, country_holiday='UK', headers=False)"),
            ("lag_features", "Lags, rolling stats, and EMA", "lag_features(data, value_col=None, date_col=None, lags=1, windows=7, stats='mean', ema=0, headers=True)"),
            ("lead_features", "Lead columns", "lead_features(data, leads=1, value_col=None, date_col=None, headers=True)"),
            ("fourier_features", "Sine/cosine Fourier terms", "fourier_features(data, period=365, order=3, headers=False)"),
            ("difference", "Regular or seasonal difference", "difference(data, lag=1, order=1, headers=False)"),
            ("impute", "Fill blanks in a series", "impute(data, method='linear', period=12, headers=False)"),
            ("seasonal_indices", "Seasonal index per slot", "seasonal_indices(data, period=12, kind='multiplicative', headers=False)"),
            ("seasonally_adjust", "Remove seasonal index", "seasonally_adjust(data, period=12, kind='multiplicative', headers=False)"),
            ("kpss_test", "KPSS stationarity test", "kpss_test(data, alpha=0.05, regression='c', headers=False)"),
            ("ets_forecast", "Holt-Winters ETS forecast", "ets_forecast(data, h=12, trend='add', seasonal='add', period=12, level=0.95, plot=False, headers=False)"),
            ("arima_forecast", "ARIMA(p,d,q) forecast", "arima_forecast(data, h=12, p=1, d=1, q=1, headers=False)"),
            ("sarima_forecast", "SARIMA forecast with interval", "sarima_forecast(data, h=12, p=1, d=1, q=1, P=1, D=1, Q=1, s=12, level=0.95, plot=False, headers=False)"),
            ("rolling_cv", "Rolling-origin CV metrics", "rolling_cv(data, h=1, min_train=None, step=1, method='naive', period=12, full=False, headers=False)"),
            ("detect_anomalies", "Flag series anomalies", "detect_anomalies(data, method='stl', period=12, z=3, headers=False)"),
            ("breakpoints", "Break dates, confidence, and type", "breakpoints(data, method='cusum', alpha=0.05, at=None, nbreaks=None, plot=False, headers=True, date_col=None)"),
            ("forecast_plot", "Actual + forecast chart", "forecast_plot(actual, forecast, lower=None, upper=None, headers=False)"),
        ],
        columns=["function", "description", "call"],
    )

"contents()"


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


def acf_ljungbox(data, lags=20, alpha=0.05, headers=False):
    """Autocorrelation (ACF) and Ljung-Box test at lags 1..lags.

    data: value column, residual column, stl() result (uses resid), Series,
        DataFrame, or ref string.
    lags: maximum lag. Default 20, capped at n-2. Need at least 3 values.
    alpha: significance level for acf_sig and lb_sig. Default 0.05.
    headers: first row is headers when data is a ref string.

    Columns: lag, acf, acf_se, acf_sig, lb_stat, lb_pvalue, lb_sig.
    acf_se is 1/sqrt(n) (white-noise Bartlett band). acf_sig is 1 when
    |acf| > 1.96 * acf_se. lb_sig is 1 when Ljung-Box p < alpha.
    """
    from statsmodels.tsa.stattools import acf
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
        raise ValueError("Need at least 3 numeric values.")

    max_lag = max(1, n - 2)
    lag = min(max_lag, int(pd.Series(lags).iloc[0]))
    lag = max(1, lag)
    alpha = float(pd.Series(alpha).iloc[0])

    acf_vals = acf(y, nlags=lag, fft=False)
    se = 1.0 / np.sqrt(n)
    zcrit = 1.96
    try:
        lb = acorr_ljungbox(y, lags=lag, return_df=True)
        lb_stat = lb["lb_stat"].to_numpy(dtype=float)
        lb_p = lb["lb_pvalue"].to_numpy(dtype=float)
    except (ValueError, np.linalg.LinAlgError):
        lb_stat = np.full(lag, np.nan)
        lb_p = np.full(lag, np.nan)

    rows = []
    for k in range(1, lag + 1):
        a = float(acf_vals[k])
        stat = float(lb_stat[k - 1]) if k - 1 < len(lb_stat) else np.nan
        pval = float(lb_p[k - 1]) if k - 1 < len(lb_p) else np.nan
        rows.append((
            k,
            a,
            se,
            1.0 if abs(a) > zcrit * se else 0.0,
            stat,
            pval,
            1.0 if np.isfinite(pval) and pval < alpha else 0.0,
        ))
    return pd.DataFrame(rows, columns=["lag", "acf", "acf_se", "acf_sig",
                                       "lb_stat", "lb_pvalue", "lb_sig"])

"acf_ljungbox(data, lags=20, alpha=0.05, headers=False)"


def acf_pacf(data, lags=20, plot=False, headers=False):
    """Sample ACF and PACF at lags 1..lags. plot=False spills a table; True is a chart.

    data: value column, residual column, stl() result (uses resid), Series,
        DataFrame, or ref string.
    lags: maximum lag. Default 20, capped at min(n-2, n//2 - 1) for PACF.
    plot: False (default) returns a table. True returns a two-panel matplotlib
        Figure (ACF above, PACF below). Keep that PY cell as a Python object.
    headers: first row is headers when data is a ref string.

    Table columns: lag, acf, pacf, se, acf_sig, pacf_sig.
    se is 1/sqrt(n). acf_sig / pacf_sig are 1 when |value| > 1.96 * se.
    """
    from statsmodels.tsa.stattools import acf, pacf
    from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

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
    if n < 4:
        raise ValueError("Need at least 4 numeric values.")

    max_lag = max(1, min(n - 2, n // 2 - 1))
    lag = min(max_lag, int(pd.Series(lags).iloc[0]))
    lag = max(1, lag)

    if plot:
        fig, axes = plt.subplots(2, 1, figsize=(8, 6))
        plot_acf(y, ax=axes[0], lags=lag)
        plot_pacf(y, ax=axes[1], lags=lag, method="ywm")
        axes[0].set_title("ACF")
        axes[1].set_title("PACF")
        fig.tight_layout()
        return fig

    acf_vals = acf(y, nlags=lag, fft=False)
    pacf_vals = pacf(y, nlags=lag, method="ywm")
    se = 1.0 / np.sqrt(n)
    zcrit = 1.96
    rows = []
    for k in range(1, lag + 1):
        a = float(acf_vals[k])
        p = float(pacf_vals[k])
        rows.append((
            k,
            a,
            p,
            se,
            1.0 if abs(a) > zcrit * se else 0.0,
            1.0 if abs(p) > zcrit * se else 0.0,
        ))
    return pd.DataFrame(rows, columns=["lag", "acf", "pacf", "se", "acf_sig", "pacf_sig"])

"acf_pacf(data, lags=20, plot=False, headers=False)"


def adf_test(data, alpha=0.05, regression="c", headers=False):
    """Augmented Dickey-Fuller unit-root test. Spills metric, value, guidance.

    H0: the series has a unit root (non-stationary). Reject H0 when
    p-value < alpha (or adf_stat is more negative than the 5% critical value).

    data: value column, ref string, Series, or DataFrame (first numeric col).
    alpha: significance level. Default 0.05.
    regression: 'c' constant (default), 'ct' constant+trend, 'n' none,
        'ctt' constant+trend+quadratic.
    headers: first row is headers when data is a ref string.

    Need at least 4 numeric values. Lag length is chosen by AIC (autolag).
    """
    from statsmodels.tsa.stattools import adfuller

    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        numeric = data.select_dtypes(include="number")
        values = numeric.iloc[:, 0] if numeric.shape[1] else data.iloc[:, 0]
    else:
        values = data
    y = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce").dropna()
    n = int(y.shape[0])
    if n < 4:
        raise ValueError("Need at least 4 observations.")

    alpha = float(pd.Series(alpha).iloc[0])
    reg = str(pd.Series(regression).iloc[0]).strip().lower() if not isinstance(
        regression, str) else regression.strip().lower()
    if reg not in ("c", "ct", "n", "ctt"):
        raise ValueError("regression must be 'c', 'ct', 'n', or 'ctt'.")

    stat, pval, usedlag, nobs, crit, _ = adfuller(y, regression=reg, autolag="AIC")
    stat, pval = float(stat), float(pval)
    usedlag, nobs = int(usedlag), int(nobs)
    c1, c5, c10 = float(crit["1%"]), float(crit["5%"]), float(crit["10%"])
    is_stat = 1.0 if pval < alpha else 0.0
    if pval < alpha:
        note = "p < alpha: reject unit root. Treat the series as stationary."
    else:
        note = "p >= alpha: fail to reject unit root. Treat as non-stationary."

    return pd.DataFrame(
        [
            ("n", n, "Count of numeric values after dropping blanks."),
            ("adf_stat", stat, "More negative than a critical value supports stationarity."),
            ("pvalue", pval, "p < alpha rejects H0 (unit root). Series is then stationary."),
            ("usedlag", usedlag, "ADF lag length chosen by AIC."),
            ("nobs", nobs, "Observations used in the regression after lags."),
            ("crit_1", c1, "1% critical value. adf_stat below this is strong evidence."),
            ("crit_5", c5, "5% critical value. Usual cutoff with alpha=0.05."),
            ("crit_10", c10, "10% critical value. Weaker evidence of stationarity."),
            ("alpha", alpha, "Significance level used for the stationary flag."),
            ("regression", reg, "c=constant, ct=constant+trend, n=none, ctt=quadratic."),
            ("stationary", is_stat, "1 if pvalue < alpha, else 0."),
            ("interpretation", note, note),
        ],
        columns=["metric", "value", "guidance"],
    )

"adf_test(data, alpha=0.05, regression='c', headers=False)"


def fft_spectrum(data, dt=1, plot=False, headers=False):
    """Real FFT periodogram. plot=False spills a table; True is a chart.

    data: value column, ref string, Series, or DataFrame (first numeric col).
    dt: time between observations. Default 1 (period is in observations).
    plot: False (default) returns a table. True returns power vs frequency
        and power vs period. Keep that PY cell as a Python object.
    headers: first row is headers when data is a ref string.

    The series is demeaned. DC (k=0) is omitted. Need at least 4 values.

    Table columns: cycles, frequency, period, power, peak.
    cycles is the DFT bin (cycles in the sample). frequency is cycles per
    time unit (1/dt). period is 1/frequency. power is |FFT|^2 / n.
    peak is 1 on the strongest non-DC bin.
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

    y = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce").dropna().to_numpy(dtype=float)
    n = int(y.size)
    if n < 4:
        raise ValueError("Need at least 4 numeric values.")
    dt = float(pd.Series(dt).iloc[0])
    if dt <= 0:
        raise ValueError("dt must be positive.")

    spec = np.fft.rfft(y - y.mean())
    freq = np.fft.rfftfreq(n, d=dt)
    power = (np.abs(spec) ** 2) / n
    k = np.arange(spec.size, dtype=float)
    period = np.where(freq > 0, 1.0 / freq, np.nan)

    keep = freq > 0
    k, freq, period, power = k[keep], freq[keep], period[keep], power[keep]
    peak = np.zeros(power.size, dtype=float)
    if power.size:
        peak[int(np.argmax(power))] = 1.0

    if plot:
        fig, axes = plt.subplots(2, 1, figsize=(8, 6))
        axes[0].stem(freq, power, basefmt=" ")
        axes[0].set_title("Power spectrum")
        axes[0].set_xlabel("Frequency (cycles per time unit)")
        axes[0].set_ylabel("Power")
        axes[1].stem(period, power, basefmt=" ")
        axes[1].set_title("Power vs period")
        axes[1].set_xlabel("Period (time units per cycle)")
        axes[1].set_ylabel("Power")
        fig.tight_layout()
        return fig

    return pd.DataFrame({
        "cycles": k,
        "frequency": freq,
        "period": period,
        "power": power,
        "peak": peak,
    })

"fft_spectrum(data, dt=1, plot=False, headers=False)"


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


def lag_features(data, value_col=None, date_col=None, lags=1, windows=7,
                 stats="mean", ema=0, headers=True):
    """Lag columns, rolling-window statistics, and EMA for a time series.

    Lags are y.shift(k). Rolling stats and EMA use only past values, so the
    current row is not in the window. EMA is recursive with alpha = 2/(span+1).

    data: table/range, DataFrame, Series, or ref string.
    value_col: header of the value column. First numeric if omitted.
    date_col: header of the date column. Auto-detected if omitted.
    lags: int n gives lag_1 .. lag_n; a list or '1,7,12' gives those lags.
        0 or None skips lags.
    windows: int or list of window sizes. 0 or None skips rolling stats.
    stats: mean, std, min, max, median, sum. Comma-separated or list.
    ema: EMA span, or a list / '12,26'. 0 or None skips EMA.
    headers: first row is headers when data is a ref string. Default True.

    Sorted by date when a date column is present. Early rows are blank
    until each lag, window, or EMA span is filled.
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
                if name is None and pd.api.types.is_numeric_dtype(s):
                    continue
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

    def to_ints(value, expand=False):
        if value is None or value is False:
            return []
        if isinstance(value, str):
            raw = [p.strip() for p in value.replace(";", ",").split(",") if p.strip()]
        else:
            raw = list(pd.Series(np.ravel(
                value.to_numpy() if isinstance(value, pd.DataFrame) else value
            )).dropna())
        nums = []
        for x in raw:
            try:
                n = int(float(x))
            except (TypeError, ValueError):
                continue
            if n > 0:
                nums.append(n)
        if expand and len(nums) == 1:
            nums = list(range(1, nums[0] + 1))
        out = []
        seen = set()
        for n in nums:
            if n not in seen:
                seen.add(n)
                out.append(n)
        return out

    def to_stats(value):
        allowed = ("mean", "std", "min", "max", "median", "sum")
        if value is None or value is False:
            return ["mean"]
        if isinstance(value, str):
            raw = [p.strip().lower() for p in value.replace(";", ",").split(",") if p.strip()]
        else:
            raw = [str(x).strip().lower() for x in pd.Series(np.ravel(
                value.to_numpy() if isinstance(value, pd.DataFrame) else value
            )).dropna()]
        out = []
        seen = set()
        for s in raw:
            if s in allowed and s not in seen:
                seen.add(s)
                out.append(s)
        if not out:
            raise ValueError("stats must be mean, std, min, max, median, or sum.")
        return out

    frame = to_frame(data)
    y = pd.to_numeric(pick_col(frame, value_col, "value"), errors="coerce")
    val_name = y.name
    if not isinstance(val_name, str) or not val_name.strip() or val_name.lower() in ("none", "nan", "date"):
        val_name = "value"
    dates = pick_col(frame, date_col, "date") if (
        date_col is not None or frame.shape[1] > 1) else None
    y = pd.Series(y).reset_index(drop=True)
    n = int(y.size)
    if n < 1:
        raise ValueError("Need at least 1 value row.")
    lag_list = to_ints(lags, expand=True)
    win_list = to_ints(windows, expand=False)
    ema_list = to_ints(ema, expand=False)
    if not lag_list and not win_list and not ema_list:
        raise ValueError("Provide at least one lag, window, or ema span.")
    out = pd.DataFrame({val_name: y})
    if dates is not None:
        dates = pd.Series(dates).reset_index(drop=True)
        out.insert(0, "date", dates)
        out = out.sort_values("date", kind="mergesort", na_position="last").reset_index(drop=True)
        y = out[val_name]
    for k in lag_list:
        out["lag_%d" % k] = y.shift(k)
    if win_list:
        past = y.shift(1)
        for w in win_list:
            rolled = past.rolling(w)
            for s in to_stats(stats):
                out["roll_%s_%d" % (s, w)] = getattr(rolled, s)()
    for s in ema_list:
        out["ema_%d" % s] = y.ewm(span=s, adjust=False, min_periods=s).mean().shift(1)
    return out

"lag_features(data, value_col=None, date_col=None, lags=1, windows=7, stats='mean', ema=0, headers=True)"

def lead_features(data, leads=1, value_col=None, date_col=None, headers=True):
    """Lead columns for a time series. Leads are y.shift(-k).

    data: table/range, DataFrame, Series, or ref string.
    leads: int n gives lead_1 .. lead_n; a list or '1,7,12' gives those leads.
    value_col: header of the value column. First numeric if omitted.
    date_col: header of the date column. Auto-detected if omitted.
    headers: first row is headers when data is a ref string. Default True.

    Sorted by date when a date column is present. Trailing rows are blank.
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
                    continue
                parsed = pd.to_datetime(s, errors="coerce")
                if parsed.notna().mean() > 0.8:
                    return parsed
            return None
        numeric = frame.select_dtypes(include="number")
        if numeric.shape[1]:
            return numeric.iloc[:, 0]
        return pd.to_numeric(frame.iloc[:, 0], errors="coerce")

    def to_ints(value):
        if value is None or value is False:
            return []
        if isinstance(value, str):
            raw = [p.strip() for p in value.replace(";", ",").split(",") if p.strip()]
        else:
            raw = list(pd.Series(np.ravel(
                value.to_numpy() if isinstance(value, pd.DataFrame) else value
            )).dropna())
        nums = []
        for x in raw:
            try:
                n = int(float(x))
            except (TypeError, ValueError):
                continue
            if n > 0:
                nums.append(n)
        if len(nums) == 1:
            nums = list(range(1, nums[0] + 1))
        out, seen = [], set()
        for n in nums:
            if n not in seen:
                seen.add(n)
                out.append(n)
        return out

    frame = to_frame(data)
    y = pd.to_numeric(pick_col(frame, value_col, "value"), errors="coerce")
    val_name = y.name
    if not isinstance(val_name, str) or not val_name.strip() or val_name.lower() in (
            "none", "nan", "date"):
        val_name = "value"
    dates = pick_col(frame, date_col, "date") if (
        date_col is not None or frame.shape[1] > 1) else None
    y = pd.Series(y).reset_index(drop=True)
    if int(y.size) < 1:
        raise ValueError("Need at least 1 value row.")
    lead_list = to_ints(leads)
    if not lead_list:
        raise ValueError("Provide at least one lead.")
    out = pd.DataFrame({val_name: y})
    if dates is not None:
        dates = pd.Series(dates).reset_index(drop=True)
        out.insert(0, "date", dates)
        out = out.sort_values("date", kind="mergesort", na_position="last").reset_index(drop=True)
        y = out[val_name]
    for k in lead_list:
        out["lead_%d" % k] = y.shift(-k)
    return out

"lead_features(data, leads=1, value_col=None, date_col=None, headers=True)"

def fourier_features(data, period=365, order=3, headers=False):
    """Sine and cosine Fourier terms for seasonal regression.

    For harmonic k = 1..order, angle = 2 * pi * k * t / period with t = 0
    at the first row. Spills the original value plus sin_k / cos_k columns.

    data: value column, ref string, Series, or DataFrame (first numeric col).
    period: seasonal length in rows. Default 365.
    order: number of harmonics. Default 3.
    headers: first row is headers when data is a ref string.
    """
    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        numeric = data.select_dtypes(include="number")
        values = numeric.iloc[:, 0] if numeric.shape[1] else data.iloc[:, 0]
    else:
        values = data
    y = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce").reset_index(drop=True)
    n = int(y.size)
    if n < 1:
        raise ValueError("Need at least 1 value row.")
    period = float(pd.Series(period).iloc[0])
    order = int(pd.Series(order).iloc[0])
    if period <= 0:
        raise ValueError("period must be positive.")
    if order < 1:
        raise ValueError("order must be at least 1.")
    t = np.arange(n, dtype="float64")
    out = pd.DataFrame({"t": t, "value": y})
    for k in range(1, order + 1):
        angle = 2.0 * np.pi * k * t / period
        out["sin_%d" % k] = np.sin(angle)
        out["cos_%d" % k] = np.cos(angle)
    return out

"fourier_features(data, period=365, order=3, headers=False)"


def difference(data, lag=1, order=1, headers=False):
    """Difference a series. lag=1 is regular; lag=period is seasonal.

    Applied `order` times. Leading rows that cannot be differenced are blank.

    data: value column, ref string, Series, or DataFrame (first numeric col).
    lag: difference step. Default 1.
    order: how many times to difference. Default 1.
    headers: first row is headers when data is a ref string.
    """
    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        numeric = data.select_dtypes(include="number")
        values = numeric.iloc[:, 0] if numeric.shape[1] else data.iloc[:, 0]
    else:
        values = data
    y = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce").reset_index(drop=True)
    lag = int(pd.Series(lag).iloc[0])
    order = int(pd.Series(order).iloc[0])
    if lag < 1 or order < 1:
        raise ValueError("lag and order must be at least 1.")
    d = y.copy()
    for _ in range(order):
        d = d.diff(lag)
    return pd.DataFrame({"value": y, "diff": d})

"difference(data, lag=1, order=1, headers=False)"


def impute(data, method="linear", period=12, headers=False):
    """Fill missing values in a series. Spills value, imputed, was_missing.

    data: value column, ref string, Series, or DataFrame (first numeric col).
    method: 'linear' (default), 'ffill', 'bfill', 'mean', 'median', or
        'seasonal' (season means; needs period).
    period: season length for method='seasonal'. Default 12.
    headers: first row is headers when data is a ref string.
    """
    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        numeric = data.select_dtypes(include="number")
        values = numeric.iloc[:, 0] if numeric.shape[1] else data.iloc[:, 0]
    else:
        values = data
    y = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce").reset_index(drop=True)
    m = str(pd.Series(method).iloc[0]).strip().lower() if not isinstance(
        method, str) else method.strip().lower()
    missing = y.isna()
    filled = y.copy()
    if m == "linear":
        filled = y.interpolate(method="linear", limit_direction="both")
    elif m == "ffill":
        filled = y.ffill().bfill()
    elif m == "bfill":
        filled = y.bfill().ffill()
    elif m == "mean":
        filled = y.fillna(float(y.mean(skipna=True)))
    elif m == "median":
        filled = y.fillna(float(y.median(skipna=True)))
    elif m == "seasonal":
        p = int(pd.Series(period).iloc[0])
        if p < 2:
            raise ValueError("period must be at least 2 for seasonal impute.")
        idx = np.arange(int(y.size)) % p
        means = y.groupby(idx).transform("mean")
        filled = y.fillna(means).fillna(float(y.mean(skipna=True)))
    else:
        raise ValueError("method must be linear, ffill, bfill, mean, median, or seasonal.")
    return pd.DataFrame({
        "value": y,
        "imputed": filled,
        "was_missing": missing.astype("float64"),
    })

"impute(data, method='linear', period=12, headers=False)"


def seasonal_indices(data, period=12, kind="multiplicative", headers=False):
    """One seasonal index per slot 1..period from the series in row order.

    Multiplicative: slot mean / grand mean (indices average to 1).
    Additive: slot mean - grand mean (indices average to 0).

    data: value column, ref string, Series, or DataFrame (first numeric col).
    period: season length. Default 12.
    kind: 'multiplicative' (default) or 'additive'.
    headers: first row is headers when data is a ref string.
    """
    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        numeric = data.select_dtypes(include="number")
        values = numeric.iloc[:, 0] if numeric.shape[1] else data.iloc[:, 0]
    else:
        values = data
    y = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce").reset_index(drop=True)
    p = int(pd.Series(period).iloc[0])
    k = str(pd.Series(kind).iloc[0]).strip().lower() if not isinstance(
        kind, str) else kind.strip().lower()
    if k in ("mult", "mul"):
        k = "multiplicative"
    if k in ("add",):
        k = "additive"
    if p < 2:
        raise ValueError("period must be at least 2.")
    if int(y.notna().sum()) < p:
        raise ValueError("Need at least one full season of numeric values.")
    if k not in ("multiplicative", "additive"):
        raise ValueError("kind must be 'multiplicative' or 'additive'.")
    slot = (np.arange(int(y.size)) % p) + 1
    g = y.groupby(slot)
    means = g.mean()
    grand = float(y.mean(skipna=True))
    if k == "multiplicative":
        if grand == 0 or not np.isfinite(grand):
            raise ValueError("Grand mean is 0; use kind='additive'.")
        idx = means / grand
    else:
        idx = means - grand
    return pd.DataFrame({
        "season": np.arange(1, p + 1),
        "index": idx.reindex(np.arange(1, p + 1)).to_numpy(dtype="float64"),
        "kind": k,
    })

"seasonal_indices(data, period=12, kind='multiplicative', headers=False)"


def seasonally_adjust(data, period=12, kind="multiplicative", headers=False):
    """Seasonally adjust a series using seasonal_indices of the same kind.

    Multiplicative: value / index. Additive: value - index.

    data: value column, ref string, Series, or DataFrame (first numeric col).
    period: season length. Default 12.
    kind: 'multiplicative' (default) or 'additive'.
    headers: first row is headers when data is a ref string.
    """
    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        numeric = data.select_dtypes(include="number")
        values = numeric.iloc[:, 0] if numeric.shape[1] else data.iloc[:, 0]
    else:
        values = data
    y = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce").reset_index(drop=True)
    p = int(pd.Series(period).iloc[0])
    k = str(pd.Series(kind).iloc[0]).strip().lower() if not isinstance(
        kind, str) else kind.strip().lower()
    if k in ("mult", "mul"):
        k = "multiplicative"
    if k in ("add",):
        k = "additive"
    if p < 2:
        raise ValueError("period must be at least 2.")
    if k not in ("multiplicative", "additive"):
        raise ValueError("kind must be 'multiplicative' or 'additive'.")
    slot = np.arange(int(y.size)) % p
    means = y.groupby(slot + 1).mean()
    grand = float(y.mean(skipna=True))
    if k == "multiplicative":
        if grand == 0 or not np.isfinite(grand):
            raise ValueError("Grand mean is 0; use kind='additive'.")
        idx_vals = (means / grand).reindex(np.arange(1, p + 1)).to_numpy(dtype="float64")
        factor = idx_vals[slot]
        adj = y.to_numpy(dtype="float64") / factor
    else:
        idx_vals = (means - grand).reindex(np.arange(1, p + 1)).to_numpy(dtype="float64")
        factor = idx_vals[slot]
        adj = y.to_numpy(dtype="float64") - factor
    return pd.DataFrame({
        "value": y,
        "season": slot + 1,
        "index": factor,
        "adjusted": adj,
    })

"seasonally_adjust(data, period=12, kind='multiplicative', headers=False)"


def kpss_test(data, alpha=0.05, regression="c", headers=False):
    """KPSS unit-root / stationarity test. Spills metric, value, guidance.

    H0: the series is stationary (around a level or a trend). Reject H0
    when p-value < alpha (treat as non-stationary). Opposite of ADF.

    data: value column, ref string, Series, or DataFrame (first numeric col).
    alpha: significance level. Default 0.05.
    regression: 'c' level-stationary (default) or 'ct' trend-stationary.
    headers: first row is headers when data is a ref string.
    """
    import warnings
    from statsmodels.tsa.stattools import kpss

    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        numeric = data.select_dtypes(include="number")
        values = numeric.iloc[:, 0] if numeric.shape[1] else data.iloc[:, 0]
    else:
        values = data
    y = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce").dropna()
    n = int(y.shape[0])
    if n < 8:
        raise ValueError("Need at least 8 observations.")
    alpha = float(pd.Series(alpha).iloc[0])
    reg = str(pd.Series(regression).iloc[0]).strip().lower() if not isinstance(
        regression, str) else regression.strip().lower()
    if reg not in ("c", "ct"):
        raise ValueError("regression must be 'c' or 'ct'.")
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        stat, pval, lags, crit = kpss(y, regression=reg, nlags="auto")
    stat, pval = float(stat), float(pval)
    lags = int(lags)
    c1 = float(crit.get("1%", np.nan))
    c5 = float(crit.get("5%", np.nan))
    c10 = float(crit.get("10%", np.nan))
    is_stat = 1.0 if pval >= alpha else 0.0
    if pval < alpha:
        note = "p < alpha: reject stationarity. Treat the series as non-stationary."
    else:
        note = "p >= alpha: fail to reject stationarity. Treat as stationary."
    return pd.DataFrame(
        [
            ("n", n, "Count of numeric values after dropping blanks."),
            ("kpss_stat", stat, "Larger than a critical value supports non-stationarity."),
            ("pvalue", pval, "p < alpha rejects H0 (stationary). Series is then non-stationary."),
            ("lags", lags, "Truncation lag used in the test."),
            ("crit_1", c1, "1% critical value."),
            ("crit_5", c5, "5% critical value. Usual cutoff with alpha=0.05."),
            ("crit_10", c10, "10% critical value."),
            ("alpha", alpha, "Significance level used for the stationary flag."),
            ("regression", reg, "c=level stationary, ct=trend stationary."),
            ("stationary", is_stat, "1 if pvalue >= alpha, else 0."),
            ("interpretation", note, note),
        ],
        columns=["metric", "value", "guidance"],
    )

"kpss_test(data, alpha=0.05, regression='c', headers=False)"


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


def arima_forecast(data, h=12, p=1, d=1, q=1, headers=False):
    """ARIMA(p,d,q) forecast. Spills actuals then forecast rows.

    data: value column, ref string, Series, or DataFrame (first numeric col).
    h: forecast horizon. Default 12.
    p, d, q: ARIMA orders. Default 1, 1, 1.
    headers: first row is headers when data is a ref string.

    Result columns: t, value, label ('Actual' or 'Forecast ARIMA').
    Pair with arima_estimate to choose p, d, q.
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
    if h < 1:
        raise ValueError("h must be at least 1.")
    n = int(y.size)
    if n < 4:
        raise ValueError("Need at least 4 observations.")
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        fit = ARIMA(y, order=(p, d, q)).fit()
        fc = np.asarray(fit.forecast(h), dtype="float64")
    actual = pd.DataFrame({
        "t": np.arange(1, n + 1, dtype="float64"),
        "value": y.to_numpy(dtype="float64"),
        "label": "Actual",
    })
    future = pd.DataFrame({
        "t": np.arange(n + 1, n + h + 1, dtype="float64"),
        "value": fc,
        "label": "Forecast ARIMA",
    })
    return pd.concat([actual, future], ignore_index=True)

"arima_forecast(data, h=12, p=1, d=1, q=1, headers=False)"


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


def detect_anomalies(data, method="stl", period=12, z=3, headers=False):
    """Flag unusual points in an ordered series.

    stl: |STL residual z-score| > z (season-aware). iqr / zscore: same
    fences as outlier_flag on the raw values.

    data: value column, ref string, Series, or DataFrame (first numeric col).
    method: 'stl' (default), 'iqr', or 'zscore'.
    period: STL seasonal length. Default 12.
    z: cutoff. STL/zscore: |z| > z (default 3). IQR: fence multiplier
        (default 3 here; pass 1.5 for Tukey).
    headers: first row is headers when data is a ref string.

    Result: t, value, residual, score, is_anomaly (1/0).
    """
    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        numeric = data.select_dtypes(include="number")
        values = numeric.iloc[:, 0] if numeric.shape[1] else data.iloc[:, 0]
    else:
        values = data
    y = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce").reset_index(drop=True)
    n = int(y.size)
    if n < 4:
        raise ValueError("Need at least 4 observations.")
    m = str(pd.Series(method).iloc[0]).strip().lower() if not isinstance(
        method, str) else method.strip().lower()
    tcut = abs(float(pd.Series(z).iloc[0]))
    period = int(pd.Series(period).iloc[0])
    resid = pd.Series(np.nan, index=y.index, dtype="float64")
    score = pd.Series(np.nan, index=y.index, dtype="float64")
    flag = pd.Series(False, index=y.index)

    if m == "stl":
        from statsmodels.tsa.seasonal import STL
        if period < 2:
            raise ValueError("period must be at least 2 for STL.")
        ok = y.notna()
        if int(ok.sum()) < period * 2:
            raise ValueError("Need at least 2 full seasons for STL.")
        fit = STL(y[ok].to_numpy(dtype="float64"), period=period, robust=True).fit()
        r = pd.Series(fit.resid, index=y.index[ok])
        resid.loc[ok] = r
        mu = float(r.mean())
        sd = float(r.std(ddof=0))
        if sd == 0 or not np.isfinite(sd):
            sc = pd.Series(0.0, index=r.index)
        else:
            sc = (r - mu) / sd
        score.loc[ok] = sc
        flag.loc[ok] = sc.abs() > tcut
    elif m == "iqr":
        q1 = float(y.quantile(0.25))
        q3 = float(y.quantile(0.75))
        iqr = q3 - q1
        lo, hi = q1 - tcut * iqr, q3 + tcut * iqr
        resid = y - float(y.median(skipna=True))
        score = y.copy()
        if iqr != 0:
            flag = (y < lo) | (y > hi)
        flag = flag.fillna(False)
    elif m == "zscore":
        mu = float(y.mean(skipna=True))
        sd = float(y.std(ddof=0, skipna=True))
        resid = y - mu
        if sd == 0 or not np.isfinite(sd):
            score = pd.Series(0.0, index=y.index)
        else:
            score = (y - mu) / sd
            flag = score.abs() > tcut
        flag = flag.fillna(False)
    else:
        raise ValueError("method must be 'stl', 'iqr', or 'zscore'.")

    out = pd.DataFrame({
        "t": np.arange(1, n + 1, dtype="float64"),
        "value": y,
        "residual": resid,
        "score": score,
        "is_anomaly": flag.astype("float64"),
    })
    blank = y.isna().to_numpy()
    if blank.any():
        out.loc[blank, ["residual", "score", "is_anomaly"]] = np.nan
    return out

"detect_anomalies(data, method='stl', period=12, z=3, headers=False)"


def breakpoints(data, method="cusum", alpha=0.05, at=None, nbreaks=None,
                plot=False, headers=True, date_col=None):
    """break_date, confidence (1-p), type (Level shift / Trend shift).

    Monthly YYYY-MM; else YYYY-MM-DD or 1-based t. plot=True is a chart.
    """
    from scipy.stats import f as fdist
    from statsmodels.stats.diagnostic import breaks_cusumolsresid
    from statsmodels.regression.linear_model import OLS

    dates = None
    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        if date_col is not None:
            key = str(pd.Series(date_col).iloc[0]).strip().lower()
            cmap = {str(c).strip().lower(): c for c in data.columns}
            dates = pd.to_datetime(data[cmap.get(key, date_col)], errors="coerce")
        else:
            for col in data.columns:
                s = data[col]
                if pd.api.types.is_numeric_dtype(s):
                    continue
                p = pd.to_datetime(s, errors="coerce")
                if pd.api.types.is_datetime64_any_dtype(s) or float(p.notna().mean()) > 0.8:
                    dates = p
                    break
        num = data.select_dtypes(include="number")
        values = num.iloc[:, 0] if num.shape[1] else data.iloc[:, 0]
    else:
        values = data
    y = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce").reset_index(drop=True)
    if dates is not None:
        dates = pd.to_datetime(pd.Series(dates).reset_index(drop=True), errors="coerce")
        ok = y.notna()
        dates, y = dates[ok].reset_index(drop=True), y[ok].reset_index(drop=True)
    else:
        y = y.dropna().reset_index(drop=True)
    y = y.to_numpy(dtype="float64")
    n = int(y.size)
    if n < 10:
        raise ValueError("Need 10+ observations.")
    alpha = float(pd.Series(alpha).iloc[0])
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1.")
    m = str(pd.Series(method).iloc[0]).strip().lower().replace("_", "-")
    if m in ("qlr", "supf", "sup-f"):
        m = "chow"
    if m in ("bp", "bai-perron", "bai perron"):
        m = "baiperron"
    if m not in ("cusum", "chow", "baiperron"):
        raise ValueError("method must be cusum, chow, or baiperron.")
    t = np.arange(1, n + 1, dtype="float64")
    X = np.column_stack([np.ones(n), t])
    monthly = dates is not None and int(dates.notna().sum()) >= 2 and (
        int(dates.dt.to_period("M").nunique()) >= n)

    def ssr(a, b):
        ya, Xa = y[a:b], X[a:b]
        if ya.size < 3:
            return np.nan
        bh = np.linalg.lstsq(Xa, ya, rcond=None)[0]
        e = ya - Xa.dot(bh)
        return float(e.dot(e))

    def chow_f(k):
        sp, s1, s2 = ssr(0, n), ssr(0, k), ssr(k, n)
        dfd = n - 4
        if dfd < 1 or not np.isfinite(s1 + s2) or s1 + s2 <= 0:
            return np.nan, np.nan
        fv = ((sp - s1 - s2) / 2.0) / ((s1 + s2) / dfd)
        return float(fv), float(fdist.sf(fv, 2, dfd))

    def rss_x(Xa):
        if y.size < Xa.shape[1] + 1:
            return np.nan
        bh = np.linalg.lstsq(Xa, y, rcond=None)[0]
        e = y - Xa.dot(bh)
        return float(e.dot(e))

    def kind(k):
        I = (t > k).astype("float64")
        sr, sl = rss_x(X), rss_x(np.c_[X, I])
        st = rss_x(np.c_[X, t * I])
        fl = (sr - sl) * (n - 3) / sl if sl > 0 else np.nan
        ft = (sr - st) * (n - 3) / st if st > 0 else np.nan
        return "Trend shift" if np.isfinite(ft) and (
            not np.isfinite(fl) or ft > fl) else "Level shift"

    def conf(p):
        return "" if not np.isfinite(p) else "%d%%" % int(
            round(100.0 * (1.0 - min(max(float(p), 0.0), 1.0))))

    def label(i):
        if dates is None or not (1 <= i <= n) or pd.isna(dates.iloc[i - 1]):
            return i
        ts = pd.Timestamp(dates.iloc[i - 1])
        return ts.strftime("%Y-%m" if monthly else "%Y-%m-%d")

    breaks, pmap, path, bound = [], {}, None, np.nan
    if m == "cusum":
        resid = np.asarray(OLS(y, X).fit().resid, dtype="float64")
        _st, pval, crit = breaks_cusumolsresid(resid, ddof=2)
        pval = float(pval)
        path = np.cumsum(resid) / np.sqrt(float(resid.dot(resid)))
        bound = float(np.asarray(crit).reshape(-1)[1]) if np.size(crit) > 1 else 1.36
        if pval < alpha:
            k = min(max(int(np.argmax(np.abs(path)) + 1), 3), n - 3)
            breaks, pmap = [k], {k: pval}
    elif m == "chow":
        lo, hi = max(int(0.15 * n), 3), min(int(np.ceil(0.85 * n)), n - 3)
        if at is None or at is False:
            best, bk = -np.inf, lo
            for k in range(lo, hi + 1):
                fv, _pv = chow_f(k)
                if np.isfinite(fv) and fv > best:
                    best, bk = fv, k
        else:
            av = float(pd.Series(at).iloc[0])
            bk = int(round(av * n)) if 0 < av < 1 else int(av)
            bk = max(bk, 1)
        _fv, pval = chow_f(bk)
        if np.isfinite(pval) and pval < alpha:
            breaks, pmap = [bk], {bk: pval}
    else:
        max_m = 5 if nbreaks is None or nbreaks is False else max(
            1, int(pd.Series(nbreaks).iloc[0]))
        hlen = max(3, int(0.1 * n))
        max_m = min(max_m, max(0, n // (2 * hlen) - 1))
        if max_m < 1:
            raise ValueError("Too short for Bai-Perron.")
        cs = np.concatenate([[0.0], np.cumsum(y)])
        cs2 = np.concatenate([[0.0], np.cumsum(y * y)])

        def rss(i, j):
            k = j - i
            if k < 1:
                return 0.0
            s = cs[j] - cs[i]
            return float(cs2[j] - cs2[i] - s * s / k)

        inf = 1e300
        F = np.full((max_m + 1, n + 1), inf)
        brk = np.full((max_m + 1, n + 1), -1, dtype=int)
        for j in range(hlen, n + 1):
            F[0, j] = rss(0, j)
        for mm in range(1, max_m + 1):
            for j in range((mm + 1) * hlen, n + 1):
                best, arg = inf, -1
                for i in range(mm * hlen, j - hlen + 1):
                    c = F[mm - 1, i] + rss(i, j)
                    if c < best:
                        best, arg = c, i
                F[mm, j], brk[mm, j] = best, arg
        bic = [inf if F[mm, n] <= 0 else n * np.log(F[mm, n] / n) + (mm + 1) * np.log(n)
               for mm in range(max_m + 1)]
        mhat = int(np.argmin(bic)) if nbreaks is None or nbreaks is False else max_m
        cur_m, cur_t = mhat, n
        while cur_m > 0:
            i = int(brk[cur_m, cur_t])
            if i < 1:
                break
            breaks.append(i)
            cur_t, cur_m = i, cur_m - 1
        breaks = sorted(set(int(b) for b in breaks if 1 <= b < n))
        pmap = {b: chow_f(b)[1] for b in breaks}

    if plot:
        if m == "cusum" and path is not None:
            fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
            axes[0].plot(t, y)
            axes[0].set_title("Series")
            axes[1].plot(t, path, color="C1")
            axes[1].axhline(bound, color="0.4", ls="--")
            axes[1].axhline(-bound, color="0.4", ls="--")
            axes[1].set_title("CUSUM")
            ax0 = axes[0]
        else:
            fig, ax0 = plt.subplots(figsize=(8, 4))
            ax0.plot(t, y)
            ax0.set_title("Breakpoints")
        for b in breaks:
            ax0.axvline(b, color="C3", ls="--", lw=1)
        fig.tight_layout()
        return fig
    cols = ["break_date", "confidence", "type"]
    if not breaks:
        return pd.DataFrame(columns=cols)
    return pd.DataFrame(
        [(label(k), conf(pmap.get(k, np.nan)), kind(k)) for k in breaks],
        columns=cols)

"breakpoints(data, method='cusum', alpha=0.05, at=None, nbreaks=None, plot=False, headers=True, date_col=None)"


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
