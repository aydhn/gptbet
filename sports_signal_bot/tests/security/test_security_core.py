from sports_signal_bot.security.redaction import RedactionEngine
from sports_signal_bot.security.secrets import SecretResolver
from sports_signal_bot.security.endpoints import EndpointAllowlist
from sports_signal_bot.security.filesystem import FilesystemAllowlist
from sports_signal_bot.security.command_gates import CommandSafetyGate

def test_redaction_engine_nested_payloads():
    engine = RedactionEngine()
    payload = {
        "event_id": "123",
        "config": {
            "TELEGRAM_BOT_TOKEN": "secret_123",
            "TELEGRAM_DECISIONS_CHAT_ID": "-1001"
        }
    }
    redacted = engine.redact_payload(payload)
    assert redacted["config"]["TELEGRAM_BOT_TOKEN"] == "***REDACTED***"
    assert redacted["config"]["TELEGRAM_DECISIONS_CHAT_ID"] == "***REDACTED***"
    assert redacted["event_id"] == "123"

def test_missing_required_secret_fail_safe():
    resolver = SecretResolver(mode="production")
    missing = resolver.check_required_secrets()
    # Assuming TELEGRAM_BOT_TOKEN isn't in env during test
    assert "TELEGRAM_BOT_TOKEN" in missing
    assert resolver.should_force_dry_run() == True

def test_endpoint_allowlist():
    allowlist = EndpointAllowlist()
    assert allowlist.validate_outbound_endpoint("https://api.telegram.org/bot123") == True
    assert allowlist.validate_outbound_endpoint("https://evil.com/data") == False

def test_filesystem_allowlist():
    allowlist = FilesystemAllowlist()
    assert allowlist.validate_write_path("data/processed/file.txt") == True
    assert allowlist.validate_write_path("/etc/passwd") == False

def test_risky_command_confirmation():
    gate = CommandSafetyGate()
    assert gate.check_command_safety("run-dispatch", mode="production", confirm=False) == False
    assert gate.check_command_safety("run-dispatch", mode="production", confirm=True) == True
    assert gate.check_command_safety("run-dispatch", mode="dry_run_preview", confirm=False) == True
