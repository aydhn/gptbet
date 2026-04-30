from typing import List, Optional
import datetime
from .contracts import StablePointerAdvanceRecord, AdvancementMode, AdoptionStatus, StableAdoptionRecord

def validate_pointer_advancement_scope(adoption_scope: str, allowed_scopes: List[str]) -> bool:
    return adoption_scope in allowed_scopes

def build_stable_pointer_advance(adoption_id: str, old_ref: str, new_ref: str, mode: AdvancementMode, rollback_target: str, scope_notes: List[str]) -> StablePointerAdvanceRecord:
    return StablePointerAdvanceRecord(
        advance_id=f"adv_{datetime.datetime.now(datetime.timezone.utc).timestamp()}",
        adoption_id=adoption_id,
        old_stable_pointer_ref=old_ref,
        new_stable_pointer_ref=new_ref,
        advancement_mode=mode,
        limited_scope_notes=scope_notes,
        rollback_target_ref=rollback_target
    )

def commit_limited_pointer_advance(adoption: StableAdoptionRecord, advance_record: StablePointerAdvanceRecord) -> StableAdoptionRecord:
    adoption.previous_stable_pointer_ref = advance_record.old_stable_pointer_ref
    adoption.proposed_stable_pointer_target = advance_record.new_stable_pointer_ref
    adoption.current_status = AdoptionStatus.STABLE_POINTER_ADVANCED
    return adoption

def validate_post_advance_state(adoption: StableAdoptionRecord) -> bool:
    if adoption.current_status != AdoptionStatus.STABLE_POINTER_ADVANCED:
        return False
    if not adoption.previous_stable_pointer_ref:
        return False
    return True
