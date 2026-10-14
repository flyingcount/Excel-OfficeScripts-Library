# Name: lift_table
# Description: Decile cumulative gain and lift from predicted probabilities.
# Parameters: data, actual=None, proba=None, bins=10, positive=1, plot=False, headers=True

def lift_table(data, actual=None, proba=None, bins=10, positive=1,
               plot=False, headers=True):
    """Rank by score and spill cumulative gain and lift by bin.

    bin 1 is the highest scores (top decile when bins=10). cum_gain is
    the share of all positives in that top slice (e.g. top 20% yield
    65% of conversions). plot=True is a two-panel gain/lift chart.

    data: table/range, or actual labels if proba is a Series/range.
    actual, proba: column names, ranges, or Series. Default: first two
        columns of data (labels, then scores).
    bins: number of equal-count groups (default 10).
    positive: value treated as the positive class (default 1).
    headers: first row is headers when a ref string is used.
    """
    def frame_of(value):
        if isinstance(value, str):
            value = xl(value, headers=headers)
        if isinstance(value, pd.DataFrame):
            return value.reset_index(drop=True)
        if isinstance(value, pd.Series):
            return value.to_frame()
        return pd.DataFrame(value)

    def col(frame, spec, idx):
        if spec is None:
            if frame.shape[1] <= idx:
                raise ValueError("Need actual and probability columns.")
            return frame.iloc[:, idx]
        if isinstance(spec, pd.DataFrame):
            return spec.iloc[:, 0]
        if isinstance(spec, pd.Series) and int(spec.size) > 1:
            return spec.reset_index(drop=True)
        key = str(pd.Series(spec).iloc[0]).strip()
        lookup = {str(c).strip().lower(): c for c in frame.columns}
        if key.lower() in lookup:
            return frame[lookup[key.lower()]]
        raw = xl(key, headers=headers)
        if isinstance(raw, pd.DataFrame):
            raw = raw.iloc[:, 0]
        return pd.Series(raw)

    def is_pos(s, pos):
        s = pd.Series(s).reset_index(drop=True)
        pn = pd.to_numeric(pd.Series([pos]), errors="coerce").iloc[0]
        if pd.notna(pn):
            return pd.to_numeric(s, errors="coerce") == float(pn)
        return s.astype(str).str.strip() == str(pos).strip()

    frame = frame_of(data)
    a = pd.Series(col(frame, actual, 0)).reset_index(drop=True)
    pr = pd.to_numeric(col(frame, proba, 1), errors="coerce")
    pr = pd.Series(pr).reset_index(drop=True)
    n0 = min(len(a), len(pr))
    a, pr = a.iloc[:n0], pr.iloc[:n0]
    a = a.replace("", np.nan)
    keep = a.notna() & pr.notna()
    a, pr = a[keep], pr[keep]
    n = int(len(a))
    nbins = int(pd.Series(bins).iloc[0])
    if nbins < 2:
        raise ValueError("bins must be >= 2.")
    if n < nbins:
        raise ValueError("Need at least as many rows as bins.")
    pos = pd.Series(positive).iloc[0]
    if not isinstance(plot, bool):
        plot = bool(pd.Series(plot).iloc[0])
    scores = pr.to_numpy(dtype="float64")
    yt = is_pos(a, pos).to_numpy()
    order = np.argsort(-scores, kind="mergesort")
    ys, ss = yt[order], scores[order]
    total_pos = float(ys.sum())
    if total_pos < 1:
        raise ValueError("Need at least 1 positive case.")
    base = total_pos / n
    bin_id = np.floor(np.arange(n) * nbins / n).astype(int) + 1
    rows = []
    cum_n = cum_pos = 0.0
    for b in range(1, nbins + 1):
        m = bin_id == b
        k = float(m.sum())
        p = float(ys[m].sum())
        rr = p / k if k else np.nan
        cum_n += k
        cum_pos += p
        pct = cum_n / n
        gain = cum_pos / total_pos
        rows.append((
            float(b), k, p, rr, rr / base if k else np.nan,
            cum_n, cum_pos, pct, gain, gain / pct if pct else np.nan,
            float(ss[m].min()) if k else np.nan,
            float(ss[m].max()) if k else np.nan,
        ))
    out = pd.DataFrame(
        rows,
        columns=["bin", "n", "positives", "response_rate", "lift",
                 "cum_n", "cum_positives", "cum_pct", "cum_gain",
                 "cum_lift", "min_proba", "max_proba"],
    )
    if plot:
        fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
        pct = [0.0] + list(out["cum_pct"])
        gain = [0.0] + list(out["cum_gain"])
        axes[0].plot(pct, gain, marker="o")
        axes[0].plot([0, 1], [0, 1], linestyle="--")
        axes[0].set_ylabel("Cumulative gain")
        axes[0].set_title("Cumulative gain and lift")
        axes[1].plot(out["cum_pct"], out["cum_lift"], marker="o")
        axes[1].axhline(1.0, linestyle="--")
        axes[1].set_xlabel("Cumulative population")
        axes[1].set_ylabel("Cumulative lift")
        fig.tight_layout()
        return fig
    return out

"lift_table(data, actual=None, proba=None, bins=10, positive=1, plot=False, headers=True)"
