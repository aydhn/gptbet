import pytest
from sports_signal_bot.refresh_controller.runner import RefreshControllerRunner
from sports_signal_bot.refresh_controller.states import RefreshActionFamily, ControllerState
from sports_signal_bot.refresh_controller.handlers import (
    catalog_refresh_handler,
    artifact_reresolve_handler,
    snapshot_reselection_handler,
    safe_fallback_handler
)

def setup_runner():
    runner = RefreshControllerRunner()
    runner.register_handler(RefreshActionFamily.CATALOG_REFRESH, catalog_refresh_handler)
    runner.register_handler(RefreshActionFamily.RERUN_ARTIFACT_RESOLUTION, artifact_reresolve_handler)
    runner.register_handler(RefreshActionFamily.SNAPSHOT_RESELECTION, snapshot_reselection_handler)
    runner.register_handler(RefreshActionFamily.ENABLE_SAFE_FALLBACK_MODE, safe_fallback_handler)
    return runner

def test_healthy_state():
    runner = setup_runner()
    monitor_output = {"global_health_score": 1.0, "stale_artifact_count": 0, "data_delay_seconds": 0}
    manifest = runner.process_monitoring_output(monitor_output)

    assert manifest.current_state == ControllerState.HEALTHY
    assert len(manifest.detected_problems) == 0

def test_artifact_freshness_auto_refresh():
    runner = setup_runner()
    monitor_output = {"stale_artifact_count": 2}
    manifest = runner.process_monitoring_output(monitor_output)

    assert len(manifest.detected_problems) == 1
    assert manifest.detected_problems[0].problem_class == "artifact_freshness"

    assert manifest.chosen_plan is not None
    assert manifest.chosen_plan.risk_level == "low"

    assert manifest.attempt is not None
    assert manifest.attempt.status == "success"
    assert manifest.attempt.validation_passed is True

    assert manifest.current_state == ControllerState.REFRESHED

def test_data_delay_snapshot_reselection():
    runner = setup_runner()
    monitor_output = {"data_delay_seconds": 4000}
    manifest = runner.process_monitoring_output(monitor_output)

    assert len(manifest.detected_problems) == 1
    assert manifest.detected_problems[0].problem_class == "data_freshness"

    assert manifest.chosen_plan is not None
    assert manifest.attempt.status == "success"
    assert manifest.current_state == ControllerState.REFRESHED

def test_dry_run_does_not_execute():
    runner = setup_runner()
    monitor_output = {"stale_artifact_count": 2}
    manifest = runner.process_monitoring_output(monitor_output, dry_run=True)

    assert manifest.attempt is None
    assert manifest.current_state == ControllerState.REFRESH_PENDING
