from src.sports_signal_bot.geo_quorum_hardening.integration import run_hardening_pass
import os

def test_run_hardening_pass():
    manifest = run_hardening_pass("conservative")
    assert manifest["overall_status"] == "healthy"
    assert os.path.exists("out/geo_quorum_hardening/geo_quorum_hardening_manifest.json")
    assert os.path.exists("out/geo_quorum_hardening/geo_quorum_hardening_health_report.json")
