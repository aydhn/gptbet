from typing import Dict, Any, List
from sports_signal_bot.security.contracts import SecretResolutionRecord
from sports_signal_bot.security.redaction import RedactionEngine

class ConfigLayerer:
    def __init__(self, secrets_resolver):
        self.resolver = secrets_resolver

    def resolve_effective_config(self) -> Dict[str, Any]:
        """Resolve config layers in order:
        1. defaults
        2. env defaults
        3. local overrides (non-secret)
        4. local secrets
        5. env vars
        6. CLI overrides
        """
        # Mock merging for now
        config = {
            "TELEGRAM_BOT_TOKEN": self.resolver.resolve_secret("TELEGRAM_BOT_TOKEN").resolved_value or "dummy:token",
            "TELEGRAM_DECISIONS_CHAT_ID": "-100123456789",
            "SECURITY_PROFILE": self.resolver.mode,
            "ENABLE_REAL_DISPATCH": False,
            "CONFIRM_RISKY_COMMANDS": True
        }
        return config
