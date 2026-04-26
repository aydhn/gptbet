from abc import ABC, abstractmethod
from typing import Tuple, List, Optional
from sports_signal_bot.sizing.contracts import SizingConfig, StakeSizingInputRecord


class BaseSizingStrategy(ABC):
    def __init__(self, config: SizingConfig):
        self.config = config

    @abstractmethod
    def propose_size(
        self, input_record: StakeSizingInputRecord
    ) -> Tuple[float, Optional[float], List[str]]:
        """
        Propose a raw sizing fraction before adjustments and risk limits.
        Returns:
            - raw_fraction: The unadjusted sizing fraction.
            - raw_kelly: The original full Kelly fraction (if applicable, else None).
            - warnings: A list of any warnings during calculation.
        """
        pass

    def apply_adjustments(
        self, raw_fraction: float, input_record: StakeSizingInputRecord
    ) -> float:
        """
        Apply confidence, uncertainty, and other strategy-specific dampening.
        Override in subclasses if needed. Default does nothing.
        """
        return raw_fraction

    def describe(self) -> str:
        return self.__class__.__name__

    def validate_config(self) -> List[str]:
        """Optional config validation. Returns list of warnings/errors."""
        return []
