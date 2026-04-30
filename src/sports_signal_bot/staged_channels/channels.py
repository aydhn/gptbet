from typing import Dict, Any, List
from sports_signal_bot.staged_channels.contracts import CandidateChannelRecord, ChannelFamily

def resolve_channel_evaluation_profile(channel_family: ChannelFamily) -> Dict[str, Any]:
    if channel_family == ChannelFamily.SHADOW_CANDIDATE:
        return {
            "level": "SHADOW",
            "comparison": "same-universe comparison",
            "active_effect": False,
            "cost": "low"
        }
    elif channel_family == ChannelFamily.CANDIDATE_EVAL:
        return {
            "level": "CANDIDATE_EVAL",
            "comparison": "stronger comparative evaluation",
            "active_effect": False,
            "cost": "medium",
            "checks": ["fleet conflict checks", "ops/review/monitoring burden summary"]
        }
    elif channel_family == ChannelFamily.LIVE_LIKE_SAFE:
        return {
            "level": "LIVE_LIKE_SAFE",
            "comparison": "stable-reference comparison mandatory",
            "active_effect": False,  # still a staged channel, no actual prod impact
            "cost": "high",
            "checks": ["stricter ops-mode assumptions", "release-readiness-like evidence expected"]
        }
    return {"level": "OTHER", "comparison": "none", "active_effect": False, "cost": "none"}

def validate_channel_readiness(record: CandidateChannelRecord) -> bool:
    if len(record.warnings) > 0:
        return False
    return True
