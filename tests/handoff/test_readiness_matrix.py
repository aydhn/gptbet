from sports_signal_bot.handoff.matrix import build_readiness_matrix, classify_readiness_outcome, validate_matrix_completeness
from sports_signal_bot.handoff.contracts import ReadinessBand

def test_build_readiness_matrix():
    context = {
        "simulation_score": 0.95,
        "gates_clean": True,
        "approvals_complete": True,
        "evidence_score": 0.9,
        "stability_score": 1.0,
        "rollback_ready": True
    }
    matrix = build_readiness_matrix(context)
    assert validate_matrix_completeness(matrix)
    assert matrix["simulation"]["band"] == ReadinessBand.PASS
    assert matrix["gates"]["band"] == ReadinessBand.PASS

def test_classify_readiness_outcome():
    context = {
        "simulation_score": 0.5, # FAIL
        "gates_clean": True,
        "approvals_complete": True,
        "evidence_score": 0.9,
        "stability_score": 1.0,
        "rollback_ready": True
    }
    matrix = build_readiness_matrix(context)
    assert classify_readiness_outcome(matrix) == ReadinessBand.FAIL
