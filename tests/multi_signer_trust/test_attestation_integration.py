from datetime import datetime
from sports_signal_bot.multi_signer_trust.attestations import verify_attestation_statement, bound_attestation_influence
from sports_signal_bot.multi_signer_trust.contracts import AttestationStatementRecord, AttestationType, AttestationScopeRecord, AttestationEvidenceRecord, AttestationProviderRecord, AttestationStatus

def test_attestation_verification():
    stmt = AttestationStatementRecord(
        statement_id="s1", provider_id="p1", attestation_type=AttestationType.REVIEW,
        scope=AttestationScopeRecord(target_family="f1", target_refs=[]),
        evidence=AttestationEvidenceRecord(evidence_id="e1", payload_hash="h1", signature="sig"),
        issued_at=datetime.utcnow()
    )
    prov = AttestationProviderRecord(provider_id="p1", provider_type="local", trust_weight_boost_cap=0.5)

    res = verify_attestation_statement(stmt, prov)
    assert res.status == AttestationStatus.VALID_SUPPORTING

def test_bound_attestation_influence():
    assert bound_attestation_influence(1.0, 0.5) == 0.3
    assert bound_attestation_influence(2.0, 0.5) == 0.5
