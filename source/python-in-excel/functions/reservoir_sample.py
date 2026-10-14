# Name: reservoir_sample
# Description: Algorithm R reservoir sample of rows from a stream or table.
# Parameters: data, k, random_state=42, headers=True

def reservoir_sample(data, k, random_state=42, headers=True):
    """Uniform sample of k rows (Algorithm R). Uses O(k) index memory.

    Fills a reservoir with the first k rows, then each later row i replaces
    a random reservoir slot with probability k / (i + 1). If there are fewer
    than k rows, all of them are returned.

    data: ref string, DataFrame, Series, list, or xl() result.
    k: desired sample size (at least 1).
    random_state: seed for reproducibility (default 42).
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

    k = int(pd.Series(k).iloc[0])
    random_state = int(pd.Series(random_state).iloc[0])
    if k < 1:
        raise ValueError("k must be at least 1.")

    rng = random.Random(random_state)
    pos = []
    for i in range(len(df)):
        if i < k:
            pos.append(i)
        else:
            j = rng.randint(0, i)
            if j < k:
                pos[j] = i
    return df.iloc[pos].reset_index(drop=True)

"reservoir_sample(data, k, random_state=42, headers=True)"
