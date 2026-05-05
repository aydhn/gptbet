import pytest
from sports_signal_bot.concurrency_hardening.integration import run_concurrency_hardening_pass

def test_run_concurrency_hardening_pass():
    result = run_concurrency_hardening_pass()
    assert "manifests" in result
    assert "overall_health" in result
    assert "guards" in result["manifests"]
    assert "regressions" in result["manifests"]
