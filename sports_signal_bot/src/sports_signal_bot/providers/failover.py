from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from sports_signal_bot.providers.requests import ProviderRequestRecord
from sports_signal_bot.providers.responses import ProviderResponseRecord


class ProviderFailoverRecord(BaseModel):
    original_provider: str
    fallback_provider: Optional[str] = None
    reason: str
    action_taken: str
    successful: bool = False


def should_failover(
    response: Optional[ProviderResponseRecord], error: Optional[Exception] = None
) -> bool:
    if error is not None:
        return True
    if response is None:
        return True
    if response.quality_summary and not response.quality_summary.is_acceptable:
        return True
    if response.partial_data_flag:
        return False  # Accept partial data might be configured
    return False


def classify_failover_reason(
    response: Optional[ProviderResponseRecord], error: Optional[Exception] = None
) -> str:
    if error:
        return f"Exception: {type(error).__name__}"
    if not response:
        return "Empty or None response"
    if response.quality_summary and not response.quality_summary.is_acceptable:
        return "Quality below threshold"
    return "Unknown"


def resolve_failover_sequence(primary: str, config: Dict[str, Any]) -> List[str]:
    sequences = config.get("failover_sequences", {})
    return sequences.get(primary, [])


def execute_provider_failover(
    request: ProviderRequestRecord, current_provider: str, failover_sequence: List[str]
) -> str:
    # Placeholder for actual failover execution logic
    if failover_sequence:
        return failover_sequence[0]
    return ""


def summarize_failover_path(
    failover_records: List[ProviderFailoverRecord],
) -> List[str]:
    return [
        f"{r.original_provider}->{r.fallback_provider} ({r.reason})"
        for r in failover_records
    ]


class ProviderFailoverEngine:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}

    def get_next_provider(self, primary: str, attempt: int) -> Optional[str]:
        sequence = resolve_failover_sequence(primary, self.config)
        if attempt < len(sequence):
            return sequence[attempt]
        return None
