from datetime import datetime, timezone, timedelta
from sports_signal_bot.multi_region_fabric.treaties import build_recovery_treaty, verify_treaty_integrity

def test_build_recovery_treaty():
    expiry = datetime.now(timezone.utc) + timedelta(days=30)
    treaty = build_recovery_treaty("t1", "review_delegation_treaty", ["us-east", "eu-west"], expiry)
    assert verify_treaty_integrity(treaty)
