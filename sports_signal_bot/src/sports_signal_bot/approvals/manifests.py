from datetime import datetime, timezone
import uuid
from typing import List
from sports_signal_bot.approvals.contracts import ApprovalWorkflowManifest

def build_workflow_manifest(
    open_review_items: int,
    approved_count: int,
    rejected_count: int,
    deferred_count: int,
    active_override_count: int,
    unresolved_critical_ack_count: int
) -> ApprovalWorkflowManifest:
    """Build a summary manifest of the workflow state."""
    return ApprovalWorkflowManifest(
        manifest_id=f"wf_{uuid.uuid4().hex[:8]}",
        open_review_items=open_review_items,
        approved_count=approved_count,
        rejected_count=rejected_count,
        deferred_count=deferred_count,
        active_override_count=active_override_count,
        unresolved_critical_ack_count=unresolved_critical_ack_count
    )
