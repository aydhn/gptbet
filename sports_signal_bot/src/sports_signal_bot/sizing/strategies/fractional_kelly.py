from typing import Tuple, List, Optional
from sports_signal_bot.sizing.contracts import StakeSizingInputRecord, SizingConfig
from sports_signal_bot.sizing.kelly import explain_kelly_estimate
from sports_signal_bot.sizing.strategies.base import BaseSizingStrategy


class FractionalKellyOverlay(BaseSizingStrategy):
    """
    Computes a simple Fractional Kelly size.
    Uses the configured fraction (e.g., 0.25 for quarter-Kelly).
    """

    def propose_size(
        self, input_record: StakeSizingInputRecord
    ) -> Tuple[float, Optional[float], List[str]]:
        fraction = self.config.fractional_kelly_by_market.get(
            input_record.market_type, self.config.fractional_kelly_default
        )

        kelly_est = explain_kelly_estimate(
            decimal_odds=input_record.market_odds,
            calibrated_probability=input_record.final_selection_probability,
            fraction=fraction,
        )

        raw_fraction = kelly_est.fractional_kelly_fraction
        return raw_fraction, kelly_est.full_kelly_fraction, kelly_est.warnings
