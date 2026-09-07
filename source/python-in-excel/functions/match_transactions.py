# Name: match_transactions
# Description: Match two transaction tables by description and value (exact and approximate).
# Parameters: df1, df2, date_col='Date', description_col='Description', value_col='Value', value_tol=0.01, desc_tol=0.8, summary=False, headers=True

def match_transactions(df1, df2, date_col="Date", description_col="Description",
                       value_col="Value", value_tol=0.01, desc_tol=0.8,
                       summary=False, headers=True):
    """Match two tables on description and value (exact then approximate).

    date_col, description_col, value_col default to Date, Description, Value
    (case-insensitive). Extra columns ignored. Difference = df1_value-df2_value
    on every row. Blank values become 0. Missing dates are None. summary=True
    groups matched vs unmatched.
    """
    from difflib import SequenceMatcher

    def to_frame(value):
        if isinstance(value, str):
            value = xl(value, headers=headers)
        if isinstance(value, pd.DataFrame):
            df = value
        elif isinstance(value, pd.Series):
            df = value.to_frame()
        else:
            df = pd.DataFrame(value)
        return df.dropna(how="all")

    def col(frame, name):
        key = str(pd.Series(name).iloc[0]).strip()
        cols = {str(c).strip().lower(): c for c in frame.columns}
        if key.lower() not in cols:
            raise ValueError("Column '%s' not found." % key)
        return cols[key.lower()]

    def as_dates(series):
        s = pd.Series(series).reset_index(drop=True)
        if pd.api.types.is_datetime64_any_dtype(s):
            p = pd.to_datetime(s)
        else:
            n = pd.to_numeric(s, errors="coerce")
            use = n.notna().mean() > 0.5 and n.dropna().size and n.dropna().median() > 200
            p = pd.to_datetime(n, unit="D", origin="1899-12-30") if use else pd.to_datetime(
                s, errors="coerce")
        return [None if pd.isna(x) else x.to_pydatetime() for x in p]

    def prep(frame):
        desc, nd = [], []
        for x in frame[col(frame, description_col)].tolist():
            if x is None or pd.isna(x):
                desc.append(None)
                nd.append("")
            else:
                t = str(x)
                desc.append(t)
                nd.append(" ".join(t.casefold().split()))
        val = pd.to_numeric(frame[col(frame, value_col)], errors="coerce").fillna(0.0)
        return as_dates(frame[col(frame, date_col)]), desc, nd, val.astype(float).tolist()

    def none_date(v):
        try:
            return None if v is None or pd.isna(v) else v
        except (TypeError, ValueError):
            return None

    value_tol = float(pd.Series(value_tol).iloc[0])
    desc_tol = float(pd.Series(desc_tol).iloc[0])
    if value_tol < 0:
        raise ValueError("value_tol must be >= 0.")
    if not 0 <= desc_tol <= 1:
        raise ValueError("desc_tol must be in [0, 1].")
    if not isinstance(summary, bool):
        summary = bool(pd.Series(summary).iloc[0])

    a, b = prep(to_frame(df1)), prep(to_frame(df2))
    n1, n2 = len(a[3]), len(b[3])
    used1, used2, pairs = set(), set(), []
    idx = {}
    for j in range(n2):
        idx.setdefault((b[2][j], round(b[3][j], 8)), []).append(j)
    for i in range(n1):
        for j in idx.get((a[2][i], round(a[3][i], 8)), []):
            if j not in used2:
                used1.add(i)
                used2.add(j)
                pairs.append((i, j, 0, 1.0))
                break
    labs = (
        "Exact match",
        "Approximate match (description)",
        "Approximate match (value)",
        "Approximate match (value and description)",
        "Exists only in df1",
        "Exists only in df2",
    )
    cands = []
    for i in range(n1):
        if i in used1:
            continue
        for j in range(n2):
            if j in used2:
                continue
            vd = abs(a[3][i] - b[3][j])
            ve, va = vd <= 1e-9, vd <= value_tol + 1e-12
            if not ve and not va:
                continue
            de = a[2][i] == b[2][j]
            if de:
                r, tier = 1.0, 0 if ve else 2
            else:
                r = SequenceMatcher(None, a[2][i], b[2][j]).ratio()
                if r < desc_tol:
                    continue
                tier = 1 if ve else 3
            cands.append((tier, -r, vd, i, j))
    cands.sort()
    for tier, neg_r, _vd, i, j in cands:
        if i in used1 or j in used2:
            continue
        used1.add(i)
        used2.add(j)
        pairs.append((i, j, tier, -neg_r))

    rows = []
    for i, j, tier, r in pairs:
        v1, v2 = a[3][i], b[3][j]
        dlt = v1 - v2
        lab = labs[tier] if not tier else (
            "%s; desc %g (tol %g)" % (
                labs[tier], round(r, 4), round(desc_tol, 4)))
        rows.append((a[0][i], a[1][i], v1, b[0][j], b[1][j], v2, dlt, lab,
                     "Matched"))
    for i in range(n1):
        if i not in used1:
            v1 = a[3][i]
            rows.append((a[0][i], a[1][i], v1, None, None, 0.0, v1, labs[4],
                         "Unmatched"))
    for j in range(n2):
        if j not in used2:
            v2 = b[3][j]
            rows.append((None, None, 0.0, b[0][j], b[1][j], v2, -v2, labs[5],
                         "Unmatched"))
    order = {k: i for i, k in enumerate(labs)}
    cols = ["df1_date", "df1_description", "df1_value", "df2_date",
            "df2_description", "df2_value", "Difference", "match_details",
            "match_group"]
    out = pd.DataFrame(rows, columns=cols)
    if not len(out):
        if summary:
            return pd.DataFrame(columns=[
                "match_group", "match_details", "count", "df1_value",
                "df2_value", "Difference"])
        return out
    out["_o"] = out["match_details"].str.split(";").str[0].map(order)
    out = out.sort_values("_o", kind="mergesort").drop(columns=["_o"]).reset_index(drop=True)
    out["df1_date"] = pd.Series([none_date(v) for v in out["df1_date"]], dtype=object)
    out["df2_date"] = pd.Series([none_date(v) for v in out["df2_date"]], dtype=object)
    if not summary:
        return out
    out = out.copy()
    out["match_details"] = out["match_details"].str.split(";").str[0]
    keys = ["match_group", "match_details"]
    agg = dict(count=("match_details", "count"), df1_value=("df1_value", "sum"),
               df2_value=("df2_value", "sum"), Difference=("Difference", "sum"))
    g = out.groupby(keys, as_index=False).agg(**agg)
    tot = out.groupby(["match_group"], as_index=False).agg(**agg)
    tot["match_details"] = "Total"
    sm = pd.concat([g, tot], ignore_index=True)
    sm["_g"] = sm["match_group"].map({"Matched": 0, "Unmatched": 1})
    sm["_d"] = sm["match_details"].map(order).fillna(99)
    return sm.sort_values(["_g", "_d"], kind="mergesort").drop(
        columns=["_g", "_d"]).reset_index(drop=True)[
            ["match_group", "match_details", "count", "df1_value", "df2_value",
             "Difference"]]

"match_transactions(df1, df2, date_col='Date', description_col='Description', value_col='Value', value_tol=0.01, desc_tol=0.8, summary=False, headers=True)"
