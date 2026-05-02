from typing import List
from sports_signal_bot.ecosystem_discovery.strategies.base import BaseEcosystemDiscoveryStrategy
from sports_signal_bot.ecosystem_discovery.contracts import (
    DiscoveryQueryRecord,
    DiscoveryResultRecord,
    CatalogEntryRecord
)
from sports_signal_bot.ecosystem_discovery.discovery import run_ecosystem_discovery

class ProtocolStrictSubsetStrategy(BaseEcosystemDiscoveryStrategy):
    def run_discovery(self, query: DiscoveryQueryRecord, available: List[CatalogEntryRecord]) -> DiscoveryResultRecord:
        return run_ecosystem_discovery(query, available)
