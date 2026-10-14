# Name: seasonally_adjust
# Description: Remove a seasonal index from a series (divide or subtract).
# Parameters: data, period=12, kind='multiplicative', headers=False

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
