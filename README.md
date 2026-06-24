# **Important** - Large CSV files are not in this repo


# London Airbnb Market Analysis

An end-to-end data engineering and analytics pipeline built on London Airbnb data from [Inside Airbnb](http://insideairbnb.com/). Covers data ingestion, profiling, cleaning, enrichment, dimensional modelling, exploratory data analysis, statistical testing, and machine learning price prediction.

---

## Project Overview

| Item | Detail |
|---|---|
| **City** | London |
| **Data Source** | Inside Airbnb |
| **Listings** | 96,871 |
| **Reviews** | 2,097,996 |
| **Target Variable** | Nightly listing price (log-transformed) |
| **Best Model** | Random Forest — R² = 0.707 |

---

## Repository Structure

```
project/
├── data/
│   └── London/
│       ├── raw/    
│       ├── extracted/
│       ├── cleaned/
│       ├── enriched/  
│       ├── profiling/                
│       └── warehouse/
│               └── airbnb_london.db              # SQLite dimensional model        
├── notebooks/
│   ├── 01_dataset_farmiliarization.ipynb
│   ├── 02_data_profiling.ipynb
│   ├── 03_data_cleaning_standardization.ipynb
│   ├── 04_data_enrichment_joining.ipynb
│   ├── 05_data_modeling.ipynb
│   ├── 06_EDA.ipynb
│   ├── 07_statistical_analysis.ipynb
│   └── 08_data_science.ipynb
├── scripts/
│   └── ingestion.py  # Automated download & extraction
└── README.md
```

---

## Pipeline Stages

1. **Data Ingestion** — Downloads and extracts Airbnb datasets from Inside Airbnb for a configured city
2. **Data Profiling** — Missing value analysis, duplicate detection, cardinality checks, domain validation
3. **Data Cleaning & Standardisation** — Price parsing, date standardisation, coordinate validation, category normalisation
4. **Feature Engineering** — Derived features: occupancy rate, estimated revenue, host tenure, listing age, neighbourhood medians
5. **Dimensional Modelling** — Star schema in SQLite (`Fact_Listing_Performance` + `Dim_Host`, `Dim_Neighbourhood`, `Dim_Property`)
6. **EDA** — Price distributions, geographic analysis, host segmentation, temporal trends, review analysis
7. **Statistical Analysis** — Hypothesis testing (t-tests, ANOVA), confidence intervals, OLS regression, correlation analysis
8. **Machine Learning** — Price prediction using Linear Regression, Random Forest, and Gradient Boosting with SHAP explainability

---

## Datasets

| File | Description | Rows | Columns |
|---|---|---|---|
| `listings.csv.gz` | Full listing details | 96,871 | 79 |
| `calendar.csv.gz` | Daily availability & pricing | 35,357,974 | 7 |
| `reviews.csv.gz` | Full guest reviews | 2,097,996 | 6 |
| `listings.csv` | Summary listing info | 96,871 | 18 |
| `reviews.csv` | Review summary | 2,097,996 | 2 |
| `neighbourhoods.csv` | Neighbourhood list | 33 | 2 |
| `neighbourhoods.geojson` | Geographic boundaries | — | — |

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Data ingestion, processing, analytics |
| Pandas | Data manipulation & transformation |
| SQLite | Dimensional model |
| Scikit-learn | Statistical modelling & machine learning |
| Matplotlib / Seaborn | Data visualisation |
| SHAP | Model explainability |

---

## Model Performance

| Model | MAE | RMSE | R² |
|---|---|---|---|
| **Random Forest** | **0.280** | **0.404** | **0.707** |
| Gradient Boosting | 0.282 | 0.407 | 0.703 |
| Linear Regression | 0.304 | 0.435 | 0.660 |

> Prices were log-transformed before modelling to reduce skew from high-end outliers.

**Top price drivers (SHAP):** Room type → Neighbourhood median price → Bathrooms → Accommodates → Bedrooms

---

## Key Findings

- Most listings price between **£75–£150/night**; the mean (£230) is skewed by a small premium tier
- **Room type and neighbourhood** are the dominant price drivers — not property size or ratings
- **Superhosts** earn ~£4,750 more per year (median) by commanding higher prices, not higher occupancy
- **Value for money** is the lowest-rated guest satisfaction dimension (avg 4.62/5)
- Listings below a **4.5 rating** face significant search visibility penalties
- The market has **fully recovered post-COVID**: 450K+ reviews in 2024 vs 49K in 2020

---

## Getting Started

### Prerequisites

```bash
pip install pandas scikit-learn matplotlib seaborn shap
```

### Run the ingestion pipeline

```bash
python scripts/ingestion_pipeline.py --city London
```

### Run notebooks in order

Open and run notebooks `01` through `07` sequentially in the `notebooks/` directory.

---

## Limitations

- Single-city snapshot (London only); no longitudinal data
- Occupancy and revenue are **estimated**, not observed
- Calendar data does not distinguish between booked and host-blocked nights
- Coordinates are anonymised within ~150m by Airbnb
- ML models use structured features only — no text (descriptions, reviews)

---

## Future Work

- Expand to multiple cities for cross-market comparison
- Integrate external data: transport access, tourism stats, local economic indicators
- Migrate from notebooks to an automated pipeline (Airflow / Prefect)
- Add demand forecasting and occupancy prediction models
- Deploy pricing recommendation tool via API or web app

---

