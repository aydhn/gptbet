import pytest

from sports_signal_bot.adjudication.cases import AdjudicationCaseBuilder
from sports_signal_bot.adjudication.contracts import (
    AdjudicationCaseCreationRequest, AdjudicationCaseFamily,
    AdjudicationCaseRecord, AdjudicationSeverity, KnowledgeScopeRecord,
    KnowledgeScopeType, PrecedentRecord)
from sports_signal_bot.adjudication.precedents import (PrecedentLookupEngine,
                                                       PrecedentRegistry)


def test_precedent_lookup():
    registry = PrecedentRegistry()
    engine = PrecedentLookupEngine(registry)

    case = AdjudicationCaseBuilder.build_adjudication_case(
        AdjudicationCaseCreationRequest(
            case_type=AdjudicationCaseFamily.data_conflict_case,
            target_entity_type="match",
            target_entity_id="m1",
            source_component="test",
            severity=AdjudicationSeverity.low,
            evidence_bundle_ref="eb1",
        )
    )

    fp = engine.fingerprint_case(case)

    prec = PrecedentRecord(
        precedent_id="p1",
        precedent_title="Test Precedent",
        case_family=AdjudicationCaseFamily.data_conflict_case,
        pattern_signature=fp,
        applicable_scope=KnowledgeScopeRecord(
            scope_type=KnowledgeScopeType.single_entity, target_value="m1"
        ),
        confidence_band="high",
        created_from_case="c0",
        created_by_operator="op1",
        validity_window="30d",
        review_status="active",
    )
    registry.register_precedent(prec)

    matches = engine.find_matching_precedents(case)
    assert len(matches) == 1
    assert matches[0].precedent_id == "p1"
