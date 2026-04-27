import pytest
from sports_signal_bot.refresh_controller.runner import RefreshControllerRunner
from sports_signal_bot.refresh_controller.handlers import (
    catalog_refresh_handler,
    artifact_reresolve_handler,
    snapshot_reselection_handler,
    safe_fallback_handler
)
from sports_signal_bot.refresh_controller.states import RefreshActionFamily, ControllerState

def setup_runner():
    runner = RefreshControllerRunner()
    runner.register_handler(RefreshActionFamily.CATALOG_REFRESH, catalog_refresh_handler)
    runner.register_handler(RefreshActionFamily.RERUN_ARTIFACT_RESOLUTION, artifact_reresolve_handler)
    runner.register_handler(RefreshActionFamily.SNAPSHOT_RESELECTION, snapshot_reselection_handler)
    runner.register_handler(RefreshActionFamily.ENABLE_SAFE_FALLBACK_MODE, safe_fallback_handler)
    return runner

def test_safe_fallback_handler_is_low_risk():
    runner = setup_runner()
    # Mocking low health which triggers safe fallback according to decisions.py
    monitor_output = {"global_health_score": 0.5, "stale_artifact_count": 0, "data_delay_seconds": 0}
    manifest = runner.process_monitoring_output(monitor_output)

    assert len(manifest.detected_problems) == 1
    assert manifest.chosen_plan is not None
    assert manifest.chosen_plan.risk_level == "low"
    assert manifest.attempt is not None
    assert manifest.attempt.status == "success"
    assert manifest.current_state == ControllerState.REFRESHED
