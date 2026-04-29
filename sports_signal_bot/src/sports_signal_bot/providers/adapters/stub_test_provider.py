from datetime import datetime
from typing import Any, Dict, List, Optional

from sports_signal_bot.providers.adapters.base import ProviderAdapterBase
from sports_signal_bot.providers.contracts import (
    DataFamily,
    ProviderCapabilityRecord,
    UnifiedFixtureRecord,
)
from sports_signal_bot.providers.requests import ProviderRequestRecord
from sports_signal_bot.providers.responses import (
    ProviderQualityRecord,
    ProviderResponseRecord,
)


class StubTestProviderAdapter(ProviderAdapterBase):
    def fetch(self, request: ProviderRequestRecord) -> ProviderResponseRecord:
        res = ProviderResponseRecord(
            provider_used=self.name,
            records=[],
            quality_summary=ProviderQualityRecord(
                is_acceptable=True, overall_score=1.0
            ),
        )
        if request.data_family == DataFamily.FIXTURES:
            res.records.append(
                UnifiedFixtureRecord(
                    event_id="test_1",
                    sport=request.sport,
                    league="test_league",
                    season="2026",
                    home_team="Home",
                    away_team="Away",
                    kickoff_time=datetime.utcnow(),
                    event_status="scheduled",
                )
            )
        return res

    def validate_raw_response(self, raw_payload: Any) -> bool:
        return True

    def normalize_to_unified(
        self, raw_payload: Any, request: ProviderRequestRecord
    ) -> ProviderResponseRecord:
        return self.fetch(request)

    def emit_quality_metadata(
        self, raw_payload: Any, request: ProviderRequestRecord
    ) -> ProviderQualityRecord:
        return ProviderQualityRecord(is_acceptable=True, overall_score=1.0)

    def describe_capabilities(self) -> ProviderCapabilityRecord:
        return ProviderCapabilityRecord(
            provider_name=self.name, sport="any", data_family=DataFamily.FIXTURES
        )

    def dry_run_preview(self, request: ProviderRequestRecord) -> ProviderResponseRecord:
        return self.fetch(request)
