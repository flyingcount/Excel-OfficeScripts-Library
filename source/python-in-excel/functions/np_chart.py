# Name: np_chart
# Description: np chart for number of defectives (binomial).
# Parameters: defectives, sample_size, plot=False, title='np chart', headers=False

def np_chart(defectives, sample_size, plot=False, title="np chart",
             headers=False):
    """np chart for the count of defective items.

    p-bar = Σd / Σn, CL_i = n_i * p-bar,
    UCL/LCL_i = n_i p-bar ± 3√(n_i p-bar(1-p-bar)).
    LCL is floored at 0; UCL is capped at n_i. Constant n is usual.
    sample_size may be a column or a scalar. plot=True is a chart
    (Python object).

    defectives, sample_size: columns, ref strings, Series, or lists.
    headers: first row is headers when a ref string is used.
    """
    def vec(x):
        if isinstance(x, str):
            x = xl(x, headers=headers)
        if isinstance(x, pd.DataFrame):
            num = x.select_dtypes(include="number")
            x = num.iloc[:, 0] if num.shape[1] else x.iloc[:, 0]
        elif not isinstance(x, pd.Series):
            x = pd.Series(x)
        s = pd.to_numeric(pd.Series(x).squeeze(), errors="coerce")
        return pd.Series(s).replace("", np.nan).reset_index(drop=True)

    d = vec(defectives)
    n = vec(sample_size)
    if int(n.size) == 1:
        d = d.dropna().reset_index(drop=True)
        nv = np.full(int(d.size), float(n.iloc[0]))
        dv = d.to_numpy(dtype="float64")
    else:
        k0 = min(int(d.size), int(n.size))
        d, n = d.iloc[:k0], n.iloc[:k0]
        keep = d.notna() & n.notna()
        d, n = d[keep].reset_index(drop=True), n[keep].reset_index(drop=True)
        dv = d.to_numpy(dtype="float64")
        nv = n.to_numpy(dtype="float64")
    k = int(dv.size)
    if k < 2:
        raise ValueError("Need at least 2 numeric values.")
    if np.any(dv < 0):
        raise ValueError("defectives must be >= 0.")
    if np.any(nv <= 0):
        raise ValueError("sample_size must be > 0.")
    if np.any(dv > nv):
        raise ValueError("defectives cannot exceed sample_size.")
    if not isinstance(plot, bool):
        plot = bool(pd.Series(plot).iloc[0])
    title = str(pd.Series(title).iloc[0])
    pb = float(dv.sum() / nv.sum())
    cl = nv * pb
    se = (np.sqrt(nv * pb * (1.0 - pb)) if 0 < pb < 1
          else np.zeros(k))
    ucl = np.minimum(nv, cl + 3.0 * se)
    lcl = np.maximum(0.0, cl - 3.0 * se)
    out = (dv > ucl) | (dv < lcl)
    t = np.arange(1, k + 1, dtype="float64")
    if plot:
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(t, dv, color="#2b5c8f", lw=1.5, marker="o", ms=4, zorder=3)
        if out.any():
            ax.scatter(t[out], dv[out], c="#d9534f", s=70, zorder=5,
                       edgecolors="k", label="Beyond limits")
            ax.legend(loc="best", fontsize=8)
        ax.plot(t, cl, color="#1f77b4", lw=1.5)
        ax.plot(t, ucl, color="#d9534f", ls="--", lw=1.2)
        ax.plot(t, lcl, color="#d9534f", ls="--", lw=1.2)
        ax.set_ylabel("np")
        ax.set_xlabel("t")
        ax.grid(True, ls=":", alpha=0.5)
        fig.suptitle(title, fontsize=12, fontweight="bold")
        fig.tight_layout()
        return fig
    return pd.DataFrame({
        "t": t,
        "defectives": dv,
        "sample_size": nv,
        "cl": cl,
        "ucl": ucl,
        "lcl": lcl,
        "is_outlier": out.astype("float64"),
    })

"np_chart(defectives, sample_size, plot=False, title='np chart', headers=False)"
