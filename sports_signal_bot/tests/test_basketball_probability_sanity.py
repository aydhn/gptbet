import math

import pytest

from sports_signal_bot.probabilistic.basketball.contracts import \
    BasketballDistributionConfig
from sports_signal_bot.probabilistic.basketball.distribution import \
    BasketballDistributionCore


def test_nan_probability_guard():
    config = BasketballDistributionConfig()
    core = BasketballDistributionCore(config)

    # _safe_prob should handle NaNs by returning 0
    assert core._safe_prob(float("nan")) == 0.0


def test_probability_clipping():
    config = BasketballDistributionConfig(probability_clip_eps=0.01)
    core = BasketballDistributionCore(config)

    assert core._safe_prob(0.999) == 0.99
    assert core._safe_prob(0.001) == 0.01
