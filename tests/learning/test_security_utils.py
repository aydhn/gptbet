from sports_signal_bot.learning.utils import SecurityUtils


def test_redact_sensitive_info():
    payload = {
        "id": "123",
        "type": "event",
        "secret_token": "abc",
        "operator_note": "test",
        "public_data": "ok",
    }
    allowlist = ["id", "type", "public_data"]
    redacted = SecurityUtils.redact_sensitive_info(
        payload, allowlist=allowlist
    )
    assert redacted["id"] == "123"
    assert redacted["type"] == "event"
    assert redacted["public_data"] == "ok"
    assert redacted["secret_token"] == "***REDACTED***"
    assert redacted["operator_note"] == "***REDACTED***"


def test_redact_sensitive_info_empty_allowlist():
    payload = {"id": "123", "type": "event"}
    redacted = SecurityUtils.redact_sensitive_info(payload)
    assert redacted["id"] == "***REDACTED***"
    assert redacted["type"] == "***REDACTED***"
