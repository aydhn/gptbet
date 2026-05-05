import pytest
from sports_signal_bot.chaos_hardening.contracts import RecoveryHonestyValidationRecord

def test_recovery_honesty():
    honesty = RecoveryHonestyValidationRecord(validation_id="val-1", claims=[])
    assert honesty.validation_id == "val-1"
