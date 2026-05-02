from typing import List
from sports_signal_bot.ecosystem_discovery.strategies.base import BaseEcosystemDiscoveryStrategy
from sports_signal_bot.ecosystem_discovery.contracts import (
    DiscoveryQueryRecord,
    DiscoveryResultRecord,
    CatalogEntryRecord
)
from sports_signal_bot.ecosystem_discovery.discovery import run_ecosystem_discovery

class ConservativeEcosystemDiscoveryStrategy(BaseEcosystemDiscoveryStrategy):
    def run_discovery(self, query: DiscoveryQueryRecord, available: List[CatalogEntryRecord]) -> DiscoveryResultRecord:
        # Filter for only local available
        safe = [e for e in available if e.availability_status == "available_local"]
        return run_ecosystem_discovery(query, safe)
