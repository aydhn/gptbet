import datetime
from sports_signal_bot.staged_channels.contracts import StageStatus, RolloutStageRecord
from sports_signal_bot.staged_channels.progression import simulate_rollout_stage, compute_next_step_readiness

def test_stage_progression():
    stage = StageStatus.CANDIDATE_QUEUED_FOR_SHADOW
    next_stage = simulate_rollout_stage("cand_1", stage)
    assert next_stage == StageStatus.RUNNING_IN_SHADOW

def test_next_step_readiness():
    readiness = compute_next_step_readiness(StageStatus.SHADOW_VERIFIED, "cand_1")
    assert readiness.readiness_level == "shadow_only_candidate"
