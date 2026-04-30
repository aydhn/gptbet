from typing import List, Optional
import datetime
from .contracts import AdoptionRollbackRecord, RollbackType, StableReferenceSnapshotRecord, RollbackReadinessRecord

def compute_rollback_readiness(adoption_id: str, snapshot: Optional[StableReferenceSnapshotRecord]) -> RollbackReadinessRecord:
    is_ready = snapshot is not None
    missing = []
    if not is_ready:
        missing.append("Missing stable reference snapshot")

    return RollbackReadinessRecord(
        readiness_id=f"ready_{datetime.datetime.now(datetime.timezone.utc).timestamp()}",
        adoption_id=adoption_id,
        is_ready=is_ready,
        missing_criteria=missing,
        snapshot_ref=snapshot.snapshot_id if snapshot else None
    )

def require_rollback_readiness_before_activation(readiness: RollbackReadinessRecord) -> bool:
    return readiness.is_ready

def explain_rollback_readiness(readiness: RollbackReadinessRecord) -> str:
    if readiness.is_ready:
        return "Rollback ready. Snapshot present."
    return f"Rollback NOT ready. Missing: {', '.join(readiness.missing_criteria)}"

def build_adoption_rollback_plan(adoption_id: str, rollback_type: RollbackType, snapshot_ref: str, reason: str) -> AdoptionRollbackRecord:
    return AdoptionRollbackRecord(
        rollback_id=f"rb_{datetime.datetime.now(datetime.timezone.utc).timestamp()}",
        adoption_id=adoption_id,
        rollback_type=rollback_type,
        target_snapshot_ref=snapshot_ref,
        reason=reason
    )

def detect_rollback_triggers(verification_failed: bool, critical_blockers_found: bool) -> Optional[str]:
    if verification_failed:
        return "verification_failed"
    if critical_blockers_found:
        return "critical_blockers_discovered"
    return None

def execute_adoption_rollback(rollback_plan: AdoptionRollbackRecord) -> bool:
    # In a real system, this would restore the snapshot
    return True

def verify_rollback_state(rollback_plan: AdoptionRollbackRecord, success: bool) -> bool:
    return success

def summarize_rollback_decision(rollback_plan: AdoptionRollbackRecord) -> str:
    return f"Rollback {rollback_plan.rollback_id} to {rollback_plan.target_snapshot_ref} initiated due to: {rollback_plan.reason}"
