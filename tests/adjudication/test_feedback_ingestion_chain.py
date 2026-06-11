import pytest

from sports_signal_bot.adjudication.contracts import ResolutionRecord
from sports_signal_bot.adjudication.feedback import FeedbackIngestor


def test_derive_feedback_signal():
    resolution = ResolutionRecord(
        resolution_id="r1",
        case_id="c1",
        resolution_family="test",
        resolution_status="applied",
        feedback_eligibility=True,
        memory_write_allowed=True,
        effective_scope="test_scope",
    )

    signal = FeedbackIngestor.derive_feedback_signal(resolution, {"k": "v"}, 0.9)
    assert signal is not None
    assert signal.confidence == 0.9
    assert FeedbackIngestor.classify_feedback_strength(signal) == "strong"

    resolution.feedback_eligibility = False
    signal_none = FeedbackIngestor.derive_feedback_signal(resolution, {"k": "v"}, 0.9)
    assert signal_none is None
