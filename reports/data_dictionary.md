# Data Dictionary & Operationalization Matrix: Flash Eurobarometer 467

This document details the operational definitions, variable names, raw measurement scales, and standardized recodes utilized in this research.

| Variable Name | Raw Item | Label / Operational Definition | Raw Coding | Cleaned / Recoded Operationalization | Role in Study |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `country` | `b` | Country of Interview (EU-28) | 1 to 46 | Mapped to country name and ISO-3 code | Geographic Macro Control |
| `age` | `vd1` | Exact Age of Respondent | Numeric (15 to 99) | Numeric continuous, median imputed | Demographic Control |
| `age_cohort` | `d1r2` | Standard Eurobarometer Age Cohort | 1='15-24' to 6='65+' | 6 categorical cohorts | Demographic Segment |
| `gender` | `d2` | Gender | 1=Male, 2=Female | Male=1, Female=0 (`gender_male`) | Demographic Control |
| `education_level` | `d4` | Age Stopped Full-time Education | 1='<=15', 2='16-19', 3='20+', 4='Still studying' | 4 categorical education tiers | Socioeconomic Control |
| `occupation_group` | `brk2` | Broad Occupation Scale | 1='Self-employed' to 4='Not working' | 4 categorical employment groups | Socioeconomic Control |
| `urbanization` | `d13` | Subjective Locality Type | 1='Rural/village', 2='Small/mid town', 3='Large town' | Ordinal (1 to 3) | Geographic Control |
| `consumer_freq_score` | `d8` | Frequency of Using Collaborative Services | 1=Never, 2=Once/few, 3=Occasionally, 4=Regularly | 0=Never/DK, 1=Once/few, 2=Occasionally, 3=Regularly | **PEI Component 1** |
| `provider_freq_score` | `d9` | Frequency of Offering Collaborative Services | 1=Never, 2=Once/few, 3=Occasionally, 4=Regularly | 0=Never/DK, 1=Once/few, 2=Occasionally, 3=Regularly | **PEI Component 2** |
| `user_profile` | `d8d9` | Composite User-Provider Profile | 1=Only user, 2=Only provider, 3=Both, 4=Neither | 'Consumer Only', 'Provider Only', 'Prosumer', 'Non-User' | Analytical Role Group |
| `consumer_sector_breadth` | `q2.1`–`q2.6` | Count of Collaborative Sectors Used | Multi-select binary items | Integer sum (0 to 6) | **PEI Component 3A** |
| `provider_sector_breadth` | `q10.1`–`q10.6` | Count of Collaborative Sectors Offered | Multi-select binary items | Integer sum (0 to 6) | **PEI Component 3B** |
| `total_sector_activity` | `q2` + `q10` | Total Sector Activity Count | Sum of used and offered sectors | Integer sum (0 to 12) | **PEI Component 3** |
| `substitution_score` | `q3` | Replacement of Traditional Channels | 1=Partial, 2=Complete, 3=Coexists, 4=New demand | 2=Complete, 1=Partial, 0=Other/None | **PEI Component 4** |
| `PEI` | Formula | Prosumer Engagement Index | Scaled 0 to 100 | Weighted formative composite score | **Core Analytical Metric** |
| `adv_economic_score` | `q4.1` | Perceived Advantage: Cheaper or Free | 1=Yes, 0=No | Binary (0/1) | Motivation Indicator |
| `adv_functional_score` | `q4.2`, `q4.3` | Perceived Advantage: Wider Choice / Convenient | Multi-select | Binary flag (1 if either endorsed) | Motivation Indicator |
| `adv_social_score` | `q4.5`, `q4.6` | Perceived Advantage: Social Interaction / Barter | Multi-select | Binary flag (1 if either endorsed) | Motivation Indicator |
| `prov_mot_sustainability` | `q11.8` | Provider Motive: Sustainable Asset Use | 1=Yes, 0=No | Binary (0/1) | **Sustainability Lens** |
| `recommend_high` | `q6` | Recommendation Advocacy | 1='Yes, definitely' to 4='Definitely not' | 1=Definitely recommend, 0=Otherwise | Criterion / Outcome |
| `future_offer_intent` | `q7` | Prospective Provider Intention | 1=Yes, 2=No | 1=Yes, 0=No | Criterion / Outcome |
| `weight_national` | `w1` | Post-stratification National Weight | Continuous weight | Continuous sampling weight | Weighted Descriptive Estimates |
| `weight_eu28` | `w23` | EU-28 Population Target Weight | Continuous weight | Continuous population weight | EU Population Projections |
