# Name: xl_df
# Description: Load an Excel range, table, or defined name as a pandas DataFrame.
# Parameters: ref, headers=True

def xl_df(ref, headers=True):
    """Load Excel data with xl() and drop rows that are entirely empty.

    ref: "A1:C10", "Table1[#All]", or a defined name.
    headers: first row is column names (default True).
    """
    data = xl(ref, headers=headers)
    if isinstance(data, pd.DataFrame):
        df = data
    elif isinstance(data, pd.Series):
        df = data.to_frame()
    else:
        df = pd.DataFrame(data)
    return df.dropna(how="all")

"xl_df(ref, headers=True)"
