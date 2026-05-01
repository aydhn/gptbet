import pytest
from sports_signal_bot.external_audit_exchange.notarization import build_notarization_digest, request_notarization, verify_notarization_receipt
from sports_signal_bot.external_audit_exchange.contracts import NotarizationReceiptRecord

def test_notarization_flow():
    digest = build_notarization_digest("target_1", "payload_data")
    req = request_notarization(digest, "notary_A", "target_1")

    receipt = NotarizationReceiptRecord(
        receipt_id="rec_1",
        request_id=req.request_id,
        notary_provider="notary_A",
        receipt_payload=f"signed:{digest}"
    )

    verification = verify_notarization_receipt(receipt, digest)
    assert verification.status == "notarization_verified"

def test_notarization_flow_unverified():
    digest = build_notarization_digest("target_1", "payload_data")
    req = request_notarization(digest, "notary_A", "target_1")

    receipt = NotarizationReceiptRecord(
        receipt_id="rec_1",
        request_id=req.request_id,
        notary_provider="notary_A",
        receipt_payload=f"signed:wrong_digest"
    )

    verification = verify_notarization_receipt(receipt, digest)
    assert verification.status == "notarization_unverified"
