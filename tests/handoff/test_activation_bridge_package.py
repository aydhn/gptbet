from sports_signal_bot.handoff.bridge import build_activation_bridge, validate_bridge_prerequisites
from sports_signal_bot.handoff.contracts import CouncilDecisionType

def test_build_activation_bridge():
    context = {"scope": "broad", "monitoring_expectations_defined": False, "decision_type": CouncilDecisionType.APPROVE_HANDOFF}
    bridge = build_activation_bridge("h1", ["c1"], "d1", context)
    assert len(bridge.activation_constraints) == 2
    assert validate_bridge_prerequisites(bridge)

def test_build_activation_bridge_not_approved():
    context = {"scope": "narrow", "monitoring_expectations_defined": True, "decision_type": CouncilDecisionType.HOLD_FOR_MORE_EVIDENCE}
    bridge = build_activation_bridge("h1", ["c1"], "d1", context)
    assert len(bridge.do_not_activate_reasons) == 1
    assert not validate_bridge_prerequisites(bridge)
