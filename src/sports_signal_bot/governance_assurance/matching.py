from typing import List, Optional
from sports_signal_bot.governance_assurance.contracts import (
    ReplayMarketOfferRecord,
    ReplayMarketRequestRecord,
    ReplayMarketMatchRecord,
    MatchOutcome
)

def create_replay_market_offer(offer_id: str, listing_ref: str, scope_classes: List[str]) -> ReplayMarketOfferRecord:
    return ReplayMarketOfferRecord(
        offer_id=offer_id,
        listing_ref=listing_ref,
        available_capacity=100,
        supported_fidelity="standard",
        supported_scope_classes=scope_classes,
        replay_evidence_profile="standard_evidence",
        price_like_priority_score=50,
        offer_status="active",
        warnings=[]
    )

def create_replay_market_request(request_id: str, target_lineage: str, required_scope: str) -> ReplayMarketRequestRecord:
    return ReplayMarketRequestRecord(
        request_id=request_id,
        target_lineage_ref=target_lineage,
        requested_replay_family="default_replay",
        required_fidelity="standard",
        required_evidence_refs=["ev1"],
        required_scope_class=required_scope,
        request_priority=50,
        request_status="open",
        warnings=[]
    )

def validate_offer_request_compatibility(offer: ReplayMarketOfferRecord, request: ReplayMarketRequestRecord) -> bool:
    if request.required_scope_class not in offer.supported_scope_classes:
        return False
    return True

def enumerate_replay_market_matches(offers: List[ReplayMarketOfferRecord], requests: List[ReplayMarketRequestRecord]) -> List[ReplayMarketMatchRecord]:
    matches = []
    for req in requests:
        best_match = None
        for off in offers:
            if validate_offer_request_compatibility(off, req):
                # Basic matching - scope preservation
                outcome = MatchOutcome.MATCHED_BOUNDED
                # Downgrade if evidence profile is weak
                if off.replay_evidence_profile == "weak_evidence":
                    outcome = MatchOutcome.MATCHED_REVIEW_ONLY

                best_match = ReplayMarketMatchRecord(
                    match_id=f"match_{req.request_id}_{off.offer_id}",
                    request_ref=req.request_id,
                    offer_ref=off.offer_id,
                    match_outcome=outcome,
                    caveat_refs=["scope_preserved"],
                    revalidation_required=(outcome == MatchOutcome.MATCHED_REVIEW_ONLY)
                )
                break # First match wins for simplicity in this bounded demo

        if not best_match:
            matches.append(ReplayMarketMatchRecord(
                match_id=f"match_{req.request_id}_none",
                request_ref=req.request_id,
                offer_ref="none",
                match_outcome=MatchOutcome.NO_SAFE_MARKET_MATCH,
                caveat_refs=["no_compatible_scope"],
                revalidation_required=False
            ))
        else:
            matches.append(best_match)

    return matches

def summarize_market_match(match: ReplayMarketMatchRecord) -> str:
    return f"Match {match.match_id}: Outcome {match.match_outcome.value}"
