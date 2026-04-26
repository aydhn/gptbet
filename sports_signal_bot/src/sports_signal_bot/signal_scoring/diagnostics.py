from typing import List, Dict, Any

from .contracts import SignalDiagnosticsRecord, SignalScoreRecord, SignalStatus

def build_signal_diagnostics(
    signals: List[SignalScoreRecord],
    strategy_name: str
) -> SignalDiagnosticsRecord:
    """Builds a diagnostic record summarizing the scoring process for a batch."""

    if not signals:
        return SignalDiagnosticsRecord(
            event_id="batch", sport="unknown", market_type="unknown", strategy_used=strategy_name
        )

    # Summarize across the batch
    # We'll just take the first event for the ID, assuming this is often called per-event
    first = signals[0]

    return SignalDiagnosticsRecord(
        event_id=first.event_id,
        sport=first.sport,
        market_type=first.market_type,
        strategy_used=strategy_name,
        top_class_gap=0.0,  # Could aggregate if needed
        entropy=0.0,
        max_disagreement=0.0,
        missing_features_ratio=0.0,
        stale_components_ratio=0.0
    )
