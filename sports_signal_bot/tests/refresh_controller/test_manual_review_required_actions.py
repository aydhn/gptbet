import pytest
from sports_signal_bot.refresh_controller.runner import RefreshControllerRunner
from sports_signal_bot.refresh_controller.states import RefreshActionFamily, ControllerState

def test_manual_review_required_for_high_risk():
    runner = RefreshControllerRunner()

    # We monkey-patch the decision engine to only return a high-risk candidate
    def mock_derive_candidates(problem):
        from sports_signal_bot.refresh_controller.contracts import RefreshAction
        from sports_signal_bot.refresh_controller.states import RefreshRiskLevel, RefreshActionFamily
        return [
            RefreshAction(
                family=RefreshActionFamily.RETRAIN_MODEL,
                risk_level=RefreshRiskLevel.HIGH,
                auto_execute_allowed=False,
                requires_manual_review=True,
                reversible=False
            )
        ]

    runner.engine.derive_refresh_candidates = mock_derive_candidates

    monitor_output = {"stale_artifact_count": 5}
    manifest = runner.process_monitoring_output(monitor_output)

    assert manifest.chosen_plan is not None
    assert manifest.chosen_plan.risk_level == "high"
    assert "requires manual review" in manifest.chosen_plan.blocked_reasons[0].lower()

    assert manifest.attempt is None # Should not execute
    assert manifest.current_state == ControllerState.MANUAL_REVIEW_REQUIRED
    assert manifest.freeze_record is not None # Should freeze
