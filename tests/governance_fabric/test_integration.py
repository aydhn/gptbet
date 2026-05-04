import pytest
from sports_signal_bot.governance_fabric.integration import run_governance_fabric_pass

def test_run_governance_fabric_pass():
    artifacts = run_governance_fabric_pass()
    assert "council" in artifacts
    assert "fabric" in artifacts
    assert "federation" in artifacts
    assert "audit_exchange" in artifacts

    assert artifacts["council"]["health_status"] == "healthy"
    assert artifacts["case"]["case_status"] in ["case_decided", "case_decided_with_caveats"]
    assert "flowed_suppressed" in artifacts["flow"]["final_signal_state"]
    assert artifacts["currentness"]["currentness_outcome"] == "projected_stale_current"
    assert artifacts["audit_decision"]["final_status"] == "capped"
