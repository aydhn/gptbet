from typing import Any, Dict, List, Optional


class SecurityUtils:
    @staticmethod
    def redact_sensitive_info(
        payload: Dict[str, Any], allowlist: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Redacts sensitive information by only allowing permitted keys."""
        if allowlist is None:
            allowlist = []

        redacted = {}
        for key, value in payload.items():
            if key in allowlist:
                redacted[key] = value
            else:
                redacted[key] = "***REDACTED***"
        return redacted
