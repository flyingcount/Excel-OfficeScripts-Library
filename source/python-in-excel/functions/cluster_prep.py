# Name: cluster_prep
# Description: Scale numeric columns and one-hot encode categoricals for clustering.
# Parameters: data, headers=True

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
