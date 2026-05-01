import pytest
from sports_signal_bot.external_audit_exchange.integration import link_notarization_to_checkpoint, summarize_notary_linkage
from sports_signal_bot.external_audit_exchange.contracts import NotarizationReceiptRecord

def test_link_notarization_to_checkpoint():
    receipt = NotarizationReceiptRecord(receipt_id="r1", request_id="req1", notary_provider="test", receipt_payload="test")
    assert link_notarization_to_checkpoint(receipt, "checkpoint_1") == True

def test_summarize_notary_linkage():
    receipts = [
        NotarizationReceiptRecord(receipt_id="r1", request_id="req1", notary_provider="test", receipt_payload="test"),
        NotarizationReceiptRecord(receipt_id="r2", request_id="req2", notary_provider="test", receipt_payload="test")
    ]
    summary = summarize_notary_linkage(receipts)
    assert "2" in summary
