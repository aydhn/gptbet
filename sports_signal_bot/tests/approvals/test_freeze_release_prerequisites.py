from sports_signal_bot.approvals.freeze_release import FreezeReleaseManager

def test_freeze_release_validation():
    # Should be valid
    assert FreezeReleaseManager.validate_prerequisites(active_critical_anomalies=0, post_refresh_passed=True) is True

    # Should fail if anomalies exist
    assert FreezeReleaseManager.validate_prerequisites(active_critical_anomalies=1, post_refresh_passed=True) is False

    # Should fail if post refresh didn't pass
    assert FreezeReleaseManager.validate_prerequisites(active_critical_anomalies=0, post_refresh_passed=False) is False
