# Name: difference
# Description: Regular or seasonal difference of a series.
# Parameters: data, lag=1, order=1, headers=False

def difference(data, lag=1, order=1, headers=False):
    """Difference a series. lag=1 is regular; lag=period is seasonal.

    Applied `order` times. Leading rows that cannot be differenced are blank.

    data: value column, ref string, Series, or DataFrame (first numeric col).
    lag: difference step. Default 1.
    order: how many times to difference. Default 1.
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
    lag = int(pd.Series(lag).iloc[0])
    order = int(pd.Series(order).iloc[0])
    if lag < 1 or order < 1:
        raise ValueError("lag and order must be at least 1.")
    d = y.copy()
    for _ in range(order):
        d = d.diff(lag)
    return pd.DataFrame({"value": y, "diff": d})

"difference(data, lag=1, order=1, headers=False)"
