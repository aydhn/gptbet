import pytest
from sports_signal_bot.distributed_coordination.councils import FederatedCouncilManager
from sports_signal_bot.distributed_coordination.arbitration import ArbitrationEngine
from sports_signal_bot.distributed_coordination.contracts import CouncilVoteRecord

def test_federated_arbitration_council():
    council_mgr = FederatedCouncilManager()
    engine = ArbitrationEngine()

    case = council_mgr.open_council_case("council_1", "contention_1")
    assert case.status == "open"

    votes = council_mgr.collect_council_positions(case.case_id, ["node_1", "node_2", "node_3"], default_position="serialize_across_nodes")
    assert len(votes) == 3

    # Let's adjust one vote to test simple logic
    votes[0].position = "reserve_for_rollback_clusterwide"

    precedence_rules = {"rollback_binding_contention": 1}
    outcome = engine.apply_council_precedence(votes, precedence_rules)
    assert outcome == "serialize_across_nodes" # Since 2 out of 3 voted for this

    decision = engine.finalize_council_decision(case.case_id, outcome, "Majority rules")
    assert decision.outcome == "serialize_across_nodes"

    resolved = engine.resolve_clusterwide_precedence("rollback_binding_contention")
    assert resolved == "reserve_for_rollback_clusterwide"
