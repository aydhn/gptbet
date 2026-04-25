import math
from typing import Tuple


def calculate_1x2_probabilities(
    home_expected: float, away_expected: float, method: str = "heuristic"
) -> Tuple[float, float, float]:
    p_h = home_expected
    p_a = away_expected
    if method == "none":
        return (p_h, 0.0, p_a)
    if method == "heuristic":
        diff = abs(p_h - p_a)
        p_draw = 0.3 * math.exp(-3.0 * diff)
        remaining = 1.0 - p_draw
        total_p = p_h + p_a
        if total_p == 0:
            return (remaining / 2, p_draw, remaining / 2)
        p_home_final = (p_h / total_p) * remaining
        p_away_final = (p_a / total_p) * remaining
        return (p_home_final, p_draw, p_away_final)
    return (p_h, 0.0, p_a)
