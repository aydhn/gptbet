from typing import Any, Dict, List

import numpy as np


def generate_threshold_grid(
    config: Dict[str, Any], strategy: str
) -> List[Dict[str, float]]:
    # This might delegate to the strategy if it's strategy specific,
    # but the instructions requested a helper. We can just use the factory.
    from .factory import ThresholdStrategyFactory

    opt = ThresholdStrategyFactory.create(strategy, config)
    return opt.generate_grid()
