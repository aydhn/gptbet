from src.sports_signal_bot.continuity_arbitration_hardening.contracts import VisibilityLedgerSuppressionRecord
from src.sports_signal_bot.continuity_arbitration_hardening.visibility_ledgers import build_worldwide_visibility_ledger

def test_build_worldwide_visibility_ledger_clean():
    ledger = build_worldwide_visibility_ledger("test_ledger", [], [])
    assert ledger.ledger_status == "ledger_verified"

def test_build_worldwide_visibility_ledger_suppressed():
    suppressions = [VisibilityLedgerSuppressionRecord(suppression_id="1", reason="test")]
    ledger = build_worldwide_visibility_ledger("test_ledger", [], suppressions)
    assert ledger.ledger_status == "ledger_caveated"
