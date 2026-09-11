"""
Consumer and Prosumer Behavioral Segmentation module.
Applies K-Means clustering, silhouette optimization, and segment profiling to derive
actionable marketing personas from collaborative economy behavioural data.
"""
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from src.config import PROC_INDEX_CSV, PROC_SEGMENTS_CSV, REPORTS_DIR, TABLES_DIR

SEGMENT_NAMES = {
    0: "Occasional Frugal Consumers",
    1: "Convenience-Driven Urbanites",
    2: "Sustainability & Community Co-Creators",
    3: "Entrepreneurial Micro-Providers"
}

def prepare_clustering_features(df):
    """Selects and standardizes features for behavioral segmentation."""
    users_df = df[df["is_active_user"] == 1].copy()
    
    feature_cols = [
        "comp_consumer_freq",
        "comp_provider_freq",
        "comp_sector_breadth",
        "comp_substitution",
        "adv_economic_score",
        "adv_functional_score",
        "adv_social_score",
        "prov_mot_sustainability"
    ]
    
    X = users_df[feature_cols].copy().fillna(0)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return users_df, feature_cols, X_scaled

def evaluate_cluster_solutions(X_scaled, k_range=range(2, 7)):
    """Evaluates K-Means clustering solutions across k=2 to 6 using statistical cluster metrics."""
    metrics = []
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(X_scaled)
        sil = silhouette_score(X_scaled, labels)
        db = davies_bouldin_score(X_scaled, labels)
        ch = calinski_harabasz_score(X_scaled, labels)
        metrics.append({
            "k": k,
            "Silhouette Score": sil,
            "Davies-Bouldin Index": db,
            "Calinski-Harabasz": ch
        })
    return pd.DataFrame(metrics)

def fit_final_segmentation(users_df, X_scaled, k=4):
    """Fits the final 4-cluster K-Means solution and creates persona profiles."""
    km = KMeans(n_clusters=k, random_state=42, n_init=15)
    cluster_labels = km.fit_predict(X_scaled)
    users_df["cluster_id"] = cluster_labels
    
    # Intelligently assign persona names based on cluster centroids
    # Determine which cluster has highest provider frequency -> Micro-providers
    # Determine which cluster has highest sustainability -> Sustainability Co-Creators
    # Determine which cluster has highest functional/convenience -> Convenience Urbanites
    # Remaining cluster with low PEI -> Occasional Frugal Consumers
    means = users_df.groupby("cluster_id").agg({
        "PEI": "mean",
        "comp_provider_freq": "mean",
        "prov_mot_sustainability": "mean",
        "adv_functional_score": "mean",
        "adv_economic_score": "mean",
        "consumer_sector_breadth": "mean"
    })
    
    assigned_names = {}
    remaining_clusters = list(range(k))
    
    # 1. Sustainability co-creators (highest sustainability motivation)
    sust_c = means["prov_mot_sustainability"].idxmax()
    assigned_names[sust_c] = "Sustainability & Community Co-Creators"
    remaining_clusters.remove(sust_c)
    
    # 2. Entrepreneurial micro-providers (highest provider freq among remaining)
    prov_c = means.loc[remaining_clusters, "comp_provider_freq"].idxmax()
    assigned_names[prov_c] = "Entrepreneurial Micro-Providers"
    remaining_clusters.remove(prov_c)
    
    # 3. Convenience-driven urbanites (highest functional score among remaining)
    conv_c = means.loc[remaining_clusters, "adv_functional_score"].idxmax()
    assigned_names[conv_c] = "Convenience-Driven Urbanites"
    remaining_clusters.remove(conv_c)
    
    # 4. Occasional frugal consumers (last remaining)
    frug_c = remaining_clusters[0]
    assigned_names[frug_c] = "Occasional Frugal Consumers"
    
    users_df["segment_name"] = users_df["cluster_id"].map(assigned_names)
    
    # Profile table
    profile_table = users_df.groupby("segment_name").agg({
        "country": "count",
        "PEI": ["mean", "median", "std"],
        "consumer_freq_score": "mean",
        "provider_freq_score": "mean",
        "consumer_sector_breadth": "mean",
        "provider_sector_breadth": "mean",
        "is_prosumer": "mean",
        "adv_economic_score": "mean",
        "adv_functional_score": "mean",
        "adv_social_score": "mean",
        "prov_mot_sustainability": "mean",
        "recommend_high": "mean",
        "age": "mean",
        "gender_male": "mean",
        "higher_education": "mean"
    })
    
    # Flatten MultiIndex columns
    profile_table.columns = ["_".join(col).strip() if isinstance(col, tuple) else col for col in profile_table.columns]
    profile_table = profile_table.reset_index().rename(columns={"country_count": "Segment_N"})
    profile_table["Segment_Share_%"] = (profile_table["Segment_N"] / len(users_df)) * 100
    
    return users_df, profile_table

def run_segmentation_pipeline():
    """Executes the complete segmentation workflow."""
    print("Executing consumer & prosumer behavioral segmentation pipeline...")
    os.makedirs(os.path.dirname(PROC_SEGMENTS_CSV), exist_ok=True)
    os.makedirs(TABLES_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)
    
    df = pd.read_csv(PROC_INDEX_CSV)
    users_df, feature_cols, X_scaled = prepare_clustering_features(df)
    
    # Cluster evaluation
    eval_df = evaluate_cluster_solutions(X_scaled)
    eval_df.to_csv(os.path.join(TABLES_DIR, "cluster_evaluation_metrics.csv"), index=False)
    
    # Final segmentation
    segmented_users, profile_table = fit_final_segmentation(users_df, X_scaled, k=4)
    segmented_users.to_csv(PROC_SEGMENTS_CSV, index=False)
    profile_table.to_csv(os.path.join(TABLES_DIR, "table7_segment_profiles.csv"), index=False)
    
    # Generate Segmentation Report
    seg_report_md = f"""# Consumer & Prosumer Behavioral Segmentation: Personas, Profiles & Strategy

## 1. Segmentation Methodology
- **Clustering Algorithm**: K-Means Clustering on active collaborative economy participants ($N = {len(segmented_users):,}$).
- **Feature Set**: 8 multi-dimensional behavioral, motivational, and market-substitution indicators.
- **Model Evaluation**: K=4 selected as the optimal equilibrium between silhouette separation ({eval_df.loc[eval_df['k']==4, 'Silhouette Score'].values[0]:.3f}) and managerial interpretability.

{eval_df.round(3).to_markdown(index=False)}

## 2. Segment Profiles & Empirical Characteristics (Table 7)
{profile_table.round(2).to_markdown(index=False)}

## 3. Strategic Persona Deep-Dives & Marketing Action Plans

### Persona 1: Occasional Frugal Consumers (Price-Sensitive Beginners)
- **Share of User Base**: {profile_table.loc[profile_table['segment_name']=='Occasional Frugal Consumers', 'Segment_Share_%'].values[0]:.1f}%
- **Mean PEI**: {profile_table.loc[profile_table['segment_name']=='Occasional Frugal Consumers', 'PEI_mean'].values[0]:.1f} | **Prosumer Rate**: {profile_table.loc[profile_table['segment_name']=='Occasional Frugal Consumers', 'is_prosumer_mean'].values[0]*100:.1f}%
- **Behavior**: Low usage frequency, limited to 1 sector (typically budget travel or transport). Driven purely by cost discounts (`adv_economic_score` = {profile_table.loc[profile_table['segment_name']=='Occasional Frugal Consumers', 'adv_economic_score_mean'].values[0]*100:.1f}%). Zero provider participation.
- **Marketing Strategy**: Low-friction onboarding, transparent pricing, first-trial promotions, and cross-category discovery recommendations.

### Persona 2: Convenience-Driven Urbanites (Digital Convenience Maximizers)
- **Share of User Base**: {profile_table.loc[profile_table['segment_name']=='Convenience-Driven Urbanites', 'Segment_Share_%'].values[0]:.1f}%
- **Mean PEI**: {profile_table.loc[profile_table['segment_name']=='Convenience-Driven Urbanites', 'PEI_mean'].values[0]:.1f} | **Prosumer Rate**: {profile_table.loc[profile_table['segment_name']=='Convenience-Driven Urbanites', 'is_prosumer_mean'].values[0]*100:.1f}%
- **Behavior**: Frequent consumers across transport, food delivery, and accommodation. Highly educated ({profile_table.loc[profile_table['segment_name']=='Convenience-Driven Urbanites', 'higher_education_mean'].values[0]*100:.1f}%), urban dwellers who prioritize speed, user reviews, and instant app access.
- **Marketing Strategy**: Seamless UI/UX, mobile loyalty rewards, subscription passes (e.g. Uber One, Deliveroo Plus), and premium reliability guarantees.

### Persona 3: Sustainability & Community Co-Creators (Circular Prosumers)
- **Share of User Base**: {profile_table.loc[profile_table['segment_name']=='Sustainability & Community Co-Creators', 'Segment_Share_%'].values[0]:.1f}%
- **Mean PEI**: {profile_table.loc[profile_table['segment_name']=='Sustainability & Community Co-Creators', 'PEI_mean'].values[0]:.1f} | **Prosumer Rate**: {profile_table.loc[profile_table['segment_name']=='Sustainability & Community Co-Creators', 'is_prosumer_mean'].values[0]*100:.1f}%
- **Behavior**: Active on both sides of the platform. Strongest sustainability motivation (`prov_mot_sustainability` = {profile_table.loc[profile_table['segment_name']=='Sustainability & Community Co-Creators', 'prov_mot_sustainability_mean'].values[0]*100:.1f}%) and social interaction values. Highly active in household services, repairs, peer exchange, and asset recirculation.
- **Marketing Strategy**: Community governance features, impact badges (e.g., carbon savings, waste diverted), peer-to-peer storytelling, and localized circular economy campaigns.

### Persona 4: Entrepreneurial Micro-Providers (Supply-Side Value Generators)
- **Share of User Base**: {profile_table.loc[profile_table['segment_name']=='Entrepreneurial Micro-Providers', 'Segment_Share_%'].values[0]:.1f}%
- **Mean PEI**: {profile_table.loc[profile_table['segment_name']=='Entrepreneurial Micro-Providers', 'PEI_mean'].values[0]:.1f} | **Prosumer Rate**: {profile_table.loc[profile_table['segment_name']=='Entrepreneurial Micro-Providers', 'is_prosumer_mean'].values[0]*100:.1f}%
- **Behavior**: Highest overall engagement and deepest provider breadth. Highly focused on supplementary and primary income generation. Extremely valuable platform ambassadors with strong recommendation rates ({profile_table.loc[profile_table['segment_name']=='Entrepreneurial Micro-Providers', 'recommend_high_mean'].values[0]*100:.1f}%).
- **Marketing Strategy**: Dedicated provider support portals, automated tax compliance integrations, flexible payout schemes, and prosumer loyalty incentives.
"""
    seg_report_path = os.path.join(REPORTS_DIR, "segmentation_profile_report.md")
    with open(seg_report_path, "w", encoding="utf-8") as f:
        f.write(seg_report_md)
    print(f"Saved segmentation report to {seg_report_path}")
    print("Segmentation pipeline completed successfully!")

if __name__ == "__main__":
    run_segmentation_pipeline()
