from typing import List, Dict, Any, Optional
from sports_signal_bot.overlay_mesh_governance.contracts import (
    MultiTierRouteGovernanceRecord,
    RouteGovernanceTierRecord,
    RouteTierDecisionRecord,
    TierPrecedenceRecord,
    OverlayMeshHealthRecord
)

def build_route_governance_tiers(
    governance_id: str,
    tiers: List[RouteGovernanceTierRecord],
    precedence_rules: TierPrecedenceRecord
) -> MultiTierRouteGovernanceRecord:
    return MultiTierRouteGovernanceRecord(
        governance_id=governance_id,
        tier_refs=[t.tier_id for t in tiers],
        tier_precedence_rules=precedence_rules,
        supported_route_classes=[],
        bounded_scope_rules={},
        sovereignty_override_rules={},
        health_status=OverlayMeshHealthRecord(status="healthy", details={})
    )

def apply_tier_precedence(governance: MultiTierRouteGovernanceRecord, decisions: List[RouteTierDecisionRecord]) -> RouteTierDecisionRecord:
    # Basic precedence logic: order by the defined precedence rules
    # In reality this would fetch the tier ranks and compare.
    # We simulate picking the "highest" priority decision here.

    if not decisions:
        return RouteTierDecisionRecord(decision_id="none", route_ref="", tier_ref="", decision_type="no_safe_route", reasons=[])

    # block > downgrade > allow
    blocks = [d for d in decisions if d.decision_type.startswith("block")]
    if blocks:
        return blocks[0]

    downgrades = [d for d in decisions if d.decision_type.startswith("downgrade")]
    if downgrades:
        # A review_only downgrade might take precedence over caveated depending on rules
        review_only = [d for d in downgrades if d.decision_type == "downgrade_to_review_only"]
        if review_only:
            return review_only[0]
        return downgrades[0]

    return decisions[0]

def downgrade_route_by_tier(route_ref: str, tier_ref: str, downgrade_type: str, reason: str) -> RouteTierDecisionRecord:
    return RouteTierDecisionRecord(
        decision_id=f"dec_{route_ref}_{tier_ref}",
        route_ref=route_ref,
        tier_ref=tier_ref,
        decision_type=downgrade_type,
        reasons=[reason]
    )

def block_route_by_tier(route_ref: str, tier_ref: str, reason: str) -> RouteTierDecisionRecord:
    return RouteTierDecisionRecord(
        decision_id=f"dec_{route_ref}_{tier_ref}",
        route_ref=route_ref,
        tier_ref=tier_ref,
        decision_type="block_route_due_to_scope",
        reasons=[reason]
    )

def summarize_route_governance(governance: MultiTierRouteGovernanceRecord) -> Dict[str, Any]:
    return {
        "governance_id": governance.governance_id,
        "tier_count": len(governance.tier_refs),
        "health": governance.health_status.status
    }

def evaluate_route_under_tiers(route_ref: str, governance: MultiTierRouteGovernanceRecord) -> RouteTierDecisionRecord:
    # Mock evaluation for demonstration
    decisions = [
        RouteTierDecisionRecord(
            decision_id=f"dec_{route_ref}_allow",
            route_ref=route_ref,
            tier_ref="mock_tier",
            decision_type="allow_bounded_route",
            reasons=[]
        )
    ]
    return apply_tier_precedence(governance, decisions)

def collect_tier_blockers(decisions: List[RouteTierDecisionRecord]) -> List[RouteTierDecisionRecord]:
    return [d for d in decisions if d.decision_type.startswith("block")]

def explain_route_tier_decision(decision: RouteTierDecisionRecord) -> str:
    return f"Decision {decision.decision_type} for {decision.route_ref} due to: {', '.join(decision.reasons)}"

def summarize_tier_effects(decisions: List[RouteTierDecisionRecord]) -> Dict[str, int]:
    summary = {}
    for d in decisions:
        summary[d.decision_type] = summary.get(d.decision_type, 0) + 1
    return summary
