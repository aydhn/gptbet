import uuid
from typing import List, Dict, Any
from .contracts import PreActivationChecklistResult, PreActivationCheckItemRecord, ActivationBlockerRecord

def build_pre_activation_checklist(handoff_id: str, context: Dict[str, Any]) -> PreActivationChecklistResult:
    items = []

    # Check gates
    gates_fresh = context.get("gates_fresh", False)
    items.append(PreActivationCheckItemRecord(
        item_id=str(uuid.uuid4()),
        description="Final quality gates are fresh (within 24h).",
        is_checked=gates_fresh,
        notes="Required before activation." if not gates_fresh else ""
    ))

    # Check approvals
    approval_complete = context.get("approval_complete", False)
    items.append(PreActivationCheckItemRecord(
        item_id=str(uuid.uuid4()),
        description="All required final approvals are complete.",
        is_checked=approval_complete,
        notes="Missing approvals." if not approval_complete else ""
    ))

    # Check rollback target
    rollback_known = context.get("rollback_target_known", False)
    items.append(PreActivationCheckItemRecord(
        item_id=str(uuid.uuid4()),
        description="Rollback target and procedure are well-defined.",
        is_checked=rollback_known,
        notes="Rollback notes incomplete." if not rollback_known else ""
    ))

    # Check docs
    docs_linked = context.get("docs_linked", False)
    items.append(PreActivationCheckItemRecord(
        item_id=str(uuid.uuid4()),
        description="Relevant documentation and runbooks are linked.",
        is_checked=docs_linked,
        notes="Docs missing." if not docs_linked else ""
    ))

    is_complete = all(item.is_checked for item in items)

    return PreActivationChecklistResult(
        checklist_id=str(uuid.uuid4()),
        handoff_id=handoff_id,
        items=items,
        is_complete=is_complete
    )

def validate_pre_activation_items(checklist: PreActivationChecklistResult) -> bool:
    return checklist.is_complete

def summarize_pre_activation_failures(checklist: PreActivationChecklistResult) -> List[ActivationBlockerRecord]:
    failures = []
    if not checklist.is_complete:
        for item in checklist.items:
            if not item.is_checked:
                failures.append(ActivationBlockerRecord(
                    blocker_id=str(uuid.uuid4()),
                    handoff_id=checklist.handoff_id,
                    description=f"Failed Checklist Item: {item.description} - {item.notes}"
                ))
    return failures
