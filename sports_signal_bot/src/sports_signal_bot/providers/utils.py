from typing import Any, Dict, List, Optional


def redact_sensitive_params(params: Dict[str, Any]) -> Dict[str, Any]:
    redacted = {}
    for k, v in params.items():
        if "token" in k.lower() or "secret" in k.lower() or "key" in k.lower():
            redacted[k] = "***REDACTED***"
        else:
            redacted[k] = v
    return redacted
