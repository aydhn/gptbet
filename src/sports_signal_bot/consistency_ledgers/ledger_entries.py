from typing import List, Dict, Any
from sports_signal_bot.consistency_ledgers.contracts import (
    ConsistencyLedgerEntryRecord,
    LedgerEntryFamily,
    ConsistencyState,
    SovereignGovernanceConsistencyLedgerRecord
)
from sports_signal_bot.consistency_ledgers.utils import generate_id

def register_consistency_entry(
    ledger: SovereignGovernanceConsistencyLedgerRecord,
    family: LedgerEntryFamily,
    source_ref: str,
    source_family: str,
    currentness: str,
    consistency: ConsistencyState,
    caveats: str
) -> ConsistencyLedgerEntryRecord:
    entry = ConsistencyLedgerEntryRecord(
        consistency_entry_id=generate_id("cons_entry"),
        entry_family=family,
        source_ref=source_ref,
        source_family=source_family,
        currentness_state=currentness,
        consistency_state=consistency,
        contradiction_state="none",
        caveat_state=caveats,
        warnings=[]
    )
    ledger.entry_refs.append(entry.consistency_entry_id)
    return entry
