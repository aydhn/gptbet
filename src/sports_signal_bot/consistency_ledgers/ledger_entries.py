from sports_signal_bot.consistency_ledgers.contracts import (
    ConsistencyEntryParams, ConsistencyLedgerEntryRecord,
    SovereignGovernanceConsistencyLedgerRecord)
from sports_signal_bot.consistency_ledgers.utils import generate_id


def register_consistency_entry(
    ledger: SovereignGovernanceConsistencyLedgerRecord,
    params: ConsistencyEntryParams,
) -> ConsistencyLedgerEntryRecord:
    entry = ConsistencyLedgerEntryRecord(
        consistency_entry_id=generate_id("cons_entry"),
        entry_family=params.family,
        source_ref=params.source_ref,
        source_family=params.source_family,
        currentness_state=params.currentness,
        consistency_state=params.consistency,
        contradiction_state="none",
        caveat_state=params.caveats,
        warnings=[],
    )
    ledger.entry_refs.append(entry.consistency_entry_id)
    return entry
