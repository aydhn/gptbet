import pytest
from sports_signal_bot.continuity_verification_hardening.continuity_evidence_exchanges import (
    build_continuity_evidence_exchange,
    create_continuity_evidence_listing,
    create_continuity_evidence_request,
    verify_continuity_evidence_exchange,
    summarize_continuity_evidence_exchange
)
from sports_signal_bot.continuity_verification_hardening.contracts import (
    ContinuityEvidenceExchangeFamily,
    ContinuityEvidenceExchangeStatus,
    ContinuityEvidenceListingRecord,
    ContinuityEvidenceRequestRecord
)

def test_build_continuity_evidence_exchange():
    exchange = build_continuity_evidence_exchange("exchange_test", ContinuityEvidenceExchangeFamily.scheduler_truth_evidence_exchange)
    assert exchange.continuity_evidence_exchange_id == "exchange_test"
    assert exchange.exchange_family == ContinuityEvidenceExchangeFamily.scheduler_truth_evidence_exchange
    assert exchange.exchange_status == ContinuityEvidenceExchangeStatus.exchange_gapped

def test_verify_continuity_evidence_exchange():
    exchange = build_continuity_evidence_exchange("exchange_test", ContinuityEvidenceExchangeFamily.scheduler_truth_evidence_exchange)
    listings = [
        ContinuityEvidenceListingRecord(listing_id="listing_1")
    ]
    verified_exchange = verify_continuity_evidence_exchange(exchange, listings, has_stale=False)
    assert verified_exchange.exchange_status == ContinuityEvidenceExchangeStatus.exchange_verified
