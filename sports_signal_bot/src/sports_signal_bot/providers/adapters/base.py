from typing import Any, Dict, List, Optional

from sports_signal_bot.providers.contracts import ProviderCapabilityRecord
from sports_signal_bot.providers.requests import ProviderRequestRecord
from sports_signal_bot.providers.responses import (
    ProviderQualityRecord,
    ProviderResponseRecord,
)


class ProviderAdapterBase:
    def __init__(self, name: str, config: Dict[str, Any] = None):
        self.name = name
        self.config = config or {}

    def fetch(self, request: ProviderRequestRecord) -> ProviderResponseRecord:
        raise NotImplementedError

    def validate_raw_response(self, raw_payload: Any) -> bool:
        raise NotImplementedError

    def normalize_to_unified(
        self, raw_payload: Any, request: ProviderRequestRecord
    ) -> ProviderResponseRecord:
        raise NotImplementedError

    def emit_quality_metadata(
        self, raw_payload: Any, request: ProviderRequestRecord
    ) -> ProviderQualityRecord:
        raise NotImplementedError

    def describe_capabilities(self) -> ProviderCapabilityRecord:
        raise NotImplementedError

    def dry_run_preview(self, request: ProviderRequestRecord) -> ProviderResponseRecord:
        raise NotImplementedError
