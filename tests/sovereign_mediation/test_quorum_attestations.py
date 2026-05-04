from sports_signal_bot.sovereign_mediation.quorum_attestations import build_governance_quorum_attestation, validate_quorum_attestation

def test_build_governance_quorum_attestation():
    attestation = build_governance_quorum_attestation(
        council_case_ref="cc_1",
        council_ref="c_1",
        decision_type="bounded_approval",
        evidence_refs=["ev_1"],
        caveat_refs=[]
    )
    assert attestation.attestation_status == "attested_verified"
    assert validate_quorum_attestation(attestation) is True

def test_build_governance_quorum_attestation_with_caveats():
    attestation = build_governance_quorum_attestation(
        council_case_ref="cc_1",
        council_ref="c_1",
        decision_type="bounded_approval",
        evidence_refs=["ev_1"],
        caveat_refs=["cav_1"]
    )
    assert attestation.attestation_status == "attested_with_caveats"
