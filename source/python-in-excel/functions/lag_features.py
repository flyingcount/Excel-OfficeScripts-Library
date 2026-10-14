# Name: lag_features
# Description: Lag columns, rolling-window statistics, and EMA from a value series.
# Parameters: data, value_col=None, date_col=None, lags=1, windows=7, stats='mean', ema=0, headers=True

def lag_features(data, value_col=None, date_col=None, lags=1, windows=7,
                 stats="mean", ema=0, headers=True):
    """Lag columns, rolling-window statistics, and EMA for a time series.

    Lags are y.shift(k). Rolling stats and EMA use only past values, so the
    current row is not in the window. EMA is recursive with alpha = 2/(span+1).

    data: table/range, DataFrame, Series, or ref string.
    value_col: header of the value column. First numeric if omitted.
    date_col: header of the date column. Auto-detected if omitted.
    lags: int n gives lag_1 .. lag_n; a list or '1,7,12' gives those lags.
        0 or None skips lags.
    windows: int or list of window sizes. 0 or None skips rolling stats.
    stats: mean, std, min, max, median, sum. Comma-separated or list.
    ema: EMA span, or a list / '12,26'. 0 or None skips EMA.
    headers: first row is headers when data is a ref string. Default True.

    Sorted by date when a date column is present. Early rows are blank
    until each lag, window, or EMA span is filled.
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
                if name is None and pd.api.types.is_numeric_dtype(s):
                    continue
                if pd.api.types.is_numeric_dtype(s):
                    num = pd.to_numeric(s, errors="coerce")
                    if num.notna().mean() > 0.8 and num.dropna().median() > 200:
                        return pd.to_datetime(num, unit="D", origin="1899-12-30")
                parsed = pd.to_datetime(s, errors="coerce")
                if parsed.notna().mean() > 0.8:
                    return parsed
            return None
        numeric = frame.select_dtypes(include="number")
        if numeric.shape[1]:
            return numeric.iloc[:, 0]
        return pd.to_numeric(frame.iloc[:, 0], errors="coerce")

    def to_ints(value, expand=False):
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
        if expand and len(nums) == 1:
            nums = list(range(1, nums[0] + 1))
        out = []
        seen = set()
        for n in nums:
            if n not in seen:
                seen.add(n)
                out.append(n)
        return out

    def to_stats(value):
        allowed = ("mean", "std", "min", "max", "median", "sum")
        if value is None or value is False:
            return ["mean"]
        if isinstance(value, str):
            raw = [p.strip().lower() for p in value.replace(";", ",").split(",") if p.strip()]
        else:
            raw = [str(x).strip().lower() for x in pd.Series(np.ravel(
                value.to_numpy() if isinstance(value, pd.DataFrame) else value
            )).dropna()]
        out = []
        seen = set()
        for s in raw:
            if s in allowed and s not in seen:
                seen.add(s)
                out.append(s)
        if not out:
            raise ValueError("stats must be mean, std, min, max, median, or sum.")
        return out

    frame = to_frame(data)
    y = pd.to_numeric(pick_col(frame, value_col, "value"), errors="coerce")
    val_name = y.name
    if not isinstance(val_name, str) or not val_name.strip() or val_name.lower() in ("none", "nan", "date"):
        val_name = "value"
    dates = pick_col(frame, date_col, "date") if (
        date_col is not None or frame.shape[1] > 1) else None
    y = pd.Series(y).reset_index(drop=True)
    n = int(y.size)
    if n < 1:
        raise ValueError("Need at least 1 value row.")
    lag_list = to_ints(lags, expand=True)
    win_list = to_ints(windows, expand=False)
    ema_list = to_ints(ema, expand=False)
    if not lag_list and not win_list and not ema_list:
        raise ValueError("Provide at least one lag, window, or ema span.")
    out = pd.DataFrame({val_name: y})
    if dates is not None:
        dates = pd.Series(dates).reset_index(drop=True)
        out.insert(0, "date", dates)
        out = out.sort_values("date", kind="mergesort", na_position="last").reset_index(drop=True)
        y = out[val_name]
    for k in lag_list:
        out["lag_%d" % k] = y.shift(k)
    if win_list:
        past = y.shift(1)
        for w in win_list:
            rolled = past.rolling(w)
            for s in to_stats(stats):
                out["roll_%s_%d" % (s, w)] = getattr(rolled, s)()
    for s in ema_list:
        out["ema_%d" % s] = y.ewm(span=s, adjust=False, min_periods=s).mean().shift(1)
    return out

"lag_features(data, value_col=None, date_col=None, lags=1, windows=7, stats='mean', ema=0, headers=True)"
