# Name: confusion_matrix
# Description: TP/FP/TN/FN counts with business labels. plot=True for a heatmap.
# Parameters: data, actual=None, predicted=None, positive=1, pos_name='Positive', neg_name='Negative', plot=False, headers=True

def confusion_matrix(data, actual=None, predicted=None, positive=1,
                     pos_name="Positive", neg_name="Negative",
                     plot=False, headers=True):
    """Confusion-matrix counts with business labels.

    data: table/range, or actual labels if predicted is a Series/range.
    actual, predicted: column names, ranges, or Series. Default: first two
        columns of data.
    positive: value treated as the positive class (default 1).
    pos_name, neg_name: words in the meaning column (e.g. 'Churn').
    plot: False (default) spills a table. True returns a 2x2 heatmap.
        Keep that PY cell as a Python object.
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

    frame = frame_of(data)
    a = pd.Series(col(frame, actual, 0)).reset_index(drop=True)
    p = pd.Series(col(frame, predicted, 1)).reset_index(drop=True)
    n0 = min(len(a), len(p))
    a, p = a.iloc[:n0], p.iloc[:n0]
    a = a.replace("", np.nan)
    p = p.replace("", np.nan)
    keep = a.notna() & p.notna()
    a, p = a[keep], p[keep]
    if len(a) < 1:
        raise ValueError("Need at least 1 row with actual and predicted.")
    pos = pd.Series(positive).iloc[0]
    pos_name = str(pd.Series(pos_name).iloc[0])
    neg_name = str(pd.Series(neg_name).iloc[0])
    if not isinstance(plot, bool):
        plot = bool(pd.Series(plot).iloc[0])
    yt, yp = is_pos(a, pos), is_pos(p, pos)
    tp = float((yt & yp).sum())
    fp = float((~yt & yp).sum())
    fn = float((yt & ~yp).sum())
    tn = float((~yt & ~yp).sum())
    if plot:
        mat = np.array([[tp, fn], [fp, tn]])
        labs = [pos_name, neg_name]
        fig, ax = plt.subplots()
        sns.heatmap(
            mat, annot=True, fmt=".0f", cmap="Blues", cbar=False,
            xticklabels=labs, yticklabels=labs, ax=ax, square=True,
        )
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")
        ax.set_title("Confusion matrix")
        fig.tight_layout()
        return fig
    return pd.DataFrame(
        [
            ("true_positive", tp,
             "Actual %s and Predicted %s" % (pos_name, pos_name)),
            ("false_positive", fp,
             "Actual %s and Predicted %s" % (neg_name, pos_name)),
            ("false_negative", fn,
             "Actual %s and Predicted %s" % (pos_name, neg_name)),
            ("true_negative", tn,
             "Actual %s and Predicted %s" % (neg_name, neg_name)),
        ],
        columns=["metric", "count", "meaning"],
    )

"confusion_matrix(data, actual=None, predicted=None, positive=1, pos_name='Positive', neg_name='Negative', plot=False, headers=True)"
