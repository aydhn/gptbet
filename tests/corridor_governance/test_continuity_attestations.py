import pytest
from datetime import datetime
from sports_signal_bot.corridor_governance.contracts import ContinuityAttestationRecord
from sports_signal_bot.corridor_governance.attestations import classify_attestation_strength
from sports_signal_bot.corridor_governance.validity import verify_attestation_validity_window

def test_classify_attestation_strength():
    strong_att = ContinuityAttestationRecord(
        continuity_attestation_id="att-1", continuity_session_ref="sess", corridor_ref="c1",
        treaty_ref="t1", source_region_ref="s1", target_region_ref="t2",
        attestation_family="fam", attested_dimensions=["d1"],
        attestation_status="attested_verified", validity_window={}, caveat_refs=[], evidence_refs=[], warnings=[]
    )
    assert classify_attestation_strength(strong_att) == "strong"

    caveated_att = ContinuityAttestationRecord(
        continuity_attestation_id="att-2", continuity_session_ref="sess", corridor_ref="c1",
        treaty_ref="t1", source_region_ref="s1", target_region_ref="t2",
        attestation_family="fam", attested_dimensions=["d1"],
        attestation_status="attested_with_caveats", validity_window={}, caveat_refs=["cav-1"], evidence_refs=[], warnings=[]
    )
    assert classify_attestation_strength(caveated_att) == "workable"

def test_attestation_validity_window():
    att = ContinuityAttestationRecord(
        continuity_attestation_id="att-1", continuity_session_ref="sess", corridor_ref="c1",
        treaty_ref="t1", source_region_ref="s1", target_region_ref="t2",
        attestation_family="fam", attested_dimensions=["d1"],
        attestation_status="attested_verified",
        validity_window={"effective_until": "2050-01-01T00:00:00"},
        caveat_refs=[], evidence_refs=[], warnings=[]
    )
    # Testing with a time way before expiry
    validity = verify_attestation_validity_window(att, datetime(2030, 1, 1))
    assert validity.is_valid == True

    # Testing with a time after expiry
    validity2 = verify_attestation_validity_window(att, datetime(2060, 1, 1))
    assert validity2.is_valid == False
    assert validity2.reason == "Attestation expired"
