from typing import Dict, Any, List, Optional
from sports_signal_bot.probabilistic.basketball.contracts import BasketballProbabilityRecord, BasketballDistributionConfig
from sports_signal_bot.probabilistic.basketball.expected_points import ExpectedPointsBuilder
from sports_signal_bot.probabilistic.basketball.distribution import BasketballDistributionCore
from sports_signal_bot.probabilistic.basketball.markets import BasketballMarketExtractor
from sports_signal_bot.probabilistic.basketball.diagnostics import DiagnosticsBuilder

class BasketballProbabilisticModel:
    """Facade uniting builders and distributions to emit probability records."""

    def __init__(self, config: BasketballDistributionConfig = None):
        self.config = config or BasketballDistributionConfig()
        self.points_builder = ExpectedPointsBuilder()
        self.dist_core = BasketballDistributionCore(self.config)
        self.extractor = BasketballMarketExtractor(self.dist_core)

    def predict(self, event_id: str, features: Dict[str, Any], model_name: str = "basketball_normal_baseline") -> List[BasketballProbabilityRecord]:
        """Generates all configured market predictions."""
        records = []

        # 1. Expected Points
        estimate = self.points_builder.build(event_id, features, self.config, model_name=model_name)

        # 2. Variance assumptions
        total_std, margin_std, dist_warnings = self.dist_core.get_variance_assumptions(features)

        # 3. Diagnostics
        diagnostics = DiagnosticsBuilder.build(
            event_id=event_id,
            expected_total=estimate.expected_total_points,
            expected_margin=estimate.expected_margin_home,
            total_std=total_std,
            margin_std=margin_std,
            builder_warnings=estimate.warnings,
            dist_warnings=dist_warnings,
            features=features
        )

        all_warnings = estimate.warnings + dist_warnings

        # Supporting metrics for all records
        supporting = {
            "expected_home_points": estimate.expected_home_points,
            "expected_away_points": estimate.expected_away_points,
            "expected_total_points": estimate.expected_total_points,
            "expected_margin_home": estimate.expected_margin_home,
            "total_std": total_std,
            "margin_std": margin_std
        }

        # Moneyline
        ml_probs = self.extractor.extract_moneyline(estimate.expected_margin_home, margin_std)
        records.append(BasketballProbabilityRecord(
            event_id=event_id,
            market_type="moneyline",
            model_name=model_name,
            predicted_probabilities=ml_probs,
            supporting_metrics=supporting,
            warnings=all_warnings
        ))

        # Totals
        totals_probs = self.extractor.extract_totals(estimate.expected_total_points, total_std)
        for k, v in totals_probs.items():
            records.append(BasketballProbabilityRecord(
                event_id=event_id,
                market_type=k,
                model_name=model_name,
                predicted_probabilities=v,
                supporting_metrics=supporting,
                warnings=all_warnings
            ))

        # Spreads
        spread_probs = self.extractor.extract_spreads(estimate.expected_margin_home, margin_std)
        for k, v in spread_probs.items():
            records.append(BasketballProbabilityRecord(
                event_id=event_id,
                market_type=k,
                model_name=model_name,
                predicted_probabilities=v,
                supporting_metrics=supporting,
                warnings=all_warnings
            ))

        return records
