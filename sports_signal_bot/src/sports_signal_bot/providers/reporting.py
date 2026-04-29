from typing import Any, Dict, List, Optional

from sports_signal_bot.providers.health import ProviderHealthRecord
from sports_signal_bot.providers.quality import ProviderQualityRecord


class ProviderReporter:
    def generate_summary(
        self,
        health_records: List[ProviderHealthRecord],
        quality_records: List[ProviderQualityRecord],
    ) -> Dict[str, Any]:
        return {
            "health_summary": [h.model_dump(mode="json") for h in health_records],
            "quality_summary": [q.model_dump(mode="json") for q in quality_records],
        }
