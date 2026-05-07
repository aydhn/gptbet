import uuid
from typing import List, Dict, Any
from datetime import datetime, timezone
from .contracts import (
    WorldwideVisibilityLedgerRecord,
    VisibilityLedgerEntryRecord,
    VisibilityLedgerSuppressionRecord
)

def build_worldwide_visibility_ledger(ledger_family: str, entries: List[VisibilityLedgerEntryRecord], suppressions: List[VisibilityLedgerSuppressionRecord]) -> WorldwideVisibilityLedgerRecord:
    status = "ledger_verified"
    warnings = []

    if suppressions:
        status = "ledger_caveated"
        warnings.append("Visibility suppression active.")

    return WorldwideVisibilityLedgerRecord(
        worldwide_visibility_ledger_id=str(uuid.uuid4()),
        ledger_family=ledger_family,
        entry_refs=[e.entry_id for e in entries],
        shift_refs=[],
        suppression_refs=[s.suppression_id for s in suppressions],
        restoration_refs=[],
        gap_refs=[],
        residue_refs=[],
        continuity_refs=[],
        ledger_status=status,
        warnings=warnings
    )

def register_visibility_ledger_entry(entry_family: str) -> VisibilityLedgerEntryRecord:
    return VisibilityLedgerEntryRecord(
        entry_id=str(uuid.uuid4()),
        entry_family=entry_family
    )

def summarize_worldwide_visibility_ledger(ledger: WorldwideVisibilityLedgerRecord) -> Dict[str, Any]:
    return {
        "ledger_id": ledger.worldwide_visibility_ledger_id,
        "status": ledger.ledger_status,
        "entry_count": len(ledger.entry_refs),
        "suppression_count": len(ledger.suppression_refs),
        "warnings": ledger.warnings
    }
