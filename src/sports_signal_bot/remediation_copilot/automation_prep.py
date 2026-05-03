import uuid
from datetime import datetime, timedelta
from typing import List, Optional
from .contracts import AutomationEnvelopeRecord, SelfHealingPreparationRecord

def build_automation_envelope(
    allowed_step_families: List[str],
    maximum_scope: str,
    required_guards: List[str],
    required_approvals_retained: List[str],
    required_rehearsal_evidence: List[str],
    required_rollback_guarantees: List[str],
    forbidden_incident_families: List[str],
    observability_minimums: List[str],
    stop_conditions: List[str]
) -> AutomationEnvelopeRecord:
    return AutomationEnvelopeRecord(
        envelope_id=f"env_{uuid.uuid4().hex[:8]}",
        allowed_step_families=allowed_step_families,
        maximum_scope=maximum_scope,
        required_guards=required_guards,
        required_approvals_retained=required_approvals_retained,
        required_rehearsal_evidence=required_rehearsal_evidence,
        required_rollback_guarantees=required_rollback_guarantees,
        forbidden_incident_families=forbidden_incident_families,
        observability_minimums=observability_minimums,
        stop_conditions=stop_conditions,
        expiration=datetime.utcnow() + timedelta(days=30)
    )

def evaluate_self_healing_eligibility(
    session_ref: str,
    rollback_sufficient: bool,
    observability_sufficient: bool,
    rehearsal_success: bool,
    envelope_ref: Optional[str] = None
) -> SelfHealingPreparationRecord:

    if not rollback_sufficient or not observability_sufficient:
        status = "blocked_for_automation"
        warnings = ["Missing rollback or observability sufficiency"]
    elif not rehearsal_success:
        status = "candidate_with_review"
        warnings = ["Requires rehearsal evidence"]
    else:
        status = "bounded_candidate"
        warnings = []

    return SelfHealingPreparationRecord(
        preparation_id=f"prep_{uuid.uuid4().hex[:8]}",
        session_ref=session_ref,
        eligibility_status=status,
        envelope_ref=envelope_ref,
        warnings=warnings
    )
