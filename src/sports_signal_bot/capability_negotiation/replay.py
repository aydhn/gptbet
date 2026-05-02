from typing import Dict, Any
from src.sports_signal_bot.capability_negotiation.contracts import (
    NegotiatedProfileRecord,
    CapabilityProfileRecord,
    ReplayOutcome
)
from src.sports_signal_bot.capability_negotiation.compatibility import diff_capability_profiles
from src.sports_signal_bot.capability_negotiation.negotiation import downgrade_to_safe_subset

def build_negotiation_replay_context(
    original_profile: NegotiatedProfileRecord,
    current_source: CapabilityProfileRecord,
    current_target: CapabilityProfileRecord
) -> Dict[str, Any]:
    return {
        "original_profile": original_profile,
        "current_source": current_source,
        "current_target": current_target
    }

def replay_capability_negotiation(context: Dict[str, Any]) -> ReplayOutcome:
    orig = context.get("original_profile")
    if not orig:
        return ReplayOutcome.replay_invalid_missing_context

    src = context.get("current_source")
    tgt = context.get("current_target")

    # Simulate a drift check by comparing a newly negotiated subset to the original scope
    new_profile = downgrade_to_safe_subset(src, tgt)

    if new_profile.scope.allowed_artifact_families != orig.scope.allowed_artifact_families:
         return ReplayOutcome.replay_changed_due_to_new_policy

    return ReplayOutcome.replay_matched
