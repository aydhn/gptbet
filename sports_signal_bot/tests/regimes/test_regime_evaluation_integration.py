import pytest

from sports_signal_bot.evaluation.contracts import LeaderboardRow
from sports_signal_bot.regimes.contracts import EventRegimeRecord
from sports_signal_bot.regimes.evaluation_integration import (
    build_regime_leaderboard, compare_sources_within_regime)


def test_build_regime_leaderboard():
    records = [
        EventRegimeRecord(
            event_id="1",
            sport="f",
            regime_family="form",
            regime_label="hot",
            assignment_method="rule",
        ),
        EventRegimeRecord(
            event_id="2",
            sport="f",
            regime_family="form",
            regime_label="hot",
            assignment_method="rule",
        ),
    ]

    def dummy_eval(events):
        return [
            LeaderboardRow(
                rank=1,
                source_name="A",
                source_family="A",
                sport="f",
                market_type="x",
                row_count=len(events),
                coverage_rate=1.0,
            )
        ]

    leaderboards = build_regime_leaderboard(records, dummy_eval, "form")
    assert "hot" in leaderboards
    assert leaderboards["hot"][0].row_count == 2


def test_compare_sources_within_regime():
    records = [
        EventRegimeRecord(
            event_id="1",
            sport="f",
            regime_family="form",
            regime_label="hot",
            assignment_method="rule",
        ),
        EventRegimeRecord(
            event_id="2",
            sport="f",
            regime_family="form",
            regime_label="cold",
            assignment_method="rule",
        ),
    ]

    def dummy_compare(events):
        return len(events)

    result = compare_sources_within_regime(records, dummy_compare, "form", "hot")
    assert result == 1
