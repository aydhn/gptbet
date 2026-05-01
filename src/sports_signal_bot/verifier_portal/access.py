from typing import Dict, Any, List
import uuid
from .contracts import PortalAccessDecisionRecord, PortalAudienceProfileRecord
from .profiles import get_profile

def evaluate_portal_access(profile_id: str, resource_type: str, resource_id: str) -> PortalAccessDecisionRecord:
    profile = get_profile(profile_id)

    # Mock logic based on profile capabilities
    decision = "denied"
    reason = "Resource not allowed for profile"

    if resource_type == "view" and resource_id in profile.visible_view_families:
        decision = "allowed"
        reason = "View explicitly allowed"
    elif resource_type == "challenge_submission" and profile.challenge_submission_rights:
        decision = "allowed"
        reason = "Challenge submission rights granted"
    elif resource_type == "feed" and profile.feed_access_level in ["all", "premium", "standard", "public"]:
        # Basic feed access check
        decision = "allowed"
        reason = f"Feed access level '{profile.feed_access_level}' allows basic access"

    return PortalAccessDecisionRecord(
        decision_id=str(uuid.uuid4()),
        profile=profile_id,
        resource_type=resource_type,
        resource_id=resource_id,
        decision=decision,
        reason=reason
    )

def enforce_profile_scope(decision: PortalAccessDecisionRecord) -> bool:
    return decision.decision == "allowed"

def deny_unsafe_access(decision: PortalAccessDecisionRecord) -> PortalAccessDecisionRecord:
    if decision.decision == "allowed" and "unsafe" in decision.resource_id:
        decision.decision = "denied"
        decision.reason = "Unsafe resource access blocked"
    return decision

def summarize_access_decision(decision: PortalAccessDecisionRecord) -> Dict[str, Any]:
    return decision.dict()
