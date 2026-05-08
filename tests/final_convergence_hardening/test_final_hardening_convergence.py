from src.sports_signal_bot.final_convergence_hardening import (
    build_final_hardening_convergence,
    ConvergenceInputRecord,
    verify_final_hardening_convergence
)

def test_convergence_build_and_verify():
    inputs = [ConvergenceInputRecord(input_id="1", source_layer="test", is_stale=False)]
    convergence = build_final_hardening_convergence("final_readiness_convergence", inputs)
    assert convergence.convergence_status == "convergence_verified"
    assert verify_final_hardening_convergence(convergence)

def test_stale_input_blocks_convergence():
    inputs = [ConvergenceInputRecord(input_id="1", source_layer="test", is_stale=True)]
    convergence = build_final_hardening_convergence("final_readiness_convergence", inputs)
    assert convergence.convergence_status == "convergence_blocked"
    assert not verify_final_hardening_convergence(convergence)
