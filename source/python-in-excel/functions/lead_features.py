# Name: lead_features
# Description: Lead columns from a value series (future values).
# Parameters: data, leads=1, value_col=None, date_col=None, headers=True

def lead_features(data, leads=1, value_col=None, date_col=None, headers=True):
    """Lead columns for a time series. Leads are y.shift(-k).

    data: table/range, DataFrame, Series, or ref string.
    leads: int n gives lead_1 .. lead_n; a list or '1,7,12' gives those leads.
    value_col: header of the value column. First numeric if omitted.
    date_col: header of the date column. Auto-detected if omitted.
    headers: first row is headers when data is a ref string. Default True.

    Sorted by date when a date column is present. Trailing rows are blank.
    """
    def to_frame(value):
        if isinstance(value, str):
            value = xl(value, headers=headers)
        if isinstance(value, pd.DataFrame):
            return value
        if isinstance(value, pd.Series):
            return value.to_frame()
        return pd.DataFrame(value)

    def pick_col(frame, name, kind):
        if name is not None:
            key = str(pd.Series(name).iloc[0]).strip()
            cols = {str(c).strip().lower(): c for c in frame.columns}
            if key.lower() in cols:
                return frame[cols[key.lower()]]
            if key in frame.columns:
                return frame[key]
            raise ValueError("Column '%s' not found in data." % key)
        if kind == "date":
            for col in frame.columns:
                s = frame[col]
                if pd.api.types.is_datetime64_any_dtype(s):
                    return pd.to_datetime(s)
                if pd.api.types.is_numeric_dtype(s):
                    continue
                parsed = pd.to_datetime(s, errors="coerce")
                if parsed.notna().mean() > 0.8:
                    return parsed
            return None
        numeric = frame.select_dtypes(include="number")
        if numeric.shape[1]:
            return numeric.iloc[:, 0]
        return pd.to_numeric(frame.iloc[:, 0], errors="coerce")

    def to_ints(value):
        if value is None or value is False:
            return []
        if isinstance(value, str):
            raw = [p.strip() for p in value.replace(";", ",").split(",") if p.strip()]
        else:
            raw = list(pd.Series(np.ravel(
                value.to_numpy() if isinstance(value, pd.DataFrame) else value
            )).dropna())
        nums = []
        for x in raw:
            try:
                n = int(float(x))
            except (TypeError, ValueError):
                continue
            if n > 0:
                nums.append(n)
        if len(nums) == 1:
            nums = list(range(1, nums[0] + 1))
        out, seen = [], set()
        for n in nums:
            if n not in seen:
                seen.add(n)
                out.append(n)
        return out

    frame = to_frame(data)
    y = pd.to_numeric(pick_col(frame, value_col, "value"), errors="coerce")
    val_name = y.name
    if not isinstance(val_name, str) or not val_name.strip() or val_name.lower() in (
            "none", "nan", "date"):
        val_name = "value"
    dates = pick_col(frame, date_col, "date") if (
        date_col is not None or frame.shape[1] > 1) else None
    y = pd.Series(y).reset_index(drop=True)
    if int(y.size) < 1:
        raise ValueError("Need at least 1 value row.")
    lead_list = to_ints(leads)
    if not lead_list:
        raise ValueError("Provide at least one lead.")
    out = pd.DataFrame({val_name: y})
    if dates is not None:
        dates = pd.Series(dates).reset_index(drop=True)
        out.insert(0, "date", dates)
        out = out.sort_values("date", kind="mergesort", na_position="last").reset_index(drop=True)
        y = out[val_name]
    for k in lead_list:
        out["lead_%d" % k] = y.shift(-k)
    return out

"lead_features(data, leads=1, value_col=None, date_col=None, headers=True)"
