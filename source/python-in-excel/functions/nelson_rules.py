# Name: nelson_rules
# Description: Nelson's eight tests for an individuals chart.
# Parameters: data, headers=False

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
