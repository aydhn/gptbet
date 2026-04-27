import pytest
from sports_signal_bot.refresh_controller.decisions import RefreshDecisionEngine
from sports_signal_bot.refresh_controller.contracts import RefreshAction
from sports_signal_bot.refresh_controller.states import RefreshRiskLevel, RefreshActionFamily

def test_risk_classification():
    engine = RefreshDecisionEngine()

    action_low = RefreshAction(
        family=RefreshActionFamily.CATALOG_REFRESH,
        risk_level=RefreshRiskLevel.LOW,
        auto_execute_allowed=True,
        requires_manual_review=False,
        reversible=True
    )

    action_high = RefreshAction(
        family=RefreshActionFamily.RETRAIN_MODEL,
        risk_level=RefreshRiskLevel.HIGH,
        auto_execute_allowed=False,
        requires_manual_review=True,
        reversible=False
    )

    assert engine.score_refresh_action_risk(action_low) == RefreshRiskLevel.LOW
    assert engine.score_refresh_action_risk(action_high) == RefreshRiskLevel.HIGH
