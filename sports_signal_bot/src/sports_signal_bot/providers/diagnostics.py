from typing import Any, Dict, List, Optional


class ProviderDiagnosticsRecord:
    def __init__(self, provider_name: str):
        self.provider_name = provider_name
        self.events: List[Dict[str, Any]] = []

    def log_event(
        self, level: str, message: str, context: Optional[Dict[str, Any]] = None
    ):
        self.events.append(
            {"level": level, "message": message, "context": context or {}}
        )


def generate_diagnostics_report(
    diagnostics: ProviderDiagnosticsRecord,
) -> Dict[str, Any]:
    return {
        "provider": diagnostics.provider_name,
        "event_count": len(diagnostics.events),
        "events": diagnostics.events,
    }
