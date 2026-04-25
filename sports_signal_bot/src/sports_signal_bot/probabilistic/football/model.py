from typing import Any, Dict, List

from sports_signal_bot.probabilistic.football.contracts import (
    FootballProbabilityRecord, LambdaBuildContext)
from sports_signal_bot.probabilistic.football.correct_score import \
    CorrectScoreExtractor
from sports_signal_bot.probabilistic.football.lambda_builder import \
    GoalLambdaBuilder
from sports_signal_bot.probabilistic.football.markets import MarketExtractor
from sports_signal_bot.probabilistic.football.score_matrix import \
    PoissonScoreMatrix


class FootballPoissonModel:
    """
    Facade for the Football Poisson probabilistic core.
    Generates all supported market predictions from features.
    """

    def __init__(self, lambda_builder: GoalLambdaBuilder = None):
        self.lambda_builder = lambda_builder or GoalLambdaBuilder()

    def predict(
        self, context: LambdaBuildContext, features: Dict[str, float]
    ) -> List[FootballProbabilityRecord]:
        """Generates predictions for all supported base markets."""
        # 1. Build Lambdas
        lambda_estimate = self.lambda_builder.build(context, features)

        # 2. Build Matrix
        score_matrix = PoissonScoreMatrix(lambda_estimate, context.config)

        # 3. Extract Markets
        records = []

        # Base expected metrics for supporting data
        exp_metrics = MarketExtractor.extract_expected_metrics(score_matrix)

        # 1X2
        probs_1x2 = MarketExtractor.extract_1x2(score_matrix)
        records.append(
            FootballProbabilityRecord(
                event_id=context.event_id,
                market_type="1x2",
                model_name=context.model_name,
                predicted_probabilities=probs_1x2,
                supporting_metrics=exp_metrics,
                warnings=lambda_estimate.warnings + score_matrix.record.warnings,
            )
        )

        # BTTS
        probs_btts = MarketExtractor.extract_btts(score_matrix)
        records.append(
            FootballProbabilityRecord(
                event_id=context.event_id,
                market_type="btts",
                model_name=context.model_name,
                predicted_probabilities=probs_btts,
                supporting_metrics=exp_metrics,
                warnings=lambda_estimate.warnings + score_matrix.record.warnings,
            )
        )

        # O/U lines
        for line in [0.5, 1.5, 2.5, 3.5, 4.5]:
            probs_ou = MarketExtractor.extract_over_under(score_matrix, line)
            # Replace dot with underscore for market type convention
            market_type = f"ou_{str(line).replace('.', '_')}"
            records.append(
                FootballProbabilityRecord(
                    event_id=context.event_id,
                    market_type=market_type,
                    model_name=context.model_name,
                    predicted_probabilities=probs_ou,
                    supporting_metrics=exp_metrics,
                    warnings=lambda_estimate.warnings + score_matrix.record.warnings,
                )
            )

        return records
