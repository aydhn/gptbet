from sports_signal_bot.staged_channels.contracts import StageStatus, RolloutStageRecord
from sports_signal_bot.staged_channels.evidences import build_rollout_evidence_packet
import datetime

def test_evidence_packet():
    record = RolloutStageRecord(
        stage_id="s1", candidate_release_id="c1", current_channel="shadow",
        stage_status=StageStatus.SHADOW_VERIFIED, entered_at=datetime.datetime.now(datetime.timezone.utc)
    )
    packet = build_rollout_evidence_packet("c1", record, {"metric_a": 10})
    assert packet["candidate_id"] == "c1"
    assert packet["stage"] == StageStatus.SHADOW_VERIFIED.value
    assert packet["metrics"]["metric_a"] == 10
