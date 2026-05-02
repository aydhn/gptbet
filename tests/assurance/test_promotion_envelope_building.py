import pytest
from sports_signal_bot.assurance.integration import run_assurance_pipeline_for_target

def test_promotion_envelope_success_flow():
    result = run_assurance_pipeline_for_target("test_target_01")
    assert result["evaluation_passed"] is True
    assert result["envelope"]["final_assurance_decision"] == "assurance_ready"
    assert len(result["claims"]) == 4
    assert len(result["bundle"]["evidence_refs"]) > 0

def test_envelope_has_validity_window():
    result = run_assurance_pipeline_for_target("test_target_02")
    env = result["envelope"]
    assert "validity_window" in env
    assert env["validity_window"]["valid_from"] is not None
