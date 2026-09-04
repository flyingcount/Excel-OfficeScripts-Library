# Name: find_optimal_threshold
# Description: Sweep probability cutoffs and pick the best F1 or P/R balance.
# Parameters: data, actual=None, proba=None, metric='f1', low=0.1, high=0.9, step=0.1, positive=1, headers=True

def find_optimal_threshold(data, actual=None, proba=None, metric="f1",
                           low=0.1, high=0.9, step=0.1, positive=1,
                           headers=True):
    """Choose a probability cutoff by F1 or precision/recall balance.

    Sweeps thresholds from low to high (default 0.1 to 0.9). metric='f1'
    maximises F1. metric='balanced' minimises |precision - recall|
    (F1 breaks ties). Default 0.5 is often weak on imbalanced data.

    data: table/range, or actual labels if proba is a Series/range.
    actual, proba: column names, ranges, or Series. Default: first two
        columns of data (labels, then scores).
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
    if n < 1:
        raise ValueError("Need at least 1 row with actual and probability.")
    pos = pd.Series(positive).iloc[0]
    metric = str(pd.Series(metric).iloc[0]).strip().lower()
    if metric not in ("f1", "balanced"):
        raise ValueError("metric must be 'f1' or 'balanced'.")
    low = float(pd.Series(low).iloc[0])
    high = float(pd.Series(high).iloc[0])
    step = float(pd.Series(step).iloc[0])
    if step <= 0 or high < low:
        raise ValueError("Need low <= high and step > 0.")
    nstep = int(round((high - low) / step))
    ts = low + np.arange(nstep + 1, dtype="float64") * step
    yt = is_pos(a, pos).to_numpy()
    scores = pr.to_numpy(dtype="float64")
    rows = []
    best_i, best_key = 0, None
    for t in ts:
        yp = scores >= t
        tp = float((yt & yp).sum())
        fp = float((~yt & yp).sum())
        fn = float((yt & ~yp).sum())
        tn = float((~yt & ~yp).sum())
        acc = (tp + tn) / n
        prec = tp / (tp + fp) if (tp + fp) else 0.0
        rec = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = (2 * prec * rec / (prec + rec)) if (prec + rec) else 0.0
        key = (f1, -abs(prec - rec)) if metric == "f1" else (
            -abs(prec - rec), f1)
        rows.append((float(t), acc, prec, rec, f1, 0.0))
        if best_key is None or key > best_key:
            best_key = key
            best_i = len(rows) - 1
    out = pd.DataFrame(rows, columns=["threshold", "accuracy", "precision",
                                      "recall", "f1", "is_best"])
    out.loc[best_i, "is_best"] = 1.0
    return out

"find_optimal_threshold(data, actual=None, proba=None, metric='f1', low=0.1, high=0.9, step=0.1, positive=1, headers=True)"
