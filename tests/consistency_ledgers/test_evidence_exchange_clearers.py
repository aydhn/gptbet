import pytest
from sports_signal_bot.consistency_ledgers.contracts import (
    EvidenceClearerFamily,
    ClearingOutcome
)
from sports_signal_bot.consistency_ledgers.evidence_clearers import (
    build_evidence_exchange_clearer,
    compute_clearing_pressure
)
from sports_signal_bot.consistency_ledgers.clearing_books import (
    build_clearing_book,
    create_clearing_listing,
    create_clearing_request,
    ingest_clearing_listing_and_request
)
from sports_signal_bot.consistency_ledgers.clearing_routes import (
    enumerate_clearing_matches,
    score_clearing_matches,
    select_clearing_outcome
)

def test_partial_evidence_caveated_route():
    clearer = build_evidence_exchange_clearer(
        family=EvidenceClearerFamily.BOUNDED_EVIDENCE_CLEARER,
        fairness_policy="standard"
    )

    book = build_clearing_book("exchange_1", "narrow")

    listing = create_clearing_listing(
        family="list_fam",
        source_ref="src_1",
        source_family="src_fam",
        trace_families=["trace_1"],
        audience_profiles=["aud_1"],
        completeness=0.6, # Partial evidence
        caveats=["missing_replay_proof"]
    )

    request = create_clearing_request(
        target_context_ref="ctx_1",
        trace_family="trace_1",
        required_evidence=["proof_1"],
        required_scope="narrow",
        required_audience="aud_1",
        priority="standard"
    )

    book, ingested = ingest_clearing_listing_and_request(book, listing, request)
    assert ingested

    listings = {listing.listing_id: listing}
    requests = {request.request_id: request}
    books = {book.clearing_book_id: book}

    matches = enumerate_clearing_matches(book, listings, requests)
    scored = score_clearing_matches(matches)

    outcome = select_clearing_outcome(scored)
    assert outcome.outcome == ClearingOutcome.CLEARED_CAVEATED_EVIDENCE_ROUTE
