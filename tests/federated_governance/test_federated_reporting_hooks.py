from sports_signal_bot.federated_governance.reporting import extract_federated_kpis, generate_federated_governance_summary
from sports_signal_bot.federated_governance.contracts import ControlPlaneRecord, PlanePrecedence, DelegatedActionRecord, EscalationCaseRecord

def test_extract_federated_kpis():
    p1 = ControlPlaneRecord(plane_id="p1", plane_name="Global", plane_family="global", precedence=PlanePrecedence.GLOBAL_GOVERNANCE)

    actions = [DelegatedActionRecord(action_id="a1", plane_id="p1", delegation_id="d1", payload={}, status="done")]
    escalations = [EscalationCaseRecord(case_id="e1", source_plane_id="p1", target_plane_id="p1", reason="issue")]

    kpis = extract_federated_kpis([p1], actions, escalations, [], [], [])

    assert kpis["delegated_action_rate"] == 1.0
    assert kpis["escalation_rate"] == 1.0

def test_generate_federated_governance_summary():
    p1 = ControlPlaneRecord(plane_id="p1", plane_name="Global", plane_family="global", precedence=PlanePrecedence.GLOBAL_GOVERNANCE)

    summary = generate_federated_governance_summary([p1], [], [], [], [], [])
    assert summary["active_plane_count"] == 1
