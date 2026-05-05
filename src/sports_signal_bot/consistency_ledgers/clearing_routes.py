from typing import List, Dict, Any, Tuple
from sports_signal_bot.consistency_ledgers.contracts import (
    ClearingBookRecord,
    ClearingListingRecord,
    ClearingRequestRecord,
    ClearingMatchRecord,
    ClearingOutcome
)
from sports_signal_bot.consistency_ledgers.clearing_books import validate_clearing_compatibility
from sports_signal_bot.consistency_ledgers.utils import generate_id

def enumerate_clearing_matches(
    book: ClearingBookRecord,
    listings: Dict[str, ClearingListingRecord],
    requests: Dict[str, ClearingRequestRecord]
) -> List[Dict[str, Any]]:
    matches = []

    for req_id in book.compatible_request_refs:
        if req_id not in requests:
            continue
        req = requests[req_id]

        for list_id in book.compatible_listing_refs:
            if list_id not in listings:
                continue
            listing = listings[list_id]

            is_compat, warnings = validate_clearing_compatibility(listing, req)
            if is_compat or req.request_priority == "critical": # Allow degraded matches for critical
                matches.append({
                    "request": req,
                    "listing": listing,
                    "warnings": warnings
                })

    return matches

def score_clearing_matches(matches: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    for match in matches:
        score = 100
        listing = match["listing"]
        req = match["request"]
        warnings = match["warnings"]

        score -= (1.0 - listing.evidence_completeness) * 50

        if listing.currentness_state != "current":
            score -= 30
            warnings.append("Stale listing lowers score.")

        if listing.caveat_refs:
            score -= 10
            warnings.append("Caveated listing.")

        if any("no_safe" in w for w in listing.warnings):
            score -= 50
            warnings.append("No-safe visibility constraint limits score.")

        match["score"] = score
        match["warnings"] = warnings

    return sorted(matches, key=lambda x: x["score"], reverse=True)

def apply_clearing_constraints(
    scored_matches: List[Dict[str, Any]],
    pressure_state: str
) -> List[Dict[str, Any]]:
    for m in scored_matches:
        if pressure_state in ["high", "critical"] and m["score"] < 80:
            m["warnings"].append(f"Match degraded due to clearing pressure: {pressure_state}")
            m["score"] -= 20
    return scored_matches

def select_clearing_outcome(scored_matches: List[Dict[str, Any]]) -> ClearingMatchRecord:
    if not scored_matches:
        return ClearingMatchRecord(
            match_id=generate_id("clear_match"),
            listing_ref="",
            request_ref="",
            outcome=ClearingOutcome.CLEARING_BLOCKED,
            warnings=["No viable matches found."]
        )

    best_match = scored_matches[0]
    score = best_match["score"]

    outcome = ClearingOutcome.CLEARED_BOUNDED_EVIDENCE_ROUTE

    if any("no_safe" in w for w in best_match["warnings"]):
        outcome = ClearingOutcome.NO_SAFE_CLEARING_ROUTE
    elif score < 50:
        outcome = ClearingOutcome.CLEARED_DEGRADED_EVIDENCE_ROUTE
    elif score < 80 and not best_match["listing"].caveat_refs:
        outcome = ClearingOutcome.CLEARED_REVIEW_ONLY_EVIDENCE_ROUTE
    elif best_match["listing"].caveat_refs:
        outcome = ClearingOutcome.CLEARED_CAVEATED_EVIDENCE_ROUTE

    return ClearingMatchRecord(
        match_id=generate_id("clear_match"),
        listing_ref=best_match["listing"].listing_id,
        request_ref=best_match["request"].request_id,
        outcome=outcome,
        warnings=best_match["warnings"]
    )

def summarize_clearing_outcome(match: ClearingMatchRecord) -> Dict[str, Any]:
    return {
        "match_id": match.match_id,
        "outcome": match.outcome.value,
        "warnings": match.warnings
    }
