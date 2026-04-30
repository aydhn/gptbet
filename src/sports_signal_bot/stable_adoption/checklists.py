from typing import List, Optional
import datetime
from .contracts import ActivationChecklistResultRecord, ActivationChecklistItemRecord, ActivationChecklistFailureRecord

def build_activation_checklist(adoption_id: str, handoff_evidence_present: bool, approvals_complete: bool,
                               rollback_target_known: bool, docs_linked: bool, post_activation_plan_ready: bool,
                               no_blockers: bool) -> ActivationChecklistResultRecord:
    items = [
        ActivationChecklistItemRecord(
            item_id="chk_fresh_handoff",
            description="fresh handoff evidence present",
            is_checked=handoff_evidence_present
        ),
        ActivationChecklistItemRecord(
            item_id="chk_approvals",
            description="final approvals complete if required",
            is_checked=approvals_complete
        ),
        ActivationChecklistItemRecord(
            item_id="chk_rollback",
            description="rollback target resolvable",
            is_checked=rollback_target_known
        ),
        ActivationChecklistItemRecord(
            item_id="chk_docs",
            description="docs/runbooks linked",
            is_checked=docs_linked
        ),
        ActivationChecklistItemRecord(
            item_id="chk_post_activation",
            description="post-activation verification plan complete",
            is_checked=post_activation_plan_ready
        ),
        ActivationChecklistItemRecord(
            item_id="chk_blockers",
            description="no unresolved critical disputes or blockers",
            is_checked=no_blockers
        )
    ]
    is_complete = all(item.is_checked for item in items)
    return ActivationChecklistResultRecord(
        checklist_id=f"chk_list_{datetime.datetime.now(datetime.timezone.utc).timestamp()}",
        adoption_id=adoption_id,
        items=items,
        is_complete=is_complete
    )

def validate_activation_checklist(checklist: ActivationChecklistResultRecord) -> bool:
    return checklist.is_complete

def summarize_activation_failures(checklist: ActivationChecklistResultRecord) -> List[ActivationChecklistFailureRecord]:
    failures = []
    if not checklist.is_complete:
        for item in checklist.items:
            if not item.is_checked:
                failures.append(ActivationChecklistFailureRecord(
                    failure_id=f"fail_{item.item_id}",
                    checklist_id=checklist.checklist_id,
                    reason=f"Failed checklist item: {item.description}"
                ))
    return failures

def block_activation_if_checklist_incomplete(checklist: ActivationChecklistResultRecord) -> bool:
    return not checklist.is_complete
