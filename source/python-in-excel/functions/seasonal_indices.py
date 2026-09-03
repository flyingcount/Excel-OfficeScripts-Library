# Name: seasonal_indices
# Description: Seasonal index per season slot (multiplicative or additive).
# Parameters: data, period=12, kind='multiplicative', headers=False

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
