# Python in Excel time series library
#
# Formulas → Initialization → replace the editor contents with this file → Save.
# This file is a complete Initialization: Excel defaults, then time series functions only.
#
# Full library (all functions): paste init/PaulPythonLibrary.py instead.
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
