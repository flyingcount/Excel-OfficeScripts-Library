# Paul Python in Excel library (general)
#
# Formulas → Initialization → replace the editor contents with this file → Save.
# General-purpose functions only. Time series → init/TimeSeries.py.
# Sampling → init/Sampling.py. SPC → init/SPC.py. Do not duplicate those collections here.
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
            ("outlier_flag", "Flag outliers by IQR, MAD, z-score, STL, or Isolation Forest", "outlier_flag(data, method='iqr', threshold=1.5, headers=False, period=12)"),
            ("detect_mixed_data_anomalies", "Flag mixed-table anomaly types (extreme, rare, multivariate, structural, consensus)", "detect_mixed_data_anomalies(data, contamination=0.05, max_categories=15, headers=True)"),
            ("rank_feature_importance", "Rank predictors vs a target (correlation, chi-square, IV)", "rank_feature_importance(data, target, top=10, headers=True)"),
            ("check_collinearity", "Flag highly correlated numeric columns (r and VIF)", "check_collinearity(data, threshold=0.8, vif_threshold=5, headers=True)"),
            ("confusion_matrix", "TP/FP/TN/FN counts, or a heatmap", "confusion_matrix(data, actual=None, predicted=None, positive=1, pos_name='Positive', neg_name='Negative', plot=False, headers=True)"),
            ("classification_metrics", "Accuracy, F1, MCC, and related class metrics", "classification_metrics(data, actual=None, predicted=None, positive=1, beta=1, headers=True)"),
            ("find_optimal_threshold", "Sweep probability cutoffs for F1 or P/R balance", "find_optimal_threshold(data, actual=None, proba=None, metric='f1', low=0.1, high=0.9, step=0.1, positive=1, headers=True)"),
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


def outlier_flag(data, method="iqr", threshold=1.5, headers=False, period=12):
    """Flag outlier rows. Spills value, is_outlier, score, lower_bound, upper_bound.

    data: value column, ref string, DataFrame, Series, or list.
    method: iqr (default), mad, zscore, stl, or iforest.
    threshold: IQR/MAD fence (default 1.5); |z| cutoff for zscore/stl (use 3);
        iforest contamination in (0, 0.5), else 'auto'.
    period: STL seasonal length. Default 12. Need 2 full seasons.
    headers: first row is headers when data is a ref string.

    stl: |residual z| after robust STL; bounds are trend+seasonal +/- t*sd.
    iforest: sklearn IsolationForest; score is -score_samples (higher = more
        anomalous); bounds are blank. random_state=42.
    Constant spread flags nothing. Blanks stay blank.
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
    m = str(pd.Series(method).iloc[0]).strip().lower().replace("_", "-")
    period = int(pd.Series(period).iloc[0])
    score = pd.Series(np.nan, index=y.index, dtype="float64")
    lo = pd.Series(np.nan, index=y.index, dtype="float64")
    hi = lo.copy()
    outliers = pd.Series(False, index=y.index)

    if m == "iqr":
        q1, q3 = float(y.quantile(0.25)), float(y.quantile(0.75))
        iqr = q3 - q1
        lo[:], hi[:] = q1 - t * iqr, q3 + t * iqr
        score = y.copy()
        if iqr != 0:
            outliers = ((y < lo) | (y > hi)).fillna(False)
    elif m == "mad":
        med = float(y.median(skipna=True))
        abs_dev = (y - med).abs()
        mad_s = float(abs_dev.median(skipna=True)) * 1.4826
        if mad_s != 0 and np.isfinite(mad_s):
            score = abs_dev / mad_s
            outliers = (score > t).fillna(False)
            lo[:], hi[:] = med - t * mad_s, med + t * mad_s
    elif m == "zscore":
        mu = float(y.mean(skipna=True))
        sigma = float(y.std(ddof=0, skipna=True))
        if sigma != 0 and np.isfinite(sigma):
            score = ((y - mu) / sigma).abs()
            outliers = (score > t).fillna(False)
            lo[:], hi[:] = mu - t * sigma, mu + t * sigma
    elif m in ("stl", "stl-resid"):
        from statsmodels.tsa.seasonal import STL
        if period < 2:
            raise ValueError("period must be at least 2 for STL.")
        ok = y.notna()
        if int(ok.sum()) < period * 2:
            raise ValueError("Need at least 2 full seasons for STL.")
        fit = STL(y[ok].to_numpy(dtype="float64"), period=period, robust=True).fit()
        r = pd.Series(fit.resid, index=y.index[ok])
        mu, sd = float(r.mean()), float(r.std(ddof=0))
        exp = y[ok] - r
        lo.loc[ok], hi.loc[ok] = exp, exp
        if sd != 0 and np.isfinite(sd):
            z = (r - mu) / sd
            score.loc[ok] = z.abs()
            outliers.loc[ok] = z.abs() > t
            lo.loc[ok], hi.loc[ok] = exp - t * sd, exp + t * sd
        else:
            score.loc[ok] = 0.0
    elif m in ("iforest", "isolation-forest", "iso"):
        from sklearn.ensemble import IsolationForest
        ok = y.notna()
        X = y[ok].to_numpy(dtype="float64").reshape(-1, 1)
        if X.shape[0] < 2:
            raise ValueError("Need at least 2 observations for Isolation Forest.")
        contam = t if 0 < t < 0.5 else "auto"
        clf = IsolationForest(contamination=contam, random_state=42)
        clf.fit(X)
        score.loc[ok] = -clf.score_samples(X)
        outliers.loc[ok] = clf.predict(X) == -1
    else:
        raise ValueError(
            "method '%s' not supported. Use 'iqr', 'mad', 'zscore', 'stl', or 'iforest'." % m)

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

"outlier_flag(data, method='iqr', threshold=1.5, headers=False, period=12)"


def detect_mixed_data_anomalies(data, contamination=0.05, max_categories=15, headers=True):
    """Flag mixed numeric/categorical rows as anomalies.

    Mahalanobis on numeric columns (needs 2+); Isolation Forest on scaled
    numbers plus one-hot categories. Also flags univariate |z|>3, rare
    categories, and within-group numeric extremes.

    data: ref string, DataFrame, Series, or xl() result.
    contamination: expected anomaly share (default 0.05).
    max_categories: skip text columns with more unique values (default 15).
    headers: first row is headers when data is a ref string.

    Result: md_distance, md_p_value, if_score, flag_md, flag_if,
    flag_extreme, flag_rare, anomaly_class.
    """
    from scipy.stats import chi2
    from sklearn.ensemble import IsolationForest
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import OneHotEncoder, StandardScaler

    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        df = data.copy()
    elif isinstance(data, pd.Series):
        df = data.to_frame()
    else:
        df = pd.DataFrame(data)
    df = df.reset_index(drop=True)
    orig = df.copy()
    contam = float(pd.Series(contamination).iloc[0])
    max_cat = int(pd.Series(max_categories).iloc[0])
    if not 0 < contam <= 0.5:
        raise ValueError("contamination must be in (0, 0.5].")

    for c in list(df.columns):
        if pd.api.types.is_numeric_dtype(df[c]):
            continue
        conv = pd.to_numeric(df[c], errors="coerce")
        if df[c].notna().any() and float(conv.notna().mean()) >= 0.8:
            df[c] = conv

    num_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = []
    n_rows = len(df)
    for c in df.select_dtypes(include=["object", "category", "string"]).columns:
        n_unq = int(df[c].nunique(dropna=True))
        n_ok = int(df[c].notna().sum())
        if 1 < n_unq <= max_cat and n_unq < max(n_ok, 2):
            cat_cols.append(c)
    if not num_cols and not cat_cols:
        raise ValueError("No numeric or categorical columns to process.")

    work = df.copy()
    keep_num = []
    for c in num_cols:
        s = pd.to_numeric(work[c], errors="coerce")
        med = s.median()
        s = s.fillna(med)
        if s.notna().any():
            work[c] = s
            keep_num.append(c)
    num_cols = keep_num
    for c in cat_cols:
        work[c] = work[c].fillna("Missing").astype(str)
    if not num_cols and not cat_cols:
        raise ValueError("No numeric or categorical columns to process.")
    if n_rows < 2:
        raise ValueError("Need at least 2 rows for Isolation Forest.")

    md_dist = np.zeros(n_rows, dtype="float64")
    p_val = np.ones(n_rows, dtype="float64")
    flag_md = np.zeros(n_rows, dtype=bool)
    if len(num_cols) >= 2:
        x = work[num_cols].to_numpy(dtype="float64")
        mean = x.mean(axis=0)
        inv = np.linalg.pinv(np.cov(x, rowvar=False))
        diff = x - mean
        md2 = np.einsum("ij,ij->i", diff @ inv, diff)
        md_dist = np.sqrt(np.clip(md2, 0, None))
        k = len(num_cols)
        p_val = 1 - chi2.cdf(md2, df=k)
        flag_md = md2 > chi2.ppf(1 - contam, df=k)

    flag_ext = np.zeros(n_rows, dtype=bool)
    if num_cols:
        x = work[num_cols].to_numpy(dtype="float64")
        sd = x.std(axis=0, ddof=0)
        sd = np.where(sd == 0, np.nan, sd)
        zmax = np.nanmax(np.abs((x - x.mean(axis=0)) / sd), axis=1)
        flag_ext = np.where(np.isnan(zmax), False, zmax > 3)

    flag_rare = np.zeros(n_rows, dtype=bool)
    for c in cat_cols:
        freq = work[c].map(work[c].value_counts(normalize=True))
        flag_rare |= (freq <= contam).to_numpy()

    flag_combo = np.zeros(n_rows, dtype=bool)
    if cat_cols and num_cols:
        for c in cat_cols:
            n_g = work.groupby(c)[num_cols[0]].transform("size")
            for nc in num_cols:
                g = work.groupby(c)[nc]
                z = (work[nc] - g.transform("mean")) / g.transform(
                    lambda s: s.std(ddof=0)).replace(0, np.nan)
                flag_combo |= (
                    (n_g >= 4) & (n_g < n_rows) & z.abs().gt(3)
                ).fillna(False).to_numpy()
    flag_combo &= ~np.asarray(flag_ext, dtype=bool)

    steps = []
    if num_cols:
        steps.append(("num", StandardScaler(), num_cols))
    if cat_cols:
        try:
            ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
        except TypeError:
            ohe = OneHotEncoder(handle_unknown="ignore", sparse=False)
        steps.append(("cat", ohe, cat_cols))
    mat = ColumnTransformer(steps, remainder="drop").fit_transform(work)
    if hasattr(mat, "toarray"):
        mat = mat.toarray()
    iso = IsolationForest(contamination=contam, random_state=42)
    iso.fit(mat)
    if_score = iso.decision_function(mat)
    flag_if = iso.predict(mat) == -1

    num_sig = flag_ext | flag_md
    cat_sig = flag_rare | flag_combo
    out = orig.copy()
    out["md_distance"] = md_dist
    out["md_p_value"] = p_val
    out["if_score"] = if_score
    out["flag_md"] = flag_md.astype("float64")
    out["flag_if"] = flag_if.astype("float64")
    out["flag_extreme"] = np.asarray(flag_ext, dtype="float64")
    out["flag_rare"] = np.asarray(flag_rare, dtype="float64")
    out["anomaly_class"] = np.select(
        [num_sig & cat_sig, flag_ext, flag_md, flag_rare,
         flag_combo | flag_if],
        ["Consensus Anomaly", "Extreme Value (Numeric)",
         "Multivariate Outlier (Numeric)", "Rare Category (Categorical)",
         "Inconsistent Structural Combo"],
        default="Normal",
    )
    return out

"detect_mixed_data_anomalies(data, contamination=0.05, max_categories=15, headers=True)"


def rank_feature_importance(data, target, top=10, headers=True):
    """Rank table columns as drivers of a target.

    Numeric vs binary: |point-biserial r|. Categorical: Cramer's V (chi-square).
    Binary targets also get Information Value (numeric features are quantile
    binned). Other targets use |Pearson r| or eta. Ranked by score (higher
    = stronger). Not a full ML model.

    data: ref string, DataFrame, Series, or xl() result.
    target: column name, range ref, or Series/column of y.
    top: rows to return (default 10). 0 returns every scored feature.
    headers: first row is headers when data or target is a ref string.
    """
    from scipy.stats import pointbiserialr, pearsonr, chi2_contingency, f_oneway

    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        df = data.copy()
    elif isinstance(data, pd.Series):
        df = data.to_frame()
    else:
        df = pd.DataFrame(data)
    df = df.reset_index(drop=True)
    if df.empty:
        raise ValueError("No data.")
    top = int(pd.Series(top).iloc[0])

    def find_col(name):
        key = str(name).strip()
        lookup = {str(c).strip().lower(): c for c in df.columns}
        if key.lower() in lookup:
            return lookup[key.lower()]
        return None

    tcol = None
    if isinstance(target, pd.DataFrame):
        y0 = target.iloc[:, 0]
        df["_target"] = pd.Series(y0).reset_index(drop=True)
        tcol = "_target"
    elif isinstance(target, pd.Series) and int(target.size) > 1:
        df["_target"] = target.reset_index(drop=True)
        tcol = "_target"
    else:
        tgt = str(pd.Series(target).iloc[0]).strip()
        hit = find_col(tgt)
        if hit is not None:
            tcol = hit
        else:
            raw = xl(tgt, headers=headers)
            if isinstance(raw, pd.DataFrame):
                raw = raw.iloc[:, 0]
            df["_target"] = pd.Series(raw).reset_index(drop=True)
            tcol = "_target"
    n0 = min(len(df), int(pd.Series(df[tcol]).size))
    df = df.iloc[:n0].copy()
    df[tcol] = df[tcol].replace("", np.nan)
    df = df.dropna(subset=[tcol]).reset_index(drop=True)
    if len(df) < 3:
        raise ValueError("Need at least 3 rows with a target.")

    y_raw = df[tcol]
    y_num = pd.to_numeric(y_raw, errors="coerce")
    n_lev = int(y_raw.nunique(dropna=True))
    y_is_num = float(y_num.notna().mean()) >= 0.8
    binary = n_lev == 2
    if binary:
        codes = pd.Categorical(y_raw).codes.astype("float64")
        y_bin = pd.Series(codes, index=df.index)
        y_cont = y_bin
        y_cat = y_raw.astype(str)
    elif y_is_num and n_lev > 12:
        y_cont = y_num
        y_cat = None
        y_bin = None
    else:
        y_cont = None
        y_cat = y_raw.astype(str)
        y_bin = None

    def iv_of(x, yb):
        tab = pd.crosstab(x, yb)
        if tab.shape[1] != 2 or tab.shape[0] < 2:
            return np.nan
        a, b = tab.columns[0], tab.columns[1]
        n_a, n_b = float(tab[a].sum()), float(tab[b].sum())
        if n_a == 0 or n_b == 0:
            return np.nan
        k = float(len(tab))
        p0 = (tab[a] + 0.5) / (n_a + 0.5 * k)
        p1 = (tab[b] + 0.5) / (n_b + 0.5 * k)
        return float(((p1 - p0) * np.log(p1 / p0)).sum())

    def cramer(a, b):
        tab = pd.crosstab(a, b)
        if tab.shape[0] < 2 or tab.shape[1] < 2:
            return np.nan, np.nan
        chi, p, _, _ = chi2_contingency(tab, correction=False)
        k = min(tab.shape[0] - 1, tab.shape[1] - 1)
        n = float(tab.to_numpy().sum())
        v = 0.0 if k <= 0 or n == 0 else float(np.sqrt(chi / (n * k)))
        return v, float(p)

    def eta_of(groups):
        groups = [g for g in groups if len(g) >= 2]
        if len(groups) < 2:
            return np.nan, np.nan
        _, p = f_oneway(*groups)
        arr = np.concatenate(groups)
        grand = float(arr.mean())
        sst = float(np.sum((arr - grand) ** 2))
        ssb = sum(len(g) * (float(g.mean()) - grand) ** 2 for g in groups)
        e = 0.0 if sst == 0 else float(np.sqrt(ssb / sst))
        return e, float(p)

    rows = []
    for c in df.columns:
        if c == tcol:
            continue
        s = df[c].replace("", np.nan)
        if pd.api.types.is_datetime64_any_dtype(s):
            continue
        is_num = pd.api.types.is_numeric_dtype(s)
        if not is_num:
            conv = pd.to_numeric(s, errors="coerce")
            if s.notna().any() and float(conv.notna().mean()) >= 0.8:
                s, is_num = conv, True
        ok = s.notna()
        if int(ok.sum()) < 3:
            continue
        n_unq = int(s[ok].nunique())
        if n_unq < 2:
            continue
        if (not is_num) and n_unq >= int(ok.sum()):
            continue
        ftype = "numeric" if is_num else "categorical"
        score = pval = iv = np.nan
        method = ""
        if is_num:
            x = pd.to_numeric(s, errors="coerce")
            m = x.notna()
            if binary:
                xb, yb = x[m], y_bin[m]
                if int(yb.nunique()) < 2:
                    continue
                r, pval = pointbiserialr(yb.to_numpy(), xb.to_numpy())
                score, method = abs(float(r)), "point-biserial"
                try:
                    bins = pd.qcut(xb, q=min(10, int(xb.nunique())),
                                   duplicates="drop")
                    iv = iv_of(bins, yb)
                except (ValueError, TypeError):
                    iv = np.nan
            elif y_cont is not None:
                yc = y_cont[m]
                keep = yc.notna()
                if int(keep.sum()) < 3:
                    continue
                r, pval = pearsonr(x[m][keep].to_numpy(),
                                   yc[keep].to_numpy())
                score, method = abs(float(r)), "pearson"
            else:
                groups = [x[m & (y_cat == lev)].dropna().to_numpy()
                          for lev in y_cat[m].unique()]
                score, pval = eta_of(groups)
                method = "eta"
        else:
            x = s.astype(str)
            if binary:
                score, pval = cramer(x, y_cat)
                method = "chi-square"
                iv = iv_of(x, y_bin)
            elif y_cat is not None:
                score, pval = cramer(x, y_cat)
                method = "chi-square"
            else:
                yc = y_cont
                m = s.notna() & yc.notna()
                groups = [yc[m & (x == lev)].dropna().to_numpy()
                          for lev in x[m].unique()]
                score, pval = eta_of(groups)
                method = "eta"
        if not np.isfinite(score):
            continue
        if score < 0.1:
            strength = "weak"
        elif score < 0.3:
            strength = "modest"
        elif score < 0.5:
            strength = "moderate"
        else:
            strength = "strong"
        rows.append((c, ftype, method, float(score),
                     float(pval) if np.isfinite(pval) else np.nan,
                     float(iv) if np.isfinite(iv) else np.nan, strength))
    if not rows:
        raise ValueError("No scorable features.")
    out = pd.DataFrame(rows, columns=["feature", "type", "method", "score",
                                      "p_value", "iv", "strength"])
    out = out.sort_values(["score", "feature"], ascending=[False, True])
    if top > 0:
        out = out.head(top)
    out.insert(0, "rank", np.arange(1, len(out) + 1, dtype="float64"))
    return out.reset_index(drop=True)

"rank_feature_importance(data, target, top=10, headers=True)"


def check_collinearity(data, threshold=0.8, vif_threshold=5, headers=True):
    """Highlight redundant numeric columns via Pearson r and VIF.

    One row per numeric feature: strongest partner (|r|), count of pairs
    above threshold, and variance inflation factor. flag is 1 if |r| >
    threshold or VIF > vif_threshold. Not a regression model.

    data: ref string, DataFrame, Series, or xl() result.
    threshold: |r| cutoff (default 0.8). Pair must be strictly greater.
    vif_threshold: VIF cutoff (default 5).
    headers: first row is headers when data is a ref string.
    """
    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        df = data.copy()
    elif isinstance(data, pd.Series):
        df = data.to_frame()
    else:
        df = pd.DataFrame(data)
    df = df.dropna(how="all").dropna(axis=1, how="all")
    if df.empty:
        raise ValueError("No data.")
    thr = float(pd.Series(threshold).iloc[0])
    vif_thr = float(pd.Series(vif_threshold).iloc[0])
    if not 0 < thr <= 1:
        raise ValueError("threshold must be in (0, 1].")
    if vif_thr <= 0:
        raise ValueError("vif_threshold must be > 0.")

    keep = []
    for c in list(df.columns):
        s = df[c].replace("", np.nan)
        if pd.api.types.is_datetime64_any_dtype(s):
            continue
        if pd.api.types.is_bool_dtype(s):
            df[c] = s.astype("float64")
            keep.append(c)
            continue
        if pd.api.types.is_numeric_dtype(s):
            df[c] = pd.to_numeric(s, errors="coerce")
            keep.append(c)
            continue
        conv = pd.to_numeric(s, errors="coerce")
        if s.notna().any() and float(conv.notna().mean()) >= 0.8:
            df[c] = conv
            keep.append(c)
    num = df[keep].copy() if keep else df.iloc[:, 0:0]
    drop = [c for c in num.columns if float(num[c].std(ddof=0) or 0) == 0]
    num = num.drop(columns=drop)
    if num.shape[1] < 2:
        raise ValueError("Need at least 2 numeric columns.")
    complete = num.dropna()
    if len(complete) < 3:
        raise ValueError("Need at least 3 complete numeric rows.")

    cmat = num.corr()
    x = complete.to_numpy(dtype="float64")
    n, p = x.shape
    vifs = np.empty(p)
    for j in range(p):
        y = x[:, j]
        z = np.column_stack([np.ones(n), np.delete(x, j, axis=1)])
        beta, *_ = np.linalg.lstsq(z, y, rcond=None)
        yhat = z @ beta
        ss_res = float(np.sum((y - yhat) ** 2))
        ss_tot = float(np.sum((y - y.mean()) ** 2))
        if ss_tot == 0:
            vifs[j] = np.nan
        elif ss_res <= 1e-12 * ss_tot:
            vifs[j] = np.inf
        else:
            vifs[j] = 1.0 / (1.0 - ss_res / ss_tot)

    names = list(complete.columns)
    rows = []
    for i, col in enumerate(names):
        others = cmat[col].drop(labels=[col])
        k = others.abs().idxmax()
        r = float(others.loc[k])
        n_high = float((others.abs() > thr).sum())
        vif = float(vifs[i])
        hi_r = bool(np.isfinite(r) and abs(r) > thr)
        hi_v = bool(np.isfinite(vif) and vif > vif_thr) or (
            not np.isfinite(vif) and not np.isnan(vif))
        rows.append((col, vif, r, str(k), n_high,
                     1.0 if hi_r else 0.0,
                     1.0 if hi_v else 0.0,
                     1.0 if (hi_r or hi_v) else 0.0))
    out = pd.DataFrame(rows, columns=["feature", "vif", "max_r", "with",
                                      "n_high", "flag_corr", "flag_vif",
                                      "flag"])
    return out.sort_values(["flag", "vif"], ascending=[False, False]).reset_index(
        drop=True)

"check_collinearity(data, threshold=0.8, vif_threshold=5, headers=True)"


def confusion_matrix(data, actual=None, predicted=None, positive=1,
                     pos_name="Positive", neg_name="Negative",
                     plot=False, headers=True):
    """Confusion-matrix counts with business labels.

    data: table/range, or actual labels if predicted is a Series/range.
    actual, predicted: column names, ranges, or Series. Default: first two
        columns of data.
    positive: value treated as the positive class (default 1).
    pos_name, neg_name: words in the meaning column (e.g. 'Churn').
    plot: False (default) spills a table. True returns a 2x2 heatmap.
        Keep that PY cell as a Python object.
    headers: first row is headers when a ref string is used.
    """
    def frame_of(value):
        if isinstance(value, str):
            value = xl(value, headers=headers)
        if isinstance(value, pd.DataFrame):
            return value.reset_index(drop=True)
        if isinstance(value, pd.Series):
            return value.to_frame()
        return pd.DataFrame(value)

    def col(frame, spec, idx):
        if spec is None:
            if frame.shape[1] <= idx:
                raise ValueError("Need actual and predicted columns.")
            return frame.iloc[:, idx]
        if isinstance(spec, pd.DataFrame):
            return spec.iloc[:, 0]
        if isinstance(spec, pd.Series) and int(spec.size) > 1:
            return spec.reset_index(drop=True)
        key = str(pd.Series(spec).iloc[0]).strip()
        lookup = {str(c).strip().lower(): c for c in frame.columns}
        if key.lower() in lookup:
            return frame[lookup[key.lower()]]
        raw = xl(key, headers=headers)
        if isinstance(raw, pd.DataFrame):
            raw = raw.iloc[:, 0]
        return pd.Series(raw)

    def is_pos(s, pos):
        s = pd.Series(s).reset_index(drop=True)
        pn = pd.to_numeric(pd.Series([pos]), errors="coerce").iloc[0]
        if pd.notna(pn):
            return pd.to_numeric(s, errors="coerce") == float(pn)
        return s.astype(str).str.strip() == str(pos).strip()

    frame = frame_of(data)
    a = pd.Series(col(frame, actual, 0)).reset_index(drop=True)
    p = pd.Series(col(frame, predicted, 1)).reset_index(drop=True)
    n0 = min(len(a), len(p))
    a, p = a.iloc[:n0], p.iloc[:n0]
    a = a.replace("", np.nan)
    p = p.replace("", np.nan)
    keep = a.notna() & p.notna()
    a, p = a[keep], p[keep]
    if len(a) < 1:
        raise ValueError("Need at least 1 row with actual and predicted.")
    pos = pd.Series(positive).iloc[0]
    pos_name = str(pd.Series(pos_name).iloc[0])
    neg_name = str(pd.Series(neg_name).iloc[0])
    if not isinstance(plot, bool):
        plot = bool(pd.Series(plot).iloc[0])
    yt, yp = is_pos(a, pos), is_pos(p, pos)
    tp = float((yt & yp).sum())
    fp = float((~yt & yp).sum())
    fn = float((yt & ~yp).sum())
    tn = float((~yt & ~yp).sum())
    if plot:
        mat = np.array([[tp, fn], [fp, tn]])
        labs = [pos_name, neg_name]
        fig, ax = plt.subplots()
        sns.heatmap(
            mat, annot=True, fmt=".0f", cmap="Blues", cbar=False,
            xticklabels=labs, yticklabels=labs, ax=ax, square=True,
        )
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")
        ax.set_title("Confusion matrix")
        fig.tight_layout()
        return fig
    return pd.DataFrame(
        [
            ("true_positive", tp,
             "Actual %s and Predicted %s" % (pos_name, pos_name)),
            ("false_positive", fp,
             "Actual %s and Predicted %s" % (neg_name, pos_name)),
            ("false_negative", fn,
             "Actual %s and Predicted %s" % (pos_name, neg_name)),
            ("true_negative", tn,
             "Actual %s and Predicted %s" % (neg_name, neg_name)),
        ],
        columns=["metric", "count", "meaning"],
    )

"confusion_matrix(data, actual=None, predicted=None, positive=1, pos_name='Positive', neg_name='Negative', plot=False, headers=True)"


def classification_metrics(data, actual=None, predicted=None, positive=1,
                           beta=1, headers=True):
    """Accuracy, rates, F1/F-beta, MCC, and related binary metrics.

    data: table/range, or actual labels if predicted is a Series/range.
    actual, predicted: column names, ranges, or Series. Default: first two
        columns of data (hard labels, not probabilities).
    positive: value treated as the positive class (default 1).
    beta: weight on recall in F-beta (default 1, same as F1).
    headers: first row is headers when a ref string is used.
    """
    def frame_of(value):
        if isinstance(value, str):
            value = xl(value, headers=headers)
        if isinstance(value, pd.DataFrame):
            return value.reset_index(drop=True)
        if isinstance(value, pd.Series):
            return value.to_frame()
        return pd.DataFrame(value)

    def col(frame, spec, idx):
        if spec is None:
            if frame.shape[1] <= idx:
                raise ValueError("Need actual and predicted columns.")
            return frame.iloc[:, idx]
        if isinstance(spec, pd.DataFrame):
            return spec.iloc[:, 0]
        if isinstance(spec, pd.Series) and int(spec.size) > 1:
            return spec.reset_index(drop=True)
        key = str(pd.Series(spec).iloc[0]).strip()
        lookup = {str(c).strip().lower(): c for c in frame.columns}
        if key.lower() in lookup:
            return frame[lookup[key.lower()]]
        raw = xl(key, headers=headers)
        if isinstance(raw, pd.DataFrame):
            raw = raw.iloc[:, 0]
        return pd.Series(raw)

    def is_pos(s, pos):
        s = pd.Series(s).reset_index(drop=True)
        pn = pd.to_numeric(pd.Series([pos]), errors="coerce").iloc[0]
        if pd.notna(pn):
            return pd.to_numeric(s, errors="coerce") == float(pn)
        return s.astype(str).str.strip() == str(pos).strip()

    def div(num, den):
        return float(num / den) if den else np.nan

    frame = frame_of(data)
    a = pd.Series(col(frame, actual, 0)).reset_index(drop=True)
    p = pd.Series(col(frame, predicted, 1)).reset_index(drop=True)
    n0 = min(len(a), len(p))
    a, p = a.iloc[:n0], p.iloc[:n0]
    a = a.replace("", np.nan)
    p = p.replace("", np.nan)
    keep = a.notna() & p.notna()
    a, p = a[keep], p[keep]
    n = int(len(a))
    if n < 1:
        raise ValueError("Need at least 1 row with actual and predicted.")
    pos = pd.Series(positive).iloc[0]
    b = float(pd.Series(beta).iloc[0])
    if b <= 0:
        raise ValueError("beta must be > 0.")
    yt, yp = is_pos(a, pos), is_pos(p, pos)
    tp = float((yt & yp).sum())
    fp = float((~yt & yp).sum())
    fn = float((yt & ~yp).sum())
    tn = float((~yt & ~yp).sum())
    tpr = tp / (tp + fn) if (tp + fn) else 0.0
    fpr = fp / (fp + tn) if (fp + tn) else 0.0
    tnr = tn / (tn + fp) if (tn + fp) else 0.0
    fnr = fn / (tp + fn) if (tp + fn) else 0.0
    prec = tp / (tp + fp) if (tp + fp) else 0.0
    npv = tn / (tn + fn) if (tn + fn) else 0.0
    acc = (tp + tn) / n
    f1 = (2 * prec * tpr / (prec + tpr)) if (prec + tpr) else 0.0
    bb = b * b
    fbeta = ((1 + bb) * prec * tpr / (bb * prec + tpr)
             if (bb * prec + tpr) else 0.0)
    lr_p = div(tpr, fpr)
    lr_n = div(fnr, tnr)
    mcc_d = float(np.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn)))
    return pd.DataFrame(
        [
            ("n", float(n)),
            ("accuracy", acc),
            ("misclassification_rate", (fp + fn) / n),
            ("true_positive_rate", tpr),
            ("false_positive_rate", fpr),
            ("true_negative_rate", tnr),
            ("false_negative_rate", fnr),
            ("precision", prec),
            ("prevalence", (tp + fn) / n),
            ("lr_positive", lr_p),
            ("lr_negative", lr_n),
            ("diagnostic_odds_ratio", div(lr_p, lr_n)),
            ("f1", f1),
            ("beta", b),
            ("f_beta", fbeta),
            ("mcc", div(tp * tn - fp * fn, mcc_d)),
            ("informedness", tpr + tnr - 1.0),
            ("markedness", prec + npv - 1.0),
            ("threat_score", div(tp, tp + fp + fn)),
        ],
        columns=["metric", "value"],
    )

"classification_metrics(data, actual=None, predicted=None, positive=1, beta=1, headers=True)"


def find_optimal_threshold(data, actual=None, proba=None, metric="f1",
                           low=0.1, high=0.9, step=0.1, positive=1,
                           headers=True):
    """Choose a probability cutoff by F1 or precision/recall balance.

    Sweeps thresholds from low to high (default 0.1 to 0.9). metric='f1'
    maximises F1. metric='balanced' minimises |precision - recall|
    (F1 breaks ties). Default 0.5 is often weak on imbalanced data.

    data: table/range, or actual labels if proba is a Series/range.
    actual, proba: column names, ranges, or Series. Default: first two
        columns of data (labels, then scores).
    positive: value treated as the positive class (default 1).
    headers: first row is headers when a ref string is used.
    """
    def frame_of(value):
        if isinstance(value, str):
            value = xl(value, headers=headers)
        if isinstance(value, pd.DataFrame):
            return value.reset_index(drop=True)
        if isinstance(value, pd.Series):
            return value.to_frame()
        return pd.DataFrame(value)

    def col(frame, spec, idx):
        if spec is None:
            if frame.shape[1] <= idx:
                raise ValueError("Need actual and probability columns.")
            return frame.iloc[:, idx]
        if isinstance(spec, pd.DataFrame):
            return spec.iloc[:, 0]
        if isinstance(spec, pd.Series) and int(spec.size) > 1:
            return spec.reset_index(drop=True)
        key = str(pd.Series(spec).iloc[0]).strip()
        lookup = {str(c).strip().lower(): c for c in frame.columns}
        if key.lower() in lookup:
            return frame[lookup[key.lower()]]
        raw = xl(key, headers=headers)
        if isinstance(raw, pd.DataFrame):
            raw = raw.iloc[:, 0]
        return pd.Series(raw)

    def is_pos(s, pos):
        s = pd.Series(s).reset_index(drop=True)
        pn = pd.to_numeric(pd.Series([pos]), errors="coerce").iloc[0]
        if pd.notna(pn):
            return pd.to_numeric(s, errors="coerce") == float(pn)
        return s.astype(str).str.strip() == str(pos).strip()

    frame = frame_of(data)
    a = pd.Series(col(frame, actual, 0)).reset_index(drop=True)
    pr = pd.to_numeric(col(frame, proba, 1), errors="coerce")
    pr = pd.Series(pr).reset_index(drop=True)
    n0 = min(len(a), len(pr))
    a, pr = a.iloc[:n0], pr.iloc[:n0]
    a = a.replace("", np.nan)
    keep = a.notna() & pr.notna()
    a, pr = a[keep], pr[keep]
    n = int(len(a))
    if n < 1:
        raise ValueError("Need at least 1 row with actual and probability.")
    pos = pd.Series(positive).iloc[0]
    metric = str(pd.Series(metric).iloc[0]).strip().lower()
    if metric not in ("f1", "balanced"):
        raise ValueError("metric must be 'f1' or 'balanced'.")
    low = float(pd.Series(low).iloc[0])
    high = float(pd.Series(high).iloc[0])
    step = float(pd.Series(step).iloc[0])
    if step <= 0 or high < low:
        raise ValueError("Need low <= high and step > 0.")
    nstep = int(round((high - low) / step))
    ts = low + np.arange(nstep + 1, dtype="float64") * step
    yt = is_pos(a, pos).to_numpy()
    scores = pr.to_numpy(dtype="float64")
    rows = []
    best_i, best_key = 0, None
    for t in ts:
        yp = scores >= t
        tp = float((yt & yp).sum())
        fp = float((~yt & yp).sum())
        fn = float((yt & ~yp).sum())
        tn = float((~yt & ~yp).sum())
        acc = (tp + tn) / n
        prec = tp / (tp + fp) if (tp + fp) else 0.0
        rec = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = (2 * prec * rec / (prec + rec)) if (prec + rec) else 0.0
        key = (f1, -abs(prec - rec)) if metric == "f1" else (
            -abs(prec - rec), f1)
        rows.append((float(t), acc, prec, rec, f1, 0.0))
        if best_key is None or key > best_key:
            best_key = key
            best_i = len(rows) - 1
    out = pd.DataFrame(rows, columns=["threshold", "accuracy", "precision",
                                      "recall", "f1", "is_best"])
    out.loc[best_i, "is_best"] = 1.0
    return out

"find_optimal_threshold(data, actual=None, proba=None, metric='f1', low=0.1, high=0.9, step=0.1, positive=1, headers=True)"
