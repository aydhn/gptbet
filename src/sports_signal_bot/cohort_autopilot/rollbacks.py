from datetime import datetime
from typing import Optional
from .contracts import CohortRollbackRecord, ActivationLevel

def build_cohort_rollback_plan(cohort_id: str, target_level: ActivationLevel) -> dict:
    return {
        "cohort_id": cohort_id,
        "target_level": target_level.value
    }

def execute_cohort_rollback(cohort_id: str, target_level: ActivationLevel, reason: str) -> CohortRollbackRecord:
    return CohortRollbackRecord(
        cohort_id=cohort_id,
        rollback_id=f"rb_{cohort_id}_{int(datetime.utcnow().timestamp())}",
        rollback_level=target_level,
        reason=reason
    )

def verify_cohort_rollback(rollback: CohortRollbackRecord) -> bool:
    return True

def summarize_cohort_rollback(rollback: CohortRollbackRecord) -> dict:
    return {
        "cohort_id": rollback.cohort_id,
        "rollback_id": rollback.rollback_id,
        "target_level": rollback.rollback_level.value,
        "reason": rollback.reason
    }
