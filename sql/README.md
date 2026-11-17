# SQL analysis with DuckDB

The SQL layer provides reproducible business summaries that complement the Python notebook. The SQL scripts are included as project deliverables; they should be executed locally against the source CSV.

## Run

From the repository root:

```bash
pip install duckdb
duckdb fraud_analytics.duckdb < sql/00_setup.sql
duckdb fraud_analytics.duckdb < sql/01_business_overview.sql
duckdb fraud_analytics.duckdb < sql/02_retrospective_risk_investigation.sql
```

The setup script creates a view named `transactions` using `data/synthetic_mobile_money_transaction_dataset.csv`.

## Concepts
- Aggregations and conditional counts
- CTEs and CASE expressions
- Grouping and amount bands
- Median and average comparisons
- Account-level aggregation and HAVING filters

**Interpretation caution:** mismatch analysis uses post-transaction balance fields and is retrospective. All reported rates refer to labels in a synthetic dataset, not real-world fraud probabilities.
