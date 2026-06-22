import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional
from .contracts import (
    AutomationEnvelopeRecord,
    SelfHealingPreparationRecord,
    AutomationEnvelopeParams,
)


def build_automation_envelope(
    params: AutomationEnvelopeParams,
) -> AutomationEnvelopeRecord:
    return AutomationEnvelopeRecord(
        envelope_id=f"env_{uuid.uuid4().hex[:8]}",
        allowed_step_families=params.allowed_step_families,
        maximum_scope=params.maximum_scope,
        required_guards=params.required_guards,
        required_approvals_retained=params.required_approvals_retained,
        required_rehearsal_evidence=params.required_rehearsal_evidence,
        required_rollback_guarantees=params.required_rollback_guarantees,
        forbidden_incident_families=params.forbidden_incident_families,
        observability_minimums=params.observability_minimums,
        stop_conditions=params.stop_conditions,
        expiration=datetime.now(timezone.utc) + timedelta(days=30),
    )


def evaluate_self_healing_eligibility(
    session_ref: str,
    rollback_sufficient: bool,
    observability_sufficient: bool,
    rehearsal_success: bool,
    envelope_ref: Optional[str] = None,
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
        warnings=warnings,
    )
