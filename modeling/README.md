# Point-in-time model experiment

Run from the repository root:

```bash
python modeling/point_in_time_model.py
```

The script uses only fields intended to be available at or before the event:
- simulation step and transaction amount
- sender and recipient balances before the transaction
- sender/recipient transaction counts and average amounts from earlier simulation steps only

It excludes new/post-transaction balances, balance mismatch features, account identifiers and the fraud label from feature construction.

The script creates a strict chronological train/validation/test split, compares a majority-class baseline with a Random Forest, and writes metrics to `modeling/outputs/`.

**Important:** this is a new experiment and its metrics must be run and inspected before they are quoted. It is not assumed to outperform the earlier model. Dataset is synthetic and results are educational only.
