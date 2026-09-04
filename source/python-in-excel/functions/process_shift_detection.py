# Name: process_shift_detection
# Description: Flag mean shifts via CUSUM, EWMA, or XmR.
# Parameters: data, method='cusum', headers=False

def process_shift_detection(data, method="cusum", headers=False):
    """Flag process mean shifts for individuals.

    method='cusum' (default) uses tabular CUSUM (k=0.5, h=5).
    method='ewma' uses EWMA limits (lambda_=0.2, L=3).
    method='xmr' uses 3-sigma individuals plus an 8-point run.
    Sigma is MR-bar / 1.128. Result is one row per point.

    data: value column, ref string, Series, DataFrame, or list.
    headers: first row is headers when data is a ref string.
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
    y = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce")
    y = y.replace("", np.nan).dropna().reset_index(drop=True)
    n = int(y.size)
    if n < 2:
        raise ValueError("Need at least 2 numeric values.")
    m = str(pd.Series(method).iloc[0]).strip().lower()
    if m in ("shewhart", "individuals"):
        m = "xmr"
    if m not in ("cusum", "ewma", "xmr"):
        raise ValueError("method must be cusum, ewma, or xmr.")
    yv = y.to_numpy(dtype="float64")
    mu = float(np.mean(yv))
    mrb = float(np.mean(np.abs(np.diff(yv))))
    sig = 0.0 if mrb == 0 else mrb / 1.128
    hi = np.zeros(n, dtype=bool)
    lo = np.zeros(n, dtype=bool)
    if m == "cusum":
        K, H = 0.5 * sig, 5.0 * sig
        ph = pl = 0.0
        for i in range(n):
            ph = max(0.0, yv[i] - mu - K + ph)
            pl = max(0.0, mu - K - yv[i] + pl)
            hi[i] = ph > H
            lo[i] = pl > H
    elif m == "ewma":
        lam, om, L = 0.2, 0.8, 3.0
        fac = lam / (2.0 - lam)
        prev = mu
        for i in range(n):
            prev = lam * yv[i] + om * prev
            w = np.sqrt(fac * (1.0 - om ** (2 * (i + 1))))
            hi[i] = prev > mu + L * sig * w
            lo[i] = prev < mu - L * sig * w
    else:
        ucl, lcl = mu + 3 * sig, mu - 3 * sig
        side = np.sign(yv - mu)
        rid = (side != pd.Series(side).shift()).cumsum()
        rlen = pd.Series(side).groupby(rid).transform("size").to_numpy()
        run = (rlen >= 8) & (side != 0)
        hi = (yv > ucl) | (run & (side > 0))
        lo = (yv < lcl) | (run & (side < 0))
    t = np.arange(1, n + 1, dtype="float64")
    return pd.DataFrame({
        "t": t,
        "value": yv,
        "method": np.full(n, m),
        "is_shift": (hi | lo).astype("float64"),
        "is_high": hi.astype("float64"),
        "is_low": lo.astype("float64"),
    })

"process_shift_detection(data, method='cusum', headers=False)"
