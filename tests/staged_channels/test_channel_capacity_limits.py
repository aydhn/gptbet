from sports_signal_bot.staged_channels.contracts import CandidateChannelRecord, ChannelFamily
from sports_signal_bot.staged_channels.capacity import compute_channel_capacity, admit_candidate_to_channel

def test_capacity_limits():
    channel = CandidateChannelRecord(
        channel_id="c1", channel_name="Test", channel_family=ChannelFamily.SHADOW_CANDIDATE,
        safety_level="high", comparison_mode="none", progression_policy="none",
        capacity_limits={"max_active": 2}, active_assignments=["c1"]
    )
    assert compute_channel_capacity(channel) == 1
    assert admit_candidate_to_channel("c2", channel) is True
    assert compute_channel_capacity(channel) == 0
    assert admit_candidate_to_channel("c3", channel) is False
