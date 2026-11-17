# Excel analysis deliverable

Run from the repository root:

```bash
python excel/build_excel_report.py
```

This creates `excel/Financial_Transaction_Fraud_Analytics.xlsx` from the local CSV.

Workbook tabs:
- Executive Summary: KPI tiles and interpretation guardrails
- Transaction Type: counts, fraud-label rates, average and median amount
- Step Trends: transfer trends by simulation step, including a line chart
- Amount Bands: grouped transfer amounts and conditional formatting
- Data Dictionary: field and metric definitions

The workbook is generated from the source CSV, rather than using invented or manually typed transaction-level figures. The dataset itself is not committed to GitHub.
