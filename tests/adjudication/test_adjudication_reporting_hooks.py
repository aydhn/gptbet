import pytest
from sports_signal_bot.adjudication.reporting import AdjudicationReporter
from sports_signal_bot.adjudication.cases import AdjudicationCaseBuilder
from sports_signal_bot.adjudication.contracts import AdjudicationCaseFamily, AdjudicationSeverity, AdjudicationCaseStatus

def test_summarize_state():
    case = AdjudicationCaseBuilder.build_adjudication_case(
        case_type=AdjudicationCaseFamily.data_conflict_case,
        target_entity_type="match",
        target_entity_id="m1",
        source_component="test",
        severity=AdjudicationSeverity.critical,
        evidence_bundle_ref="eb1"
    )
    case.current_status = AdjudicationCaseStatus.queued

    summary = AdjudicationReporter.summarize_adjudication_state([case], [])
    assert summary.open_cases == 1
    assert summary.urgent_backlog_count == 1
    assert summary.cases_by_type["data_conflict_case"] == 1
