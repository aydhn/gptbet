from src.sports_signal_bot.capability_negotiation.profiles import build_capability_profile
from src.sports_signal_bot.capability_negotiation.negotiation import downgrade_to_safe_subset
from src.sports_signal_bot.capability_negotiation.replay import build_negotiation_replay_context, replay_capability_negotiation
from src.sports_signal_bot.capability_negotiation.contracts import ReplayOutcome

def test_replay():
    src = build_capability_profile("src", supported_artifact_families=["a", "b"])
    tgt = build_capability_profile("tgt", supported_artifact_families=["b", "c"])

    orig_profile = downgrade_to_safe_subset(src, tgt)

    ctx = build_negotiation_replay_context(orig_profile, src, tgt)
    assert replay_capability_negotiation(ctx) == ReplayOutcome.replay_matched

    new_tgt = build_capability_profile("tgt", supported_artifact_families=["c", "d"]) # Lost 'b'
    ctx2 = build_negotiation_replay_context(orig_profile, src, new_tgt)
    assert replay_capability_negotiation(ctx2) == ReplayOutcome.replay_changed_due_to_new_policy
