from sports_signal_bot.sizing.contracts import StakeSizingInputRecord
from sports_signal_bot.sizing.strategies.fractional_kelly import FractionalKellyOverlay
from sports_signal_bot.sizing.adjustments import compute_sizing_adjustments


class ConfidenceAdjustedKellyOverlay(FractionalKellyOverlay):
    """
    Computes a Fractional Kelly size, then adjusts it based on confidence,
    uncertainty, disagreement, etc.
    """

    def apply_adjustments(
        self, raw_fraction: float, input_record: StakeSizingInputRecord
    ) -> float:
        components = compute_sizing_adjustments(input_record, self.config)
        return raw_fraction * components.combined_multiplier

    def describe(self) -> str:
        return "ConfidenceAdjustedKellyOverlay"
