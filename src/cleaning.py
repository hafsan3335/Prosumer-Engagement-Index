"""
Data cleaning and preprocessing module for Flash Eurobarometer 467.
Handles structural skip patterns, recoding, variable standardization, and analytical sample extraction.
"""
import os
import pandas as pd
import numpy as np
from src.config import (
    RAW_CSV_PATH, PROC_FULL_CSV, PROC_USERS_CSV, REPORTS_DIR,
    COUNTRY_MAP, COUNTRY_ISO3, SECTOR_COLS_CONSUMER, SECTOR_COLS_PROVIDER,
    ADVANTAGE_COLS, DISADVANTAGE_COLS, PROVIDER_MOTIVATION_COLS
)

def load_raw_dataset(path=RAW_CSV_PATH):
    """Loads the raw Eurobarometer 467 CSV dataset using tilde delimiter."""
    print(f"Loading raw dataset from {path}...")
    df = pd.read_csv(path, sep="~", encoding="utf-8-sig", low_memory=False)
    print(f"Loaded {df.shape[0]:,} rows and {df.shape[1]} columns.")
    return df

def clean_demographics(df):
    """Cleans and standardizes demographic control variables."""
    d_df = pd.DataFrame(index=df.index)
    
    # Country Name & ISO3
    d_df["country_id"] = pd.to_numeric(df["b"], errors="coerce")
    d_df["country"] = d_df["country_id"].map(COUNTRY_MAP)
    d_df["country_iso3"] = d_df["country"].map(COUNTRY_ISO3)
    
    # Exact Age
    d_df["age"] = pd.to_numeric(df["vd1"], errors="coerce")
    median_age = d_df["age"].median()
    d_df["age_imputed"] = d_df["age"].fillna(median_age)
    
    # Age Cohort (d1r2: 1='15-24', 2='25-34', 3='35-44', 4='45-54', 5='55-64', 6='65+')
    age_cohort_map = {
        1: "15-24", 2: "25-34", 3: "35-44", 4: "45-54", 5: "55-64", 6: "65+"
    }
    d_df["age_cohort"] = pd.to_numeric(df["d1r2"], errors="coerce").map(age_cohort_map).fillna("Unknown")
    
    # Gender (d2: 1=Male, 2=Female)
    d_df["gender_raw"] = pd.to_numeric(df["d2"], errors="coerce")
    d_df["gender"] = d_df["gender_raw"].map({1: "Male", 2: "Female"}).fillna("Unknown")
    d_df["gender_male"] = (d_df["gender_raw"] == 1).astype(int)
    
    # Education Level (d4: 1='<=15', 2='16-19', 3='20+', 4='Still Studying', 5='No full-time', 6='Refusal', 7='DK')
    edu_map = {
        1: "Up to 15 yrs", 2: "16-19 yrs", 3: "20+ yrs (Higher Edu)",
        4: "Still Studying", 5: "No Full-time Edu"
    }
    d_df["education_level"] = pd.to_numeric(df["d4"], errors="coerce").map(edu_map).fillna("Other/Unknown")
    d_df["higher_education"] = (pd.to_numeric(df["d4"], errors="coerce") == 3).astype(int)
    
    # Occupation Category (brk2: 1='Self-employed', 2='Employees', 3='Manual workers', 4='Not working')
    occ_map = {
        1: "Self-employed", 2: "Employee", 3: "Manual Worker", 4: "Not Working / Retired / Student"
    }
    d_df["occupation_group"] = pd.to_numeric(df["brk2"], errors="coerce").map(occ_map).fillna("Other/Unknown")
    
    # Urbanization (d13: 1='Rural area or village', 2='Small or middle sized town', 3='Large town')
    urban_map = {
        1: "Rural", 2: "Small/Mid Town", 3: "Large Town"
    }
    d_df["urbanization"] = pd.to_numeric(df["d13"], errors="coerce").map(urban_map).fillna("Unknown")
    d_df["urbanization_score"] = pd.to_numeric(df["d13"], errors="coerce").apply(lambda x: x if x in [1, 2, 3] else np.nan)
    
    # Survey Weights
    d_df["weight_national"] = pd.to_numeric(df["w1"], errors="coerce").fillna(1.0)
    d_df["weight_eu28"] = pd.to_numeric(df["w23"], errors="coerce").fillna(1.0)
    
    return d_df

def clean_participation_and_roles(df):
    """Cleans consumer and provider participation frequencies and user profile roles."""
    p_df = pd.DataFrame(index=df.index)
    
    # Consumer Usage Frequency (d8: 1=Never, 2=Once/few, 3=Occasionally, 4=Regularly, 5=DK/NA)
    d8_num = pd.to_numeric(df["d8"], errors="coerce")
    p_df["consumer_freq_raw"] = d8_num
    p_df["consumer_freq_label"] = d8_num.map({
        1: "Never", 2: "Once or few times", 3: "Occasionally", 4: "Regularly"
    }).fillna("DK/NA")
    p_df["consumer_freq_score"] = d8_num.map({1: 0, 2: 1, 3: 2, 4: 3}).fillna(0).astype(int)
    p_df["is_consumer"] = d8_num.isin([2, 3, 4]).astype(int)
    
    # Provider Offering Frequency (d9: 1=Never, 2=Once/few, 3=Occasionally, 4=Regularly, 5=DK/NA)
    d9_num = pd.to_numeric(df["d9"], errors="coerce")
    p_df["provider_freq_raw"] = d9_num
    p_df["provider_freq_label"] = d9_num.map({
        1: "Never", 2: "Once or few times", 3: "Occasionally", 4: "Regularly"
    }).fillna("DK/NA")
    p_df["provider_freq_score"] = d9_num.map({1: 0, 2: 1, 3: 2, 4: 3}).fillna(0).astype(int)
    p_df["is_provider"] = d9_num.isin([2, 3, 4]).astype(int)
    
    # User Profile (d8d9: 1=Only user, 2=Only provider, 3=User and provider, 4=Not user nor provider)
    d8d9_num = pd.to_numeric(df["d8d9"], errors="coerce")
    profile_map = {
        1: "Consumer Only",
        2: "Provider Only",
        3: "Prosumer",
        4: "Non-User"
    }
    p_df["user_profile"] = d8d9_num.map(profile_map).fillna("Non-User")
    p_df["is_prosumer"] = (p_df["user_profile"] == "Prosumer").astype(int)
    p_df["is_active_user"] = p_df["user_profile"].isin(["Consumer Only", "Provider Only", "Prosumer"]).astype(int)
    
    return p_df

def clean_sectors(df, is_consumer_series, is_provider_series):
    """Cleans consumer and provider participation sectors handling skip logic."""
    s_df = pd.DataFrame(index=df.index)
    
    # Consumer Sectors (q2.1 - q2.6)
    cons_cols = []
    for col, name in SECTOR_COLS_CONSUMER.items():
        clean_col = f"cons_sector_{name.lower().replace(' ', '_')}"
        cons_cols.append(clean_col)
        raw_val = pd.to_numeric(df[col], errors="coerce").fillna(0)
        # Apply structural skip logic: 0 if not a consumer
        s_df[clean_col] = np.where(is_consumer_series == 1, (raw_val == 1).astype(int), 0)
        
    s_df["consumer_sector_breadth"] = s_df[cons_cols].sum(axis=1)
    
    # Provider Sectors (q10.1 - q10.6)
    prov_cols = []
    for col, name in SECTOR_COLS_PROVIDER.items():
        clean_col = f"prov_sector_{name.lower().replace(' ', '_')}"
        prov_cols.append(clean_col)
        raw_val = pd.to_numeric(df[col], errors="coerce").fillna(0)
        # Apply structural skip logic: 0 if not a provider
        s_df[clean_col] = np.where(is_provider_series == 1, (raw_val == 1).astype(int), 0)
        
    s_df["provider_sector_breadth"] = s_df[prov_cols].sum(axis=1)
    
    # Combined Metrics
    s_df["total_sector_activity"] = s_df["consumer_sector_breadth"] + s_df["provider_sector_breadth"]
    
    # Unique sector overlap (e.g. transport as consumer OR provider)
    unique_sectors = []
    for (_, name_c), (_, name_p) in zip(SECTOR_COLS_CONSUMER.items(), SECTOR_COLS_PROVIDER.items()):
        c_col = f"cons_sector_{name_c.lower().replace(' ', '_')}"
        p_col = f"prov_sector_{name_p.lower().replace(' ', '_')}"
        u_col = f"active_in_{name_c.lower().replace(' ', '_')}"
        s_df[u_col] = ((s_df[c_col] == 1) | (s_df[p_col] == 1)).astype(int)
        unique_sectors.append(u_col)
        
    s_df["unique_sector_breadth"] = s_df[unique_sectors].sum(axis=1)
    
    return s_df

def clean_market_substitution(df, is_consumer_series):
    """Cleans traditional service substitution question (q3)."""
    sub_df = pd.DataFrame(index=df.index)
    q3_num = pd.to_numeric(df["q3"], errors="coerce")
    
    # 1=Partially replaced, 2=Completely replaced, 3=Used on top, 4=Only started because of platform, 5=None, 6=DK/NA
    sub_map = {
        1: "Partial Replacement",
        2: "Complete Replacement",
        3: "Coexists with Traditional",
        4: "New Demand Created",
        5: "No Substitution",
        6: "DK/NA"
    }
    sub_df["substitution_label"] = q3_num.map(sub_map).fillna("Not Applicable / Non-Consumer")
    
    # Substitution intensity score:
    # 2 = Complete replacement (deepest market integration)
    # 1 = Partial replacement
    # 0 = Coexistence / No substitution / Non-consumer
    sub_score = q3_num.map({2: 2, 1: 1, 3: 0, 4: 0, 5: 0, 6: 0}).fillna(0).astype(int)
    sub_df["substitution_score"] = np.where(is_consumer_series == 1, sub_score, 0)
    sub_df["is_substitutor"] = (sub_df["substitution_score"] > 0).astype(int)
    
    return sub_df

def clean_perceptions_and_motives(df, is_consumer_series, is_provider_series):
    """Cleans consumer perceived advantages, barriers, provider motives, and outcomes."""
    m_df = pd.DataFrame(index=df.index)
    
    # Consumer Advantages (q4.1 - q4.6)
    adv_cols = []
    for col, label in ADVANTAGE_COLS.items():
        clean_name = f"adv_{label.split(' ')[0].lower()}"
        adv_cols.append(clean_name)
        val = pd.to_numeric(df[col], errors="coerce").fillna(0)
        m_df[clean_name] = np.where(is_consumer_series == 1, (val == 1).astype(int), 0)
    
    m_df["adv_economic_score"] = m_df["adv_cheaper"]
    m_df["adv_functional_score"] = ((m_df["adv_wider"] == 1) | (m_df["adv_convenient"] == 1)).astype(int)
    m_df["adv_information_score"] = m_df["adv_ratings"]
    m_df["adv_social_score"] = ((m_df["adv_social"] == 1) | (m_df["adv_exchange"] == 1)).astype(int)
    
    # Consumer Disadvantages (q5.1 - q5.6)
    for col, label in DISADVANTAGE_COLS.items():
        clean_name = f"disadv_{col.replace('.', '_')}"
        val = pd.to_numeric(df[col], errors="coerce").fillna(0)
        m_df[clean_name] = np.where(is_consumer_series == 1, (val == 1).astype(int), 0)
        
    # Provider Motivations (q11.1 - q11.8)
    for col, label in PROVIDER_MOTIVATION_COLS.items():
        clean_name = f"prov_mot_{col.replace('.', '_')}"
        val = pd.to_numeric(df[col], errors="coerce").fillna(0)
        m_df[clean_name] = np.where(is_provider_series == 1, (val == 1).astype(int), 0)
        
    # Key Motivational Indicators
    m_df["prov_mot_economic"] = ((m_df["prov_mot_q11_1"] == 1) | (m_df["prov_mot_q11_2"] == 1)).astype(int)
    m_df["prov_mot_flexibility"] = m_df["prov_mot_q11_3"]
    m_df["prov_mot_innovation"] = m_df["prov_mot_q11_5"]
    m_df["prov_mot_sustainability"] = m_df["prov_mot_q11_8"] # Core sustainability motivation variable!
    
    # Recommendation Intention (q6: 1=Definitely, 2=To some extent, 3=Not really, 4=Definitely not, 5=Some types, 6=DK/NA)
    q6_num = pd.to_numeric(df["q6"], errors="coerce")
    m_df["recommendation_raw"] = q6_num
    m_df["recommendation_label"] = q6_num.map({
        1: "Yes, definitely",
        2: "Yes, to some extent",
        3: "No, not really",
        4: "No, definitely not",
        5: "Some types only",
        6: "DK/NA"
    }).fillna("Not Asked")
    m_df["recommend_high"] = np.where(is_consumer_series == 1, (q6_num == 1).astype(int), 0)
    m_df["recommend_positive"] = np.where(is_consumer_series == 1, q6_num.isin([1, 2]).astype(int), 0)
    
    # Future Intention to Offer Services (q7: 1=Yes, 2=No, 3=DK/NA)
    q7_num = pd.to_numeric(df["q7"], errors="coerce")
    m_df["future_offer_intent"] = (q7_num == 1).astype(int)
    
    return m_df

def run_cleaning_pipeline():
    """Executes end-to-end data cleaning pipeline and exports processed datasets."""
    os.makedirs(os.path.dirname(PROC_FULL_CSV), exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)
    
    raw_df = load_raw_dataset()
    
    # Process sections
    demo_df = clean_demographics(raw_df)
    part_df = clean_participation_and_roles(raw_df)
    sect_df = clean_sectors(raw_df, part_df["is_consumer"], part_df["is_provider"])
    sub_df = clean_market_substitution(raw_df, part_df["is_consumer"])
    mot_df = clean_perceptions_and_motives(raw_df, part_df["is_consumer"], part_df["is_provider"])
    
    # Combine full cleaned dataframe
    full_df = pd.concat([demo_df, part_df, sect_df, sub_df, mot_df], axis=1)
    print(f"Full cleaned dataset created: {full_df.shape[0]:,} rows, {full_df.shape[1]} variables.")
    
    # Filter active collaborative platform users (Consumers, Providers, Prosumers)
    users_df = full_df[full_df["is_active_user"] == 1].copy()
    print(f"Active collaborative economy users: {users_df.shape[0]:,} respondents.")
    print("User breakdown:")
    print(users_df["user_profile"].value_counts())
    
    # Export CSVs
    full_df.to_csv(PROC_FULL_CSV, index=False)
    users_df.to_csv(PROC_USERS_CSV, index=False)
    print(f"Saved full cleaned dataset to {PROC_FULL_CSV}")
    print(f"Saved active users dataset to {PROC_USERS_CSV}")
    
    # Generate Data Cleaning Log
    log_content = f"""# Data Cleaning & Harmonization Log: Flash Eurobarometer 467

## 1. Overview
- **Raw Microdata File**: `{RAW_CSV_PATH}`
- **Total Initial Records**: {raw_df.shape[0]:,} respondents across 28 EU Member States
- **Cleaned Attributes**: {full_df.shape[1]} standardized variables
- **Analytical Samples**:
  - **Full Sample ($N = {full_df.shape[0]:,}$)**: General population analysis, adoption barriers, national benchmarking.
  - **Active Platform Users ($N = {users_df.shape[0]:,}$)**: Platform consumers, micro-providers, and dual prosumers.

## 2. Participation & Role Distribution
| Category | Frequency ($N$) | Unweighted % | Description |
| :--- | :--- | :--- | :--- |
| **Non-Users** | {(full_df['user_profile'] == 'Non-User').sum():,} | {((full_df['user_profile'] == 'Non-User').mean()*100):.1f}% | Never used nor provided collaborative services |
| **Consumer Only** | {(full_df['user_profile'] == 'Consumer Only').sum():,} | {((full_df['user_profile'] == 'Consumer Only').mean()*100):.1f}% | Uses services but has never offered services |
| **Provider Only** | {(full_df['user_profile'] == 'Provider Only').sum():,} | {((full_df['user_profile'] == 'Provider Only').mean()*100):.1f}% | Offers services without personal consumption |
| **Prosumers (Dual Actors)** | {(full_df['user_profile'] == 'Prosumer').sum():,} | {((full_df['user_profile'] == 'Prosumer').mean()*100):.1f}% | Both consumes and offers collaborative services |
| **Total Active Users** | {users_df.shape[0]:,} | {((users_df.shape[0] / full_df.shape[0])*100):.1f}% | Total collaborative economy participant pool |

## 3. Structural Skip Pattern Treatments
1. **Consumer Sector Questions (`q2.1` to `q2.8`)**: Asked only if `d8 in [2, 3, 4]`. Structural skips for non-consumers were assigned `0` (not active) rather than treated as random missing values.
2. **Provider Sector Questions (`q10.1` to `q10.9`)**: Asked only if `d9 in [2, 3, 4]`. Structural skips for non-providers were assigned `0`.
3. **Market Substitution (`q3`)**: Asked to platform consumers. Non-consumers assigned score `0` (no substitution).
4. **Provider Motivations (`q11.1` to `q11.11`)**: Filtered strictly to active providers. Missing values outside the provider sub-population are structural.
"""
    log_path = os.path.join(REPORTS_DIR, "data_cleaning_log.md")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(log_content)
    print(f"Saved cleaning log to {log_path}")

if __name__ == "__main__":
    run_cleaning_pipeline()
