from sports_signal_bot.staged_channels.contracts import StageStatus
from sports_signal_bot.staged_channels.progression import simulate_rollout_stage

def test_shadow_to_eval():
    assert simulate_rollout_stage("c1", StageStatus.SHADOW_VERIFIED) == StageStatus.PENDING_CANDIDATE_EVAL
