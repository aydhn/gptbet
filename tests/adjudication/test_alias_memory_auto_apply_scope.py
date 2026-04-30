import pytest
from sports_signal_bot.adjudication.contracts import ResolutionRecord
from sports_signal_bot.adjudication.feedback import FeedbackLoopIntegrator

def test_alias_memory():
    resolution = ResolutionRecord(
        resolution_id="r1",
        case_id="c1",
        resolution_family="alias_resolution",
        resolution_status="applied",
        feedback_eligibility=True,
        memory_write_allowed=True,
        effective_scope="sport_specific"
    )

    mem = FeedbackLoopIntegrator.build_alias_resolution_memory(resolution, "team_a", "team_b", "mapped_id")
    assert mem["entity_a"] == "team_a"
    assert mem["resolved_identity"] == "mapped_id"
