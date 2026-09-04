# Name: capability_report
# Description: Cp, Cpk, Pp, Ppk and expected overall PPM.
# Parameters: data, usl, lsl, headers=False

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
