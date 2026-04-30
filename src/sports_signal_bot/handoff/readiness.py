import uuid
from typing import List, Dict, Any, Tuple
from .contracts import AdoptionReadinessStatus, AdoptionReadinessRecord, ActivationBlockerRecord

def compute_adoption_readiness(handoff_id: str, context: Dict[str, Any]) -> AdoptionReadinessRecord:
    blockers = []
    hints = []

    if context.get("has_unresolved_critical_blockers", False):
        blockers.append("Unresolved critical blockers present.")

    if not context.get("candidate_stable_across_channels", False):
        blockers.append("Candidate lacks stability across previous channels.")

    if not context.get("monitoring_expectations_defined", False):
        blockers.append("Post-activation monitoring expectations are not defined.")

    if context.get("release_family_frozen", False):
        blockers.append("Target release family is currently frozen.")

    if context.get("candidate_is_stale", False):
        blockers.append("Candidate package is stale.")

    if not blockers:
        status = AdoptionReadinessStatus.ACTIVATION_REVIEW_READY
        if context.get("scope", "broad") == "narrow":
            hints.append("Narrow scope candidate; fast activation recommended.")
        hints.append("All adoption readiness criteria met.")
    else:
        status = AdoptionReadinessStatus.BLOCKED_FOR_ACTIVATION
        hints.append(f"Activation blocked due to {len(blockers)} issues.")

    # Override if only bridge ready is intended
    if context.get("bridge_ready_only", False) and status != AdoptionReadinessStatus.BLOCKED_FOR_ACTIVATION:
        status = AdoptionReadinessStatus.BRIDGE_READY

    return AdoptionReadinessRecord(
        adoption_id=str(uuid.uuid4()),
        handoff_id=handoff_id,
        status=status,
        blockers=blockers,
        hints=hints
    )

def collect_activation_blockers(readiness_record: AdoptionReadinessRecord) -> List[ActivationBlockerRecord]:
    return [
        ActivationBlockerRecord(
            blocker_id=str(uuid.uuid4()),
            handoff_id=readiness_record.handoff_id,
            description=blocker
        )
        for blocker in readiness_record.blockers
    ]

def summarize_adoption_risks(readiness_record: AdoptionReadinessRecord) -> str:
    if readiness_record.status == AdoptionReadinessStatus.ACTIVATION_REVIEW_READY:
        return "Low risk for adoption. Readiness criteria met."
    elif readiness_record.status == AdoptionReadinessStatus.BRIDGE_READY:
        return "Candidate is bridge ready, but requires further activation constraints review."
    else:
        return f"High risk. Adoption blocked by {len(readiness_record.blockers)} issues."

def explain_activation_readiness(readiness_record: AdoptionReadinessRecord) -> str:
    explanation = f"Adoption Status: {readiness_record.status.value}\n"
    if readiness_record.blockers:
        explanation += "Blockers:\n" + "\n".join(f"- {b}" for b in readiness_record.blockers) + "\n"
    if readiness_record.hints:
        explanation += "Hints:\n" + "\n".join(f"- {h}" for h in readiness_record.hints)
    return explanation
