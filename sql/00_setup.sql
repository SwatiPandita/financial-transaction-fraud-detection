-- Create a typed DuckDB view over the local source CSV.
-- Run from the repository root.
CREATE OR REPLACE VIEW transactions AS
SELECT
    CAST(step AS INTEGER) AS step,
    CAST(transactionType AS VARCHAR) AS transaction_type,
    CAST(amount AS DOUBLE) AS amount,
    CAST(initiator AS VARCHAR) AS sender_id,
    CAST(oldBalInitiator AS DOUBLE) AS sender_balance_before,
    CAST(newBalInitiator AS DOUBLE) AS sender_balance_after,
    CAST(recipient AS VARCHAR) AS recipient_id,
    CAST(oldBalRecipient AS DOUBLE) AS recipient_balance_before,
    CAST(newBalRecipient AS DOUBLE) AS recipient_balance_after,
    CAST(isFraud AS INTEGER) AS is_fraud
FROM read_csv_auto('data/synthetic_mobile_money_transaction_dataset.csv', header = true);

SELECT COUNT(*) AS row_count,
       SUM(is_fraud) AS fraud_label_count,
       COUNT(DISTINCT transaction_type) AS transaction_types
FROM transactions;
