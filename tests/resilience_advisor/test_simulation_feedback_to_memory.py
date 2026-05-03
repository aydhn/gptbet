from sports_signal_bot.resilience_advisor.feedback import summarize_feedback_loop_effect

def test_feedback():
    assert "Feedback loop integrated." in summarize_feedback_loop_effect()
