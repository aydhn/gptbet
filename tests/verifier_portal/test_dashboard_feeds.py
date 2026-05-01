from sports_signal_bot.verifier_portal.feeds import build_dashboard_feed, redact_feed_for_profile

def test_build_dashboard_feed():
    feed = build_dashboard_feed("test_family", [{"data": "test"}])
    assert feed.feed_family == "test_family"
    assert len(feed.content) == 1

def test_redact_feed_for_profile():
    feed = build_dashboard_feed("test_family", [{"data": "test", "signer_metadata": "secret"}])

    redacted = redact_feed_for_profile(feed, "public_viewer")
    assert redacted.content[0]["signer_metadata"] == "[REDACTED]"
