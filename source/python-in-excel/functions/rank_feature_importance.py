# Name: rank_feature_importance_simple
# Description: Rank predictors vs a target with correlation, chi-square, and IV.
# Parameters: data, target, top=10, headers=True

def rank_feature_importance_simple(data, target, top=10, headers=True):
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

"rank_feature_importance_simple(data, target, top=10, headers=True)"
