from typing import Dict, Type
from sports_signal_bot.sizing.contracts import SizingStrategyName
from sports_signal_bot.sizing.strategies.base import BaseSizingStrategy
from sports_signal_bot.sizing.strategies.fractional_kelly import FractionalKellyOverlay
from sports_signal_bot.sizing.strategies.capped_fractional_kelly import (
    CappedFractionalKellyOverlay,
)
from sports_signal_bot.sizing.strategies.confidence_adjusted_kelly import (
    ConfidenceAdjustedKellyOverlay,
)
from sports_signal_bot.sizing.strategies.edge_band import EdgeBandSizingOverlay
from sports_signal_bot.sizing.strategies.conservative_research import (
    ConservativeResearchSizingOverlay,
)
from sports_signal_bot.sizing.strategies.hybrid_kelly_flat_floor import (
    HybridKellyFlatFloorOverlay,
)


class SizingRegistry:
    _registry: Dict[SizingStrategyName, Type[BaseSizingStrategy]] = {
        SizingStrategyName.FRACTIONAL_KELLY: FractionalKellyOverlay,
        SizingStrategyName.CAPPED_FRACTIONAL_KELLY: CappedFractionalKellyOverlay,
        SizingStrategyName.CONFIDENCE_ADJUSTED_KELLY: ConfidenceAdjustedKellyOverlay,
        SizingStrategyName.EDGE_BAND_SIZING: EdgeBandSizingOverlay,
        SizingStrategyName.CONSERVATIVE_RESEARCH: ConservativeResearchSizingOverlay,
        SizingStrategyName.HYBRID_KELLY_FLAT_FLOOR: HybridKellyFlatFloorOverlay,
    }

    @classmethod
    def get(cls, name: SizingStrategyName) -> Type[BaseSizingStrategy]:
        if name not in cls._registry:
            raise ValueError(f"Sizing strategy '{name}' not found in registry.")
        return cls._registry[name]

    @classmethod
    def register(
        cls, name: SizingStrategyName, strategy_class: Type[BaseSizingStrategy]
    ):
        cls._registry[name] = strategy_class

    @classmethod
    def list_available(cls) -> list[str]:
        return [s.value for s in cls._registry.keys()]
