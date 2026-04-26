from typing import Tuple, List, Optional
from sports_signal_bot.sizing.contracts import StakeSizingInputRecord
from sports_signal_bot.sizing.strategies.fractional_kelly import FractionalKellyOverlay
from sports_signal_bot.sizing.adjustments import compute_sizing_adjustments


class ConservativeResearchSizingOverlay(FractionalKellyOverlay):
    """
    Very small base fraction (e.g. 1/8th Kelly) heavily dampened by any uncertainty.
    Used for safe research testing.
    """

    def propose_size(
        self, input_record: StakeSizingInputRecord
    ) -> Tuple[float, Optional[float], List[str]]:
        # Force a very low fraction
        from sports_signal_bot.sizing.kelly import explain_kelly_estimate

        kelly_est = explain_kelly_estimate(
            decimal_odds=input_record.market_odds,
            calibrated_probability=input_record.final_selection_probability,
            fraction=0.125,  # 1/8th Kelly
        )
        return (
            kelly_est.fractional_kelly_fraction,
            kelly_est.full_kelly_fraction,
            kelly_est.warnings,
        )

    def apply_adjustments(
        self, raw_fraction: float, input_record: StakeSizingInputRecord
    ) -> float:
        components = compute_sizing_adjustments(input_record, self.config)

        # Double the penalties for conservative
        mult = components.combined_multiplier
        if mult < 1.0:
            mult = mult * mult  # Square it to penalize harder

        return raw_fraction * mult
