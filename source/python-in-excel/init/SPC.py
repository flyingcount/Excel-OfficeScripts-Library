# Python in Excel SPC library
#
# Formulas → Initialization → replace the editor contents with this file → Save.
# This file is a complete Initialization: Excel defaults, then SPC functions only.
# After Save, call contents() in a PY cell for the public function list.
#
# General (non-SPC) functions: paste init/PaulPythonLibrary.py instead.
# Sampling functions only: paste init/Sampling.py instead.
# Time series functions only: paste init/TimeSeries.py instead.
# Restore defaults only: paste init/DefaultInitialization.py instead.
#
# Requires Microsoft 365 Python in Excel. Functions use Excel's xl() helper.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels as sm
import excel
import warnings

warnings.simplefilter('ignore')

excel.set_xl_scalar_conversion(excel.convert_to_scalar)
excel.set_xl_array_conversion(excel.convert_to_dataframe)


def contents():
    """List SPC functions in this Initialization.

    Result spills as function / description / call. A readable description is
    enough when it already says what the function does. call matches the
    quoted signature after each def.
    """
    return pd.DataFrame(
        [
            ("contents", "List library functions", "contents()"),
            ("xmr", "XmR individuals and moving-range chart", "xmr(data, dates=None, plot=False, title='XmR chart', headers=False)"),
            ("xbar_r", "X-bar and R chart for rational subgroups", "xbar_r(data, subgroup_size, plot=False, title='X-bar R chart', headers=False)"),
            ("xbar_s", "X-bar and S chart for rational subgroups", "xbar_s(data, subgroup_size, plot=False, title='X-bar S chart', headers=False)"),
            ("ewma", "EWMA chart for individuals", "ewma(data, lambda_=0.2, l=3, plot=False, title='EWMA chart', headers=False)"),
            ("cusum", "Two-sided tabular CUSUM", "cusum(data, k=0.5, h=5, plot=False, title='CUSUM chart', headers=False)"),
            ("capability_report", "Cp, Cpk, Pp, Ppk and expected PPM", "capability_report(data, usl, lsl, headers=False)"),
            ("process_shift_detection", "Flag mean shifts (CUSUM, EWMA, or XmR)", "process_shift_detection(data, method='cusum', headers=False)"),
            ("nelson_rules", "Nelson's eight tests for individuals", "nelson_rules(data, headers=False)"),
            ("c_chart", "c chart for defect counts", "c_chart(defects, plot=False, title='c chart', headers=False)"),
            ("u_chart", "u chart for defects per unit", "u_chart(defects, units, plot=False, title='u chart', headers=False)"),
            ("p_chart", "p chart for fraction defective", "p_chart(defectives, sample_size, plot=False, title='p chart', headers=False)"),
            ("np_chart", "np chart for number of defectives", "np_chart(defectives, sample_size, plot=False, title='np chart', headers=False)"),
        ],
        columns=["function", "description", "call"],
    )

"contents()"


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


def xbar_r(data, subgroup_size, plot=False, title="X-bar R chart",
           headers=False):
    """X-bar and R process-control chart for rational subgroups.

    plot=False spills one row per subgroup. plot=True returns a two-panel
    figure (X-bar on top, R below). Leave that PY cell as a Python object.

    data: value stream (first numeric column, grouped in time order) or a
        table with at least subgroup_size numeric columns (one subgroup
        per row). Ref string, DataFrame, Series, or list.
    subgroup_size: n = 2 to 10 (Shewhart A2/D3/D4). Incomplete last
        groups are dropped. Need at least 2 complete subgroups.
    plot: False (default) table; True chart.
    title: figure title when plot=True.
    headers: first row is headers when data is a ref string.
    """
    ns = int(pd.Series(subgroup_size).iloc[0])
    if ns < 2 or ns > 10:
        raise ValueError("subgroup_size must be 2 to 10.")
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
    a2 = (0, 0, 1.880, 1.023, 0.729, 0.577, 0.483, 0.419, 0.373, 0.337, 0.308)
    d3 = (0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.076, 0.136, 0.184, 0.223)
    d4 = (0, 0, 3.267, 2.574, 2.282, 2.114, 2.004, 1.924, 1.864, 1.816, 1.777)
    xb = mat.mean(axis=1)
    rv = mat.max(axis=1) - mat.min(axis=1)
    xbb = float(xb.mean())
    rb = float(rv.mean())
    cl, ucl, lcl = xbb, xbb + a2[ns] * rb, xbb - a2[ns] * rb
    rcl, ru, rl = rb, d4[ns] * rb, d3[ns] * rb
    out_x = (xb > ucl) | (xb < lcl)
    out_r = (rv > ru) | (rv < rl)
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
        ax1.plot(t, rv, color="#2b5c8f", lw=1.5, marker="o", ms=4, zorder=3)
        if out_r.any():
            ax1.scatter(t[out_r], rv[out_r], c="#d9534f", s=70, zorder=5,
                        edgecolors="k", label="R beyond limits")
            ax1.legend(loc="best", fontsize=8)
        ax1.axhline(rcl, color="#1f77b4", lw=1.5)
        ax1.axhline(ru, color="#d9534f", ls="--", lw=1.2)
        ax1.axhline(rl, color="#d9534f", ls="--", lw=1.2)
        ax1.set_ylabel("R")
        ax1.set_title("Range")
        ax1.set_xlabel("Subgroup")
        ax1.grid(True, ls=":", alpha=0.5)
        fig.suptitle(title, fontsize=12, fontweight="bold")
        fig.tight_layout()
        return fig
    return pd.DataFrame({
        "subgroup": t,
        "n": np.full(k, float(ns)),
        "xbar": xb,
        "r": rv,
        "cl": np.full(k, cl),
        "ucl": np.full(k, ucl),
        "lcl": np.full(k, lcl),
        "r_cl": np.full(k, rcl),
        "r_ucl": np.full(k, ru),
        "r_lcl": np.full(k, rl),
        "is_outlier": out_x.astype("float64"),
        "is_r_outlier": out_r.astype("float64"),
    })

"xbar_r(data, subgroup_size, plot=False, title='X-bar R chart', headers=False)"


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


def capability_report(data, usl, lsl, headers=False):
    """Process capability for individuals (Cp, Cpk, Pp, Ppk, PPM).

    Spills one row: mean, stdev_within (MR-bar / 1.128), stdev_overall
    (sample s), cp, cpk, pp, ppk, and expected overall ppm (normal).
    Need at least 2 numeric values. usl must be > lsl.

    data: value column, ref string, Series, DataFrame, or list.
    headers: first row is headers when data is a ref string.
    """
    import math
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
    u = float(pd.Series(usl).iloc[0])
    lo = float(pd.Series(lsl).iloc[0])
    if not np.isfinite(u) or not np.isfinite(lo):
        raise ValueError("usl and lsl must be numeric.")
    if u <= lo:
        raise ValueError("usl must be > lsl.")
    yv = y.to_numpy(dtype="float64")
    mu = float(np.mean(yv))
    so = float(np.std(yv, ddof=1))
    mrb = float(np.mean(np.abs(np.diff(yv))))
    sw = 0.0 if mrb == 0 else mrb / 1.128
    spread = u - lo

    def idx6(sig):
        if sig == 0:
            return np.nan
        return spread / (6.0 * sig)

    def idxk(sig):
        if sig == 0:
            return np.nan
        return min((u - mu) / (3.0 * sig), (mu - lo) / (3.0 * sig))

    if so == 0:
        ppm = 0.0 if lo <= mu <= u else 1e6
    else:
        def ncdf(z):
            return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))
        ppm = 1e6 * (ncdf((lo - mu) / so) + (1.0 - ncdf((u - mu) / so)))
    return pd.DataFrame({
        "mean": [mu],
        "stdev_within": [sw],
        "stdev_overall": [so],
        "cp": [idx6(sw)],
        "cpk": [idxk(sw)],
        "pp": [idx6(so)],
        "ppk": [idxk(so)],
        "ppm": [float(ppm)],
    })

"capability_report(data, usl, lsl, headers=False)"


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


def nelson_rules(data, headers=False):
    """Nelson's eight tests on individuals (mean and MR-bar / 1.128).

    Flags the point that completes each pattern. One row per value.
    Rule column headers include a brief explanation. Need at least
    2 numeric values.

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
    yv = y.to_numpy(dtype="float64")
    mu = float(np.mean(yv))
    mrb = float(np.mean(np.abs(np.diff(yv))))
    sig = 0.0 if mrb == 0 else mrb / 1.128
    z = np.zeros(n) if sig == 0 else (yv - mu) / sig
    side = np.sign(z)

    def wflag(mask, w, k):
        out = np.zeros(n, dtype=bool)
        if n >= w:
            c = np.convolve(np.asarray(mask, dtype="float64"),
                            np.ones(w), "valid")
            out[w - 1:] = c >= k
        return out

    rid = (side != pd.Series(side).shift()).cumsum()
    pos = pd.Series(side).groupby(rid).cumcount().to_numpy() + 1
    r2 = (pos >= 9) & (side != 0)
    r3 = np.zeros(n, dtype=bool)
    r4 = np.zeros(n, dtype=bool)
    d = np.diff(yv)
    if n >= 6:
        c = np.convolve((d > 0).astype("float64"), np.ones(5), "valid")
        e = np.convolve((d < 0).astype("float64"), np.ones(5), "valid")
        r3[5:] = (c == 5) | (e == 5)
    if n >= 14:
        s = np.sign(d)
        alt = (s[:-1] != 0) & (s[1:] == -s[:-1])
        c = np.convolve(alt.astype("float64"), np.ones(12), "valid")
        r4[13:] = c == 12
    rules = np.column_stack([
        np.abs(z) > 3,
        r2,
        r3,
        r4,
        wflag(z > 2, 3, 2) | wflag(z < -2, 3, 2),
        wflag(z > 1, 5, 4) | wflag(z < -1, 5, 4),
        wflag(np.abs(z) < 1, 15, 15),
        wflag(np.abs(z) > 1, 8, 8),
    ])
    notes = (
        "One point beyond 3σ",
        "Nine in a row on the same side of x̄",
        "Six in a row steadily up or down",
        "Fourteen alternating up and down",
        "Two of three beyond 2σ, same side",
        "Four of five beyond 1σ, same side",
        "Fifteen in a row within 1σ",
        "Eight in a row beyond 1σ",
    )
    t = np.arange(1, n + 1, dtype="float64")
    out = pd.DataFrame(
        rules.astype("float64"),
        columns=[f"rule_{i}: {notes[i - 1]}" for i in range(1, 9)],
    )
    out.insert(0, "value", yv)
    out.insert(0, "t", t)
    out["n_rules"] = rules.sum(axis=1).astype("float64")
    out["is_signal"] = (out["n_rules"] > 0).astype("float64")
    return out

"nelson_rules(data, headers=False)"


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


def p_chart(defectives, sample_size, plot=False, title="p chart",
            headers=False):
    """p chart for the fraction of defective items.

    p_i = d_i / n_i, p-bar = Σd / Σn,
    UCL/LCL_i = p-bar ± 3√(p-bar(1-p-bar)/n_i).
    LCL is floored at 0; UCL is capped at 1.
    sample_size may be a column or a scalar (constant n).
    plot=True is a chart (Python object).

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
    se = (np.sqrt(pb * (1.0 - pb) / nv) if 0 < pb < 1
          else np.zeros(k))
    cl = np.full(k, pb)
    ucl = np.minimum(1.0, cl + 3.0 * se)
    lcl = np.maximum(0.0, cl - 3.0 * se)
    pv = dv / nv
    out = (pv > ucl) | (pv < lcl)
    t = np.arange(1, k + 1, dtype="float64")
    if plot:
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(t, pv, color="#2b5c8f", lw=1.5, marker="o", ms=4, zorder=3)
        if out.any():
            ax.scatter(t[out], pv[out], c="#d9534f", s=70, zorder=5,
                       edgecolors="k", label="Beyond limits")
            ax.legend(loc="best", fontsize=8)
        ax.plot(t, cl, color="#1f77b4", lw=1.5)
        ax.plot(t, ucl, color="#d9534f", ls="--", lw=1.2)
        ax.plot(t, lcl, color="#d9534f", ls="--", lw=1.2)
        ax.set_ylabel("p")
        ax.set_xlabel("t")
        ax.grid(True, ls=":", alpha=0.5)
        fig.suptitle(title, fontsize=12, fontweight="bold")
        fig.tight_layout()
        return fig
    return pd.DataFrame({
        "t": t,
        "defectives": dv,
        "sample_size": nv,
        "p": pv,
        "cl": cl,
        "ucl": ucl,
        "lcl": lcl,
        "is_outlier": out.astype("float64"),
    })

"p_chart(defectives, sample_size, plot=False, title='p chart', headers=False)"


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
