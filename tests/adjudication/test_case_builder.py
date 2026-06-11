import pytest

from sports_signal_bot.adjudication.cases import AdjudicationCaseBuilder
from sports_signal_bot.adjudication.contracts import (
    AdjudicationCaseCreationRequest, AdjudicationCaseFamily,
    AdjudicationCaseStatus, AdjudicationSeverity)


def test_build_adjudication_case():
    case = AdjudicationCaseBuilder.build_adjudication_case(
        AdjudicationCaseCreationRequest(
            case_type=AdjudicationCaseFamily.data_conflict_case,
            target_entity_type="match",
            target_entity_id="m123",
            source_component="reconciliation_engine",
            severity=AdjudicationSeverity.high,
            evidence_bundle_ref="eb_456",
        )
    )

    assert case.case_id is not None
    assert case.case_type == AdjudicationCaseFamily.data_conflict_case
    assert case.target_entity_type == "match"
    assert case.target_entity_id == "m123"
    assert case.severity == AdjudicationSeverity.high
    assert case.evidence_bundle_ref == "eb_456"
    assert case.current_status == AdjudicationCaseStatus.queued
    assert case.queue_priority.value == "high"
