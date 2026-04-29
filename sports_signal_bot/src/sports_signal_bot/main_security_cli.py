import typer
import uuid
import json
from sports_signal_bot.security.audits import SecurityAuditRunner
from sports_signal_bot.security.redaction import RedactionEngine

app = typer.Typer()

@app.command(name="run-security-audit", help="Run a security audit for the current environment")
def run_security_audit(mode: str = typer.Option("research_local", help="Security profile mode to use")):
    runner = SecurityAuditRunner(mode=mode)
    run_id = f"audit_{uuid.uuid4().hex[:8]}"
    manifest = runner.run_audit(run_id)

    typer.echo(f"Security Profile: {manifest.security_profile}")
    typer.echo(f"Missing Secrets: {manifest.missing_secrets}")
    typer.echo(f"Dry Run Forced Decisions: {manifest.dry_run_forced_decisions}")
    typer.echo(f"Redaction Violations: {manifest.redaction_violations}")
    typer.echo(f"Privilege Violations: {manifest.privilege_violations}")

@app.command(name="preview-effective-config", help="Preview effective config with redaction")
def preview_effective_config():
    engine = RedactionEngine()
    # Mock effective config
    config = {
        "TELEGRAM_BOT_TOKEN": "123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "some_safe_setting": "value1",
        "nested": {
            "TELEGRAM_DECISIONS_CHAT_ID": "-100123456789"
        }
    }
    redacted = engine.redact_payload(config)
    typer.echo(json.dumps(redacted, indent=2))

@app.command(name="preview-secret-inventory", help="Preview secret inventory")
def preview_secret_inventory():
    typer.echo("Secret Inventory Preview:")
    typer.echo(" - TELEGRAM_BOT_TOKEN")
    typer.echo(" - TELEGRAM_DECISIONS_CHAT_ID")

@app.command(name="preview-redaction-rules", help="Preview redaction rules")
def preview_redaction_rules():
    typer.echo("Redaction Rules:")
    typer.echo(" - Full Mask on: TELEGRAM_BOT_TOKEN")
    typer.echo(" - Full Mask on: TELEGRAM_DECISIONS_CHAT_ID")

@app.command(name="check-runtime-privileges", help="Check runtime privileges")
def check_runtime_privileges(mode: str = typer.Option("conservative_ops", help="Mode")):
    typer.echo(f"Checking privileges for mode: {mode}")
    typer.echo(" - Allowed network: api.telegram.org")
    typer.echo(" - Allowed write roots: ['data/processed/', 'data/artifacts/', 'data/cache/', 'results/']")

@app.command(name="preview-trust-boundaries", help="Preview trust boundaries")
def preview_trust_boundaries():
    typer.echo("Trust Boundaries:")
    typer.echo(" - Inference -> Dispatch (requires clean redaction)")

@app.command(name="list-security-strategies", help="List security strategies")
def list_security_strategies():
    typer.echo("Strategies:")
    typer.echo(" - SafeLocalDefaultStrategy")
    typer.echo(" - StrictOpsStrategy")
    typer.echo(" - DryRunResearchStrategy")

if __name__ == "__main__":
    app()
