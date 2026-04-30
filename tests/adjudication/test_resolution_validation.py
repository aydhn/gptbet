import pytest
from sports_signal_bot.adjudication.contracts import AdjudicationDecisionRecord, ResolutionType
from sports_signal_bot.adjudication.validators import AdjudicationGuardrails

def test_resolution_has_evidence():
    decision_valid = AdjudicationDecisionRecord(
        decision_id="d1",
        case_id="c1",
        operator_id="op1",
        decision_type="override",
        resolution_type=ResolutionType.override_field_value,
        resolution_payload={},
        confidence_in_resolution=1.0,
        rationale_code="evidence_found",
        operator_note="Confirmed via source",
        applied_scope="single_entity"
    )
    assert AdjudicationGuardrails.check_resolution_has_evidence(decision_valid)

    decision_invalid = AdjudicationDecisionRecord(
        decision_id="d2",
        case_id="c1",
        operator_id="op1",
        decision_type="override",
        resolution_type=ResolutionType.override_field_value,
        resolution_payload={},
        confidence_in_resolution=1.0,
        rationale_code="",
        operator_note="",
        applied_scope="single_entity"
    )
    assert not AdjudicationGuardrails.check_resolution_has_evidence(decision_invalid)
