from src.sports_signal_bot.geo_quorum_hardening.budgets import summarize_geo_quorum_budgets

def test_summarize_geo_quorum_budgets():
    record = summarize_geo_quorum_budgets({"quorum_erosion_breach": True})
    assert record.status == "degraded"
    assert "Quorum erosion budget breached." in record.warnings
