from typing import List, Dict, Any

class SecurityUtils:
    @staticmethod
    def redact_sensitive_info(payload: Dict[str, Any]) -> Dict[str, Any]:
        """Redacts sensitive information like internal IDs or operator notes."""
        redacted = payload.copy()
        for key in list(redacted.keys()):
            if any(term in key.lower() for term in ["note", "internal", "secret", "operator"]):
                redacted[key] = "***REDACTED***"
        return redacted
