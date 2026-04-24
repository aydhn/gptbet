from typing import List
from sports_signal_bot.probabilistic.football.contracts import FootballProbabilityRecord

class Diagnostics:
    """Helper to collect and format warnings from prediction records."""

    @staticmethod
    def format_warnings(records: List[FootballProbabilityRecord]) -> List[str]:
        # Deduplicate warnings across multiple market records for the same event
        all_warnings = set()
        for r in records:
            for w in r.warnings:
                all_warnings.add(f"[{r.event_id}] {w}")
        return list(all_warnings)
