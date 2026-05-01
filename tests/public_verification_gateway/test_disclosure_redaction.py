from src.sports_signal_bot.public_verification_gateway.redaction import (
    build_publication_redaction_plan,
    redact_disclosure_payload,
    verify_disclosure_safe
)

def test_redaction():
    payload = {"safe": "value", "secret": "shh", "nested": {"operator_notes": "foo"}}
    forbidden = ["secret", "operator_notes"]
    rules = build_publication_redaction_plan("test_family", forbidden)

    redacted, decision = redact_disclosure_payload(payload, rules)
    assert redacted["safe"] == "value"
    assert redacted["secret"] == "[REDACTED]"
    assert redacted["nested"]["operator_notes"] == "[REDACTED]"

    is_safe = verify_disclosure_safe(redacted, forbidden, "bundle_123")
    assert is_safe
