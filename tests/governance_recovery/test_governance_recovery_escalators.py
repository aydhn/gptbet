from sports_signal_bot.governance_recovery.escalators import (
    build_governance_recovery_escalator,
    advance_recovery_escalator
)
from sports_signal_bot.governance_recovery.contracts import EscalationStage

def test_build_governance_recovery_escalator():
    escalator = build_governance_recovery_escalator("esc_1", "quorum_health_recovery_escalator")
    assert escalator.escalator_id == "esc_1"
    assert escalator.current_state == EscalationStage.MONITORING

def test_advance_recovery_escalator():
    escalator = build_governance_recovery_escalator("esc_1", "quorum_health_recovery_escalator")
    escalator = advance_recovery_escalator(escalator, EscalationStage.REVIEW_BIAS)
    assert escalator.current_state == EscalationStage.REVIEW_BIAS
