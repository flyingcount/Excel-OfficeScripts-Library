# Name: stratified_sample
# Description: Proportional stratified sample from a range, table, or DataFrame.
# Parameters: data, strata_col, total_n, random_state=42, headers=True

def stratified_sample(data, strata_col, total_n, random_state=42, headers=True):
    """Draw a proportional stratified sample.

    Each stratum gets round(total_n * its share of the population) rows,
    at least 1 when the stratum is non-empty, capped at the stratum size.

    data: ref string, DataFrame, Series, or xl() result.
    strata_col: column name that defines the strata.
    total_n: target sample size across all strata.
    random_state: seed for reproducibility (default 42).
    headers: used only when data is a ref string.
    """
    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        df = data
    elif isinstance(data, pd.Series):
        df = data.to_frame()
    else:
        df = pd.DataFrame(data)
    df = df.dropna(how="all")
    if df.empty:
        raise ValueError("No data after dropping empty rows.")

    strata_col = str(pd.Series(strata_col).iloc[0]).strip()
    if strata_col not in df.columns:
        lookup = {str(c).strip().lower(): c for c in df.columns}
        key = strata_col.lower()
        if key not in lookup:
            raise ValueError("strata_col not found.")
        strata_col = lookup[key]

    total_n = int(pd.Series(total_n).iloc[0])
    random_state = int(pd.Series(random_state).iloc[0])
    if total_n < 1:
        raise ValueError("total_n must be at least 1.")

    df = df.copy()
    df[strata_col] = df[strata_col].replace("", np.nan)
    df = df.dropna(subset=[strata_col])
    if df.empty:
        raise ValueError("No rows with a stratum value.")

    pop = len(df)
    sampled = []
    for _, group in df.groupby(strata_col, dropna=True):
        n = max(1, int(round(total_n * len(group) / pop)))
        n = min(n, len(group))
        sampled.append(group.sample(n=n, random_state=random_state))
    return pd.concat(sampled).reset_index(drop=True)

"stratified_sample(data, strata_col, total_n, random_state=42, headers=True)"
