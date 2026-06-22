from typing import Any, Dict, List, Tuple

from sports_signal_bot.consistency_ledgers.contracts import (
    ClearingBookRecord,
    ClearingFairnessRecord,
    ClearingListingRecord,
    ClearingPressureRecord,
    ClearingRequestRecord,
    EvidenceClearerFamily,
    EvidenceExchangeClearerRecord,
    HealthStatus,
)
from sports_signal_bot.consistency_ledgers.utils import generate_id


def build_evidence_exchange_clearer(
    family: EvidenceClearerFamily, fairness_policy: str
) -> EvidenceExchangeClearerRecord:
    return EvidenceExchangeClearerRecord(
        evidence_clearer_id=generate_id("ev_clearer"),
        clearer_family=family,
        source_exchange_refs=[],
        clearing_book_refs=[],
        active_listing_refs=[],
        active_request_refs=[],
        active_match_refs=[],
        fairness_policy_ref=fairness_policy,
        health_status=HealthStatus.HEALTHY,
        warnings=[],
    )


def compute_clearing_pressure(
    clearer: EvidenceExchangeClearerRecord,
    books: Dict[str, ClearingBookRecord],
    listings: Dict[str, ClearingListingRecord],
    requests: Dict[str, ClearingRequestRecord],
) -> ClearingPressureRecord:
    stale_listings = sum(
        1 for l in listings.values() if l.currentness_state != "current"
    )
    backlogged_reqs = sum(len(b.backlog_refs) for b in books.values())

    metrics = {
        "stale_listing_density": stale_listings / max(1, len(listings)),
        "clearing_backlog": backlogged_reqs,
        "evidence_gap_ratio": 0.1,
        "no_safe_visibility_burden": 0.05,
    }

    score = 0.0
    if metrics["stale_listing_density"] > 0.4:
        score += 40
    if metrics["clearing_backlog"] > 10:
        score += 40

    warnings = []
    if score >= 80:
        warnings.append("Critical clearing pressure.")
    elif score >= 50:
        warnings.append("High clearing pressure.")

    return ClearingPressureRecord(
        record_id=generate_id("clear_press"),
        clearer_id=clearer.evidence_clearer_id,
        pressure_score=score,
        metrics=metrics,
        warnings=warnings,
    )


def compute_clearing_fairness(
    clearer: EvidenceExchangeClearerRecord, pressure: ClearingPressureRecord
) -> ClearingFairnessRecord:
    metrics = {"request_aging": 10.0, "review_only_spillover": 0.2}

    score = 100.0 - pressure.pressure_score

    return ClearingFairnessRecord(
        record_id=generate_id("clear_fair"),
        clearer_id=clearer.evidence_clearer_id,
        fairness_score=max(0.0, score),
        metrics=metrics,
    )


def preserve_fairness_without_scope_widening(
    fairness: ClearingFairnessRecord,
) -> Tuple[ClearingFairnessRecord, bool]:
    # Fairness adjustments must not authorize scope widening
    if fairness.fairness_score < 50:
        return fairness, False  # Degraded fairness, do not widen scope
    return fairness, True


def summarize_clearing_pressure_and_fairness(
    pressure: ClearingPressureRecord, fairness: ClearingFairnessRecord
) -> Dict[str, Any]:
    return {
        "pressure_score": pressure.pressure_score,
        "fairness_score": fairness.fairness_score,
        "pressure_warnings": pressure.warnings,
    }
