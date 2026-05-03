from typing import List, Dict, Any
from datetime import datetime, timezone
from sports_signal_bot.multi_region_fabric.contracts import CrossClusterRecoveryTreatyRecord, TreatyDecisionRecord

TREATY_FAMILIES = [
    "advisory_only_treaty",
    "review_delegation_treaty",
    "bounded_runtime_treaty",
    "rollback_visibility_treaty",
    "failover_assistance_treaty",
    "closure_observer_treaty",
    "token_translation_forbidden_treaty",
    "replay_required_transfer_treaty"
]

TREATY_OUTCOMES = [
    "allow_review_delegation",
    "allow_observer_visibility",
    "allow_bounded_transfer_preparation",
    "allow_failover_assistance",
    "allow_rollback_visibility",
    "deny_token_portability",
    "deny_live_runtime_transfer",
    "review_required_before_transfer",
    "treaty_expired_block",
    "sovereignty_override_block"
]

def build_recovery_treaty(t_id: str, family: str, parties: List[str], expiry: datetime) -> CrossClusterRecoveryTreatyRecord:
    return CrossClusterRecoveryTreatyRecord(
        treaty_id=t_id,
        treaty_family=family,
        treaty_parties=parties,
        allowed_lane_families=["*"],
        forbidden_lane_families=[],
        delegation_rules={},
        token_acceptance_rules={},
        replay_requirements={},
        rollback_visibility_rules={},
        expiry=expiry
    )

def verify_treaty_integrity(treaty: CrossClusterRecoveryTreatyRecord) -> bool:
    return datetime.now(timezone.utc) < treaty.expiry

def evaluate_treaty_applicability(treaty: CrossClusterRecoveryTreatyRecord, lane: str) -> bool:
    return True

def summarize_treaty_scope(treaty: CrossClusterRecoveryTreatyRecord) -> str:
    return f"Treaty {treaty.treaty_id} for {len(treaty.treaty_parties)} parties."

def resolve_treaty_decision(treaty_id: str, action: str) -> TreatyDecisionRecord:
    return TreatyDecisionRecord(
        decision_id=f"td_{treaty_id}",
        treaty_id=treaty_id,
        outcome="allow_bounded_transfer_preparation" if action == "transfer" else "allow_review_delegation",
        reasoning="Treaty permits action"
    )

def map_treaty_rules_to_runtime(treaty_id: str) -> Dict[str, Any]:
    return {"allowed": True}

def block_unsupported_treaty_path(treaty_id: str) -> bool:
    return False

def explain_treaty_decision(decision: TreatyDecisionRecord) -> str:
    return f"Treaty decision: {decision.outcome} due to {decision.reasoning}"
