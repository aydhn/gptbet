from typing import List
from sports_signal_bot.ecosystem_discovery.strategies.base import BaseEcosystemDiscoveryStrategy
from sports_signal_bot.ecosystem_discovery.contracts import (
    DiscoveryQueryRecord,
    DiscoveryResultRecord,
    CatalogEntryRecord
)
from sports_signal_bot.ecosystem_discovery.discovery import run_ecosystem_discovery

class NotarizedCatalogPreferenceStrategy(BaseEcosystemDiscoveryStrategy):
    def run_discovery(self, query: DiscoveryQueryRecord, available: List[CatalogEntryRecord]) -> DiscoveryResultRecord:
        allowed = [e for e in available if "notarized" in e.trust_notes]
        if not allowed:
            # Fallback
            allowed = available
        return run_ecosystem_discovery(query, allowed)
