import pytest
from sports_signal_bot.consistency_ledgers.contracts import (
    ConsistencyLedgerFamily,
    LedgerEntryFamily,
    ConsistencyState,
    ContradictionFamily,
    ConsistencyShiftFamily
)
from sports_signal_bot.consistency_ledgers.consistency_ledgers import build_governance_consistency_ledger
from sports_signal_bot.consistency_ledgers.ledger_entries import register_consistency_entry
from sports_signal_bot.consistency_ledgers.contradictions import detect_consistency_contradictions, classify_contradiction_severity
from sports_signal_bot.consistency_ledgers.shifts import compute_consistency_shifts

def test_stale_entries_create_contradiction():
    ledger = build_governance_consistency_ledger(ConsistencyLedgerFamily.GOVERNANCE_CONSISTENCY_LEDGER)

    entry1 = register_consistency_entry(
        ledger, LedgerEntryFamily.CONTEXT_CONSISTENCY_ENTRY, "src1", "fam1", "stale", ConsistencyState.STALE_CONSISTENCY, "none"
    )
    entry2 = register_consistency_entry(
        ledger, LedgerEntryFamily.PROOF_FRESHNESS_CONSISTENCY_ENTRY, "src2", "fam2", "stale", ConsistencyState.STALE_CONSISTENCY, "none"
    )

    entries = {entry1.consistency_entry_id: entry1, entry2.consistency_entry_id: entry2}

    contradictions = detect_consistency_contradictions(ledger, entries)
    assert len(contradictions) == 1
    assert contradictions[0].contradiction_family == ContradictionFamily.FRESHNESS_CONTRADICTION
    assert classify_contradiction_severity(contradictions[0]) == "high"

def test_consistency_shift_computation():
    ledger = build_governance_consistency_ledger(ConsistencyLedgerFamily.GOVERNANCE_CONSISTENCY_LEDGER)
    entry = register_consistency_entry(
        ledger, LedgerEntryFamily.CONTEXT_CONSISTENCY_ENTRY, "src1", "fam1", "current", ConsistencyState.CONSISTENT_WITH_CAPS, "none"
    )

    shift = compute_consistency_shifts(
        ledger, entry, ConsistencyState.CONSISTENT_WITH_CAPS, ConsistencyState.CONTRADICTED, "Conflict detected"
    )
    assert shift.shift_family == ConsistencyShiftFamily.NEWLY_CONTRADICTED

    shift2 = compute_consistency_shifts(
        ledger, entry, ConsistencyState.CONTRADICTED, ConsistencyState.CONSISTENT_WITH_CAPS, "Conflict resolved"
    )
    assert shift2.shift_family == ConsistencyShiftFamily.CONTRADICTION_RESOLVED
