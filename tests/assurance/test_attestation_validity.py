import pytest
from sports_signal_bot.assurance.attestations import build_assurance_attestation
from sports_signal_bot.assurance.contracts import AttestationIssuerFamily, AttestationStatus

def test_attestation_validity():
    att = build_assurance_attestation(AttestationIssuerFamily.conformance_runner_attester, "t1", ["c1"])
    assert att.attestation_status == AttestationStatus.valid
