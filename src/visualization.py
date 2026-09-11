"""
Publication-quality visualization module for Prosumer Engagement Index (PEI) research.
Generates all 12 publication figures using Matplotlib and Seaborn with clean academic styling.
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from src.config import (
    PROC_INDEX_CSV, PROC_SEGMENTS_CSV, FIGURES_DIR,
    ADVANTAGE_COLS, DISADVANTAGE_COLS, PROVIDER_MOTIVATION_COLS, PALETTE
)

# Academic styling settings
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
plt.rcParams["axes.edgecolor"] = "#CBD5E1"
plt.rcParams["axes.linewidth"] = 0.8
plt.rcParams["grid.color"] = "#F1F5F9"
plt.rcParams["grid.linestyle"] = "--"

def save_fig(fig, filename):
    os.makedirs(FIGURES_DIR, exist_ok=True)
    path = os.path.join(FIGURES_DIR, filename)
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved figure to {path}")

def generate_figure1_awareness_participation(df):
    """Figure 1: Collaborative-platform awareness and participation breakdown."""
    fig, ax = plt.subplots(figsize=(9, 5))
    
    # Categories: Non-users, Consumer only, Prosumer, Provider only
    counts = df["user_profile"].value_counts()
    categories = ["Non-User", "Consumer Only", "Prosumer", "Provider Only"]
    vals = [counts.get(c, 0) for c in categories]
    pcts = [v / len(df) * 100 for v in vals]
    colors = [PALETTE["non_user"], PALETTE["consumer"], PALETTE["prosumer"], PALETTE["provider"]]
    
    bars = ax.barh(categories, pcts, color=colors, height=0.55, edgecolor="none")
    ax.set_xlabel("Share of EU-28 Population (%)", fontsize=11, fontweight="bold", labelpad=8)
    ax.set_title("Figure 1: Collaborative Platform Market Participation Structure (EU-28, N=26,544)", 
                 fontsize=13, fontweight="bold", pad=12)
    ax.set_xlim(0, 85)
    
    for bar, pct, val in zip(bars, pcts, vals):
        ax.text(bar.get_width() + 1.0, bar.get_y() + bar.get_height()/2, 
                f"{pct:.1f}%  (n = {val:,})", va="center", fontsize=10, fontweight="bold", color="#1E293B")
        
    sns.despine(left=True, bottom=True)
    save_fig(fig, "fig1_awareness_and_participation.png")

def generate_figure2_consumer_frequency(df):
    """Figure 2: Consumer usage frequency distribution."""
    fig, ax = plt.subplots(figsize=(8, 5))
    
    cons_df = df[df["is_consumer"] == 1]
    order = ["Once or few times", "Occasionally", "Regularly"]
    counts = cons_df["consumer_freq_label"].value_counts()[order]
    pcts = counts / len(cons_df) * 100
    
    bars = ax.bar(order, pcts, color=PALETTE["consumer"], width=0.45, edgecolor="none")
    ax.set_ylabel("Share of Collaborative Consumers (%)", fontsize=11, fontweight="bold", labelpad=8)
    ax.set_title("Figure 2: Consumer Usage Frequency Distribution (N=5,590)", fontsize=13, fontweight="bold", pad=12)
    ax.set_ylim(0, 55)
    
    for bar, pct, count in zip(bars, pcts, counts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.2,
                f"{pct:.1f}% (n={count:,})", ha="center", fontsize=10, fontweight="bold", color="#1E293B")
        
    sns.despine(top=True, right=True)
    save_fig(fig, "fig2_consumer_usage_frequency.png")

def generate_figure3_provider_frequency(df):
    """Figure 3: Provider offering frequency distribution."""
    fig, ax = plt.subplots(figsize=(8, 5))
    
    prov_df = df[df["is_provider"] == 1]
    order = ["Once or few times", "Occasionally", "Regularly"]
    counts = prov_df["provider_freq_label"].value_counts()[order]
    pcts = counts / len(prov_df) * 100
    
    bars = ax.bar(order, pcts, color=PALETTE["provider"], width=0.45, edgecolor="none")
    ax.set_ylabel("Share of Service Providers (%)", fontsize=11, fontweight="bold", labelpad=8)
    ax.set_title("Figure 3: Service Provider Offering Frequency Distribution (N=1,431)", fontsize=13, fontweight="bold", pad=12)
    ax.set_ylim(0, 60)
    
    for bar, pct, count in zip(bars, pcts, counts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.2,
                f"{pct:.1f}% (n={count:,})", ha="center", fontsize=10, fontweight="bold", color="#1E293B")
        
    sns.despine(top=True, right=True)
    save_fig(fig, "fig3_provider_frequency.png")

def generate_figure4_consumer_vs_prosumer(df):
    """Figure 4: Consumer vs Prosumer behavioral profile comparison."""
    fig, ax = plt.subplots(figsize=(10, 5.5))
    
    users = df[df["user_profile"].isin(["Consumer Only", "Prosumer"])].copy()
    metrics = {
        "Consumer Sector Breadth (Mean)": users.groupby("user_profile")["consumer_sector_breadth"].mean(),
        "Market Substitution Rate (%)": users.groupby("user_profile")["is_substitutor"].mean() * 100,
        "Strong Recommendation Rate (%)": users.groupby("user_profile")["recommend_high"].mean() * 100,
        "Social Value Orientation (%)": users.groupby("user_profile")["adv_social_score"].mean() * 100,
        "Future Provider Intent (%)": users.groupby("user_profile")["future_offer_intent"].mean() * 100
    }
    comp_df = pd.DataFrame(metrics).T
    
    x = np.arange(len(comp_df))
    width = 0.35
    
    rects1 = ax.bar(x - width/2, comp_df["Consumer Only"], width, label="Consumer Only (N=4,441)", color=PALETTE["consumer"])
    rects2 = ax.bar(x + width/2, comp_df["Prosumer"], width, label="Prosumer (N=1,149)", color=PALETTE["prosumer"])
    
    ax.set_ylabel("Score / Percentage (%)", fontsize=11, fontweight="bold", labelpad=8)
    ax.set_title("Figure 4: Behavioral Comparison: Consumer-Only vs. Dual Prosumers", fontsize=13, fontweight="bold", pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(comp_df.index, fontsize=9.5, fontweight="bold")
    ax.legend(frameon=True, facecolor="white", edgecolor="#E2E8F0", loc="upper left")
    
    for r in rects1:
        h = r.get_height()
        ax.text(r.get_x() + r.get_width()/2, h + 1.0, f"{h:.1f}", ha="center", fontsize=8.5, color="#1E293B")
    for r in rects2:
        h = r.get_height()
        ax.text(r.get_x() + r.get_width()/2, h + 1.0, f"{h:.1f}", ha="center", fontsize=8.5, fontweight="bold", color="#5B21B6")
        
    ax.set_ylim(0, max(comp_df.max()) * 1.15)
    sns.despine(top=True, right=True)
    save_fig(fig, "fig4_consumer_vs_prosumer_comparison.png")

def generate_figure5_and_6_sectors(df):
    """Figures 5 & 6: Number of sectors used and offered."""
    # Figure 5: Consumer sectors used
    fig5, ax5 = plt.subplots(figsize=(8, 5))
    cons_users = df[df["is_consumer"] == 1]
    counts5 = cons_users["consumer_sector_breadth"].value_counts().sort_index()
    pcts5 = counts5 / len(cons_users) * 100
    
    bars5 = ax5.bar(counts5.index, pcts5, color=PALETTE["consumer"], width=0.55)
    ax5.set_xlabel("Number of Collaborative Sectors Used", fontsize=11, fontweight="bold", labelpad=8)
    ax5.set_ylabel("Share of Consumers (%)", fontsize=11, fontweight="bold", labelpad=8)
    ax5.set_title("Figure 5: Sector Breadth of Collaborative Consumption (N=5,590)", fontsize=13, fontweight="bold", pad=12)
    ax5.set_xticks(range(0, 7))
    for b, p in zip(bars5, pcts5):
        if p > 0.5:
            ax5.text(b.get_x() + b.get_width()/2, b.get_height() + 1.0, f"{p:.1f}%", ha="center", fontsize=9, fontweight="bold")
    sns.despine(top=True, right=True)
    save_fig(fig5, "fig5_consumer_sector_breadth.png")
    
    # Figure 6: Provider sectors offered
    fig6, ax6 = plt.subplots(figsize=(8, 5))
    prov_users = df[df["is_provider"] == 1]
    counts6 = prov_users["provider_sector_breadth"].value_counts().sort_index()
    pcts6 = counts6 / len(prov_users) * 100
    
    bars6 = ax6.bar(counts6.index, pcts6, color=PALETTE["provider"], width=0.55)
    ax6.set_xlabel("Number of Collaborative Sectors Offered", fontsize=11, fontweight="bold", labelpad=8)
    ax6.set_ylabel("Share of Service Providers (%)", fontsize=11, fontweight="bold", labelpad=8)
    ax6.set_title("Figure 6: Sector Breadth of Collaborative Provision (N=1,431)", fontsize=13, fontweight="bold", pad=12)
    ax6.set_xticks(range(0, 7))
    for b, p in zip(bars6, pcts6):
        if p > 0.5:
            ax6.text(b.get_x() + b.get_width()/2, b.get_height() + 1.0, f"{p:.1f}%", ha="center", fontsize=9, fontweight="bold")
    sns.despine(top=True, right=True)
    save_fig(fig6, "fig6_provider_sector_breadth.png")

def generate_figure7_age_demographics(df):
    """Figure 7: Prosumer rate and user rate by age cohort."""
    fig, ax = plt.subplots(figsize=(9, 5))
    
    age_cohorts = ["15-24", "25-34", "35-44", "45-54", "55-64", "65+"]
    age_df = df[df["age_cohort"].isin(age_cohorts)].groupby("age_cohort").agg({
        "is_active_user": lambda x: x.mean() * 100,
        "is_prosumer": lambda x: x.mean() * 100,
        "PEI": "mean"
    }).loc[age_cohorts]
    
    x = np.arange(len(age_cohorts))
    width = 0.35
    
    r1 = ax.bar(x - width/2, age_df["is_active_user"], width, label="Active Platform User Rate (%)", color=PALETTE["consumer"])
    r2 = ax.bar(x + width/2, age_df["is_prosumer"], width, label="Prosumer Rate (%)", color=PALETTE["prosumer"])
    
    ax.set_ylabel("Population Rate (%)", fontsize=11, fontweight="bold", labelpad=8)
    ax.set_title("Figure 7: Collaborative Platform Adoption & Prosumption by Age Cohort (EU-28)", fontsize=13, fontweight="bold", pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(age_cohorts, fontsize=10, fontweight="bold")
    ax.legend(frameon=True, facecolor="white", loc="upper right")
    
    for r in r1:
        ax.text(r.get_x() + r.get_width()/2, r.get_height() + 0.8, f"{r.get_height():.1f}%", ha="center", fontsize=8.5)
    for r in r2:
        ax.text(r.get_x() + r.get_width()/2, r.get_height() + 0.8, f"{r.get_height():.1f}%", ha="center", fontsize=8.5, fontweight="bold", color="#5B21B6")
        
    ax.set_ylim(0, 45)
    sns.despine(top=True, right=True)
    save_fig(fig, "fig7_prosumer_rate_by_age.png")

def generate_figure8_gender_education(df):
    """Figure 8: Prosumer rate and PEI by Gender and Education Level."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Subplot 1: Gender
    gender_df = df[df["gender"].isin(["Male", "Female"])].groupby("gender").agg({
        "is_active_user": lambda x: x.mean() * 100,
        "is_prosumer": lambda x: x.mean() * 100,
        "PEI": "mean"
    })
    x_g = np.arange(len(gender_df))
    ax1.bar(x_g - 0.17, gender_df["is_active_user"], 0.34, label="User Rate (%)", color=PALETTE["consumer"])
    ax1.bar(x_g + 0.17, gender_df["is_prosumer"], 0.34, label="Prosumer Rate (%)", color=PALETTE["prosumer"])
    ax1.set_title("Adoption by Gender", fontsize=12, fontweight="bold", pad=10)
    ax1.set_xticks(x_g)
    ax1.set_xticklabels(gender_df.index, fontweight="bold")
    ax1.set_ylabel("Rate (%)", fontweight="bold")
    ax1.legend(frameon=True, facecolor="white")
    ax1.set_ylim(0, 32)
    
    # Subplot 2: Education
    edu_order = ["Up to 15 yrs", "16-19 yrs", "20+ yrs (Higher Edu)", "Still Studying"]
    edu_df = df[df["education_level"].isin(edu_order)].groupby("education_level").agg({
        "is_active_user": lambda x: x.mean() * 100,
        "is_prosumer": lambda x: x.mean() * 100,
        "PEI": "mean"
    }).loc[edu_order]
    x_e = np.arange(len(edu_order))
    ax2.bar(x_e - 0.17, edu_df["is_active_user"], 0.34, label="User Rate (%)", color=PALETTE["consumer"])
    ax2.bar(x_e + 0.17, edu_df["is_prosumer"], 0.34, label="Prosumer Rate (%)", color=PALETTE["prosumer"])
    ax2.set_title("Adoption by Education Level", fontsize=12, fontweight="bold", pad=10)
    ax2.set_xticks(x_e)
    ax2.set_xticklabels(edu_order, rotation=15, ha="right", fontsize=9, fontweight="bold")
    ax2.legend(frameon=True, facecolor="white")
    ax2.set_ylim(0, 42)
    
    plt.suptitle("Figure 8: Prosumer Participation Disparities by Gender and Education Level", fontsize=13, fontweight="bold", y=1.02)
    sns.despine(top=True, right=True)
    save_fig(fig, "fig8_prosumer_rate_by_gender_and_education.png")

def generate_figure9_occupation(df):
    """Figure 9: Prosumer rate by occupation group."""
    fig, ax = plt.subplots(figsize=(9, 5))
    
    occ_order = ["Self-employed", "Employee", "Manual Worker", "Not Working / Retired / Student"]
    occ_df = df[df["occupation_group"].isin(occ_order)].groupby("occupation_group").agg({
        "is_active_user": lambda x: x.mean() * 100,
        "is_prosumer": lambda x: x.mean() * 100
    }).loc[occ_order]
    
    x = np.arange(len(occ_order))
    width = 0.35
    
    r1 = ax.bar(x - width/2, occ_df["is_active_user"], width, label="Active User Rate (%)", color=PALETTE["consumer"])
    r2 = ax.bar(x + width/2, occ_df["is_prosumer"], width, label="Prosumer Rate (%)", color=PALETTE["prosumer"])
    
    ax.set_ylabel("Population Share (%)", fontsize=11, fontweight="bold", labelpad=8)
    ax.set_title("Figure 9: Platform Participation and Prosumption by Occupation Group", fontsize=13, fontweight="bold", pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(occ_order, fontsize=10, fontweight="bold")
    ax.legend(frameon=True, facecolor="white")
    ax.set_ylim(0, 38)
    
    for r in r1:
        ax.text(r.get_x() + r.get_width()/2, r.get_height() + 0.8, f"{r.get_height():.1f}%", ha="center", fontsize=8.5)
    for r in r2:
        ax.text(r.get_x() + r.get_width()/2, r.get_height() + 0.8, f"{r.get_height():.1f}%", ha="center", fontsize=8.5, fontweight="bold", color="#5B21B6")
        
    sns.despine(top=True, right=True)
    save_fig(fig, "fig9_prosumer_rate_by_occupation.png")

def generate_figure10_consumer_advantages(df):
    """Figure 10: Perceived consumer advantages and value orientations."""
    fig, ax = plt.subplots(figsize=(10, 5))
    
    cons_df = df[df["is_consumer"] == 1]
    adv_rates = {
        "Cheaper or Free (Economic)": cons_df["adv_cheaper"].mean() * 100,
        "More Convenient Access (Functional)": cons_df["adv_convenient"].mean() * 100,
        "Ratings & Reviews (Informational)": cons_df["adv_ratings"].mean() * 100,
        "Wider Choice (Functional)": cons_df["adv_wider"].mean() * 100,
        "Social Interaction (Social)": cons_df["adv_social"].mean() * 100,
        "Exchanging Services (Collaborative)": cons_df["adv_exchange"].mean() * 100
    }
    s_adv = pd.Series(adv_rates).sort_values(ascending=True)
    
    colors = ["#94A3B8", "#94A3B8", "#38BDF8", "#0284C7", "#0EA5E9", "#1D4ED8"]
    bars = ax.barh(s_adv.index, s_adv.values, color=colors, height=0.55)
    ax.set_xlabel("Percentage of Collaborative Consumers Endorsing Advantage (%)", fontsize=11, fontweight="bold", labelpad=8)
    ax.set_title("Figure 10: Perceived Value Dimensions of Collaborative Platform Use (N=5,590)", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlim(0, 75)
    
    for b in bars:
        ax.text(b.get_width() + 1.0, b.get_y() + b.get_height()/2, f"{b.get_width():.1f}%", va="center", fontsize=10, fontweight="bold")
        
    sns.despine(left=True, bottom=True)
    save_fig(fig, "fig10_consumer_perceived_advantages.png")

def generate_figure11_provider_motivations(df):
    """Figure 11: Service provider motivations (Highlighting Sustainability)."""
    fig, ax = plt.subplots(figsize=(10, 5.5))
    
    prov_df = df[df["is_provider"] == 1]
    mot_rates = {
        "Additional Income (Economic)": prov_df["prov_mot_q11_2"].mean() * 100,
        "Flexible Working Hours (Autonomy)": prov_df["prov_mot_q11_3"].mean() * 100,
        "Easy Opportunity to Provide (Access)": prov_df["prov_mot_q11_4"].mean() * 100,
        "Access to More Consumers (Reach)": prov_df["prov_mot_q11_6"].mean() * 100,
        "Sustainable & Efficient Asset Use (Sustainability)": prov_df["prov_mot_q11_8"].mean() * 100,
        "Easy Consumer Interaction (Social)": prov_df["prov_mot_q11_7"].mean() * 100,
        "Offer Innovative Services (Innovation)": prov_df["prov_mot_q11_5"].mean() * 100,
        "Main Income Source (Primary Livelihood)": prov_df["prov_mot_q11_1"].mean() * 100
    }
    s_mot = pd.Series(mot_rates).sort_values(ascending=True)
    
    # Highlight sustainability with distinct emerald color
    colors = [PALETTE["secondary"] if "Sustainability" in k else "#3B82F6" for k in s_mot.index]
    bars = ax.barh(s_mot.index, s_mot.values, color=colors, height=0.55)
    
    ax.set_xlabel("Percentage of Service Providers Endorsing Reason (%)", fontsize=11, fontweight="bold", labelpad=8)
    ax.set_title("Figure 11: Service Provider Value Motivations (N=1,431, Highlight: Sustainability)", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlim(0, 65)
    
    for b in bars:
        ax.text(b.get_width() + 1.0, b.get_y() + b.get_height()/2, f"{b.get_width():.1f}%", va="center", fontsize=9.5, fontweight="bold")
        
    sns.despine(left=True, bottom=True)
    save_fig(fig, "fig11_provider_motivations_sustainability.png")

def generate_figure12_participation_barriers(df):
    """Figure 12: Barriers preventing consumer and provider adoption."""
    from src.config import RAW_CSV_PATH
    raw_df = pd.read_csv(RAW_CSV_PATH, sep="~", encoding="utf-8-sig", low_memory=False)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    
    # Non-user consumer barriers (q1.1 to q1.6)
    non_user_mask = (df["user_profile"] == "Non-User").values
    raw_non_users = raw_df[non_user_mask]
    c_barriers = {
        "Don't Know What Platforms Are": (pd.to_numeric(raw_non_users["q1.1"], errors="coerce") == 1).mean() * 100,
        "Prefer Traditional Channels": (pd.to_numeric(raw_non_users["q1.5"], errors="coerce") == 1).mean() * 100,
        "Lack of Trust in Services": (pd.to_numeric(raw_non_users["q1.4"], errors="coerce") == 1).mean() * 100,
        "Lack of Technical Knowledge": (pd.to_numeric(raw_non_users["q1.3"], errors="coerce") == 1).mean() * 100,
        "Data Privacy Concerns": (pd.to_numeric(raw_non_users["q1.6"], errors="coerce") == 1).mean() * 100,
        "Poor Internet Access": (pd.to_numeric(raw_non_users["q1.2"], errors="coerce") == 1).mean() * 100
    }
    s_cb = pd.Series(c_barriers).sort_values(ascending=True)
    ax1.barh(s_cb.index, s_cb.values, color="#E11D48", height=0.55)
    ax1.set_title("Non-Consumer Barriers (N=20,672)", fontsize=11, fontweight="bold")
    ax1.set_xlabel("% Endorsement", fontweight="bold")
    ax1.set_xlim(0, 50)
    for b in ax1.patches:
        ax1.text(b.get_width() + 0.8, b.get_y() + b.get_height()/2, f"{b.get_width():.1f}%", va="center", fontsize=9)
        
    # Non-provider barriers (q8.1 to q8.8)
    non_prov_mask = (df["is_provider"] == 0).values
    raw_non_prov = raw_df[non_prov_mask]
    p_barriers = {
        "No Time or Interest": (pd.to_numeric(raw_non_prov["q8.1"], errors="coerce") == 1).mean() * 100,
        "Unclear Legal Rules": (pd.to_numeric(raw_non_prov["q8.6"], errors="coerce") == 1).mean() * 100,
        "Complicated Tax System": (pd.to_numeric(raw_non_prov["q8.7"], errors="coerce") == 1).mean() * 100,
        "Lack of Trust in Online Payments": (pd.to_numeric(raw_non_prov["q8.4"], errors="coerce") == 1).mean() * 100,
        "Lack of Trust in Consumers": (pd.to_numeric(raw_non_prov["q8.5"], errors="coerce") == 1).mean() * 100,
        "Unclear Employment Impact": (pd.to_numeric(raw_non_prov["q8.8"], errors="coerce") == 1).mean() * 100
    }
    s_pb = pd.Series(p_barriers).sort_values(ascending=True)
    ax2.barh(s_pb.index, s_pb.values, color="#D97706", height=0.55)
    ax2.set_title("Non-Provider Barriers (N=25,113)", fontsize=11, fontweight="bold")
    ax2.set_xlabel("% Endorsement", fontweight="bold")
    ax2.set_xlim(0, 60)
    for b in ax2.patches:
        ax2.text(b.get_width() + 0.8, b.get_y() + b.get_height()/2, f"{b.get_width():.1f}%", va="center", fontsize=9)
        
    plt.suptitle("Figure 12: Adoption Friction: Consumer Barriers vs. Provider Compliance Barriers", fontsize=13, fontweight="bold", y=1.02)
    sns.despine(left=True, bottom=True)
    save_fig(fig, "fig12_consumer_and_provider_barriers.png")

def generate_figure13_cluster_profiles(seg_df):
    """Figure 13: Radar/Bar profile comparison across behavioral segments."""
    fig, ax = plt.subplots(figsize=(10, 5.5))
    
    seg_means = seg_df.groupby("segment_name").agg({
        "PEI": "mean",
        "consumer_sector_breadth": lambda x: x.mean() * 10, # scaled for visual comparability
        "adv_economic_score": lambda x: x.mean() * 100,
        "adv_functional_score": lambda x: x.mean() * 100,
        "prov_mot_sustainability": lambda x: x.mean() * 100,
        "recommend_high": lambda x: x.mean() * 100
    })
    
    seg_means.T.plot(kind="bar", ax=ax, width=0.75, colormap="viridis")
    ax.set_title("Figure 13: Behavioral and Motivational Centroids Across Prosumer Segments", fontsize=13, fontweight="bold", pad=12)
    ax.set_ylabel("Normalized Mean / Percentage (%)", fontweight="bold")
    ax.set_xticklabels(["Mean PEI", "Sector Breadth (x10)", "Economic Value (%)", "Convenience Value (%)", "Sustainability Motive (%)", "Advocacy (%)"], 
                       rotation=15, ha="right", fontweight="bold")
    ax.legend(title="Consumer Segment", frameon=True, facecolor="white")
    ax.set_ylim(0, 105)
    sns.despine(top=True, right=True)
    save_fig(fig, "fig13_cluster_centroids_profile.png")

def run_visualization_pipeline():
    """Runs generation for all 12 publication figures."""
    print("Generating all publication figures (Figures 1-13)...")
    df = pd.read_csv(PROC_INDEX_CSV)
    seg_df = pd.read_csv(PROC_SEGMENTS_CSV)
    
    generate_figure1_awareness_participation(df)
    generate_figure2_consumer_frequency(df)
    generate_figure3_provider_frequency(df)
    generate_figure4_consumer_vs_prosumer(df)
    generate_figure5_and_6_sectors(df)
    generate_figure7_age_demographics(df)
    generate_figure8_gender_education(df)
    generate_figure9_occupation(df)
    generate_figure10_consumer_advantages(df)
    generate_figure11_provider_motivations(df)
    generate_figure12_participation_barriers(df)
    generate_figure13_cluster_profiles(seg_df)
    print("All figures successfully created in figures/ directory!")

if __name__ == "__main__":
    run_visualization_pipeline()
