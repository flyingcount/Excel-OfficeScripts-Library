# Name: ewma
# Description: EWMA control chart; table or chart.
# Parameters: data, lambda_=0.2, l=3, plot=False, title='EWMA chart', headers=False

def ewma(data, lambda_=0.2, l=3, plot=False, title="EWMA chart",
         headers=False):
    """EWMA process-control chart for individuals.

    z_t = lambda_ * x_t + (1-lambda_) * z_{t-1}, starting at x-bar.
    Limits use L * sigma * sqrt(lambda_/(2-lambda_) * (1-(1-lambda_)^{2t})).
    sigma is MR-bar / 1.128. plot=True is a chart (Python object).

    data: value column, ref string, Series, DataFrame, or list.
    lambda_: EWMA weight in (0, 1]. Default 0.2.
    l: width of the limits in sigma units. Default 3.
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
    lam = float(pd.Series(lambda_).iloc[0])
    L = float(pd.Series(l).iloc[0])
    if not 0 < lam <= 1:
        raise ValueError("lambda_ must be in (0, 1].")
    if L <= 0:
        raise ValueError("l must be > 0.")
    if not isinstance(plot, bool):
        plot = bool(pd.Series(plot).iloc[0])
    title = str(pd.Series(title).iloc[0])
    yv = y.to_numpy(dtype="float64")
    mu = float(np.mean(yv))
    mrb = float(np.mean(np.abs(np.diff(yv))))
    sig = 0.0 if mrb == 0 else mrb / 1.128
    om = 1.0 - lam
    fac = lam / (2.0 - lam)
    z = np.empty(n)
    ucl = np.empty(n)
    lcl = np.empty(n)
    prev = mu
    for i in range(n):
        prev = lam * yv[i] + om * prev
        z[i] = prev
        w = np.sqrt(fac * (1.0 - om ** (2 * (i + 1))))
        ucl[i] = mu + L * sig * w
        lcl[i] = mu - L * sig * w
    out = (z > ucl) | (z < lcl)
    t = np.arange(1, n + 1, dtype="float64")
    if plot:
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(t, z, color="#2b5c8f", lw=1.5, marker="o", ms=4, zorder=3)
        if out.any():
            ax.scatter(t[out], z[out], c="#d9534f", s=70, zorder=5,
                       edgecolors="k", label="Beyond limits")
            ax.legend(loc="best", fontsize=8)
        ax.plot(t, np.full(n, mu), color="#1f77b4", lw=1.5)
        ax.plot(t, ucl, color="#d9534f", ls="--", lw=1.2)
        ax.plot(t, lcl, color="#d9534f", ls="--", lw=1.2)
        ax.set_ylabel("EWMA")
        ax.set_xlabel("t")
        ax.grid(True, ls=":", alpha=0.5)
        fig.suptitle(title, fontsize=12, fontweight="bold")
        fig.tight_layout()
        return fig
    return pd.DataFrame({
        "t": t,
        "value": yv,
        "ewma": z,
        "cl": np.full(n, mu),
        "ucl": ucl,
        "lcl": lcl,
        "is_outlier": out.astype("float64"),
    })

"ewma(data, lambda_=0.2, l=3, plot=False, title='EWMA chart', headers=False)"
