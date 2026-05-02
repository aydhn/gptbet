import pytest
from sports_signal_bot.assurance.contracts import MachineCheckableReleaseClaimRecord, GateOutcome, ClaimFamily

def test_release_claim():
    rec = MachineCheckableReleaseClaimRecord(
        release_claim_id="rc_1",
        promotion_target_ref="t1",
        claim_set_ref="cs_1",
        required_claim_families=[ClaimFamily.policy_conformance_claim],
        satisfied_claim_families=[ClaimFamily.policy_conformance_claim],
        blocking_missing_claims=[],
        claim_verification_status=GateOutcome.pass_
    )
    assert rec.claim_verification_status == GateOutcome.pass_
