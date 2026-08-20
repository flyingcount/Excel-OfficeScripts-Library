# Name: acf_pacf
# Description: ACF and PACF plot (or lag table) to identify lag effects and momentum.
# Parameters: data, lags=None, plot=True, headers=False

def acf_pacf(data, lags=None, plot=True, headers=False):
    """Autocorrelation and partial autocorrelation of a series.

    ACF: correlation of the series with its own lags (momentum / mean-reversion).
    PACF: correlation at lag k after removing earlier lags.

    data: value column, ref string, Series, or DataFrame (first numeric column).
    lags: number of lags. Default min(10, n//2 - 1).
    plot: True (default) returns a two-panel matplotlib Figure. Keep the PY cell
    as a Python object. False spills a table with columns lag, acf, pacf.
    headers: first row is headers when data is a ref string.

    Need at least 4 numeric values.
    """
    import matplotlib.pyplot as plt
    from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
    from statsmodels.tsa.stattools import acf, pacf

    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        numeric = data.select_dtypes(include="number")
        values = numeric.iloc[:, 0] if numeric.shape[1] else data.iloc[:, 0]
    else:
        values = data
    y = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce").dropna().to_numpy(dtype=float)
    n = int(y.size)
    if n < 4:
        raise ValueError("Need at least 4 numeric values for ACF/PACF.")

    max_lag = max(1, n // 2 - 1)
    lag = min(max_lag, 10 if lags is None else int(pd.Series(lags).iloc[0]))
    lag = max(1, lag)

    if plot:
        fig, axes = plt.subplots(1, 2, figsize=(10, 4))
        plot_acf(y, ax=axes[0], lags=lag)
        plot_pacf(y, ax=axes[1], lags=lag)
        axes[0].set_title("ACF")
        axes[1].set_title("PACF")
        fig.suptitle("Autocorrelation")
        fig.tight_layout()
        return fig

    return pd.DataFrame(
        {
            "lag": np.arange(lag + 1, dtype=int),
            "acf": acf(y, nlags=lag, fft=True),
            "pacf": pacf(y, nlags=lag),
        }
    )

"acf_pacf(data, lags=None, plot=True, headers=False)"
