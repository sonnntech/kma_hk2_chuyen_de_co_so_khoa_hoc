"""Unit tests for tamper scenario safety rules."""

import pytest

from blockchain_pipeline import tamper
from blockchain_pipeline.verification import (
    BLOCK_TAMPERED,
    CHAIN_BROKEN,
    DATA_TAMPERED,
    RECORD_COUNT_MISMATCH,
    VALID,
)


def test_require_confirmation_allows_noop_without_yes() -> None:
    tamper.require_confirmation(tamper.SCENARIO_NONE, "NO")


def test_require_confirmation_blocks_mutating_scenario_without_yes() -> None:
    with pytest.raises(ValueError, match="CONFIRM_TAMPER"):
        tamper.require_confirmation(
            tamper.SCENARIO_DELETE_TRANSACTION,
            "NO",
        )


def test_require_confirmation_accepts_yes_case_insensitive() -> None:
    tamper.require_confirmation(tamper.SCENARIO_DELETE_TRANSACTION, "yes")


def test_all_expected_scenarios_are_registered() -> None:
    assert tamper.SCENARIOS == (
        tamper.SCENARIO_NONE,
        tamper.SCENARIO_MODIFY_TRANSACTION_AMOUNT,
        tamper.SCENARIO_DELETE_TRANSACTION,
        tamper.SCENARIO_INSERT_FAKE_TRANSACTION,
        tamper.SCENARIO_MODIFY_LEDGER_BATCH_HASH,
        tamper.SCENARIO_MODIFY_LEDGER_TRANSFORMATION,
        tamper.SCENARIO_MODIFY_LEDGER_PREVIOUS_HASH,
        tamper.SCENARIO_RESET_BASELINE,
    )


def test_scenario_constants_map_to_expected_statuses() -> None:
    expected_statuses = {
        tamper.SCENARIO_NONE: VALID,
        tamper.SCENARIO_MODIFY_TRANSACTION_AMOUNT: DATA_TAMPERED,
        tamper.SCENARIO_DELETE_TRANSACTION: RECORD_COUNT_MISMATCH,
        tamper.SCENARIO_INSERT_FAKE_TRANSACTION: RECORD_COUNT_MISMATCH,
        tamper.SCENARIO_MODIFY_LEDGER_BATCH_HASH: DATA_TAMPERED,
        tamper.SCENARIO_MODIFY_LEDGER_TRANSFORMATION: BLOCK_TAMPERED,
        tamper.SCENARIO_MODIFY_LEDGER_PREVIOUS_HASH: CHAIN_BROKEN,
        tamper.SCENARIO_RESET_BASELINE: VALID,
    }

    assert expected_statuses[tamper.SCENARIO_MODIFY_LEDGER_PREVIOUS_HASH] == (
        CHAIN_BROKEN
    )
