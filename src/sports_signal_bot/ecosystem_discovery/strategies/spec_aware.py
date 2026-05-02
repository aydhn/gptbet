from typing import List
from sports_signal_bot.ecosystem_discovery.strategies.base import BaseEcosystemDiscoveryStrategy
from sports_signal_bot.ecosystem_discovery.contracts import (
    DiscoveryQueryRecord,
    DiscoveryResultRecord,
    CatalogEntryRecord
)
from sports_signal_bot.ecosystem_discovery.discovery import run_ecosystem_discovery

class SpecAwareDiscoveryStrategy(BaseEcosystemDiscoveryStrategy):
    def run_discovery(self, query: DiscoveryQueryRecord, available: List[CatalogEntryRecord]) -> DiscoveryResultRecord:
        # Require spec family presence
        allowed = [e for e in available if len(e.spec_family_summary) > 0]
        return run_ecosystem_discovery(query, allowed)
