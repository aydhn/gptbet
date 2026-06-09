from typing import List

from sports_signal_bot.reconciliation.contracts import (
    FieldConflictRecord, ReconciliationGroupRecord)


def detect_conflicts(
    group: ReconciliationGroupRecord,
) -> List[FieldConflictRecord]:
    conflicts = []
    if len(group.observations) <= 1:
        return conflicts

    all_fields = set().union(*(obs.payload for obs in group.observations))

    for field in all_fields:
        values_seen = {}
        for obs in group.observations:
            if field in obs.payload:
                values_seen[obs.provider_name] = obs.payload[field]

        # Are there distinct values?
        distinct_vals = set(str(v) for v in values_seen.values())
        if len(distinct_vals) > 1:
            severity = "medium"
            if field in ["status", "final_score"]:
                severity = "critical"

            conflicts.append(
                FieldConflictRecord(
                    conflict_id=f"conf_{group.entity_key}_{field}",
                    group_id=group.group_id,
                    field_name=field,
                    severity=severity,
                    conflict_type=f"{field}_mismatch",
                    values=values_seen,
                )
            )
    return conflicts


def classify_conflict_severity(conflict_type: str) -> str:
    if "status" in conflict_type or "score" in conflict_type:
        return "critical"
    return "medium"
