# Name: c_chart
# Description: c chart for defect counts (equal opportunity).
# Parameters: defects, plot=False, title='c chart', headers=False

def c_chart(defects, plot=False, title="c chart", headers=False):
    """c chart for the count of defects per inspection unit.

    CL = c-bar, UCL/LCL = c-bar ± 3√c-bar. LCL is floored at 0.
    Equal area of opportunity. plot=True is a chart (Python object).

    defects: count column, ref string, Series, DataFrame, or list.
    headers: first row is headers when defects is a ref string.
    """
    if isinstance(defects, str):
        defects = xl(defects, headers=headers)
    if isinstance(defects, pd.DataFrame):
        numeric = defects.select_dtypes(include="number")
        values = (numeric.iloc[:, 0] if numeric.shape[1]
                  else defects.iloc[:, 0])
    elif isinstance(defects, pd.Series):
        values = defects
    else:
        values = pd.Series(defects)
    y = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce")
    y = y.replace("", np.nan).dropna().reset_index(drop=True)
    k = int(y.size)
    if k < 2:
        raise ValueError("Need at least 2 numeric values.")
    yv = y.to_numpy(dtype="float64")
    if np.any(yv < 0):
        raise ValueError("defects must be >= 0.")
    if not isinstance(plot, bool):
        plot = bool(pd.Series(plot).iloc[0])
    title = str(pd.Series(title).iloc[0])
    cb = float(np.mean(yv))
    se = 0.0 if cb == 0 else float(np.sqrt(cb))
    cl = cb
    ucl = cb + 3.0 * se
    lcl = max(0.0, cb - 3.0 * se)
    out = (yv > ucl) | (yv < lcl)
    t = np.arange(1, k + 1, dtype="float64")
    if plot:
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(t, yv, color="#2b5c8f", lw=1.5, marker="o", ms=4, zorder=3)
        if out.any():
            ax.scatter(t[out], yv[out], c="#d9534f", s=70, zorder=5,
                       edgecolors="k", label="Beyond limits")
            ax.legend(loc="best", fontsize=8)
        ax.axhline(cl, color="#1f77b4", lw=1.5)
        ax.axhline(ucl, color="#d9534f", ls="--", lw=1.2)
        ax.axhline(lcl, color="#d9534f", ls="--", lw=1.2)
        ax.set_ylabel("c")
        ax.set_xlabel("t")
        ax.grid(True, ls=":", alpha=0.5)
        fig.suptitle(title, fontsize=12, fontweight="bold")
        fig.tight_layout()
        return fig
    return pd.DataFrame({
        "t": t,
        "defects": yv,
        "cl": np.full(k, cl),
        "ucl": np.full(k, ucl),
        "lcl": np.full(k, lcl),
        "is_outlier": out.astype("float64"),
    })

"c_chart(defects, plot=False, title='c chart', headers=False)"
