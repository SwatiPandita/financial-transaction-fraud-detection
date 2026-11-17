# Financial Transaction Fraud Analytics

An end-to-end data analytics and exploratory machine-learning case study using a **synthetic mobile-money transaction dataset**. The project analyses transaction patterns, examines fraud-labelled activity, evaluates a classification model, and communicates findings through a Power BI dashboard.

> **Scope:** This is an exploratory case study on synthetic data, not a production-ready fraud detection system.

## Project objectives
- Explore transaction patterns and fraud-label distribution.
- Analyse transaction amounts and activity across simulation steps.
- Examine balance-mismatch patterns by fraud label.
- Train and evaluate a classification model.
- Present the analysis in an interactive Power BI dashboard.

## Dataset and scope

The analysis focuses on the TRANSFER transaction subset.

| Measure | Result |
|---|---:|
| Transfer transactions | 569,328 |
| Fraud-labelled transfers | 175,518 |
| Fraud-labelled share | 30.83% |
| Non-fraud-labelled share | 69.17% |

These figures describe this synthetic dataset and selected subset; they are not real-world fraud prevalence estimates.

**Dataset-specific observation:** All fraud-labelled records in the supplied dataset are TRANSFER transactions. This should not be generalised to real mobile-money systems.

## Workflow
1. Data loading, inspection and preparation.
2. Exploratory data analysis of fraud labels, transaction amounts and simulation steps.
3. Feature engineering and preprocessing.
4. Classification model development.
5. Held-out test evaluation.
6. Power BI dashboard development.

## Model evaluation

Held-out test-set results:

| Metric | Result |
|---|---:|
| Accuracy | 64% |
| Precision | 33% |
| Recall | 22% |
| F1-score | 0.26 |
| ROC-AUC | 0.5471 |
| PR-AUC | 0.3295 |

The majority-class accuracy baseline is approximately **70.52%**. The model's accuracy is below that baseline, and its recall is low. The ROC-AUC indicates only marginal ranking ability.

**Interpretation:** The results do not support claiming that this model is an effective fraud detector. They demonstrate the importance of transparent evaluation and documenting model limitations.

## Power BI dashboard

The dashboard includes:
- Total transfer transactions, fraudulent transactions and fraud-label rate.
- Fraud rate across simulation steps.
- Fraud versus non-fraud label distribution.
- Average transaction amount by fraud status.
- Transaction volume across simulation steps.
- Fraud rate by balance-mismatch status.
- Transaction-level sample table and fraud-status slicer.

### Balance mismatch observation

The observed fraud-label rate is 44.74% for records with a balance mismatch and 30.05% for records without one. This is an association in this synthetic dataset, not evidence of causation.

## Limitations
- The dataset is synthetic and may not represent real transaction behaviour.
- The fraud-label distribution is dataset-specific.
- Model performance is weak and below the majority-class accuracy baseline.
- Post-transaction balance fields may not be available at real-time decision points.
- Associations do not establish causal relationships.

## Tools
Python · Jupyter Notebook · Pandas · NumPy · Scikit-learn · Imbalanced-learn · Matplotlib · Seaborn · Power BI

## Intended repository structure

```text
financial-transaction-fraud-detection/
├── README.md
├── notebooks/
│   └── Financial_Transaction_Fraud_Analysis.ipynb
├── dashboard/
│   ├── Financial_Transaction_Fraud_Analytics_Dashboard.pbix
│   └── dashboard_screenshot.png
├── data/
│   └── README.md
└── requirements.txt
```

Large or licensed datasets should not be committed. Document how to obtain the dataset in `data/README.md`.

## Future improvements
- Validate on representative real-world data where legally available.
- Restrict predictors to information available at prediction time.
- Compare models using stratified validation and imbalance-aware metrics.
- Tune thresholds using the business costs of false positives and false negatives.
- Investigate temporal validation and data leakage.

---
**Project focus:** Data Analytics · Exploratory Machine Learning · Power BI
