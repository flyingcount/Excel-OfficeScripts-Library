# Paul Python in Excel library (general)
#
# Formulas → Initialization → replace the editor contents with this file → Save.
# General-purpose functions only. Time series → init/TimeSeries.py.
# Sampling → init/Sampling.py. Do not duplicate those collections here.
# After Save, call contents() in a PY cell for the public function list.
#
# Restore defaults only: paste init/DefaultInitialization.py instead.
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


def contents():
    """List general library functions in this Initialization.

    Result spills as function / description / call. A readable description is
    enough when it already says what the function does. call matches the
    quoted signature after each def.
    """
    return pd.DataFrame(
        [
            ("contents", "List library functions", "contents()"),
            ("xl_df", "Load Excel data, drop empty rows", "xl_df(ref, headers=True)"),
            ("describe", "Summary statistics", "describe(data, headers=True)"),
            ("corr", "Pairwise correlation", "corr(data, method='pearson', headers=True)"),
            ("shapiro", "Shapiro-Wilk", "shapiro(data, metric=None, headers=False)"),
            ("anderson", "Anderson-Darling", "anderson(data, metric=None, headers=False)"),
            ("normality_check", "Q-Q plot with Shapiro-Wilk and Anderson-Darling", "normality_check(data, plot=True, headers=False)"),
            ("qq_norm", "Alias for normality_check", "qq_norm(data, plot=True, headers=False)"),
            ("cluster_prep", "Scale and one-hot encode for clustering", "cluster_prep(data, headers=True)"),
            ("outlier_flag", "Flag outliers by IQR, MAD, or z-score", "outlier_flag(data, method='iqr', threshold=1.5, headers=False)"),
        ],
        columns=["function", "description", "call"],
    )

"contents()"


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
      iqr     â€” outlier when value < Q1 - t*IQR or > Q3 + t*IQR.
      mad     â€” outlier when |value - median| / MAD > t  (MAD scaled by
                1.4826 to approximate std for normal data).
      zscore  â€” outlier when |value - mean| / std > t  (population std,
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
