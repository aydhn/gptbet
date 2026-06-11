import pytest

from sports_signal_bot.adjudication.contracts import ResolutionRecord
from sports_signal_bot.adjudication.feedback import FeedbackLoopIntegrator


def test_provider_damping():
    assert FeedbackLoopIntegrator.prevent_small_sample_overreaction(4, threshold=5)
    assert not FeedbackLoopIntegrator.prevent_small_sample_overreaction(5, threshold=5)

    res = ResolutionRecord(
        resolution_id="r1",
        case_id="c1",
        resolution_family="provider_trust",
        resolution_status="applied",
        feedback_eligibility=True,
        memory_write_allowed=False,
        effective_scope="provider_family",
    )
    fb = FeedbackLoopIntegrator.derive_provider_feedback_from_resolution(res, "prov_x")
    assert (
        fb["penalized"] is False
    )  # resolution_family is provider_trust, but penalize is not in it directly, "penalize_provider_for_family" would be true.

    # Modify to make it true
    res.resolution_family = "penalize_provider"
    fb2 = FeedbackLoopIntegrator.derive_provider_feedback_from_resolution(res, "prov_x")
    assert fb2["penalized"] is True
