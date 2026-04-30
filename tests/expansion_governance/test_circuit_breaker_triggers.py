import pytest
from sports_signal_bot.expansion_governance.breakers import evaluate_circuit_breakers
from sports_signal_bot.expansion_governance.contracts import ExpansionControlStateRecord

def test_circuit_breaker_triggers_and_actions():
    state = ExpansionControlStateRecord(control_state_id="test")
    metrics = {
        "critical_verification_failures": 4,
        "global_budget_usage_pct": 0.96
    }

    evaluation = evaluate_circuit_breakers(state, metrics)

    assert len(evaluation.triggers_fired) == 2
    action_types = [a.action_type for a in evaluation.actions_proposed]
    assert "global_pause" in action_types
    assert "shrink_multiple_cohorts" in action_types
    assert any(a.manual_ack_required for a in evaluation.actions_proposed)
