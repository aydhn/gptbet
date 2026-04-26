import pytest

from sports_signal_bot.probabilistic.basketball.contracts import (
    BasketballDistributionConfig,
)
from sports_signal_bot.probabilistic.basketball.distribution import (
    BasketballDistributionCore,
)


def test_variance_assumptions_floor():
    config = BasketballDistributionConfig(total_std=1.0, margin_std=0.5, std_floor=2.0)
    core = BasketballDistributionCore(config)

    t_std, m_std, warnings = core.get_variance_assumptions({})

    assert t_std == 2.0
    assert m_std == 2.0
    assert len(warnings) == 2


def test_variance_modifiers():
    config = BasketballDistributionConfig(total_std=10.0, margin_std=10.0)
    core = BasketballDistributionCore(config)

    features = {"total_std_modifier": 1.5, "margin_std_modifier": 0.8}

    t_std, m_std, _ = core.get_variance_assumptions(features)

    assert t_std == 15.0
    assert m_std == 8.0
