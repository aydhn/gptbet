from typing import Any, Dict


class PaceMapper:
    """Maps pace and tempo variables into expected point adjustments."""

    @staticmethod
    def calculate_pace_adjustment(
        features: Dict[str, Any], base_possessions: float = 100.0
    ) -> float:
        """
        Calculates a simple pace adjustment proxy.
        If 'home_pace' and 'away_pace' are provided, blends them.
        Assumes average points per possession ~ 1.1 if not specified.
        Returns point adjustment relative to base.
        """
        home_pace = features.get("home_pace")
        away_pace = features.get("away_pace")
        league_pace = features.get("league_avg_pace", base_possessions)
        points_per_possession = features.get("league_ppp", 1.1)

        if home_pace is not None and away_pace is not None:
            # Simple average of paces (could be more complex, e.g. Pythagorean or weighted)
            combined_pace = (home_pace + away_pace) / 2.0

            # Additional recent tempo shift if available
            recent_shift = features.get("recent_tempo_shift", 0.0)
            combined_pace += recent_shift

            # Fatigue modifier (e.g. back-to-back might reduce pace slightly)
            fatigue_modifier = features.get("fatigue_pace_modifier", 1.0)
            combined_pace *= fatigue_modifier

            # Difference from league average translated to points
            pace_diff = combined_pace - league_pace

            # Since total points is roughly (pace * ppp * 2 teams),
            # the adjustment to the total is (pace_diff * ppp * 2)
            return pace_diff * points_per_possession * 2.0

        return 0.0
