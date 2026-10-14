# Name: breakpoints
# Description: Structural breaks via CUSUM, Chow, or Bai-Perron. plot=True for a chart.
# Parameters: data, method='cusum', alpha=0.05, at=None, nbreaks=None, plot=False, headers=True, date_col=None

def breakpoints(data, method="cusum", alpha=0.05, at=None, nbreaks=None,
                plot=False, headers=True, date_col=None):
    """break_date, confidence (1-p), type (Level shift / Trend shift).

    Monthly YYYY-MM; else YYYY-MM-DD or 1-based t. plot=True is a chart.
    """
    from scipy.stats import f as fdist
    from statsmodels.stats.diagnostic import breaks_cusumolsresid
    from statsmodels.regression.linear_model import OLS

    dates = None
    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        if date_col is not None:
            key = str(pd.Series(date_col).iloc[0]).strip().lower()
            cmap = {str(c).strip().lower(): c for c in data.columns}
            dates = pd.to_datetime(data[cmap.get(key, date_col)], errors="coerce")
        else:
            for col in data.columns:
                s = data[col]
                if pd.api.types.is_numeric_dtype(s):
                    continue
                p = pd.to_datetime(s, errors="coerce")
                if pd.api.types.is_datetime64_any_dtype(s) or float(p.notna().mean()) > 0.8:
                    dates = p
                    break
        num = data.select_dtypes(include="number")
        values = num.iloc[:, 0] if num.shape[1] else data.iloc[:, 0]
    else:
        values = data
    y = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce").reset_index(drop=True)
    if dates is not None:
        dates = pd.to_datetime(pd.Series(dates).reset_index(drop=True), errors="coerce")
        ok = y.notna()
        dates, y = dates[ok].reset_index(drop=True), y[ok].reset_index(drop=True)
    else:
        y = y.dropna().reset_index(drop=True)
    y = y.to_numpy(dtype="float64")
    n = int(y.size)
    if n < 10:
        raise ValueError("Need 10+ observations.")
    alpha = float(pd.Series(alpha).iloc[0])
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1.")
    m = str(pd.Series(method).iloc[0]).strip().lower().replace("_", "-")
    if m in ("qlr", "supf", "sup-f"):
        m = "chow"
    if m in ("bp", "bai-perron", "bai perron"):
        m = "baiperron"
    if m not in ("cusum", "chow", "baiperron"):
        raise ValueError("method must be cusum, chow, or baiperron.")
    t = np.arange(1, n + 1, dtype="float64")
    X = np.column_stack([np.ones(n), t])
    monthly = dates is not None and int(dates.notna().sum()) >= 2 and (
        int(dates.dt.to_period("M").nunique()) >= n)

    def ssr(a, b):
        ya, Xa = y[a:b], X[a:b]
        if ya.size < 3:
            return np.nan
        bh = np.linalg.lstsq(Xa, ya, rcond=None)[0]
        e = ya - Xa.dot(bh)
        return float(e.dot(e))

    def chow_f(k):
        sp, s1, s2 = ssr(0, n), ssr(0, k), ssr(k, n)
        dfd = n - 4
        if dfd < 1 or not np.isfinite(s1 + s2) or s1 + s2 <= 0:
            return np.nan, np.nan
        fv = ((sp - s1 - s2) / 2.0) / ((s1 + s2) / dfd)
        return float(fv), float(fdist.sf(fv, 2, dfd))

    def rss_x(Xa):
        if y.size < Xa.shape[1] + 1:
            return np.nan
        bh = np.linalg.lstsq(Xa, y, rcond=None)[0]
        e = y - Xa.dot(bh)
        return float(e.dot(e))

    def kind(k):
        I = (t > k).astype("float64")
        sr, sl = rss_x(X), rss_x(np.c_[X, I])
        st = rss_x(np.c_[X, t * I])
        fl = (sr - sl) * (n - 3) / sl if sl > 0 else np.nan
        ft = (sr - st) * (n - 3) / st if st > 0 else np.nan
        return "Trend shift" if np.isfinite(ft) and (
            not np.isfinite(fl) or ft > fl) else "Level shift"

    def conf(p):
        return "" if not np.isfinite(p) else "%d%%" % int(
            round(100.0 * (1.0 - min(max(float(p), 0.0), 1.0))))

    def label(i):
        if dates is None or not (1 <= i <= n) or pd.isna(dates.iloc[i - 1]):
            return i
        ts = pd.Timestamp(dates.iloc[i - 1])
        return ts.strftime("%Y-%m" if monthly else "%Y-%m-%d")

    breaks, pmap, path, bound = [], {}, None, np.nan
    if m == "cusum":
        resid = np.asarray(OLS(y, X).fit().resid, dtype="float64")
        _st, pval, crit = breaks_cusumolsresid(resid, ddof=2)
        pval = float(pval)
        path = np.cumsum(resid) / np.sqrt(float(resid.dot(resid)))
        bound = float(np.asarray(crit).reshape(-1)[1]) if np.size(crit) > 1 else 1.36
        if pval < alpha:
            k = min(max(int(np.argmax(np.abs(path)) + 1), 3), n - 3)
            breaks, pmap = [k], {k: pval}
    elif m == "chow":
        lo, hi = max(int(0.15 * n), 3), min(int(np.ceil(0.85 * n)), n - 3)
        if at is None or at is False:
            best, bk = -np.inf, lo
            for k in range(lo, hi + 1):
                fv, _pv = chow_f(k)
                if np.isfinite(fv) and fv > best:
                    best, bk = fv, k
        else:
            av = float(pd.Series(at).iloc[0])
            bk = int(round(av * n)) if 0 < av < 1 else int(av)
            bk = max(bk, 1)
        _fv, pval = chow_f(bk)
        if np.isfinite(pval) and pval < alpha:
            breaks, pmap = [bk], {bk: pval}
    else:
        max_m = 5 if nbreaks is None or nbreaks is False else max(
            1, int(pd.Series(nbreaks).iloc[0]))
        hlen = max(3, int(0.1 * n))
        max_m = min(max_m, max(0, n // (2 * hlen) - 1))
        if max_m < 1:
            raise ValueError("Too short for Bai-Perron.")
        cs = np.concatenate([[0.0], np.cumsum(y)])
        cs2 = np.concatenate([[0.0], np.cumsum(y * y)])

        def rss(i, j):
            k = j - i
            if k < 1:
                return 0.0
            s = cs[j] - cs[i]
            return float(cs2[j] - cs2[i] - s * s / k)

        inf = 1e300
        F = np.full((max_m + 1, n + 1), inf)
        brk = np.full((max_m + 1, n + 1), -1, dtype=int)
        for j in range(hlen, n + 1):
            F[0, j] = rss(0, j)
        for mm in range(1, max_m + 1):
            for j in range((mm + 1) * hlen, n + 1):
                best, arg = inf, -1
                for i in range(mm * hlen, j - hlen + 1):
                    c = F[mm - 1, i] + rss(i, j)
                    if c < best:
                        best, arg = c, i
                F[mm, j], brk[mm, j] = best, arg
        bic = [inf if F[mm, n] <= 0 else n * np.log(F[mm, n] / n) + (mm + 1) * np.log(n)
               for mm in range(max_m + 1)]
        mhat = int(np.argmin(bic)) if nbreaks is None or nbreaks is False else max_m
        cur_m, cur_t = mhat, n
        while cur_m > 0:
            i = int(brk[cur_m, cur_t])
            if i < 1:
                break
            breaks.append(i)
            cur_t, cur_m = i, cur_m - 1
        breaks = sorted(set(int(b) for b in breaks if 1 <= b < n))
        pmap = {b: chow_f(b)[1] for b in breaks}

    if plot:
        if m == "cusum" and path is not None:
            fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
            axes[0].plot(t, y)
            axes[0].set_title("Series")
            axes[1].plot(t, path, color="C1")
            axes[1].axhline(bound, color="0.4", ls="--")
            axes[1].axhline(-bound, color="0.4", ls="--")
            axes[1].set_title("CUSUM")
            ax0 = axes[0]
        else:
            fig, ax0 = plt.subplots(figsize=(8, 4))
            ax0.plot(t, y)
            ax0.set_title("Breakpoints")
        for b in breaks:
            ax0.axvline(b, color="C3", ls="--", lw=1)
        fig.tight_layout()
        return fig
    cols = ["break_date", "confidence", "type"]
    if not breaks:
        return pd.DataFrame(columns=cols)
    return pd.DataFrame(
        [(label(k), conf(pmap.get(k, np.nan)), kind(k)) for k in breaks],
        columns=cols)

"breakpoints(data, method='cusum', alpha=0.05, at=None, nbreaks=None, plot=False, headers=True, date_col=None)"
