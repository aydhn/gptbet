import datetime
from typing import List, Dict

from .contracts import SignalManifest, SignalRankingRecord, SignalScoreRecord, SignalStatus

def generate_signal_manifest(
    run_id: str,
    sport: str,
    market_type: str,
    strategy_name: str,
    scored_signals: List[SignalScoreRecord],
    ranked_signals: List[SignalRankingRecord]
) -> SignalManifest:

    total = len(scored_signals)
    scored = sum(1 for s in scored_signals if s.status == SignalStatus.SCORED)
    weak = sum(1 for s in scored_signals if s.status == SignalStatus.WEAK_SIGNAL)
    no_ref = sum(1 for s in scored_signals if s.status == SignalStatus.NO_MARKET_REFERENCE)
    invalid = sum(1 for s in scored_signals if s.status == SignalStatus.INVALID)

    # Bucket distribution
    distribution = {"<0": 0, "0-20": 0, "20-40": 0, "40-60": 0, "60-80": 0, "80-100": 0, ">100": 0}
    for s in scored_signals:
        if s.normalized_score is None:
            continue
        v = s.normalized_score
        if v < 0: distribution["<0"] += 1
        elif v <= 20: distribution["0-20"] += 1
        elif v <= 40: distribution["20-40"] += 1
        elif v <= 60: distribution["40-60"] += 1
        elif v <= 80: distribution["60-80"] += 1
        elif v <= 100: distribution["80-100"] += 1
        else: distribution[">100"] += 1

    top = ranked_signals[:10] if ranked_signals else []
    weakest = ranked_signals[-10:] if len(ranked_signals) > 10 else []

    return SignalManifest(
        run_id=run_id,
        timestamp=datetime.datetime.utcnow(),
        sport=sport,
        market_type=market_type,
        strategy_name=strategy_name,
        total_processed=total,
        scored_count=scored,
        weak_signal_count=weak,
        no_market_reference_count=no_ref,
        invalid_count=invalid,
        top_signals=top,
        weakest_signals=weakest,
        score_distribution=distribution
    )
