import pytest
from datetime import datetime
from sports_signal_bot.ratings.benchmark import RatingBenchmarkEngine
from sports_signal_bot.markets.definitions import MarketDefinition
from sports_signal_bot.core.constants import SportType, MarketType
from sports_signal_bot.ratings.contracts import RatingSnapshotRecord

def test_rating_benchmark_football_1x2():
    engine = RatingBenchmarkEngine()
    market = MarketDefinition(sport=SportType.FOOTBALL, market_type=MarketType.MATCH_ODDS, possible_outcomes=["1", "X", "2"], settlement_rule_name="", selection_schema=[], required_inputs=[])

    snapshot = RatingSnapshotRecord(
        event_id="e1", sport=SportType.FOOTBALL, league="L", season="S",
        event_datetime_utc=datetime.utcnow(), home_team_id="A", away_team_id="B",
        pre_home_rating=1600.0, pre_away_rating=1500.0,
        expected_home_score=0.64, expected_away_score=0.36
    )

    ctx = {"rating_snapshots": [snapshot]}
    pred = engine.generate_prediction("e1", market, ctx)

    assert pred.predicted_class in ["1", "X", "2"]
    assert "1" in pred.predicted_probabilities
    assert "X" in pred.predicted_probabilities

    # Due to rating diff, Home should have higher prob than Away
    assert pred.predicted_probabilities["1"] > pred.predicted_probabilities["2"]

def test_rating_benchmark_basketball_moneyline():
    engine = RatingBenchmarkEngine()
    market = MarketDefinition(sport=SportType.BASKETBALL, market_type=MarketType.MONEYLINE, possible_outcomes=["1", "2"], settlement_rule_name="", selection_schema=[], required_inputs=[])

    snapshot = RatingSnapshotRecord(
        event_id="e1", sport=SportType.BASKETBALL, league="L", season="S",
        event_datetime_utc=datetime.utcnow(), home_team_id="A", away_team_id="B",
        pre_home_rating=1400.0, pre_away_rating=1600.0,
        expected_home_score=0.24, expected_away_score=0.76
    )

    ctx = {"rating_snapshots": [snapshot]}
    pred = engine.generate_prediction("e1", market, ctx)

    assert pred.predicted_class == "2" # Away strongly favored
    assert "X" not in pred.predicted_probabilities
    assert round(pred.predicted_probabilities["1"] + pred.predicted_probabilities["2"], 5) == 1.0
