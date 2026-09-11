# Prosumer Engagement Index (PEI): Methodological Report & Specification

## 1. Conceptual Grounding & Formative Specification
In accordance with Diamantopoulos & Winklhofer (2001) and consumer co-creation theory (Xie, Bagozzi & Troye, 2008), the **Prosumer Engagement Index (PEI)** is constructed as a **formative behavioural index**. Unlike reflective psychometric scales (which assume items reflect an unobservable latent trait and require high internal item correlation/Cronbach's alpha), a formative index represents an aggregation of distinct, observable market activities that jointly define the intensity of prosumer participation.

### Primary Formulation (Design A: Equal-Weighted Formative Index)
$$\text{PEI} = 100 \times \left[ 0.25 \cdot \left(\frac{\text{Consumer Freq}}{3}\right) + 0.25 \cdot \left(\frac{\text{Provider Freq}}{3}\right) + 0.25 \cdot \left(\frac{\text{Total Sectors}}{12}\right) + 0.25 \cdot \left(\frac{\text{Market Substitution}}{2}\right) \right]$$

- **Scale Range**: $0.0$ to $100.0$
- **Component Weights**:
  - $w_1 = 0.25$: Consumer Usage Frequency (`d8_score` / 3)
  - $w_2 = 0.25$: Provider Offering Frequency (`d9_score` / 3)
  - $w_3 = 0.25$: Total Sector Activity Breadth (`total_sectors` / 12)
  - $w_4 = 0.25$: Market Substitution / Integration (`substitution_score` / 2)

## 2. Distributional Characteristics
| Sample                          |   Mean PEI |   Std Dev |   Median |     IQR |   Skewness |
|:--------------------------------|-----------:|----------:|---------:|--------:|-----------:|
| Full Population (N=26,544)      |    5.92154 |   13.1298 |   0      |  0      |   2.5058   |
| Active Platform Users (N=5,872) |   26.7679  |   14.8756 |  22.9167 | 20.8333 |   1.05531  |
| Dual Prosumers (N=1,149)        |   43.09    |   15.8075 |  39.5833 | 22.9167 |   0.560256 |

### Key Empirical Distribution Findings:
- **Active Platform Users ($N = 5,872$)**: Mean PEI = 26.77, Median = 22.92, Std Dev = 14.88.
- **Dual Prosumers ($N = 1,149$)**: Mean PEI = 43.09, Median = 39.58. Prosumers score significantly higher across all four components than consumer-only respondents (Mean = 23.26).

## 3. Engagement Tier Classification
| Engagement Tier | PEI Range | Full Sample Count ($N$) | Full Sample % | Active User Count ($N$) | Active User % |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **0. Non-User** | $\text{PEI} = 0$ | 20,672 | 77.9% | 0 | 0.0% |
| **1. Occasional Consumer** | $0 < \text{PEI} \le 20$ | 2,248 | 8.5% | 2,248 | 38.3% |
| **2. Active Multi-Sector Consumer** | $20 < \text{PEI} \le 40$ | 2,618 | 9.9% | 2,618 | 44.6% |
| **3. Emerging Prosumer** | $40 < \text{PEI} \le 60$ | 814 | 3.1% | 814 | 13.9% |
| **4. High-Engagement Prosumer** | $\text{PEI} > 60$ | 192 | 0.7% | 192 | 3.3% |

## 4. Sensitivity & Robustness Analysis
Pearson correlation between alternative index formulations among active platform users ($N = 5,872$):
|                       |   PEI |   PEI_provider_weighted |   PEI_no_substitution |   PEI_unique_breadth |   CII |   PII |
|:----------------------|------:|------------------------:|----------------------:|---------------------:|------:|------:|
| PEI                   | 1     |                   0.927 |                 0.82  |                0.991 | 0.797 | 0.529 |
| PEI_provider_weighted | 0.927 |                   1     |                 0.919 |                0.907 | 0.588 | 0.798 |
| PEI_no_substitution   | 0.82  |                   0.919 |                 1     |                0.812 | 0.651 | 0.719 |
| PEI_unique_breadth    | 0.991 |                   0.907 |                 0.812 |                1     | 0.825 | 0.488 |
| CII                   | 0.797 |                   0.588 |                 0.651 |                0.825 | 1     | 0.006 |
| PII                   | 0.529 |                   0.798 |                 0.719 |                0.488 | 0.006 | 1     |

- The primary PEI correlates extremely highly with the Provider-Weighted PEI ($r = 0.927$) and the Non-Substitution PEI ($r = 0.820$), demonstrating that relative respondent rankings and empirical findings are robust to component weighting variations.

## 5. Criterion-Related Validity Evidence
| Criterion Outcome                               |   Correlation (r) with PEI |     p-value | Statistical Interpretation                                                                                 |
|:------------------------------------------------|---------------------------:|------------:|:-----------------------------------------------------------------------------------------------------------|
| Strong Recommendation Intention (q6=Definitely) |                   0.216746 | 2.21959e-63 | Positive and highly significant (p < 0.001) - Higher engagement predicts platform advocacy.                |
| Future Service Offering Intention (q7=Yes)      |                   0.11631  | 1.32347e-80 | Positive and highly significant (p < 0.001) - Higher engagement predicts future supply-side participation. |

- The empirical results provide strong criterion-related evidence: higher PEI scores are significantly associated with both strong platform advocacy ($r = 0.217, p < 0.001$) and prospective service-offering intentions ($r = 0.116, p < 0.001$).
