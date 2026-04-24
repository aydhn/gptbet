import pytest
from sports_signal_bot.data.validators.schema_validator import RequiredFieldsValidator, UniqueEventValidator, HomeAwayValidator
from sports_signal_bot.data.validators.odds_validator import OddsSanityValidator

def test_required_fields_validator():
    validator = RequiredFieldsValidator(["event_id", "sport"])
    records = [
        {"event_id": "1", "sport": "football"},
        {"sport": "football"},  # missing event_id
        {"event_id": "2"}       # missing sport
    ]
    valid, issues = validator.validate(records)
    assert len(valid) == 1
    assert len(issues) == 2

def test_unique_event_validator():
    validator = UniqueEventValidator("event_id")
    records = [
        {"event_id": "1"},
        {"event_id": "1"},  # duplicate
        {"event_id": "2"}
    ]
    valid, issues = validator.validate(records)
    assert len(valid) == 2
    assert len(issues) == 1

def test_home_away_validator():
    validator = HomeAwayValidator()
    records = [
        {"home_team": "A", "away_team": "B"},
        {"home_team": "A", "away_team": "A"}  # invalid
    ]
    valid, issues = validator.validate(records)
    assert len(valid) == 1
    assert len(issues) == 1

def test_odds_sanity_validator():
    validator = OddsSanityValidator()
    records = [
        {"decimal_odds": 1.5},
        {"decimal_odds": 0.5},  # invalid
        {"decimal_odds": -1.0}, # invalid
        {"decimal_odds": "invalid"} # invalid
    ]
    valid, issues = validator.validate(records)
    assert len(valid) == 1
    assert len(issues) == 3
