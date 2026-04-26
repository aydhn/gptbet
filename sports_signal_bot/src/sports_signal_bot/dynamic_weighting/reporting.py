from typing import List

from sports_signal_bot.dynamic_weighting.contracts import (
    WeightingDecisionRecord, WeightingDiagnosticsRecord)


def summarize_diagnostics(diagnostics: List[WeightingDiagnosticsRecord]) -> dict:
    total_events = len(diagnostics)
    if total_events == 0:
        return {}

    fallbacks = sum(1 for d in diagnostics if d.fallback_used)
    avg_trust = sum(d.average_trust for d in diagnostics) / total_events

    # Count occurrences
    top_sources = {}
    for d in diagnostics:
        if d.top_source:
            top_sources[d.top_source] = top_sources.get(d.top_source, 0) + 1

    return {
        "total_events": total_events,
        "fallback_rate": fallbacks / total_events,
        "average_trust": avg_trust,
        "most_frequent_top_sources": dict(
            sorted(top_sources.items(), key=lambda item: item[1], reverse=True)[:5]
        ),
    }
