from typing import Dict, Any
from .contracts import CohortShrinkRecord, ShrinkReasonRecord

def build_shrink_scope_plan(cohort_id: str, original: Dict[str, Any], new: Dict[str, Any]) -> dict:
    return {
        "cohort_id": cohort_id,
        "original_scope": original,
        "target_scope": new
    }

def apply_cohort_shrink(cohort_id: str, original: Dict[str, Any], new: Dict[str, Any], reason: str) -> CohortShrinkRecord:
    return CohortShrinkRecord(
        cohort_id=cohort_id,
        original_scope=original,
        new_scope=new,
        reason=reason
    )

def summarize_shrink_reason(reason_id: str, description: str) -> ShrinkReasonRecord:
    return ShrinkReasonRecord(
        reason_id=reason_id,
        description=description
    )
