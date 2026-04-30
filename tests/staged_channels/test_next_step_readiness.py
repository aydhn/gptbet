from sports_signal_bot.staged_channels.contracts import StageStatus
from sports_signal_bot.staged_channels.progression import compute_next_step_readiness

def test_readiness():
    r1 = compute_next_step_readiness(StageStatus.SHADOW_VERIFIED, "c1")
    assert r1.readiness_level == "shadow_only_candidate"

    r2 = compute_next_step_readiness(StageStatus.ROLLOUT_READY_FOR_NEXT_PROMOTION_STEP, "c1")
    assert r2.readiness_level == "release_step_consideration_ready"
