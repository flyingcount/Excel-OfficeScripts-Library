# Name: normality_check
# Description: Shapiro-Wilk, Anderson-Darling, and a Q-Q plot. One paste for all three.
# Parameters: see normality_check / qq_norm, shapiro, anderson

def _norm_values(data, headers=False):
    """First numeric column as float. Drops blanks. Need at least 3 values."""
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


def _norm_df(rows, notes):
    return pd.DataFrame({"metric": list(rows), "value": list(rows.values()), "interpretation": notes})


def shapiro(data, metric=None, headers=False):
    """Shapiro-Wilk W and p. metric 'pvalue' or 'stat' for a float; omit for the table."""
    from scipy import stats

    y = _norm_values(data, headers)
    try:
        sh_stat, sh_p = (float(x) for x in stats.shapiro(y))
    except ValueError:
        sh_stat, sh_p = float("nan"), float("nan")
    rows = {"shapiro_stat": sh_stat, "shapiro_pvalue": sh_p}
    if metric is not None:
        key = str(pd.Series(metric).iloc[0]).strip().lower()
        aliases = {"stat": "shapiro_stat", "w": "shapiro_stat", "pvalue": "shapiro_pvalue", "p": "shapiro_pvalue", "p_value": "shapiro_pvalue"}
        aliases.update({k: k for k in rows})
        if key not in aliases:
            raise ValueError("metric must be 'stat', 'pvalue', or omitted for the table.")
        return float(rows[aliases[key]])
    if not np.isfinite(sh_p):
        p_note = "Test did not run."
    elif sh_p > 0.05:
        p_note = "p > 0.05: a normal distribution in the data can be assumed."
    else:
        p_note = "p <= 0.05: data are not consistent with a normal distribution."
    return _norm_df(rows, ["Shapiro-Wilk W. Values near 1 support normality.", p_note])


def anderson(data, metric=None, headers=False):
    """Anderson-Darling A^2. metric 'stat' or 'critical_5' for a float; omit for the table."""
    from scipy import stats

    y = _norm_values(data, headers)
    rows = {"anderson_stat": float("nan")}
    aliases = {"stat": "anderson_stat", "a2": "anderson_stat", "anderson_stat": "anderson_stat"}
    try:
        ad = stats.anderson(y, dist="norm")
        rows["anderson_stat"] = float(ad.statistic)
        for sig, val in zip(np.asarray(ad.significance_level, dtype=float), np.asarray(ad.critical_values, dtype=float)):
            tag = "2_5" if abs(sig - 2.5) < 1e-9 else str(int(sig)) if abs(sig - int(sig)) < 1e-9 else str(sig).replace(".", "_")
            name, short = f"anderson_critical_{tag}", f"critical_{tag}"
            rows[name] = float(val)
            aliases[short] = aliases[name] = name
            aliases[str(int(sig)) if abs(sig - int(sig)) < 1e-9 else str(sig)] = name
    except ValueError:
        pass
    if metric is not None:
        key = str(pd.Series(metric).iloc[0]).strip().lower()
        if key not in aliases:
            raise ValueError("metric must be 'stat', 'critical_5', or omitted for the table.")
        return float(rows[aliases[key]])
    ad_stat, crit_5 = rows["anderson_stat"], rows.get("anderson_critical_5", float("nan"))
    if not np.isfinite(ad_stat) or not np.isfinite(crit_5):
        ad_note = "A^2. Larger than the 5% critical value suggests non-normality."
    elif ad_stat > crit_5:
        ad_note = "A^2 above the 5% critical value: data are not normal at 5%."
    else:
        ad_note = "A^2 at or below the 5% critical value: normality not rejected at 5%."
    crit_note = "Reject normality at this level if A^2 exceeds this critical value."
    notes = [ad_note if n == "anderson_stat" else crit_note if n.startswith("anderson_critical_") else "" for n in rows]
    return _norm_df(rows, notes)


def normality_check(data, plot=True, headers=False):
    """Q-Q plot with Shapiro-Wilk and Anderson-Darling. plot=False spills a table."""
    from scipy import stats

    y = _norm_values(data, headers)
    sh, ad = shapiro(y), anderson(y)
    table = pd.concat(
        [
            pd.DataFrame({"metric": ["n"], "value": [int(y.size)], "interpretation": ["Count after dropping blanks."]}),
            sh,
            ad.loc[ad["metric"].isin(["anderson_stat", "anderson_critical_5"])],
        ],
        ignore_index=True,
    )
    if not plot:
        return table
    idx = table.set_index("metric")["value"]
    sh_stat, sh_p = float(idx["shapiro_stat"]), float(idx["shapiro_pvalue"])
    ad_stat, crit_5 = float(idx["anderson_stat"]), float(idx["anderson_critical_5"])
    fig, ax = plt.subplots(figsize=(6, 5))
    stats.probplot(y, dist="norm", plot=ax)
    ax.set_title("Q-Q plot")
    ax.text(
        0.02,
        0.98,
        f"Shapiro-Wilk  W = {sh_stat:.3f}  p = {sh_p:.3f}\n"
        f"(If p > 0.05, normal distribution in the data can be assumed)\n"
        f"Anderson-Darling  A^2 = {ad_stat:.3f}  (5% crit. {crit_5:.3f})",
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
 anderson(data, metric=None, headers=False)"""
