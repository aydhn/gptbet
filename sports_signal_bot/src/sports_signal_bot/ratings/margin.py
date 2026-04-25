import math
from typing import Optional


def get_margin_multiplier(
    method: str,
    home_score: float,
    away_score: float,
    rating_diff: float = 0.0,
    cap: Optional[float] = None,
) -> float:
    if method == "no_margin":
        return 1.0
    margin = abs(home_score - away_score)
    if margin == 0:
        return 1.0
    if method == "log_margin":
        return max(1.0, math.log(margin + 1))
    elif method == "capped_margin":
        eff_margin = min(margin, cap) if cap and cap > 0 else margin
        return max(1.0, eff_margin / 2.0)
    elif method == "football_default":
        if margin <= 1:
            return 1.0
        elif margin == 2:
            return 1.5
        else:
            return (11.0 + margin) / 8.0
    elif method == "basketball_default":
        eff_margin = min(margin, cap) if cap and cap > 0 else margin
        num = (eff_margin + 3) ** 0.8
        den = 7.5 + 0.006 * max(-1000, min(1000, abs(rating_diff)))
        return max(1.0, num / den)
    return 1.0
