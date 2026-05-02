import pytest
from sports_signal_bot.assurance.claims import create_claim
from sports_signal_bot.assurance.contracts import ClaimFamily, SupportStrength

def test_claim_generation():
    claim = create_claim("clm_1", ClaimFamily.policy_conformance_claim, "target_1", "statement", SupportStrength.high)
    assert claim.claim_id == "clm_1"
    assert claim.support_strength == SupportStrength.high
