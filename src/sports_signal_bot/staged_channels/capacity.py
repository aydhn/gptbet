from typing import Dict, List, Any
from sports_signal_bot.staged_channels.contracts import CandidateChannelRecord

def compute_channel_capacity(channel: CandidateChannelRecord) -> int:
    # simple mock logic
    return channel.capacity_limits.get("max_active", 10) - len(channel.active_assignments)

def admit_candidate_to_channel(candidate_id: str, channel: CandidateChannelRecord) -> bool:
    if compute_channel_capacity(channel) > 0:
        channel.active_assignments.append(candidate_id)
        return True
    return False

def explain_capacity_decision(candidate_id: str, channel: CandidateChannelRecord, admitted: bool) -> str:
    if admitted:
        return f"Candidate {candidate_id} admitted to {channel.channel_name}."
    return f"Candidate {candidate_id} deferred from {channel.channel_name} due to capacity."
