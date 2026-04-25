from typing import Any, Callable, Dict, List

from sports_signal_bot.evaluation.contracts import LeaderboardRow
from sports_signal_bot.regimes.contracts import (EventRegimeRecord,
                                                 RegimeEvaluationRecord)


def build_regime_leaderboard(
    event_regimes: List[EventRegimeRecord], eval_func: Callable, regime_family: str
) -> Dict[str, List[LeaderboardRow]]:
    """Groups events by regime label and builds a leaderboard for each group."""
    grouped = {}
    for r in event_regimes:
        if r.regime_family == regime_family:
            grouped.setdefault(r.regime_label, []).append(r)

    leaderboards = {}
    for label, events in grouped.items():
        leaderboards[label] = eval_func(events)

    return leaderboards


def compare_sources_within_regime(
    event_regimes: List[EventRegimeRecord],
    compare_func: Callable,
    regime_family: str,
    regime_label: str,
) -> Any:
    """Runs a pairwise comparison function only on events matching a regime."""
    filtered = [
        r
        for r in event_regimes
        if r.regime_family == regime_family and r.regime_label == regime_label
    ]
    return compare_func(filtered)
