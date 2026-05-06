from sports_signal_bot.operational_hardening.recovery_checkpoints import create_recovery_checkpoint

def test_create_recovery_checkpoint():
    assert create_recovery_checkpoint() == {"status": "checkpoint_created"}
