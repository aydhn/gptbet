import pytest
from sports_signal_bot.refresh_controller.runner import RefreshControllerRunner
from sports_signal_bot.refresh_controller.states import RefreshActionFamily
from sports_signal_bot.refresh_controller.handlers import catalog_refresh_handler

def test_refresh_history_tracking():
    runner = RefreshControllerRunner()
    runner.register_handler(RefreshActionFamily.CATALOG_REFRESH, catalog_refresh_handler)
    runner.register_handler(RefreshActionFamily.RERUN_ARTIFACT_RESOLUTION, catalog_refresh_handler)

    # Run once
    runner.process_monitoring_output({"stale_artifact_count": 1})

    assert len(runner.history.attempts) == 1
    assert runner.history.get_last_successful_attempt() is not None
    assert runner.history.get_consecutive_failures() == 0
    assert len(runner.history.transitions) > 0
    assert len(runner.history.manifests) == 1

def test_history_failure_counting():
    runner = RefreshControllerRunner()
    # Missing handler for CATALOG_REFRESH will cause failure

    runner.process_monitoring_output({"stale_artifact_count": 1})
    assert len(runner.history.attempts) == 1
    assert runner.history.get_consecutive_failures() == 1

    runner.process_monitoring_output({"stale_artifact_count": 1})
    assert len(runner.history.attempts) == 2
    assert runner.history.get_consecutive_failures() == 2
