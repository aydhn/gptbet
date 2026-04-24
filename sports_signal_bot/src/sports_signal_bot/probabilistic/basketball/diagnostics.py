from typing import List, Dict, Any
from sports_signal_bot.probabilistic.basketball.contracts import BasketballModelDiagnostics

class DiagnosticsBuilder:
    """Builds diagnostic metrics and warnings for a prediction run."""

    @staticmethod
    def build(event_id: str, expected_total: float, expected_margin: float,
              total_std: float, margin_std: float, builder_warnings: List[str],
              dist_warnings: List[str], features: Dict[str, Any]) -> BasketballModelDiagnostics:

        uncertainties = []
        if total_std > 20.0:
            uncertainties.append("High total variance detected")
        if margin_std > 16.0:
            uncertainties.append("High margin variance detected")

        if not features:
            uncertainties.append("No features provided. Using defaults.")

        return BasketballModelDiagnostics(
            event_id=event_id,
            implied_total=expected_total,
            implied_margin=expected_margin,
            total_variance=total_std ** 2,
            margin_variance=margin_std ** 2,
            uncertainty_flags=uncertainties,
            clipping_warnings=builder_warnings + dist_warnings
        )
