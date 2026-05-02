from sports_signal_bot.ecosystem_discovery.protocols import (
    build_verifier_protocol_profile,
    negotiate_protocol_profile,
    restrict_protocol_to_safe_subset
)

def test_negotiation():
    p1 = build_verifier_protocol_profile("offered")
    p1.supported_request_families = ["base", "ext1"]

    p2 = build_verifier_protocol_profile("required")
    p2.supported_request_families = ["base", "ext2"]

    neg = negotiate_protocol_profile(p1, p2)
    assert "base" in neg.supported_request_families
    assert "ext1" not in neg.supported_request_families
    assert "ext2" not in neg.supported_request_families

def test_restriction():
    p1 = build_verifier_protocol_profile("test")
    p1.supported_request_families = ["base", "unsafe_extension"]

    safe = restrict_protocol_to_safe_subset(p1)
    assert "unsafe_extension" not in safe.supported_request_families
