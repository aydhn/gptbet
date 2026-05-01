import pytest
from sports_signal_bot.external_audit_exchange.contracts import ExternalAuditResponseRecord, ExternalAuditRequestRecord
from sports_signal_bot.external_audit_exchange.responses import ingest_external_response, validate_external_response_schema, evaluate_external_response_trust, decide_external_response_outcome

def test_ingest_external_response():
    response = ExternalAuditResponseRecord(
        external_response_id="ext_1",
        request_id="req_1",
        responder_family="test",
        response_status="completed",
        trust_level_claimed="high"
    )
    import_record = ingest_external_response(response)
    assert import_record.external_response_id == "ext_1"
    assert import_record.status == "imported_pending_verification"

def test_validate_external_response_schema():
    raw_response = {
        "external_response_id": "ext_1",
        "request_id": "req_1",
        "responder_family": "test",
        "response_status": "completed",
        "trust_level_claimed": "high"
    }
    assert validate_external_response_schema(raw_response) == True

def test_decide_external_response_outcome():
    response = ExternalAuditResponseRecord(
        external_response_id="ext_1",
        request_id="req_1",
        responder_family="test",
        response_status="completed",
        trust_level_claimed="high"
    )
    import_record = ingest_external_response(response)
    outcome = decide_external_response_outcome(import_record, "trusted")
    assert outcome == "verified_supporting"
    assert import_record.status == "imported_verified_supporting"
    assert "add_supporting_evidence" in import_record.local_actions
