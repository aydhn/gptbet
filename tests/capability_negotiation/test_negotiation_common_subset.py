from src.sports_signal_bot.capability_negotiation.profiles import build_capability_profile
from src.sports_signal_bot.capability_negotiation.negotiation import downgrade_to_safe_subset

def test_downgrade_to_safe_subset():
    src = build_capability_profile("src", supported_artifact_families=["a", "b"])
    tgt = build_capability_profile("tgt", supported_artifact_families=["b", "c"])

    negotiated = downgrade_to_safe_subset(src, tgt)
    assert negotiated.scope.allowed_artifact_families == ["b"]
