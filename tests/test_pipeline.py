"""
Unit and integration test suite for the Prosumer Behavioral Index research pipeline.
Verifies data loading, cleaning, index calculations, statistical models, segmentation, and report exports.
"""
import os
import pytest
import pandas as pd
import numpy as np
from src.config import (
    RAW_CSV_PATH, PROC_FULL_CSV, PROC_USERS_CSV, PROC_INDEX_CSV,
    PROC_SEGMENTS_CSV, FIGURES_DIR, REPORTS_DIR, TABLES_DIR, DASHBOARD_DIR
)

def test_raw_data_dimensions():
    """Verify that the official raw Eurobarometer 467 CSV loads with correct dimensions."""
    assert os.path.exists(RAW_CSV_PATH), f"Raw data file missing at {RAW_CSV_PATH}"
    df = pd.read_csv(RAW_CSV_PATH, sep="~", encoding="utf-8-sig", nrows=10)
    assert df.shape[1] == 326, f"Expected 326 columns, got {df.shape[1]}"

def test_cleaned_datasets_exist():
    """Verify processed full and user datasets exist and have expected structure."""
    assert os.path.exists(PROC_FULL_CSV), "fl467_full_cleaned.csv missing"
    assert os.path.exists(PROC_USERS_CSV), "fl467_cleaned_users.csv missing"
    
    full_df = pd.read_csv(PROC_FULL_CSV)
    users_df = pd.read_csv(PROC_USERS_CSV)
    
    assert len(full_df) == 26544, f"Expected 26,544 rows in full dataset, got {len(full_df)}"
    assert len(users_df) == 5872, f"Expected 5,872 active users, got {len(users_df)}"
    assert "user_profile" in full_df.columns
    assert "is_prosumer" in full_df.columns

def test_pei_score_properties():
    """Verify Prosumer Engagement Index properties and boundary conditions."""
    assert os.path.exists(PROC_INDEX_CSV), "fl467_prosumer_index.csv missing"
    idf = pd.read_csv(PROC_INDEX_CSV)
    
    # Boundary check
    assert idf["PEI"].min() >= 0.0, "PEI cannot be negative"
    assert idf["PEI"].max() <= 100.0, "PEI cannot exceed 100.0"
    assert idf["PEI"].isna().sum() == 0, "PEI contains NaN values"
    
    # Monotonic role hierarchy
    mean_cons = idf[idf["user_profile"] == "Consumer Only"]["PEI"].mean()
    mean_pros = idf[idf["user_profile"] == "Prosumer"]["PEI"].mean()
    assert mean_pros > mean_cons, f"Prosumers ({mean_pros:.2f}) must have higher mean PEI than consumers ({mean_cons:.2f})"

def test_statistical_tables_exist():
    """Verify statistical results and hypothesis tables are populated."""
    t5_path = os.path.join(TABLES_DIR, "table5_hypothesis_tests.csv")
    t6a_path = os.path.join(TABLES_DIR, "table6a_logistic_prosumer_status.csv")
    
    assert os.path.exists(t5_path), "table5_hypothesis_tests.csv missing"
    assert os.path.exists(t6a_path), "table6a_logistic_prosumer_status.csv missing"
    
    h_df = pd.read_csv(t5_path)
    assert len(h_df) == 5, f"Expected 5 hypothesis test records, got {len(h_df)}"

def test_segmentation_output():
    """Verify K-Means segmentation outputs and cluster assignments."""
    assert os.path.exists(PROC_SEGMENTS_CSV), "prosumer_segments.csv missing"
    seg_df = pd.read_csv(PROC_SEGMENTS_CSV)
    
    assert len(seg_df) == 5872, "Segmentation must assign all active users"
    assert "segment_name" in seg_df.columns
    assert seg_df["segment_name"].nunique() == 4, "Expected 4 distinct personas"

def test_figures_and_dashboard_generated():
    """Verify all 13 figures and HTML dashboard exist."""
    expected_figs = [
        "fig1_awareness_and_participation.png",
        "fig2_consumer_usage_frequency.png",
        "fig3_provider_frequency.png",
        "fig4_consumer_vs_prosumer_comparison.png",
        "fig5_consumer_sector_breadth.png",
        "fig6_provider_sector_breadth.png",
        "fig7_prosumer_rate_by_age.png",
        "fig8_prosumer_rate_by_gender_and_education.png",
        "fig9_prosumer_rate_by_occupation.png",
        "fig10_consumer_perceived_advantages.png",
        "fig11_provider_motivations_sustainability.png",
        "fig12_consumer_and_provider_barriers.png",
        "fig13_cluster_centroids_profile.png"
    ]
    for fig_name in expected_figs:
        fig_path = os.path.join(FIGURES_DIR, fig_name)
        assert os.path.exists(fig_path), f"Figure missing: {fig_name}"
        
    dash_html = os.path.join(DASHBOARD_DIR, "index.html")
    assert os.path.exists(dash_html), "dashboard/index.html missing"
    with open(dash_html, "r", encoding="utf-8") as f:
        html = f.read()
    assert "plotly" in html.lower(), "Dashboard HTML missing Plotly references"
