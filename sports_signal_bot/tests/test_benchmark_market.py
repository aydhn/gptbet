import pytest

from sports_signal_bot.benchmark.factory import BENCHMARK_FACTORY
from sports_signal_bot.core.constants import SportType
from sports_signal_bot.markets.registry import MARKET_REGISTRY


def test_market_registry():
    defs = MARKET_REGISTRY.list_supported_markets(SportType.FOOTBALL)
    assert len(defs) > 0

    m_def = MARKET_REGISTRY.get_market_definition(SportType.FOOTBALL, "football_1x2")
    assert m_def is not None
    assert m_def.settlement_rule_name == "football_1x2"

    lines = MARKET_REGISTRY.get_default_lines("football_over_under")
    assert len(lines) > 0
    assert MARKET_REGISTRY.is_line_market("football_over_under")


def test_benchmark_factory():
    bm = BENCHMARK_FACTORY.get_benchmark("random")
    assert bm is not None
    assert bm.name == "random"

    bm_implied = BENCHMARK_FACTORY.get_benchmark("bookmaker_implied")
    assert bm_implied is not None
