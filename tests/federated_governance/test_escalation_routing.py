from sports_signal_bot.federated_governance.escalation import detect_escalation_need, build_escalation_case, route_escalation, resolve_escalation_outcome
from sports_signal_bot.federated_governance.contracts import ControlPlaneRecord, PlanePrecedence, EscalationOutcome

def test_detect_escalation_need():
    assert detect_escalation_need(True, "critical") is True
    assert detect_escalation_need(True, "low") is False

def test_escalation_lifecycle():
    case = build_escalation_case("source_plane", "parent_plane", "Budget issue")
    assert case.status == "open"

    target_plane = ControlPlaneRecord(plane_id="target_plane", plane_name="Target", plane_family="global", precedence=PlanePrecedence.GLOBAL_GOVERNANCE)
    routed_case = route_escalation(case, target_plane)
    assert routed_case.target_plane_id == "target_plane"
    assert routed_case.status == "routed"

    outcome = resolve_escalation_outcome(routed_case.case_id, EscalationOutcome.ESCALATED_TO_GLOBAL_PLANE, "Requires global review")
    assert outcome.outcome == EscalationOutcome.ESCALATED_TO_GLOBAL_PLANE
