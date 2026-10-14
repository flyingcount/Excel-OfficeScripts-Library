# Name: xmr
# Description: Individuals and moving-range (XmR) SPC limits; table or two-panel chart.
# Parameters: data, dates=None, plot=False, title='XmR chart', headers=False

def xmr(data, dates=None, plot=False, title="XmR chart", headers=False):
    """XmR (individuals + moving range) process-control chart.

    plot=False spills a table. plot=True returns a two-panel figure
    (X on top, MR below). Leave that PY cell as a Python object.

    data: value column, ref string, Series, or DataFrame (first numeric col).
    dates: optional x-axis (range ref, Series, or list). Pass data['Date'],
        not the header string 'Date'.
    plot: False (default) table; True chart.
    title: figure title when plot=True.
    headers: first row is headers when data or dates is a ref string.

    Limits use d2=1.128 and D4=3.267 (n=2). LCL is not floored at 0.
    An 8+ point run on one side of X-bar is a shift: CL/UCL/LCL and MR
    limits are recomputed on each regime. Need at least 2 numeric values.
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
    y = y.reset_index(drop=True)
    x_date = None
    if dates is not None:
        if isinstance(dates, str):
            dates = xl(dates, headers=headers)
        if isinstance(dates, pd.DataFrame):
            x_date = dates.iloc[:, 0]
        else:
            x_date = pd.Series(dates)
        x_date = pd.Series(x_date).reset_index(drop=True)
        n0 = min(len(y), len(x_date))
        y, x_date = y.iloc[:n0], x_date.iloc[:n0]
        keep = y.notna() & x_date.notna()
        y = y[keep].reset_index(drop=True)
        x_date = x_date[keep].reset_index(drop=True)
    else:
        y = y.dropna().reset_index(drop=True)
    n = int(y.size)
    if n < 2:
        raise ValueError("Need at least 2 numeric values.")
    if not isinstance(plot, bool):
        plot = bool(pd.Series(plot).iloc[0])
    title = str(pd.Series(title).iloc[0])

    yv = y.to_numpy(dtype="float64")
    mrv = pd.Series(yv).diff().abs().to_numpy(dtype="float64")
    cl0 = float(np.mean(yv))
    side = np.sign(yv - cl0)
    run_id = (side != pd.Series(side).shift()).cumsum()
    run_len = pd.Series(side).groupby(run_id).transform("size").to_numpy()
    is_shift = (run_len >= 8) & (side != 0)
    rid = np.asarray(run_id)
    cuts = [0] + [
        i for i in range(1, n)
        if rid[i] != rid[i - 1] and (is_shift[i] or is_shift[i - 1])] + [n]

    def lims(seg):
        c = float(np.mean(seg))
        if len(seg) < 2:
            return (c, c, c, 0.0, 0.0, 0.0)
        mrb = float(np.mean(np.abs(np.diff(seg))))
        sig = 0.0 if (not np.isfinite(mrb) or mrb == 0) else mrb / 1.128
        return (c, c + 3 * sig, c - 3 * sig, mrb, 3.267 * mrb, 0.0)

    cl_arr = np.empty(n)
    ucl_arr = np.empty(n)
    lcl_arr = np.empty(n)
    mr_cl_arr = np.empty(n)
    mr_ucl_arr = np.empty(n)
    mr_lcl_arr = np.empty(n)
    prev = lims(yv)
    for a, b in zip(cuts[:-1], cuts[1:]):
        if b - a >= 2:
            prev = lims(yv[a:b])
        c, u, lo, mc, mu, ml = prev
        cl_arr[a:b] = c
        ucl_arr[a:b] = u
        lcl_arr[a:b] = lo
        mr_cl_arr[a:b] = mc
        mr_ucl_arr[a:b] = mu
        mr_lcl_arr[a:b] = ml
    out_x = (yv > ucl_arr) | (yv < lcl_arr)
    out_mr = np.zeros(n, dtype=bool)
    out_mr[1:] = mrv[1:] > mr_ucl_arr[1:]

    t = np.arange(1, n + 1, dtype="float64")
    if plot:
        xp = t if x_date is None else x_date.to_numpy()
        fig, (ax0, ax1) = plt.subplots(
            2, 1, sharex=True, figsize=(10, 6),
            gridspec_kw={"height_ratios": [2, 1]})
        if (cl_arr == cl_arr[0]).all():
            sig = (ucl_arr[0] - cl_arr[0]) / 3.0
            z1, z2 = sig, 2 * sig
            c0, u0, l0 = cl_arr[0], ucl_arr[0], lcl_arr[0]
            ax0.axhspan(c0 - z1, c0 + z1, color="#eef7ee", alpha=0.6, zorder=0)
            ax0.axhspan(c0 - z2, c0 - z1, color="#fff9e6", alpha=0.6, zorder=0)
            ax0.axhspan(c0 + z1, c0 + z2, color="#fff9e6", alpha=0.6, zorder=0)
            ax0.axhspan(l0, c0 - z2, color="#fde8e8", alpha=0.5, zorder=0)
            ax0.axhspan(c0 + z2, u0, color="#fde8e8", alpha=0.5, zorder=0)
        ax0.plot(xp, yv, color="#2b5c8f", lw=1.5, marker="o", ms=4, zorder=3)
        if out_x.any():
            ax0.scatter(xp[out_x], yv[out_x], c="#d9534f", s=70, zorder=5,
                        edgecolors="k", label="X beyond 3σ")
        if is_shift.any():
            ax0.scatter(xp[is_shift], yv[is_shift], c="#f0ad4e", s=55, zorder=4,
                        edgecolors="k", label="Shift (8+ run)")
        kw = dict(drawstyle="steps-pre", zorder=2)
        ax0.plot(xp, cl_arr, color="#1f77b4", lw=1.5, **kw)
        ax0.plot(xp, ucl_arr, color="#d9534f", ls="--", lw=1.2, **kw)
        ax0.plot(xp, lcl_arr, color="#d9534f", ls="--", lw=1.2, **kw)
        ax0.set_ylabel("X")
        ax0.set_title("Individuals")
        ax0.grid(True, ls=":", alpha=0.5)
        if out_x.any() or is_shift.any():
            ax0.legend(loc="best", fontsize=8)
        ax1.plot(xp, mrv, color="#2b5c8f", lw=1.5, marker="o", ms=4, zorder=3)
        if out_mr.any():
            ax1.scatter(xp[out_mr], mrv[out_mr], c="#d9534f", s=70, zorder=5,
                        edgecolors="k", label="MR beyond UCL")
            ax1.legend(loc="best", fontsize=8)
        ax1.plot(xp, mr_cl_arr, color="#1f77b4", lw=1.5, **kw)
        ax1.plot(xp, mr_ucl_arr, color="#d9534f", ls="--", lw=1.2, **kw)
        ax1.plot(xp, mr_lcl_arr, color="#d9534f", ls="--", lw=1.2, **kw)
        ax1.set_ylabel("MR")
        ax1.set_title("Moving range")
        ax1.grid(True, ls=":", alpha=0.5)
        if x_date is not None:
            fig.autofmt_xdate(rotation=45)
        fig.suptitle(title, fontsize=12, fontweight="bold")
        fig.tight_layout()
        return fig

    out = pd.DataFrame({
        "t": t,
        "value": yv,
        "mr": mrv,
        "cl": cl_arr,
        "ucl": ucl_arr,
        "lcl": lcl_arr,
        "mr_cl": mr_cl_arr,
        "mr_ucl": mr_ucl_arr,
        "mr_lcl": mr_lcl_arr,
        "is_outlier": out_x.astype("float64"),
        "is_shift": is_shift.astype("float64"),
        "is_mr_outlier": out_mr.astype("float64"),
    })
    if x_date is not None:
        out.insert(1, "date", x_date.to_numpy())
    return out

"xmr(data, dates=None, plot=False, title='XmR chart', headers=False)"
