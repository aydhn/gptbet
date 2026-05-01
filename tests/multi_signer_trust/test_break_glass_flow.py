from datetime import datetime, timedelta
from sports_signal_bot.multi_signer_trust.break_glass import issue_break_glass_exception, validate_break_glass_eligibility
from sports_signal_bot.multi_signer_trust.contracts import BreakGlassRecord

def test_break_glass_issue_and_validate():
    bg = issue_break_glass_exception("ref1", "emergency", "user1")
    assert bg.is_active == True

    assert validate_break_glass_eligibility(bg, "emergency_override") == True
    assert validate_break_glass_eligibility(bg, "other_family") == False

    # Force expire
    bg.expiry.expires_at = datetime.utcnow() - timedelta(hours=1)
    assert validate_break_glass_eligibility(bg, "emergency_override") == False
