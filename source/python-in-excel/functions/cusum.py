# Name: cusum
# Description: Two-sided tabular CUSUM; table or chart.
# Parameters: data, k=0.5, h=5, plot=False, title='CUSUM chart', headers=False

def cusum(data, k=0.5, h=5, plot=False, title="CUSUM chart", headers=False):
    """Two-sided tabular CUSUM for individuals.

    S+_t = max(0, x_t - mu - k*sigma + S+_{t-1})
    S-_t = max(0, mu - k*sigma - x_t + S-_{t-1})
    Signal when S+ or S- exceeds h*sigma. sigma is MR-bar / 1.128.
    k and h are in sigma units (defaults 0.5 and 5). plot=True is a
    chart of S+ and -S- with ±h*sigma (Python object).

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
    kv = float(pd.Series(k).iloc[0])
    hv = float(pd.Series(h).iloc[0])
    if kv <= 0:
        raise ValueError("k must be > 0.")
    if hv <= 0:
        raise ValueError("h must be > 0.")
    if not isinstance(plot, bool):
        plot = bool(pd.Series(plot).iloc[0])
    title = str(pd.Series(title).iloc[0])
    yv = y.to_numpy(dtype="float64")
    mu = float(np.mean(yv))
    mrb = float(np.mean(np.abs(np.diff(yv))))
    sig = 0.0 if mrb == 0 else mrb / 1.128
    K, H = kv * sig, hv * sig
    sh = np.empty(n)
    sl = np.empty(n)
    ph = pl = 0.0
    for i in range(n):
        ph = max(0.0, yv[i] - mu - K + ph)
        pl = max(0.0, mu - K - yv[i] + pl)
        sh[i] = ph
        sl[i] = pl
    hi = sh > H
    lo = sl > H
    t = np.arange(1, n + 1, dtype="float64")
    if plot:
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(t, sh, color="#d9534f", lw=1.5, marker="o", ms=4, label="S+")
        ax.plot(t, -sl, color="#2b5c8f", lw=1.5, marker="o", ms=4, label="S-")
        ax.axhline(H, color="#d9534f", ls="--", lw=1.2)
        ax.axhline(-H, color="#2b5c8f", ls="--", lw=1.2)
        ax.axhline(0.0, color="#1f77b4", lw=1.0)
        ax.set_ylabel("CUSUM")
        ax.set_xlabel("t")
        ax.legend(loc="best", fontsize=8)
        ax.grid(True, ls=":", alpha=0.5)
        fig.suptitle(title, fontsize=12, fontweight="bold")
        fig.tight_layout()
        return fig
    return pd.DataFrame({
        "t": t,
        "value": yv,
        "s_high": sh,
        "s_low": sl,
        "h_limit": np.full(n, H),
        "is_high": hi.astype("float64"),
        "is_low": lo.astype("float64"),
    })

"cusum(data, k=0.5, h=5, plot=False, title='CUSUM chart', headers=False)"
