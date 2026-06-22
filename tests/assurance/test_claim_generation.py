import pytest
from sports_signal_bot.assurance.claims import create_claim
from sports_signal_bot.assurance.contracts import ClaimFamily, SupportStrength, ClaimInputRecord

def test_claim_generation():
    claim = create_claim(ClaimInputRecord(claim_id="clm_1", family=ClaimFamily.policy_conformance_claim, target_ref="target_1", statement="statement", strength=SupportStrength.high))
    assert claim.claim_id == "clm_1"
    assert claim.support_strength == SupportStrength.high
