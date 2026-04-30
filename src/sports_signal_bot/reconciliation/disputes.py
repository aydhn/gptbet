
from typing import List
from sports_signal_bot.reconciliation.contracts import FieldConflictRecord, DisputeRecord, ReconciliationGroupRecord

def should_raise_dispute(conflicts: List[FieldConflictRecord]) -> bool:
    for c in conflicts:
        if c.severity == "critical":
            return True
    return False

def build_dispute_record(group: ReconciliationGroupRecord, conflicts: List[FieldConflictRecord]) -> DisputeRecord:
    reasons = [f"Critical conflict in {c.field_name}" for c in conflicts if c.severity == "critical"]
    return DisputeRecord(
        dispute_id=f"dispute_{group.entity_key}",
        group_id=group.group_id,
        data_family=group.data_family,
        entity_key=group.entity_key,
        reasons=reasons,
        severity="critical"
    )

def summarize_dispute_reasons(dispute: DisputeRecord) -> str:
    return "; ".join(dispute.reasons)

def suggest_manual_resolution_path(dispute: DisputeRecord) -> str:
    return "Manual review required by operator."
