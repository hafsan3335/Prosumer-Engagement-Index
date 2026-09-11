"""
Configuration module for Prosumer Engagement Index (PEI) research project.
Defines file paths, column mappings, categorical labels, country codes, and visual styling palettes.
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
DATA_PROC_DIR = os.path.join(BASE_DIR, "data", "processed")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
FIGURES_DIR = os.path.join(BASE_DIR, "figures")
TABLES_DIR = os.path.join(BASE_DIR, "tables")
NOTEBOOKS_DIR = os.path.join(BASE_DIR, "notebooks")
DASHBOARD_DIR = os.path.join(BASE_DIR, "dashboard")

RAW_CSV_PATH = os.path.join(DATA_RAW_DIR, "fl467_csv.csv")
Q_DESC_PATH = os.path.join(DATA_RAW_DIR, "DESCRIPT_1467_QUESTION.csv")
R_DESC_PATH = os.path.join(DATA_RAW_DIR, "DESCRIPT_1467_RESPONSE.csv")

PROC_USERS_CSV = os.path.join(DATA_PROC_DIR, "fl467_cleaned_users.csv")
PROC_FULL_CSV = os.path.join(DATA_PROC_DIR, "fl467_full_cleaned.csv")
PROC_INDEX_CSV = os.path.join(DATA_PROC_DIR, "fl467_prosumer_index.csv")
PROC_SEGMENTS_CSV = os.path.join(DATA_PROC_DIR, "prosumer_segments.csv")

# EU-28 Country Code Mapping
COUNTRY_MAP = {
    1: "Belgium", 2: "Denmark", 3: "Germany", 4: "Greece", 5: "Spain",
    6: "Finland", 7: "France", 8: "Ireland", 9: "Italy", 10: "Luxembourg",
    11: "Netherlands", 12: "Austria", 13: "Portugal", 14: "Sweden", 15: "United Kingdom",
    31: "Bulgaria", 32: "Cyprus", 33: "Czech Republic", 34: "Estonia", 35: "Hungary",
    36: "Latvia", 37: "Lithuania", 38: "Malta", 39: "Poland", 40: "Romania",
    41: "Slovakia", 42: "Slovenia", 46: "Croatia"
}

# ISO-3 Code mapping for Choropleth Maps
COUNTRY_ISO3 = {
    "Belgium": "BEL", "Denmark": "DNK", "Germany": "DEU", "Greece": "GRC", "Spain": "ESP",
    "Finland": "FIN", "France": "FRA", "Ireland": "IRL", "Italy": "ITA", "Luxembourg": "LUX",
    "Netherlands": "NLD", "Austria": "AUT", "Portugal": "PRT", "Sweden": "SWE", "United Kingdom": "GBR",
    "Bulgaria": "BGR", "Cyprus": "CYP", "Czech Republic": "CZE", "Estonia": "EST", "Hungary": "HUN",
    "Latvia": "LVA", "Lithuania": "LTU", "Malta": "MLT", "Poland": "POL", "Romania": "ROU",
    "Slovakia": "SVK", "Slovenia": "SVN", "Croatia": "HRV"
}

# Collaborative Economy Sectors
SECTOR_COLS_CONSUMER = {
    "q2.1": "Transport",
    "q2.2": "Accommodation",
    "q2.3": "Food Services",
    "q2.4": "Household Services",
    "q2.5": "Professional Services",
    "q2.6": "Collaborative Finance"
}

SECTOR_COLS_PROVIDER = {
    "q10.1": "Transport",
    "q10.2": "Accommodation",
    "q10.3": "Food Services",
    "q10.4": "Household Services",
    "q10.5": "Professional Services",
    "q10.6": "Collaborative Finance"
}

# Advantages / Perceived Value Dimensions
ADVANTAGE_COLS = {
    "q4.1": "Cheaper or Free (Economic)",
    "q4.2": "Wider Choice (Functional)",
    "q4.3": "Convenient Access (Functional)",
    "q4.4": "Ratings & Reviews (Informational)",
    "q4.5": "Social Interaction (Social)",
    "q4.6": "Exchange Services (Social/Collaborative)"
}

# Disadvantages / Barriers
DISADVANTAGE_COLS = {
    "q5.1": "Booking / Payment Problems",
    "q5.2": "Low Trust in Providers",
    "q5.3": "Poor Service Quality",
    "q5.4": "Misleading Reviews",
    "q5.5": "Unclear Responsibility / Liability",
    "q5.6": "Personal Data Misuse"
}

# Provider Motivations
PROVIDER_MOTIVATION_COLS = {
    "q11.1": "Main Income Source (Economic)",
    "q11.2": "Additional Income (Economic)",
    "q11.3": "Flexible Working Hours (Autonomy)",
    "q11.4": "Easy Opportunity to Provide (Market Access)",
    "q11.5": "Offer Innovative Services (Innovation)",
    "q11.6": "Access to More Consumers (Reach)",
    "q11.7": "Easy Interaction with Consumers (Social)",
    "q11.8": "Sustainable & Efficient Asset Use (Sustainability)"
}

# Color Palettes
PALETTE = {
    "primary": "#1E3A8A",      # Oxford Blue
    "secondary": "#0D9488",    # Teal
    "accent": "#F59E0B",       # Amber
    "dark": "#0F172A",         # Slate Dark
    "light": "#F8FAFC",        # Slate Light
    "prosumer": "#8B5CF6",     # Purple
    "consumer": "#3B82F6",     # Blue
    "provider": "#10B981",     # Emerald
    "non_user": "#94A3B8"      # Gray
}
