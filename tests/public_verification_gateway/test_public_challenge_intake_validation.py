from src.sports_signal_bot.public_verification_gateway.intake import validate_public_challenge_intake
from src.sports_signal_bot.public_verification_gateway.contracts import PublicChallengeEnvelopeRecord, ChallengeIntakeSchemaRecord

def test_intake_validation():
    schema = ChallengeIntakeSchemaRecord(schema_id="s1", version="1", required_fields=["claim", "severity"])
    envelope = PublicChallengeEnvelopeRecord(envelope_id="e1", payload={"claim": "bad stuff", "severity": "high"})

    valid, errors = validate_public_challenge_intake(envelope, schema)
    assert valid
    assert len(errors) == 0

    bad_envelope = PublicChallengeEnvelopeRecord(envelope_id="e2", payload={"claim": "bad stuff"})
    valid, errors = validate_public_challenge_intake(bad_envelope, schema)
    assert not valid
    assert len(errors) == 1
