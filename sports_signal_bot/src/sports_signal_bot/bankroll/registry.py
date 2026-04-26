from typing import List
from typing import Dict, Type
from sports_signal_bot.bankroll.contracts import OverlayStrategyName
from sports_signal_bot.bankroll.overlays.base import BaseOverlayStrategy
from sports_signal_bot.bankroll.overlays.flat_stake import FlatStakeOverlay
from sports_signal_bot.bankroll.overlays.fixed_fraction import FixedFractionOfBankrollOverlay
from sports_signal_bot.bankroll.overlays.tiered_flat import SignalTieredFlatOverlay
from sports_signal_bot.bankroll.overlays.conservative_capped_fraction import ConservativeCappedFractionOverlay
from sports_signal_bot.bankroll.overlays.no_financial_shadow import NoFinancialShadowOverlay

class OverlayStrategyRegistry:
    _strategies: Dict[OverlayStrategyName, Type[BaseOverlayStrategy]] = {
        OverlayStrategyName.FLAT_STAKE: FlatStakeOverlay,
        OverlayStrategyName.FIXED_FRACTION: FixedFractionOfBankrollOverlay,
        OverlayStrategyName.TIERED_FLAT: SignalTieredFlatOverlay,
        OverlayStrategyName.CONSERVATIVE_CAPPED_FRACTION: ConservativeCappedFractionOverlay,
        OverlayStrategyName.NO_FINANCIAL_SHADOW: NoFinancialShadowOverlay,
    }

    @classmethod
    def get(cls, name: OverlayStrategyName) -> Type[BaseOverlayStrategy]:
        if name not in cls._strategies:
            raise ValueError(f"Overlay strategy '{name}' not found.")
        return cls._strategies[name]

    @classmethod
    def list_strategies(cls) -> List[OverlayStrategyName]:
        return list(cls._strategies.keys())
