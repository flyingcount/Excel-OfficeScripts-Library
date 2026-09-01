# Python in Excel sampling library
#
# Formulas → Initialization → replace the editor contents with this file → Save.
# This file is a complete Initialization: Excel defaults, then sampling functions only.
#
# Full library (all functions): paste init/PaulPythonLibrary.py instead.
# Restore defaults only: paste init/DefaultInitialization.py instead.
#
# Requires Microsoft 365 Python in Excel. Functions use Excel's xl() helper.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels as sm
import excel
import warnings

warnings.simplefilter('ignore')

excel.set_xl_scalar_conversion(excel.convert_to_scalar)
excel.set_xl_array_conversion(excel.convert_to_dataframe)


def stratified_sample(data, strata_col, total_n, random_state=42, headers=True):
    """Draw a proportional stratified sample.

    Each stratum gets round(total_n * its share of the population) rows,
    at least 1 when the stratum is non-empty, capped at the stratum size.

    data: ref string, DataFrame, Series, or xl() result.
    strata_col: column name that defines the strata.
    total_n: target sample size across all strata.
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

    strata_col = str(pd.Series(strata_col).iloc[0]).strip()
    if strata_col not in df.columns:
        lookup = {str(c).strip().lower(): c for c in df.columns}
        key = strata_col.lower()
        if key not in lookup:
            raise ValueError("strata_col not found.")
        strata_col = lookup[key]

    total_n = int(pd.Series(total_n).iloc[0])
    random_state = int(pd.Series(random_state).iloc[0])
    if total_n < 1:
        raise ValueError("total_n must be at least 1.")

    df = df.copy()
    df[strata_col] = df[strata_col].replace("", np.nan)
    df = df.dropna(subset=[strata_col])
    if df.empty:
        raise ValueError("No rows with a stratum value.")

    pop = len(df)
    sampled = []
    for _, group in df.groupby(strata_col, dropna=True):
        n = max(1, int(round(total_n * len(group) / pop)))
        n = min(n, len(group))
        sampled.append(group.sample(n=n, random_state=random_state))
    return pd.concat(sampled).reset_index(drop=True)

"stratified_sample(data, strata_col, total_n, random_state=42, headers=True)"


def systematic_sample(data, sample_size, random_state=42, headers=True):
    """Draw a systematic sample of rows.

    Interval k = N // sample_size. Start is random in 0..k-1. Then every
    kth row: start, start+k, start+2k, ... trimmed to sample_size.

    data: ref string, DataFrame, Series, list, or xl() result.
    sample_size: number of rows to return. Must be 1..N.
    random_state: seed for the start position (default 42).
    headers: used only when data is a ref string.
    """
    import random

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

    sample_size = int(pd.Series(sample_size).iloc[0])
    random_state = int(pd.Series(random_state).iloc[0])
    n = len(df)
    if sample_size < 1:
        raise ValueError("sample_size must be at least 1.")
    if sample_size > n:
        raise ValueError("sample_size cannot exceed population size.")

    k = n // sample_size
    start = random.Random(random_state).randint(0, k - 1)
    idx = list(range(start, n, k))[:sample_size]
    return df.iloc[idx].reset_index(drop=True)

"systematic_sample(data, sample_size, random_state=42, headers=True)"


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
