import os
from typing import Dict, List, Optional
from sports_signal_bot.security.contracts import SecretResolutionRecord

class SecretResolver:
    def __init__(self, mode: str = "research_local"):
        self.mode = mode
        # Dummy config mappings for demonstration
        self.required_secrets = {
            "production": ["TELEGRAM_BOT_TOKEN"],
            "research_local": [],
            "dry_run_preview": []
        }.get(mode, [])

    def resolve_secret(self, secret_name: str) -> SecretResolutionRecord:
        val = os.environ.get(secret_name)
        if val:
            return SecretResolutionRecord(
                secret_name=secret_name,
                resolved_source="env",
                resolved_value=val,
                is_placeholder=val == "" or "dummy" in val.lower()
            )

        # Mock .env resolution
        # We would use python-dotenv here ideally
        return SecretResolutionRecord(
            secret_name=secret_name,
            resolved_source="none",
            error="Secret not found"
        )

    def check_required_secrets(self) -> List[str]:
        missing = []
        for secret in self.required_secrets:
            res = self.resolve_secret(secret)
            if res.error or res.is_placeholder:
                missing.append(secret)
        return missing

    def should_force_dry_run(self) -> bool:
        return len(self.check_required_secrets()) > 0
