# Name: fourier_features
# Description: Sine/cosine Fourier terms for a seasonal period.
# Parameters: data, period=365, order=3, headers=False

def fourier_features(data, period=365, order=3, headers=False):
    """Sine and cosine Fourier terms for seasonal regression.

    For harmonic k = 1..order, angle = 2 * pi * k * t / period with t = 0
    at the first row. Spills the original value plus sin_k / cos_k columns.

    data: value column, ref string, Series, or DataFrame (first numeric col).
    period: seasonal length in rows. Default 365.
    order: number of harmonics. Default 3.
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
    n = int(y.size)
    if n < 1:
        raise ValueError("Need at least 1 value row.")
    period = float(pd.Series(period).iloc[0])
    order = int(pd.Series(order).iloc[0])
    if period <= 0:
        raise ValueError("period must be positive.")
    if order < 1:
        raise ValueError("order must be at least 1.")
    t = np.arange(n, dtype="float64")
    out = pd.DataFrame({"t": t, "value": y})
    for k in range(1, order + 1):
        angle = 2.0 * np.pi * k * t / period
        out["sin_%d" % k] = np.sin(angle)
        out["cos_%d" % k] = np.cos(angle)
    return out

"fourier_features(data, period=365, order=3, headers=False)"
