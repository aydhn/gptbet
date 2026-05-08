from src.sports_signal_bot.final_convergence_hardening import (
    build_final_convergence_matrix,
    summarize_final_convergence_matrix,
    build_final_hardening_convergence,
    build_frozen_baseline,
    build_production_readiness_review_surface,
    build_terminal_acceptance_pack,
    ConvergenceInputRecord
)

def test_matrix_build_and_summarize():
    inputs = [ConvergenceInputRecord(input_id="1", source_layer="test")]
    c = build_final_hardening_convergence("final_readiness_convergence", inputs)
    b = build_frozen_baseline("release_gating_baseline", [], [])
    r = build_production_readiness_review_surface("release_readiness_review_surface", [])
    a = build_terminal_acceptance_pack("final_readiness_acceptance_pack", [])

    matrix = build_final_convergence_matrix(c, b, r, a)
    assert len(matrix) == 4

    summary = summarize_final_convergence_matrix(matrix)
    assert summary["surfaces_evaluated"] == 4
    assert summary["all_verified"] == True
