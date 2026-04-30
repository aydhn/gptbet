from sports_signal_bot.cohort_autopilot.manifests import create_autopilot_manifest

def test_manifest_creation():
    manifest = create_autopilot_manifest(5, [])
    assert manifest.active_cohorts == 5
    assert len(manifest.decisions_made) == 0
