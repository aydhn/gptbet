from sports_signal_bot.staged_channels.contracts import StageStatus
from sports_signal_bot.staged_channels.progression import simulate_rollout_stage

def test_eval_to_live():
    assert simulate_rollout_stage("c1", StageStatus.CANDIDATE_EVAL_VERIFIED) == StageStatus.PENDING_LIVE_LIKE_SAFE
