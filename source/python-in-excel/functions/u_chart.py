# Name: u_chart
# Description: u chart for defects per unit (varying n).
# Parameters: defects, units, plot=False, title='u chart', headers=False

def u_chart(defects, units, plot=False, title="u chart", headers=False):
    """u chart for defects per unit.

    u_i = c_i / n_i, CL = Σc / Σn,
    UCL/LCL_i = ū ± 3√(ū / n_i). LCL is floored at 0.
    units may be a column or a scalar (constant n).
    plot=True is a chart (Python object).

    defects, units: columns, ref strings, Series, DataFrame, or lists.
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

    c = vec(defects)
    u = vec(units)
    if int(u.size) == 1:
        c = c.dropna().reset_index(drop=True)
        nv = np.full(int(c.size), float(u.iloc[0]))
        cv = c.to_numpy(dtype="float64")
    else:
        k0 = min(int(c.size), int(u.size))
        c, u = c.iloc[:k0], u.iloc[:k0]
        keep = c.notna() & u.notna()
        c, u = c[keep].reset_index(drop=True), u[keep].reset_index(drop=True)
        cv = c.to_numpy(dtype="float64")
        nv = u.to_numpy(dtype="float64")
    k = int(cv.size)
    if k < 2:
        raise ValueError("Need at least 2 numeric values.")
    if np.any(cv < 0):
        raise ValueError("defects must be >= 0.")
    if np.any(nv <= 0):
        raise ValueError("units must be > 0.")
    if not isinstance(plot, bool):
        plot = bool(pd.Series(plot).iloc[0])
    title = str(pd.Series(title).iloc[0])
    ub = float(cv.sum() / nv.sum())
    se = np.sqrt(ub / nv) if ub > 0 else np.zeros(k)
    cl = np.full(k, ub)
    ucl = cl + 3.0 * se
    lcl = np.maximum(0.0, cl - 3.0 * se)
    uv = cv / nv
    out = (uv > ucl) | (uv < lcl)
    t = np.arange(1, k + 1, dtype="float64")
    if plot:
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(t, uv, color="#2b5c8f", lw=1.5, marker="o", ms=4, zorder=3)
        if out.any():
            ax.scatter(t[out], uv[out], c="#d9534f", s=70, zorder=5,
                       edgecolors="k", label="Beyond limits")
            ax.legend(loc="best", fontsize=8)
        ax.plot(t, cl, color="#1f77b4", lw=1.5)
        ax.plot(t, ucl, color="#d9534f", ls="--", lw=1.2)
        ax.plot(t, lcl, color="#d9534f", ls="--", lw=1.2)
        ax.set_ylabel("u")
        ax.set_xlabel("t")
        ax.grid(True, ls=":", alpha=0.5)
        fig.suptitle(title, fontsize=12, fontweight="bold")
        fig.tight_layout()
        return fig
    return pd.DataFrame({
        "t": t,
        "defects": cv,
        "units": nv,
        "u": uv,
        "cl": cl,
        "ucl": ucl,
        "lcl": lcl,
        "is_outlier": out.astype("float64"),
    })

"u_chart(defects, units, plot=False, title='u chart', headers=False)"
