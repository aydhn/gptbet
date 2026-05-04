from sports_signal_bot.capability_negotiation.profiles import build_capability_profile
from sports_signal_bot.capability_negotiation.negotiation import downgrade_to_safe_subset, enforce_interop_safety

def test_interop_safety():
    src = build_capability_profile("src", supported_artifact_families=["a"])
    tgt = build_capability_profile("tgt", supported_artifact_families=["b"])

    # Gap in artifact families
    negotiated = downgrade_to_safe_subset(src, tgt)
    assert enforce_interop_safety(negotiated) is False
