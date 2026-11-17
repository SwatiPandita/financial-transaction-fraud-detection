"""Point-in-time fraud-label modelling experiment.

Uses only transaction fields available before/at the transaction event plus
account history from strictly earlier simulation steps. The supplied dataset
is synthetic; this experiment is not a production fraud system.
"""
from pathlib import Path
import json
import warnings

import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, average_precision_score, precision_score,
    recall_score, f1_score, roc_auc_score, confusion_matrix,
    classification_report
)

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "synthetic_mobile_money_transaction_dataset.csv"
OUTPUT_DIR = ROOT / "modeling" / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Dataset missing: {DATA_PATH}. See data/README.md for setup."
    )

df = pd.read_csv(DATA_PATH)
required = {
    "step", "transactionType", "amount", "initiator", "oldBalInitiator",
    "recipient", "oldBalRecipient", "isFraud"
}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")

# The label is excluded from every feature calculation.
transfers = df.loc[df["transactionType"].eq("TRANSFER")].copy()
transfers["initiator"] = transfers["initiator"].astype(str)
transfers["recipient"] = transfers["recipient"].astype(str)
transfers = transfers.sort_values(["step"], kind="stable").reset_index(drop=True)

def prior_step_features(data: pd.DataFrame, account_col: str, prefix: str) -> pd.DataFrame:
    """Aggregate by account and step, then shift cumulative stats by one step."""
    per_step = (
        data.groupby([account_col, "step"], sort=True)["amount"]
        .agg(step_txn_count="size", step_amount_sum="sum")
        .reset_index()
        .sort_values([account_col, "step"], kind="stable")
    )
    grouped = per_step.groupby(account_col, sort=False)
    per_step[f"{prefix}_prior_count"] = (
        grouped["step_txn_count"].cumsum() - per_step["step_txn_count"]
    )
    per_step[f"{prefix}_prior_amount_sum"] = (
        grouped["step_amount_sum"].cumsum() - per_step["step_amount_sum"]
    )
    per_step[f"{prefix}_prior_avg_amount"] = (
        per_step[f"{prefix}_prior_amount_sum"] /
        per_step[f"{prefix}_prior_count"].replace(0, np.nan)
    )
    return per_step[
        [account_col, "step", f"{prefix}_prior_count", f"{prefix}_prior_avg_amount"]
    ]

sender_history = prior_step_features(transfers, "initiator", "sender")
recipient_history = prior_step_features(transfers, "recipient", "recipient")

data = transfers.merge(sender_history, on=["initiator", "step"], how="left")
data = data.merge(recipient_history, on=["recipient", "step"], how="left")
history_cols = [
    "sender_prior_count", "sender_prior_avg_amount",
    "recipient_prior_count", "recipient_prior_avg_amount"
]
data[history_cols] = data[history_cols].fillna(0)

# Point-in-time features: no post-transaction balances, mismatch flags,
# new balances, target-derived aggregates, or account IDs.
feature_cols = [
    "step", "amount", "oldBalInitiator", "oldBalRecipient",
    *history_cols
]
X = data[feature_cols].replace([np.inf, -np.inf], np.nan).fillna(0)
y = data["isFraud"].astype(int)

# Strict chronological split by simulation step: early train, middle validation,
# latest test. Boundaries are quantiles of unique step values.
steps = np.sort(data["step"].dropna().unique())
if len(steps) < 5:
    raise ValueError("Not enough distinct simulation steps for chronological evaluation.")
train_end = steps[int((len(steps) - 1) * 0.65)]
val_end = steps[int((len(steps) - 1) * 0.80)]

train_mask = data["step"] <= train_end
val_mask = (data["step"] > train_end) & (data["step"] <= val_end)
test_mask = data["step"] > val_end
if not train_mask.any() or not val_mask.any() or not test_mask.any():
    raise ValueError("Chronological split produced an empty partition.")

X_train, y_train = X.loc[train_mask], y.loc[train_mask]
X_val, y_val = X.loc[val_mask], y.loc[val_mask]
X_test, y_test = X.loc[test_mask], y.loc[test_mask]

models = {
    "Majority baseline": DummyClassifier(strategy="most_frequent"),
    "Random Forest (point-in-time)": RandomForestClassifier(
        n_estimators=160,
        max_depth=14,
        min_samples_leaf=8,
        class_weight="balanced_subsample",
        random_state=42,
        n_jobs=-1
    )
}

rows = []
details = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    val_prob = model.predict_proba(X_val)[:, 1]
    test_prob = model.predict_proba(X_test)[:, 1]

    # Use a fixed threshold as a transparent reference point; threshold
    # selection should later be tied to operational review capacity and costs.
    threshold = 0.50
    pred = (test_prob >= threshold).astype(int)
    row = {
        "model": name,
        "train_rows": int(len(X_train)),
        "validation_rows": int(len(X_val)),
        "test_rows": int(len(X_test)),
        "train_last_step": int(train_end),
        "validation_last_step": int(val_end),
        "test_first_step": int(data.loc[test_mask, "step"].min()),
        "test_fraud_rate_pct": float(y_test.mean() * 100),
        "threshold": threshold,
        "accuracy": float(accuracy_score(y_test, pred)),
        "precision": float(precision_score(y_test, pred, zero_division=0)),
        "recall": float(recall_score(y_test, pred, zero_division=0)),
        "f1": float(f1_score(y_test, pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, test_prob)) if y_test.nunique() > 1 else None,
        "pr_auc": float(average_precision_score(y_test, test_prob)),
        "confusion_matrix": confusion_matrix(y_test, pred).tolist()
    }
    rows.append(row)
    details[name] = {
        "classification_report": classification_report(
            y_test, pred, output_dict=True, zero_division=0
        ),
        "confusion_matrix": row["confusion_matrix"]
    }

metrics = pd.DataFrame(rows)
metrics.to_csv(OUTPUT_DIR / "point_in_time_model_comparison.csv", index=False)
with open(OUTPUT_DIR / "point_in_time_model_results.json", "w", encoding="utf-8") as f:
    json.dump({
        "scope": "Synthetic dataset; exploratory only; not production-ready.",
        "feature_cols": feature_cols,
        "excluded_post_event_fields": [
            "newBalInitiator", "newBalRecipient",
            "sender/recipient balance mismatch features"
        ],
        "split": {
            "train_last_step": int(train_end),
            "validation_last_step": int(val_end),
            "test_first_step": int(data.loc[test_mask, "step"].min())
        },
        "metrics": rows,
        "details": details
    }, f, indent=2)

print("Point-in-time model comparison")
print(metrics.drop(columns=["confusion_matrix"]).round(4).to_string(index=False))
print("\nSaved outputs to:", OUTPUT_DIR)
print("\nIMPORTANT: Interpret performance on this synthetic dataset only.")
