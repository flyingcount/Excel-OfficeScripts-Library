# Name: detect_mixed_data_anomalies
# Description: Flag mixed-table anomalies via Mahalanobis distance and Isolation Forest.
# Parameters: data, contamination=0.05, max_categories=15, headers=True

def detect_mixed_data_anomalies(data, contamination=0.05, max_categories=15, headers=True):
    """Flag mixed numeric/categorical rows as anomalies.

    Mahalanobis on numeric columns (needs 2+); Isolation Forest on scaled
    numbers plus one-hot categories. Result keeps input columns.

    data: ref string, DataFrame, Series, or xl() result.
    contamination: expected anomaly share (default 0.05).
    max_categories: skip text columns with more unique values (default 15).
    headers: first row is headers when data is a ref string.

    Result: md_distance, md_p_value, if_score, flag_md, flag_if,
    anomaly_class (Consensus anomaly / Numeric outlier (MD) /
    Structural outlier (IF) / Normal).
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
    flag_md = np.zeros(n_rows, dtype="float64")
    if len(num_cols) >= 2:
        x = work[num_cols].to_numpy(dtype="float64")
        mean = x.mean(axis=0)
        inv = np.linalg.pinv(np.cov(x, rowvar=False))
        diff = x - mean
        md2 = np.einsum("ij,ij->i", diff @ inv, diff)
        md_dist = np.sqrt(np.clip(md2, 0, None))
        k = len(num_cols)
        p_val = 1 - chi2.cdf(md2, df=k)
        flag_md = (md2 > chi2.ppf(1 - contam, df=k)).astype("float64")

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
    flag_if = (iso.predict(mat) == -1).astype("float64")

    out = orig.copy()
    out["md_distance"] = md_dist
    out["md_p_value"] = p_val
    out["if_score"] = if_score
    out["flag_md"] = flag_md
    out["flag_if"] = flag_if
    out["anomaly_class"] = np.select(
        [(flag_md == 1) & (flag_if == 1),
         (flag_md == 1) & (flag_if == 0),
         (flag_md == 0) & (flag_if == 1)],
        ["Consensus anomaly", "Numeric outlier (MD)", "Structural outlier (IF)"],
        default="Normal",
    )
    return out

"detect_mixed_data_anomalies(data, contamination=0.05, max_categories=15, headers=True)"
