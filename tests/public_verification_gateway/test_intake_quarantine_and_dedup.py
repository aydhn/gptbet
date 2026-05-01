from datetime import datetime
from src.sports_signal_bot.public_verification_gateway.intake import deduplicate_intake
from src.sports_signal_bot.public_verification_gateway.contracts import PublicChallengeIntakeRecord

def test_dedup():
    intake = PublicChallengeIntakeRecord(
        intake_id="i1", envelope_id="e1", status="received", trust_class="anonymous", received_at=datetime.utcnow()
    )
    payload = {"claim": "Duplicate claim text"}
    recent = [{"intake_id": "i0", "payload": {"claim": "Duplicate claim text"}}]

    res = deduplicate_intake(intake, payload, recent)
    assert res.duplicate_of == "i0"
