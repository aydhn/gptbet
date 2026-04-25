from typing import Dict, List, Optional

from sports_signal_bot.core.constants import SportType

from .definitions import MarketDefinition
from .enums import ExtendedMarketType


class MarketRegistry:
    def __init__(self):
        self._definitions: Dict[str, MarketDefinition] = {}
        self._default_lines: Dict[str, List[float]] = {}
        self._setup_football_markets()
        self._setup_basketball_markets()

    def _setup_football_markets(self):
        self._definitions[ExtendedMarketType.FOOTBALL_1X2] = MarketDefinition(
            market_type=ExtendedMarketType.FOOTBALL_1X2,
            sport=SportType.FOOTBALL,
            selection_schema=["home", "draw", "away"],
            required_inputs=["final_home_score", "final_away_score"],
            settlement_rule_name="football_1x2",
            supports_multiclass=True,
        )
        self._definitions[ExtendedMarketType.FOOTBALL_OVER_UNDER] = MarketDefinition(
            market_type=ExtendedMarketType.FOOTBALL_OVER_UNDER,
            sport=SportType.FOOTBALL,
            selection_schema=["over", "under"],
            required_inputs=["final_home_score", "final_away_score"],
            settlement_rule_name="football_over_under",
        )
        self._definitions[ExtendedMarketType.FOOTBALL_BTTS] = MarketDefinition(
            market_type=ExtendedMarketType.FOOTBALL_BTTS,
            sport=SportType.FOOTBALL,
            selection_schema=["yes", "no"],
            required_inputs=["final_home_score", "final_away_score"],
            settlement_rule_name="football_btts",
        )
        # Defaults
        self._default_lines[ExtendedMarketType.FOOTBALL_OVER_UNDER] = [
            0.5,
            1.5,
            2.5,
            3.5,
            4.5,
        ]

    def _setup_basketball_markets(self):
        self._definitions[ExtendedMarketType.BASKETBALL_MATCH_WINNER] = (
            MarketDefinition(
                market_type=ExtendedMarketType.BASKETBALL_MATCH_WINNER,
                sport=SportType.BASKETBALL,
                selection_schema=["home", "away"],
                required_inputs=["final_home_score", "final_away_score"],
                settlement_rule_name="basketball_moneyline",
            )
        )
        self._definitions[ExtendedMarketType.BASKETBALL_HANDICAP] = MarketDefinition(
            market_type=ExtendedMarketType.BASKETBALL_HANDICAP,
            sport=SportType.BASKETBALL,
            selection_schema=["home", "away"],
            required_inputs=["final_home_score", "final_away_score"],
            settlement_rule_name="basketball_spread",
            supports_push=True,
        )
        self._definitions[ExtendedMarketType.BASKETBALL_TOTAL_POINTS] = (
            MarketDefinition(
                market_type=ExtendedMarketType.BASKETBALL_TOTAL_POINTS,
                sport=SportType.BASKETBALL,
                selection_schema=["over", "under"],
                required_inputs=["final_home_score", "final_away_score"],
                settlement_rule_name="basketball_totals",
                supports_push=True,
            )
        )
        # Defaults
        self._default_lines[ExtendedMarketType.BASKETBALL_TOTAL_POINTS] = [
            180.5,
            190.5,
            200.5,
            210.5,
            220.5,
            230.5,
        ]
        self._default_lines[ExtendedMarketType.BASKETBALL_HANDICAP] = [
            -10.5,
            -7.5,
            -5.5,
            -3.5,
            -1.5,
            1.5,
            3.5,
            5.5,
            7.5,
            10.5,
        ]

    def get_market_definition(
        self, sport: SportType, market_type: str
    ) -> Optional[MarketDefinition]:
        market = self._definitions.get(market_type)
        if market and market.sport == sport:
            return market
        return None

    def list_supported_markets(self, sport: SportType) -> List[MarketDefinition]:
        return [m for m in self._definitions.values() if m.sport == sport]

    def is_line_market(self, market_type: str) -> bool:
        return market_type in self._default_lines

    def get_default_lines(self, market_type: str) -> List[float]:
        return self._default_lines.get(market_type, [])


# Singleton registry
MARKET_REGISTRY = MarketRegistry()
