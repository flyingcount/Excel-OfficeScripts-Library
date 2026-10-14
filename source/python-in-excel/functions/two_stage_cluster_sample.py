# Name: two_stage_cluster_sample
# Description: Two-stage cluster sample: pick clusters, then rows within each.
# Parameters: data, cluster_col, n_clusters, sample_per_cluster, random_state=42, headers=True

def two_stage_cluster_sample(
    data, cluster_col, n_clusters, sample_per_cluster, random_state=42, headers=True
):
    """Two-stage cluster sample.

    Stage 1: randomly select n_clusters from all clusters. Stage 2: within
    each selected cluster, randomly sample sample_per_cluster rows (or the
    whole cluster if it is smaller).

    data: ref string, DataFrame, Series, or xl() result.
    cluster_col: column that identifies cluster membership.
    n_clusters: how many clusters to select in stage 1.
    sample_per_cluster: how many rows to sample per selected cluster.
    random_state: seed for reproducibility (default 42).
    headers: used only when data is a ref string.
    """
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

    cluster_col = str(pd.Series(cluster_col).iloc[0]).strip()
    if cluster_col not in df.columns:
        lookup = {str(c).strip().lower(): c for c in df.columns}
        key = cluster_col.lower()
        if key not in lookup:
            raise ValueError("cluster_col not found.")
        cluster_col = lookup[key]

    n_clusters = int(pd.Series(n_clusters).iloc[0])
    sample_per_cluster = int(pd.Series(sample_per_cluster).iloc[0])
    random_state = int(pd.Series(random_state).iloc[0])
    if n_clusters < 1:
        raise ValueError("n_clusters must be at least 1.")
    if sample_per_cluster < 1:
        raise ValueError("sample_per_cluster must be at least 1.")

    df = df.copy()
    df[cluster_col] = df[cluster_col].replace("", np.nan)
    df = df.dropna(subset=[cluster_col])
    if df.empty:
        raise ValueError("No rows with a cluster value.")

    all_clusters = df[cluster_col].unique()
    n_all = len(all_clusters)
    if n_clusters > n_all:
        raise ValueError("n_clusters cannot exceed the number of clusters.")

    rng = np.random.default_rng(random_state)
    selected = rng.choice(all_clusters, size=n_clusters, replace=False)
    sampled = []
    for cluster_id in selected:
        cluster_data = df[df[cluster_col] == cluster_id]
        n = min(sample_per_cluster, len(cluster_data))
        sampled.append(cluster_data.sample(n=n, random_state=random_state))
    return pd.concat(sampled).reset_index(drop=True)

"two_stage_cluster_sample(data, cluster_col, n_clusters, sample_per_cluster, random_state=42, headers=True)"
