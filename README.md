# Financial Transaction Fraud Analytics & Risk Investigation

**An end-to-end analytics case study** exploring fraud-labelled patterns across 1.72 million synthetic mobile-money transactions with Python, DuckDB SQL, statistical analysis, machine-learning evaluation, Power BI and an Excel report generator.

> **Honest scope:** This is a retrospective educational analysis on synthetic data. The original classifier is weak and is not suitable for production fraud decisions. A separate point-in-time model experiment is provided and must be run before quoting its results.

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
- Balance-mismatch indicators have statistically significant chi-square associations, but small effect sizes: Cramér's V is approximately 0.0375 (sender) and 0.0413 (recipient).
- Historical sender and recipient activity features are built from earlier simulation steps.
- The original Random Forest has weak chronological test performance.

## Original model evaluation

| Metric | Result |
|---|---:|
| Accuracy | 64% |
| Precision (fraud class) | 33% |
| Recall (fraud class) | 22% |
| F1-score (fraud class) | 0.26 |
| ROC-AUC | 0.5471 |
| PR-AUC | 0.3295 |

The majority-class accuracy baseline is approximately **70.52%**. The original model's accuracy is below this baseline, and its ROC-AUC is only slightly above random ranking. It is not suitable for operational decisions.

### Feature-timing limitation
The original notebook's balance mismatch features use post-transaction balance values. They are suitable for retrospective investigation but may not be available at authorisation time. The new `modeling/point_in_time_model.py` experiment excludes these fields and uses pre-transaction values plus history from earlier simulation steps. Its metrics are not known until the script is run locally.

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
├── modeling/
│   ├── README.md
│   └── point_in_time_model.py
├── sql/
│   ├── README.md
│   ├── 00_setup.sql
│   ├── 01_business_overview.sql
│   └── 02_retrospective_risk_investigation.sql
├── excel/
│   ├── README.md
│   └── build_excel_report.py
├── docs/
│   ├── business_brief.md
│   └── interview_guide.md
└── dashboard/
    ├── Financial_Transaction_Fraud_Analytics_Dashboard.pbix
    └── financial_transaction_fraud_dashboard_final.png
```

## Reproduce the analysis

1. Clone this repository.
2. Place the source CSV at `data/synthetic_mobile_money_transaction_dataset.csv`. The dataset is not committed to GitHub.
3. Install dependencies: `pip install -r requirements.txt`.
4. Run the original notebook from the repository root.
5. Run the point-in-time modelling experiment: `python modeling/point_in_time_model.py`.
6. Generate the Excel workbook: `python excel/build_excel_report.py`.
7. For SQL analysis, follow [sql/README.md](sql/README.md).

## Tools and skills
Python · Pandas · NumPy · SciPy · Scikit-learn · DuckDB SQL · Excel report automation (openpyxl) · Matplotlib · Seaborn · Jupyter · Power BI

Excel is represented by a reproducible workbook-generation script. The generated workbook is created locally from the source CSV; it is not claimed to have been generated or validated in this repository until that script has been run.

## Project files
- [Python analysis notebook](notebooks/Financial_Transaction_Fraud_Analysis_Reviewed.ipynb)
- [Point-in-time model experiment](modeling/README.md)
- [SQL analysis](sql/README.md)
- [Excel report generator](excel/README.md)
- [Business brief](docs/business_brief.md)
- [Interview preparation guide](docs/interview_guide.md)
- [Power BI dashboard](dashboard/Financial_Transaction_Fraud_Analytics_Dashboard.pbix)
- [Dashboard preview](dashboard/financial_transaction_fraud_dashboard_final.png)

## Future work
- Run and inspect the point-in-time model metrics.
- Compare additional transparent baselines and tune alert thresholds against review capacity and error costs.
- Validate on independent, representative data before making real-world claims.
- Add automated data-quality checks and model monitoring if representative data becomes available.

---
**Project domain:** Financial Services Analytics · Fraud Investigation · Business Intelligence · Machine Learning Evaluation
