from sports_signal_bot.approvals.acknowledgements import acknowledge_alert, summarize_unacked_criticals

def test_acknowledge_flow():
    ack = acknowledge_alert("alarm_1", "op1", "I see it")
    assert ack.alarm_id == "alarm_1"
    assert ack.resolved is False

    ack2 = acknowledge_alert("alarm_2", "op1", "Fixed", resolved=True)

    summary = summarize_unacked_criticals([ack, ack2], total_critical=3)
    assert summary.unacked_critical_alarms == 2
