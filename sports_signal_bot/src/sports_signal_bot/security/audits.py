from sports_signal_bot.security.contracts import SecurityManifest
from sports_signal_bot.security.secrets import SecretResolver
from sports_signal_bot.security.redaction import RedactionEngine

class SecurityAuditRunner:
    def __init__(self, mode: str = "research_local"):
        self.mode = mode
        self.resolver = SecretResolver(mode)

    def run_audit(self, run_id: str) -> SecurityManifest:
        missing_secrets = self.resolver.check_required_secrets()
        forced_dry_run = 1 if self.resolver.should_force_dry_run() else 0

        manifest = SecurityManifest(
            run_id=run_id,
            security_profile=self.mode,
            missing_secrets=missing_secrets,
            dry_run_forced_decisions=forced_dry_run
        )
        return manifest
