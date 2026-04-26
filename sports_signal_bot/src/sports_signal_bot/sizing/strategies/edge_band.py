from typing import Tuple, List, Optional
from sports_signal_bot.sizing.contracts import StakeSizingInputRecord
from sports_signal_bot.sizing.strategies.base import BaseSizingStrategy


class EdgeBandSizingOverlay(BaseSizingStrategy):
    """
    Allocates size based on the edge magnitude band, independent of strict Kelly.
    """

    def propose_size(
        self, input_record: StakeSizingInputRecord
    ) -> Tuple[float, Optional[float], List[str]]:
        warnings = []
        edge = input_record.edge_estimate

        if edge <= 0:
            return 0.0, None, ["No positive edge. Size zeroed."]

        # Example bands - these should ideally be configurable
        if edge > 0.15:
            fraction = 0.05
        elif edge > 0.10:
            fraction = 0.04
        elif edge > 0.05:
            fraction = 0.02
        elif edge > 0.02:
            fraction = 0.01
        else:
            fraction = 0.005  # Minimal play for tiny edges

        return fraction, None, warnings
