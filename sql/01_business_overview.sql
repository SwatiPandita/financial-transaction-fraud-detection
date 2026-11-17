-- Transaction-type overview
SELECT transaction_type,
       COUNT(*) AS transaction_count,
       SUM(is_fraud) AS fraud_label_count,
       ROUND(100.0 * AVG(is_fraud), 2) AS fraud_label_rate_pct,
       ROUND(AVG(amount), 2) AS average_amount,
       ROUND(MEDIAN(amount), 2) AS median_amount
FROM transactions
GROUP BY transaction_type
ORDER BY fraud_label_rate_pct DESC, transaction_count DESC;

-- Fraud-label trend by simulation step for transfers
SELECT step,
       COUNT(*) AS transaction_count,
       SUM(is_fraud) AS fraud_label_count,
       ROUND(100.0 * AVG(is_fraud), 2) AS fraud_label_rate_pct
FROM transactions
WHERE transaction_type = 'TRANSFER'
GROUP BY step
ORDER BY step;

-- Amount bands for transfer investigation
WITH amount_bands AS (
    SELECT *,
        CASE WHEN amount < 1000 THEN '< 1K'
             WHEN amount < 10000 THEN '1K–10K'
             WHEN amount < 50000 THEN '10K–50K'
             WHEN amount < 100000 THEN '50K–100K'
             ELSE '100K+' END AS amount_band
    FROM transactions
    WHERE transaction_type = 'TRANSFER'
)
SELECT amount_band,
       COUNT(*) AS transaction_count,
       SUM(is_fraud) AS fraud_label_count,
       ROUND(100.0 * AVG(is_fraud), 2) AS fraud_label_rate_pct,
       ROUND(AVG(amount), 2) AS average_amount
FROM amount_bands
GROUP BY amount_band
ORDER BY MIN(amount);
