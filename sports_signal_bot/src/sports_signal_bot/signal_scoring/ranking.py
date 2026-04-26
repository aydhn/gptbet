from typing import List, Dict

from .contracts import SignalRankingRecord, SignalScoreRecord, SignalStatus

def rank_signals(
    scored_signals: List[SignalScoreRecord],
    limit: int = -1
) -> List[SignalRankingRecord]:
    """Sorts and ranks signals based on final score and tie-breakers."""

    # Filter out invalid or purely pending ones (unless we want to rank weak signals)
    valid_signals = [s for s in scored_signals if s.status != SignalStatus.INVALID]

    # Sort
    # 1. final_signal_score (desc)
    # 2. edge_estimate (desc)
    # 3. confidence_score (desc)
    # 4. uncertainty_penalty (asc)
    sorted_signals = sorted(
        valid_signals,
        key=lambda s: (
            s.final_signal_score,
            s.components.edge_estimate,
            s.components.confidence_score,
            -s.components.uncertainty_penalty
        ),
        reverse=True
    )

    ranked_records = []
    for idx, s in enumerate(sorted_signals):
        rank = idx + 1

        tier = "unranked"
        if s.status == SignalStatus.SCORED:
            if rank <= 5:
                tier = "S"
            elif rank <= 15:
                tier = "A"
            else:
                tier = "B"
        elif s.status == SignalStatus.WEAK_SIGNAL:
            tier = "C"
        else:
            tier = "D"

        record = SignalRankingRecord(
            event_id=s.event_id,
            sport=s.sport,
            market_type=s.market_type,
            selection=s.selection,
            final_signal_score=s.final_signal_score,
            normalized_score=s.normalized_score,
            rank=rank,
            tier=tier,
            status=s.status,
            edge_estimate=s.components.edge_estimate,
            confidence_score=s.components.confidence_score,
            uncertainty_penalty=s.components.uncertainty_penalty
        )
        ranked_records.append(record)

    if limit > 0:
        return ranked_records[:limit]

    return ranked_records
