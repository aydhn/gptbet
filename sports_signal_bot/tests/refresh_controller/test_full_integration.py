import pytest
from sports_signal_bot.refresh_controller.runner import RefreshControllerRunner
from sports_signal_bot.refresh_controller.handlers import (
    catalog_refresh_handler,
    artifact_reresolve_handler,
    snapshot_reselection_handler,
    safe_fallback_handler
)
from sports_signal_bot.refresh_controller.states import RefreshActionFamily, ControllerState

def test_full_integration_runner_flow():
    runner = RefreshControllerRunner()
    runner.register_handler(RefreshActionFamily.CATALOG_REFRESH, catalog_refresh_handler)
    runner.register_handler(RefreshActionFamily.RERUN_ARTIFACT_RESOLUTION, artifact_reresolve_handler)
    runner.register_handler(RefreshActionFamily.SNAPSHOT_RESELECTION, snapshot_reselection_handler)
    runner.register_handler(RefreshActionFamily.ENABLE_SAFE_FALLBACK_MODE, safe_fallback_handler)

    # Run once
    manifest = runner.process_monitoring_output({"stale_artifact_count": 1})

    assert manifest.current_state == ControllerState.REFRESHED
    assert len(manifest.detected_problems) == 1
    assert manifest.chosen_plan is not None
    assert manifest.chosen_plan.risk_level == "low"
    assert manifest.attempt is not None
    assert manifest.attempt.status == "success"

    # Assert runner history tracked it
    assert len(runner.history.attempts) == 1
    assert len(runner.history.transitions) > 0
    assert len(runner.history.manifests) == 1
