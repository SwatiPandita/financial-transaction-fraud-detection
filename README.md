# Financial Transaction Fraud Analytics & Risk Investigation

**An end-to-end analytics case study** exploring fraud-labelled patterns across 1.72 million synthetic mobile-money transactions with Python, DuckDB SQL, statistical analysis, machine-learning evaluation and Power BI.

> **Honest scope:** This is a retrospective educational analysis on synthetic data. The model evaluated here is weak and is not suitable for production fraud decisions. The project makes that limitation explicit.

## At a glance

| Dataset measure | Result |
|---|---:|
| Transactions | 1,720,181 |
| Transfer transactions analysed | 569,328 |
| Fraud-labelled transfers | 175,518 |
| Fraud-label rate among transfers | 30.83% |
| Fraud-label rate overall | 10.20% |

All fraud-labelled rows in this supplied dataset are TRANSFER transactions. This is a property of this dataset, not a universal rule about financial fraud.

## Business questions
1. Which transaction types contain fraud-labelled records?
2. How do amount distributions and label rates vary over simulation time?
3. Are balance-mismatch indicators associated with fraud labels, and how strong are those associations?
4. What do sender and recipient historical activity patterns reveal?
5. How does a model perform when evaluated on later simulation steps?

## Selected findings
- Initial data-quality checks found no missing values or exact duplicate rows.
- Fraud labels occur only in TRANSFER records in this dataset.
- Balance-mismatch indicators have statistically significant chi-square associations, but small effect sizes: Cramér's V is approximately 0.0375 (sender) and 0.0413 (recipient). Large samples can produce tiny p-values for weak associations.
- Historical sender and recipient activity features are built from earlier simulation steps.
- The current Random Forest does **not** perform well enough for operational use.

## Model evaluation: transparent, not inflated

Chronological held-out test results at a 0.50 threshold:

| Metric | Result |
|---|---:|
| Accuracy | 64% |
| Precision (fraud class) | 33% |
| Recall (fraud class) | 22% |
| F1-score (fraud class) | 0.26 |
| ROC-AUC | 0.5471 |
| PR-AUC | 0.3295 |

The majority-class accuracy baseline is approximately **70.52%**. The model's accuracy is below this baseline, and its ROC-AUC is only slightly above random ranking. It misses many fraud-labelled transactions. This is a useful learning outcome, not a successful detector.

### Critical feature-timing limitation
Balance mismatch features are derived using post-transaction balance values. They are suitable for retrospective investigation but may not be available at authorisation time. The next modelling iteration must use only point-in-time, pre-authorisation features and be re-evaluated on later data. Do not deploy or claim this model as a real-time fraud system.

## Power BI dashboard

![Financial Transaction Fraud Analytics Dashboard](dashboard/financial_transaction_fraud_dashboard_final.png)

The dashboard includes transaction and fraud-label KPIs, label distribution, trends over simulation steps, average amount by label, transaction volume, mismatch comparisons, a transaction sample table and a fraud-status slicer.

## Repository structure

```text
financial-transaction-fraud-detection/
├── README.md
├── requirements.txt
├── data/
│   └── README.md
├── notebooks/
│   └── Financial_Transaction_Fraud_Analysis_Reviewed.ipynb
├── sql/
│   ├── README.md
│   ├── 00_setup.sql
│   ├── 01_business_overview.sql
│   └── 02_retrospective_risk_investigation.sql
├── docs/
│   ├── business_brief.md
│   └── interview_guide.md
└── dashboard/
    ├── Financial_Transaction_Fraud_Analytics_Dashboard.pbix
    └── financial_transaction_fraud_dashboard_final.png
```

## Reproduce the analysis

1. Clone this repository.
2. Create the `data/` folder and place the source CSV at `data/synthetic_mobile_money_transaction_dataset.csv`. The dataset is not committed to GitHub.
3. Install Python dependencies: `pip install -r requirements.txt`.
4. Open the notebook from the repository root and run its cells in order.
5. For the SQL analysis, follow [sql/README.md](sql/README.md). The scripts use DuckDB and the same CSV path.

## Tools and skills demonstrated
Python · Pandas · NumPy · SciPy · Scikit-learn · DuckDB SQL · Matplotlib · Seaborn · Jupyter · Power BI

Excel is not claimed as a tool used in this project. The SQL scripts are an additional repository deliverable; the notebook and dashboard findings remain grounded in the existing analysis.

## Project files
- [Python analysis notebook](notebooks/Financial_Transaction_Fraud_Analysis_Reviewed.ipynb)
- [SQL analysis](sql/README.md)
- [Business brief](docs/business_brief.md)
- [Interview preparation guide](docs/interview_guide.md)
- [Power BI dashboard](dashboard/Financial_Transaction_Fraud_Analytics_Dashboard.pbix)
- [Dashboard preview](dashboard/financial_transaction_fraud_dashboard_final.png)

## Future work
- Rebuild the model with strictly pre-authorisation features.
- Benchmark against simple, transparent baselines.
- Evaluate precision-recall trade-offs against an explicit investigation-capacity and error-cost framework.
- Validate on independent, representative data before making real-world claims.
- Add automated data-quality checks and model monitoring if representative data becomes available.

---
**Project domain:** Financial Services Analytics · Fraud Investigation · Business Intelligence · Machine Learning Evaluation
