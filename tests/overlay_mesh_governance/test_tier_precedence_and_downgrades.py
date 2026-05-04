import pytest
from sports_signal_bot.overlay_mesh_governance import (
    build_route_governance_tiers,
    apply_tier_precedence,
    RouteTierDecisionRecord,
    TierPrecedenceRecord
)

def test_tier_precedence():
    prec = TierPrecedenceRecord(precedence_rule_id="r1", precedence_order=["t1"])
    gov = build_route_governance_tiers("g1", [], prec)
    decisions = [
        RouteTierDecisionRecord(decision_id="d1", route_ref="r1", tier_ref="t1", decision_type="allow_bounded_route", reasons=[]),
        RouteTierDecisionRecord(decision_id="d2", route_ref="r1", tier_ref="t2", decision_type="block_route_due_to_scope", reasons=[])
    ]
    res = apply_tier_precedence(gov, decisions)
    # block should take precedence over allow
    assert res.decision_type == "block_route_due_to_scope"

def test_tier_precedence_downgrade():
    prec = TierPrecedenceRecord(precedence_rule_id="r1", precedence_order=["t1"])
    gov = build_route_governance_tiers("g1", [], prec)
    decisions = [
        RouteTierDecisionRecord(decision_id="d1", route_ref="r1", tier_ref="t1", decision_type="allow_bounded_route", reasons=[]),
        RouteTierDecisionRecord(decision_id="d2", route_ref="r1", tier_ref="t2", decision_type="downgrade_to_review_only", reasons=[])
    ]
    res = apply_tier_precedence(gov, decisions)
    # downgrade should take precedence over allow
    assert res.decision_type == "downgrade_to_review_only"
