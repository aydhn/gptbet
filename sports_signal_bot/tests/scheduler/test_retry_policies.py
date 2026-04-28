from sports_signal_bot.scheduler.retries import decide_retry_action

def test_decide_retry_action():
    # No retry policy
    rec = decide_retry_action("job", 1, "no_retry", "ConnectionError", "fam")
    assert rec.will_retry == False

    # Immediate retry
    rec = decide_retry_action("job", 1, "immediate_retry_once", "ConnectionError", "fam")
    assert rec.will_retry == True
    assert rec.delay_seconds == 0

    # Bounded retry backoff
    rec = decide_retry_action("job", 2, "bounded_retry_with_backoff", "ConnectionError", "fam")
    assert rec.will_retry == True
    assert rec.delay_seconds == 60 # 30 * 2^(2-1)

    # Fatal error
    rec = decide_retry_action("job", 1, "bounded_retry_with_backoff", "ValidationError", "fam")
    assert rec.will_retry == False
