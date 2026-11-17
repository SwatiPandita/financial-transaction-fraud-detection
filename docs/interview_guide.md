# Interview guide: Financial Transaction Fraud Analytics

## 30-second explanation
I analysed 1.72 million synthetic mobile-money transactions to investigate where fraud labels were concentrated and which transaction and account patterns were associated with them. I used Python for data quality checks, EDA, statistical association tests and historical account-feature engineering, built a Power BI dashboard, and added DuckDB SQL scripts for reusable business summaries. I evaluated a Random Forest chronologically and reported its weak performance transparently rather than presenting it as production-ready.

## Questions to prepare

### Why focus on TRANSFER transactions?
All fraud-labelled rows in this supplied dataset were TRANSFER records. I focused detailed analysis there because that is where labels occur in this sample. I would not generalise this pattern to other payment systems.

### Why use Cramér's V after chi-square?
Chi-square tests association. With a very large sample, a tiny association can still have a very small p-value. Cramér's V communicates effect size; the observed values (about 0.038 and 0.041) are small.

### Why is the model not good enough?
Chronological test ROC-AUC is 0.5471 and fraud recall is 22%. It misses many fraud-labelled records. Accuracy is also below the majority-class baseline, so it is not a useful operational detector.

### What is the feature-timing concern?
Balance mismatch features use new balances after a transaction. These may not be available at authorisation time. They support retrospective investigation but should not be treated as valid pre-authorisation predictors without verifying when the data becomes available.

### What would you do next?
Create point-in-time features using only information available before authorisation, including historical sender/recipient behaviour from earlier steps. Compare transparent baselines and models on a later chronological holdout. Select thresholds based on false-alert and missed-fraud costs, not accuracy alone.

## Describe tools accurately
- Python: notebook analysis, statistics, feature engineering and model evaluation.
- Power BI: interactive dashboard.
- DuckDB SQL: reusable SQL scripts added to the repository.
- Excel: do not claim it was used in this project unless an actual Excel deliverable is added and documented.
