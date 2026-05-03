from sports_signal_bot.resilience_advisor.orchestration import build_recovery_orchestration_plan
from sports_signal_bot.resilience_advisor.guards import aggregate_recovery_guards
from sports_signal_bot.resilience_advisor.contracts import RemediationPlaybookRecord

def test_guards():
    playbook = RemediationPlaybookRecord(
        playbook_id="pb1", playbook_family="test", target_incident_family="test",
        synthesized_from_pattern_refs=[], steps=[], prerequisites=[],
        risk_notes=[], rollback_notes=[], expected_signals=[]
    )
    plan = build_recovery_orchestration_plan(playbook, "inc1")
    guards = aggregate_recovery_guards(plan)
    assert len(guards) == 3
    # Check scope guard passes since bounded_scope=True by default in build_recovery_orchestration_plan
    assert any(g.guard_family == "scope_guard" and g.outcome == "guard_pass" for g in guards)
