# Customer Churn Prediction and Analytics Solution
**AWS-Based Data Science Group Project — Team 05**

---

## 📌 Project Overview
Customer churn is a critical operational and financial challenge in the telecommunications industry. This project designs and implements a cloud-oriented data science pipeline using the real-world **Cell2Cell Telecom Dataset** (from the Teradata Center for Customer Relationship Management at Duke University).

The objective is to analyze historical customer usage, billing, equipment history, and service interactions to identify churn risk factors, evaluate data quality, and engineer robust features for downstream machine learning modeling and cloud analytics.

---

## 📂 Repository Structure

```text
AWS_Project_Team_05/
│
├── 5_6181716506095657051.md                 # Dataset Card & Research Notes
├── AWS Assignment.pdf                       # Project Scenario & Requirements
├── Cell2Cell Dataset - Detailed Variable Card.md  # Detailed 78-Variable Reference
├── README.md                                # Project Documentation & Evaluation Summary
│
└── src/
    ├── data/
    │   └── Sample Dataset.csv               # Raw Cell2Cell Telecom Dataset (71,047 records)
    │
    ├── data_validation.ipynb                # Module 1: Automated Data Quality & Schema Validation
    ├── eda.ipynb                            # Module 2: Exploratory Data Analysis & Churn Visualizations
    ├── preprocessing.ipynb                  # Module 3: Data Cleaning, Feature Engineering & Train/Test Split
    │
    └── outputs/
        └── plots/                           # Generated Publication-Quality Visualizations
            ├── viz1_churn_distribution.png
            ├── viz2_equipment_tenure_impact.png
            ├── viz3_financial_distributions.png
            ├── viz4_qos_service_friction.png
            └── viz6_correlation_heatmap.png
```

---

## 📊 Modules & Evaluation Summary

### 1. Data Validation & Quality Inspection (`src/data_validation.ipynb`)
The validation module systematically verifies schema integrity, missingness, and data domain anomalies across the 71,047 customer records:
* **Schema Integrity**: Validates all **78 required attributes** against the data dictionary. Status: `PASSED`.
* **Duplicate Check**: Verified 0 duplicate `CUSTOMER` identifiers.
* **Target Distribution**:
  * Non-Churn (`0`): 50,438 customers (**70.99%**)
  * Churn (`1`): 20,609 customers (**29.01%**)
  * Demonstrates a moderate class imbalance typical of real-world telecom retention scenarios.
* **Data Quality & Anomaly Detection**:
  * Identified **107 records** with negative values in `EQPDAYS` (Current Equipment Age in Days), requiring domain correction during preprocessing.
  * Verified valid positive months in service (`MONTHS > 0`).
  * Missing value profile: 13 continuous features (`REVENUE`, `MOU`, `RECCHRGE`, `DIRECTAS`, `OVERAGE`, `ROAM`, `CHANGEM`, `CHANGER`, `AGE1`, `AGE2`, etc.) contain exactly 216 missing entries (0.3% of the dataset), and `CSA` contains missing service areas.

---

### 2. Exploratory Data Analysis (EDA) & Churn Analytics (`src/eda.ipynb`)
Comprehensive statistical analysis and visual profiling of churn drivers:
* **Class Distribution (`viz1_churn_distribution.png`)**: Quantifies the 71% retained vs 29% churn ratio.
* **Hardware Age & Tenure (`viz2_equipment_tenure_impact.png`)**:
  * Churned customers have significantly higher equipment age (`EQPDAYS`), indicating that customers with aging, outdated handsets are at a substantially higher risk of leaving.
  * Newer subscribers (shorter `MONTHS` tenure) show higher churn volatility during initial contract periods.
* **Financial Distributions (`viz3_financial_distributions.png`)**:
  * Kernel density estimation (KDE) reveals that churned customers frequently incur unexpected monthly overage charges (`OVERAGE`), indicating plan misalignment and bill shock.
* **Network Quality / QoS Friction (`viz4_qos_service_friction.png`)**:
  * Customers experiencing higher mean dropped voice calls (`DROPVCE`) and blocked calls (`BLCKVCE`) exhibit markedly elevated churn rates, confirming that network service quality is a primary driver of customer defection.
* **Feature Correlation Analysis (`viz6_correlation_heatmap.png`)**:
  * Examines multi-collinearity across voice call types, overage charges, recurring billing, and tenure.

---

### 3. Preprocessing & Feature Engineering (`src/preprocessing.ipynb`)
Prepares clean, leakage-free feature matrices for classification models:
* **Calibration Sample Selection**: Filters the balanced calibration subset (`CALIBRAT == 1`, 40,000 records; 20,000 churn / 20,000 non-churn) for controlled model training and validation.
* **Anomaly Rectification**: Converts negative values in `EQPDAYS` to `NaN` and imputes them using the feature median.
* **Missing Value Imputation**: Continuous variables imputed with column medians; categorical `CSA` imputed with `'UNKNOWN'`.
* **Domain Feature Engineering**:
  * `TOTAL_FAILED_CALLS = DROPVCE + BLCKVCE`: Combined network quality friction index.
  * `REV_PER_MOU = REVENUE / (MOU + 1.0)`: Unit revenue per minute of usage.
  * High-cardinality categorical encoding: Frequency encoding applied to Communications Service Area (`CSA_FREQ`).
* **Stratified Train/Test Split & Scaling**:
  * Stratified split (80% train / 20% test): Train shape `(32,000, 76)`, Test shape `(8,000, 76)`.
  * Standardized numerical features using `StandardScaler` fitted strictly on training data to prevent data leakage.

---

## 🚀 Execution Instructions

### Prerequisites
* Python 3.10+
* Required libraries: `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `jupyter`

Install dependencies:
```bash
pip install pandas numpy matplotlib seaborn scikit-learn jupyter
```

### Running the Notebooks
Execute each notebook from within the `src/` directory:

```bash
cd src

# 1. Run Data Validation
jupyter nbconvert --to notebook --execute --inplace data_validation.ipynb

# 2. Run Exploratory Data Analysis & Visualizations
jupyter nbconvert --to notebook --execute --inplace eda.ipynb

# 3. Run Preprocessing & Feature Engineering
jupyter nbconvert --to notebook --execute --inplace preprocessing.ipynb
```

---

## 👥 Team 05 Group Work Division
This repository represents our group assignment deliverables for the data ingestion, validation, exploratory analysis, and preprocessing stages of the AWS Data Science pipeline. Downstream modeling, AWS cloud architecture, and Athena SQL queries are integrated collaboratively as part of our group workflow.
