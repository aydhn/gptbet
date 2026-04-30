from datetime import datetime
from .contracts import CohortPauseRecord, PauseReasonRecord

def pause_cohort_progression(cohort_id: str, reason: str) -> CohortPauseRecord:
    return CohortPauseRecord(
        cohort_id=cohort_id,
        reason=reason
    )

def summarize_pause_reason(reason_id: str, description: str) -> PauseReasonRecord:
    return PauseReasonRecord(
        reason_id=reason_id,
        description=description
    )
