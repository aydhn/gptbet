from src.sports_signal_bot.capability_negotiation.profiles import build_capability_profile
from src.sports_signal_bot.capability_negotiation.compatibility import compute_capability_drift, classify_capability_drift
from src.sports_signal_bot.capability_negotiation.contracts import DriftOutcome

def test_capability_drift():
    old = build_capability_profile("reg", supported_artifact_families=["a", "b"])
    new = build_capability_profile("reg", supported_artifact_families=["b", "c"])

    diff = compute_capability_drift(old, new)
    outcome = classify_capability_drift(diff)

    assert outcome == DriftOutcome.review_required_drift
