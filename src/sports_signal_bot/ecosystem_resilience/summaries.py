from datetime import datetime
from sports_signal_bot.ecosystem_resilience.contracts import EcosystemResilienceScoreSummaryRecord

def build_ecosystem_resilience_summary(
    overlay_score: float,
    hub_score: float,
    signal_score: float,
    degraded_duration: float
) -> EcosystemResilienceScoreSummaryRecord:
    return EcosystemResilienceScoreSummaryRecord(
        summary_id="summary-" + datetime.now().strftime("%Y%m%d%H%M%S"),
        overlay_stability_score=overlay_score,
        hub_health_score=hub_score,
        signal_freshness_score=signal_score,
        participant_stability_score=1.0,
        federation_hygiene_score=1.0,
        scorecard_variance=0.0,
        suppression_burden=0.0,
        degraded_state_duration=degraded_duration,
        timestamp=datetime.now()
    )

def compute_resilience_dimension_trends() -> str:
    return "Stable"

def summarize_resilience_burden(summary: EcosystemResilienceScoreSummaryRecord) -> str:
    return f"Resilience Burden - Degraded duration: {summary.degraded_state_duration}h"
