from sports_signal_bot.staged_channels.contracts import ChannelFamily, CandidateChannelRecord
from sports_signal_bot.staged_channels.channels import resolve_channel_evaluation_profile, validate_channel_readiness

def test_resolve_channel_evaluation_profile():
    profile = resolve_channel_evaluation_profile(ChannelFamily.SHADOW_CANDIDATE)
    assert profile["level"] == "SHADOW"
    assert profile["active_effect"] is False

    profile_live = resolve_channel_evaluation_profile(ChannelFamily.LIVE_LIKE_SAFE)
    assert profile_live["level"] == "LIVE_LIKE_SAFE"
    assert profile_live["active_effect"] is False

def test_validate_channel_readiness():
    record = CandidateChannelRecord(
        channel_id="c1",
        channel_name="Shadow 1",
        channel_family=ChannelFamily.SHADOW_CANDIDATE,
        safety_level="high",
        comparison_mode="side_by_side",
        progression_policy="conservative"
    )
    assert validate_channel_readiness(record) is True

    record.warnings.append("High load")
    assert validate_channel_readiness(record) is False
