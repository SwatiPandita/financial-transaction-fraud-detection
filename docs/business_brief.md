# Business brief: Financial Transaction Fraud Analytics

## Executive question
What patterns distinguish fraud-labelled mobile-money transfers in this synthetic transaction sample, and what can an investigation team responsibly learn from them?

## Scope
- 1,720,181 synthetic transactions across 10 columns.
- 569,328 TRANSFER transactions analysed.
- 175,518 fraud-labelled transfers (30.83% of transfers).
- All fraud-labelled rows in this supplied dataset are TRANSFER records; this is dataset-specific.

## Evidence-led observations
1. Fraud labels are concentrated in TRANSFER records in this sample. This guides the scope of this dataset's investigation, not a universal fraud rule.
2. Balance-mismatch indicators have statistically significant chi-square associations, but small Cramér's V effect sizes (sender 0.0375; recipient 0.0413). Tiny p-values in a large sample do not imply strong predictive value or causation.
3. The chronological Random Forest test metrics are weak: precision 33%, recall 22%, ROC-AUC 0.5471 and PR-AUC 0.3295. Accuracy (64%) is below the approximately 70.52% majority-class baseline.
4. Balance mismatch variables use post-transaction balance fields. They support retrospective investigation but may not exist at authorisation time.

## Recommendations
- Treat this as retrospective analysis; do not use the current classifier to block transactions.
- Build a point-in-time feature set using only data available before authorisation.
- Compare against simple baselines and evaluate on later time periods.
- Define false-positive and false-negative costs and investigation capacity before selecting a threshold.
- Validate on representative, governed real-world data before making operational claims.

## Future success criteria
A future model should outperform transparent baselines on a genuinely future holdout, produce an alert volume investigators can review, remain stable across time and segments, and have documented feature availability and monitoring controls.

## Disclaimer
Educational case study using synthetic data. It does not establish causality, real-world fraud prevalence or production model performance.
