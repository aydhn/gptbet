import math
from typing import Any, Dict, Tuple

from sports_signal_bot.probabilistic.football.contracts import \
    LambdaBuildContext


class StrengthMapper:
    """
    Maps various rating proxies and context to basic attacking/defending strengths.
    In later phases this connects tightly with Phase 5 rating engines.
    """

    def map_strengths(
        self, context: LambdaBuildContext, features: Dict[str, float]
    ) -> Tuple[float, float, float]:
        """
        Maps features to home strength, away strength, and a base total proxy.
        Returns: (home_strength_proxy, away_strength_proxy, base_total_proxy)
        """
        config = context.config

        # 1. Base Total Proxy
        base_total = features.get(
            "league_total_goal_baseline", config.default_league_goal_baseline
        )
        if base_total <= 0:
            base_total = config.fallback_goal_baseline

        # 2. Rating Differentials
        # We assume ratings are roughly centered around 1500 (Elo style)
        # Or a rating diff is directly provided
        rating_diff = features.get("rating_diff")
        if rating_diff is None:
            home_rating = features.get("home_rating_proxy", 1500.0)
            away_rating = features.get("away_rating_proxy", 1500.0)
            rating_diff = home_rating - away_rating

        # Convert rating diff to a goal expectancy shift
        # e.g., 100 Elo points ~ 0.5 goals diff (simplified linear mapping)
        goal_diff_proxy = rating_diff / 200.0

        # 3. Incorporate specific attack/defense if available (fallback to 1.0 multiplier)
        home_attack = features.get("home_attack_strength", 1.0)
        away_attack = features.get("away_attack_strength", 1.0)
        home_defense = features.get(
            "home_defense_weakness", 1.0
        )  # >1 means weak defense
        away_defense = features.get("away_defense_weakness", 1.0)

        # Blend approaches
        # If we have specific attack/def, use them. Otherwise rely on overall rating diff.
        if "home_attack_strength" in features and "away_defense_weakness" in features:
            # Multiplicative model proxy
            home_strength = home_attack * away_defense
            away_strength = away_attack * home_defense
        else:
            # Rating diff model
            # Base home share is (base_total / 2) + home_advantage
            # Then we shift it by goal_diff_proxy
            # This is a very rough proxy just to get us a number
            home_share = 0.5 + (goal_diff_proxy / base_total) if base_total > 0 else 0.5
            # Bound the share
            home_share = max(0.1, min(0.9, home_share))
            away_share = 1.0 - home_share

            home_strength = home_share * 2.0  # center around 1.0
            away_strength = away_share * 2.0

        return home_strength, away_strength, base_total
