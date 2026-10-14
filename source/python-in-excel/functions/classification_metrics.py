# Name: classification_metrics
# Description: Binary class metrics (accuracy, F1, MCC, likelihood ratios, …).
# Parameters: data, actual=None, predicted=None, positive=1, beta=1, headers=True

def classification_metrics(data, actual=None, predicted=None, positive=1,
                           beta=1, headers=True):
    """Accuracy, rates, F1/F-beta, MCC, and related binary metrics.

    data: table/range, or actual labels if predicted is a Series/range.
    actual, predicted: column names, ranges, or Series. Default: first two
        columns of data (hard labels, not probabilities).
    positive: value treated as the positive class (default 1).
    beta: weight on recall in F-beta (default 1, same as F1).
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
                raise ValueError("Need actual and predicted columns.")
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

    def div(num, den):
        return float(num / den) if den else np.nan

    frame = frame_of(data)
    a = pd.Series(col(frame, actual, 0)).reset_index(drop=True)
    p = pd.Series(col(frame, predicted, 1)).reset_index(drop=True)
    n0 = min(len(a), len(p))
    a, p = a.iloc[:n0], p.iloc[:n0]
    a = a.replace("", np.nan)
    p = p.replace("", np.nan)
    keep = a.notna() & p.notna()
    a, p = a[keep], p[keep]
    n = int(len(a))
    if n < 1:
        raise ValueError("Need at least 1 row with actual and predicted.")
    pos = pd.Series(positive).iloc[0]
    b = float(pd.Series(beta).iloc[0])
    if b <= 0:
        raise ValueError("beta must be > 0.")
    yt, yp = is_pos(a, pos), is_pos(p, pos)
    tp = float((yt & yp).sum())
    fp = float((~yt & yp).sum())
    fn = float((yt & ~yp).sum())
    tn = float((~yt & ~yp).sum())
    tpr = tp / (tp + fn) if (tp + fn) else 0.0
    fpr = fp / (fp + tn) if (fp + tn) else 0.0
    tnr = tn / (tn + fp) if (tn + fp) else 0.0
    fnr = fn / (tp + fn) if (tp + fn) else 0.0
    prec = tp / (tp + fp) if (tp + fp) else 0.0
    npv = tn / (tn + fn) if (tn + fn) else 0.0
    acc = (tp + tn) / n
    f1 = (2 * prec * tpr / (prec + tpr)) if (prec + tpr) else 0.0
    bb = b * b
    fbeta = ((1 + bb) * prec * tpr / (bb * prec + tpr)
             if (bb * prec + tpr) else 0.0)
    lr_p = div(tpr, fpr)
    lr_n = div(fnr, tnr)
    mcc_d = float(np.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn)))
    return pd.DataFrame(
        [
            ("n", float(n)),
            ("accuracy", acc),
            ("misclassification_rate", (fp + fn) / n),
            ("true_positive_rate", tpr),
            ("false_positive_rate", fpr),
            ("true_negative_rate", tnr),
            ("false_negative_rate", fnr),
            ("precision", prec),
            ("prevalence", (tp + fn) / n),
            ("lr_positive", lr_p),
            ("lr_negative", lr_n),
            ("diagnostic_odds_ratio", div(lr_p, lr_n)),
            ("f1", f1),
            ("beta", b),
            ("f_beta", fbeta),
            ("mcc", div(tp * tn - fp * fn, mcc_d)),
            ("informedness", tpr + tnr - 1.0),
            ("markedness", prec + npv - 1.0),
            ("threat_score", div(tp, tp + fp + fn)),
        ],
        columns=["metric", "value"],
    )

"classification_metrics(data, actual=None, predicted=None, positive=1, beta=1, headers=True)"
