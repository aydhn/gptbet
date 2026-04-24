import math
from typing import Dict, Tuple, List
from scipy.stats import norm
from sports_signal_bot.probabilistic.basketball.contracts import BasketballDistributionConfig, BasketballModelDiagnostics

class BasketballDistributionCore:
    """Core logic for calculating probabilities using a Normal approximation."""

    def __init__(self, config: BasketballDistributionConfig):
        self.config = config

    def _safe_prob(self, p: float) -> float:
        """Clips probability to valid bounds and handles NaNs."""
        if math.isnan(p):
            return 0.0
        eps = self.config.probability_clip_eps
        return max(eps, min(1.0 - eps, p))

    def get_variance_assumptions(self, features: Dict[str, float] = None) -> Tuple[float, float, List[str]]:
        """Determines total and margin standard deviations, allowing feature-based hooks."""
        warnings = []
        features = features or {}

        # Start with fixed base
        total_std = self.config.total_std
        margin_std = self.config.margin_std

        # Optional: Feature-driven STD adjustments (e.g., pace_adjusted_std, injury_adjusted_std)
        if "total_std_modifier" in features:
            total_std *= features["total_std_modifier"]
        if "margin_std_modifier" in features:
            margin_std *= features["margin_std_modifier"]

        # Floor guardrail
        floor = self.config.std_floor
        if total_std < floor:
            warnings.append(f"Total STD {total_std} below floor {floor}. Clipped.")
            total_std = floor
        if margin_std < floor:
            warnings.append(f"Margin STD {margin_std} below floor {floor}. Clipped.")
            margin_std = floor

        return total_std, margin_std, warnings

    def prob_moneyline_home(self, expected_margin_home: float, margin_std: float) -> float:
        """P(Home Win) = P(Margin > 0). Ties are assumed negligible."""
        # Margin is Home - Away. So Home wins if Margin > 0.
        # We calculate 1 - CDF(0) which is sf(0)
        p = norm.sf(0, loc=expected_margin_home, scale=margin_std)
        return self._safe_prob(p)

    def prob_moneyline_away(self, prob_home: float) -> float:
        """Complement of Home Win. Overtime pushes ties to a winner."""
        return self._safe_prob(1.0 - prob_home)

    def prob_total_over(self, line: float, expected_total: float, total_std: float) -> float:
        """P(Total > line)."""
        p = norm.sf(line, loc=expected_total, scale=total_std)
        return self._safe_prob(p)

    def prob_total_under(self, line: float, expected_total: float, total_std: float) -> float:
        """P(Total < line)."""
        p = norm.cdf(line, loc=expected_total, scale=total_std)
        return self._safe_prob(p)

    def prob_home_cover(self, spread_line: float, expected_margin_home: float, margin_std: float) -> float:
        """
        Calculates probability Home covers the spread.
        Sign Convention: A negative spread (e.g. -3.5) means Home is favored.
        Home covers if expected_margin_home > (-spread_line).
        Example: Spread is -3.5. Home covers if margin > 3.5.
        So we check P(Margin > -spread_line).
        """
        # The threshold to beat is the inverse of the spread.
        # If spread is -5.5, threshold is 5.5.
        threshold = -spread_line
        p = norm.sf(threshold, loc=expected_margin_home, scale=margin_std)
        return self._safe_prob(p)

    def prob_away_cover(self, spread_line: float, expected_margin_home: float, margin_std: float) -> float:
        """
        Calculates probability Away covers the spread.
        Away covers if expected_margin_home < (-spread_line).
        """
        threshold = -spread_line
        p = norm.cdf(threshold, loc=expected_margin_home, scale=margin_std)
        return self._safe_prob(p)
