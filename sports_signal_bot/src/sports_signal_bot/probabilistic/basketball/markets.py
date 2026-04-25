from typing import Dict, List

from sports_signal_bot.probabilistic.basketball.distribution import \
    BasketballDistributionCore


class BasketballMarketExtractor:
    """Extracts odds/probabilities for specific markets from the distribution core."""

    def __init__(self, core: BasketballDistributionCore):
        self.core = core

    def extract_moneyline(
        self, expected_margin_home: float, margin_std: float
    ) -> Dict[str, float]:
        """Extracts Moneyline probabilities."""
        p_home = self.core.prob_moneyline_home(expected_margin_home, margin_std)
        p_away = self.core.prob_moneyline_away(p_home)
        return {"home_win": p_home, "away_win": p_away}

    def extract_totals(
        self, expected_total: float, total_std: float, lines: List[float] = None
    ) -> Dict[str, Dict[str, float]]:
        """Extracts Over/Under probabilities for a list of lines."""
        if not lines:
            lines = self.core.config.default_preview_lines.get("totals", [])

        results = {}
        for line in lines:
            key = f"total_{str(line).replace('.', '_')}"
            p_over = self.core.prob_total_over(line, expected_total, total_std)
            p_under = self.core.prob_total_under(line, expected_total, total_std)
            results[key] = {"over": p_over, "under": p_under}
        return results

    def extract_spreads(
        self, expected_margin_home: float, margin_std: float, lines: List[float] = None
    ) -> Dict[str, Dict[str, float]]:
        """
        Extracts Spread cover probabilities for a list of lines.
        Sign Convention: A negative spread indicates Home is the favorite.
        """
        if not lines:
            lines = self.core.config.default_preview_lines.get("spreads", [])

        results = {}
        for line in lines:
            key = f"spread_{str(line).replace('.', '_').replace('-', 'm')}"
            p_home_cover = self.core.prob_home_cover(
                line, expected_margin_home, margin_std
            )
            p_away_cover = self.core.prob_away_cover(
                line, expected_margin_home, margin_std
            )
            results[key] = {"home_cover": p_home_cover, "away_cover": p_away_cover}
        return results
