# Name: xbar_s
# Description: X-bar and S SPC limits by subgroup; table or two-panel chart.
# Parameters: data, subgroup_size, plot=False, title='X-bar S chart', headers=False

def xbar_s(data, subgroup_size, plot=False, title="X-bar S chart",
           headers=False):
    """X-bar and S process-control chart for rational subgroups.

    plot=False spills one row per subgroup. plot=True returns a two-panel
    figure (X-bar on top, S below). Leave that PY cell as a Python object.

    data: value stream (first numeric column, grouped in time order) or a
        table with at least subgroup_size numeric columns (one subgroup
        per row). Ref string, DataFrame, Series, or list.
    subgroup_size: n = 2 to 25 (Shewhart A3/B3/B4). Prefer n > 10;
        use xbar_r when n is 2 to 10. Incomplete last groups are
        dropped. Need at least 2 complete subgroups.
    plot: False (default) table; True chart.
    title: figure title when plot=True.
    headers: first row is headers when data is a ref string.
    """
    import math
    ns = int(pd.Series(subgroup_size).iloc[0])
    if ns < 2 or ns > 25:
        raise ValueError("subgroup_size must be 2 to 25.")
    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        num = data.select_dtypes(include="number")
        if num.shape[1] == 0:
            num = data
    elif isinstance(data, pd.Series):
        num = data.to_frame()
    else:
        num = pd.DataFrame(data)
    num = num.apply(lambda c: pd.to_numeric(
        pd.Series(c).replace("", np.nan), errors="coerce"))
    if num.shape[1] >= ns:
        mat = num.iloc[:, :ns].dropna(how="any").to_numpy(dtype="float64")
    else:
        y = num.iloc[:, 0].dropna().to_numpy(dtype="float64")
        k0 = int(y.size) // ns
        mat = y[: k0 * ns].reshape(k0, ns) if k0 else np.empty((0, ns))
    k = int(mat.shape[0])
    if k < 2:
        raise ValueError("Need at least 2 complete subgroups.")
    if not isinstance(plot, bool):
        plot = bool(pd.Series(plot).iloc[0])
    title = str(pd.Series(title).iloc[0])
    c4 = (math.sqrt(2.0 / (ns - 1))
          * math.gamma(ns / 2.0) / math.gamma((ns - 1) / 2.0))
    a3 = 3.0 / (c4 * math.sqrt(ns))
    b = 3.0 * math.sqrt(max(0.0, 1.0 - c4 * c4)) / c4
    b3, b4 = max(0.0, 1.0 - b), 1.0 + b
    xb = mat.mean(axis=1)
    sv = mat.std(axis=1, ddof=1)
    xbb = float(xb.mean())
    sb = float(sv.mean())
    cl, ucl, lcl = xbb, xbb + a3 * sb, xbb - a3 * sb
    scl, su, sl = sb, b4 * sb, b3 * sb
    out_x = (xb > ucl) | (xb < lcl)
    out_s = (sv > su) | (sv < sl)
    t = np.arange(1, k + 1, dtype="float64")
    if plot:
        fig, (ax0, ax1) = plt.subplots(
            2, 1, sharex=True, figsize=(10, 6),
            gridspec_kw={"height_ratios": [2, 1]})
        ax0.plot(t, xb, color="#2b5c8f", lw=1.5, marker="o", ms=4, zorder=3)
        if out_x.any():
            ax0.scatter(t[out_x], xb[out_x], c="#d9534f", s=70, zorder=5,
                        edgecolors="k", label="X-bar beyond limits")
            ax0.legend(loc="best", fontsize=8)
        ax0.axhline(cl, color="#1f77b4", lw=1.5)
        ax0.axhline(ucl, color="#d9534f", ls="--", lw=1.2)
        ax0.axhline(lcl, color="#d9534f", ls="--", lw=1.2)
        ax0.set_ylabel("X-bar")
        ax0.set_title("X-bar")
        ax0.grid(True, ls=":", alpha=0.5)
        ax1.plot(t, sv, color="#2b5c8f", lw=1.5, marker="o", ms=4, zorder=3)
        if out_s.any():
            ax1.scatter(t[out_s], sv[out_s], c="#d9534f", s=70, zorder=5,
                        edgecolors="k", label="S beyond limits")
            ax1.legend(loc="best", fontsize=8)
        ax1.axhline(scl, color="#1f77b4", lw=1.5)
        ax1.axhline(su, color="#d9534f", ls="--", lw=1.2)
        ax1.axhline(sl, color="#d9534f", ls="--", lw=1.2)
        ax1.set_ylabel("S")
        ax1.set_title("Std dev")
        ax1.set_xlabel("Subgroup")
        ax1.grid(True, ls=":", alpha=0.5)
        fig.suptitle(title, fontsize=12, fontweight="bold")
        fig.tight_layout()
        return fig
    return pd.DataFrame({
        "subgroup": t,
        "n": np.full(k, float(ns)),
        "xbar": xb,
        "s": sv,
        "cl": np.full(k, cl),
        "ucl": np.full(k, ucl),
        "lcl": np.full(k, lcl),
        "s_cl": np.full(k, scl),
        "s_ucl": np.full(k, su),
        "s_lcl": np.full(k, sl),
        "is_outlier": out_x.astype("float64"),
        "is_s_outlier": out_s.astype("float64"),
    })

"xbar_s(data, subgroup_size, plot=False, title='X-bar S chart', headers=False)"
