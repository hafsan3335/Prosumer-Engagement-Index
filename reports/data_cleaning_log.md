# Data Cleaning & Harmonization Log: Flash Eurobarometer 467

## 1. Overview
- **Raw Microdata File**: `data/raw/fl467_csv.csv`
- **Total Initial Records**: 26,544 respondents across 28 EU Member States
- **Cleaned Attributes**: 85 standardized variables
- **Analytical Samples**:
  - **Full Sample ($N = 26,544$)**: General population analysis, adoption barriers, national benchmarking.
  - **Active Platform Users ($N = 5,872$)**: Platform consumers, micro-providers, and dual prosumers.

## 2. Participation & Role Distribution
| Category | Frequency ($N$) | Unweighted % | Description |
| :--- | :--- | :--- | :--- |
| **Non-Users** | 20,672 | 77.9% | Never used nor provided collaborative services |
| **Consumer Only** | 4,441 | 16.7% | Uses services but has never offered services |
| **Provider Only** | 282 | 1.1% | Offers services without personal consumption |
| **Prosumers (Dual Actors)** | 1,149 | 4.3% | Both consumes and offers collaborative services |
| **Total Active Users** | 5,872 | 22.1% | Total collaborative economy participant pool |

## 3. Structural Skip Pattern Treatments
1. **Consumer Sector Questions (`q2.1` to `q2.8`)**: Asked only if `d8 in [2, 3, 4]`. Structural skips for non-consumers were assigned `0` (not active) rather than treated as random missing values.
2. **Provider Sector Questions (`q10.1` to `q10.9`)**: Asked only if `d9 in [2, 3, 4]`. Structural skips for non-providers were assigned `0`.
3. **Market Substitution (`q3`)**: Asked to platform consumers. Non-consumers assigned score `0` (no substitution).
4. **Provider Motivations (`q11.1` to `q11.11`)**: Filtered strictly to active providers. Missing values outside the provider sub-population are structural.
