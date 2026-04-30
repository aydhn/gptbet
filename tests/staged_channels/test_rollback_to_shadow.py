from sports_signal_bot.staged_channels.stages import rollback_candidate_to_shadow
from sports_signal_bot.staged_channels.contracts import StageStatus

def test_rollback_candidate():
    record = rollback_candidate_to_shadow("cand_1")
    assert record.stage_status == StageStatus.ROLLBACK_TO_SHADOW
    assert record.candidate_release_id == "cand_1"
    assert record.current_channel == "shadow_candidate_channel"
