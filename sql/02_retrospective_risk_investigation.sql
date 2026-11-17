-- RETROSPECTIVE ONLY: these indicators require post-transaction balances.
-- Do not treat them as pre-authorisation predictors.
WITH transfer_features AS (
    SELECT *,
        ABS((sender_balance_before - sender_balance_after) - amount) AS sender_mismatch,
        ABS((recipient_balance_after - recipient_balance_before) - amount) AS recipient_mismatch
    FROM transactions
    WHERE transaction_type = 'TRANSFER'
)
SELECT CASE WHEN sender_mismatch > 0.01 THEN 'Mismatch' ELSE 'No mismatch' END AS sender_balance_check,
       CASE WHEN recipient_mismatch > 0.01 THEN 'Mismatch' ELSE 'No mismatch' END AS recipient_balance_check,
       COUNT(*) AS transaction_count,
       SUM(is_fraud) AS fraud_label_count,
       ROUND(100.0 * AVG(is_fraud), 2) AS fraud_label_rate_pct
FROM transfer_features
GROUP BY 1, 2
ORDER BY transaction_count DESC;

-- Account-level retrospective summary; observed label rate is not a causal risk score.
SELECT sender_id,
       COUNT(*) AS transfer_count,
       SUM(is_fraud) AS fraud_label_count,
       ROUND(100.0 * AVG(is_fraud), 2) AS observed_label_rate_pct,
       ROUND(AVG(amount), 2) AS average_transfer_amount
FROM transactions
WHERE transaction_type = 'TRANSFER'
GROUP BY sender_id
HAVING COUNT(*) >= 5
ORDER BY observed_label_rate_pct DESC, transfer_count DESC
LIMIT 100;
