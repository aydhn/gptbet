import pytest
from sports_signal_bot.assurance.gates import evaluate_assurance_gate
from sports_signal_bot.assurance.contracts import PromotionEnvelopeRecord, EnvelopeStatus

def test_assurance_gate():
    env = PromotionEnvelopeRecord(
        envelope_id="env_1",
        target_ref="t1",
        required_claims_summary={},
        satisfied_claims=[],
        blocked_claims=[],
        proof_carrying_bundle_ref="p1",
        assurance_attestations=[],
        trust_signature_status="ok",
        drift_cleanliness="ok",
        conformance_summary="ok",
        final_assurance_decision=EnvelopeStatus.assurance_ready
    )
    assert evaluate_assurance_gate(env).value == "pass"
