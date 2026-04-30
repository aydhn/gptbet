from typing import Dict, Any, List, Optional
import datetime
from .contracts import ActivationCouncilRecord, ActivationDecisionType, AdoptionBlockerRecord

def evaluate_activation_safety_lens(blockers: List[AdoptionBlockerRecord]) -> Dict[str, Any]:
    critical_blockers = [b for b in blockers if b.severity == "critical"]
    return {
        "lens": "safety",
        "passed": len(critical_blockers) == 0,
        "critical_blockers_count": len(critical_blockers)
    }

def evaluate_activation_evidence_lens(evidence_complete: bool) -> Dict[str, Any]:
    return {
        "lens": "evidence",
        "passed": evidence_complete
    }

def evaluate_adoption_scope_lens(scope: str, allowed_scopes: List[str]) -> Dict[str, Any]:
    return {
        "lens": "scope",
        "passed": scope in allowed_scopes
    }

def evaluate_rollback_lens(rollback_ready: bool) -> Dict[str, Any]:
    return {
        "lens": "rollback",
        "passed": rollback_ready
    }

def evaluate_verification_lens(verification_plan_complete: bool) -> Dict[str, Any]:
    return {
        "lens": "verification",
        "passed": verification_plan_complete
    }

def build_activation_council_packet(adoption_id: str,
                                    blockers: List[AdoptionBlockerRecord],
                                    evidence_complete: bool,
                                    scope: str,
                                    allowed_scopes: List[str],
                                    rollback_ready: bool,
                                    verification_plan_complete: bool) -> ActivationCouncilRecord:
    lenses = {
        "safety": evaluate_activation_safety_lens(blockers),
        "evidence": evaluate_activation_evidence_lens(evidence_complete),
        "scope": evaluate_adoption_scope_lens(scope, allowed_scopes),
        "rollback": evaluate_rollback_lens(rollback_ready),
        "verification": evaluate_verification_lens(verification_plan_complete)
    }

    recommendations = aggregate_activation_council_decision(lenses)

    return ActivationCouncilRecord(
        council_id=f"council_{datetime.datetime.now(datetime.timezone.utc).timestamp()}",
        adoption_id=adoption_id,
        lenses=lenses,
        recommendations=[recommendations.value]
    )

def aggregate_activation_council_decision(lenses: Dict[str, Dict[str, Any]]) -> ActivationDecisionType:
    if not lenses["safety"]["passed"]:
        return ActivationDecisionType.REJECT_ACTIVATION
    if not lenses["rollback"]["passed"]:
        return ActivationDecisionType.HOLD_ACTIVATION
    if not lenses["evidence"]["passed"]:
        return ActivationDecisionType.REQUIRE_MORE_EVIDENCE
    if not lenses["verification"]["passed"]:
        return ActivationDecisionType.HOLD_ACTIVATION
    if not lenses["scope"]["passed"]:
        return ActivationDecisionType.REQUIRE_NARROWER_SCOPE

    return ActivationDecisionType.APPROVE_ACTIVATION
