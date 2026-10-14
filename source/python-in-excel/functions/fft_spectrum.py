# Name: fft_spectrum
# Description: FFT periodogram: cycles, frequency, period, and power. Table or plot.
# Parameters: data, dt=1, plot=False, headers=False

def fft_spectrum(data, dt=1, plot=False, headers=False):
    """Real FFT periodogram. plot=False spills a table; True is a chart.

    data: value column, ref string, Series, or DataFrame (first numeric col).
    dt: time between observations. Default 1 (period is in observations).
    plot: False (default) returns a table. True returns power vs frequency
        and power vs period. Keep that PY cell as a Python object.
    headers: first row is headers when data is a ref string.

    The series is demeaned. DC (k=0) is omitted. Need at least 4 values.

    Table columns: cycles, frequency, period, power, peak.
    cycles is the DFT bin (cycles in the sample). frequency is cycles per
    time unit (1/dt). period is 1/frequency. power is |FFT|^2 / n.
    peak is 1 on the strongest non-DC bin.
    """
    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        numeric = data.select_dtypes(include="number")
        values = numeric.iloc[:, 0] if numeric.shape[1] else data.iloc[:, 0]
    elif isinstance(data, pd.Series):
        values = data
    else:
        values = pd.Series(data)

    y = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce").dropna().to_numpy(dtype=float)
    n = int(y.size)
    if n < 4:
        raise ValueError("Need at least 4 numeric values.")
    dt = float(pd.Series(dt).iloc[0])
    if dt <= 0:
        raise ValueError("dt must be positive.")

    spec = np.fft.rfft(y - y.mean())
    freq = np.fft.rfftfreq(n, d=dt)
    power = (np.abs(spec) ** 2) / n
    k = np.arange(spec.size, dtype=float)
    period = np.where(freq > 0, 1.0 / freq, np.nan)

    keep = freq > 0
    k, freq, period, power = k[keep], freq[keep], period[keep], power[keep]
    peak = np.zeros(power.size, dtype=float)
    if power.size:
        peak[int(np.argmax(power))] = 1.0

    if plot:
        fig, axes = plt.subplots(2, 1, figsize=(8, 6))
        axes[0].stem(freq, power, basefmt=" ")
        axes[0].set_title("Power spectrum")
        axes[0].set_xlabel("Frequency (cycles per time unit)")
        axes[0].set_ylabel("Power")
        axes[1].stem(period, power, basefmt=" ")
        axes[1].set_title("Power vs period")
        axes[1].set_xlabel("Period (time units per cycle)")
        axes[1].set_ylabel("Power")
        fig.tight_layout()
        return fig

    return pd.DataFrame({
        "cycles": k,
        "frequency": freq,
        "period": period,
        "power": power,
        "peak": peak,
    })

"fft_spectrum(data, dt=1, plot=False, headers=False)"
