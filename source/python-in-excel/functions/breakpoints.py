# Name: breakpoints
# Description: Structural breaks via CUSUM, Chow, or Bai-Perron. plot=True for a chart.
# Parameters: data, method='cusum', alpha=0.05, at=None, nbreaks=None, plot=False, headers=True

def breakpoints(data, method="cusum", alpha=0.05, at=None, nbreaks=None,
                plot=False, headers=True):
    """CUSUM, Chow, or Bai-Perron breaks. plot=True is a chart (Python object).

    cusum: OLS residual CUSUM (intercept+trend). chow: F at `at` (1-based t
    or fraction); omitted = sup-F, 15% trim. baiperron: mean-shift; nbreaks
    omitted uses BIC (max 5). data: first numeric col. alpha default 0.05.
    """
    from scipy.stats import f as fdist
    from statsmodels.stats.diagnostic import breaks_cusumolsresid
    from statsmodels.regression.linear_model import OLS

    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        num = data.select_dtypes(include="number")
        values = num.iloc[:, 0] if num.shape[1] else data.iloc[:, 0]
    else:
        values = data
    y = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce").dropna()
    y = y.to_numpy(dtype="float64")
    n = int(y.size)
    if n < 10:
        raise ValueError("Need at least 10 observations.")
    alpha = float(pd.Series(alpha).iloc[0])
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1.")
    m = str(pd.Series(method).iloc[0]).strip().lower().replace("_", "-")
    if m in ("qlr", "supf", "sup-f"):
        m = "chow"
    if m in ("bp", "bai-perron", "bai perron"):
        m = "baiperron"
    if m not in ("cusum", "chow", "baiperron"):
        raise ValueError("method must be 'cusum', 'chow', or 'baiperron'.")
    t = np.arange(1, n + 1, dtype="float64")
    X = np.column_stack([np.ones(n), t])

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

    breaks, path, bound = [], None, np.nan
    if m == "cusum":
        resid = np.asarray(OLS(y, X).fit().resid, dtype="float64")
        stat, pval, crit = breaks_cusumolsresid(resid, ddof=2)
        stat, pval = float(stat), float(pval)
        c5 = float(np.asarray(crit).reshape(-1)[1]) if np.size(crit) > 1 else 1.36
        path = np.cumsum(resid) / np.sqrt(float(resid.dot(resid)))
        bound, flag = c5, 1.0 if pval < alpha else 0.0
        rows = [
            ("method", "cusum", "Ploberger-Kramer CUSUM, intercept+trend OLS."),
            ("n", n, "Count after dropping blanks."),
            ("statistic", stat, "Sup |CUSUM|/sqrt(n). Larger: break."),
            ("pvalue", pval, "p < alpha: reject stability."),
            ("crit_5", c5, "5% critical value."),
            ("alpha", alpha, "Cutoff for is_break."),
            ("is_break", flag, "1 if pvalue < alpha."),
        ]
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
        fv, pval = chow_f(bk)
        flag = 1.0 if np.isfinite(pval) and pval < alpha else 0.0
        breaks = [bk] if flag else []
        rows = [
            ("method", "chow", "Chow F, intercept+trend, split after t."),
            ("n", n, "Count after dropping blanks."),
            ("t", bk, "1-based last t of regime 1."),
            ("statistic", fv, "Chow F. Larger: break at t."),
            ("pvalue", pval, "p < alpha: regimes differ."),
            ("alpha", alpha, "Cutoff for is_break."),
            ("is_break", flag, "1 if pvalue < alpha."),
        ]
    else:
        max_m = 5 if nbreaks is None or nbreaks is False else max(
            1, int(pd.Series(nbreaks).iloc[0]))
        hlen = max(3, int(0.1 * n))
        max_m = min(max_m, max(0, n // (2 * hlen) - 1))
        if max_m < 1:
            raise ValueError("Series too short for Bai-Perron.")
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
        rows = [
            ("method", "baiperron", "Bai-Perron mean-shift; BIC if nbreaks omitted."),
            ("n", n, "Count after dropping blanks."),
            ("n_breaks", len(breaks), "Estimated mean-shift dates."),
            ("ssr_none", F[0, n], "SSR, one mean."),
            ("ssr_m", F[mhat, n], "SSR with chosen breaks."),
            ("is_break", 1.0 if breaks else 0.0, "1 if any break date."),
        ]
        for i, b in enumerate(breaks, 1):
            rows.append(("break_%d" % i, b, "1-based last t of regime %d." % i))

    if plot:
        if m == "cusum" and path is not None:
            fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
            axes[0].plot(t, y, color="C0")
            axes[0].set_title("Series")
            axes[1].plot(t, path, color="C1")
            axes[1].axhline(bound, color="0.4", ls="--")
            axes[1].axhline(-bound, color="0.4", ls="--")
            axes[1].set_title("CUSUM")
            axes[1].set_xlabel("t")
            ax0 = axes[0]
        else:
            fig, ax0 = plt.subplots(figsize=(8, 4))
            ax0.plot(t, y, color="C0")
            ax0.set_xlabel("t")
            ax0.set_title("Breakpoints")
        for b in breaks:
            ax0.axvline(b, color="C3", ls="--", lw=1)
        fig.tight_layout()
        return fig
    return pd.DataFrame(rows, columns=["metric", "value", "guidance"])

"breakpoints(data, method='cusum', alpha=0.05, at=None, nbreaks=None, plot=False, headers=True)"
