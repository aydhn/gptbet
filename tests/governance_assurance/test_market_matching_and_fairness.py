import pytest
from sports_signal_bot.governance_assurance.contracts import MatchOutcome
from sports_signal_bot.governance_assurance.matching import (
    create_replay_market_offer, create_replay_market_request,
    validate_offer_request_compatibility, enumerate_replay_market_matches
)

def test_market_matching_flow():
    offer = create_replay_market_offer("o1", "l1", ["scope_A", "scope_B"])
    req1 = create_replay_market_request("req1", "lin1", "scope_A")
    req2 = create_replay_market_request("req2", "lin1", "scope_C")

    assert validate_offer_request_compatibility(offer, req1) == True
    assert validate_offer_request_compatibility(offer, req2) == False

    matches = enumerate_replay_market_matches([offer], [req1, req2])
    assert len(matches) == 2

    # req1 should match
    assert matches[0].match_outcome == MatchOutcome.MATCHED_BOUNDED
    assert matches[0].request_ref == "req1"

    # req2 should fail
    assert matches[1].match_outcome == MatchOutcome.NO_SAFE_MARKET_MATCH
    assert matches[1].request_ref == "req2"

def test_market_matching_weak_evidence():
    offer = create_replay_market_offer("o1", "l1", ["scope_A"])
    offer.replay_evidence_profile = "weak_evidence"
    req = create_replay_market_request("req1", "lin1", "scope_A")

    matches = enumerate_replay_market_matches([offer], [req])
    assert matches[0].match_outcome == MatchOutcome.MATCHED_REVIEW_ONLY
    assert matches[0].revalidation_required == True
