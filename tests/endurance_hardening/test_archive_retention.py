from sports_signal_bot.endurance_hardening.archive_retention import build_archive_retention_policy

def test_build_archive_retention_policy():
    res = build_archive_retention_policy("test_policy")
    assert res.retention_id == "policy_test_policy"
