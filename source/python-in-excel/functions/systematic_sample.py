# Name: systematic_sample
# Description: Systematic sample of rows at a regular interval from a random start.
# Parameters: data, sample_size, random_state=42, headers=True

def systematic_sample(data, sample_size, random_state=42, headers=True):
    """Draw a systematic sample of rows.

    Interval k = N // sample_size. Start is random in 0..k-1. Then every
    kth row: start, start+k, start+2k, ... trimmed to sample_size.

    data: ref string, DataFrame, Series, list, or xl() result.
    sample_size: number of rows to return. Must be 1..N.
    random_state: seed for the start position (default 42).
    headers: used only when data is a ref string.
    """
    import random

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

    sample_size = int(pd.Series(sample_size).iloc[0])
    random_state = int(pd.Series(random_state).iloc[0])
    n = len(df)
    if sample_size < 1:
        raise ValueError("sample_size must be at least 1.")
    if sample_size > n:
        raise ValueError("sample_size cannot exceed population size.")

    k = n // sample_size
    start = random.Random(random_state).randint(0, k - 1)
    idx = list(range(start, n, k))[:sample_size]
    return df.iloc[idx].reset_index(drop=True)

"systematic_sample(data, sample_size, random_state=42, headers=True)"
