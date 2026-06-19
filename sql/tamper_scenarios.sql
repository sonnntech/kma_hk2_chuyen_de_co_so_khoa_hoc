-- Task 08 reference SQL snippets.
-- Replace catalog/schema/table names with values from config/demo_config.py.
-- The Python notebook is the supported runner because it enforces confirmation,
-- shows before/after rows, and runs verification after each scenario.

-- Modify one transaction amount.
UPDATE workspace.blockchain_pipeline_demo.silver_transactions
SET amount = CAST(amount + 1.00 AS DECIMAL(18, 2))
WHERE transaction_id = '<TRANSACTION_ID>';

-- Delete one transaction.
DELETE FROM workspace.blockchain_pipeline_demo.silver_transactions
WHERE transaction_id = '<TRANSACTION_ID>';

-- Insert one fake transaction.
INSERT INTO workspace.blockchain_pipeline_demo.silver_transactions
SELECT
    'TX_FAKE_TAMPER_0001',
    'CUS_FAKE',
    current_timestamp(),
    'Tamper Product',
    CAST(1 AS INT),
    CAST(99.99 AS DECIMAL(18, 2)),
    CAST(99.99 AS DECIMAL(18, 2)),
    'TAMPER_DEMO',
    '<PIPELINE_RUN_ID>',
    current_timestamp(),
    'tamper_scenario';

-- Ledger metadata tampering examples.
UPDATE workspace.blockchain_pipeline_demo.blockchain_ledger
SET transformation = 'tampered transformation metadata'
WHERE pipeline_run_id = '<PIPELINE_RUN_ID>'
  AND pipeline_stage = 'SILVER';
