import pytest
from sports_signal_bot.adjudication.contracts import AdjudicationDecisionRecord, ResolutionType
from sports_signal_bot.adjudication.validators import AdjudicationGuardrails

def test_secondary_review_bypass():
    decision = AdjudicationDecisionRecord(
        decision_id="d1",
        case_id="c1",
        operator_id="op1",
        decision_type="override",
        resolution_type=ResolutionType.override_field_value,
        resolution_payload={},
        confidence_in_resolution=1.0,
        rationale_code="code",
        operator_note="note",
        applied_scope="global",
        requires_secondary_review=True,
        secondary_review_status="pending"
    )
    assert not AdjudicationGuardrails.validate_secondary_review_bypass(decision)

    decision.secondary_review_status = "approved"
    assert AdjudicationGuardrails.validate_secondary_review_bypass(decision)
