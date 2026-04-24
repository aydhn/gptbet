import pytest
from sports_signal_bot.ratings.timeline import RatingTimelineProcessor
from sports_signal_bot.ratings.elo import EloRatingEngine
from sports_signal_bot.ratings.contracts import RatingConfig, TeamRatingState
from sports_signal_bot.core.constants import SportType

def test_season_transition_carryover():
    config = RatingConfig(base_rating=1500.0, season_carryover=0.5, scope_mode="sport_league_season")
    processor = RatingTimelineProcessor(EloRatingEngine(config), config)

    # Simulate end of season 1
    s1_state_good = TeamRatingState(team_id="A", sport=SportType.FOOTBALL, league="L", season="S1", current_rating=1600.0)
    s1_state_bad = TeamRatingState(team_id="B", sport=SportType.FOOTBALL, league="L", season="S1", current_rating=1400.0)

    processor.apply_season_transition([s1_state_good, s1_state_bad], "S2")

    s2_good = processor.get_latest_state("A", "football", "L", "S2")
    s2_bad = processor.get_latest_state("B", "football", "L", "S2")

    assert s2_good.current_rating == 1550.0 # 1500 + 100 * 0.5
    assert s2_bad.current_rating == 1450.0  # 1500 - 100 * 0.5
    assert s2_good.matches_played == 0
