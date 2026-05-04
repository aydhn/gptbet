from typing import List
from sports_signal_bot.ecosystem_resilience.contracts import (
    BaselineMarketplaceSignalRecord,
    MarketplaceSignalRelevanceBand
)

def ingest_marketplace_signal(
    signal_id: str,
    signal_family: str,
    source_baseline_ref: str,
    target_scope_ref: str,
    dimension_refs: List[str],
    is_stale: bool = False
) -> BaselineMarketplaceSignalRecord:
    band = compute_signal_relevance(is_stale, len(dimension_refs))

    return BaselineMarketplaceSignalRecord(
        signal_id=signal_id,
        signal_family=signal_family,
        source_baseline_ref=source_baseline_ref,
        target_scope_ref=target_scope_ref,
        dimension_refs=dimension_refs,
        freshness_state="stale" if is_stale else "fresh",
        relevance_band=band,
        caveat_refs=[],
        projection_status="pending",
        warnings=[]
    )

def validate_signal_freshness(signal: BaselineMarketplaceSignalRecord) -> bool:
    return signal.freshness_state == "fresh"

def compute_signal_relevance(is_stale: bool, dim_count: int) -> MarketplaceSignalRelevanceBand:
    if is_stale:
        return MarketplaceSignalRelevanceBand.SUPPRESSED_SIGNAL
    if dim_count > 3:
        return MarketplaceSignalRelevanceBand.USEFUL_SIGNAL
    elif dim_count > 1:
        return MarketplaceSignalRelevanceBand.BOUNDED_HINT
    return MarketplaceSignalRelevanceBand.WEAK_HINT

def summarize_signal_quality(signal: BaselineMarketplaceSignalRecord) -> str:
    return f"Signal {signal.signal_id} ({signal.signal_family}): {signal.relevance_band.value}"
