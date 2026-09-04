# Name: check_collinearity
# Description: Flag numeric columns that are highly correlated (r and VIF).
# Parameters: data, threshold=0.8, vif_threshold=5, headers=True

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
