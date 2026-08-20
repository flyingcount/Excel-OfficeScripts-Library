# Name: expsmooth
# Description: Last simple-exponential-smoothing value (default alpha 0.2). Matches LAMBDA EXPSMOOTH.
# Parameters: data, alpha=0.2, headers=False

def expsmooth(data, alpha=0.2, headers=False):
    """Last SES value. Seed is the first numeric observation.

    St = alpha * xt + (1 - alpha) * S(t-1), with S0 = first value.
    For 10, 12, 14 and alpha 0.2 the result is 11.12 (same as EXPSMOOTH).

    data: column range, ref string, Series, or single-column DataFrame.
    headers: used only when data is a ref string (default False for a value column).
    """
    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        numeric = data.select_dtypes(include="number")
        values = numeric.iloc[:, 0] if numeric.shape[1] else data.iloc[:, 0]
    else:
        values = data
    series = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce").dropna()
    if series.empty:
        return float("nan")
    smooth = float(series.iloc[0])
    for x in series.iloc[1:]:
        smooth = alpha * float(x) + (1 - alpha) * smooth
    return smooth
