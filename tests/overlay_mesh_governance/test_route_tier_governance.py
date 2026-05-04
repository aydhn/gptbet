import pytest
from sports_signal_bot.overlay_mesh_governance import (
    build_route_governance_tiers,
    evaluate_route_under_tiers,
    RouteGovernanceTierRecord,
    TierPrecedenceRecord,
    TierDowngradeRecord,
    TierBlockingReasonRecord
)

def test_evaluate_route():
    tier1 = RouteGovernanceTierRecord(
        tier_id="t1", tier_family="local_scope_tier", tier_scope="local",
        policy_ref="p1", precedence_rank=1, downgrade_rules=[], block_rules=[],
        visibility_profile="open"
    )
    prec = TierPrecedenceRecord(precedence_rule_id="r1", precedence_order=["local_scope_tier"])
    gov = build_route_governance_tiers("g1", [tier1], prec)
    dec = evaluate_route_under_tiers("route_1", gov)
    assert dec.route_ref == "route_1"
    assert "allow_bounded_route" in dec.decision_type
