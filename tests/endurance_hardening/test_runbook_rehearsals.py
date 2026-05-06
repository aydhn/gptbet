from sports_signal_bot.endurance_hardening.rehearsals import run_runbook_rehearsal
from sports_signal_bot.endurance_hardening.runbooks import build_runbook_record

def test_run_runbook_rehearsal():
    rb = build_runbook_record("rb_1", "test_family")
    reh = run_runbook_rehearsal(rb)
    assert reh.rehearsal_id == "rehearsal_rb_1"
    assert reh.status == "completed"
