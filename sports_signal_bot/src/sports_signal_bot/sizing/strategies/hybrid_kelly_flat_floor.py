from typing import Tuple, List, Optional
from sports_signal_bot.sizing.contracts import StakeSizingInputRecord
from sports_signal_bot.sizing.strategies.fractional_kelly import FractionalKellyOverlay


class HybridKellyFlatFloorOverlay(FractionalKellyOverlay):
    """
    If Kelly proposal is positive but very small, bumps it up to a minimum flat fraction,
    provided quality gates are met. Useful for comparing Kelly vs Flat.
    """

    def propose_size(
        self, input_record: StakeSizingInputRecord
    ) -> Tuple[float, Optional[float], List[str]]:
        raw_frac, full_kelly, warnings = super().propose_size(input_record)

        if full_kelly is not None and full_kelly > 0:
            min_floor_fraction = 0.01  # 1% floor
            if raw_frac > 0 and raw_frac < min_floor_fraction:
                # Check basic quality - if confidence is okay, apply floor
                if (
                    input_record.confidence_score >= 1.0
                    and input_record.data_quality_penalty < 0.2
                ):
                    raw_frac = min_floor_fraction
                    warnings.append(
                        f"Applied hybrid flat floor: raised to {min_floor_fraction}"
                    )

        return raw_frac, full_kelly, warnings
