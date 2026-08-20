# Copy into a function that should accept a range string, xl() result, or DataFrame.


def as_dataframe(data, headers=True):
    """Return a pandas DataFrame from a ref string, xl() result, Series, or array."""
    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        df = data
    elif isinstance(data, pd.Series):
        df = data.to_frame()
    else:
        df = pd.DataFrame(data)
    return df.dropna(how="all")
