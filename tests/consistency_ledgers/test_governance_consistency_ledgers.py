from sports_signal_bot.consistency_ledgers.consistency_ledgers import (
    build_governance_consistency_ledger,
)
from sports_signal_bot.consistency_ledgers.contracts import (
    ConsistencyEntryParams,
    ConsistencyLedgerFamily,
    ConsistencyShiftFamily,
    ConsistencyState,
    ContradictionFamily,
    LedgerEntryFamily,
)
from sports_signal_bot.consistency_ledgers.contradictions import (
    classify_contradiction_severity,
    detect_consistency_contradictions,
)
from sports_signal_bot.consistency_ledgers.ledger_entries import (
    register_consistency_entry,
)
from sports_signal_bot.consistency_ledgers.shifts import (
    compute_consistency_shifts,
)


def test_stale_entries_create_contradiction():
    ledger = build_governance_consistency_ledger(
        ConsistencyLedgerFamily.GOVERNANCE_CONSISTENCY_LEDGER
    )

    params1 = ConsistencyEntryParams(
        family=LedgerEntryFamily.CONTEXT_CONSISTENCY_ENTRY,
        source_ref="src1",
        source_family="fam1",
        currentness="stale",
        consistency=ConsistencyState.STALE_CONSISTENCY,
        caveats="none",
    )
    entry1 = register_consistency_entry(ledger, params1)
    params2 = ConsistencyEntryParams(
        family=LedgerEntryFamily.PROOF_FRESHNESS_CONSISTENCY_ENTRY,
        source_ref="src2",
        source_family="fam2",
        currentness="stale",
        consistency=ConsistencyState.STALE_CONSISTENCY,
        caveats="none",
    )
    entry2 = register_consistency_entry(ledger, params2)

    entries = {
        entry1.consistency_entry_id: entry1,
        entry2.consistency_entry_id: entry2,
    }

    contradictions = detect_consistency_contradictions(ledger, entries)
    assert len(contradictions) == 1
    assert (
        contradictions[0].contradiction_family
        == ContradictionFamily.FRESHNESS_CONTRADICTION
    )
    assert classify_contradiction_severity(contradictions[0]) == "high"


def test_consistency_shift_computation():
    ledger = build_governance_consistency_ledger(
        ConsistencyLedgerFamily.GOVERNANCE_CONSISTENCY_LEDGER
    )
    params = ConsistencyEntryParams(
        family=LedgerEntryFamily.CONTEXT_CONSISTENCY_ENTRY,
        source_ref="src1",
        source_family="fam1",
        currentness="current",
        consistency=ConsistencyState.CONSISTENT_WITH_CAPS,
        caveats="none",
    )
    entry = register_consistency_entry(ledger, params)

    shift = compute_consistency_shifts(
        ledger,
        entry,
        ConsistencyState.CONSISTENT_WITH_CAPS,
        ConsistencyState.CONTRADICTED,
        "Conflict detected",
    )
    assert shift.shift_family == ConsistencyShiftFamily.NEWLY_CONTRADICTED

    shift2 = compute_consistency_shifts(
        ledger,
        entry,
        ConsistencyState.CONTRADICTED,
        ConsistencyState.CONSISTENT_WITH_CAPS,
        "Conflict resolved",
    )
    assert shift2.shift_family == ConsistencyShiftFamily.CONTRADICTION_RESOLVED
