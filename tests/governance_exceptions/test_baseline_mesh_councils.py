import pytest
from sports_signal_bot.governance_exceptions.contracts import BaselineMeshCouncilRecord, BaselineCouncilCaseRecord
from sports_signal_bot.governance_exceptions.baseline_councils import build_baseline_mesh_council, open_baseline_council_case, resolve_baseline_council_case

def test_build_baseline_mesh_council():
    council = build_baseline_mesh_council("currentness_resolution_council", "quorum_policy", "precedence_policy")
    assert council.council_family == "currentness_resolution_council"
    assert council.health_status == "healthy"

def test_open_and_resolve_baseline_council_case():
    case = open_baseline_council_case("current_pointer_conflict_case", ["baseline_1"])
    assert case.case_status == "open"
    assert "baseline_1" in case.source_baseline_refs

    resolve_baseline_council_case(case)
    assert case.case_status == "resolved"
