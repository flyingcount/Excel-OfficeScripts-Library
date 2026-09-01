# Name: normality_check
# Description: Shapiro-Wilk, Anderson-Darling, and a normal Q-Q plot. Paste this one file to use all three.
# Parameters: see normality_check / qq_norm, shapiro, anderson

def _norm_values(data, headers=False):
    """First numeric column as a float array. Drops blanks. Need at least 3 values."""
    if isinstance(data, str):
        data = xl(data, headers=headers)
    if isinstance(data, pd.DataFrame):
        numeric = data.select_dtypes(include="number")
        values = numeric.iloc[:, 0] if numeric.shape[1] else data.iloc[:, 0]
    else:
        values = data
    y = pd.to_numeric(pd.Series(values).squeeze(), errors="coerce").dropna().to_numpy(dtype=float)
    if y.size < 3:
        raise ValueError("Need at least 3 numeric values.")
    return y


def shapiro(data, metric=None, headers=False):
    """Shapiro-Wilk W and p-value.

    data: column range, ref string, Series, list, or xl() result.
    metric: omit to spill a metric/value table. "pvalue" or "stat" returns that float.
    headers: first row is headers when data is a ref string.

    Switch the PY cell to Excel value. Need at least 3 numeric values.
    If p > 0.05, a normal distribution in the data can be assumed.
    The spilled table has metric, value, and interpretation.
    """
    from scipy import stats

    y = _norm_values(data, headers)
    try:
        sh_stat, sh_p = stats.shapiro(y)
        sh_stat, sh_p = float(sh_stat), float(sh_p)
    except ValueError:
        sh_stat, sh_p = float("nan"), float("nan")

    rows = {"shapiro_stat": sh_stat, "shapiro_pvalue": sh_p}
    if metric is not None:
        key = str(pd.Series(metric).iloc[0]).strip().lower()
        aliases = {
            "stat": "shapiro_stat",
            "w": "shapiro_stat",
            "shapiro_stat": "shapiro_stat",
            "pvalue": "shapiro_pvalue",
            "p": "shapiro_pvalue",
            "p_value": "shapiro_pvalue",
            "shapiro_pvalue": "shapiro_pvalue",
        }
        if key not in aliases:
            raise ValueError("metric must be 'stat', 'pvalue', or omitted for the table.")
        return float(rows[aliases[key]])

    if not np.isfinite(sh_p):
        p_note = "Test did not run."
    elif sh_p > 0.05:
        p_note = "p > 0.05: a normal distribution in the data can be assumed."
    else:
        p_note = "p ≤ 0.05: the data are not consistent with a normal distribution."
    interp = {
        "shapiro_stat": "Shapiro-Wilk W. Values near 1 support normality.",
        "shapiro_pvalue": p_note,
    }
    return pd.DataFrame(
        {
            "metric": list(rows.keys()),
            "value": list(rows.values()),
            "interpretation": [interp[k] for k in rows],
        }
    )


def anderson(data, metric=None, headers=False):
    """Anderson-Darling A^2 and critical values for a normal distribution.

    data: column range, ref string, Series, list, or xl() result.
    metric: omit to spill a metric/value table. "stat" or "critical_5" returns that float.
    headers: first row is headers when data is a ref string.

    Switch the PY cell to Excel value. Need at least 3 numeric values.
    A^2 above the 5% critical value suggests the data are not normal.
    The spilled table has metric, value, and interpretation.
    """
    from scipy import stats

    y = _norm_values(data, headers)
    rows = {"anderson_stat": float("nan")}
    aliases = {
        "stat": "anderson_stat",
        "a2": "anderson_stat",
        "anderson_stat": "anderson_stat",
    }
    try:
        ad = stats.anderson(y, dist="norm")
        rows["anderson_stat"] = float(ad.statistic)
        for sig, val in zip(
            np.asarray(ad.significance_level, dtype=float),
            np.asarray(ad.critical_values, dtype=float),
        ):
            if abs(sig - 2.5) < 1e-9:
                name = "anderson_critical_2_5"
                short = "critical_2_5"
            elif abs(sig - int(sig)) < 1e-9:
                name = f"anderson_critical_{int(sig)}"
                short = f"critical_{int(sig)}"
            else:
                tag = str(sig).replace(".", "_")
                name = f"anderson_critical_{tag}"
                short = f"critical_{tag}"
            rows[name] = float(val)
            aliases[short] = name
            aliases[name] = name
            aliases[str(int(sig)) if abs(sig - int(sig)) < 1e-9 else str(sig)] = name
    except ValueError:
        pass

    if metric is not None:
        key = str(pd.Series(metric).iloc[0]).strip().lower()
        if key not in aliases:
            raise ValueError(
                "metric must be 'stat', 'critical_5' (or another critical_*), or omitted for the table."
            )
        return float(rows[aliases[key]])

    ad_stat = rows["anderson_stat"]
    crit_5 = rows.get("anderson_critical_5", float("nan"))
    if not np.isfinite(ad_stat) or not np.isfinite(crit_5):
        ad_note = "Anderson-Darling A^2. Larger than the 5% critical value suggests non-normality."
    elif ad_stat > crit_5:
        ad_note = "A^2 above the 5% critical value: data are not normal at 5%."
    else:
        ad_note = "A^2 at or below the 5% critical value: normality not rejected at 5%."
    interp = []
    for name in rows:
        if name == "anderson_stat":
            interp.append(ad_note)
        elif name.startswith("anderson_critical_"):
            interp.append(
                "Reject normality at this significance level if A^2 exceeds this critical value."
            )
        else:
            interp.append("")
    return pd.DataFrame(
        {
            "metric": list(rows.keys()),
            "value": list(rows.values()),
            "interpretation": interp,
        }
    )


def normality_check(data, plot=True, headers=False):
    """Q-Q plot against the normal distribution, with Shapiro-Wilk and Anderson-Darling.

    data: column range, ref string, Series, list, or xl() result.
    plot: True (default) returns a matplotlib Figure; False spills metric, value, interpretation.
    headers: first row is headers when data is a ref string.

    Chart: leave the PY cell as a Python object. The figure is annotated with both
    tests, and the same values are attributes for other PY cells, for example
    B2.shapiro_pvalue, B2.anderson_stat, B2.results (if the chart is in B2).

    For a single number in another cell, call shapiro(data, 'pvalue') or
    anderson(data, 'stat') and switch that cell to Excel value.
    Need at least 3 numeric values.
    """
    import matplotlib.pyplot as plt
    from scipy import stats

    y = _norm_values(data, headers)
    n = int(y.size)
    sh_stat = shapiro(y, "stat")
    sh_p = shapiro(y, "pvalue")
    ad_stat = anderson(y, "stat")
    crit_5 = anderson(y, "critical_5")

    if not np.isfinite(sh_p):
        p_note = "Test did not run."
    elif sh_p > 0.05:
        p_note = "p > 0.05: a normal distribution in the data can be assumed."
    else:
        p_note = "p ≤ 0.05: the data are not consistent with a normal distribution."
    if not np.isfinite(ad_stat) or not np.isfinite(crit_5):
        ad_note = "Anderson-Darling A^2. Larger than the 5% critical value suggests non-normality."
    elif ad_stat > crit_5:
        ad_note = "A^2 above the 5% critical value: data are not normal at 5%."
    else:
        ad_note = "A^2 at or below the 5% critical value: normality not rejected at 5%."
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
            "interpretation": [
                "Count of numeric values after dropping blanks.",
                "Shapiro-Wilk W. Values near 1 support normality.",
                p_note,
                ad_note,
                "Reject normality at 5% if A^2 exceeds this critical value.",
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

qq_norm = normality_check

"""normality_check(data, plot=True, headers=False)
 qq_norm(data, plot=True, headers=False)
 shapiro(data, metric=None, headers=False)
 anderson(data, metric=None, headers=False)
 _norm_values(data, headers=False)"""
