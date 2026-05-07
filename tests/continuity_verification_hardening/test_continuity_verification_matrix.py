import pytest
from sports_signal_bot.continuity_verification_hardening.summaries import (
    build_continuity_verification_matrix,
    summarize_continuity_verification_matrix
)

def test_build_and_summarize_matrix():
    matrix = build_continuity_verification_matrix(
        [{"id": "fed_1"}],
        [{"id": "lane_1"}],
        [{"id": "council_1"}],
        [{"id": "exchange_1"}]
    )
    summary = summarize_continuity_verification_matrix(matrix)
    assert summary["total_federations"] == 1
    assert summary["total_lanes"] == 1
    assert summary["total_councils"] == 1
    assert summary["total_exchanges"] == 1
