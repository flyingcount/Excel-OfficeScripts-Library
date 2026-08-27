# Name: qq_norm
# Description: Q-Q plot vs normal with Shapiro-Wilk and Anderson-Darling on the chart. Stats are also attributes for other PY cells.
# Parameters: data, plot=True, headers=False

def qq_norm(data, plot=True, headers=False):
    """Q-Q plot against the normal distribution, with Shapiro-Wilk and Anderson-Darling.

    data: column range, ref string, Series, list, or xl() result.
    plot: True (default) returns a matplotlib Figure; False spills a metric/value table.
    headers: first row is headers when data is a ref string.

    Chart: leave the PY cell as a Python object. The figure is annotated with both
    tests, and the same values are attributes for other PY cells, for example
    B2.shapiro_pvalue, B2.anderson_stat, B2.results (if the chart is in B2).

    Table includes n, Shapiro-Wilk W and p, Anderson-Darling A^2, and the 5%
    critical value. Need at least 3 numeric values.
    """
    import matplotlib.pyplot as plt
    from scipy import stats

    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        numeric = data.select_dtypes(include="number")
        values = numeric.iloc[:, 0] if numeric.shape[1] else data.iloc[:, 0]
    else:
        values = data
    y = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce").dropna().to_numpy(dtype=float)
    n = int(y.size)
    if n < 3:
        raise ValueError("Need at least 3 numeric values.")

    try:
        sh_stat, sh_p = stats.shapiro(y)
        sh_stat, sh_p = float(sh_stat), float(sh_p)
    except ValueError:
        sh_stat, sh_p = float("nan"), float("nan")

    ad_stat = float("nan")
    crit_5 = float("nan")
    try:
        ad = stats.anderson(y, dist="norm")
        ad_stat = float(ad.statistic)
        sig = np.asarray(ad.significance_level, dtype=float)
        crit = np.asarray(ad.critical_values, dtype=float)
        match = np.where(np.isclose(sig, 5.0))[0]
        if match.size:
            crit_5 = float(crit[int(match[0])])
    except ValueError:
        pass

    table = pd.DataFrame(
        {
            "metric": [
                "n",
                "shapiro_stat",
                "shapiro_pvalue",
                "anderson_stat",
                "anderson_critical_5",
            ],
            "value": [
                n,
                sh_stat,
                sh_p,
                ad_stat,
                crit_5,
            ],
        }
    )

    if not plot:
        return table

    fig, ax = plt.subplots(figsize=(6, 5))
    stats.probplot(y, dist="norm", plot=ax)
    ax.set_title("Q-Q plot")
    note = (
        f"Shapiro-Wilk  W = {sh_stat:.3f}  p = {sh_p:.3f}\n"
        f"(If p > 0.05, normal distribution in the data can be assumed)\n"
        f"Anderson-Darling  A^2 = {ad_stat:.3f}  (5% crit. {crit_5:.3f})"
    )
    ax.text(
        0.02,
        0.98,
        note,
        transform=ax.transAxes,
        va="top",
        ha="left",
        fontsize=9,
        bbox={"boxstyle": "round", "facecolor": "white", "alpha": 0.85},
    )
    fig.tight_layout()
    fig.shapiro_stat = sh_stat
    fig.shapiro_pvalue = sh_p
    fig.anderson_stat = ad_stat
    fig.anderson_critical_5 = crit_5
    fig.results = table
    return fig

"qq_norm(data, plot=True, headers=False)"
